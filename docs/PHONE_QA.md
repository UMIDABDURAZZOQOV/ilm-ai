# Five-subject Android phone sandbox

Only branch/worktree `qa/android-five-subjects` integrates the existing reviewed
Biology, Physics, Chemistry, Uzbekistan History and World History adapters.
Original feature branches and main remain untouched. This is not publication,
production startup, a migration against an existing database, or an AI feature.

## Integration inputs

| Subject | Backend feature commit | Lessons |
| --- | --- | ---: |
| Biology | c0f84d0603905393904083f59f5d2a61a125c9bd406 | 406 |
| Physics | e2aab00ecac29294600a3ac4e5e95d5299c3eeaf | 316 |
| Chemistry | 9b37213cfeeebb358f2179d76c8c5d97417f18612 | 268 |
| Uzbekistan History | 1a4f9823f52cd2bbd738efab5437ecb3b201275d | 172 |
| World History | 8a7556a6da0bef14089c2753ab95d4d9a92c9a83 | 219 |

Physics is an ancestor of the Uzbekistan History integration input. World History
already includes the reviewed Biology/Chemistry runtime. The normal `main.py`
was retained byte for byte from the World History base; the new standalone server
mounts the adapters without importing production startup or modifying their gates.

## Ownership and source safety

`scripts/serve_phone_qa.py` requires a new directory outside Git, or explicit
`--resume` with an owned sandbox marker and existing owned SQLite file. It never
accepts a database URL or remote host argument. It sets environment and random
JWT secret before importing services, creates a new synthetic account (990005),
imports every reviewed lesson through the existing validators, and checks actual
counts. The existing three subject-specific staging filename checks all remain.

Windows `core.autocrlf=true` changed checkout bytes for newly integrated Physics
and Uzbekistan History JSONs. Their Git object bytes were restored unchanged and
LF checkout attributes added. No SHA manifests or source validators were weakened,
regenerated or reapproved. PDFs, full extracted texts and credentials are not added.

The app binds only to 127.0.0.1:8925 and rejects forwarded/non-loopback requests.
The one-time pairing code expires in 10 minutes and locks after 5 failed tries.
Tokens are issued at runtime, stored by the ordinary auth system, and never
compiled into Flutter. Signup, email reset/diagnostic, Google exchange/callback
and tutor routes are blocked in this server. Google credentials are empty.
Original OAuth code and all original preview gates remain unchanged.

Use fictional profile information. The private sandbox folder contains secrets,
SQLite state and transient pairing code; it is outside Git and must not be shared.
Resume is idempotent and preserves QA progress. Do not copy production data here.

See the companion Flutter worktree's `docs/PHONE_QA.md` for installation, pairing,
build commands, adapter limitations and manual handset checklist. In particular,
Biology has existing v1 MCQ; other subjects have their existing v2 preview FRQ.
A QA hub and shared XP do not claim a fully unified five-subject production UI.

## Tests

`tests/test_phone_qa.py` creates its own separate owned temporary database. It
checks all five authenticated catalogues, no private grading spec leakage,
idempotent full imports, single-use/expired/locked pairing, local host/peer guards,
auth requirements and the absence of email/AI endpoints. It never uses the phone
sandbox's user progress or tokens. Run separately from other fixtures, whose
module-level DB imports intentionally patch their own repositories:

```powershell
$env:PYTHONUTF8 = '1'
python -X utf8 -m pytest tests/test_phone_qa.py -q --basetemp C:/Users/Page/Desktop/Projects/ilm-ai-phone-qa-test-run
```

No Google end-to-end, native handset visual, IME or TalkBack verification is implied
by these automated checks. Android installation must use the distinct QA package.
