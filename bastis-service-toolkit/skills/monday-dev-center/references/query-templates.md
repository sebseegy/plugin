# Query templates (paste into the CLIENT playground)

Replace `<WS>`, `<BOARD>`, `<BOARD_IDS>` and so on. Every read here selects structure and item values only.
Don't add `users { email }` dumps or item updates/comments unless the task needs them. Keep the
client data Claude sees to the minimum.

## 0. Identity check (first query of every session)
Confirms which account and workspace the playground is pointed at, before anything else runs.
```graphql
query {
  me { name account { slug name } }
  workspaces(ids: [<WS>]) { id name kind }
}
```
Stop if `account.slug` isn't the client in the project context.

## 1. Structure (the whole workspace) → `01_structure.json`
```graphql
query {
  complexity { before query after }
  folders(workspace_ids: [<WS>], limit: 100) { id name parent { id } children { id name } }
  boards(workspace_ids: [<WS>], limit: 100, state: active) {
    id name type board_kind description items_count updated_at board_folder_id
    owners { id name }
    groups { id title position }
    columns { id title type description settings_str }
    views { id name type }
  }
}
```
- If 100 boards come back, add `page: 2`.
- Subitem boards are included (`type: sub_items_board`).
- If one is missing, add `sub: boards(ids: [<SUB_ID>]) { id name type items_count columns { id title type settings_str } }`.

## 2. Item usage → `02_items_<group>.json` (one file per 3–6 boards)
Always keep `id name` on each board so `devcenter.py usage` can match it to the structure.
```graphql
query {
  complexity { before query after }
  b1: boards(ids: [<BOARD>]) { id name items_page(limit: 500) { cursor items { id name group { title } column_values { id text ... on BoardRelationValue { linked_item_ids } ... on MirrorValue { display_value } ... on FormulaValue { display_value } } } } }
  b2: boards(ids: [<BOARD>]) { id name items_page(limit: 500) { cursor items { id name group { title } column_values { id text ... on BoardRelationValue { linked_item_ids } ... on MirrorValue { display_value } ... on FormulaValue { display_value } } } } }
}
```
- For a subitem board, add `parent_item { id name }` to the items.
- Several small boards (e.g. a product catalogue): `boards(ids: [<ID1>, <ID2>, ...]) { id name items_page(limit: 500) { ... } }`.
- **More than 500 items:** a non-null `cursor` means there are more pages. Continue with
  `next_items_page(cursor: "<cursor>", limit: 500) { cursor items { ... } }`.
- **If `FormulaValue { display_value }` errors:** that API version doesn't support it. Drop the fragment.
- **Complexity error:** split the query into smaller groups of boards.

## 3. Automations → `03_automations.json` (API version **dev**)
```graphql
query {
  a1: board_automations(board_ids: <BOARD>, limit: 100) { items { id title description active created_at updated_at workflow_blocks workflow_variables } legacy_automations cursor }
  a2: board_automations(board_ids: <BOARD>, limit: 100) { items { id title description active created_at updated_at workflow_blocks workflow_variables } legacy_automations cursor }
}
```
Include every board that could have automations, subitem boards too. Then run:
`devcenter.py automations --file 03_automations.json --structure 01_structure.json --alias a1=<BOARD> a2=<BOARD>`

## 4. Targeted reads (small; paste in chat)
```graphql
# a few columns on one board
query { boards(ids: [<BOARD>]) { columns(ids: ["<col1>", "<col2>"]) { id title type description settings_str } } }

# specific items and columns
query { items(ids: [<ITEM1>, <ITEM2>]) { id name column_values(ids: ["<col1>", "<col2>"]) { id text } } }

# one user by name (for owner / people ids)
query { users(name: "<First Last>") { id name } }
```

## 5. Mutation patterns (label each part; ask for OK before deletes)
```graphql
mutation {
  # --- deletes / archive (reversible via board trash / archive)
  del_x:  delete_column(board_id: <BOARD>, column_id: "<col>") { id }
  arc_y:  archive_item(item_id: <ITEM>) { id }
  del_a:  delete_board_automation(id: <NEW_BUILDER_ID>, board_id: <BOARD>) { __typename }

  # --- metadata
  t_col:  change_column_title(board_id: <BOARD>, column_id: "<col>", title: "<New title>") { id title }
  d_col:  change_column_metadata(board_id: <BOARD>, column_id: "<col>", column_property: description, value: "<text>") { id description }
  b_desc: update_board(board_id: <BOARD>, board_attribute: description, new_value: "<text>")

  # --- values
  v1:     change_simple_column_value(board_id: <BOARD>, item_id: <ITEM>, column_id: "<status_col>", value: "<Label>") { id name }
  clr:    change_multiple_column_values(board_id: <BOARD>, item_id: <ITEM>, column_values: "{\"<date_col>\":null}") { id name }
  link:   change_multiple_column_values(board_id: <BOARD>, item_id: <ITEM>, column_values: "{\"<rel_col>\":{\"item_ids\":[<ID>]}}") { id }

  # --- workspace organisation
  fold:   create_folder(workspace_id: <WS>, name: "1 · Pipeline") { id name }
  move:   update_board_hierarchy(board_id: <BOARD>, attributes: { workspace_id: <WS>, folder_id: <FOLDER> }) { __typename }
  own:    add_users_to_board(board_id: <BOARD>, user_ids: [<USER>], kind: owner) { id }
}
```

### Columns with JSON defaults (Variables panel)
```graphql
mutation ($f: JSON, $m: JSON) {
  f1: create_column(board_id: <BOARD>, id: "fc_example", title: "_Example £ (numeric)", column_type: formula, defaults: $f) { id title settings_str }
  m1: create_column(board_id: <BOARD>, title: "Example £", column_type: mirror, defaults: $m) { id title settings_str }
}
```
```json
{
  "f": { "formula": "IF({deal_stage} = \"Confirmed\", {deal_value}, 0)" },
  "m": { "relation_column": { "<rel_col>": true }, "displayed_linked_columns": [{ "board_id": "<LINKED_BOARD>", "column_ids": ["<col>"] }], "function": "sum" }
}
```
Check that `settings_str` in the response isn't `{}`. If it is, the defaults were lost.

### Table view (this form worked on 30 Sep 2026)
Hide the columns you don't want; everything else stays visible. `filter` and `sort` are optional.
```graphql
mutation {
  v: create_view_table(board_id: <BOARD>, name: "Catalogue",
       filter: { rules: [{ column_id: "<year_col>", compare_value: [1], operator: any_of }] },
       sort: [{ column_id: "<date_col>", direction: asc }],
       settings: { columns: { column_properties: [
         { column_id: "<col_to_hide_1>", visible: false },
         { column_id: "<col_to_hide_2>", visible: false } ] } }) { id name }
}
```
- Status `compare_value` takes label **ids**.
- The Main table can't be changed. Point the team at the new view instead.
- Grouping is set with `settings: { group_by: ... }`. Check `TableViewSettingsInput` in the schema before using it.

### Dashboard + widget
```graphql
mutation ($w1: JSON!) {
  d:  create_dashboard(name: "Team – Pipeline", workspace_id: <WS>, board_ids: [<BOARD>], kind: PUBLIC, board_folder_id: <FOLDER>) { id name }
}
# then, with the new dashboard id:
mutation ($w1: JSON!) {
  n1: create_widget(parent: { kind: DASHBOARD, id: <DASH> }, kind: NUMBER, name: "Pipeline £", settings: $w1) { id name }
}
```
Get the widget settings schema first (`all_widgets_schema` via the schema tools, or ask Basti). Set the filters in the UI afterwards.
