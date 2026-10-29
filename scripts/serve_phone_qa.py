"""Five-subject phone sandbox. Loopback only; no production startup or baked tokens."""
import argparse
import contextlib
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
UID = 990005
DB_NAME = 'chemistry_staging_world_history_staging_uzbekistan_history_staging.db'


def sandbox_directory(raw, resume):
    path = Path(raw).absolute()
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise ValueError('sandbox_symlinks_forbidden')
    path = path.resolve()
    if any((p / '.git').exists() for p in [path, *path.parents]):
        raise ValueError('sandbox_must_be_outside_git')
    if path.exists() != resume:
        raise ValueError('new_directory_or_explicit_resume_required')
    if resume and any((path / n).is_symlink() for n in ['server.json', DB_NAME, 'pairing.json']):
        raise ValueError('sandbox_symlinks_forbidden')
    return path


def configure(path, resume, port):
    if os.getenv('ENVIRONMENT') == 'production' or not 1024 <= port <= 65535:
        raise ValueError('local_test_only')
    if resume:
        config = json.loads((path / 'server.json').read_text('utf8'))
        if config.get('phone_qa_sandbox') != 1 or not (path / DB_NAME).is_file():
            raise ValueError('not_owned_phone_sandbox')
    else:
        path.mkdir(parents=True)
        (path / '.gitignore').write_text('*\n')
        config = dict(phone_qa_sandbox=1, jwt_secret=secrets.token_urlsafe(48))
        (path / 'server.json').write_text(json.dumps(config))
    from sqlalchemy.engine import URL
    os.environ.update(ENVIRONMENT='test', AUTH_STORAGE='database',
        DATABASE_URL=URL.create('sqlite', database=str(path / DB_NAME)).render_as_string(),
        JWT_SECRET=config['jwt_secret'], SECRET_KEY=config['jwt_secret'],
        ACCESS_TOKEN_EXPIRE_MINUTES='15', REFRESH_TOKEN_EXPIRE_DAYS='1',
        PHYSICS_PREVIEW_ENABLED='true', CHEMISTRY_PREVIEW_ENABLED='true',
        WORLD_HISTORY_PREVIEW_ENABLED='true', UZBEKISTAN_HISTORY_PREVIEW_ENABLED='true',
        MOBILE_PUBLISHED_SUBJECTS='biologiya', GOOGLE_CLIENT_ID='', GOOGLE_CLIENT_SECRET='',
        OPENAI_API_KEY='', MOBILE_OAUTH_REDIRECT_URI=f'http://127.0.0.1:{port}/auth/google-callback-mobile')


def initialize(path, *, seed_user=True):
    # Import only after setting the owned SQLite URL. Never import main/startup.
    from services.db import Base, engine, SessionLocal
    from services.models import User
    from services.assessment_models import AssessmentBase
    from services.uzbekistan_history_models import HistoryBase
    from services.chemistry_curriculum import install_schema as chemistry_schema, import_reviewed_lessons as chemistry_import
    from services.world_history_curriculum import install_schema as world_schema, import_reviewed_lessons as world_import
    from services.uzbekistan_history_curriculum import import_course
    from services.physics_curriculum import load_course, import_batch
    from services.curriculum_validation import load_documents, load_lesson_set
    from services.curriculum import import_curriculum
    Base.metadata.create_all(engine)
    AssessmentBase.metadata.create_all(engine)
    HistoryBase.metadata.create_all(engine)
    chemistry_schema(engine)
    world_schema(engine)
    catalog, _ = load_documents()
    with SessionLocal.begin() as db:
        if seed_user and db.get(User, UID) is None:
            db.add(User(id=UID, name='Telefon QA', email='phone-qa@example.test', xp_total=0, email_verified=True))
            db.flush()
        biology = load_lesson_set()
        for lesson in biology:
            import_curriculum(db, catalog, lesson, allow_source_upgrade=True)
        physics = load_course()
        for batch in physics:
            import_batch(db, batch)
        chemistry = chemistry_import(db)
        world = world_import(db)
        history = import_course(db)
    counts = dict(biologiya=len(biology), fizika=sum(len(b['lessons']) for b in physics), kimyo=len(chemistry),
                  jahon_tarixi=len(world), ozbekiston_tarixi=history['created'] + history['skipped'])
    assert counts == dict(biologiya=406, fizika=316, kimyo=268, jahon_tarixi=219, ozbekiston_tarixi=172), counts
    (path / 'readiness.json').write_text(json.dumps(counts, indent=2))
    return counts


def create_app(path, counts):
    from fastapi import FastAPI, Depends, HTTPException, Request
    from pydantic import BaseModel, ConfigDict, Field
    from starlette.middleware.trustedhost import TrustedHostMiddleware
    from services.db import SessionLocal
    from services.models import User
    from services.auth_deps import get_authenticated_user_id
    from services.tokens import create_access_token, create_refresh_token
    from routers.auth import router as auth
    from routers.mobile_skills import router as biology
    from routers.physics_preview import router as physics
    from routers.chemistry_preview import router as chemistry
    from routers.world_history_preview import router as world
    from routers.uzbekistan_history_preview import router as history

    app = FastAPI(title='ILM AI Phone QA', docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost', '[::1]'])
    @app.middleware('http')
    async def local_only(request: Request, call_next):
        from starlette.responses import JSONResponse
        if request.client.host not in {'127.0.0.1', '::1'} or any(h in request.headers for h in ['forwarded','x-forwarded-for','x-forwarded-host']):
            return JSONResponse({'detail':'loopback_only'}, status_code=403)
        if '/tutor' in request.url.path:
            return JSONResponse({'detail':'not_in_phone_qa'}, status_code=404)
        if request.url.path.startswith('/auth/') and not (
            request.url.path in {'/auth/refresh', '/auth/logout', '/auth/complete-onboarding',
                                 '/auth/update-profile', '/auth/mobile/config', '/auth/google-login'}
            or request.url.path == f'/auth/profile/{UID}'
        ):
            return JSONResponse({'detail':'not_in_phone_qa'}, status_code=404)
        return await call_next(request)
    for router in [auth, biology, physics, chemistry, world, history]:
        app.include_router(router)
    pairing = dict(code=secrets.token_hex(4).upper(), expires_at=int(time.time())+600, used=False, attempts=0)
    pairing_file = path / 'pairing.json'
    pairing_file.write_text(json.dumps(pairing))
    lock = threading.Lock()
    class Pair(BaseModel):
        model_config = ConfigDict(extra='forbid')
        code: str = Field(min_length=8,max_length=8)
    @app.get('/health')
    def health():
        return {'status':'ok','mode':'phone_qa','google_oauth_tested':False}
    @app.post('/qa/pair')
    def pair(data: Pair):
        with lock:
            if pairing['used'] or pairing['expires_at'] < time.time() or pairing['attempts'] >= 5:
                raise HTTPException(401,'pairing_expired_or_used')
            pairing['attempts'] += 1
            if not secrets.compare_digest(data.code.upper(),pairing['code']):
                raise HTTPException(401,'invalid_pairing_code')
            pairing['used'] = True
            pairing_file.write_text(json.dumps(pairing))
        with SessionLocal() as db:
            user = db.get(User,UID)
            payload = dict(user_id=UID,name=user.name,email=user.email,needs_onboarding=user.age is None)
        return dict(payload,access_token=create_access_token(UID),refresh_token=create_refresh_token(UID))
    @app.get('/qa/me')
    def me(uid: int = Depends(get_authenticated_user_id)):
        if uid != UID:
            raise HTTPException(403,'owned_synthetic_account_only')
        with SessionLocal() as db:
            user=db.get(User,uid)
            return dict(user_id=uid,name=user.name,xp_total=user.xp_total,streak_days=user.streak_days,subjects=counts)
    return app


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',required=True)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--create-only',action='store_true')
    parser.add_argument('--port',type=int,default=8925)
    args=parser.parse_args()
    path=sandbox_directory(args.directory,args.resume)
    configure(path,args.resume,args.port)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        counts=initialize(path)
        app=create_app(path,counts)
    (path/'setup.log').write_text(output.getvalue(),encoding='utf8')
    print('Owned local phone sandbox ready:',json.dumps(counts))
    print('Enter the one-time code from this private file on the phone:',path/'pairing.json')
    print('Code expires after10minutes; --resume preserves all QA progress and renews pairing.')
    if not args.create_only:
        import uvicorn
        uvicorn.run(app,host='127.0.0.1',port=args.port,access_log=False,proxy_headers=False)


if __name__=='__main__':
    main()
