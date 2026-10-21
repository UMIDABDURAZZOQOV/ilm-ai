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
        ("mobile_catalog_config", "/mobile/skills/config"),
        ("subjects", "/mobile/skills/subjects"),
        ("mobile_auth", "/auth/mobile/config"),
        ("biology_grades", "/mobile/skills/subjects/biologiya/grades"),
    ]:
        try:
            with urlopen(args.base_url.rstrip("/") + route, timeout=15) as response:
                data = json.load(response)
                value = {"http_status": response.status}
                if label == "subjects":
                    value.update(
                        valid_shape=isinstance(data, list),
                        count=len(data) if isinstance(data, list) else None,
                        slugs=[r.get("slug") for r in data] if isinstance(data, list) else [],
                        ready_lessons=sum(r.get("ready_lessons", 0) for r in data) if isinstance(data, list) else 0,
                    )
                elif label == "mobile_catalog_config":
                    value["mobile_curriculum_version"] = data.get("mobile_curriculum_version")
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
        and report["subjects"].get("slugs") == ["biologiya"]
        and report["subjects"].get("ready_lessons") == 406
        and report["mobile_catalog_config"].get("mobile_curriculum_version") == 1
        and report["mobile_auth"].get("mobile_auth_version") == 2
        and report["mobile_auth"].get("google_configured") is True
        and [(r.get("grade"), r.get("ready_lessons"))
             for r in report["biology_grades"].get("grades", [])]
        == list(zip(range(5, 12), [30, 66, 64, 68, 67, 62, 49]))
    )
    raise SystemExit(0 if ready else 1)


if __name__ == "__main__":
    main()
