"""Replay JSON must not depend on the PostgreSQL session's timezone."""
from datetime import datetime, timedelta, timezone
import importlib
from types import SimpleNamespace
import pytest
from services.study import iso_utc


class Query:
    def filter_by(self, **kwargs):
        return self

    def __iter__(self):
        return iter([SimpleNamespace(assessment_key='q1', response={'is_correct': True})])


class Database:
    def query(self, model):
        return Query()


@pytest.mark.parametrize('module', [
    'assessment_runtime', 'chemistry_runtime', 'world_history_runtime', 'uzbekistan_history_runtime',
])
@pytest.mark.parametrize('offset', [-7, 0, 5, 5.5, None])
def test_public_attempt_replay_is_byte_stable_for_database_timezone(module, offset):
    runtime = importlib.import_module('services.'+module)
    instant = datetime(2026, 11, 9, 4, 52, 49, 810203, tzinfo=timezone.utc)
    row = SimpleNamespace(id='synthetic-attempt', scope='synthetic-lesson',
                          started_at=instant, response=None,
                          questions=dict(title='Fixture', content=[], assessments=[]))
    issued = runtime.public_attempt(Database(), row)
    row.started_at = (instant.replace(tzinfo=None) if offset is None
                      else instant.astimezone(timezone(timedelta(hours=offset))))
    replay = runtime.public_attempt(Database(), row)
    assert replay == issued
    assert replay['expires_at'] == '2026-11-10T04:52:49.810203+00:00'
    assert replay['answers'] == {'q1': {'is_correct': True}}


def test_canonical_wire_time_preserves_the_instant_and_microseconds():
    value = datetime(2026, 11, 9, 10, 22, 49, 810203,
                     tzinfo=timezone(timedelta(hours=5, minutes=30)))
    assert datetime.fromisoformat(iso_utc(value)) == value
