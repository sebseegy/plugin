---
name: local-setup-context
description: Local counterpart to bastis-service-toolkit:setup-context (v2). For a new or existing client folder under Work/Clients/, gathers everything that already exists (files already on disk, monday Notetaker calls, Gong gap-fill, Kremer account + contract data) and files it into the canonical client structure from Clients/CLAUDE.md, then updates CLAUDE.md, meta.json, SKU meta, account-overview.md, call-inventory.md and decisions-log.md. Use when Basti says "set up this client locally", "new client folder", "local setup-context", "pull everything for [client]", "reconcile/clean up the [client] folder", "refresh the client context", or points at a client folder that is empty, messy, or missing meta.json / Client Context / All Calls. Reach for it whenever a client folder's context or organization is the thing being worked on, even if the skill isn't named.
---

# local-setup-context (v2)

One pass that does what `project-setup` + `setup-context` do on the shared drive, but on the local disk:

```
/Users/sebastianse/Desktop/Sebastian Seegy /Work/Clients/<Client>/
```

**Start of every run:** re-read `Clients/CLAUDE.md` (live rules) and use this skill's `templates/CLIENT-CLAUDE.md` (same file as `Clients/_templates/CLIENT-CLAUDE.md`; if the two differ, the one in `Clients/_templates/` wins). If they disagree with this file, they win; fix this file afterwards.

Canonical shape:

```
<Client>/
  CLAUDE.md          built from templates/CLIENT-CLAUDE.md
  meta.json          client record
  Client Context/    account-overview.md, people, decisions-log.md
  All Calls/         call-inventory.md + call summaries (transcripts only on demand)
  SKU level/<SKU>/   meta.json, SKU Context/, Projects/<project>/{meta.json,inputs,docs,deliverables}
```

## Rules that apply to every phase

- **Idempotent and additive.** Create only what is missing; never overwrite. Merge into existing `meta.json`, adding only missing fields. Case-insensitive filesystem: no case-variant duplicates.
- **Moves only, never deletes.** Superseded files go to `_archive/<YYYY-MM-DD>/` with a one-line reason. No file is moved before Basti approves the plan (Phase 3).
- **No nested client-named folder** (the forbidden pattern in `Clients/CLAUDE.md`).
- **Do not ask** whether the account is Enterprise (it is the default), how many calls to capture (all, summaries only), or for facts a tool can supply. Ask only for what cannot be inferred: client name if unclear, project names, ambiguous placement.
- **Missing is missing.** Never invent calls, dates, ids, contacts or status. Unconfirmed items are labelled `unconfirmed`.
- **Never send or finalize client communication.** Drafts only.
- If a source fails, log it under "Not captured this run" in `call-inventory.md` and continue.

## Phase 0: orient (read-only)

1. Locate `Clients/<Client>/`. Empty or missing = new client. Otherwise existing.
2. Read `meta.json`, `CLAUDE.md`, `Client Context/*`, `All Calls/call-inventory*.md`, each `SKU level/*/meta.json`. Note what is already present so nothing is re-pulled.
3. List client-wide loose material: root files, ad-hoc subfolders (2 to 3 levels), transcripts (`.txt/.docx/.vtt`), decks, PDFs, `.md` docs.

## Phase 1: scaffold what is missing

Create the missing parts of the canonical tree. A new client gets: `meta.json` (`level: client`, `client_name`, `aliases`, `skus: []`, `email_domains`, `call_sources`, null sync fields), `Client Context/{account-overview.md,decisions-log.md}`, `All Calls/call-inventory.md`, and `CLAUDE.md` from `templates/CLIENT-CLAUDE.md`. SKU folders are created only for real contracts (Phase 2c). Do not invent projects.

## Phase 2: gather everything that already exists

### 2a. Local material
Index what is already on disk (name, type, size, modified). Convert call-like files at the root (transcripts, notes) into entries for `All Calls/` (`source: local-file`, `content_level: summary`) rather than leaving them loose. Keep the original in place until Phase 3 approval.

### 2b. Notetaker first (monday MCP, **monday.monday** account)
1. If several monday connectors are loaded, call `get_user_context` on each and use the monday.monday one (not Spaces/demo/client).
2. Domains: `meta.json` `email_domains`; if empty, infer from local files/contacts, and save.
3. List metadata only: `get_meetings_content(search: "<domain>", access: ALL, include_summary: false)` per domain, plus `explore_meetings(query: "<client name>", access: ALL, limit: 20)` for internal calls. Dedupe by id; skip ids already in `call_sources.notetaker_meeting_ids`.
4. Capture in batches of at most 5: `get_meetings_content(ids, include_summary: true, include_action_items: true)`. Add `include_topics` only for discovery/scoping calls. No transcripts.
5. Write `All Calls/notetaker-<YYYY-MM-DD>-<id>.md` with the real meeting id (never `TBC`; if an id is unavailable, record it under "Not captured").

### 2c. Kremer: account + contracts (data-expert-agent MCP)
Resolve the account (aliases), poll `check-query-status`, and capture: `pulse_account_id`, domain, seats, plan, ARR bands, adoption and usage trends, then contracts from `cco.l3.dim_delivery_solutions` (product name, SKU code, group, recurring, start/end, stage, project status/kickoff). Write `Client Context/account-overview.md` with `source: kremer` and `fetched_at`. Create one SKU folder per won or active contract with a lean `meta.json` (no volatile figures like hours remaining or ARR).

### 2d. Gong, gaps only
List Gong calls for the account(s) from `bigbrain.l2.gong_conversations_w_transcript_and_opportunities` (full raw conversation ids). Drop any call matching a Notetaker meeting (start within 30 minutes and overlapping participants) or an id already in `call_sources.gong_call_ids`. For the rest, pull spotlight brief, key points, next steps (at most 5 per query) into `All Calls/gong-<date>-<id>.md`.

Never use Zoom as a call source.

### 2e. Tag every call
Header fields: `source, id, date, title, participants, projects, relevance (project|commercial|internal|mixed|unrelated), audience (client-safe|internal-only), content_level, fetched_at`. Unsure relevance = `mixed`; unsure audience = `internal-only`. `projects` is a project name (a call may map to several) or `general`; never blank.

## Phase 3: classify, plan, approve, move

1. **Flag, don't guess** (needs Basti's decision):
   - Competing master-context documents (`CONTEXT.md`, `MEMORY.md`, `*Master_Context*`, or status/decision logs). List with modified dates; ask which is live.
   - A folder named after the client nested inside the client folder. Check whether it holds a half-migrated structure before proposing anything.
2. **Bucket the rest** (group by pattern, not file by file):
   - call transcripts and notes go to `All Calls/`
   - account, stakeholder and standing decisions go to `Client Context/`
   - SOWs, contracts and scope go to `SKU level/<SKU>/SKU Context/`
   - client-supplied files go to the project's `inputs/`
   - working files go to `docs/`
   - anything sent to the client goes to `deliverables/`
   - superseded master docs go to `_archive/`
   Where a project boundary is unclear, ask; do not invent project names.
3. Write the plan as a table (from, to, rule, count) and stop for approval.
4. After approval, generate one script, show it, run it, and verify the moved count equals the plan. No overwrites: on a name collision, suffix with the date.

## Phase 4: update the records

1. **`meta.json` (client):** merge `client_name, aliases, monday_account_id/pulse_account_id, account_domain, email_domains, skus, last_context_sync (ISO now), call_sources` (id lists extended, not replaced). Add `monday_environments` only with confirmed values.
2. **SKU and project `meta.json`:** lean shape from `project-setup`; add project names to the SKU `projects` list.
3. **`All Calls/call-inventory.md`:** local markdown table, newest first, columns `date | source | id | title | participants | projects | themes/tags | relevance | audience | content_level | file_path | key_next_steps`, plus a "Not captured this run" section.
4. **`Client Context/account-overview.md`:** identifiers, contracts, key contacts (from calls and Kremer), with a source and date on every block.
5. **`CLAUDE.md`:** rebuild from `templates/CLIENT-CLAUDE.md` with real values: aliases, account id, SKUs as `Name (SKU level/Name/)`, `Read first` imports (`@Client\ Context/account-overview.md`), a Current status filled only from what calls and docs confirm (otherwise `TODO`), and client-specific rules only if already stated somewhere. Keep under 200 lines.
6. **`Client Context/decisions-log.md`:** append a dated entry: what was gathered, what was archived and why, which master doc won, what was not captured.

## Verify before finishing

- Count calls in `All Calls/` equals rows in `call-inventory.md` (excluding the inventories themselves).
- Every id in `call_sources` has a file; every file's id is in `call_sources`.
- No `TBC` ids; no empty `projects` fields; `meta.json` parses as JSON.
- `CLAUDE.md` under 200 lines and its imports resolve.

## Output

One short chat summary: calls captured per source, contracts found, files moved/archived, items needing a decision, sources that failed. Mention `pull-gong-transcripts` for deepening any call on demand.
