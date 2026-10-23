---
name: monday-workflow-specialist
description: "Specialist for the ADVANCED blocks of monday.com's Workflow Builder - the webhook trigger ('When a webhook is received'), the Code block (Python), HTTP request and API call, Run any MCP action, JSON Parser, Categorize with AI, loops, run-once/manual trigger and the external-app blocks - and the patterns that combine them: one workflow serving N boards, cross-board lookups and writes, status guards, team/user provisioning, external systems posting into monday, calling external APIs. Use whenever the ask involves a webhook trigger or payload, 'Code block'/'code node', HTTP request block, calling api.monday.com from a workflow, parsing JSON in a workflow, 'what else can the Code block do', 'can a workflow do X that no native block does', Code output binding failures, 'Code block must return an object', or consolidating N near-identical workflows. Owns block-level capability and implementation patterns; monday-workflow-architect still owns automation-vs-workflow, tiers, limits and the build sequence via the MCP workflow tools. Not for board schema (monday-solution-architecture) or formulas (monday-formulas)."
---

# monday Workflow Specialist - advanced blocks and patterns

Know what each advanced block can and cannot do, pick the cheapest block that does the job, and build patterns that survive production. Everything below carries an evidence grade. Do not present C or D items to a client as fact.

## Evidence grades

| Grade | Meaning |
|---|---|
| A | Machine truth (planner/MCP catalog, API schema, DaPulse source code and commit history) or tested by Basti in a real account with output seen |
| B | Owner announcement (Slack product-updates, owner reply) or official support/developer docs |
| C | Expert tool or docs read, not independently tested; or API call ran but end effect unobserved |
| D | Field report, bot answer, colleague report, my inference |

Only A/B go into client commitments. Full ledger with sources and open questions: `references/evidence-ledger.md`.

## Step 0 - Is this the right skill and the right engine?

1. Automation vs Workflow Builder, tiers, quotas, active-workflow caps: `monday-workflow-architect` Gate 0 and Gate 1. Do not re-derive here.
2. Needs only one board and native blocks? Stop: build native. Native is maintainable by the client admin.
3. AI-judgement steps (classify, summarise, extract)? Native AI blocks first, scoped via `aitp-advisor`.

## Design stance: built to be handed over

Assume the consultant leaves, the client admin cannot read Python, and the creating user, any token holder or the whole integration may be deactivated later. The best option is the one that keeps running and can be understood with no one from us. So rank every candidate by how it fails after handover, not by how fast it is to build.

| Rank | Option | Why it survives or not |
|---|---|---|
| 1 | Native blocks only, one board per workflow | Client admin can read and edit it. No secrets. |
| 2 | Native plus native AI/parse blocks (JSON Parser, Categorize with AI, Information extractor) | Still no code and no secrets. AI blocks draw credits. |
| 3 | Code block | No token to expire (auth is injected, A), but the client cannot maintain Python and it runs under the account and user of the auth context, so a deactivated creator may break it (C, inference from source, untested). Needs documentation and a named owner. |
| 4 | MCP block with OAuth | Tied to the connecting person's grant. Dies when that user or grant goes. |
| 5 | HTTP block with API token | Last resort. Token comes from the Credentials app, usually a person's or app's secret. Expires, rotates, or goes with the user. Visibility to workflow editors unverified (C). |

Rules that follow:
1. Pick the lowest rank that does the job. Moving down a rank needs a stated reason in the design doc.
2. API tokens are only for systems we cannot reach otherwise. Never use a token for monday's own API: Code (rank 3) or native blocks cover it.
3. Prefer N simple native workflows over 1 clever webhook+Code workflow when N is small and the active-workflow cap allows it. The clever version has more moving parts (sender recipes, parse, Code), and one failure stops all boards.
4. If Code is unavoidable: under about 40 lines, one job, comments that say why, a header with owner and date, a fallback plan if it is switched off, and the code pasted into the client handover doc.
5. Ownership: build under a named service or admin account the client controls and keeps licensed, never under a consultant seat. Record it in the handover doc (the creator single point of failure is in `monday-workflow-architect/references/limits-and-failure-modes.md`).
6. Every workflow gets a failure path that notifies a client owner, and a one-page runbook: what it does, what it depends on (user, token, URL, board IDs), how to disable it safely.
7. State plainly in the recommendation what happens if the creator, token or integration is deactivated.

## Step 1 - Pick the block (cheapest that works)

Walk in order, first yes wins. This ladder applies the ranking above.

1. Native block exists for the exact action? Use it. Catalog: `references/capability-matrix.md` (block IDs, A-graded 2026-10-23).
2. Need to split a JSON string into fields? Try JSON Parser (JSONata, 20264061) or Information extractor before Code (C: not tested on webhook bodies; Code parse is the owner-documented path, B).
3. Need loops, lookups and conditionals native blocks can express in more steps? Use more native steps. More blocks is fine, Python is not.
4. Native cannot express it (read-modify-write, per-board lookups, computed conditionals, monday API or MCP calls, parsing nested payloads)? **Code block**, under the handover rules above.
5. Need a third-party app via OAuth with no dedicated block? **Run any MCP action** or the app-specific variant. Document whose grant it uses.
6. Need a non-monday HTTP endpoint and nothing else works? **HTTP request and API call**, last resort, with a named token owner, rotation plan and the exposure caveat. Code cannot reach it (egress is monday API + MCP server only, A).
7. Open-ended reasoning over input? Agent blocks, hand to `monday-agents`.

Code vs HTTP for monday's own API: always Code. It needs no token. HTTP would need a Credentials-app token and supports GET/POST/PUT only (B).

## Step 2 - What each advanced block really does

### Webhook trigger "When a webhook is received" (22970502)
- One unique URL. Request JSON body arrives as ONE string field `body` (B, Oct 6 release). Fields are not auto-split; parse in a Code block (owner snippet) or JSON Parser.
- No standalone "Get webhook data" action exists (A, planner). The 15 Oct partner announcement names it, but the data is emitted by the trigger. Treat as naming, not a block.
- The URL is the credential. Never paste it in docs or screenshots (D).
- The public route acks 200 immediately and publishes to a queue (A, source). HTTP 200 never proves a run started. A deactivated, expired or unknown URL is silently dropped, also with 200. Always confirm in Run history.
- No auth, no HMAC signature, no per-webhook rate limit, no custom response (A, design non-goals). Empty body arrives as `"{}"`.
- Reactivation bug (Sep 23): fixed in code 24 Sep, "reactivate deactivated webhook on subscribe instead of failing" (A, commit #1830). Same URL persists across deactivate/reactivate. Not field-verified, so still test activate -> deactivate -> reactivate -> real POST before handover.
- A URL generated in the builder is held pending and expires if the workflow is not activated (TTL raised from 1 h to 12 h, A, commit #1690). Activate the same session.
- Details and the N-boards-to-1-workflow pattern: `references/webhook-patterns.md`.

### Code block (23557427)
- Python 3.11, top-level statements, `input["name"]`, ends with top-level `return {...}` dict (A, source: your code is grafted into a function body, so `return` works). `print()` is allowed. Declared outputs must match returned keys, names must be valid identifiers, types string/number/boolean/array.
- Preinstalled: pandas, numpy, matplotlib, pillow, requests, httpx, openpyxl and other Excel readers (A, sandbox README). No pip install possible (egress blocked).
- Network: default-deny. Only api.monday.com and mcp.monday.com (path /mcp) (A, code-execution invariants). Auth is injected outside the sandbox as a bearer token for the run's account and user, narrowed to the caller's scopes, valid about 6 min (A). You never handle a key. Which user the writes are attributed to is still unconfirmed.
- Limits (A, source): timeout 300 s, code max 1 MB, output max 512 KB. The block is NOT retried on failure, because code may have written data (A). Execution is rate limited per account; a 429 shows as "Code block rate limited" (A), the numeric limit is in a config not readable here.
- Run history shows config and trigger item, Output tab can be empty on failures (D). Add your own error fields.
- Incident Oct 13-14: outputs over about 4 KB were cut off in transit, producing "Code block must return an object". Owner team reported fix on Oct 14 (B). Real cap is 512 KB (A); a clear error "output exceeds maximum size" appears above it. Still prefer returning IDs and pointers, not payloads (design rule).
- Known open bugs (D, two independent reports): Code output bound to Change column value / Update item saves as null and fails validation with MISSING_REQUIRED_INPUT. Safe pattern: do the write inside Code via the API, or route through a native text/number step only after validating.
- Cookbook, templates and use-case catalogue: `references/code-block-cookbook.md`.

### HTTP request and API call (15947681)
- Methods GET, POST, PUT. URL must be public http(s), no private network addresses (B).
- Auth: pick a token from the Credentials app, reference as `{{token}}` in a header, e.g. `Authorization:Bearer {{token}}`. If the placeholder is not in a header the token is not sent (B). Headers are `name:value` lines, no spaces.
- Errors: 4xx/config errors stop the run; 5xx/timeouts retry (severity 2000) (B). Run history shows full input and output (B).
- Counts against the target's limits. Calls to api.monday.com count toward the account API quota (B).
- Open: who can read the token or see it in run history. Do not promise secrecy (C).

### Run any MCP action (22629575) and app-specific MCP blocks
- Core block reaches arbitrary MCP servers; app-specific variants exist for monday, GitHub, Slack, Google Drive, HubSpot, QuickBooks, Confluence, Canva, Dropbox (A, ids in matrix). OAuth-protected apps supported (B, Sep release).
- Prefer the app-specific block when it exists.

### Loops, manual/run-once, conditions
- Loop over item/subitem/user collections exists (B). No loop inside a loop (D).
- Manual trigger and run-once (test now, and by chat/MCP) exist (B). Run-once on a live workflow can write real data. Test on a test board.
- Conditions: Smart condition (AI), If text matches (multi-branch), Categorize with AI (one label from your list, step fails if none fits) (B).

## Step 3 - Design rules for production

1. Split `ok` (payload parsed) from `relevant` (this event should act). Notify only on `ok=false`.
2. Return every Code output as a string. `str(False)` is `"False"`.
3. Wrap Code in try/except. On failure return `{"ok":"false","error":"..."}`, never raise.
4. Idempotency: webhooks and run-once can double-fire. Store a dedupe key (event id, `triggerUuid`) or make the write idempotent.
5. Blast radius: one deactivated webhook workflow stops every sender. Use a service user as creator, keep old workflows paused (not deleted) for 1-2 weeks, add a failure notify path.
6. Archiving or deleting the trigger item can deactivate a workflow (D). Design triggers on items that are not archived by other automations.
7. Governance: no confirmed admin switch to disable the Code block per user or group (Sep 2 question unanswered, D). For regulated clients (bank, public sector) raise it as an open question before promising Code.
8. Never autonomously post or notify real users from tests. Use a test board, test user, say so before running.

## Step 4 - Build sequence (delegates to monday-workflow-architect Part B)

1. Capture ONE real payload from the sender. Never map from memory.
2. Create the shell and trigger via MCP (`create_workflow`, `invoke_workflow_expert`). The expert tool cannot set the Code editor (requires-schema-override, A).
3. User pastes Code as a FULL file, declares inputs/outputs in UI, saves. Check the generated input names (`code_output_<field>`).
4. Test Code in the editor with the captured payload plus negative cases. The editor Run hits live data.
5. Add conditions and notify blocks only after Code outputs are saved.
6. `validate_workflow`, then explicit approval before `publish_workflow`. Omitting `workflowDraftId` addresses the LIVE version.
7. Post-publish: send one real event, read Run history, confirm Output, record the editor link via `get_workflow_editor_link`.

## Output format when advising

1. Recommendation in one line (which block combination).
2. Block chain with IDs.
3. What is A/B vs C/D, one line each.
4. Risks and the test that retires each.
5. Hand-off: `monday-workflow-architect` (build), `monday-build-docs` (document), `monday-scaling-watch` (limits), `aitp-advisor` (AI scope).

## Freshness

This area moves weekly. Before quoting any capability to a client, check `references/changelog.md` and the Slack owner channels in the ledger (#ai-workflows-product-updates, #partners-workflows-updates, #ask-ai-workflows). The weekly-pulse audit tracks the claims in `weekly-pulse/references/audit/claims.csv` (rows C049+).
