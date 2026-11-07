"""Execute the actual guarded bootstrap AST without importing application/DB code.

This proves the edited bootstrap policy, not hosted startup or deployed schema.
"""

import ast
import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def execute_guarded_calls(filename, names, production):
    tree = ast.parse((ROOT / filename).read_text(encoding="utf-8-sig"))
    guarded = [
        n
        for n in tree.body
        if isinstance(n, ast.If)
        and ast.dump(n.test)
        == ast.dump(ast.parse("not IS_PRODUCTION", mode="eval").body)
    ]
    guarded_calls = {
        n.func.id
        for block in guarded
        for n in ast.walk(block)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    assert set(names) <= guarded_calls
    # Fail if an old migration/seed call escapes its production guard.
    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            or node in guarded
        ):
            continue
        assert not any(
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name)
            and n.func.id in names
            for n in ast.walk(node)
        )

    class NoImports(ast.NodeTransformer):
        def visit_Import(self, node):
            return ast.copy_location(ast.Pass(), node)

        def visit_ImportFrom(self, node):
            return ast.copy_location(ast.Pass(), node)

    called = []
    namespace = {
        "IS_PRODUCTION": production,
        "engine": object(),
        "Base": SimpleNamespace(
            metadata=SimpleNamespace(
                create_all=lambda **kwargs: called.append("create_all")
            )
        ),
    }
    namespace.update({name: lambda name=name: called.append(name) for name in names})
    module = ast.fix_missing_locations(
        NoImports().visit(ast.Module(body=guarded, type_ignores=[]))
    )
    exec(compile(module, filename, "exec"), namespace)
    return called


@pytest.mark.parametrize("production", [True, False])
def test_production_never_bootstraps_schema_or_legacy_seeds(production):
    names = [
        "seed_question_bank_if_empty",
        "seed_skilltree_if_empty",
        "seed_placement_if_needed",
        "seed_ielts21_if_needed",
        "clean_question_text",
        "retag_general_questions",
    ]
    called = execute_guarded_calls("main.py", names, production)
    assert called == ([] if production else ["create_all", *names])


@pytest.mark.parametrize("production", [True, False])
def test_production_never_runs_import_time_legacy_schema_repairs(production):
    names = [
        "add_profile_picture_column",
        "migrate_sqlite_columns",
        "migrate_postgres_columns",
        "make_password_nullable",
    ]
    called = execute_guarded_calls("services/db.py", names, production)
    assert called == ([] if production else names)


@pytest.mark.parametrize(
    "stage,expected", [("staging", []), ("production", ["start"]), ("", ["start"])]
)
def test_reminders_preserved_at_startup_but_not_sent_from_staging(stage, expected):
    tree = ast.parse((ROOT / "main.py").read_text(encoding="utf-8-sig"))
    function = next(
        n
        for n in tree.body
        if isinstance(n, ast.AsyncFunctionDef) and n.name == "_scheduler_startup"
    )
    function.decorator_list = []
    called = []
    namespace = {
        "os": SimpleNamespace(getenv=lambda key: stage),
        "start_scheduler": lambda: called.append("start"),
    }
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    exec(compile(module, "main.py", "exec"), namespace)
    asyncio.run(namespace["_scheduler_startup"]())
    assert called == expected
