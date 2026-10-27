"""Disposable local Mathematics sandbox. Never use the production app/database.

python -m scripts.serve_mathematics_preview --directory /tmp/ilm-mathematics-qa
python -m scripts.serve_mathematics_preview --directory /tmp/ilm-mathematics-qa --resume
The private Flutter defines file contains a one-hour, sandbox-only test JWT.
No Google login bypass is added to the normal application.
"""

import argparse
import contextlib
import io
import json
import os
import secrets
from pathlib import Path


def sandbox_path(raw, resume):
    path = Path(raw).expanduser()
    if path.is_symlink():
        raise ValueError("sandbox_symlinks_not_permitted")
    path = path.resolve()
    if any((parent / ".git").exists() for parent in [path, *path.parents]):
        raise ValueError("sandbox_must_be_outside_all_git_repositories")
    if path.exists() != resume:
        raise ValueError("use_new_directory_or_explicit_resume_of_existing_sandbox")
    if resume and any(
        (path / name).is_symlink()
        for name in ("server.json", "mathematics_staging.db", "flutter-defines.json")
    ):
        raise ValueError("sandbox_symlinks_not_permitted")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--create-only", action="store_true")
    parser.add_argument("--host", choices=["127.0.0.1", "0.0.0.0"], default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8892)
    args = parser.parse_args()
    if os.getenv("ENVIRONMENT") == "production" or not 1024 <= args.port <= 65535:
        parser.error("local_test_only_and_unprivileged_port_required")
    try:
        path = sandbox_path(args.directory, args.resume)
    except ValueError as exc:
        parser.error(str(exc))
    os.umask(0o077)
    if args.resume:
        config = json.loads((path / "server.json").read_text())
        if (
            config.get("mathematics_preview_sandbox") != 1
            or not (path / "mathematics_staging.db").is_file()
        ):
            parser.error("not_an_existing_mathematics_preview_sandbox")
    else:
        path.mkdir(parents=True, mode=0o700)
        config = {
            "mathematics_preview_sandbox": 1,
            "jwt_secret": secrets.token_urlsafe(48),
        }
        (path / "server.json").write_text(json.dumps(config))
    from sqlalchemy.engine import URL

    os.environ.update(
        ENVIRONMENT="test",
        MATHEMATICS_PREVIEW_ENABLED="true",
        AUTH_STORAGE="database",
        DATABASE_URL=URL.create(
            "sqlite", database=str(path / "mathematics_staging.db")
        ).render_as_string(),
        JWT_SECRET=config["jwt_secret"],
        ACCESS_TOKEN_EXPIRE_MINUTES="60",
    )
    # Existing legacy DB import hooks print missing-table diagnostics on a fresh
    # DB. Keep this local setup log private; never import main/startup seeders.
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        from routers.mathematics_preview import router
        from services.db import Base, SessionLocal, engine
        from services.mathematics_curriculum import import_course
        from services.mathematics_models import MathBase
        from services.models import User
        from services.tokens import create_access_token
    (path / "setup.log").write_text(output.getvalue())
    if not args.resume:
        Base.metadata.create_all(engine)
        MathBase.metadata.create_all(engine)
        with SessionLocal.begin() as db:
            db.add(
                User(
                    id=900004,
                    name="Lokal Matematika sinovi",
                    email="mathematics-sandbox@example.test",
                    xp_total=0,
                )
            )
            db.flush()
    # Resume adds only reviewed immutable content; it never resets the user,
    # completed sessions, XP, answers or existing lesson revisions.
    with SessionLocal.begin() as db:
        import_course(db)
    token = create_access_token(900004)
    defines = {
        "MATHEMATICS_PREVIEW": True,
        "API_URL": f"http://127.0.0.1:{args.port}",
        "MATHEMATICS_TEST_USER_ID": 900004,
        "MATHEMATICS_TEST_TOKEN": token,
    }
    (path / "flutter-defines.json").write_text(json.dumps(defines))
    print(
        f"Local sandbox ready. Private Flutter configuration: {path / 'flutter-defines.json'}"
    )
    print(
        "Test JWT expires in 60 minutes. --resume preserves progress and reissues a sandbox token."
    )
    if args.create_only:
        engine.dispose()
        return
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="ILM AI local Mathematics QA only")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:7358", "http://127.0.0.1:7358"],
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(router)
    uvicorn.run(app, host=args.host, port=args.port, access_log=False)


if __name__ == "__main__":
    main()
