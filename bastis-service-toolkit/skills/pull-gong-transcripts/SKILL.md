---
name: pull-gong-transcripts
description: On-demand, targeted retrieval of FULL verbatim Gong transcripts for specific calls. Use when a consultant or another skill needs the complete transcript text of one or more specific Gong calls (by conversation id) — not summaries, and not the whole account. Triggers include "pull the full transcript for that call", "get verbatim for that conversation", or invocation as /pull-gong-transcripts. setup-context captures summaries for all calls; this skill deepens specific ones to full transcripts.
---

# Pull Gong Transcripts (targeted, on-demand)

> **Notetaker calls don't come through here.** If the call is a Notetaker meeting
> (`source: notetaker`, uuid id), fetch verbatim directly with
> `get_meetings_content(ids: [uuid], include_transcript: true)` on the monday.monday
> connector — one call at a time, then save it as `content_level: full`. This skill
> is only for Gong calls (mostly pre-sales/AE calls Notetaker didn't record).

Retrieve the FULL verbatim transcript for one or more **specific** Gong calls and
upgrade their context files from summary to full. This is a surgical deepening
step, not a bulk operation — `setup-context` already captured summaries for every
call; run this only for the calls that actually need verbatim depth (e.g.
`design-solution` needs exact requirements from a scoping call).

## Input

One or more `CONVERSATION_ID`s. If the consultant didn't give ids, help them pick:
read the All Calls/call-inventory Sheet (filter to `content_level = summary`), show candidate
calls by date/title, and confirm which to deepen. Never pull the whole account
here — that's the slow, unreliable path setup-context deliberately avoids.

## Data location

- Table: `bigbrain.l2.gong_conversations_w_transcript_and_opportunities`
- `CONVERSATION_ID` — the call id (also the dedupe key and filename component)
- `TRANSCRIPT` — VARIANT, a JSON array of segments (speaker + text). Flatten to
  `Speaker: text` lines, in order.
- `TITLE`, `EFFECTIVE_START_DATETIME`, `PARTICIPANTS_INFO` — metadata
- `CALL_SPOTLIGHT_BRIEF` / `_KEY_POINTS` / `_NEXT_STEPS` — summary fallback

Kremer is async: submit with `Kremer:data-expert-agent`, poll
`Kremer:check-query-status` (≥5s between polls).

## Step 1 — get the expected segment count first

Before pulling text, ask for the segment count so you can verify completeness
afterwards (Kremer falsely claims "complete" — see quirks):
> "For CONVERSATION_ID = '<id>' in
> `bigbrain.l2.gong_conversations_w_transcript_and_opportunities`, how many
> segments/elements are in the TRANSCRIPT array? Return only the number."

## Step 2 — pull the transcript, verify, chunk if needed

For each id, one call at a time (never batch transcript bodies):
1. Ask Kremer to flatten and return the full verbatim transcript:
   > "For CONVERSATION_ID = '<id>', flatten the TRANSCRIPT VARIANT array into plain
   > lines 'Speaker: text', one segment per line, in order. Return ALL <N> segments
   > verbatim — do not summarize, paraphrase, shorten, or omit any. Also return
   > TITLE, EFFECTIVE_START_DATETIME, PARTICIPANTS_INFO."
2. **Verify against the expected count from Step 1.** Do not trust any "complete"
   claim — count the returned lines. A known failure mode: a 5+ minute pull
   returning only the last ~60 of 1,061 segments while claiming completeness.
3. If short, pull in explicit ranges and concatenate:
   > "Return segments 1–300 of the TRANSCRIPT for CONVERSATION_ID '<id>' as
   > 'Speaker: text' lines, verbatim." …then 301–600, etc., until the count matches.
   Run range-pulls in separate sessions (omit sessionId) to avoid serialization.
4. When the flattened line count matches (or is within a small tolerance), write
   `All Calls/gong-<date>-<conversationId>.md` with `content_level: full`,
   transcript under `## Transcript`. Overwrite the prior summary-level file for that
   id (keep the summary fields in the header/Summary section).
5. If after careful range-chunking the verbatim text still can't be assembled,
   leave the file at `content_level: summary`, add a note "full transcript not
   retrievable on <date> (returned <x>/<N> segments)", and move on. Never fabricate
   or "reconstruct" transcript text.

## Step 3 — update inventory + meta.json

For each deepened call, set its inventory row `content_level` to `full`. Ensure the
`CONVERSATION_ID` is in `the client meta.json call_sources.gong_call_ids` (it should already be from
setup-context). Update the All Calls/call-inventory Sheet via the Drive connector.

## Output

Per call: full / partial (x of N segments) / summary-only fallback, with the
title and date. Brief — content is in the files.

## Known tool quirks

**Don't trust completeness claims** — verify segment counts every time (this is the
single most important rule here).
**Sessions serialize / cache:** omit `sessionId` for concurrent or genuinely fresh
queries; reusing one can return a cached answer or drop an in-flight question.
**Force raw IDs** if you ever list calls here: demand plain `ID|datetime|title`,
full unabbreviated CONVERSATION_ID.
**Write via file tools; read existing binaries via the Drive connector** — the
shell mount is unreliable mid-session. Filesystem is case-insensitive.
