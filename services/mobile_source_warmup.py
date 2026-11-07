"""Validate immutable source caches before reviewed mobile accepts traffic."""
import os


def warm_reviewed_sources():
    if os.getenv("MOBILE_REVIEWED_RELEASE") != "true":
        return
    from services.reviewed_mobile_release import expected_rows
    from services.mobile_publication import reviewed_content
    # Same validators and process-local caches used by request guards.
    expected_rows()
    reviewed_content()


async def prepare_reviewed_mobile():
    from starlette.concurrency import run_in_threadpool
    try:
        await run_in_threadpool(warm_reviewed_sources)
    except Exception:
        raise RuntimeError("reviewed_mobile_source_warmup_failed") from None
