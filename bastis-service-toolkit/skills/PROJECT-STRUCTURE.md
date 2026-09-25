# Drive structure & path contract (reference)

The single source of truth for WHERE everything lives in the client shared drive.
Every skill files its inputs and outputs according to this. Skills inline what they
need, so they don't depend on this file at runtime — it's the maintainer reference.
Naming is plain and human (no phase numbers). Filesystem is case-insensitive.

## The hierarchy: Client → SKU/Contract → Project

```
<Client> shared drive/
├─ meta.json                     CLIENT identity (see below)
├─ Client Context/               client-wide context: org info, stakeholders, account overview
│   └─ account-overview.md       account facts from Kremer (Snowflake)
├─ All Calls/                    EVERY call for the client, in one place
│   ├─ call-inventory            a GOOGLE SHEET — one row per call, tagged by project + relevance + audience
│   ├─ gong-<YYYY-MM-DD>-<id>.md
│   └─ notetaker-<YYYY-MM-DD>-<id>.md
└─ SKU level/
    └─ <SKU or Contract name>/
        ├─ meta.json             SKU identity incl. engagement_type
        ├─ SKU Context/          contract scope, terms, SKU-wide docs
        └─ Projects/
            └─ <Project name>/
                ├─ meta.json      PROJECT identity (links up to SKU + client)
                ├─ inputs/        consultant-uploaded source material (read-only inputs)
                ├─ deliverables/  task outputs: handover brief, scope, solution design, go/no-go, etc.
                └─ docs/          build documentation, diagrams, reference docs
```

Why this shape: calls and account data are client-wide (one client may have several
SKUs/contracts and several projects; a single call often serves more than one). SKUs
carry the contract/engagement type. Projects hold the actual working files. This
supports professional services, managed services, and multiple projects per client
without forcing a linear "phase" lifecycle on anyone.

## Calls live once, tagged by project

Calls are NEVER copied into project folders. They live in `All Calls/`, and the
`call-inventory` Sheet maps each call to the project(s) it serves. A task working on
a project reads `All Calls/`, filters by the `projects` tag, and respects
`relevance`/`audience` tags.

**Every call carries a `projects` tag — this is what makes per-project context fast.**
The value is one or more project names, or `general` (client-level: relationship/
commercial/cross-project calls that serve no single project). It is never left blank.
A call can legitimately map to **multiple** projects. The tagging is done by
`project-setup` when projects are created (it infers from call content, participants,
and dates vs each contract's window) and by `refresh-check`/`update-context` for new
calls. If a project task ever finds the project has no tagged calls (tagging never
ran), it should run that mapping before relying on the filter.

`call-inventory` columns (one row per call, newest first):
`date | source (gong/notetaker) | id | title | participants | projects (comma-sep project names or 'general') | themes/tags | relevance (project/commercial/internal/mixed/unrelated) | audience (client-safe/internal-only) | content_level (summary/full) | file_path | key_next_steps`
Plus a "Not captured this run" range with reasons.

## meta.json at each level

**Client** `<Client>/meta.json`:
```json
{
  "level": "client",
  "client_name": "Acme Corp",
  "monday_account_id": null,
  "account_domain": null,
  "aliases": [],
  "skus": [],
  "email_domains": [],
  "last_context_sync": null,
  "call_sources": { "notetaker_meeting_ids": [], "gong_call_ids": [] },
  "monday_environments": {
    "client_account": { "name": null, "slug": null, "mcp_access": false },
    "build_accounts": [
      { "label": "Spaces / demo", "slug": null, "purpose": "demo + pre-transfer build", "mcp_access": true }
    ]
  }
}
```
`email_domains` (e.g. `["whsmith.co.uk"]`) is how Notetaker finds every client
call, including ones titled "Emily Hall and Sebastian Seegy". `monday_environments`
records which monday accounts exist for this client and whether Claude can see
them — see "monday environments" below.

**SKU/Contract** `SKU level/<SKU>/meta.json`:
```json
{
  "level": "sku",
  "client_name": "Acme Corp",
  "sku_name": "Q3 Professional Services",
  "engagement_type": "professional_services",
  "projects": []
}
```
`engagement_type` is one of: `professional_services`, `managed_services`,
`aitp` (AI Transformation Package), `other`. Skills adapt to it — e.g. managed
services has no launch/closure arc; professional services does.

**Project** `SKU level/<SKU>/Projects/<Project>/meta.json`:
```json
{
  "level": "project",
  "client_name": "Acme Corp",
  "sku_name": "Q3 Professional Services",
  "project_name": "CRM rollout",
  "build": {
    "stage": "demo_build",
    "build_account": "Spaces / demo",
    "build_workspace_ids": [],
    "client_workspace": null,
    "transferred_at": null,
    "source_of_truth": "build_account"
  }
}
```
`build.stage` is one of `not_started` · `demo_build` (building in Spaces/demo) ·
`transferred` (moved to the client's account) · `client_build` (built directly in
the client account) · `live`. `source_of_truth` is `build_account` until transfer,
then `client_account`.

## Source / deliverable file headers

Call files (in `All Calls/`):
```markdown
---
source: notetaker       # notetaker (primary) | gong (fallback)
id: 12345
date: 2026-05-20
title: Discovery call
participants: [...]
projects: [CRM rollout]  # which project(s) this call serves; [] if general/client-level
relevance: project       # project | commercial | internal | mixed | unrelated
audience: client-safe    # client-safe | internal-only
content_level: summary   # summary | full
language: en             # normalize content to English
fetched_at: <ISO timestamp>
---
```

Deliverables (in a project's `deliverables/`): start with a short header noting the
client, SKU, project, the task that produced it, and date; then the content.

## Resolving "which project am I working on" (every skill follows this)

**The Cowork project points at the high-level client folder.** That client folder is
the top — never look above it. The whole client folder is synced **locally**, so:

- **Read local synced files first.** The client folder and everything under it is on
  disk — read it directly. Use the **Google Drive connector only as a fallback** when
  a file genuinely isn't on disk (e.g. a sync hiccup). Do NOT reach for the connector
  to inventory the client or "discover" structure that's already local.

- **Establish the project once per chat, then remember it.** Which engagement project
  a chat is about is chosen per-chat. On the first skill invocation that needs a
  project: if the working location or the user's words make it unambiguous (e.g. a
  project folder name like "UKTV", or they said the project), use that. **If it's not
  clear, ASK the user which project they're working on** — don't guess, and don't go
  spelunking through the client folder to infer it. Once established, every later
  skill in the same chat reuses that project without re-asking. (Different chats on
  the same client can each hold a different project.)

- **Stay in scope — never climb sideways.** Once the project is known, read only:
  that project's folder (`inputs/`, `deliverables/`, `docs/`), the client-level
  shared context it needs (calls in `All Calls/` tagged for this project, plus
  `general`; `Client Context/account-overview.md`), and the client/SKU `meta.json`
  for identity. Do **NOT** read, inventory, or wander into *other* projects' folders
  or other SKUs. The screenshot anti-pattern — surveying every SKU and other projects
  — is exactly what to avoid.

- Write outputs to the project's `deliverables/` (or `docs/` for documentation).

If no project context exists at all (the client folder is empty/new), that's when
`project-setup` scaffolds — see that skill.

## Relevance & audience filtering (applies everywhere)

- Project work: use `project`/`mixed` calls tagged for this project; treat
  `commercial`/`internal` as background, not requirements; skip `unrelated`.
- **Client-facing outputs HARD RULE:** include ONLY `client-safe`, project-relevant
  content. Never surface `internal-only`/`commercial`/`internal` material (pricing,
  renewal, internal politics, candid risk language). If excluding leaves a gap, note
  it internally rather than filling from internal-only sources.
- When relevance/project mapping is genuinely ambiguous, flag to the consultant
  rather than guessing.

## Tool quirks (apply when a skill touches these)

Kremer: sessions serialize and can cache (omit sessionId for fresh/parallel);
summary batches ≤5 calls; force raw CONVERSATION_IDs; verify transcript completeness
(don't trust "complete" claims). Notetaker: set include_* flags explicitly — with
all flags false `get_meetings_content` returns metadata only, which earlier runs
mistook for "the API has no content"; `include_action_items: true` works again
(re-tested 2026-09-25); transcripts are large/mixed-language (don't inline,
normalize to English). Drive: shell mount unreliable mid-session — read
binaries via the connector, write via file tools; filesystem case-insensitive.

## Call sources — Notetaker first (applies to every skill that recalls calls)

Basti records every client call with the **monday AI Notetaker** in the
**monday.monday** account. That is the system of record for calls. Gong only covers
calls an AE recorded (mostly pre-sales), and Zoom is never a call source.

**Order — stop at the first source that answers the question:**
1. **Notetaker** (monday MCP connector on the monday.monday account — confirm with
   `get_user_context` if several monday connectors are loaded; it's the Enterprise
   account with ~3k members, not the Spaces/demo or client account).
2. **Gong via Kremer** — only for gaps: calls before Basti joined (sales handover),
   or a date where Notetaker has no recording. Before pulling a Gong call, drop it
   if a Notetaker meeting exists within ±30 min with overlapping participants.
3. **Never** Zoom MCP / Zoom plugin, Gmail Gong digests, or calendar for call
   *content*. Calendar is fine for attendee lists (meeting-followup).

**Cheapest correct Notetaker calls (measured 2026-09-25):**

| Need | Call | Cost (approx.) |
|---|---|---|
| List/ID-check every client call | `get_meetings_content(search: "<client email domain>", access: ALL, include_summary: false)` | ~100 tokens/meeting — metadata only (id, title, time, participants) |
| Find calls by topic/person | `explore_meetings(query: "<1–4 words>", access: ALL, start_time_from, limit ≤10)` | ~130 tokens/meeting (id + one-paragraph gist) |
| Find where something was said/decided | `search_meetings_content(query, search_in: [SUMMARY, ACTION_ITEM, TOPIC], access: ALL, limit ≤5)` | passages only, ~1–2k total |
| Capture a call | `get_meetings_content(ids: [≤5], include_summary: true, include_action_items: true)` | ~1.5–2k tokens per 30–60 min call |
| Deeper context | add `include_topics: true` | roughly doubles it (~4k for a 1 h call) |
| Verbatim | `include_transcript: true` for ONE call, on demand only | very large — never in bulk |

Rules that make this work:
- Always pass `access: ALL` (default `OWN` misses calls shared by colleagues).
- The domain search catches calls whose titles don't name the client. Search every
  domain in `email_domains`; add `explore_meetings` with the client name/aliases to
  catch internal prep calls without client attendees.
- A Notetaker meeting URL
  (`…/notetaker/meetings-page-product-view/summaries/<uuid>`) → the uuid is the id;
  pass it straight to `get_meetings_content(ids: [uuid], include_summary: true, …)`.
- Why this beats Gong on tokens: Gong pulls go through the async Kremer agent
  (submit → poll → SQL narrative, ≤5 calls per batch), so every batch costs several
  round trips before any content arrives; Notetaker returns structured summaries and
  action items synchronously in one call.

## monday environments — which account is the truth (applies to every skill that reads boards)

Typical lifecycle: Basti builds a **demo in the monday Spaces / demo account** via
MCP (Claude or Cursor), then **transfers it to the client's own account**. After the
transfer the client account is the only truth — and Claude usually has **no MCP
access** to it. The demo workspace becomes a stale snapshot.

Rules:
1. Before reading any board to judge progress, read `build.stage` in the project
   `meta.json` and `monday_environments` in the client `meta.json`. If they're
   missing, ask once: "Is this project still in the Spaces/demo account, or has it
   moved to <client>'s account?" — and write the answer back.
2. `stage = transferred | client_build | live` and `client_account.mcp_access =
   false` → **do not report anything as "not done" or "missing" based on the
   demo/Spaces account.** Judge progress from Notetaker calls, deliverables, and what
   Basti tells you. Mark board-level facts "unverified — lives in <client> account
   (no MCP access)" and ask Basti to confirm or paste a screenshot/export.
3. `stage = demo_build` → the build account is the truth; read it normally.
4. Before any monday MCP call, confirm which account the connector is on
   (`get_user_context`) and name it in the output. Never write to monday.monday
   (internal, Notetaker only) or to a client account without explicit approval.

## Useful warehouse tables (via Kremer)

- **Gong calls + transcripts:** `bigbrain.l2.gong_conversations_w_transcript_and_opportunities`
  (account link `JOINT_PULSE_ACCOUNT_ID`; `TRANSCRIPT` VARIANT for verbatim).
- **Contracts / SKUs / engagement type:** `cco.l3.dim_delivery_solutions` — PS /
  Managed Services / AITP service lines per account (link `pulse_account_id`). Key
  columns: `product_name`, `product_identifier_sku`, `product_group`, `is_recurring`
  (recurring ≈ managed services), `service_start_date`, `service_end_date`,
  `plan_tier`, `platform_type`, and project-delivery fields (`project_id`,
  `project_status`, `project_kickoff_date`, `project_total_hours`). This is the
  source for SKU names and engagement type — `project-setup` and `monday-scoping`
  can read it instead of asking.
- **Subscription / ARR:** `billing.l3.dim_bs_subscriptions` (link `pulse_account_id`)
  — plan tier, term dates, ARR, renewal.
