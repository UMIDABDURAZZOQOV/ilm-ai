# Frozen subject baselines and reviewed shared-runtime integration

Original subject manifests remain unchanged. The first Linux full CI run exposed
two independent issues in their coarse whole-file preservation tests:

1. Historical Python files were hashed with Windows CRLF. Git Linux checkouts
   contain LF. One JSON outline had the inverse representation locally. Only
   CRLF/LF representation of `.py`/`.json` is made portable; no stripping, JSON
   reserialization, alias/fact/source mutation or PDF/image hash exception exists.
2. Three shared runtime files had previously authorized integration changes.
   Their diffs against the subject checkpoint were reviewed explicitly:

| File | Reviewed change | Evidence |
| --- | --- | --- |
| services/curriculum.py | Same per-lesson validator/immutability; catalog preparation shared only within one caller transaction | Fresh PG and actual46-table structural clone import/reimport/137XP preservation; cache scope rejects another DB/catalog |
| services/db.py | Import-time production ALTER calls disabled; explicit migration policy | Production startup AST regressions and actual PG/main contract |
| main.py | Reviewed router mounting/deletion install, secure sessions, safe lifecycle, explicit migration policy, source warmup before-ready |197 legacy method/path fixture, real main PG acceptance, startup tests and actual hosted staging SHA/API checks |

`shared_runtime_review_20261107.json` binds each exact original subject-manifest
hash to the exact current LF hash at reviewed source23d9ed3. The test helper pins
that review document's own digest and permits only these three runtime paths.
Unknown runtime changes or a different original baseline still fail. Biology,
Chemistry, Physics/history lesson/source/catalogue/rubric files receive no such
override. This review is technical integration evidence, not textbook fact or
expert approval. The original subject feature branches are not modified.

Tests prove unknown code changes, changed source claims, PDF bytes, forged review
documents, wrong original hashes and later changes to approved runtime files are
rejected. Both original preservation tests pass with all687 world-baseline and
552 Uzbekistan-baseline records checked.5 targeted portability/preservation
tests passed; they do not establish a passing whole backend suite.

## CI fixture corrections

The old full run42374751415 produced5224 passed,2 failed,64 skipped,77 fixture
errors. A new google-genai dependency pulled httpx2 2.16.0; Starlette uses that
transport while the World History fixture inherited httpx.Auth. Callable auth
now supports both transports, still issues real JWTs and preserves explicitly
provided expired/other-owner headers. Actual expired JWT401 regression passed
under an isolated httpx2 2.16.0 install; application authentication is unchanged.

Full-suite collection can cache services.db before Beta config. The Beta fixture
now always creates/patches its own engine/factory and restores configured env on
teardown/skip. Production/local-only/source gates are unchanged. The targeted
cached-engine/real-auth/expiry scenarios passed3 tests with the CI transport.
Broader targeted and corrected full CI results must be recorded separately; an
old failed run or pending rerun is never described as full-suite success.
