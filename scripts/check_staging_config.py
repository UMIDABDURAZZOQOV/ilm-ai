"""Validate a private staging env file offline; output fixed check names only."""

import argparse
import json
from pathlib import Path
import sys
from dotenv import dotenv_values

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.deployment_config import staging_errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True, type=Path)
    args = parser.parse_args()
    try:
        env = dotenv_values(args.env_file, interpolate=False, encoding="utf-8-sig")
        errors = staging_errors(env)
    except (OSError, ValueError):
        errors = ["private_configuration_unreadable"]
    print(
        json.dumps(
            {
                "configuration_valid": not errors,
                "failed_checks": errors,
                "network_tested": False,
                "server_started": False,
                "production_signoff": False,
            },
            indent=2,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
