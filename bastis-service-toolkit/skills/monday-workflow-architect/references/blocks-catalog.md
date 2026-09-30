# Workflow Builder block catalog

Snapshot date: August 2026, sourced from monday-all Knowledge Base ("workflow
builder/AI Workflows Blocks", CX-maintained, verified) **plus a live
verification pass against the internal `#ask-ai-workflows` Slack channel on
August 27, 2026** — that pass is what surfaced the corrections and gaps marked
"(live, Aug 2026)" below, several of which contradict or refine the older KB
article. Blocks ship weekly — treat all of this as a strong starting point,
not a guarantee of completeness. If a design depends on a block not listed
here, search monday-all (`knowledge_search`) or ask `invoke_process_planner`
before telling a client something isn't possible — and if this file's KB
source and a live check disagree, trust the more recent one and say so.

## Triggers

- When status changes to something / from something to something
- When subitem status changes
- When item created / when subitem created
- When date arrives / when subitem date arrives
- When form is submitted
- When column changes / when subitem column changes
- Every time period
- When button clicked
- When item moves to group / when item moves to board

**Missing vs. classic Automations (live, Aug 2026):** "When person is
assigned" exists as an Automations trigger but was confirmed **not present**
in Workflow Builder as of this scan. Don't assume Workflow Builder's trigger
list is a strict superset of Automations' — check both catalogs for the
specific trigger a design needs.

**Structural limits, not just missing triggers (live, Aug 2026):** a single
workflow can only be triggered from **one board** (no multi-board trigger) and
by **one trigger at a time** (no multiple trigger types feeding one workflow).
Both were live pain points this week with no confirmed fix on the roadmap —
see `references/limits-and-failure-modes.md` for the client-facing framing.
- When user joins the account (any role, or a specific role)
- When board created (workspace-scoped)
- When update created
- When item name changes
- When item deleted / when subitem deleted
- When item archived / when subitem archived
- When email is received (Gmail and Outlook blocks)
- When message is received in channel (MS Teams only, currently)

Several of these (item deleted, item archived, board created) exist **only** in
Workflow Builder, not classic Automations — that's often the deciding factor on
Gate 0 by itself.

## Conditions

- If status is something
- If all subitems' status is something (if the item has no subitems, this
  branch resolves to "no" — don't assume "no subitems" silently passes)
- If dropdown meets condition / if number meets condition
- If item is in this group
- If column is empty
- If person is someone
- **Smart condition** — natural-language condition evaluated by AI, e.g. "check
  if the email text has no spelling or grammar mistakes." Useful for fuzzy
  judgment calls a rigid column-comparison can't express, but it's an AI block —
  it draws credits and its judgment should be spot-checked before it gates
  something consequential (e.g. auto-rejecting a request).

Multi-branch conditions let one condition block fan out into more than two
paths (e.g. per-assignee routing) — don't chain multiple binary if/else blocks
when a single multi-branch block expresses the same logic more legibly.

## Actions

Board/item manipulation: Create item, Create subitem, Update item, Update
subitem, Change status, Move item to group, Move item to board, Connect boards,
Change column value (items and subitems), Clear column value, Set date, Push
date, Set hour / set hour to current time, Add assignee, Replace assignee,
Duplicate item, Duplicate group, Duplicate board, Create group, Create board,
Create board from template, Create update, Assign item creator, Delete item,
Archive item, Subscribe user to board, Start/stop time tracking.

Cross-board / cross-workspace lookups: **Get item data** (fetch values from an
item anywhere, not just the current board — this is what makes cross-board
flows possible), **Find matching item/subitem** (search any board by column
value; branches into found/not-found), **Find connected item/subitem** (follow
a connect-boards column to fetch the linked item's data).

Communication: Notify someone, Notify in channel (Slack), Notify users (Slack),
Send email (Outlook, Gmail), Search email (Outlook, Gmail — fetches, doesn't
act, feeds later blocks), Download attachments (Gmail — needs a message ID,
typically piped from a preceding "search emails" block), Get calendar events
(Google, Outlook), Search channel/chat messages (MS Teams).

External reach without a pre-built integration: **HTTP Request block** (sends
outbound API requests directly from a workflow), **MCP block** (calls any
external system's own MCP server — e.g. GitHub, Salesforce — from inside the
workflow). Both need their own auth set up before the flow can run; flag as a
build dependency, not just a design detail. **Live note (Aug 2026):** an
outbound HTTP Request has been reported timing out specifically from monday's
own network in at least one case while working fine from outside it — if a
client's webhook/API endpoint isn't receiving calls, don't assume it's purely
a client-side firewall issue; test the exact endpoint early rather than late.

**Loop block:** iterates an action across multiple items/subitems. **Live
note (Aug 2026):** column-type support inside loops is inconsistent —
Number columns on all-subitems updates and Timeline columns at the subitem
level have both been reported as not mappable/selectable inside a loop.
Confirm the specific column type actually works inside a loop for the
account in question before designing a bulk-update flow around it, don't
assume every column type behaves the same inside a loop as it does in a
plain action block.

Docs: Create Doc, Add Doc Content (can pull content dynamically from item
data across boards). Known gap as of this snapshot: can't create a doc
column-scoped or template-based via these blocks — check current state before
promising it.

CRM-specific: Send Campaign (must originate from the Marketing Contacts board),
Duplication detection.

## AI-powered blocks (draw AI credits — see limits file)

Translate text, improve text, custom calculation/action via natural-language
instruction, **search the web**, **call my agent** (invoke an existing AI Agent,
including CRM agents like Chris/Lexi, or a custom agent already built — agents
themselves are created elsewhere, this block only invokes one that exists).

## Column-specific behavior worth knowing

- **Mirror — conflicting sources, trust the live one.** The older KB article
  says a step can be populated with a mirror column's textual value. A **live
  Slack check on Aug 27, 2026 says the opposite: mirror columns are not
  usable as inputs inside workflow blocks at all**, and any formula that
  itself references a mirror is also excluded (see Formula below). Given the
  live source is more recent and came directly from an internal engineering
  Q&A thread, treat mirror-column support as **not available** until you've
  confirmed otherwise for the specific account — this is exactly the kind of
  conflict worth telling the client about rather than silently picking one
  answer: "our reference material disagrees with itself here, let me confirm
  against your account before we depend on it."
- **Dependency** — can only be populated via "create new item" and "change
  column value" blocks.
- **Files** — can be copied item-to-item via "create new item" / "change column
  value"; can also be pulled from an update, but only via the "when update is
  created" trigger.
- **Formula** — supported as read values in a workflow (via trigger item or
  "get item data"), and convertible to Date/Number via "convert text to
  number"/similar converter blocks — **but only for a "plain" formula.**
  Confirmed live: a formula is **not selectable in a workflow block at all if
  it references another formula column, a mirror column, or a creation-log
  column** (the earlier "cannot use a formula that depends on a mirror" note
  undersold this — it's not just mirrors, it's formula-of-formula and
  creation-log too). If a formula column feeding a design chains off any of
  those, expect the workflow builder to simply not offer it as an option and
  plan a workaround (e.g. a plain intermediate formula/number column
  maintained separately) rather than discovering this mid-build. **This
  restriction isn't Workflow-Builder-specific** — confirmed live in classic
  Automations too: a formula referencing a creation-log column can no longer
  be mapped into an automation's "change column value" action either. Whether
  a formula can directly *trigger* a classic automation recipe is unconfirmed
  as of this scan — verify rather than assume it works.
- **Timeline** — settable via "create item"/"create subitem"/"change column
  value" (e.g. set start = creation date, end = due date on a status change).
- **Triggering user** — any people-type field or notify action can reference
  "the user who triggered this run" directly, without looking them up.
- **Multi-Level Subitem (MLS) boards — live correctness risk, not just a
  limitation.** A confirmed live bug: a trigger correctly fires on the
  triggered (sub-)item, but certain actions (e.g. "change item name," a
  status-label action) have been observed applying to the **top-level parent
  item instead of the actual triggered item.** If a design touches an MLS
  board, budget extra test time specifically to confirm actions land on the
  item you expect, not just that the run completed without an error.
