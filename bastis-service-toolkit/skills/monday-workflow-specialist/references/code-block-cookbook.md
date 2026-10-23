# Code block cookbook

Grades: A tested in real account by Basti (from his build, 2026-10); B owner-stated; C written from API knowledge, NOT run - run `get_graphql_schema` / `get_type_details` before use.

## Contract (A)
```python
# Inputs: input["name"]. Return a dict whose keys equal the declared outputs.
return {"example_output": input["example_input"]}
```
- Top-level code, no `def main`. Mapped inputs get auto names `code_output_<field>`, `_2`, `_3`. Use the exact generated name.
- Return strings for everything. Always try/except and return `ok`/`error`.
- Give the user the FULL file, never a patch (indentation broke twice, A).
- Expert tool cannot set the Code editor (A). User pastes code and declares inputs/outputs, then saves, before downstream blocks can bind.
- Output cap 512 KB, code 1 MB, timeout 300 s (A, source). Keep outputs small anyway (Oct 13-14 truncation incident at ~4 KB, B).
- Not retried on failure (A): make writes idempotent, add your own dedupe.
- Rate limited per account: 429 shows as "Code block rate limited" (A). Avoid fan-out of many concurrent Code steps.
- Runtime: Python 3.11, pandas, numpy, matplotlib, pillow, requests, httpx, openpyxl (A). `print()` is fine, only the returned dict is the result.

## API helper (A, no Authorization header needed)
```python
import requests
API = "https://api.monday.com/v2"
def gql(query, variables=None):
    r = requests.post(API, json={"query": query, "variables": variables or {}},
                      headers={"Content-Type": "application/json"}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise Exception(str(data["errors"])[:300])
    return data["data"]
```
Egress is limited to api.monday.com and mcp.monday.com/mcp (A). Library install is not possible (A). The bearer token is injected outside the sandbox and narrowed to the caller's scopes, so operations beyond the caller's permissions can fail (A, invariants).

## Tested queries (A/B)
```graphql
# connected items (works for subitems via items(ids:)) - A
query($ids:[ID!],$col:[String!]){ items(ids:$ids){ name parent_item{name}
  column_values(ids:$col){ ... on BoardRelationValue{ linked_item_ids } } } }
# post update - A
mutation($id:ID!,$b:String!){ create_update(item_id:$id, body:$b){ id } }
# owners from any People column - B
query($ids:[ID!]){ items(ids:$ids){ id creator{id}
  column_values(types:[people]){ id ... on PeopleValue{ persons_and_teams{ id kind } } } } }
# users - B
query($u:[ID!]){ users(ids:$u){ id name } }
# notification opening the update - B (delivery not observed)
mutation($u:ID!,$t:ID!,$txt:String!){ create_notification(user_id:$u, target_id:$t, text:$txt, target_type:Post){ text } }
```

## Use-case catalogue (what else the Code block unlocks)
| # | Use case | Evidence | Native alternative |
|---|---|---|---|
| 1 | One workflow for N identical boards via webhook | A (Basti build) | none |
| 2 | Cross-board lookup via connected items where board/column is fixed in native blocks | A | Find connected item (static) |
| 3 | Status guard: block a premature "Done" - read previous value, revert, notify editor, in one block | B (owner-stated, Sep 24) | none |
| 4 | Add people to a team, create team if missing; items on a repository board = teams | B/D (EMEA IC build, Oct 12, video playbook) | none |
| 5 | Relative date push beyond parent/subitem reference | D (Sep 16 reply) | Push date (relative) |
| 6 | Move externally hosted API scripts in-platform | B (owner confirms possible, Sep 23) | none |
| 7 | Parse webhook body | B | JSON Parser (C) |
| 8 | Bulk reads, aggregation, de-dup across items | C | Get all items + loop (limits apply) |
| 9 | Create items/subitems with computed values in one call | C | Create item |
| 10 | Read/write via MCP server | B (stated), endpoint/auth not documented | MCP blocks |
| 11 | Build board/workspace objects native blocks lack | C (needs schema check) | none |

## Pattern: status guard (C sketch, not run)
1. Trigger: status column changes on board.
2. Code: input item id, new label, previous label. Query item, check rule. If violation, `change_column_value` back and `create_notification` to editor. Return `{"ok":"true","reverted":"true"}`.
3. Test on a test board only. The editor Run uses live data.

## Pattern: ensure team exists, add users (C sketch)
Check schema for `teams`, `create_team`, `add_users_to_team` with `get_graphql_schema` (Teams API requires appropriate account permissions). Return only counts and the team ID.

## Failure triage
| Symptom | Likely cause | Action |
|---|---|---|
| "Code block must return an object" | Output not a dict, or truncated over ~4 KB (Oct 13-14 incident, fixed) | Return small dict; rerun; check Run history |
| Code ran long, run marked failed "took too long to respond" | ECONNRESET misreported as timeout (B, incident analysis) | Re-run; store result on a board, return pointer |
| MISSING_REQUIRED_INPUT on Change column value bound to Code output | Open bug, 2 reports (D) | Write inside Code via API |
| Input name mismatch | Auto-generated name differs | Use exact `code_output_...` name |
| Condition never true | `"False"` vs `"false"` | Normalise with `.lower()` |
| Webhook returns 200 but nothing runs | Activation/UUID bug (D) | Re-publish fresh workflow; escalate with run ids |
