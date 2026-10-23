# Evidence ledger and open questions

Snapshot 2026-10-23. Primary sources: DaPulse source read-only via your gh login - automations-framework (core-blocks/run-code-block, webhooks-app, openspec/webhook-received-trigger), code-execution, code-execution-sandbox (A); planner catalog (A), developer docs (Create Workflow, Manage Agent Triggers - dev preview schema, no stable public GraphQL, B), support article "HTTP Request block in the AI workflow builder" 33515393103378 (B), owner Slack posts (B), field reports (D).

## Findings and corrections
| # | Claim | Grade | Source | vs uploaded draft |
|---|---|---|---|---|
| 1 | Webhook body flows into workflow as one JSON string; parse with Code | B | #ai-workflows-product-updates 6 Oct (Daniel Abergel); #partners-workflows-updates 15 Oct | Consistent; now announced |
| 2 | Code egress: monday API and monday MCP server only | B | #ask-ai-workflows 16 Sep (Daniel Abergel) | Draft said API only; add MCP |
| 3 | Cannot install libraries; isolated env | B | same thread | Draft listed allowed libs as C; keep C |
| 4 | Auth automatic, no key | B | 24 Sep post + gist | Confirms A |
| 5 | HTTP token via Credentials app, `{{token}}` header | B | support article 33515393103378 | CORRECTS draft ("no secrets vault") |
| 6 | HTTP methods GET/POST/PUT; public URLs only; 5xx retry; run history shows I/O | B | same | New |
| 7 | HTTP can call api.monday.com with `Authorization:{{token}}`, counts against API quota | B | same + API rate-limit article | New |
| 8 | ~4 KB output truncation incident 13-14 Oct, fixed 14 Oct | B | #ask-ai-workflows 14 Oct (Shiraz Behar) | New |
| 9 | Code output binding to Change column value saves null | D | #ask-ai-workflows 3 Sep, 28 Sep | Unresolved |
| 10 | Get all items filter fields save null | D | 28 Sep | Unresolved |
| 11 | Webhook trigger could not be reactivated / HTTP 200 without run | A | Sep 23 report; fix commit 24 Sep #1830 (webhooks-app); routing spec: 200 ack then silent drop | RESOLVED in code; 200-without-run is by design for inactive URLs |
| 12 | No Get webhook data block; no Set variable block | A | planner 23 Oct | Resolves naming conflict with 15 Oct announcement |
| 13 | JSON Parser (JSONata) block 20264061 exists | A | planner | New alternative to Code |
| 14 | Programmatic workflow builds: trigger must use Direct (not Routes) next-block config or UI add-action gives 409 | D | #ask-ai-workflows 30 Sep-1 Oct (internal) | Only for custom-object API builders |
| 15 | Create/Update Workflow via Platform MCP run on dev (preview) schema; drafts must be published | B | developer docs Create Workflow | Matches architect |
| 16 | Agent triggers: only triggers addable programmatically appear in agent_catalog; OAuth triggers need UI | B | Manage Agent Triggers doc | New |
| 18 | Code runtime: Python 3.11, pandas/numpy/matplotlib/pillow/requests/httpx/openpyxl; egress api.monday.com + mcp.monday.com/mcp only; 300 s; output 512 KB; code 1 MB; no retry; token narrowed to caller scopes, ~6 min | A | code-execution-sandbox README; code-execution invariants; run-code-block source | Upgrades B items; draft's "pandas, numpy, requests" confirmed |
| 19 | Code outputs may be string/number/boolean/array | A | run-code-block types | Answers list-output question for declaration; Loop binding untested |
| 20 | Webhook: public POST, no auth/HMAC/rate limit, 200 ack via queue, empty body "{}", pending URL TTL 12 h, no custom response | A | openspec spec + commits #1690, #1848, #1850 | New |
| 21 | Block kinds in source: HTTP block URL validation can exclude internal domains (Aug 13) | A | commit #1729 | Config on monday side |
| 17 | No public support article for Code block as of 23 Oct (knowledge search) | D | get_monday_knowledge | Docs: monday.monday doc 18429902902, release board cards 12464666328 (webhook, doc 18425024829), 12464744837 (code, doc 18425024842) not read |

## Open questions (owner queue)
1. Admin control to disable the Code block per user/group? (JP Morgan question, 2 Sep, unanswered) - Ziv Pitshon / Daniel Abergel.
2. Webhook reactivation: code fixed 24 Sep (#1830). Ask Idan Moral whether the Harmony.ai account confirmed in production.
3. Code output binding to Change column value: fix ETA? - automations-wfb.
4. Can Code call the MCP server, with which endpoint and auth? - Daniel Abergel.
5. Quota and metering for Code and HTTP blocks (actions, credits, concurrency).
6. Who can read the Credentials-app token inside a workflow, and is it masked in run history?
7. Does JSON Parser (JSONata) work on a webhook body string? Needs a test in a demo account (write action, requires approval).
8. Webhook payload size limit and auth/signature options.
9. Code array output -> Loop input binding (declaration supported, A; binding untested).
10. Which user are Code-block API writes and notifications attributed to (workflow creator vs triggering user)? Source passes accountId/userId from auth context; read getAuthContext in core-blocks.
11. Numeric rate limit for code execution (Ignite config `code-execution-rate-limits`, not readable).

## Not verified by me
No live workflow was created, run or published. Source was read through gh (read-only); no repo was cloned or changed. Docs behind the release-board cards and the Code block monday.monday doc were not read (read_docs ids argument broken on this MCP).
