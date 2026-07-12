import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid, formatdate
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


def is_email_configured() -> bool:
    return bool(GMAIL_ADDRESS and GMAIL_APP_PASSWORD)


def _build_message(to_email: str, subject: str, code: str, intro_html: str, intro_text: str) -> MIMEMultipart:
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
    return msg


def send_verification_code(to_email: str, code: str, purpose: str = "signup") -> bool:
    """
    Send a 6-digit verification code by email.

    Returns True if actually sent, False if email isn't configured (dev
    fallback: the code is printed to the console instead, so the flow can
    still be tested end-to-end without SMTP credentials).
    """
    if purpose == "signup":
        subject = "Ilm AI — Emailingizni tasdiqlang"
        intro = "Ro'yxatdan o'tishni yakunlash uchun quyidagi kodni kiriting:"
    else:
        subject = "Ilm AI — Parolni tiklash kodi"
        intro = "Parolingizni tiklash uchun quyidagi kodni kiriting:"

    if not is_email_configured():
        print(f"[email] SMTP not configured — {purpose} code for {to_email}: {code}")
        return False

    try:
        msg = _build_message(to_email, subject, code, intro, intro)
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, [to_email], msg.as_string())
        return True
    except Exception as e:
        from services.monitoring import track_error
        track_error(e, context={"operation": "send_verification_code", "to_email": to_email, "purpose": purpose})
        print(f"[email] Failed to send to {to_email}, falling back to console — code: {code}")
        return False
