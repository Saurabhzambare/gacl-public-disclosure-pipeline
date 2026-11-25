# Security and data handling

- Use only the official public report URLs in config/sources.json.
- Never add SAP credentials, plant network details, employee records or internal files.
- Keep .env files, credential JSON, SQLite databases and logs outside Git.
- Use Google Application Default Credentials for local cloud authentication; do not paste credential contents into issues or documentation.
- Cloud deployment is optional and not performed by the local pipeline.
- Review staged changes before committing and review outputs before sharing.
- If a credential is accidentally committed, revoke/rotate it through its issuer; deleting a file alone does not remove history.
- Report project defects through a private channel to the repository owner. Do not disclose secrets in public issues.

## Phase 2 — public-document AI boundaries

The current local retrieval prototype is read-only and has no LLM, model-selected
tools or shell execution. Quoted lexical terms and parameterized filters prevent
user question text being executed as SQL; this is not evidence of an LLM passing
prompt-injection tests. Hashes detect source/configuration mismatch; an editable
local index is not a signed or tamper-proof security boundary.

The following are requirements for planned implementation, not claims of existing
agent protection:

- Treat PDF passages, questions and tool results as untrusted data. Embedded
  instructions must not alter tool permissions or reveal secrets.
- Expose only validated read tools for approved source pages, metrics,
  comparisons and identified check results. No arbitrary shell, write-SQL,
  manifest changes, private endpoints, external messaging or plant operations.
- Enforce tool/provider-call, time, token and output limits in code. Start with
  a proposed six-tool-call cap and test exhaustion, errors and repeated calls.
- Keep model files, vectors, raw prompts/responses and traces out of Git. Review
  curated summaries for sensitive content and source-material rights before
  sharing. Do not request or publish hidden model reasoning.
- Verify model/runtime license, revision, dependencies and laptop suitability
  before installation. Pin compatible embedding/index metadata; reject stale
  models or dimensions rather than silently switching.
- An external generation provider requires an explicit cost/data-flow decision
  before use. Keep credentials in approved local secret mechanisms, never
  configuration or example prompts. Public sources do not make arbitrary user
  questions safe to disclose to an external service.
- Render retrieved text and model output as data, with escaping appropriate to
  the selected interface. No generated code or HTML is implicitly trusted.
- Preserve numerical/claim limits: no unsupported cause, live reading, private
  access, regulatory certification or accidental KL/day-to-KL aggregation.

Test actual model/agent behavior separately once it exists; a safe-looking prompt
alone is insufficient. See [contracts](docs/AI_CONTRACTS.md),
[evaluation plan](docs/AI_EVALUATION_PLAN.md) and
[build order](docs/PHASE_2_BUILD_ORDER.md). Documentation and development do not
authorize publication, deployment or outreach.

