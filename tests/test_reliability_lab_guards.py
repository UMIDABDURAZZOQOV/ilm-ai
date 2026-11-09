"""The local lab must refuse larger or under-resourced runs before creating an app."""
import asyncio
import json
from types import SimpleNamespace
from scripts.reliability import component_lab as lab
from scripts.reliability.capacity_plan import scenarios


def test_low_memory_aborts_without_load_or_database(tmp_path, monkeypatch):
    monkeypatch.setattr(lab.psutil, 'virtual_memory', lambda: SimpleNamespace(available=1,total=1))
    def forbidden(*args, **kwargs):
        raise AssertionError('database_created_before_resource_gate')
    monkeypatch.setattr(lab, 'create_engine', forbidden)
    target = tmp_path/'blocked.json'
    asyncio.run(lab.experiment(10,target))
    result = json.loads(target.read_text())
    assert result['status'] == 'BLOCKED' and result['phases'] == []
    assert result['external_provider_calls'] == 0


def test_even_available_resources_do_not_authorize_1000_user_run(tmp_path, monkeypatch):
    monkeypatch.setattr(lab.psutil, 'virtual_memory', lambda: SimpleNamespace(available=32*1024**3,total=32*1024**3))
    monkeypatch.setattr(lab.shutil, 'disk_usage', lambda _: SimpleNamespace(free=32*1024**3))
    target = tmp_path/'blocked-large.json'
    asyncio.run(lab.experiment(1000,target))
    result = json.loads(target.read_text())
    assert result['status'] == 'BLOCKED' and result['phases'] == []
    assert 'operator_review' in result['reason']


def test_capacity_model_is_explicitly_hypothetical_and_separates_registered_users():
    result = scenarios()
    assert result['status'] == 'PLANNED'
    assert [r['assumed_peak_concurrent'] for r in result['scenarios']] == [3,25,250,2500]
    assert all(r['assumed_dau'] < r['registered'] for r in result['scenarios'])


def test_blocked_aborted_or_partial_lab_cannot_be_reported_complete():
    assert not lab.completed({'status':'BLOCKED'})
    assert not lab.completed({'status':'SIMULATED','aborted':True})
    assert not lab.completed({'status':'SIMULATED','aborted':False,'phases':[]})
