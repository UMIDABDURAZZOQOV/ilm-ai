import os
import secrets
import requests
from starlette.concurrency import run_in_threadpool
from typing import Tuple
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException
from services.users import find_user_by_email, create_user_with_oauth
from services.tokens import create_access_token, create_refresh_token

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth = OAuth()

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=GOOGLE_DISCOVERY_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


def is_google_oauth_enabled() -> bool:
    """Check if Google OAuth is properly configured."""
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def generate_state_token() -> str:
    """Generate a secure state token for CSRF protection."""
    return secrets.token_urlsafe(32)


async def get_google_auth_url(request: Request, redirect_uri: str, challenge: str | None = None) -> Tuple[str, str]:
    """
    Generate Google OAuth authorization URL with state token.
    
    Returns:
        Tuple of (auth_url, state_token)
    """
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )
    
    state = generate_state_token()
    from services.mobile_oauth import save_state
    save_state(state, redirect_uri, challenge)

    client = oauth.create_client('google')
    if not client:
        raise HTTPException(status_code=503, detail="Failed to create OAuth client")

    # Build authorization URL directly without redirect
    metadata = await client.load_server_metadata()
    auth_endpoint = metadata['authorization_endpoint']

    import urllib.parse
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline',
    }
    auth_url = auth_endpoint + '?' + urllib.parse.urlencode(params)
    return (auth_url, state)


async def handle_google_callback(request: Request, redirect_uri: str, mobile: bool = False) -> dict:
    """
    Handle Google OAuth callback and exchange code for user tokens.

    Returns:
        Dict with user info and JWT tokens

    State is persisted, bound to this redirect URI, expires after ten minutes,
    and is consumed once across workers. Mobile callbacks issue a short-lived
    PKCE grant; only its HTTPS exchange returns access/refresh credentials.
    """
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )

    # Verify state token
    state = request.query_params.get('state')
    code = request.query_params.get('code')
    from services.mobile_oauth import consume_state
    challenge = consume_state(state, redirect_uri)
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code from Google")
    if mobile and not challenge:
        raise HTTPException(status_code=400, detail="mobile_client_upgrade_required")

    try:
        token_resp = await run_in_threadpool(requests.post,
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=15,
        )
        if token_resp.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="Google token exchange failed",
            )
        google_access_token = token_resp.json().get("access_token")

        userinfo_resp = await run_in_threadpool(requests.get,
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {google_access_token}"},
            timeout=15,
        )
        if userinfo_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve user information from Google")
        user_info = userinfo_resp.json()

        if (not user_info or not user_info.get('email') or
                user_info.get('email_verified') is not True or not user_info.get('sub')):
            raise HTTPException(status_code=400, detail="Failed to retrieve user information from Google")

        email = user_info['email'].lower()
        name = user_info.get('name', '')
        google_id = user_info.get('sub')
        picture = user_info.get('picture', '')

        # Check if user exists by email
        existing_user = find_user_by_email(email)

        if existing_user:
            if (existing_user.get('oauth_provider') == 'google' and
                    existing_user.get('oauth_provider_id') and
                    existing_user['oauth_provider_id'] != google_id):
                raise HTTPException(400, "Google identity does not match this account")
            # User exists, generate tokens for existing user
            user_id = existing_user['id']
            # Update OAuth provider info if not set
            if not existing_user.get('oauth_provider'):
                from services.users import update_user_oauth_info
                update_user_oauth_info(user_id, 'google', google_id, picture)
            # Existing users who never went through onboarding still need a name+age.
            needs_onboarding = existing_user.get('age') is None
        else:
            # Create new user with OAuth
            user = create_user_with_oauth(
                name=name or email.split('@')[0],
                email=email,
                provider='google',
                provider_id=google_id,
                picture=picture
            )
            user_id = user['id']
            needs_onboarding = True  # brand-new user: must pick a name + age

        if mobile:
            from services.mobile_oauth import issue_grant
            return {"user_id": user_id, "email": email, "code": issue_grant(user_id, challenge)}
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        return {
            "message": "Google login successful",
            "user_id": user_id,
            "name": name or email.split('@')[0],
            "email": email,
            "picture": picture,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "provider": "google",
            "needs_onboarding": needs_onboarding,
        }

    except HTTPException:
        raise
    except Exception as e:
        import logging
        # Provider/DB exceptions may embed parameters. Record only their category.
        logging.getLogger(__name__).warning("Google OAuth callback failed (%s)", type(e).__name__)
        raise HTTPException(status_code=500, detail="Authentication failed")
