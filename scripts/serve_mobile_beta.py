"""Isolated integrated mobile beta. No production startup, data or embedded tokens."""
import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import secrets
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.serve_phone_qa import sandbox_directory, initialize

DB_NAME = 'chemistry_staging_world_history_staging_uzbekistan_history_staging_beta_staging.db'


def configure(path, resume, port, oauth_file=None):
    if os.getenv('ENVIRONMENT') == 'production' or not 1024 <= port <= 65535:
        raise ValueError('beta_local_test_only')
    if resume:
        if any((path / name).is_symlink() for name in ['server.json', DB_NAME]):
            raise ValueError('sandbox_symlinks_forbidden')
        config = json.loads((path/'server.json').read_text(encoding='utf8'))
        if config.get('integrated_beta_sandbox') != 1 or not (path/DB_NAME).is_file():
            raise ValueError('not_owned_beta_sandbox')
    else:
        path.mkdir(parents=True)
        (path/'.gitignore').write_text('*\n')
        config = dict(integrated_beta_sandbox=1, jwt_secret=secrets.token_urlsafe(48))
        (path/'server.json').write_text(json.dumps(config))
    oauth = json.loads(Path(oauth_file).read_text(encoding='utf8')) if oauth_file else {}
    if set(oauth) - {'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET'}:
        raise ValueError('unexpected_oauth_config_fields')
    from sqlalchemy.engine import URL
    os.environ.update(ENVIRONMENT='test', AUTH_STORAGE='database', ILM_BETA_ENABLED='true',
        DATABASE_URL=URL.create('sqlite', database=str(path/DB_NAME)).render_as_string(),
        JWT_SECRET=config['jwt_secret'], SECRET_KEY=config['jwt_secret'],
        ACCESS_TOKEN_EXPIRE_MINUTES='15', REFRESH_TOKEN_EXPIRE_DAYS='7',
        PHYSICS_PREVIEW_ENABLED='true', CHEMISTRY_PREVIEW_ENABLED='true',
        WORLD_HISTORY_PREVIEW_ENABLED='true', UZBEKISTAN_HISTORY_PREVIEW_ENABLED='true',
        MOBILE_PUBLISHED_SUBJECTS='biologiya', OPENAI_API_KEY='',
        GOOGLE_CLIENT_ID=oauth.get('GOOGLE_CLIENT_ID',''), GOOGLE_CLIENT_SECRET=oauth.get('GOOGLE_CLIENT_SECRET',''),
        MOBILE_OAUTH_REDIRECT_URI=f'http://127.0.0.1:{port}/auth/google-callback-mobile',
        MOBILE_APP_SCHEME='ilmai-beta', BETA_TEST_AUTH_ENABLED='true', BETA_SERVER_MODE='local')


def create_app():
    from fastapi import FastAPI, HTTPException, Request
    from pydantic import BaseModel, ConfigDict, Field
    from sqlalchemy.exc import IntegrityError
    from starlette.middleware.trustedhost import TrustedHostMiddleware
    from services.db import SessionLocal
    from services.models import User
    from services.beta_models import BetaTestIdentity
    from services.tokens import create_access_token, create_refresh_token
    from services.google_oauth import is_google_oauth_enabled
    from routers import auth as auth_module
    from routers.auth import router as auth
    from routers.mobile_skills import router as original_mobile
    from routers.beta_mobile import router as integrated
    from services.beta_curriculum import gate

    if os.getenv('ILM_BETA_ENABLED') != 'true' or os.getenv('ENVIRONMENT') not in {'test','development'}:
        raise ValueError('beta_test_environment_required')
    with SessionLocal() as db:
        gate(db)
    app = FastAPI(title='ILM AI Beta', docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1','localhost','[::1]'])
    @app.middleware('http')
    async def local_only(request: Request, call_next):
        from starlette.responses import JSONResponse
        if request.client.host not in {'127.0.0.1','::1'} or any(h in request.headers for h in ['forwarded','x-forwarded-for','x-forwarded-host']):
            return JSONResponse({'detail':'loopback_only'},status_code=403)
        if '/tutor' in request.url.path or request.url.path.startswith(('/qa','/preview')) or request.url.path in {
            '/auth/signup','/auth/login','/auth/resend-code','/auth/verify-email','/auth/_diag/email',
            '/auth/password-reset/request','/auth/password-reset/confirm'}:
            return JSONResponse({'detail':'not_available_in_beta'},status_code=404)
        return await call_next(request)
    @app.get('/auth/google-callback-mobile')
    async def beta_callback(request: Request, code: str | None = None, state: str | None = None, error: str | None = None):
        # Delegate PKCE/state/code exchange unchanged; only the beta app's
        # final custom URI differs. The ordinary OAuth router stays byte-identical.
        from urllib.parse import urlsplit, parse_qs
        from starlette.responses import RedirectResponse
        response = await auth_module.google_callback_mobile(request,code,state,error)
        uri = urlsplit(response.headers.get('location',''))
        if uri.scheme != 'ilmai' or uri.netloc != 'auth' or uri.path != '/callback' or uri.fragment or set(parse_qs(uri.query)) - {'code','state','error'}:
            raise HTTPException(503,'invalid_beta_callback')
        return RedirectResponse(uri._replace(scheme='ilmai-beta').geturl(),status_code=response.status_code)

    app.include_router(auth)
    app.include_router(integrated)
    app.include_router(original_mobile)
    lock = threading.Lock()
    requests = []
    class TestLogin(BaseModel):
        model_config = ConfigDict(extra='forbid')
        installation_secret: str = Field(min_length=43,max_length=43,pattern=r'^[A-Za-z0-9_-]+$')

    def test_auth_available():
        return os.getenv('BETA_TEST_AUTH_ENABLED') == 'true' and os.getenv('BETA_SERVER_MODE') == 'local'

    @app.get('/health')
    def health():
        return {'status':'ok','mode':'integrated_beta'}

    @app.get('/beta/config')
    def config():
        return dict(google_configured=is_google_oauth_enabled(), test_auth_available=test_auth_available(),
                    app_scheme='ilmai-beta', subjects=5, production_ready=False)

    @app.post('/beta/auth/test-login')
    def test_login(data: TestLogin):
        if not test_auth_available():
            raise HTTPException(404,'beta_test_auth_disabled')
        digest = hashlib.sha256(data.installation_secret.encode()).hexdigest()
        with lock:
            now=time.monotonic()
            requests[:] = [t for t in requests if t > now-60]
            if len(requests) >= 15:
                raise HTTPException(429,'try_again_later')
            requests.append(now)
            with SessionLocal() as db:
                identity=db.get(BetaTestIdentity,digest)
                if identity is None:
                    user=User(name='Beta o‘quvchi',email=f'beta-{secrets.token_hex(12)}@example.test',email_verified=True,xp_total=0)
                    db.add(user); db.flush()
                    identity=BetaTestIdentity(credential_hash=digest,user_id=user.id)
                    db.add(identity)
                    try:
                        db.commit()
                    except IntegrityError:
                        db.rollback()
                        identity=db.get(BetaTestIdentity,digest)
                        if identity is None:
                            raise
                user=db.get(User,identity.user_id)
                result=dict(user_id=user.id,name=user.name,email=user.email,needs_onboarding=user.age is None)
        return dict(result,access_token=create_access_token(result['user_id']),refresh_token=create_refresh_token(result['user_id']))
    return app


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',required=True)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--port',type=int,default=8930)
    parser.add_argument('--oauth-config-file')
    parser.add_argument('--ai-config-file', help='Audience-reviewed private evidence-selector config outside checkout; omitted = reviewed fallback')
    args=parser.parse_args()
    path=sandbox_directory(args.directory,args.resume)
    configure(path,args.resume,args.port,args.oauth_config_file)
    from services.study_help import configure_provider
    configure_provider(args.ai_config_file)
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):
        counts=initialize(path,seed_user=False)
        from services.beta_models import BetaBase
        from services.db import engine
        BetaBase.metadata.create_all(engine)
        app=create_app()
    (path/'setup.log').write_text(captured.getvalue(),encoding='utf8')
    print('Integrated beta ready:',json.dumps(counts),flush=True)
    print('Local test authentication enabled. Google OAuth requires explicit private configuration.',flush=True)
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=args.port,access_log=False,proxy_headers=False)


if __name__=='__main__':
    main()
