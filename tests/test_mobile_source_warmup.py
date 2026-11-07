"""Source caches stay strict; startup failures never become successful health."""
import asyncio
from types import SimpleNamespace
import sys
import pytest
from services.mobile_source_warmup import prepare_reviewed_mobile, warm_reviewed_sources


@pytest.mark.parametrize("flag", [None, "false", "true"])
def test_only_reviewed_release_prepares_both_existing_caches(monkeypatch, flag):
    calls = []
    monkeypatch.setitem(sys.modules, "services.reviewed_mobile_release", SimpleNamespace(
        expected_rows=lambda: calls.append("reviewed")))
    monkeypatch.setitem(sys.modules, "services.mobile_publication", SimpleNamespace(
        reviewed_content=lambda: calls.append("biology")))
    monkeypatch.delenv("MOBILE_REVIEWED_RELEASE", raising=False)
    if flag is not None:
        monkeypatch.setenv("MOBILE_REVIEWED_RELEASE", flag)
    warm_reviewed_sources()
    assert calls == (["reviewed", "biology"] if flag == "true" else [])


def test_source_validation_failure_blocks_startup_without_echo(monkeypatch):
    from services import mobile_source_warmup
    def fail():
        raise ValueError("synthetic-private-error")
    monkeypatch.setattr(mobile_source_warmup, "warm_reviewed_sources", fail)
    with pytest.raises(RuntimeError, match="^reviewed_mobile_source_warmup_failed$") as error:
        asyncio.run(prepare_reviewed_mobile())
    assert "synthetic-private-error" not in str(error.value)


def test_real_main_registers_source_warmup_before_other_startup_hooks():
    import ast
    from pathlib import Path
    tree = ast.parse((Path(__file__).resolve().parents[1] / "main.py").read_text(encoding="utf-8-sig"))
    hooks = [n.name for n in tree.body if isinstance(n, ast.AsyncFunctionDef)
             and any(isinstance(d, ast.Call) and ast.unparse(d) == "app.on_event('startup')"
                     for d in n.decorator_list)]
    assert hooks[0] == "_reviewed_mobile_startup"
