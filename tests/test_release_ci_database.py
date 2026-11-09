"""Fast offline contracts catch isolated CI setup mistakes before course imports."""
from pathlib import Path
import re
from types import SimpleNamespace
from sqlalchemy.engine import make_url


def test_ci_database_name_satisfies_both_preview_guards_without_relaxing_them(monkeypatch):
    workflow = (Path(__file__).resolve().parents[1] / '.github/workflows/ci.yml').read_text()
    name = re.search(r'POSTGRES_DB:\s*(\w+)', workflow)[1]
    url = make_url('postgresql://synthetic:synthetic@127.0.0.1/' + name)
    monkeypatch.setenv('ENVIRONMENT', 'test')
    monkeypatch.setenv('CHEMISTRY_PREVIEW_ENABLED', 'true')
    monkeypatch.setenv('WORLD_HISTORY_PREVIEW_ENABLED', 'true')
    from services.chemistry_curriculum import require_local as chemistry_guard
    from services.world_history_curriculum import require_local as history_guard
    chemistry_guard(SimpleNamespace(url=url))
    history_guard(SimpleNamespace(url=url))
    assert 'image: postgres:18' in workflow
    assert '/'+name+"'" in workflow
    assert 'python -m pip check' in workflow
    assert 'requirements-source-review.txt' in workflow
