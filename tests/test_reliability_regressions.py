"""Small regressions for confirmed reliability gaps; no network or database."""
import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_postgres_engine_uses_explicit_bounded_pool_policy():
    tree = ast.parse((ROOT / 'services/db.py').read_text(encoding='utf-8-sig'))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name)]
    assert any(n.func.id == 'postgres_engine_options' for n in calls)
    assert any(n.func.id == 'create_engine' and any(
        k.arg is None and isinstance(k.value, ast.Name) and k.value.id == 'postgres_options'
        for k in n.keywords) for n in calls)


def test_container_does_not_start_four_embedded_schedulers():
    source = (ROOT / 'Dockerfile').read_text()
    assert '"--workers", "4"' not in source
    assert 'run_backend.py' in source


def telemetry_function(name):
    tree = ast.parse((ROOT / 'services/monitoring.py').read_text(encoding='utf-8-sig'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace = {'os': __import__('os')}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])),
                 'monitoring-test', 'exec'), namespace)
    return namespace[name]


def test_telemetry_does_not_forward_standard_sentry_auth_or_personal_fields():
    event = {'request': {'url': 'https://example.test/auth?code=private-value',
                         'headers': {'Authorization': 'Bearer private-value'},
                         'data': {'email': 'private-value'}, 'cookies': 'private-value'},
             'user': {'email': 'private-value'},
             'exception': {'values': [{'type': 'RuntimeError', 'value': 'private-value'}]}}
    result = telemetry_function('before_send_event')(event, {})
    assert 'private-value' not in str(result)


def test_telemetry_drops_nested_exception_and_breadcrumb_values():
    event = {'breadcrumbs': {'values': [{'data': {'password':'private-value'}}]},
             'extra': {'access_token':'private-value'}, 'contexts': {'profile': 'private-value'},
             'exception': {'values': [{'type': 'DatabaseError', 'value':'private-value',
                                        'stacktrace': {'frames':[{'vars':{'email':'private-value'}}]}}]}}
    result = telemetry_function('before_send_event')(event,{})
    assert 'private-value' not in str(result)
    assert result['exception']['values'][0]['type'] == 'DatabaseError'


def test_repeated_provider_failures_open_a_circuit_and_release_slots():
    from services.study_help_provider import EvidenceSelector, SelectorUnavailable
    selector = EvidenceSelector(['synthetic-key-only'], 'test-model')
    calls = []

    def unavailable(body):
        calls.append(body)
        raise SelectorUnavailable

    selector._select = unavailable
    context = {'evidence': [{'id': 'e1', 'kind': 'cards', 'text': 'Reviewed fixture'}]}
    for _ in range(6):
        with pytest.raises(SelectorUnavailable):
            selector.select(context)
    assert len(calls) == 3
    assert selector._slots.acquire(blocking=False)
    selector._slots.release()
