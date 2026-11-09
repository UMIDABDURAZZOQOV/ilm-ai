# ILM AI1.0.3 final AI/release audit — feature freeze

Scope: fix confirmed defects only. No new feature, redesign, paid service,
production deploy/database write, or Play submission is authorized here.

## 1. NVIDIA: actual owner-authorized authentication checks

The owner explicitly requested checking the eight credentials previously pasted
in chat. On2026-11-09 each was sent once, in a Bearer header, only to NVIDIA's
documented `https://integrate.api.nvidia.com/v1/chat/completions`, using the selected
`meta/muse-glimmer-30b` model and a tiny synthetic integration prompt. This
supersedes historical statements that these values had never been transmitted.

**All8 returned HTTP401. Zero authenticated inference responses.** This is an
actual rejection at that endpoint, not an inference from credential formatting,
and does not establish which service originally issued them. No rate/quota
response was bypassed. The diagnostic stops on any non401, including quota,
permission, success or network failure; no provider/key rotation was installed.

Credential input used a hidden terminal and process memory only. No values were
written into source/config/logs/APK/AAB; no raw upstream body or learner data was
persisted. Only sanitized status/index/timing receipts are outside Git:
`nvidia-disclosed-key1-auth-probe-20261109.json` and
`nvidia-disclosed-remaining-auth-probes-20261109.json`.

**Real NVIDIA model/staging quality evaluation remains BLOCKED.** There is no
accepted credential, configured private provider, or real Uzbek MCQ/FRQ inference
to grade. Verified lesson explanations remain the default. No failed auth result
is represented as a successful provider integration. An accepted private NVIDIA
credential and actual operator/audience/trial review are still required.

The existing NVIDIA adapter is an evidence-ID selector: it cannot introduce
generated scientific prose. Trial guards remain test+internalBeta only, never
production. Hosted trial terms restrict use to internal evaluation; free trial
access is not production entitlement. No paid capacity or other provider was
activated. Exposed credentials must not become final production credentials.

Official references rechecked2026-11-09:

- [NVIDIA API contract](https://docs.api.nvidia.com/nim/reference/meta-muse-glimmer-30b-infer)
- [Model card and governing terms](https://build.nvidia.com/meta/muse-glimmer-30b/modelcard)
- [NVIDIA API Trial Terms](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)

## Existing accepted baseline

Flutter implementation68d0697, documentationce1541f:1428 full tests passed,
analyze clean. Google-only debug APK installed, owner third-account login and
session restoration accepted. Recovery backendcc239d0 is Live on existing Free
HTTPS staging; exact-source9/9 public contracts passed.83critical coverage gaps
actually passed locally, plus one SQLite guard control; new backend full CI is a
separate pending gate. Existing signed AAB is verified but explicitly NO-GO.

No new application implementation fix has been made by this audit yet. Do not
rebuild unchanged artifacts merely to label them new. All remaining sections
must be completed with actual evidence or explicit blockers before a GO decision.

## Full CI follow-up: exact runtime provenance, not source relaxation

Run 42570996008, commit cc239d0: 5,455 passed, 2 failed, 11 skipped,
5,468 collected. The two failures were frozen-runtime comparisons in the
Uzbekistan and World History source suites. They detected the reviewed UTC
serialization change from commit 95847462f6c24aabc7c4d469be4940498f17bca5.
The original subject manifests and all textbook/content evidence are unchanged.

The existing pinned integration-review mechanism now also records the exact
original and current hashes of assessment_runtime.py, chemistry_runtime.py and
study.py. The first two only import/use iso_utc for the unchanged expiry instant;
study.py only adds that pure helper. No grading, reward, source or lesson changes
are authorized by this review. Unknown bytes, wrong original baselines, changed
review manifests and modified binary/source evidence still fail closed.

The combined source suites, timestamp and portability/tampering regressions
passed: **101 tests in 8.04 seconds**, including all six review paths. This is a
targeted result, not a replacement for the next exact-commit full CI. The eleven
Linux skips are Windows ACL tests previously executed successfully on Windows;
their separate local receipt is release-gap-accepted-summary-20261109.json.

## Phone and public API follow-up

The diagnostic profile APK from Flutter ce1541f (implementation 68d0697) was
installed with adb install -r, preserving staging data. On the connected Samsung
the first catalogue request timed out. A public cold sample also timed out;
the subsequent warm exact-revision preflight passed all 9 checks against
cc239d059a7db57d29bda9ef122b1f4eff6f0a80. These observations do not establish
the root cause or acceptable cold-start performance.

After the warm preflight, the visible retry button restored the Physics grade-6
lesson catalogue on the phone without logout or data clearing. A blank interim
capture was transient; it is not evidence of a permanent blank-screen defect.
Controlled profile measurements remain a separate acceptance gate. Production
read-only preflight still reports mobile endpoints 404; no production fix has
been deployed.
