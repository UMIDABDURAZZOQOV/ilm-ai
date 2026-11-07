# Real Google/Samsung staging acceptance — updated 2026-11-08

This records isolated HTTPS staging checks, not production approval. Google
selection, consent and age entry were performed by the owner. Account identities,
tokens, secrets and raw authentication logs are excluded from this report.

## Exact running sources

- Staging: https://ilm-ai-103-stage-8b0727.onrender.com
- Backend Live: `d587f9b56cb9aa54fb35f6bbf92af9dcf7a285f9`.
- Service `srv-dbniform8hqs73caemig`, deploy `dep-dbnlssm417fc73e49rn0`.
- Flutter application source: `23f696f3732d2bfdaef56a7b9940153e89be7e10`.
- Production remains `e97c029f341da172fc753ab07b44b783cdf13b5f` on `main`.
- Free web/PostgreSQL only; staging auto-deploy off, external DB access disabled.
  No production deployment, schema/import, OAuth/env or Play change was made.

## Actual Samsung SM-A125F acceptance

| Journey | Observed result |
| --- | --- |
| Account A registration | Real Google identity and owner-entered age; onboarding completed |
| Session restoration | Force-stop/relaunch restored the account without Google/onboarding |
| Five-subject switch | All five visible; real grade locks update between grades 6 and 7 |
| Save draft, logout, same-account Google login | Physics6 question 3/6 restored; no repeated age/onboarding |
| Physics6 MCQ lesson | Correct and incorrect feedback; 5/6 correct, two stars, +10 XP |
| Feedback explanations | Optional button after checked answers, reviewed fallback without provider; closes on next question |
| Chemistry7 theory and MCQ | Eight teaching screens, nine source-checked MCQs; no textbook links added |
| Chemistry7 correct FRQ | `Kimyo` and `Polimerlar` accepted on the current installed APK |
| Chemistry7 incorrect FRQ | Deliberate `test` rejected, expected `Alkaloidlar` shown; optional fallback explanation opened |
| Chemistry7 completion | 11/12, 92%, three stars, +20 XP; next lesson unlocked |
| Account A profile | 30 XP, two completed lessons, one-day activity; Physics progress retained after subject switch |
| Account B registration | Owner selected the second Audience-approved Google account; independent onboarding |
| Account B initial state | Chemistry7 starts at 0 XP / zero lessons; A's completion was not inherited |
| Account B restart | Same B session and 0/10 daily goal restored; onboarding did not repeat |
| Account B MCQ/FRQ completion | Nine MCQs and three FRQs; 12/12, 100%, three stars, +20 XP |
| Account B saved profile | 20 XP, one completed lesson, one-day activity; 10-XP daily goal |
| B logout, owner logs back into A | A restores exactly 30 XP / two lessons and its original 20-XP goal; no onboarding |
| Server identity evidence | Ten sampled profile access rows include two distinct auth and learning owners; counts only |

The real A→B→A journey passed: A's totals stayed30 XP/two lessons while B's
independently saved result stayed20 XP/one lesson. Different daily goals also
restored correctly. This is an observed two-account acceptance, not a proof of
all possible concurrent-device scenarios. Only owned staging accounts are used. Lesson clocks include lengthy QA pauses and are not performance data.
The generic Chemistry assessment did not replay the incorrect FRQ before its
completion screen; no automatic-remediation replay acceptance is claimed.

## Three real defects fixed

1. **Route-extra crash** (`e3571d3`): actual pushed-route serialization and auth
   refresh dropped `SkillTreeLesson`. A versioned route DTO codec and safe
   missing-lesson fallback preserve restoration. Existing source, prerequisite,
   auth and draft checks remain enforced. The corrected phone lesson completed.
2. **Authenticated profile404** (`d587f9b`): aggregation called preview-only
   guards in reviewed release. It now uses the same capability-checked adapter as
   tree/start/answer. Own profile200, other-user403, unchanged XP on GET, five
   subject aggregation and direct disabled-preview404 have regression coverage.
   No preview flag, schema or authentication bypass was introduced.
3. **Android FRQ semantics** (`470313d`, completed by `23f696f`): progress and the
   exercise prompt merged into the editable answer's accessibility value. Separate
   progress/exercise semantic containers now keep question and progress outside
   the actual answer. A widget regression and fresh UIAutomator empty-field
   guards were accepted by typing/submitting correct and incorrect real FRQs.

## Current-source tests

- Flutter `23f696f`: **1,375 full-suite tests passed**, concurrency1, 38:33.
- Current default targeted suite: **105 passed**; matching reviewed-staging
  contract suite: **10 passed**. These overlap the full suite; do not sum counts.
- Full `flutter analyze`: **No issues found**, 271.3s. Debug build: 192.1s.
- Earlier parallel full attempt exited1 after824 passes with incomplete tests;
  root cause was not established. Its log is retained. The complete serial
  current-source run above succeeded without loosening assertions/timeouts.
- A legacy `math` fixture run under reviewed publication flags had two failures;
  that subject has no published grades. Default fixture tests pass, and the
  appropriate reviewed contract tests pass. Publication guards were not weakened.
- Backend `d587f9b`, Linux CI42395951490: **5,334 passed,65 skipped,21 warnings**,
  5731.06s; import check and Docker build successful. Skips are not passes.
- Profile-fix targeted:13 passed/13 optional PostgreSQL skipped/one deprecation.
- Exact awake Live public preflight **9/9 passed**. Earlier source OAuth
  initiation/negative smoke12/12 passed; neither script alone accepts real login.

[Backend full CI](https://github.com/UMIDABDURAZZOQOV/ilm-ai/actions/runs/42395951490).

## OAuth, identity and isolation

The actual private Web-client filename remains `staging-google-oauth.json.json`;
the requested single-extension file does not exist. A read-only comparison on
2026-11-08 confirms that file's client ID/secret match active staging in memory
and its exact callback is valid. Adding test accounts to Audience did not rotate
the client. No secret or client ID is printed or committed.

Callback: `https://ilm-ai-103-stage-8b0727.onrender.com/auth/google-callback-mobile`.
Package `com.ilmai.app.staging`; scheme `ilmai-staging`; HTTPS needs no ADB reverse.
Test auth/preview flags and account deletion remain off. Strict staging validation
and separate production/staging client/database identity were verified earlier.
The final bounded sample contains10 profile rows, with two distinct owners on
both authenticated profile route families, recorded as counts only; no identifiers/raw logs are persisted.

## Current installed APK

`ilm-ai-beta-artifacts/ILM-AI-Staging-1.0.3-code4-23f696f.apk`

- 180,506,516 bytes /172.14 MiB; debug1.0.3/code4.
- SHA256 `0268df56e4bee55d097dbb885a3b46c0ade13dd04322eda463257419c430abe2`.
- Installed `Success` on Samsung without uninstalling or clearing data.
- 676 ZIP entries scanned: zero exact private OAuth values in plain/UTF16LE/
  base64, zero checked credential-format entries. This is a bounded scan.
- Real staging origin and separate native identity verified. Older ac168c3,
  e3571d3 and470313d artifacts are superseded for this acceptance.
- Existing Beta package/data retained. No production AAB built or Play upload.

```powershell
& C:\Android\platform-tools\adb.exe devices -l
& C:\Android\platform-tools\adb.exe -s R58NC0JNBXJ install -r C:\Users\Page\Desktop\Projects\ilm-ai-beta-artifacts\ILM-AI-Staging-1.0.3-code4-23f696f.apk
& C:\Android\platform-tools\adb.exe -s R58NC0JNBXJ shell am start -n com.ilmai.app.staging/com.ilmai.ilm_ai_flutter.MainActivity
```

## Remaining production gates

**Production NO-GO.** See [current release gates](PRODUCTION_READINESS_20261108.md).
Still required: production46-table baseline/verified backup restore and separately
approved migration/import/deploy, real deletion sender/privacy/storage acceptance,
Play-signed1.0.2 update/OAuth compatibility, external-provider configuration and
audience approval, exposed operator-key rotation, stable hosting/performance and
final production artifact acceptance. Verified lesson fallback works without AI.

Free host idle wake previously took156.09s/188s. A later bounded health read took
28.31s after timeouts; awake requests were fast. Failed timeout receipts remain.
The app's Retry restored the authenticated grade/draft after the server became
ready. No current cold-start SLA or release/profile benchmark is accepted and no
persistent keepalive is running. Desktop computer-use initialization failed;
Google authentication stayed with the owner throughout.

Receipts outside Git: `staging-final-current-flutter-validation-20261108.json`,
`staging-frq-final-apk-20261107.json`, `staging-two-account-device-acceptance-20261108.json`,
`staging-two-account-server-evidence-20261108.json`,
`staging-final-phone-warm-preflight-20261107.json`,
`recovery-profile-fix-ci-result-20261107.json` and prior non-overwritten logs.
