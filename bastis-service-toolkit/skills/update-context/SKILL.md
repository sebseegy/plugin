---
name: update-context
description: "Incrementally refresh a client's context with anything new since the last sync. Pulls SUMMARIES for only new calls — monday Notetaker first, Gong only for gaps — into the client-level All Calls folder, refreshes account data, re-tags new calls (project/relevance/audience), and updates the call-inventory Sheet. Use when new calls have happened, or the user says 'update context', 'pull new calls', 'refresh the context'. Like setup-context, summaries only — full transcripts stay on-demand via pull-gong-transcripts."
---

# Update Client Context

Refresh an already-set-up client with what's new — no duplication. Summaries only;
deepening specific calls is the separate on-demand `pull-gong-transcripts`. Read
`PROJECT-STRUCTURE.md` for layout, meta shapes, and inventory columns. Operates at
the **client level**.

If the client `meta.json` or `All Calls/call-inventory` is missing, tell the user to
run `/project-setup` first (it sets up structure and pulls context) rather than doing a full initial pull here.

## Step 1 — read existing state
Read client `meta.json` (`client_name`, aliases, account id/domain,
`last_context_sync`, `call_sources` id lists) and the `call-inventory` Sheet. These
tell you what NOT to fetch again.

## Step 2 — new Notetaker calls FIRST (monday.monday connector)
Use the monday connector on the **monday.monday** account (check `get_user_context`
if several are loaded). For each domain in `email_domains`:
`get_meetings_content(search: "<domain>", access: ALL, include_summary: false)` —
metadata only, cheap. Add `explore_meetings(query: "<client name>", access: ALL,
start_time_from: <last_context_sync>)` for internal calls about the client. Keep ids
not already in `call_sources.notetaker_meeting_ids`, then fetch them ≤5 at a time
with `include_summary: true, include_action_items: true`. Write to `All Calls/`,
summary level, English. (Guide: "Call sources — Notetaker first" in
PROJECT-STRUCTURE.md.)

## Step 3 — Gong gap-fill + refreshed account data (Kremer)
List Gong calls dated after `last_context_sync` (force raw CONVERSATION_IDs); drop
ids already in `call_sources.gong_call_ids` **and any call matching a Notetaker
meeting (±30 min, overlapping participants)**. Pull summary fields ≤5 per batch
only for what's left; write to `All Calls/`. If Notetaker already covers every call
since the last sync, skip Gong. Optionally refresh `Client Context/account-overview.md`
if account facts likely changed (overwrite snapshot, update `fetched_at`). Never use
Zoom as a call source.

## Step 4 — tag new calls
Set `relevance`, `audience`, and `projects` on each new call (unsure relevance →
mixed; unsure audience → internal-only; for `projects`, tag the project(s) it serves
or `general` if it serves none/the relationship broadly — never leave blank).

## Step 5 — update inventory + meta.json
Add new rows to `call-inventory` (newest first), refresh the "Not captured this run"
range, set `last_context_sync` = now, append new ids to `call_sources`.

## Output
Say what changed: new calls (count + titles, all summary-level), whether account
data refreshed, anything that failed. If nothing new, say so plainly.

## Defensive rules
Dedupe strictly against `call_sources`. If a source is unavailable, record it and
continue. Never invent content.
