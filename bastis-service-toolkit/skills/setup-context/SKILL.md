---
name: setup-context
description: "Internal context-fetch engine, normally run BY project-setup — not a direct entry point. Pulls call SUMMARIES for every client call — monday Notetaker first, Gong only for gaps — plus account data from Kremer, into the client-level Client Context and All Calls folders, and builds the call-inventory Google Sheet. If a user invokes this directly, redirect them to project-setup (the entry point) unless they explicitly want to re-pull context for an already-set-up client. Does NOT create folder structure and does NOT pull verbatim transcripts (that is pull-gong-transcripts)."
---

# Set Up Client Context (internal engine)

This is the **context-fetch engine**: it pulls account data + all call summaries and
builds the call-inventory. It is **not the entry point** — `project-setup` is. For a
brand-new client, `project-setup` creates the folder structure and then runs THIS
skill to populate context. Keeping the fetch here (rather than inside project-setup)
means `update-context` and `refresh-check` have one canonical fetch to mirror.

## Entry guard — redirect direct invocation

If you're invoked **directly** by a user (not called by `project-setup`):

- **If the client structure doesn't exist yet** (no client `meta.json` / folders) →
  do NOT run. Tell the user the entry point is **`project-setup`**, which scaffolds
  the folders (and runs this automatically for a new client), and stop. Running this
  alone would dump calls into a structure that isn't there.
- **If the client IS already set up** and they clearly want a **deliberate re-pull**
  of context (e.g. "re-fetch all calls", context got corrupted) → that's the one
  valid direct use; proceed, but note `update-context` is the lighter option for
  just catching new calls.
- **If it's ambiguous** → ask which they mean rather than assuming; default to
  pointing at `project-setup`.

When called by `project-setup`, skip the guard and just run.

Populate a client's shared-drive context fast and completely: account data in
`Client Context/`, and a **summary of every call** in `All Calls/`, fully indexed
in the `call-inventory` Sheet. Verbatim transcripts are expensive and unreliable in
bulk, so they're on-demand later (`pull-gong-transcripts`, which also handles Notetaker transcripts). Calls are stored ONCE at
client level and tagged by project — never copied into project folders.

**Capture ALL calls as summaries — never ask how many.** Summaries are cheap, so
the default is always the complete set, however large (100+ is normal and fine).
Do NOT pause to ask the consultant whether to capture all calls, or to pick a date
range or subset — just capture them all. The only time you scope down is if the
consultant *proactively* tells you to; otherwise, all calls, no question.

Read `PROJECT-STRUCTURE.md` (in this plugin) for the full drive layout, meta.json
shapes, and the inventory column list. This skill operates at the **client level**
and owns the **context** (calls + account data). It assumes the client folder
structure already exists — **`project-setup` creates the folders/meta.json** (and
auto-runs this skill for a brand-new client). If the client folders aren't there
yet, suggest running `project-setup` first.

## Step 1 — client identity

1. Read the client `meta.json` at the shared-drive root. If missing, create it
   (`level: client`, the client name — ask if not obvious, empty `skus`, etc.).
2. Note `client_name`, `aliases`, and `monday_account_id`/`account_domain` if known.

## Step 2 — Notetaker calls FIRST (monday MCP, monday.monday account)

Notetaker is the system of record for Basti's calls — capture from it before
touching Gong. Full tool guide: "Call sources — Notetaker first" in
PROJECT-STRUCTURE.md. In short:

1. **Confirm the connector.** If more than one monday connector is loaded, call
   `get_user_context` and use the one on the **monday.monday** account (Enterprise,
   ~3k members) — not the Spaces/demo or client account.
2. **Get the client's email domain(s)** from `meta.json` `email_domains`; if empty,
   infer from known contacts/calls or ask once, and save it.
3. **List every call, metadata only:** `get_meetings_content(search: "<domain>",
   access: ALL, include_summary: false)` per domain (~100 tokens/meeting). Add
   `explore_meetings(query: "<client name>", access: ALL, limit: 20)` for internal
   calls about the client with no client attendees. Merge and dedupe by id.
4. **Capture content in batches of ≤5 ids:** `get_meetings_content(ids: [...],
   include_summary: true, include_action_items: true)`. Add `include_topics: true`
   only for discovery/scoping calls where detail matters. Never pull transcripts here.
5. Write each to `All Calls/notetaker-<date>-<id>.md`, `content_level: summary`,
   English, with the meeting link in the header.

## Step 3 — account data + Gong ONLY for gaps (Kremer / Snowflake)

See "Tool quirks" in PROJECT-STRUCTURE.md before querying (batching/session rules
matter).

**Account overview:** ask Kremer for account id, domain, plan, seats, ARR,
adoption, active users, usage trends for the client (with aliases). Poll
`Kremer:check-query-status`. Capture any account id/domain for meta. Write
`Client Context/account-overview.md`.

**Gong gap-fill:** list Gong calls from
`bigbrain.l2.gong_conversations_w_transcript_and_opportunities`
(account link `JOINT_PULSE_ACCOUNT_ID`) as `CONVERSATION_ID|EFFECTIVE_START_DATETIME|TITLE`,
demanding the full raw id. **Drop every call that matches a Notetaker meeting**
(start within ±30 min, overlapping participants) — those are already captured. For
the rest (typically pre-sales/AE calls before Basti joined), pull
`CALL_SPOTLIGHT_BRIEF/_KEY_POINTS/_NEXT_STEPS` + title/date/participants, ≤5 per
query, into `All Calls/gong-<date>-<id>.md`, `content_level: summary`. If the
account's calls sit under several account IDs, capture all of them.

Never use Zoom (MCP or plugin) as a call source.

## Step 4 — tag every call (relevance, audience, project)

For each call, set in the file header and the inventory row:
- **relevance** — project / commercial / internal / mixed / unrelated (unsure → mixed)
- **audience** — client-safe / internal-only (unsure → internal-only)
- **projects** — which project(s) the call serves; or `general` for client-level
  (relationship/commercial/cross-project) calls. Never leave it blank. If projects
  already exist when this runs, tag the obvious ones (a call may map to several). If
  no projects exist yet (first setup before `project-setup` created them), tag every
  call `general` for now — `project-setup` does the real call→project mapping when it
  creates the projects. Never silently drop a call.

## Step 5 — build the call-inventory Sheet + update meta.json

Create/update `All Calls/call-inventory` as a **Google Sheet** (via the Drive
connector) with the columns in PROJECT-STRUCTURE.md (including `projects`,
`relevance`, `audience`, `content_level`), newest first, plus a "Not captured this
run" range. Update client `meta.json`: `last_context_sync`, discovered
`monday_account_id`/`account_domain`, and `call_sources` id lists.

## Output

Brief chat summary: how many calls captured (all summary-level), headline account
facts, anything not captured. Mention any call can be deepened on demand with
`pull-gong-transcripts`. Don't paste context back — it's in the drive, synced for
the team.

## Defensive rules

- If a source is unavailable, record under "Not captured this run" and continue —
  never abort the whole run.
- Never invent calls, dates, account numbers, or content. Missing is missing.
