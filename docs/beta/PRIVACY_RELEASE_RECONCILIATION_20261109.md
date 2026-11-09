# Privacy / Data safety reconciliation for1.0.3

Unpublished engineering review. Do not paste this into Play Console or publish it
as an approved policy. Existing1.0.2 and candidate1.0.3 must be described accurately;
the former's production data flow must not be assumed to match current staging.

## Evidence and current implementation

Public privacy URL: https://ilm-ai-edu.vercel.app/privacy . Snapshot retrieved
2026-11-08, HTTP200, SHA256
564130be740429f37ebfe0aab1b48b20f8ed3df768adb8c7cc4f986a583ed5d8.
It names OpenAI and a data-sharing/model-improvement program. Reviewed1.0.3 staging
currently has no external AI provider configured; optional post-answer assistance
uses reviewed lesson explanations. Do not activate external processing by merely
adding a key without reviewing data flow, audience, consent and disclosure.

| Data / feature | Candidate code behavior | Required release declaration review |
| --- | --- | --- |
| Authentication | Candidate UI uses Google only, per latest owner instruction; verified subject/name/email/picture, server-signed sessions and encrypted local tokens. Legacy password contracts remain for older clients | Account management; Google and hosting/database processor roles; mixed-audience Google policy review remains open |
| Profile | Name, entered age, subject/grade/preferences | Necessity, consent/child treatment and retention before collection; age after login is not proof of parental consent |
| Learning | Answers, attempts, progress, XP/activity | App functionality and server synchronization; disclose linked account data |
| Notifications | Optional Firebase/FCM code; registration only when Firebase initialization succeeds | Inspect actual release configuration/merged manifest and network behavior; dependency presence alone does not prove collection |
| Media / files | Legacy dependencies and manifest include camera/microphone/storage; reviewed subject routes restrict available flows | Remove unnecessary permissions or document genuinely enabled use; verify final merged manifest and runtime requests |
| AI | No external provider accepted/configured in current reviewed staging; verified source fallback | Keep declarations version/configuration specific; do not claim all historical uploads were never sent externally |
| Support / deletion | Verified in-app/public-web reauth; separate final consent; manual email claims create review tickets and cannot delete accounts | Monitored contact, response time, operator verification and ticket retention must be established |
| Backups / security | Minimal UID tombstone/job receipts, token revocation; private encrypted backup rehearsal | Publish actual retention and restoration safeguards, not immediate physical erasure from every backup |
| Financial records | Retention-review state where necessary rather than falsely reporting erasure | Operator/legal decision and specific retention basis; no invented duration |

No ad/analytics collection is established merely from a dependency inventory.
Actual configured SDKs, hosting logs and enabled legacy services still require
deployment-specific reconciliation. Data safety collection/sharing classifications
must follow the current Console definitions and applicable processor exceptions.

## Draft wording for operator completion

ILM AI uses account and learning information to sign you in, personalize your
learning choices and synchronize your study results. The candidate app uses Google
sign-in for both registration and returning users. We use the verified Google
identity and the profile details authorized for that sign-in. The owner explicitly
removed the optional-password UI; this draft does not claim policy approval.
Your progress is associated with your authenticated account.

The reviewed lesson assistance in this release can show explanations based on the
lesson material. External AI processing is not configured in the tested staging
release. Any production AI service must be named here with the actual data sent,
purpose, audience restrictions and retention before it is enabled.

You can request account deletion in the app or through the external deletion page.
Ownership verification and your separate confirmation are required. A deletion
request is not reported as completed while cleanup or necessary retention review
is outstanding. Some minimal security records and provider backups may remain
subject to the specific periods and safeguards listed in the final policy.

**Complete before publishing:** actual production deletion URL availability;
operator/legal identity and monitored contact; approved age/parental-consent
procedure; per-category retention periods; backup expiry and deletion replay after
restore; manual ticket and financial record review operations; actual enabled
processors and cross-border handling. The existing public support address is not
evidence that its queue is monitored or a response deadline is implemented.

## Play review record

Owner confirms previous audience review passed. The supplied wizard text lists
age options and policy guidance, not selected checkbox states. New1.0.3 Data safety
and App access were not independently read or changed. Prepare reviewer credentials
privately for a dedicated non-production-data review account; do not publish test
tokens or production learner credentials. A previous approval does not substitute
for checking the new release's actual functionality and data handling.

## Official references

- [Google API user data policy](https://developers.google.com/terms/api-services-user-data-policy):
  Mixed-audience Google access requirements remain a release-review gate after
  the owner's Google-only decision. No age declaration was silently changed.
- [Families requirements](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en):
  declared audience, appropriate content, SDK/API behavior and child data handling
  must match the actual app. Do not silently change the audience to18+.
- [User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en):
  accurate privacy disclosures, secure data handling, in-app and external deletion.
- [Data safety guidance](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en).
