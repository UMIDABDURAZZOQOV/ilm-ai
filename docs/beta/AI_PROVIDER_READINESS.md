# AI provider readiness — 2026-11-06

## Actual state and decision

The user confirmed the supplied credentials belong to **Google AI Studio**.
They were disclosed in chat and must be revoked/replaced at the provider. No
credential value was copied to a repository, private configuration, APK, report
or provider request. Do not print the attachment unredacted or repeat credentials.
The attachment's complete 195 lines were read with credential redaction.

**Google AI Studio / Gemini Developer API is not connected to ILM AI.** Its
[current additional terms](https://ai.google.dev/gemini-api/terms), effective
2026-03-23, prohibit API clients directed towards or likely to be accessed by
under-18s. ILM AI serves school pupils. This is the user's explicit requirement:
do not activate a provider whose terms do not fit the audience. Do not route these
Google credentials to OpenAI or bypass this restriction with account switching.
Do not generalize this finding to all Google Cloud products: a separate enterprise
service, contract and privacy review would need independent evaluation.

[Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) are per
project, not per key. Eight keys do not establish eight independent allowances.
[Google API terms](https://developers.google.com/terms) require express consent
for use beyond assigned limits. Use approved capacity/billing, not free-account
quota hopping. The previous generic seeding/legacy adapters are separate and were
not wired into student study help or changed by this patch.

## Source-bound fallback and optional selector

No key remains the default: reviewed textbook explanations work without external
inference. The existing MCQ/FRQ grading, awards, prerequisites, source validation,
answer-result-only Flutter entry points and progress formats are unchanged.

The optional **existing OpenAI evidence-ID selector** has been hardened; this is
not activation of a new OpenAI subscription or approval of that provider for all
ages. [OpenAI under-18 guidance](https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance)
requires safeguards; under-13 personal data needs the specified retention/privacy
controls. Account-level retention settings and an operator's audience/privacy
review have not been verified. Leave inference off pending that review.

- Credentials: explicit private JSON secret mount outside every checkout, no
  symlink paths, no automatic environment-key discovery, max 32KB, strict schema,
  unique 1–8 keys. Known Google credential formats and non-OpenAI provider fields
  are rejected before any external call. Old `api_key`/`model` configs now fail
  closed; migrate deliberately after review, not by copying exposed keys.
- Exact config fields: `provider` (`openai`), `model` (operator-approved available
  model), `api_keys` (private list), `audience_review_reference` (the actual review
  record reference). This reference is operator provenance, **not automated legal
  verification**. Config errors never print file contents or upstream messages.
- Endpoint remains fixed to `https://api.openai.com/v1`; no arbitrary base URL.
- External payload: server-reviewed subject/grade/title/question and teaching
  snippets' IDs/kinds/text only. No follow-up text, selected answer, correctness,
  account/session IDs, tokens, source metadata or grader feedback/solution is sent.
  Feedback and solutions are appended locally from reviewed server evidence.
  User-authored follow-ups continue to receive the reviewed lesson material;
  this adapter does not answer unrestricted personal messages with generated text.
- Structured JSON IDs only, at most 12 unique whitelisted IDs. Unknown IDs,
  malformed output, unexpected fields, refusal or errors use reviewed fallback.
  Generated prose never replaces scientific facts or the authoritative grader.
- `store=false`; this alone **does not establish zero data retention**.
- 24,000-character input ceiling and 1,024 completion-token ceiling per call.
- Two concurrent calls, nonblocking admission; at most two network attempts per
  request with 6s SDK timeout per attempt and SDK retries disabled. These are
  network-attempt bounds, not a measured hard end-to-end latency guarantee.
- Failed attempts consume the same 20/minute and 1,000/UTC-day per-process budget
  as successes. These do not provide a durable distributed monetary cap. Before
  production/multiple workers: shared durable rate/budget accounting, provider
  billing hard caps, monitoring and reconfiguration policy are still required.
- 401 disables the invalid key until reconfiguration; connection failure or 5xx
  can try a configured authorized standby once. Timeout, 400/403/404/422 and bad
  model output immediately fall back. Retry-After pauses the entire pool without
  blocking a request thread with sleep. 429 never hops to another account.
- Explicit credit/spend/quota exhaustion disables external selection across the
  pool until operator reconfiguration. Limits are not silently increased.
  See [official error handling](https://developers.openai.com/api/docs/guides/error-codes).

## Configuration without exposing credentials

Leave `--ai-config-file` omitted to keep source fallback. If a compatible provider
and audience review is completed later, the operator provisions **new** credentials
through the hosting secret manager mounted as a private JSON file outside the
checkout, then supplies its path with `--ai-config-file`. Do not send new keys in
chat or pass values in CLI arguments, dart-define, APK, logs or Git.

The running port8930 server has intentionally **not** been restarted or configured
with external AI: existing phone sessions and progress remain on the unchanged
running process. A source-only backend update needs a controlled restart before
its new adapter code is live; tests exercise disposable processes/fixtures.

## Production status

Readiness is **NO-GO**. Provider keys do not resolve missing production mobile
auth/catalogue APIs, five-subject publication, deletion workflow, Data safety,
real OAuth/Play upgrade or handset performance acceptance. See Flutter
`docs/PRODUCTION_UPDATE_AUDIT.md` and the backend production handoff. Existing
signed artifacts remain the previous candidates; no new release was uploaded.
