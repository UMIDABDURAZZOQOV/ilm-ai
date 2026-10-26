"""Disposable loopback-only WorldHistory QA. No production application startup.

The private Flutter defines file contains an expiring sandbox-only test token.
Normal mobile auth/publication and other running development servers are intact.
"""
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import secrets
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))


def sandbox_path(raw, resume):
    path = Path(raw).expanduser()
    if path.is_symlink():
        raise ValueError("sandbox_symlinks_forbidden")
    path = path.resolve()
    if any((p / ".git").exists() for p in (path,*path.parents)):
        raise ValueError("sandbox_must_be_outside_git_repositories")
    if path.exists() != resume:
        raise ValueError("new_directory_or_explicit_resume_required")
    if resume and any((path/n).is_symlink() for n in
                      ("server.json","world_history_staging.db","flutter-defines.json")):
        raise ValueError("sandbox_symlinks_forbidden")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",required=True)
    parser.add_argument("--resume",action="store_true")
    parser.add_argument("--create-only",action="store_true")
    parser.add_argument("--port",type=int,default=8916)
    args = parser.parse_args()
    if os.getenv("ENVIRONMENT") == "production" or not 1024 <= args.port <= 65535:
        parser.error("local_test_only_unprivileged_port_required")
    try:
        path = sandbox_path(args.directory,args.resume)
    except ValueError as exc:
        parser.error(str(exc))
    if args.resume:
        config = json.loads((path/"server.json").read_text())
        if config.get("world_history_sandbox") != 1 or not (path/"world_history_staging.db").is_file():
            parser.error("not_a_world_history_sandbox")
    else:
        path.mkdir(parents=True)
        (path/".gitignore").write_text("*\n")
        config = {"world_history_sandbox":1,"jwt_secret":secrets.token_urlsafe(48)}
        (path/"server.json").write_text(json.dumps(config))
    from sqlalchemy.engine import URL
    os.environ.update(ENVIRONMENT="test",WORLD_HISTORY_PREVIEW_ENABLED="true",
        AUTH_STORAGE="database",JWT_SECRET=config["jwt_secret"],ACCESS_TOKEN_EXPIRE_MINUTES="60",
        DATABASE_URL=URL.create("sqlite",database=str(path/"world_history_staging.db")).render_as_string())
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        from services.db import Base,engine,SessionLocal
        from services.models import User
        from services.world_history_curriculum import import_reviewed_lessons,install_schema
        from services.tokens import create_access_token
        from routers.world_history_preview import router
    (path/"setup.log").write_text(output.getvalue())
    if not args.resume:
        Base.metadata.create_all(engine)
        install_schema(engine)
        with SessionLocal.begin() as db:
            db.add(User(id=900006,name="Lokal Jahon tarixi sinovi",email="world_history-qa@example.test",xp_total=0))
    with SessionLocal.begin() as db:
        import_reviewed_lessons(db)
    defines={"WORLD_HISTORY_PREVIEW":True,"API_URL":f"http://127.0.0.1:{args.port}",
             "WORLD_HISTORY_TEST_USER_ID":900006,"WORLD_HISTORY_TEST_TOKEN":create_access_token(900006)}
    (path/"flutter-defines.json").write_text(json.dumps(defines))
    print("Local WorldHistory sandbox ready; private defines file:",path/"flutter-defines.json")
    if args.create_only:
        engine.dispose()
        return
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    app=FastAPI(title="ILM AI local WorldHistory QA only")
    app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:7366","http://127.0.0.1:7366"],
                       allow_methods=["GET","POST"],allow_headers=["Authorization","Content-Type"])
    app.include_router(router)
    uvicorn.run(app,host="127.0.0.1",port=args.port,access_log=False)


if __name__ == "__main__":
    main()
