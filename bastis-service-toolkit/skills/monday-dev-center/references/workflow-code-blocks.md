# Workflow Builder Code blocks that call the monday API (field-tested)

Learned on a live client build (Oct 2026). Read this before proposing a Code block, and before debugging one.
Claude writes the code; Basti pastes it into the Code block in the client account and runs the tests.
Claude still never calls the client account.

## Contents
1. When a Code block is the right tool
2. What the Code block can do
3. Pattern: two workflows (do the work, then link)
4. Code template
5. Gotchas (each one cost a test round)
6. Test and debug routine

---

## 1. When a Code block is the right tool
Use one when a native block can't do the job. These limits come up most often:
- **"Find connected item" and "Connect boards" need a fixed board.** If the target board is dynamic (e.g. "the activation on whichever campaign board the request picked"), native blocks can't do it.
- **Connect-board fields only accept connect-type variables.** A connect field can't be filled from a text value, an item id, or a Code output.
- **Mirror columns can't be used as inputs.**
- The work needs logic across several items: create a subitem, then link back to it, with guards.

If a native block or a classic automation can do it, use that instead. A Code block is code that someone has to maintain.

## 2. What the Code block can do
- **Language:** Python. `requests` and `json`/`re` are available.
- **monday API without a token:** `requests.post("https://api.monday.com/v2", json={"query": q}, headers={"API-Version": "2025-10"})` is **authenticated automatically**, as the workflow's owner. Never put a token in the code.
  - Source: internal doc "Code block" on monday.monday.com (doc 18429902902) and #ask-ai-workflows (Daniel Abergel, 16 Sep 2026).
- **Inputs:** the chips in the Input field. Under "Rename inputs" they get the names the code reads with `input.get("<name>")`.
- **Outputs:** declared under Output (name + type). The code ends with `return {"<output>": value, ...}`.
- **Connect-column values arrive as** `{'linkedPulseIds': [{'linkedPulseId': '3104262507'}]}`. Pull ids out with `re.findall(r"\d{8,}", str(value))` rather than parsing the shape.
- **Output can't feed a connect field** in a later block. If a link has to be set, the code sets it itself via the API.

## 3. Pattern: two workflows (do the work, then link)
For "route a request to a team board and link it back to the parent record", split the work:

**Workflow 1 (routing):** trigger "item created" → get item data → switch on team → per branch:
1. Create item (team board)
2. Change column value: **`<Job ID text column>` = Create item › Item ID** (this branch's step)
3. Change status: Routed

**Workflow 2 (link-back):** trigger **"When column changes: `<Job ID text column>`"** → Code (one input: Item ID from Step 1) → Change column value: **`<Result text column>` = Code › result**.

Why this beats one Code block per branch:
- One copy of the code instead of N. A fix happens in one place.
- No copied step references (see §5).
- A link-back error can't stop routing.
- **Retro-linking for free:** typing a job id into the Job ID column links an old request.

Rules:
- **Confirmed:** "When column changes" fires on a value written by **another workflow**.
- The result goes into a **separate** column, never back into the trigger column. Otherwise the workflow triggers itself.
- **Look for clear-on-status rules** (e.g. "status → Routed ⇒ clear the connect column"). They race workflow 2 and wipe its input. Switch them off, or read a value that isn't cleared.
- Keep it as Workflow Builder, not classic automations. Branching and passing the created item's id on are both things classic recipes can't do.

## 4. Code template
Paste the whole thing into the Code block. One input: `item_id` = trigger › Item ID. One output: `result` (String).
Fill in the CONFIG part from a structure read. The code reads every other value itself, so no input mapping can be swapped (see §5).

```python
import json, re, requests

def gql(q):
    r = requests.post("https://api.monday.com/v2", json={"query": q}, headers={"API-Version": "2025-10"})
    d = r.json()
    if d.get("errors"):
        raise Exception(json.dumps(d["errors"])[:400])
    return d["data"]

# ---- CONFIG (from a structure read) ----
PARENT_CONNECT_COL = "<request: connect column to the parent, e.g. board_relation_xxx>"
PARENT_ID_TEXT_COL = "<request: text column with a prefilled parent id, fallback>"
JOB_ID_COL         = "<request: text column workflow 1 writes the job id into>"
TASK_COL = {                              # team board id -> its connect column back to the parent's subitem
    "<team board id>": "<board_relation_xxx>",
}
SUB_LINK_COL   = "<subitem: connect column to the team job>"
SUB_STATUS_COL = "<subitem: status column>"          # optional
# ----------------------------------------

req = re.sub(r"\D", "", str(input.get("item_id", "")))
cv, name, read_err = {}, "Request", ""
if req:
    try:
        it = gql(f'query {{ items(ids: [{req}]) {{ name column_values(ids: ["{PARENT_CONNECT_COL}", "{PARENT_ID_TEXT_COL}", "{JOB_ID_COL}"]) {{ id text ... on BoardRelationValue {{ linked_item_ids }} }} }} }}')["items"]
        if it:
            name = it[0]["name"].strip() or "Request"
            cv = {c["id"]: c for c in it[0]["column_values"]}
    except Exception as e:
        read_err = str(e)

found = list((cv.get(PARENT_CONNECT_COL) or {}).get("linked_item_ids") or []) or re.findall(r"\d{8,}", str((cv.get(PARENT_ID_TEXT_COL) or {}).get("text") or ""))
act = str(found[0]) if found else ""
jobs = re.findall(r"\d{8,}", str((cv.get(JOB_ID_COL) or {}).get("text") or ""))
job = jobs[0] if jobs else ""

if read_err:
    result = f"error: could not read request {req}: {read_err}"[:450]
elif not act or not job:
    result = f"skipped: no parent or no job id (request {req}, parent '{act}', job '{job}')"
else:
    try:
        boards = {i["id"]: str(i["board"]["id"]) for i in gql(f"query {{ items(ids: [{job}, {act}]) {{ id board {{ id }} }} }}")["items"]}
        board = boards.get(job, "")
        col = TASK_COL.get(board)
        if not col:
            raise Exception(f"job {job} is not on a team board (board {board})")
        if act == job or boards.get(act, "") in TASK_COL:          # guard: swapped ids
            raise Exception(f"parent {act} is on a team board - check the request's parent fields")
        linked = gql(f'query {{ items(ids: [{job}]) {{ column_values(ids: ["{col}"]) {{ ... on BoardRelationValue {{ linked_item_ids }} }} }} }}')["items"][0]["column_values"][0]["linked_item_ids"]
        if linked:                                                    # guard: already done
            raise Exception(f"already linked (two-way): job {job} <-> subitem {linked[0]}")
        subs = gql(f'query {{ items(ids: [{act}]) {{ subitems {{ id column_values(ids: ["{SUB_LINK_COL}"]) {{ ... on BoardRelationValue {{ linked_item_ids }} }} }} }} }}')["items"][0]["subitems"] or []
        sub = next((s["id"] for s in subs if job in (s["column_values"][0]["linked_item_ids"] if s["column_values"] else [])), None)
        if not sub:                                                   # reuse on retry, else create
            vals = json.dumps({SUB_LINK_COL: {"item_ids": [int(job)]}, SUB_STATUS_COL: {"label": "New"}})
            sub = gql(f"mutation {{ create_subitem(parent_item_id: {act}, item_name: {json.dumps(name)}, column_values: {json.dumps(vals)}) {{ id }} }}")["create_subitem"]["id"]
        try:
            back = json.dumps({col: {"item_ids": [int(sub)]}})
            gql(f"mutation {{ change_multiple_column_values(board_id: {board}, item_id: {job}, column_values: {json.dumps(back)}) {{ id }} }}")
            result = f"two-way: job {job} <-> subitem {sub} (parent {act})"
        except Exception as e:
            msg = "subitem board missing from the team's connect column" if "not in the connected boards" in str(e) else str(e)
            result = f"one-way: subitem {sub} -> job {job} (parent {act}); link back failed: {msg}"
    except Exception as e:
        result = (str(e) if str(e).startswith("already linked") else f"error: {e}")[:450]

return {"result": result}
```

Before handing it over, check the syntax locally. The block's top-level `return` needs a wrapper:
`python3 -c "import ast,textwrap; ast.parse('def _wb(input):\n'+textwrap.indent(open('code.py').read(),'    '))"`

## 5. Gotchas (each one cost a test round)
- **Input renaming swaps fields.** Under "Rename inputs" the names drifted onto the wrong chips: `job_id` received the item name, and `activation_text` received the job id. The most likely trigger is an input whose source column id matches an **output** name (column `activation_id` vs output `activation_id`). **Fix: pass only the item id and let the code read the rest via the API** (§4).
- **Copied branches keep the original's step references.** After duplicating steps into other branches, `job_id` still pointed at Step 10 of another branch, so it was empty in this run. In every branch, the step number on each chip must belong to that branch's own cards.
- **A pasted block can keep old code.** Check the line numbers in the editor against the version you expect before you test.
- **"There are items that are not in the connected boards"** means the target connect column doesn't list the board of the item you're linking. Either the board is missing from the column settings, or the ids are swapped (e.g. the subitem was created under the job instead of the parent).
- **Two-way connections update themselves for template-created boards.** A new board from a template whose subitem connect column points at the team boards is added to the team boards' reverse column automatically. Boards created another way can be missing on some team boards: compare the `boardIds` lists across all team boards with one read.
- **Classic automations can't do this split.** They can't branch, and they can't pass the created item's id on.

## 6. Test and debug routine
1. **One test per branch.** Duplicating an item re-runs "item created" workflows. Re-typing the trigger column's value re-runs workflow 2 without a new request.
2. **Read the result column, then verify both sides with a read query.** Check the parent's subitems (exactly one per request) and the job's connect column.
3. **On `skipped`, echo the inputs.** Temporarily put `str(dict(input))[:350]` into the skipped message. One run then shows which input arrives empty or under the wrong name.
4. **Typical real-world causes, in the order we hit them:** old code still pasted → copied step references → input fields swapped → a value overwritten by hand while re-triggering → board missing from the connect column.
5. **Test data you create:** tell Basti exactly which items or subitems to delete. Claude doesn't delete them via the API without an explicit OK.
