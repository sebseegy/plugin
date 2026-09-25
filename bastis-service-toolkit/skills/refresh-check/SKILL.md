---
name: refresh-check
description: "Lightweight context freshness check that delivery tasks run first, automatically. Does a cheap ID-only check for new calls and pulls summaries for ONLY genuinely new ones, then proceeds. Designed to be near-instant when nothing is new — no content fetches, no transcripts, bail fast. Invoked at the start of other tasks; the user does not call this directly and it stays silent unless it actually pulls new calls."
---

# Refresh Check (lightweight, auto-run)

A fast freshness check that runs at the **start of delivery tasks** so the consultant
never has to remember `/update-context`. The whole design goal is **speed when
nothing is new** — it must add negligible time in the common case. Do the cheap
check, and the moment it's clear there's nothing new, stop and let the calling task
proceed.

This runs **silently** unless it actually pulls new calls. Do not narrate the check,
do not print "context is current" — only speak up if you fetched something (one line)
or hit an error worth flagging.

## The check (keep it cheap — ID-only, no content)

1. **Resolve the client** and read the client `meta.json` (one small read). Note
   `call_sources.notetaker_meeting_ids` and `call_sources.gong_call_ids` — the IDs
   already captured. If there's no client `meta.json` / no context set up yet, do
   nothing and let the task proceed (don't try to set up context here — that's
   `setup-context`).

2. **Cheap ID-only lookups — never pull content here:**
   - **Notetaker first** (monday.monday connector): for each domain in
     `email_domains`, `get_meetings_content(search: "<domain>", access: ALL,
     include_summary: false)` — returns ids/titles/dates/participants only
     (~100 tokens per meeting). If `email_domains` is empty, use
     `explore_meetings(query: "<client name>", access: ALL, start_time_from:
     <last_context_sync>, limit: 10)` instead.
   - **Gong only as a gap check**: skip it when Notetaker shows calls on the dates in
     question. Run the single Kremer ids-only query (`CONVERSATION_ID`s after
     `last_context_sync`) only if `last_context_sync` is older than 7 days or the
     task is a sales handover. Never Zoom.

3. **Diff against `call_sources`.** Any ids returned that aren't already captured are
   "new". **If there are none → stop immediately and return control to the task.**
   This is the common path and must be fast. (Optionally stamp `last_context_sync`
   to now.)

## Only if there ARE new calls

Pull summaries for **just the new ids** (not everything) — same logic as
`update-context` Step 2/3, scoped to the new calls only: summary fields ≤5 per Kremer
batch, notetaker `include_summary: true, include_action_items: true` (≤5 ids per call), written to
`All Calls/` at `content_level: summary`, English, tagged (relevance / audience /
projects — unsure → mixed + internal-only; for `projects`, infer the project(s) the
new call serves and tag them, or `general` if it serves none/the relationship
broadly — never leave it blank). Add rows to the `call-inventory` Sheet, append the
new ids to `call_sources`, set `last_context_sync` = now.

Then say **one line** to the user, e.g. "Pulled 2 new calls into context before
continuing." and let the task proceed.

## Hard constraints (this is the point of the skill)

- **Never pull transcripts** here — verbatim is always on-demand via
  `pull-gong-transcripts`. This check is summaries-only, and only for new calls.
- **Never do a full re-sync** — only the diff. If a huge number of ids come back new
  (e.g. context was never really populated), don't churn: pull a reasonable recent
  batch, note that a full `/project-setup` (or `/update-context`) is recommended, and
  proceed.
- **Fail open, fast.** If a lookup errors or a tool isn't available, don't block the
  task — proceed silently with existing context (optionally note the check couldn't
  run). A task running on slightly stale context is far better than a task that
  won't run.
- **Stay silent on the no-op path.** No output when nothing's new.

## How tasks use this

Delivery tasks (`handover-brief`, `kickoff`, `discovery-synthesis`, `solution-build`,
`uat`, `go-no-go`, `hypercare-report`, `closure-package`, `solution-card`) and
`status` run this as their first step, before reading calls. `setup-context` and
`update-context` do NOT (they own context themselves). `services-help` does NOT auto-pull —
it only reads state — though it may *recommend* `update-context` when it notices
staleness.
