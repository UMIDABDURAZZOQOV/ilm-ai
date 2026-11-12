# NVIDIA generated explanations: isolated QA and deployment contract

This is a new text provider, **not** a renamed trial evidence selector.
`nvidia_trial` remains unchanged. `nvidia_explanation` returns generated Uzbek
paragraphs alongside the original verified feedback/evidence. It never grades,
awards XP, writes progress or replaces the source-validated curriculum.

No private key/configuration is committed. No live result, deployment or Android
acceptance is implied by this implementation or its synthetic tests.

## Service and audience review

Model: `meta/muse-glimmer-30b`; pinned origin:
`https://integrate.api.nvidia.com/v1/chat/completions`.
The current [API reference](https://docs.api.nvidia.com/nim/reference/meta-muse-glimmer-30b-infer)
is used without unsupported structured-output parameters. Strict JSON is
requested in the prompt and validated independently. No tools, browsing or
reasoning output is exposed.

The [model page](https://build.nvidia.com/meta/muse-glimmer-30b/build) describes a
free prototype. The [Trial Terms,1.2/1.4](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
restrict trial use to internal evaluation; public production use needs separate
subscription/product terms. A free key is not production authorization.
The [general terms](https://developer.nvidia.com/legal/terms) and actual service
agreement must also be reviewed for audience, data processing and rights to
submit the original interactive lesson excerpts. Do not promise zero retention
or permission for children's data without reviewing the applicable agreement.

Both configurations require a reviewed free-only plan. Nothing purchases a plan,
changes billing or switches accounts when a quota ends. Nonempty reference
strings record operator provenance; they are **not** a legal certification,
consent mechanism or proof that a plan exists.

This implementation conservatively allows external inference only for an
authenticated profile whose server-side age is18–120. Unknown/child profiles
keep verified server-side explanations. This is a temporary integration scope,
not a claim that NVIDIA universally bans under18 end users, that self-reported
age establishes legal consent, or that ILM AI should be adult-only. The separate
mixed-audience account/guardian proposal and Google policy gate remain open.

## Private configuration, no secret in commands

Run `scripts/configure_nvidia_explanations.ps1` locally with a **new** private
directory outside every Git checkout. It applies and verifies an owner-only
Windows ACL before asking for a key with hidden input. It will not overwrite an
existing directory or follow a reparse path. It performs no API/server action.

```powershell
.\scripts\configure_nvidia_explanations.ps1 `
  -PrivateDirectory "$env:USERPROFILE\ILM-AI-secrets\nvidia-text-eval" `
  -Usage internal_evaluation `
  -UsageReviewReference '<actual internal-evaluation review>' `
  -AudienceReviewReference '<actual adult QA audience review>' `
  -DataProcessingReviewReference '<actual minimized-data review>' `
  -FreePlanReviewReference '<actual free-only account/budget review>'
```

Enter the confirmation and one fresh NVIDIA key in the local prompt. Never
paste it into chat, a command argument, Flutter define or artifact. Historical
disclosed credentials must be revoked/rotated by the account owner.

The saved `nvidia-explanations.json` has these exact fields:

- `provider`: `nvidia_explanation`
- `model`: `meta/muse-glimmer-30b`
- `api_key`: the private key (one only)
- `usage`: `internal_evaluation` or `authorized_hosted_application`
- `audience`: `adults_only`
- `free_only`: true
- `audience_review_reference`, `data_processing_review_reference`,
  `free_plan_review_reference`: actual operator review references
- `trial_review_reference` for internal evaluation, **or**
  `hosted_use_review_reference` for separately authorized hosted use

Internal evaluation requires `ENVIRONMENT=test` and `ILM_BETA_ENABLED=true` at
load and on **every** call. It cannot run in normal HTTPS staging/production.
The hosted configuration does not inherit a trial right; do not fabricate its
review reference to bypass the service agreement.

## Normal server startup

`main.py` configures optional AI only after the mandatory reviewed-source
warmup. A failed source check prevents AI setup and later startup hooks.
The new hook calls `configure_from_environment()`. With no
`STUDY_HELP_CONFIG_FILE`, no provider is loaded or contacted. When supplied, the
value is an absolute private filename outside Git; only the new explanation
provider is accepted. Raw `NVIDIA_API_KEY` discovery is deliberately absent.
Invalid explicit configuration fails closed without printing its contents.

HTTPS staging keeps `ENVIRONMENT=production`, preview/test auth disabled and an
isolated DB. A configured file additionally requires
`STAGING_EXTERNAL_AI_REVIEW_REFERENCE`; raw provider-key environment variables
remain forbidden. Do not change staging to test mode. Remote configuration or
deployment requires separate exact owner approval.

## Isolated local Android evaluation

With an actual authorized internal configuration, use a **new synthetic** local
Beta directory. Do not resume the owner's existing account/progress sandbox.

```powershell
python -X utf8 scripts/serve_mobile_beta.py `
  --directory '<new owned local QA directory>' `
  --port 8931 `
  --ai-config-file '<absolute private nvidia-explanations.json path>'
```

Port8931 avoids replacing an existing8930 backend. The debug Beta Android app
uses its existing loopback8930 origin; USB can map it to host8931:

```powershell
C:\Android\platform-tools\adb.exe devices -l
C:\Android\platform-tools\adb.exe reverse tcp:8930 tcp:8931
```

Only install/open a matching isolated Beta artifact after checking device and
package identity. Never uninstall, clear data or overwrite a protected Staging/
production account as a shortcut. Real user authentication remains owner-operated.
Creating this runbook does not mean a backend was started or a device tested.

## Backward-compatible wire protocol

New Flutter sends `X-ILM-Study-Help: nvidia-text-v1`; no new JSON request field is
added to the old extra-forbid schema. Old backends ignore the header and keep
verified fallback. New backends return generated mode only to capable clients,
after an owned issued question is checked and eligibility passes. Old Android
receives its original `reviewed_evidence` schema and no upstream call.

Success: `mode=generated_explanation`, `provider_status=generated`, the original
context/evidence plus `generation` containing pinned provider/model, usage,
HTTP200, opaque request ID, request/response hashes, Uzbek paragraphs and valid
evidence IDs. These receipts are not a global `LIVE_AI_VERIFIED` certificate.
Flutter checks context/provenance and renders the actual paragraph text in a
separate card; the verified solution remains visible below. A question/account
change retains existing cancellation/close behavior.

Fallback keeps `mode=reviewed_evidence`, no `generation`, and status
`unconfigured`, `answer_required`, `audience_unavailable`,
`client_upgrade_required` or `unavailable`. It preserves grades/XP/progress.

## Privacy, grounding and reliability limits

Only reviewed subject/grade/title/question, server correctness and referenced
lesson/solution snippets go upstream. Raw FRQ text, selected learner text,
follow-up message, user/attempt IDs, age, email, source filenames/paths, OAuth
tokens and secrets do not. The model must not guess which choice was selected
when that information is absent. Diagnostic feedback already comes from the
existing grader, not the model.

Each paragraph must include an exact supplied quote and valid evidence IDs;
wrong grading flags/language labels, invented references/numeric quantities,
obvious sensitive/HTML/link output, truncation, tools and malformed JSON are
rejected as a whole. These mechanical checks cannot prove semantic entailment,
Uzbek fluency, suitability or the truth of every generated sentence. Actual
subject review and safe audience acceptance remain mandatory before release.
Generated text is never persisted as a verified textbook fact or answer key.

Two inference slots, existing per-process20/minute and1000/day admission,
bounded body/envelope, connect/read/overall deadlines, a finite circuit and at
most one same-key transient retry are used. Auth/permission/quota/rate responses
never trigger cross-account rotation. Per-process limits are not a distributed
billing or capacity guarantee. All provider waits occur after releasing the
read-only DB connection. Optional inference must not affect grader transactions.

The route also stops waiting after18seconds even if an underlying resolver or
driver ignores its socket timeout. Its response uses already verified evidence;
it performs no second provider request. An abandoned worker keeps its inference
slot until completion, so two stalled transports cannot create an unbounded
upstream request pool. The wall-clock regression reproduced20.078seconds before
this change and18.157seconds after; all faults use synthetic transport.

## Verification

Tests use actual catalogue questions on new owned databases and synthetic HTTP
transport. Keep those separate from authenticated live provider+Android proof.
The backend exports source-bound case receipts; the optional Flutter
`tool/qa/nvidia_backend_contract_test.dart` consumes the exact response text from
an explicitly supplied local contract file, not a live model fixture.

The current external receipts live under `ilm-ai-beta-artifacts/`; refer to the
latest `NVIDIA_AI_LIVE_VERIFICATION.md` and `FINAL_GO_NO_GO.md`, not a green
unit test count, for release status. No model invocation, deployment, GitHub
push, database migration or Play upload is authorized by this document.
