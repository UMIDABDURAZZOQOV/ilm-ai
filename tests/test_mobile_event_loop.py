"""Synchronous database work in async mobile routes must run off the event loop.

A blocking call on the loop freezes every other request for its duration; in
production this showed up as random 15 s+ stalls on unrelated endpoints.
"""
import asyncio
import threading

from routers import beta_mobile as bm


def endpoint(router, path):
    return next(r.endpoint for r in router.routes if getattr(r, 'path', None) == path)


def test_grades_and_tree_query_the_database_in_a_worker_thread(monkeypatch):
    monkeypatch.delenv('CATALOG_CACHE_SECONDS', raising=False)
    seen = {}

    def fake_grades(db, slug):
        seen['grades'] = threading.current_thread()
        return {'grades': []}

    def fake_tree(db, user_id, subject, grade):
        seen['tree'] = threading.current_thread()
        return {'units': []}

    monkeypatch.setattr(bm.beta, 'grades', fake_grades)
    monkeypatch.setattr(bm.beta, 'tree', fake_tree)
    router = bm.create_router('/probe', lambda: None)

    async def run():
        loop_thread = threading.current_thread()
        await endpoint(router, '/probe/skills/subjects/{subject_slug}/grades')(
            subject_slug='fizika', request=None, db=object())
        await endpoint(router, '/probe/skills/{user_id}/tree')(
            subject='fizika', grade=7, request=None, db=object(), user_id=1)
        return loop_thread

    loop_thread = asyncio.run(run())
    assert seen['grades'] is not loop_thread
    assert seen['tree'] is not loop_thread
