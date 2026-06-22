import os
import secrets
from typing import Optional, Tuple
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import Request, HTTPException
from services.users import find_user_by_email, create_user_with_oauth
from services.tokens import create_access_token, create_refresh_token

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


async def get_google_auth_url(request: Request, redirect_uri: str) -> Tuple[str, str]:
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
    # Use a simple dict for state management instead of sessions
    import secrets
    state_store = getattr(request.app.state, 'oauth_state_store', {})
    state_store[state] = {'valid': True}
    request.app.state.oauth_state_store = state_store
    
    client = oauth.create_client('google')
    if not client:
        raise HTTPException(status_code=503, detail="Failed to create OAuth client")
    
    # Set redirect URI dynamically
    client.redirect_uri = redirect_uri
    
    auth_url = client.authorize_redirect(request, state=state)
    return (auth_url.url, state)


async def handle_google_callback(request: Request, redirect_uri: str) -> dict:
    """
    Handle Google OAuth callback and exchange code for user tokens.
    
    Returns:
        Dict with user info and JWT tokens
    """
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )
    
    # Verify state token
    state = request.query_params.get('state')
    state_store = getattr(request.app.state, 'oauth_state_store', {})
    
    if not state or state not in state_store or not state_store[state].get('valid'):
        raise HTTPException(status_code=400, detail="Invalid state token. CSRF protection failed.")
    
    try:
        client = oauth.create_client('google')
        if not client:
            raise HTTPException(status_code=503, detail="Failed to create OAuth client")
        
        client.redirect_uri = redirect_uri
        
        # Exchange authorization code for access token
        token = await client.authorize_access_token(request)
        
        # Get user info from Google
        user_info = await client.parse_id_token(request, token)
        
        if not user_info or 'email' not in user_info:
            raise HTTPException(status_code=400, detail="Failed to retrieve user information from Google")
        
        email = user_info['email'].lower()
        name = user_info.get('name', '')
        google_id = user_info.get('sub')
        picture = user_info.get('picture', '')
        
        # Check if user exists by email
        existing_user = find_user_by_email(email)
        
        if existing_user:
            # User exists, generate tokens for existing user
            user_id = existing_user['id']
            # Update OAuth provider info if not set
            if not existing_user.get('oauth_provider'):
                from services.users import update_user_oauth_info
                update_user_oauth_info(user_id, 'google', google_id, picture)
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
        
        # Generate JWT tokens
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        
        # Clean up state
        state_store[state] = {'valid': False}
        
        return {
            "message": "Google login successful",
            "user_id": user_id,
            "name": name or email.split('@')[0],
            "email": email,
            "picture": picture,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "provider": "google"
        }
        
    except OAuthError as e:
        from services.monitoring import track_error
        track_error(e, context={"operation": "google_oauth_callback", "error_type": "OAuthError"})
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")
    except Exception as e:
        from services.monitoring import track_error
        track_error(e, context={"operation": "google_oauth_callback", "error_type": "GeneralError"})
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")