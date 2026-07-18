import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid, formatdate
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# Resend (https://resend.com) — the preferred transactional-email provider:
# far better deliverability than a personal Gmail, a simple HTTP API (no SMTP /
# app-password hassle), and a free tier (~3000/month). Set RESEND_API_KEY to
# enable it; RESEND_FROM defaults to Resend's shared test sender (which only
# delivers to the account owner until you verify your own domain).
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_FROM = os.environ.get("RESEND_FROM", "Ilm AI <onboarding@resend.dev>")

# Brevo (https://brevo.com) — HTTP email API (port 443). This is the provider
# that WORKS on Render's free tier, which blocks outbound SMTP ports (25/465/587)
# so Gmail SMTP fails with "Network is unreachable". Free tier ~300/day, and you
# can send to any recipient after verifying a single sender email (no domain
# needed). BREVO_FROM_EMAIL must be a Brevo-verified sender (defaults to the
# Gmail address for convenience).
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
BREVO_FROM_EMAIL = os.environ.get("BREVO_FROM_EMAIL", GMAIL_ADDRESS or "")
BREVO_FROM_NAME = os.environ.get("BREVO_FROM_NAME", "Ilm AI")


def is_email_configured() -> bool:
    return bool(BREVO_API_KEY or RESEND_API_KEY or (GMAIL_ADDRESS and GMAIL_APP_PASSWORD))


def _send_via_brevo(to_email: str, subject: str, html: str, text: str) -> bool:
    import requests

    resp = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json", "accept": "application/json"},
        json={
            "sender": {"email": BREVO_FROM_EMAIL, "name": BREVO_FROM_NAME},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": html,
            "textContent": text,
        },
        timeout=15,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Brevo API {resp.status_code}: {resp.text[:200]}")
    return True


def _send_via_resend(to_email: str, subject: str, html: str, text: str) -> bool:
    import requests

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
        json={"from": RESEND_FROM, "to": [to_email], "subject": subject, "html": html, "text": text},
        timeout=15,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Resend API {resp.status_code}: {resp.text[:200]}")
    return True


def _render(code: str, intro_html: str, intro_text: str) -> tuple[str, str]:
    """Build the (html, plain-text) bodies for a verification-code email."""
    html = f"""
    <div style="font-family: -apple-system, Segoe UI, Roboto, sans-serif; max-width: 480px; margin: 0 auto;">
      <div style="text-align: center; padding: 24px 0 8px;">
        <div style="display: inline-block; width: 56px; height: 56px; background: #1a1a3e; border-radius: 14px; position: relative;">
          <div style="width: 22px; height: 22px; background: #f59e0b; transform: rotate(45deg); border-radius: 4px; position: absolute; top: 17px; left: 17px;"></div>
        </div>
        <div style="margin-top: 10px; font-size: 22px;"><span style="color:#1f2937;font-weight:300;">Ilm </span><span style="color:#f59e0b;font-weight:800;">AI</span></div>
      </div>
      <div style="background: #f8fafc; border-radius: 16px; padding: 28px; text-align: center; margin-top: 12px;">
        <p style="color:#374151; font-size:15px; line-height:22px; margin: 0 0 20px;">{intro_html}</p>
        <div style="font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #1a1a3e; background: #fff; border-radius: 12px; padding: 16px; border: 1.5px solid #e5e7eb;">
          {code}
        </div>
        <p style="color:#9ca3af; font-size:12px; margin-top: 20px;">Bu kod 10 daqiqa amal qiladi. Agar bu so'rovni siz yubormagan bo'lsangiz, shunchaki e'tiborsiz qoldiring.</p>
      </div>
    </div>
    """
    text = f"Ilm AI\n\n{intro_text}\n\n{code}\n\nBu kod 10 daqiqa amal qiladi. Agar bu so'rovni siz yubormagan bo'lsangiz, shunchaki e'tiborsiz qoldiring."
    return html, text


def _send_via_gmail(to_email: str, subject: str, html: str, text: str) -> bool:
    # A plain-text alternative + proper Message-ID/Date headers noticeably
    # improve deliverability — HTML-only mail with no envelope metadata is a
    # common spam-filter trigger, especially from a personal Gmail sender.
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Ilm AI <{GMAIL_ADDRESS}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = GMAIL_ADDRESS
    msg["Message-ID"] = make_msgid(domain="gmail.com")
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, [to_email], msg.as_string())
    return True


def send_verification_code(to_email: str, code: str, purpose: str = "signup") -> bool:
    """
    Send a 6-digit verification code by email. Tries Resend first (best
    deliverability), then Gmail SMTP, then a console fallback for local dev.

    Returns True if actually sent, False if no provider is configured (dev
    fallback: the code is printed to the console instead, so the flow can
    still be tested end-to-end without any email credentials).
    """
    if purpose == "signup":
        subject = "Ilm AI — Emailingizni tasdiqlang"
        intro = "Ro'yxatdan o'tishni yakunlash uchun quyidagi kodni kiriting:"
    else:
        subject = "Ilm AI — Parolni tiklash kodi"
        intro = "Parolingizni tiklash uchun quyidagi kodni kiriting:"

    html, text = _render(code, intro, intro)

    # Try providers in order of preference; fall through to the next on failure.
    for name, enabled, sender in (
        ("brevo", bool(BREVO_API_KEY and BREVO_FROM_EMAIL), lambda: _send_via_brevo(to_email, subject, html, text)),
        ("resend", bool(RESEND_API_KEY), lambda: _send_via_resend(to_email, subject, html, text)),
        ("gmail", bool(GMAIL_ADDRESS and GMAIL_APP_PASSWORD), lambda: _send_via_gmail(to_email, subject, html, text)),
    ):
        if not enabled:
            continue
        try:
            sender()
            return True
        except Exception as e:
            from services.monitoring import track_error
            track_error(e, context={"operation": "send_verification_code", "provider": name, "to_email": to_email, "purpose": purpose})
            print(f"[email] {name} send failed for {to_email}: {e}")

    print(f"[email] No email provider configured/working — {purpose} code for {to_email}: {code}")
    return False
