---
name: monday-scaling-watch
description: >-
  Reference knowledge of monday.com's scaling limits and scale initiatives, PLUS
  a Slack workflow that checks whether any of it has changed. Use whenever the
  user asks about monday board/dashboard/API limits (items per board, connected
  items, columns, subscribers, widgets, automation/workflow caps, file storage,
  Excel import/export), about mondayDB (2.0/3.0) scale, Portfolio at Scale (PAS),
  Vibe app board limits, or performance at scale. ALSO use it when the user asks
  "what's the latest", "has this changed", "any updates on", "check Slack for",
  or "is this still true" about any monday scaling limit or initiative — these
  numbers move, so verify against Slack before answering. Trigger even when the
  user names a specific limit (e.g. "is it still 750 connected items per
  portfolio board?"). Not for monday API/GraphQL authoring (use
  monday-solution-architecture) or formula authoring (use monday-formulas).
---

# monday Scaling Watch

monday.com publishes hard limits and ships scale improvements faster than any
single document can keep up with. A consultant who quotes a stale number — "the
portfolio limit is 750" when a beta now allows far more, or "100k items on ENT"
when the customer is being offered 1M in a Data Set beta — loses credibility and
mis-scopes work. This skill exists to solve that: it carries a **baseline
snapshot** of what's true, and it tells you **how to confirm whether that
baseline still holds** by checking the places where monday's own teams announce
changes (primarily Slack).

The mindset: treat the bundled references as *last known good*, not gospel. When
the stakes are real (you're scoping, answering a client, or sizing a build),
check Slack for movement before you commit to a number.

## When you're answering from memory vs. checking Slack

Use judgment about how fresh the answer needs to be.

Answer directly from the references (no Slack check needed) when the user wants a
quick orientation, is exploring, or asks about a limit that almost never changes
(character limits, batch-action sizes, subscriber caps). Cite the reference and
note it reflects the snapshot date.

Check Slack first when any of these are true: the user says "latest", "current",
"still", "changed", "updated", or "check"; the topic is one of the **fast-moving
areas** (mondayDB scale, Portfolio at Scale, Vibe board limits, dashboard/perf at
scale, 1M-item beta); the answer will go into a client deliverable or scope; or
the user is making a decision (upgrade, migration, architecture) where a wrong
number is costly.

When in doubt on a fast-moving topic, check. It's cheap and the references
themselves flag which topics drift.

## The reference snapshot

Two files hold the baseline. Read the one that matches the question.

- `references/limits.md` — the stable hard-limits table (items, connected items,
  columns, groups, subscribers, dashboards, files, Excel import/export, API
  rate-ish caps, workflow blocks, portfolio limits). This mirrors the monday CX
  "Is there a limit?" Guru card. Most of these are durable; a few marked with
  *(moves)* are tied to mondayDB scale and should be re-verified.

- `references/scaling-themes.md` — the live, moving initiatives as of the
  snapshot date: mondayDB 3.0 rollout + 1M-item Data Set beta, Portfolio at Scale
  (PAS), Vibe connected-board limit, dashboard/performance-at-scale issues, and
  the infra context. Each theme lists what was true, who owns it, and **exactly
  what to search Slack for to detect a change.**

- `references/changelog.md` — a separate, dated log of *transient platform
  incidents* (bugs, outages) fed automatically by `weekly-pulse` each week.
  Not a scaling limit, but worth checking if a client reports something odd —
  it may already be a known, recently-flagged issue.

Always open the relevant reference before answering — don't rely on this file
alone for specific numbers.

## How to check Slack for updates

The goal is a **targeted recent sweep**: search the channels where monday's
product, enablement, and support teams announce scale changes, look at roughly
the last 30–60 days, and report only what differs from the baseline.

### Channels that matter (search these first)

These are where scale news actually lands. Prefer them over a global search:

- `#cco-enablement-updates` — official enablement announcements (mondayDB rollout
  status, beta sign-ups, limit changes). Highest signal.
- `#ask-monday-db` — mondayDB scale questions and PM answers.
- `#ask-boards` — board-level limits (items, columns, connected items, cells).
- `#ask-projects` — portfolio/project board limits.
- `#ask-dashboards-widgets` — dashboard item/widget/connect-board limits and perf.
- `#ask-vibe-ai` — Vibe app board-connection limits.
- `#ask-work-management` — plan-tier item limits, upgrade questions.
- `#ask-ai-workflows` / `#ask-ai-agents` — workflow block/complexity caps, agent limits.
- `#platform-performance` — infra incidents that reveal practical scale ceilings.

### Search method

Use `slack_search_public_and_private` (load via ToolSearch with
`select:mcp__d548ed99-735e-4721-aa97-f4485c4dab31__slack_search_public_and_private`
— the server ID prefix may differ in the user's session, so search ToolSearch for
"slack search" if that exact name fails). Run several narrow queries rather than
one broad one; Slack keyword search treats spaces as AND and supports no boolean
OR.

Compute a date ~45 days back from today and append `after:YYYY-MM-DD`. Sort by
`timestamp` so the newest announcements surface first. Useful query shapes:

- `mondayDB scale after:<date>` and `mdb 3.0 after:<date>`
- `1M items beta data set after:<date>`
- `item limit board after:<date>` / `connected items limit after:<date>`
- `portfolio limit items after:<date>`
- `vibe board limit after:<date>`
- `column limit after:<date>` / `dashboard items limit after:<date>`
- `<specific number> after:<date>` (e.g. `750 portfolio` or `100k items`) to see
  if a quoted figure is being corrected
- Scope a query to one channel with `in:#cco-enablement-updates <terms>`.

For any promising hit, read the full thread (`slack_read_thread`) before
concluding — announcements are often corrected or qualified in replies (e.g. "1M
is Data Set beta only", "750 is still the per-project limit"). The most reliable
signal is a message from enablement or a PM, not a peer's guess.

### What counts as a change worth reporting

A new number, a beta opening or closing, a "soon" becoming "released", a rollout
default changing (e.g. DB 3.0 becoming standard for new ENT), a workaround being
deprecated, or a limit-increase request path changing. Ignore one-off customer
tickets unless they reveal a real limit shift.

## Reporting the result

Lead with what changed, not with a process recap. For each topic, state the
baseline, then the current status, then the source. Be explicit when something is
beta vs. GA, and which plan tiers it applies to — that distinction is usually
where consultants get burned.

If nothing changed, say so plainly and confirm the baseline still holds (with the
threads you checked as evidence). A confirmed "still 750" is a useful answer.

Always include a Sources section with Slack permalinks for any claim drawn from
Slack, and name the reference file for anything drawn from the snapshot.

## Keeping the snapshot current

When a Slack check turns up a confirmed change, offer to update the relevant
reference file so the baseline doesn't drift further. Edit the specific line,
keep the *(moves)* markers, and bump the "snapshot date" note at the top of the
file. This is what keeps the skill honest over time. If the user also uses a
persistent memory system, offer to record the confirmed change there too.

## Scheduling

Because these numbers drift, this skill pairs naturally with a recurring check.
If the user wants ongoing monitoring ("keep an eye on this", "tell me when it
changes", "every Monday"), offer to set up a scheduled task that runs the Slack
sweep and reports deltas against the snapshot. If Basti just wants the general
"what shipped this week" sweep rather than a specific limit, point him at
`weekly-pulse` instead — it already runs on a weekly schedule and covers this
board plus Slack and monday-all in one digest. weekly-pulse also automatically
appends any confirmed platform incidents it finds to `references/changelog.md`
here, so that file stays current without anyone running this skill directly.
