"""Read-only mobile API diagnostics. Never starts OAuth or prints credentials."""

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url", default="https://ilm-ai-backend-256x.onrender.com"
    )
    args = parser.parse_args()
    report = {}
    for label, route in [
        ("health", "/health"),
        ("subjects", "/skills/subjects"),
        ("mobile_auth", "/auth/mobile/config"),
        ("biology_grades", "/skills/subjects/biologiya/grades"),
    ]:
        try:
            with urlopen(args.base_url.rstrip("/") + route, timeout=15) as response:
                data = json.load(response)
                value = {"http_status": response.status}
                if label == "subjects":
                    value.update(
                        valid_shape=isinstance(data, list),
                        count=len(data) if isinstance(data, list) else None,
                    )
                elif label == "mobile_auth":
                    value.update(
                        mobile_auth_version=data.get("mobile_auth_version"),
                        google_configured=data.get("google_configured"),
                    )
                elif label == "biology_grades":
                    value["grades"] = [
                        {
                            "grade": r.get("grade"),
                            "status": r.get("status"),
                            "ready_lessons": r.get("ready_lessons"),
                        }
                        for r in data.get("grades", [])
                    ]
                report[label] = value
        except HTTPError as error:
            report[label] = {"http_status": error.code}
        except (URLError, TimeoutError, ValueError, AttributeError) as error:
            report[label] = {"reachable": False, "error_type": type(error).__name__}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    ready = (
        all(r.get("http_status") == 200 for r in report.values())
        and report["subjects"].get("valid_shape")
        and report["mobile_auth"].get("mobile_auth_version") == 2
        and report["mobile_auth"].get("google_configured") is True
        and any(
            r.get("grade") == 5 and r.get("ready_lessons", 0) > 0
            for r in report["biology_grades"].get("grades", [])
        )
    )
    raise SystemExit(0 if ready else 1)


if __name__ == "__main__":
    main()
