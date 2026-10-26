"""Read-only source audit; missing books stay blocked, never generated."""

import argparse
import json

from services.uzbekistan_history_sources import (
    load_catalog,
    validate_catalog,
    verify_originals,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    catalog = load_catalog()
    result = validate_catalog(catalog)
    if args.pdf_dir:
        result.update(verify_originals(catalog, args.pdf_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.require_complete and result["blocked_grades"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
