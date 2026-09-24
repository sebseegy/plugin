---
name: weekly-pulse
description: >-
  Basti's personal weekly digest of what's new on monday.com, pulled live from
  the ICs Product Updates board, Slack, and monday-all. Use when Basti asks
  "what's new this week", "run my pulse", "weekly digest", "what did I miss",
  "product update digest", or "catch me up on monday.com" — and automatically
  once a week via the scheduled task set up alongside this skill. Filters and
  ranks everything through his lens: Enterprise EMEA delivery + AITP/AI
  Champion work. Not for one-off "is X still true" checks on a specific
  limit or feature (use monday-scaling-watch / monday-ai-advisor for that) —
  this is the broad, recurring sweep.
---

# Weekly pulse

Basti's own freshness engine. The stock `services-toolkit` skills (`monday-scaling-watch`,
`monday-ai-suggester`) check Slack and a couple of AI-only boards on demand. This skill is
broader and recurring: every run (manual or scheduled) it sweeps three sources, filters for
what actually matters to an Enterprise EMEA Implementation Consultant who is also the
Delivery org's AI Champion, and produces one short digest.

## Sources — pull all three every run

### 1. ICs Product Updates board (primary — structured, already IC-curated)

This is a monday.com board maintained by the ICs Product Updates team (workspace
**15557960**, board **18411697232**, name "Product Updates") that logs every product
release relevant to Implementation Consultants, tagged and ready to filter. There is also
a Vibe app view of the same board (object id `18413653333`, app-feature id `21100584`,
reachable at `https://monday.monday.com/misc/vibe/full-page-app/object?object-id=18413653333&app-feature-id=21100584`)
— same data, nicer to browse, no need to hit it separately for this skill.

Pull with `get_board_items_page` on board `18411697232`:
- Filter `date_mm32grnh` (Date) to the window since the last run (default: last 7 days;
  widen to 14 if it's the first run or the last run failed).
- Include columns: `color_mm32e1eb` (Status), `color_mm32a8vv` (IC Relevance),
  `long_text_mm32vqr` (Use Cases), `color_mm32td82` (Source Type), `link_mm329g2s`
  (Source Link), `long_text_mm32d2hf` (Summary), `dropdown_mm32s9p3` (Platform Area),
  `color_mm32rdj5` (Product), `dropdown_mm32k9yh` (AI Type), `dropdown_mm327517`
  (Release Status).
- If unfamiliar with the board, run `get_board_info` first — the label sets above can
  shift.

### 2. Slack — catches anything not yet logged on the board

Reuse the channel logic from `monday-ai-suggester`/`monday-scaling-watch`: search
`slack_search_public_and_private` scoped to the same date window, across
`#ask-vibe-ai`, `#ask-ai-agents`, `#ai-agents-product-updates`, `#ai-workflow-group`,
`#monday-platform-notifications`, `#cco-enablement-updates`. Run queries in parallel.
Treat this as a supplement — skip anything that's clearly already captured on the board
(same release, same week) to avoid duplicate items in the digest.

### 3. monday-all — company-wide announcements

Call `news_list_articles` for anything published in the window, and `knowledge_search`
for AITP / AI Transformation Package / Enterprise-EMEA-relevant terms if News is thin.
This catches org-wide comms (pricing changes, packaging, enablement) that wouldn't show
up on a product-tracking board.

If any source errors or comes back empty, say so in one line under "Sources pulled" and
proceed with the rest — never block the digest on one bad source.

## Filtering — Basti's lens, not a generic feed

Rank, don't just list:

1. **AITP / AI relevant** (`AI Type` set, or `dropdown_mm32s9p3` = AI, or Slack/News
   about Agents, Sidekick, Vibe, AI Workflows) — surface first, he's the Delivery org's
   AI Champion.
2. **Enterprise-relevant** (`Product` = All/WM/CRM at Enterprise tier, scaling/governance
   items, permissions/admin) — surface second.
3. **IC Relevance = "Most Relevant"** items from the board outrank "Good to know" ones
   regardless of category — that tag is already a human judgment call, trust it.
4. Drop anything tagged `IC Relevance = Good to know` AND unrelated to AI/Enterprise
   unless the digest would otherwise be very short.

## Output — one digest, short

```
# Weekly pulse — [date range]

Sources pulled: Product Updates board (N items, [date range]) · Slack ([channels that
returned data]) · monday-all ([News/KB hits, or "nothing new"]).

## Most relevant
- **[Title]** — [Release Status]. [One-line why it matters, EMEA/AITP angle if there
  is one]. [Source link]

## Also worth knowing
- **[Title]** — [one line]. [Source link]

## Nothing new this week
[Only if genuinely nothing worth surfacing — say so plainly, don't pad.]
```

Keep it scannable — this is a five-minute Monday read, not a report. No corporate fluff.
If an item's client relevance is a stretch, don't force it — just state what shipped.

## Feeding the toolkit — update skill changelogs automatically

After producing the digest (every run, manual or scheduled), write the relevant
findings into the toolkit's own reference files so other skills stay current
without Basti ever asking. This is the whole point of doing this automatically —
he shouldn't have to remember to paste findings anywhere.

Write into the connected workspace folder (Basti's local copy of this toolkit —
currently `/Users/sebastianse/Desktop/skills copy`, but always resolve it as
"the connected workspace folder" rather than hardcoding the path, since it may
move):

- `monday-vibe/references/changelog.md` — any Vibe feature releases/changes this run found.
- `monday-ai-suggester/references/changelog.md` — a summary by bucket (Agents / Sidekick / Vibe / AI in Automations) of what shipped, cross-referencing monday-vibe's changelog rather than duplicating full detail.
- `monday-ai-advisor/references/changelog.md` — releases that change how a feature should be explained or pitched (new capability, new "how it works" detail), written so it's easy to fold into a client explanation.
- `monday-scaling-watch/references/changelog.md` — platform bugs/incidents only (not feature releases, not scaling-limit changes — those still go through monday-scaling-watch's own update flow into `limits.md`/`scaling-themes.md` when confirmed).

For each file:
1. Read the current file (create it with a short header explaining its purpose and the "newest first, fed by weekly-pulse" convention if it doesn't exist yet — see any of the existing changelog.md files in this toolkit for the header format to match).
2. Write a new dated section for this run's window (e.g. "## 2026-09-01 to 2026-09-07"), formatted like the existing entries in that file (source links included).
3. Insert the new section **right after the header/intro paragraph, before all previous entries** — newest first.
4. Only write to a given file if this run actually found something relevant to it. Don't create empty or "nothing new" sections — that's noise. If nothing relevant landed for a skill this week, skip writing to its changelog entirely.

If the workspace folder isn't connected/writable in a given run (e.g. a scheduled
run before Basti has connected it), skip this step silently — don't fail the
whole digest over it. The chat digest is still the primary deliverable; the
changelog writes are a bonus that keeps the rest of the toolkit fresh.

## Scheduling

This skill is designed to run on a recurring weekly schedule (a scheduled task calling
this skill, e.g. Monday mornings) so Basti never has to remember to run it. On a
scheduled run, skip any conversational framing and go straight to the digest —
then do the changelog updates above before finishing.
