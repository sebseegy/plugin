# monday Platform API — facts this skill relies on

Verified against developer.monday.com on **2026-09-29** (API Current = 2026-07; 2026-10 is
Release Candidate and is expected to become Current on 2026-10-01). Re-verify anything
marked ⚠ before trusting it on a large build. If a doc page contradicts this file, the doc
page wins — update this file.

## Contents
1. Transport & playground
2. Boards
3. Columns (generic create + typed settings)
4. Groups
5. Views
6. Folders / workspaces
7. Subitems
8. Hard limits
9. Not replicable via public API
10. Open verification items

---

## 1. Transport & playground
- Endpoint `https://api.monday.com/v2`, single POST, `Authorization: <token>`, `API-Version` header.
- Playground: `https://monday.com/developers/v2/try-it-yourself` (Developer Center). Runs as the
  logged-in user of **that** account — this is why the consultant runs target mutations there
  and no token is ever needed by Claude.
- Multiple mutations in one document with aliases (`a1: create_x(...)`) execute **serially**
  (GraphQL spec for root mutation fields). A failing field returns `null` + an `errors[]` entry
  whose `path[0]` is the alias; later fields still run. The replicator relies on this for
  per-op success tracking.
- Playground: inline literals, no `$variables` (copy-paste ready).

## 2. Boards
- `create_board(board_name, board_kind: public|private|share, workspace_id, folder_id,
  description, empty: Boolean, board_owner_ids, template_id, item_nickname)` → `Board`.
  - `empty: true` = "without any default items". Default columns/groups may still exist →
    the replicator selects `columns { id type title } groups { id title }` in the response and
    cleans them up later.
  - **40 create_board / duplicate_board calls per minute.** Chunk ≤35 and wait 60 s between parts.
  - Arg is `board_owner_ids` (not `board_owners_ids`).
  - `use_mls_template` (multi-level boards) is **2026-10+ only** → MLS boards are manual in v1.
- `boards(workspace_ids: [...], hierarchy_types: [classic, multi_level], ...)` — without
  `hierarchy_types`, only classic boards are returned for workspace queries.
- `type` on Board: `board | custom_object | document | sub_items_board`.
- `duplicate_board` is same-account only → cannot be used cross-account.

## 3. Columns
- `create_column(board_id, id, title, column_type, description, defaults: JSON, after_column_id, capabilities)`.
  - **Custom `id`**: 1–20 chars, **only lowercase letters and underscores**, unique on board,
    cannot reuse IDs of deleted columns. Source IDs with digits (e.g. `date4`, `text_mkx1`)
    are invalid → replicator slugs from title.
  - `defaults` validated against the type schema: `query { get_column_type_schema(type: X) }`.
  - Read `settings` (JSON) ≈ write `defaults.settings` for: status, formula, mirror,
    board_relation (verified shapes below). `settings_str` deprecated since 2025-10.
- **status**: settings `{labels:[{id,label,color,index,is_done,description,hex?,is_deactivated?}]}`.
  Create requires `label,color,index`. **Label ID = color enum numeric ID** (each color once per
  column) → reproducing colors reproduces label IDs, so status-based view filters stay valid.
  `hex` overrides and deactivated labels are not reproduced → manual sheet.
- **formula**: `defaults: {"settings":{"formula":"{col_id} * 2"}}` — references column IDs → remap.
  Formula `display_value` can't read mirror/connect columns (read-side limit only).
- **mirror**: `{"settings":{"relation_column":{"<relation_col_id>":true},
  "displayed_linked_columns":[{"board_id":"<id as string>","column_ids":["..."]}]}}`.
  Needs the relation column and target columns to exist first.
- **board_relation** (connect boards): settings `{boardIds:[int], allowMultipleItems, allowCreateReflectionColumn}`.
  ⚠ Doc example passes these at top level of `defaults`; schema nests under `settings`.
  Replicator uses `{"settings":{...}}` (schema form). If it errors, retry without the wrapper via `override-settings`.
- **dropdown** ⚠ settings shape not confirmed on the doc page read — check `get_column_type_schema(type: dropdown)`
  on first failure and use `override-settings`.
- Types always skipped: `name` (exists). `subtasks` handled via subitem spawn.
- Types treated manual: `button` (action = automation), integration/app columns, AI columns.

## 4. Groups
- `create_group(board_id, group_name, group_color: "#hex", relative_to, position_relative_method: before_at|after_at)`.
  Without positioning, new groups insert **at the top** → initial build creates in reverse order;
  delta adds anchor to neighbours with `relative_to`.
- `update_group(group_attribute: color)` wants named colors, not hex (create accepts hex).
- A board must keep ≥1 group → defaults deleted only after replicated groups exist.

## 5. Views
- `create_view(type: ViewKind)` — **ViewKind = APP | DASHBOARD | FORM | TABLE only.**
  Kanban, Gantt, Timeline, Calendar, Chart, Workload, Map, etc. → manual.
- `create_view_table(board_id, name, filter: ItemsQueryGroup, sort: [ItemsQueryOrderBy], settings, tags)`.
- Read: `views { id name type settings filter sort tags }`. ⚠ read `filter` JSON → `ItemsQueryGroup`
  input mapping is best-effort; always confirm filters in UI.
- `duplicate_view` exists (2026-10+) but same-board only.

## 6. Folders / workspaces
- `folders(workspace_ids:[..], limit ≤100) { id name color parent { id } sub_folders { id } }`.
- `create_folder(name, workspace_id, parent_folder_id, color: FolderColor)` — same enum read and write.
- `create_workspace(name, kind: open|closed, description)`.

## 7. Subitems
- Subitem board is created by the platform on first subitem. Replicator: placeholder item →
  `create_subitem` (select `board { id columns {..} }` and `parent_item { board { columns(types:[subtasks]) } }`)
  → add columns to the subitem board → delete placeholder.
- ⚠ Confirm the subitems column/board persists after the placeholder is deleted (expected yes).

## 8. Hard limits (Rate limits page, 2026-09-06)
- Complexity: 10M/min per token (1M trial/free), 5M per query.
- Daily calls: 1k (Free–Standard) / 10k (Pro) / 25k (Enterprise); failed calls count.
- Requests/min 1,000 / 2,500 / 5,000; concurrency 40 / 100 / 250.
- 60 s per-call timeout. Keep chunks ≈20 mutations.

## 9. Not replicable via public API (customer accounts)
- Board automations & Workflow Builder workflows (dev-only, account allowlist, FORBIDDEN).
- Integration recipes. Dashboards/widgets (possible but out of v1 scope). Workspace docs (v1 scope).
- Board owners/subscribers mapping (different users per account). Column widths/hidden state.
- Non-TABLE views. Multi-level boards (v1).

## 10. Open verification items (test in a sandbox target first)
- dropdown `defaults` shape. - board_relation wrapper. - `progress`, `dependency`, `time_tracking`
  settings shapes. - whether `empty: true` still creates default columns. - column position when
  created without `after_column_id` (expected: appended right). - subitems persistence after
  placeholder deletion. - view filter translation.
