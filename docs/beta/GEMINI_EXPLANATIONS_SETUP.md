# Gemini explanation integration (local QA)

The selected provider is now Google AI Studio / Gemini. This adapter uses
`https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`
and `gemini-3.1-flash-lite`. It never sends Google credentials to NVIDIA or
OpenAI. The legacy `services/gemini.py` OpenAI wrapper is unchanged.

Official references, checked 2026-11-13: [REST compatibility](https://aistudio.google.com/docs/openai),
[model](https://aistudio.google.com/docs/models/gemini-3.1-flash-lite),
[key types](https://aistudio.google.com/docs/api-key),
[pricing](https://aistudio.google.com/docs/pricing#gemini-3.1-flash-lite).

## Runtime contract

- `gemini_explanation` is a separate private configuration provider.
- Only checked, owned MCQ/FRQ questions with reviewed evidence are eligible.
  No identity, age, access token, raw learner answer or follow-up message goes
  upstream. Grade/title/question and original evidence snippets are sent.
- The existing server-side adult-profile guard is retained. Internal evaluation
  requires `ENVIRONMENT=test` and `ILM_BETA_ENABLED=true` at load and every call.
  This is not certification that a mixed-age production client meets terms.
- New Flutter capability `reviewed-text-v2` accepts an exact provider/model pair.
  Old NVIDIA-only clients receive reviewed fallback for Gemini. New clients
  still accept NVIDIA. Old servers ignore the new capability and retain fallback.
- Google's minimal reasoning and JSON response mode are used. The prompt
  explicitly requires supporting quotations to appear literally in each paragraph.
  Quotes, references, numeric quantities, envelope/model and grading flag are
  checked. This mechanical validation is not proof of semantic correctness.
- Two concurrency slots; shared local budgets; 16-second internal deadline,
  12-second socket read ceiling and existing 18-second API wait ceiling. Quota,
  credential failure, malformed or ungrounded output returns verified fallback.
  No cross-account quota rotation or billing activation.

## Private configuration

Use a private JSON outside every Git checkout, protected by owner-only ACL.
The fields match `NVIDIA_EXPLANATIONS_SETUP.md` except:

- `provider`: `gemini_explanation`
- `model`: `gemini-3.1-flash-lite`
- `api_key`: one Google standard or authorization API key

`usage`, `audience`, `free_only` and review reference fields remain mandatory.
Nonempty references are operator provenance, not legal approval or proof of an
account's billing tier. `free_only` records intent; it does not disable billing
on an externally managed Google account. No paid plan is enabled by this code.

Local server:

```powershell
python -X utf8 scripts/serve_mobile_beta.py --directory '<owned-local-beta-directory>' --resume --port 8931 --ai-config-file '<absolute-private-json-path>'
```

Normal hosted startup can read `STUDY_HELP_CONFIG_FILE` after source validation,
but **no hosted Gemini deployment is performed or approved by this change**.
The owner deferred audience/service decisions; those release gates remain open.
The chat-disclosed test credential is not a releasable production credential.

## Evidence scope

On 2026-11-13 a real Google models GET returned 200 and listed the selected model.
A real internal synthetic generation later returned 200 and passed the unchanged
grounding validator in 2.235 seconds. Earlier rejected output and a transport
timeout are retained in local artifacts. This proves bounded live adapter
operation, not all-subject Android E2E or production readiness.

Artifacts: `probe-gemini-auth-20261113.json`,
`probe-gemini-generation-20261113.json`, `GEMINI_LOCAL_ACCEPTANCE_20261113.json`.
No credential belongs in those receipts, Git, Flutter defines or APK/AAB.
