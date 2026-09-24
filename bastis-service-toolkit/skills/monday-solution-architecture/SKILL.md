---
name: monday-solution-architecture
description: "Design AND build monday.com board architecture — the craft skill spanning solution design through API/MCP execution. Decomposes a need into the three archetypes (PROJECT, PROCESS, REPOSITORY), applies one-board-per-unit-type, picks topology, pressure-tests against scale, then builds it doc-first via the monday MCP, GraphQL, or API-token scripts. Use whenever shaping HOW a workflow is STRUCTURED in monday or building/changing it: 'how should I build this', 'what boards do I need', 'design a solution for this client', 'is this a project or a process', writing/debugging queries-mutations-column payloads, or reviewing a build before it ships. Pulls monday-scaling-watch on limit decisions, aitp-advisor when AI is in scope, hands to monday-build-docs to document. Not for effort/SOW estimation (use monday-scoping) or formula authoring (use monday-formulas)."
---

# monday.com Solution Architecture (design → build)

You design the **board architecture** for a monday.com solution and then build it
with discipline. This spans two jobs that belong together: the **design** (which
boards exist, what each is for, how they connect) and the **build** (doing it
correctly via MCP/GraphQL/scripts without breaking the workspace). A good design
makes the build obvious and stays clean and performant as it grows; a bad one
mixes unrelated work onto one board, breaks reporting, and hits scale ceilings.

Output of the design half is a **written, client-presentable solution design**.
Output of the build half is **correct, documentation-grounded** boards/columns/
automations created via the right surface.

---

# PART A — DESIGN

## The one governing principle

**One board per unit type.** A board manages exactly one kind of work unit. A
project's *task* board holds tasks — not risks, lessons learned, or stakeholders.
When a different unit type appears, it gets its own board and you connect them.
This is the rule messy accounts violate; honoring it keeps each board's items
homogeneous, which is what makes status, automation, filtering, and reporting
behave. The urge to "add one more column" for a different kind of thing is usually
the signal that a new board (or a connection) is the right move instead.

## Before you recommend anything: two gates

### Gate 1 — Scope: which products and AI features?

Establish and state in the design:
- **Which monday product(s):** Work Management, **monday CRM**, monday Dev, monday
  Service. CRM has a canonical board model (Leads → Contacts → Accounts →
  Opportunities, plus Activities) — don't reinvent it. See `references/products.md`.
- **Whether AI features are in scope, and which.** If AI is in play, this skill
  does NOT select the AI tools — hand that to **`aitp-advisor`** (and the AI
  builder skills), then reflect the chosen features in the board design (e.g. a
  form-fed intake board an Agent triages, an Insights widget on a dashboard).

If the user hasn't said, ask before designing.

### Gate 2 — Discovery readiness

Confirm discovery inputs are captured before recommending. Check against
`references/discovery.md` — at minimum the **six core questions** (project or
process and what's the entity; volume/scale; the steps; do all entities follow the
same steps; info captured per step; reporting insights) and the **Intake / Manage
/ Report / Permissions** frame, plus the use-case bank (PMO / Marketing / CRM).

If inputs are missing, ask the user to fill the gaps. Don't hard-block — if they
say "proceed anyway," design and **explicitly flag the assumptions** per unknown.
If discovery itself still needs to be *run*, that's `monday-scoping`'s job — point
there.

## The three archetypes

Classify every work unit — the classification drives the design. Think in terms of
the **entity**: the core unit that moves through the board.

- **PROJECT** — finite work with start and end, toward a deliverable. Items are
  *tasks*; groups are usually *phases*. Related units that orbit it (risks, issues,
  change requests, decisions, lessons learned, stakeholders, milestones, budget)
  belong on their *own* boards.
- **PROCESS** — a repeatable, status-driven pipeline; every item is the same kind
  of entity flowing through the same stages. Never finishes; keeps processing
  arrivals. Usually form-fed. e.g. New → Reviewing → Approved → In progress → Complete.
- **REPOSITORY** — reference / master data; the static "nouns" other boards point
  at (employee directory, asset library, client register). Minimal automation;
  single source of truth.

After classifying, choose a **topology** (Horizontal vs Vertical for a process;
single-board / multi-board / single-for-all for projects). Read
`references/archetypes.md` for templates AND topology trade-offs before laying out
boards — wrong topology is a common, costly mistake. It also lists, per archetype,
which sub-units to keep OFF the main board and give their own.

## How a solution is assembled

A real solution is several boards of different archetypes, **connected** — not one
big board. The marketing example:
- *Requests* → PROCESS (intake + lifecycle)
- *Campaign* → PROJECT (tasks toward launch)
- *Digital Assets* → REPOSITORY (shared library)

An approved request spins up campaign work; both link to the asset repository.
Connect-boards columns wire them; the repository is the shared reference. Make
these relationships explicit.

## The design routine

1. **Clear the gates** (scope + discovery readiness).
2. **Identify entities and workflows** — how does work *enter, move, end*?
3. **Classify each unit** PROJECT / PROCESS / REPOSITORY.
4. **Assign one board per unit type**, name each clearly.
5. **Choose each board's topology** from `references/archetypes.md`.
6. **Define connections** — which boards link, direction, where mirrors roll up.
   Favor a few clean connections over a cross-link web.
7. **Lay out each board** — groups, key columns, and (for a process) the status
   lifecycle in order.
8. **Pressure-test against scale** with `monday-scaling-watch`: items/board,
   connected items, the ~50-boards-per-dashboard reporting ceiling, portfolio
   limits if multi-project, high-volume processes (plan archiving). Verify current
   numbers rather than quoting memory, especially before a client sees it.
9. **Write the design** using the template below.

## Design output template (Markdown)

```
# [Client / Solution name] — monday.com Solution Design

## Overview
1–2 paragraphs: the workflow in plain language and the solution shape.
State the product(s) and any AI features in scope.

## Assumptions & open questions
Discovery gaps and the assumptions made. (Omit if discovery complete.)

## Board architecture
Table: Board | Archetype | Topology | Purpose (the one unit type) | Fed by

## Board details
Per board: archetype + the single unit type; groups; key columns (for a PROCESS,
the status lifecycle in order); connections; automations (high level).

## Connection map
Which connects to which, direction, mirrors for roll-up.

## Scale check
What was verified against current limits and any risks/mitigations.

## AI features (if in scope)
The features chosen (via aitp-advisor) and where each lands.

## Build notes
Sequence, identifiers, gotchas.
```

Keep it client-presentable: justify each board by the one-board-per-unit principle
so it can be defended in a proposal.

---

# PART B — BUILD (API / MCP discipline)

Once the design is set (or when the user is building/changing anything in monday),
build it correctly. You work across three surfaces and advise on **how to build**,
not just how to call an endpoint. North star: every recommendation is grounded in
official documentation and protects workspace stability and scalability.

## Choose the right surface: MCP vs GraphQL vs token script

Three doors into the same platform; pick by job, not habit.

- **monday MCP tools** — interactive, in-session building where monday validates
  inputs. Reach for it when something should be *built now* and maps cleanly to a
  tool. The tool layer often renames parameters and reshapes payloads vs the raw
  API, so **inspect a tool's actual input/output once before relying on its shape.**
- **GraphQL / developer playground** — precise reads, audits, debugging, one-off
  complex operations, and confirming what the API truly supports.
- **API-token script** — **bulk** work (large pulls, migrations, repeated writes)
  needing pagination, retries, dry-run safety. Prefer Python.

When unsure whether a capability exists on a surface, check docs first and say
plainly if it isn't supported. Don't force an operation through a surface that
doesn't cleanly support it.

## Mandatory documentation lookup

ALWAYS search **developer.monday.com** before stating field names, mutation
shapes, column JSON formats, pagination rules, API-version behavior, or whether a
capability exists. This is the single habit that prevents breaking a workspace.

1. Primary entry: `https://developer.monday.com/api-reference/reference/docs`.
2. Run a scoped search (`site:developer.monday.com <topic>`) or open the relevant
   API Reference page directly.
3. Prefer current API Reference pages over memory, forum posts, or screenshots.
4. Never hallucinate capabilities. If a feature isn't documented, state it is
   **not supported** for API purposes.
5. If docs are ambiguous or silent, say so. Don't invent arguments or behaviors.

## Build advisor: structures that scale

Design for where the account is going, not just today's data — a structure fine at
2,000 items can fall over at 80,000.

- **Lead with the workflow, then the structure.**
- **Favor stable identifiers and clean connections** over sprawling cross-board webs.
- **Call out tradeoffs** when two structures both work (scalability, performance,
  governance) so the user/client chooses with eyes open.
- **Protect against bulk-operation ceilings** — mass duplication, large imports,
  heavy automation fan-out can hit processing limits even when no documented cap is
  exceeded.

On any choice touching a limit (items/board, connected items, columns, subscribers,
dashboard items/widgets, connected boards, portfolio sizing, automation/workflow
caps) — or before finalizing a client-facing recommendation — consult
**`monday-scaling-watch`** (it verifies against Slack whether numbers moved). Tell
the user you're doing it and why. For formula columns, defer to `monday-formulas`.

## Standard board query templates

Substitute the board id. Keep `settings` and `settings_str` (the latter may be
phased out; include for backward compatibility and explain why when you paste it).

```graphql
query {
  boards(ids: BOARD_ID_HERE) {
    id
    name
    columns { id title type settings settings_str }
    groups { id title position }
    items_page(limit: 500) {
      items { id name column_values { id value text } }
    }
  }
}
```

For a comprehensive audit including subscribers (permissions, access, guest status):

```graphql
query {
  boards(ids: BOARD_ID_HERE) {
    id
    name
    type
    permissions
    subscribers { name is_guest teams { name id is_guest } }
    columns { id title type settings settings_str }
    groups { id title position }
    items_page(limit: 500) {
      items { id name column_values { id value text } }
    }
  }
}
```

Use type filters to focus a query, e.g. `columns(types: formula)`.

## Group colors: create vs update

- **`create_group`** — `group_color` with **hex codes** (include `#`), e.g.
  `group_color: "#ff642e"`.
- **`update_group`** — `group_attribute: color` with `new_value` as an **accepted
  color string** (not hex). Hex returns "Input color is not in colors options".

Accepted strings for `update_group` `new_value`: `"dark-green"`, `"green"`,
`"lime-green"`, `"turquoise"`, `"orange"`, `"dark-orange"`, `"blue"`,
`"dark-blue"`, `"red"`, `"dark-red"`, `"yellow"`, `"brown"`, `"grey"`,
`"trolley-grey"`, `"purple"`, `"dark-purple"`, `"dark-pink"`, `"light-pink"`.
When mirroring colors from another board, map each source hex to the closest
accepted string.

## Group creation order

`create_group` always inserts the new group **at the top**. To get a specific
top-to-bottom sequence (e.g. PLAN → DESIGN → EXECUTION → LEARN), **create groups in
reverse order**. To fix existing groups in the wrong order: (1) create new groups
in reverse with a temp suffix, (2) `move_item_to_group` all items across, (3)
`delete_group` the old groups, (4) `update_group` to strip the temp suffix.

## Column types

- **People column:** the API `column_type` value is **`people`** — not
  `multiple-person`/`multiple_person`. Wrong value returns HTTP 400.
- Generic `column_values { value text }` is often empty/misleading for structured
  types (dependency, connect boards, mirror, formula). Use the documented **inline
  fragments / typed fields** per column type. If `value` is null, check docs for
  the correct fragment before concluding the cell is empty.

## GraphQL construction (playground vs code)

- **Developer playground:** do NOT use `$variables` unless the user runs from
  code/CLI and wants them. **Inline** board ids, cursors, literals so it's
  copy-paste ready.
- Provide the **whole** query/mutation, not fragments.

## Secrets and `.env`

- Keep monday API tokens in a local **`.env`** (not committed). Scripts read from
  environment variables — never hard-code tokens in source, chat, or examples.
- **Never** print the token, paste `.env` contents, or ask the user to paste a live
  token. Use placeholders (`YOUR_TOKEN_FROM_ENV`) and refer to variable names only.

## Shell and scripts

- For shell commands that could mutate data, include and emphasize a **dry-run**
  mode first when supported.
- For large board/item pulls from the terminal, prefer **Python** (pagination,
  retries, clearer handling than one-off curl).

## Writes and identifiers

- Prefer **`column_id`** (stable) over column title in mutations and scripts.
- Use the documented mutation and payload shape for that column type.
- Cross-board/clone workflows: **read source → map source ids to target ids →
  write on target.** Never reuse item ids across boards.

## Cache, drift, and "API does not match UI"

- If `boards { columns }` omits a column the UI shows (especially right after UI
  changes), suspect **delayed consistency** and **re-query** before creating a
  column programmatically.
- **Avoid** "column not in list → create column" without a guard; it duplicates
  columns. Prefer: wait/re-query, try item-level `column_values`, or ask for the
  column id from settings/URL and target writes by id.
- When debugging odd behavior, note the **API-Version** header used and retry with
  the version the docs recommend.

## Honesty, verification, access

- When the UI exposes a setting the public API doesn't document, state **not
  exposed / not supported for migration** and describe the platform default after
  write. Don't imply API/UI parity unless docs confirm it.
- For "confirm this row/cell/edge" questions, answer using **item id** and **column
  id**, not display name (duplicate names are common). Show the exact query/mutation
  and the minimal parsed result supporting the conclusion.
- Don't assume access to live boards. Ask for ids or use placeholders.

## When building a designed solution — execution order

When turning an approved design into a real workspace, build in dependency order so
mirrored-from boards exist first: folders → boards → columns → groups →
connect/mirror columns → items → column values → automations → dashboards+widgets →
forms → docs → views. For anything without a dedicated MCP tool, fall back to the
general monday API tool (inspect the schema/type details first). **If you are
building for a demo or client workspace, get explicit approval of the full plan
before creating anything** (see the lifecycle build phase, which owns the
approval-gated demo build flow and delegates the method here).

---

## How this skill relates to others

- **Before:** `monday-scoping` runs discovery and sizes effort; build the design on
  top of it.
- **During:** `monday-scaling-watch` validates topology against current limits;
  `aitp-advisor` owns AI tool selection when AI is in scope; `monday-formulas` owns
  formula columns.
- **After:** `monday-build-docs` turns the design/build into client documentation
  and the process-flow diagram.

Stay in your lane on the things that have their own skill (hours/SOW, AI tool
selection, formulas, scaling numbers) — but design and build are one continuum and
both live here.
