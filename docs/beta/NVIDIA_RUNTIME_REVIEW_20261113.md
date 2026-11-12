# Exact shared-runtime review — optional NVIDIA startup

This records a technical runtime change authorized by the owner's NVIDIA
integration request. It grants no textbook erratum, model entitlement, live AI,
deployment, GitHub push or production approval. Original subject manifests,
facts, rubrics, source/PDF digests, IDs, XP and prerequisites remain unchanged.

Reviewed code commit: `1ae74cb` on `qa/nvidia-explanations-20261112`.

## Exact main change

Relative to accepted backend93d899b, the final `main.py` adds only
`_study_help_startup()` calling `configure_from_environment()`, immediately
**after** the existing reviewed-source warmup. Removing that single function
and decorator exactly recovers the earlier LF bytes. Existing hooks, router
mounting, auth, migrations, reliability and scheduler code are unchanged.
Startup performs no model request. A failed source warmup stops AI setup.

The first full candidate run caught an incorrectly placed AI hook and a stale
shared-runtime digest. Both failed receipts remain in the artifacts. The
existing source-first test is retained. New execution regressions require
source-before-AI and no AI setup after source failure.

## Controlled review binding

`shared_runtime_review_20261107.json` updates only the `main.py` row and its
technical review description. That row records the previous main/review digest
and code commit. All original baseline maps and the other five rows are equal
to the previous document. `tests/protected_baseline.py` changes only its exact
review-document digest constant. Its whitelist, comparison logic and rejection
of later unknown bytes remain unchanged.

This is not a wildcard exception or an automatic hash refresh. The original
subject manifests are never rewritten. Negative tests must still reject a
wrong original baseline, an added runtime mutation, a forged review document,
changed source claims and changed PDF/image bytes. Existing preservation tests
remain unmodified and must be rerun against the reviewed binding.

Exact old/new hashes, structural comparison and unchanged-row checks:
`ilm-ai-beta-artifacts/NVIDIA_RUNTIME_REVIEW_BINDING_20261113.json`.

## Full-suite applicability

The earlier full groups and real PostgreSQL supplement were frozen before this
follow-up. Their failures are retained. The startup, optional-provider and
preservation regressions are rerun after this change. Course handlers, grader,
XP and source-content code are unchanged from those runs. Report combined case
coverage and follow-up results separately; do not describe them as a new Linux
CI run or one uninterrupted full-suite pass on the final commit.

The Phone QA fixture also now uses its own fresh engine/factories and private
signing secret after collection preloads `services.db`; the earlier accidental
bootstrap-DB use is rejected by the existing Chemistry isolation guard. That
guard is retained. A new fixture regression verifies owned URL, factory,
signing-secret binding and synthetic user isolation. Application Phone QA code
and real user databases are unchanged.

Current release authority remains the external `FINAL_GO_NO_GO.md` and
`NVIDIA_AI_LIVE_VERIFICATION.md`. Missing live configuration, Android proof,
new exact-source hosted CI and other release gates remain NO-GO.
