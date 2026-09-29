---
name: monday-build-replicator
description: Replicate a monday.com build (workspace, folders, boards, groups, columns incl. status labels, dropdowns, connect-boards, mirrors, formulas, subitems, table views) from a source account — monday Spaces, a demo or sandbox account — into a CLIENT account that has no AI/MCP enabled, by generating staged, copy-paste-ready GraphQL for the client's Developer Center API playground. Also pushes later changes (delta) from the source build to the client. Use this whenever Basti says "move/port/copy/replicate/push the build to the client", "write the queries to build this in the client account", "pull the setup from Spaces/demo", "client has no MCP/AI", "rebuild these boards in [client]", "sync my changes to the client", or pastes a monday API JSON response while doing a build hand-over — even if he doesn't say "replicate". Not for designing the architecture (monday-solution-architecture), formulas (monday-formulas), or automation logic (monday-workflow-architect).
---

# monday build replicator

Source build (Spaces / demo / sandbox) → portable blueprint → staged mutations the consultant
pastes into the **client's** API playground → pasted responses feed the next stage → verification diff.

Claude never touches the client account and never sees a token. That is the point of the design,
not a limitation: it keeps this workflow outside the "AI tool connected to a client account" problem
(Delivery hold of May 2026, Legal's sub-processor rule). The only client data Claude sees is what the
consultant pastes back — and every target query here selects **IDs and structure only**.

Part of **bastis-service-toolkit** (Craft — Build). Upstream: `solution-build` /
`monday-solution-architecture` design and build the source; this skill moves it. Downstream:
`monday-build-docs` documents the client build, `uat` tests it.

Engine: `scripts/replicator.py` in this skill's directory (stdlib Python). API facts it relies on, with sources and open
verification items: `references/api-facts.md` — read it before debugging any failed op.

## Guardrails (why each exists)

1. **No tokens in chat.** If a token is pasted, say so plainly and tell Basti to regenerate it in the
   Developer Center. Tokens never go into files, commands, or examples.
2. **Source ≠ client.** Extraction runs only against the source account. If a monday MCP read tool is
   connected, you may run the extraction through it **only after** `query { me { account { slug name } } }`
   shows the source account. Never run anything against a client account yourself.
3. **Additive by default.** The engine only generates deletions for objects the plan itself created
   (default columns/groups of boards it created, its own placeholder items). Never hand-write a
   delete/archive for a client object; removals in delta mode go to the manual sheet.
4. **Nothing is "done" until a response is ingested.** Don't advance stages on "looks fine" — ingest
   the pasted JSON; the engine tracks per-op success.
5. **Dry-run on a second sandbox first** for any build >5 boards or with mirrors/subitems. The open
   items in `references/api-facts.md §10` are real.
6. **Structure only.** No item data migration in this skill. Sample data → separate, explicit request.

## Project context (toolkit convention)

If the project folder is available, read the project `meta.json` **before asking anything**:
- `build.build_account` / `build.build_workspace_ids` → source account + workspace ID(s).
- `build.client_workspace` → target workspace (pass as `--target-workspace-id`).
- client `meta.json` → `monday_environments.client_account` (`slug`, `mcp_access`). Even when
  `mcp_access` is true, use this skill for the transfer unless Basti says otherwise — it keeps the
  client account outside Claude's reach.
- If `build.stage` is already `transferred`/`client_build`/`live`, this is a **delta** run (see below).

File outputs into the project:
- `deliverables/replication/state.json` (engine state — re-upload this to continue later)
- `deliverables/replication/<project>_<stage>_partN.graphql` (what was pasted, for the audit trail)
- `deliverables/manual-build-sheet.md`
- Append non-replicable items (automations first) to `deliverables/risk-log.md` if it exists.

After a clean `diff` (all boards OK), propose — and on "yes" write — the project `meta.json`
update the toolkit expects: `build.stage = "transferred"`, `transferred_at = <today>`,
`source_of_truth = "client_account"`, `client_workspace = <target WS id>`. This is what stops
`status` / `solution-build` from judging progress off the stale Spaces copy.

## Working files

Work in `/home/claude/replicator/<project>/` (then copy into the project's `deliverables/` as above). Save every pasted JSON to a file there before running
the engine (`source_p1.json`, `resp_structure_1.json`, …). After **every** ingest, copy `state.json`
and `manual_build_sheet.md` to `/mnt/user-data/outputs/` and present them — the sandbox filesystem does
not persist across sessions. At the start of a continuing job, look for an uploaded `state.json`
first; if absent, ask Basti to upload it rather than rebuilding state from memory.

```bash
R="python3 <dir of this SKILL.md>/scripts/replicator.py"   # resolve once with: find /mnt/skills -path "*monday-build-replicator/scripts/replicator.py"
```

## Workflow

### Step 0 — Scope (one short exchange, only what's missing)
Take from project `meta.json` first; ask only for what's missing: source workspace ID; whether the
client workspace already exists (then its ID) or should be created; project slug for filenames. Workspace ID is in the URL `/workspaces/<id>`.

### Step 1 — Extract from the source
```bash
$R extract-query --workspace-id <SRC_WS>            # page 1 (includes me/workspace/folders)
$R extract-query --workspace-id <SRC_WS> --page 2   # only if page 1 returned 25 boards
```
Give Basti the query in one code block: *"Paste into the **source** account playground → paste the full
JSON back."* Repeat pages until a page returns <25 boards. If the blueprint later reports
`missing_subitem_boards`, run `extract-query --board-ids <ids>` and include that file too.

### Step 2 — Blueprint + gap report
```bash
$R blueprint --source source_p1.json [source_p2.json ...] --name <project> \
   --out state.json --sheet manual_build_sheet.md [--target-workspace-id <CLIENT_WS>]
```
Report back, compactly: boards / columns by bucket (auto, verify, manual) / table vs non-table views /
the manual items that matter (automations, non-table views, outside-set relations, custom hex labels).
**Flag the automation gap explicitly** — it is the biggest manual cost and Basti should see it before
committing to a hand-over date.

### Step 3 — Stage loop
```bash
$R next  --state state.json                         # what's next and why
$R stage --state state.json --outdir out            # writes out/<project>_<stage>_partN.graphql
# ... Basti pastes each part in the CLIENT playground, pastes the responses back ...
$R ingest --state state.json --stage <stage> --response resp_<stage>_1.json [resp_<stage>_2.json]
```
Stages run in fixed order (the engine refuses out-of-order): `workspace → folders (repeats per nesting
level) → boards → structure → subitems → finish → verify`.

| Stage | What it does | Paste-back needed because |
|---|---|---|
| workspace | `create_workspace` (skipped if client WS given) | workspace ID |
| folders | `create_folder`, one nesting level per round | folder IDs |
| boards | `create_board(empty: true)`; returns default cols/groups | board IDs + defaults to clean |
| structure | groups (order-preserving), all columns in dependency order with **pre-assigned IDs**, name-column rename, subitem placeholders, default-column cleanup | group IDs, placeholder IDs, per-op success |
| subitems | `create_subitem` on placeholders → spawns subitem boards | subitem board IDs + their defaults |
| finish | subitem-board columns, subitems-column rename, table views (sort/filter remapped), placeholder + default-group cleanup | per-op success |
| verify | read-only structure query → `diff` | proof |

Presentation per stage — keep it this tight:
- One line: which account, what this stage creates, how many ops, how many parts.
- Each part in its own ```graphql block, in order. For `boards` with >1 part: wait 60 s between parts (40 create_board/min).
- One line: "Paste each response back (full JSON, including `errors` if any)."

Column IDs are assigned deterministically before execution (valid source IDs kept; digit-containing
IDs like `date4` slugged from title). That's why formulas, mirrors, and view filters are rewritten
correctly without extra round-trips — don't hand-edit IDs inside generated files.

### Step 4 — Failures
After ingest, the engine prints `FAILED <op>: <message>`. Per failure:
1. Read the message. Settings/validation error → give Basti
   `query { get_column_type_schema(type: <type>) }` for the **client** playground, read the schema he
   pastes back, then:
   `$R override-settings --state state.json --board <SRC_BOARD> --column <SRC_COL> --settings-json '<inner settings>'`
2. Not reproducible via API → `$R skip-op --state state.json --op <op> --reason "<why>"` (lands on the manual sheet).
3. Regenerate the same stage (`$R stage ...` — only failed/pending ops are emitted) and repeat.
Never re-send ops that succeeded; the engine already filters them.

### Step 5 — Verify
```bash
$R verify-query --state state.json      # Basti runs it in the CLIENT playground
$R diff --state state.json --response resp_verify.json
```
`OK` per board or a precise list of missing/extra columns, groups, table views. Then refresh the
manual sheet (`$R sheet --state state.json --out manual_build_sheet.md`) and present both files.

### Delta — pushing later changes
When Basti iterates in Spaces after the first hand-over:
```bash
$R extract-query --workspace-id <SRC_WS>      # fresh extraction, same as step 1
$R refresh --state state.json --source new_p1.json [...]
```
Additive only: new folders/boards/groups/columns/views get queued; column and group **title** changes
become rename ops; settings edits (labels, formulas), removals, and view changes go to the manual sheet
(changing labels on a live client column can remap existing values — a human decides). Then run the
normal stage loop from `next`.

## What gets replicated

| Replicated automatically | Needs a check after run | Manual (sheet) |
|---|---|---|
| Workspace, nested folders (+color) | dropdown, progress, dependency, time tracking settings | Automations & Workflow Builder |
| Boards (kind, description, folder) | table-view filters | Non-table views (Kanban, Gantt, Chart, …) |
| Groups (title, hex color, order) | column order vs source | Dashboards, docs, forms |
| Columns incl. status labels (IDs preserved via colors), numbers unit, connect boards, mirror, formula | | Owners/subscribers/permissions |
| Subitem boards + their columns | | Button/AI/integration columns, custom hex labels, deactivated labels, relations to boards outside the set, multi-level boards, item terminology |
| Table views (name, sort, best-effort filter) | | |

## Output discipline
- Absolute Mode: no preamble, structured, one code block per paste unit.
- Always say which account each block goes into (**SOURCE** or **CLIENT**) — the one mistake that
  actually hurts is pasting into the wrong playground.
- Never claim a stage succeeded without an ingested response.
- If a request exceeds scope (item data, automations), say so and point to the manual sheet or the right skill.
