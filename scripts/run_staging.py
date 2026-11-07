"""Run only an operator-configured isolated staging backend; never provision it."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services.deployment_config import staging_errors  # noqa: E402 - standalone CLI


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument(
        "--serve", action="store_true", help="explicitly start local port 8931"
    )
    args = parser.parse_args()
    try:
        filename = args.env_file.resolve(strict=True)
        # Private configuration must live outside any checkout, including siblings.
        if any((p / ".git").exists() for p in filename.parents):
            raise ValueError
        values = dotenv_values(filename, interpolate=False, encoding="utf-8-sig")
        errors = staging_errors(values)
    except (OSError, ValueError):
        errors = ["private_configuration_unreadable_or_inside_checkout"]
    if errors:
        print(
            json.dumps(
                {
                    "configuration_valid": False,
                    "failed_checks": errors,
                    "server_started": False,
                }
            )
        )
        return 1
    if not args.serve:
        print(
            json.dumps(
                {
                    "configuration_valid": True,
                    "server_started": False,
                    "https_tested": False,
                    "production_signoff": False,
                }
            )
        )
        return 0
    # Avoid inheriting production provider keys, auth secrets or database URLs.
    allowed = {
        "PATH",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "PATHEXT",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "LOCALAPPDATA",
        "APPDATA",
        "LANG",
    }
    env = {k: v for k, v in os.environ.items() if k.upper() in allowed}
    env.update({k: v for k, v in values.items() if v is not None})
    env["PYTHON_DOTENV_DISABLED"] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8931",
            "--no-access-log",
        ],
        cwd=ROOT,
        env=env,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
