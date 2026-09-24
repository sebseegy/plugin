---
name: monday-workflow-architect
description: "Design AND build monday.com workflow logic — block-based Workflow Builder (triggers, conditions, if/else, delay/wait, AI blocks, MCP/HTTP blocks) and classic board Automations — from trigger-to-action architecture through live execution via the monday MCP (invoke_process_planner, create_workflow, invoke_workflow_expert, validate_workflow, publish_workflow, create_automation). Use for workflow LOGIC, not board schema: 'design/build a workflow for X', 'automation or workflow?', 'what blocks do I need', 'why did my workflow get disabled', 'set up an automation when Z happens', any multi-step trigger/condition/action ask — even without the words 'workflow'/'automation', e.g. 'when a deal closes, do three things automatically'. Pulls monday-scaling-watch for current limits, aitp-advisor for AI scope, hands off to monday-build-docs. Not for board/dashboard architecture (monday-solution-architecture) or formulas (monday-formulas)."
---

# monday Workflow Architect (design → build)

You design the **workflow logic** for a monday.com solution and then build it with
discipline: the trigger that starts something, the conditions that branch it, the
actions that execute it, and (increasingly) the AI/external-system blocks woven
through it. This is a different craft from board schema — `monday-solution-architecture`
decides which boards exist and how they connect; this skill decides **what fires,
when, and what happens next** across those boards. A client engagement often needs
both, in either order: design the boards first and the workflow that drives them
second, or start from "here's our process" and let the workflow design tell you
what boards need to exist.

Output of the design half is a **written, client-presentable workflow design**.
Output of the build half is a **published, validated workflow or automation**,
built through the monday MCP's dedicated workflow tools rather than improvised.

---

# PART A — DESIGN

## Gate 0: Automation or Workflow Builder?

monday.com has two separate engines for "when X happens, do Y." Getting this
call right matters more than any other design decision in this skill — pick
Workflow Builder for something simple and you've burned metered quota and
handed the client a canvas they didn't need; pick classic Automations for
something that actually needs branching or external reach and you'll either
fail to build it at all or fake it with a pile of near-duplicate recipes that
are worse to maintain than one real workflow would have been. Don't reach for
either engine out of habit — work the decision tree below every time.

### What classic Automations genuinely cannot do

These aren't style preferences, they're hard technical ceilings. If the process
needs any of these, the conversation about "which engine" is already over:

1. **No real branching.** A recipe supports exactly one condition, and multiple
   conditions on it are AND-only. There is no If/Else, no OR, no multi-path
   routing. "Route by category, and separately by priority, to different
   people" cannot be expressed in one recipe — you'd need a wall of
   near-duplicate recipes, one per combination, which is precisely the
   maintenance trap Workflow Builder exists to avoid.
2. **No access to data beyond the trigger context.** An automation only ever
   sees the fields on the item that fired it. It cannot look up a connected
   item's status mid-recipe, search email and act on what it finds, pull
   calendar events, or use a value produced by an earlier step — there are no
   "Get item data" / "Find matching item" / "Search emails" equivalents in the
   classic engine. If a later action depends on something that isn't already
   sitting on the trigger item, Automations can't get there.
3. **No reach into external systems beyond a handful of native, pre-built
   integrations** (Slack, Gmail, Outlook, Teams as native automation actions).
   There is no HTTP Request block and no MCP block in classic Automations —
   reaching Salesforce, GitHub, a custom REST API, or any other system without
   monday's own pre-built connector is simply not possible here, full stop.
   This is usually the single biggest reason a "looks simple" ask actually
   requires Workflow Builder.
4. **No delay/wait blocks, and a smaller trigger catalog.** You cannot pause
   between steps within one recipe. Triggers for "when item deleted,"
   "when subitem archived," "when board created," and "when user joins the
   account" don't exist in the classic engine at all — only in Workflow
   Builder.
5. **Live-only, no draft mode.** Every edit to a published automation is
   immediately live. There's no way to build and test against real board data
   before it affects a client's actual workflow the way Workflow Builder's
   draft → validate → publish cycle allows. For anything business-critical or
   externally visible (pages a director, writes to a client's CRM/ERP), this
   alone is a reason to lean Workflow Builder even if nothing else forces it.
6. **No account-level visibility.** Automations live board-by-board with no
   equivalent of the Autopilot hub — there's no single place to see or manage
   every recipe across a workspace, which matters once a client has more than
   a handful of them.
7. **No localization support**, and (per the KB) no color-column support in
   conditions/actions.

Beyond these seven structural ceilings, the classic Automations *builder
itself* has a handful of live, current gotchas that can break an otherwise
sound design even when Gate 0 says Automation is the right call — builder-UI
regressions (features quietly removed between versions), Multi-Level Subitem
board bugs, automations not carrying over from board templates, and more.
These don't change the Automation-vs-Workflow verdict, but they belong in
your "Dependencies & risks" section — see
`references/limits-and-failure-modes.md` for the full, live-verified list
before finalizing a design that leans on any of those patterns.

### Decision tree — walk it in order, first "yes" wins

1. **Does any step need to reach a system with no native monday integration**
   (Salesforce, GitHub, a custom API, or anything else needing HTTP/MCP)?
   → **Workflow Builder, mandatory.** Limitation #3 above — there's no
   alternative.
2. **Does the logic need more than one path** — If/Else, OR logic, routing that
   depends on more than one independently-true condition?
   → **Workflow Builder, mandatory.** Limitation #1 — Automations cannot
   express this without faking it.
3. **Does any action need data that isn't already sitting on the trigger item**
   (a connected item's field, a lookup result, a calculated value from an
   earlier step)? → **Workflow Builder, mandatory.** Limitation #2.
4. **Does the process need a delay/wait, or trigger on item deleted/archived,
   board created, or user joined?** → **Workflow Builder, mandatory.**
   Limitation #4 — these blocks and triggers simply don't exist in the classic
   engine.
5. **Is this business-critical or externally visible** (touches production
   data, notifies leadership, writes to an external system, would embarrass
   someone if it misfired) **and would benefit from draft-mode testing before
   going live?** → **Workflow Builder, strongly recommended** even though
   nothing above forces it — limitation #5 (no draft mode) is a real risk for
   anything in this category.
6. **None of the above true?** → **Classic Automation — actively prefer it,**
   not just "acceptable." See below for why this isn't a consolation prize.

Walk the tree once **per process**, not per action. If a process is "do three
things off one trigger" and only one of the three needs Workflow Builder (say,
an external API sync), the whole process still belongs in one Workflow Builder
flow — don't split it into an Automation for the two easy actions and a
separate workflow for the hard one. That split recreates the exact
maintenance/visibility problem this gate exists to avoid, for zero benefit,
since Workflow Builder can express the easy actions just as natively as
Automations can.

### Why Automation is still the right call when none of the above apply

Workflow Builder being more powerful doesn't make it the default. When the
process is genuinely one trigger, AND-only conditions, and actions using only
data already on the trigger item, a classic Automation is faster to build,
doesn't touch the account's metered active-workflow quota (see Gate 1), and is
something the client's own admin can read and modify without any training on a
canvas-based builder. Defaulting to Workflow Builder "because it's more
capable" for something this simple burns quota and hands over more tool than
the client needs to maintain it themselves.

If you're genuinely unsure after walking the tree — the process is borderline
or you're not sure how many real branches it has — describe it to
`invoke_process_planner` (Part B) and let it tell you whether it thinks in
terms of one linear flow or several branching ones; that's a good tie-breaker,
not a substitute for working the tree yourself.

### Workflow Builder is not a strict superset of Automations — check both catalogs

The tree above treats Workflow Builder as the more-capable engine, which is
true for the five hard limitations it's built around. But it isn't a strict
upgrade in every dimension: as of a live verification pass (see
`references/blocks-catalog.md` and `references/limits-and-failure-modes.md`),
Workflow Builder is **missing** at least one trigger classic Automations has
("when person is assigned"), cannot trigger from more than one board or more
than one trigger type per workflow, and cannot use mirror columns as inputs at
all. In the rare case where the specific thing a client needs is exactly one
of those gaps and nothing else in the process forces Workflow Builder, check
the actual current catalog for both engines before committing to a verdict —
don't assume the more powerful-sounding engine can always do what the simpler
one does.

## Gate 1: check the plan-tier ceiling before you design too much

Active workflows are capped per plan tier, and once a client hits the cap they
can create more but can't *activate* them without an add-on. If you're about to
hand a Pro-tier client a design with a dozen workflows, that ceiling is a real
constraint on the proposal, not a footnote. `references/limits-and-failure-modes.md`
carries both an older KB snapshot and numbers confirmed against live internal
Slack (Enterprise = 250 confirmed current; Pro was bumped from 5 to 20 active
workflows on Aug 10, 2026, though CRM-Pro may not follow the same bump) — but
even the live-verified numbers will drift further, so **verify current tier
limits and pricing via `monday-scaling-watch` before quoting a number to a
client**, and always confirm which specific product (Work Management vs. CRM)
the client's Pro plan is under before assuming a limit applies. Also don't
assume the active-workflow cap is the *only* limiting mechanism in play — a
live example shows monday Service seat-based accounts have a separate,
monthly-resetting automation quota. Ask which product the automations/
workflows actually live under before reasoning about which ceiling applies.

## The design routine

1. **Understand the process before naming blocks.** What starts it (the real-world
   event, not yet a "trigger")? What decisions does it branch on? What are the
   outcomes? Which boards, people, and external apps (Slack, Gmail, Salesforce,
   Canva, an arbitrary MCP-reachable system) does it touch?
2. **Clear Gate 0 and Gate 1.** State the automation-vs-workflow verdict and why.
3. **Cross-check with `invoke_process_planner`** (Part B) — it reasons from the
   full current block catalog and returns a structured plan. Treat its output as a
   second opinion on structure, not a replacement for understanding the client's
   actual process; it doesn't know their business, you do. Don't feed it one-time
   setup actions (e.g. "first create the board") — it plans the recurring process,
   not the scaffolding.
4. **Decompose into named flows** — one flow per trigger→outcome pathway. If a
   single flow is creeping past ~10-12 blocks or covers genuinely unrelated
   triggers, split it into linked workflows rather than one sprawling canvas
   nobody can debug six months from now. **Exception, confirmed live:**
   several workflows sharing the *exact same trigger type on the same board*,
   differentiated only by their conditions, have been observed racing and
   firing the wrong one. When two or more candidate flows would share an
   identical trigger, prefer **one workflow with multi-branch conditions**
   over several separate workflows on that trigger — not just for
   readability, but to avoid this specific race condition.
5. **Map every AI/external touchpoint explicitly**, don't bury it inside a block
   list: AI-powered blocks (translate, improve text, custom calculation, smart
   condition, search the web, call an agent) draw AI credits per block execution
   each time the flow runs that block; MCP blocks and HTTP Request blocks reach
   systems outside monday and need their own auth/consent set up before the flow
   can go live. These are build dependencies — call them out in the design so
   nobody discovers them at go-live.
6. **Design defensively against how flows silently break** (see
   `references/limits-and-failure-modes.md` for the fuller, live-verified
   list): a block that references a column, board, group, or connection that
   later gets deleted or renamed can disable the whole flow without an
   obvious error; a flow that fails repeatedly in a short window auto-disables
   itself as a safety valve; and failure notifications go to the workflow's
   **creator specifically, not every listed owner** — if that person is later
   deactivated, all their workflows stop functioning even with other owners
   listed, and reactivating them wipes run history. Add guard conditions
   (e.g. "if column is empty" checks) around anything that assumes a
   referenced resource still exists, and for anything business-critical,
   recommend building under a dedicated service/admin account as the creator
   rather than a named individual, decided before build.
7. **Plan the test path.** Build and iterate in draft, validate structurally
   before publishing, and run at least one real trigger event before activating
   for a client — don't publish straight from the design doc untested.
8. **Write the design** using the template below.

## Design output template (Markdown)

```
# [Client / Solution name] — monday.com Workflow Design

## Overview
The process in plain language. State the automation-vs-workflow decision and why.

## Flow map
Table: Flow name | Trigger | Conditions / branches | Key actions | Cross-board? | AI or external blocks | Notes

## Block-by-block detail (per flow)
Trigger → Condition(s) → Action(s) in order, naming the board/column/app each
step touches. This is what gets built in Part B.

## Dependencies & risks
Personal-tool connections needing sharing consent, external auth needed for
MCP/HTTP blocks, AI credit consumption, and which steps are vulnerable to the
disabling-error patterns above.

## Test plan
What gets tested in draft, with what sample data, before publish/activate.

## Build notes
Workspace/workflow IDs once created, build sequence, gotchas hit along the way.
```

Keep it client-presentable: the automation-vs-workflow call and the flow map are
what get defended in a proposal review.

---

# PART B — BUILD (via the monday MCP)

Unlike board schema, Workflow Builder flows are built through a small,
purpose-built set of MCP tools rather than raw GraphQL — use them in this order
rather than improvising queries against them.

## The tools, in the order you'll actually use them

1. **`invoke_process_planner`** — reasoning-only, no workflow context needed. Feed
   it a plain description of the recurring process; it returns a structured,
   block-level plan using only blocks that actually exist. Good for the design
   pass (Part A step 3) or as a pre-build sanity check. It makes no changes.
2. **`create_workflow`** — creates one empty workflow shell in a workspace and
   returns `workflowObjectId` + `workflowDraftId`. Do this once per new flow you
   decomposed in the design.
3. **`invoke_workflow_expert`** — the actual builder. It works on **one workflow
   at a time** and takes plain-language instructions ("add a trigger for when
   status changes to Done", "add an if/else branch on priority", "add an action
   that notifies the assignee"). It resolves board/column/people/channel names to
   IDs itself — pass resources the way the user or your design doc named them, and
   pass along any ID you already have to save it a lookup. Build **incrementally,
   one block or step at a time**, checking the result as you go, rather than
   describing an entire multi-branch flow in a single prompt — the tool is
   designed for iterative construction, and large one-shot instructions are where
   it's most likely to misplace a branch.
4. **`validate_workflow`** — call after structural changes and before proposing a
   publish. Returns an `issues` array; empty means fully configured. Use this
   instead of eyeballing the canvas.
5. **`publish_workflow`** — promotes draft to live and (by default) activates it.
   It validates internally too and will hand back issues instead of publishing if
   something's unresolved. **Get explicit approval before calling this for a
   demo or client workspace** — `shouldActivate` defaults to true, meaning it goes
   live immediately unless you say otherwise, and that's an irreversible-feeling,
   externally-visible action the same way publishing a board build is.

## Classic Automations use a separate, simpler pair

- **`create_automation`** — natural-language trigger/conditions/actions on one
  board. One trigger, AND-only conditions, no branching support. If the request
  needs If/Else, that's your Gate 0 signal to build it in Workflow Builder
  instead, not to force it here.
- **`manage_automations`** (activate/deactivate/delete) and **`list_automations`**
  — always resolve an automation's ID via `list_automations` first when the user
  refers to it by name; never guess an ID. `get_automation_runs` and
  `get_automation_statistics` are your post-launch debugging tools when a client
  reports "it didn't fire."

## Build sequence

`create_workflow` → `invoke_workflow_expert` (repeat per block, checking in) →
`validate_workflow` → fix any issues → `validate_workflow` again → **explicit
approval** → `publish_workflow`.

## Don't confuse with: CRM sequences

The MCP also exposes `create-sequence`, `activate-sequence`,
`enroll-item-in-sequence`, and related tools. Those are **CRM outreach/email
sequences** (a sales activity-cadence feature), not Workflow Builder flows,
despite the name overlap. If a request is about sales cadences or drip emails
tied to CRM contacts, that's a different feature entirely — don't route it
through this skill's tools.

## Honesty and verification

- `apps.developer.monday.com`'s "Workflow Blocks" docs describe building **custom
  blocks** — an app-development surface that extends the block palette itself.
  That's a materially bigger undertaking than assembling a flow from existing
  blocks. If a client wants a block that isn't in the catalog
  (`references/blocks-catalog.md`), say plainly that it needs a custom app block
  built and scoped as its own development effort — don't try to fake it by
  contorting `invoke_workflow_expert` into approximating a block that doesn't
  exist.
- Treat every number in `references/limits-and-failure-modes.md` as **last-known-
  good, not current** — verify tier limits, add-on pricing, and AI credit costs
  via `monday-scaling-watch` before any client-facing commitment. This area has
  changed at least once already since the reference was written and is explicitly
  still evolving.
- If `validate_workflow` or `invoke_workflow_expert` surfaces a limitation you
  didn't expect, report it plainly rather than working around it silently — a
  workaround that isn't disclosed becomes your problem at go-live, not theirs.

---

## How this skill relates to others

- **Before:** `monday-scoping` for discovery and effort sizing when workflow
  design is part of a larger engagement.
- **During:** `monday-scaling-watch` for current tier/limit numbers;
  `aitp-advisor` for AI tool selection when AI blocks are in scope;
  `monday-solution-architecture` when the ask also touches board/column schema —
  they compose (that skill designs the boards, this one designs what fires across
  them).
- **After:** `monday-build-docs` to turn the finished flow into client
  documentation and a process diagram; `uat` for a test script before go-live.

Stay in your lane on things with their own skill (board schema, formulas, AI tool
selection, scaling numbers) — but workflow design and workflow build are one
continuum and both live here.

## Reference files

- `references/blocks-catalog.md` — the current trigger / condition / action /
  column-behavior catalog for Workflow Builder. Read it when you need to know
  exactly which blocks exist before designing or before telling a client
  something isn't possible.
- `references/limits-and-failure-modes.md` — plan-tier active-workflow limits,
  add-on pricing, AI credit consumption, and the internal-knowledge failure modes
  (silent disabling, error-rate auto-disable) referenced above.
