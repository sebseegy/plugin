#!/usr/bin/env python3
"""
monday build replicator
=======================
Source account (monday Spaces / demo sandbox)  ->  portable blueprint  ->
staged, copy-paste-ready GraphQL for the TARGET (client) account's API playground.

Design invariants (do not weaken):
  * No API tokens ever pass through this tool. Source data arrives as pasted JSON;
    target mutations are pasted by the consultant into the client's playground.
  * Target responses request IDs/structure only (no item data).
  * Deletions are only ever generated for objects this plan itself created
    (default columns/groups on boards we created, placeholder items we created).
  * Column IDs on the target are assigned deterministically BEFORE execution, so
    formulas / mirrors / views can be remapped without extra round-trips.

Subcommands
  extract-query   Print the source extraction query (paste into SOURCE playground).
  blueprint       Build state.json + manual build sheet from pasted source JSON.
  next            Show which stage is next and why.
  stage           Generate playground-ready GraphQL for a stage (chunked).
  ingest          Record the pasted target response for a stage.
  verify-query    Print the target verification query.
  diff            Compare a pasted verification response against the blueprint.
  status          Print a compact progress summary.
"""
import argparse
import copy
import datetime as _dt
import json
import os
import re
import sys

COL_ID_RE = re.compile(r"^[a-z_]{1,20}$")
ALIAS_BAD = re.compile(r"[^_0-9A-Za-z]")
ENUM_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

SKIP_TYPES = {"name"}                      # exists on every board
SUBITEM_TYPES = {"subtasks"}               # spawned via placeholder subitem
MANUAL_TYPES = {                           # not reproducible deterministically without AI/apps
    "button", "integration", "unsupported", "ai", "ai_column", "custom",
}
VERIFY_TYPES = {                           # attempted, but settings shape unverified
    "progress", "dependency", "time_tracking", "auto_number", "doc", "direct_doc",
}
BOARD_ID_KEYS = {"boardIds", "boardId", "board_ids", "board_id"}
PLACEHOLDER = "__replicator_placeholder__"
PLACEHOLDER_SUB = "__replicator_placeholder_sub__"
STAGE_ORDER = ["workspace", "folders", "boards", "structure", "subitems", "finish", "verify"]


# ----------------------------------------------------------------------------- utils
def now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json_loose(path):
    """Load JSON pasted from a playground. Accepts {"data":...} or bare data."""
    with open(path, encoding="utf-8") as f:
        txt = f.read().strip()
    # tolerate code fences
    txt = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", txt)
    obj = json.loads(txt)
    return obj


def unwrap(obj):
    if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], dict):
        return obj["data"], obj.get("errors") or []
    return obj, (obj.get("errors") if isinstance(obj, dict) else []) or []


def gstr(s):
    """GraphQL string literal."""
    return json.dumps("" if s is None else str(s), ensure_ascii=False)


def gjson(obj):
    """JSON scalar passed as an escaped GraphQL string (works for every JSON arg)."""
    return gstr(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def genum(v, what):
    if v is None or not ENUM_RE.match(str(v)):
        raise ValueError(f"Invalid enum value for {what}: {v!r}")
    return str(v)


def alias(*parts):
    a = "_".join(ALIAS_BAD.sub("_", str(p)) for p in parts)
    return a if re.match(r"^[A-Za-z_]", a) else "x_" + a


def as_settings(raw):
    if raw is None or raw == "":
        return {}
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return raw


def slug_col_id(title, taken):
    base = re.sub(r"[^a-z]+", "_", (title or "col").lower()).strip("_") or "col"
    base = base[:16]
    cand = base
    n = 0
    letters = "abcdefghijklmnopqrstuvwxyz"
    while cand in taken or not COL_ID_RE.match(cand):
        suffix = ""
        k = n
        while True:
            suffix = letters[k % 26] + suffix
            k = k // 26 - 1
            if k < 0:
                break
        cand = (base[: 19 - len(suffix)] + "_" + suffix)[:20]
        n += 1
    return cand


def save_state(state, path):
    state["meta"]["updated_at"] = now()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_state(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------------------------------- extraction
def extraction_query(ws_id, page=1, limit=25, board_ids=None):
    if board_ids:
        ids = ", ".join(str(int(b)) for b in board_ids)
        return f"""query {{
  boards(ids: [{ids}]) {{
    id name description board_kind type hierarchy_type item_terminology board_folder_id
    groups {{ id title color position }}
    columns {{ id title type description settings }}
    views {{ id name type settings filter sort tags }}
  }}
}}"""
    head = ""
    if page == 1:
        head = f"""  me {{ account {{ id slug name }} }}
  workspaces(ids: [{int(ws_id)}]) {{ id name kind description }}
  folders(workspace_ids: [{int(ws_id)}], limit: 100) {{ id name color parent {{ id }} }}
"""
    return f"""query {{
{head}  boards(workspace_ids: [{int(ws_id)}], limit: {limit}, page: {page}, state: active, hierarchy_types: [classic, multi_level]) {{
    id name description board_kind type hierarchy_type item_terminology board_folder_id
    groups {{ id title color position }}
    columns {{ id title type description settings }}
    views {{ id name type settings filter sort tags }}
  }}
}}"""


# ----------------------------------------------------------------------------- blueprint
def build_blueprint(raw_paths, name):
    account, workspace, folders, boards = None, None, [], {}
    for p in raw_paths:
        data, errors = unwrap(load_json_loose(p))
        if errors:
            print(f"WARNING: {p} contains API errors: {json.dumps(errors)[:400]}", file=sys.stderr)
        if data.get("me"):
            account = (data["me"] or {}).get("account")
        if data.get("workspaces"):
            workspace = data["workspaces"][0]
        for f in data.get("folders") or []:
            folders.append(f)
        for b in data.get("boards") or []:
            boards[str(b["id"])] = b

    bp = {"workspace": None, "folders": [], "boards": [], "subitem_boards": {}}
    if workspace:
        bp["workspace"] = {
            "src_id": str(workspace["id"]), "name": workspace.get("name"),
            "kind": workspace.get("kind") or "open", "description": workspace.get("description"),
        }
    seen_f = set()
    for f in folders:
        if str(f["id"]) in seen_f:
            continue
        seen_f.add(str(f["id"]))
        bp["folders"].append({
            "src_id": str(f["id"]), "name": f.get("name"), "color": f.get("color"),
            "parent_src_id": str(f["parent"]["id"]) if f.get("parent") else None,
        })

    def norm_board(b):
        return {
            "src_id": str(b["id"]), "name": b.get("name"), "description": b.get("description"),
            "board_kind": b.get("board_kind") or "public", "type": b.get("type") or "board",
            "hierarchy_type": b.get("hierarchy_type") or "classic",
            "item_terminology": b.get("item_terminology"),
            "folder_src_id": str(b["board_folder_id"]) if b.get("board_folder_id") else None,
            "groups": [
                {"src_id": str(g["id"]), "title": g.get("title"), "color": g.get("color"),
                 "position": g.get("position")}
                for g in (b.get("groups") or [])
            ],
            "columns": [
                {"src_id": str(c["id"]), "title": c.get("title"), "type": c.get("type"),
                 "description": c.get("description"), "settings": as_settings(c.get("settings"))}
                for c in (b.get("columns") or [])
            ],
            "views": [
                {"src_id": str(v["id"]), "name": v.get("name"), "type": v.get("type"),
                 "settings": as_settings(v.get("settings")), "filter": as_settings(v.get("filter")),
                 "sort": as_settings(v.get("sort")), "tags": v.get("tags") or []}
                for v in (b.get("views") or [])
            ],
            "subitem_board_src_id": None,
        }

    for b in boards.values():
        nb = norm_board(b)
        if nb["type"] == "sub_items_board":
            bp["subitem_boards"][nb["src_id"]] = nb
        else:
            bp["boards"].append(nb)

    missing_sub = []
    for b in bp["boards"]:
        for c in b["columns"]:
            if c["type"] in SUBITEM_TYPES:
                ids = c["settings"].get("boardIds") or []
                if ids:
                    sid = str(ids[0])
                    b["subitem_board_src_id"] = sid
                    if sid not in bp["subitem_boards"]:
                        missing_sub.append(sid)

    state = {
        "meta": {
            "name": name, "created_at": now(), "updated_at": now(), "tool_version": 1,
            "source_account": account, "api_version_hint": "Current (2026-07) or later",
        },
        "blueprint": bp,
        "target": {
            "workspace_id": None, "folders": {}, "boards": {}, "groups": {},
            "col_ids": {}, "default_columns": {}, "default_groups": {},
            "placeholders": {}, "subitem_boards": {}, "subitem_default_columns": {},
            "subtasks_col": {},
        },
        "ops": {},
        "missing_subitem_boards": sorted(set(missing_sub)),
        "log": [],
    }
    state["manual"] = manual_items(state)
    return state


# ----------------------------------------------------------------------------- helpers over state
def bp_all_boards(state):
    bp = state["blueprint"]
    out = list(bp["boards"])
    out += list(bp["subitem_boards"].values())
    return out


def board_by_src(state, src):
    for b in bp_all_boards(state):
        if b["src_id"] == str(src):
            return b
    return None


def is_subitem_board(state, src):
    return str(src) in state["blueprint"]["subitem_boards"]


def parent_of_subitem(state, sub_src):
    for b in state["blueprint"]["boards"]:
        if b.get("subitem_board_src_id") == str(sub_src):
            return b
    return None


def replicable_boards(state):
    """Top-level boards we create via create_board."""
    out = []
    for b in state["blueprint"]["boards"]:
        if b["type"] == "document":
            continue
        if b["hierarchy_type"] == "multi_level":
            continue
        out.append(b)
    return out


def target_board_id(state, src):
    src = str(src)
    t = state["target"]
    if src in t["boards"]:
        return t["boards"][src]
    if src in t["subitem_boards"]:
        return t["subitem_boards"][src]
    return None


def column_class(state, board, col):
    """Return (bucket, reason). bucket in auto|verify|manual|skip|subitems."""
    t = col["type"]
    if t in SKIP_TYPES:
        return "skip", "exists on every board"
    if t in SUBITEM_TYPES:
        return "subitems", "spawned via placeholder subitem"
    if t in MANUAL_TYPES or (t or "").startswith("ai"):
        return "manual", f"type '{t}' not reproducible via plain API"
    # relations to boards outside the blueprint
    for bid in board_refs(col["settings"]):
        if not board_by_src(state, bid):
            return "manual", f"references board {bid} outside the replicated set"
    if t == "mirror":
        s = col["settings"]
        for entry in s.get("displayed_linked_columns") or []:
            if not board_by_src(state, entry.get("board_id")):
                return "manual", f"mirror source board {entry.get('board_id')} outside set"
    if t in VERIFY_TYPES:
        return "verify", f"type '{t}' settings shape not verified - check after run"
    return "auto", ""


def board_refs(settings):
    refs = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in BOARD_ID_KEYS:
                    if isinstance(v, list):
                        refs.extend(str(x) for x in v)
                    elif v is not None:
                        refs.append(str(v))
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(settings or {})
    return refs


def col_deps(board, col):
    """Return list of (board_src, col_src) this column depends on."""
    deps = []
    s = col["settings"] or {}
    if col["type"] == "formula":
        for ref in re.findall(r"\{([a-z0-9_]+)\}", s.get("formula") or ""):
            deps.append((board["src_id"], ref))
    elif col["type"] == "mirror":
        for k in (s.get("relation_column") or {}):
            deps.append((board["src_id"], k))
        for entry in s.get("displayed_linked_columns") or []:
            for cid in entry.get("column_ids") or []:
                deps.append((str(entry.get("board_id")), cid))
    return deps


def topo_columns(state):
    """Global dependency-ordered list of (board, col, stage) for creatable columns."""
    nodes, order_key = {}, {}
    idx = 0
    for b in bp_all_boards(state):
        if not is_subitem_board(state, b["src_id"]) and b not in replicable_boards(state):
            continue
        for c in b["columns"]:
            bucket, _ = column_class(state, b, c)
            if bucket in ("auto", "verify"):
                key = (b["src_id"], c["src_id"])
                nodes[key] = (b, c)
                order_key[key] = idx
                idx += 1
    indeg = {k: 0 for k in nodes}
    edges = {k: [] for k in nodes}
    for k, (b, c) in nodes.items():
        for d in col_deps(b, c):
            if d in nodes and d != k:
                edges[d].append(k)
                indeg[k] += 1
    ready = sorted([k for k in nodes if indeg[k] == 0], key=lambda k: order_key[k])
    out = []
    while ready:
        k = ready.pop(0)
        out.append(k)
        for n in edges[k]:
            indeg[n] -= 1
            if indeg[n] == 0:
                ready.append(n)
                ready.sort(key=lambda x: order_key[x])
    cyclic = [k for k in nodes if k not in out]
    stage_of = {}
    for k in out:
        b, c = nodes[k]
        st = "finish" if is_subitem_board(state, b["src_id"]) else "structure"
        for d in col_deps(b, c):
            if d in stage_of and stage_of[d] == "finish":
                st = "finish"
        stage_of[k] = st
    return [(nodes[k][0], nodes[k][1], stage_of[k]) for k in out], cyclic


# ----------------------------------------------------------------------------- manual sheet
def manual_items(state):
    items = []
    bp = state["blueprint"]
    items.append(("ALL", "Automations (board recipes) and Workflow Builder workflows",
                  "Not creatable via the public API for customer accounts (dev-only, allowlisted). "
                  "Rebuild in UI from the source Automations Center; use the checklist per board."))
    items.append(("ALL", "Integrations / integration recipes", "UI only."))
    items.append(("ALL", "Board owners, subscribers, team access, board permissions",
                  "Source users don't exist in the client account. Assign in UI or via "
                  "add_users_to_board / set_board_permission once client user IDs are known."))
    items.append(("ALL", "Dashboards and widgets", "Out of scope for v1 (widget settings embed board IDs). Rebuild in UI."))
    items.append(("ALL", "Workspace docs", "Out of scope for v1. Export as markdown from source and recreate."))
    for b in bp["boards"]:
        if b["type"] == "document":
            items.append((b["name"], "Document-type board", "Recreate manually."))
            continue
        if b["hierarchy_type"] == "multi_level":
            items.append((b["name"], "Multi-level board", "create_board(use_mls_template) is 2026-10+ only; not automated in v1."))
            continue
        if b.get("item_terminology") and str(b["item_terminology"]).lower() not in ("item", "items"):
            items.append((b["name"], f"Item terminology '{b['item_terminology']}'", "Set in board settings."))
        for c in b["columns"] + (bp["subitem_boards"].get(b.get("subitem_board_src_id") or "", {}) or {}).get("columns", []):
            bucket, reason = column_class(state, b, c)
            if bucket == "manual":
                items.append((b["name"], f"Column '{c['title']}' ({c['type']})", reason))
            if c["type"] == "status":
                for lab in (c["settings"] or {}).get("labels") or []:
                    if lab.get("hex"):
                        items.append((b["name"], f"Status '{c['title']}' label '{lab.get('label')}' uses custom hex {lab['hex']}",
                                      "Enum color applied; reapply hex in UI if it matters."))
                    if lab.get("is_deactivated"):
                        items.append((b["name"], f"Status '{c['title']}' deactivated label '{lab.get('label')}'",
                                      "Dropped on create; recreate+deactivate in UI if needed."))
        for v in b["views"]:
            if not is_table_view(v):
                items.append((b["name"], f"View '{v['name']}' (type {v['type']})",
                              "Public API can only create TABLE/APP/FORM/DASHBOARD views; rebuild in UI."))
            elif v.get("filter"):
                items.append((b["name"], f"Table view '{v['name']}' filter",
                              "Filter translated best-effort; confirm it in UI."))
    for sid in state.get("missing_subitem_boards", []):
        items.append(("?", f"Subitem board {sid} not extracted",
                      "Run: replicator.py extract-query --board-ids " + sid + " and re-run blueprint."))
    return items


def is_table_view(v):
    t = str(v.get("type") or "").lower()
    return t in ("table", "tableview", "table_view", "boardview_table") or t.startswith("table")


def write_manual_sheet(state, path):
    lines = [f"# Manual build sheet — {state['meta']['name']}", "",
             f"Generated {now()}. Items the API cannot (or should not) replicate. Tick off in the client account.", "",
             "| Board | Item | Why / how |", "|---|---|---|"]
    for b, item, why in state["manual"]:
        lines.append(f"| {b} | {item} | {why} |")
    lines += ["", "## Automations checklist (fill from source Automations Center)", ""]
    for b in replicable_boards(state):
        lines.append(f"- [ ] **{b['name']}** — list each recipe: trigger → condition → action")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ----------------------------------------------------------------------------- column id assignment + settings remap
def assign_ids_for_board(state, board_src, defaults):
    t = state["target"]
    cmap = t["col_ids"].setdefault(board_src, {})
    taken = {d["id"] for d in defaults} | set(cmap.values())
    b = board_by_src(state, board_src)
    # name column always maps to name
    cmap.setdefault("name", "name")
    for c in b["columns"]:
        if c["src_id"] in cmap:
            continue
        bucket, _ = column_class(state, b, c)
        if bucket not in ("auto", "verify"):
            continue
        src = c["src_id"]
        tgt = src if (COL_ID_RE.match(src) and src not in taken) else slug_col_id(c["title"], taken)
        cmap[src] = tgt
        taken.add(tgt)
    return cmap


def remap_board(state, bid):
    tb = target_board_id(state, bid)
    return int(tb) if tb and str(tb).isdigit() else tb


def remap_settings(state, board, col):
    if col.get("settings_override") is not None:
        return copy.deepcopy(col["settings_override"])   # consultant-supplied, already target-shaped
    s = copy.deepcopy(col["settings"] or {})
    cmap = state["target"]["col_ids"].get(board["src_id"], {})
    t = col["type"]
    if t == "status":
        labels = []
        for lab in s.get("labels") or []:
            if lab.get("is_deactivated"):
                continue
            nl = {k: lab[k] for k in ("label", "color", "index", "is_done", "description") if k in lab}
            labels.append(nl)
        return {"labels": labels}
    if t == "dropdown":
        labels = [{k: l[k] for k in ("id", "name") if k in l} for l in (s.get("labels") or [])
                  if not l.get("is_deactivated")]
        out = {k: v for k, v in s.items() if k not in ("labels",)}
        out["labels"] = labels
        return out
    if t == "formula":
        f = s.get("formula") or ""
        s["formula"] = re.sub(r"\{([a-z0-9_]+)\}", lambda m: "{" + cmap.get(m.group(1), m.group(1)) + "}", f)
        return s
    if t == "mirror":
        rel = {}
        for k, v in (s.get("relation_column") or {}).items():
            rel[cmap.get(k, k)] = v
        s["relation_column"] = rel
        dl = []
        for e in s.get("displayed_linked_columns") or []:
            ob = str(e.get("board_id"))
            omap = state["target"]["col_ids"].get(ob, {})
            dl.append({"board_id": str(target_board_id(state, ob)),
                       "column_ids": [omap.get(x, x) for x in e.get("column_ids") or []]})
        s["displayed_linked_columns"] = dl
        return s

    # generic: remap any board-id keys
    def walk(o):
        if isinstance(o, dict):
            out = {}
            for k, v in o.items():
                if k in BOARD_ID_KEYS:
                    if isinstance(v, list):
                        out[k] = [remap_board(state, x) for x in v]
                    else:
                        out[k] = remap_board(state, v)
                else:
                    out[k] = walk(v)
            return out
        if isinstance(o, list):
            return [walk(x) for x in o]
        return o

    return walk(s)


# ----------------------------------------------------------------------------- op registry
def put_op(state, op_id, stage, kind, gql, meta):
    ops = state["ops"]
    if op_id in ops and ops[op_id]["status"] == "done":
        return None
    ops[op_id] = {"stage": stage, "kind": kind, "gql": gql, "meta": meta,
                  "status": ops.get(op_id, {}).get("status", "pending"),
                  "error": ops.get(op_id, {}).get("error")}
    if ops[op_id]["status"] == "failed":
        ops[op_id]["status"] = "pending"   # regenerate failed ops
    return op_id


def stage_done(state, stage):
    ops = [o for o in state["ops"].values() if o["stage"] == stage]
    return bool(ops) and all(o["status"] == "done" for o in ops)


# ----------------------------------------------------------------------------- stage generators
def gen_workspace(state):
    ws = state["blueprint"]["workspace"]
    if state["target"]["workspace_id"]:
        return []
    if not ws:
        raise SystemExit("Source is the Main workspace. Pass --target-workspace-id with an existing client workspace.")
    kind = ws.get("kind") if ws.get("kind") in ("open", "closed") else "open"
    g = (f"create_workspace(name: {gstr(ws['name'])}, kind: {kind}"
         + (f", description: {gstr(ws['description'])}" if ws.get("description") else "")
         + ") { id }")
    return [put_op(state, "ws", "workspace", "create_workspace", g, {})]


def gen_folders(state):
    t = state["target"]
    wsid = t["workspace_id"]
    out = []
    for f in state["blueprint"]["folders"]:
        if f["src_id"] in t["folders"]:
            continue
        parent = f.get("parent_src_id")
        if parent and parent not in t["folders"]:
            continue  # next round
        args = [f"name: {gstr(f['name'])}", f"workspace_id: {wsid}"]
        if parent:
            args.append(f"parent_folder_id: {t['folders'][parent]}")
        if f.get("color") and ENUM_RE.match(str(f["color"])) and str(f["color"]).upper() != "NULL":
            args.append(f"color: {f['color']}")
        op = put_op(state, alias("f", f["src_id"]), "folders", "create_folder",
                    f"create_folder({', '.join(args)}) {{ id }}", {"src": f["src_id"]})
        if op:
            out.append(op)
    return out


def gen_boards(state):
    t = state["target"]
    out = []
    for b in replicable_boards(state):
        if b["src_id"] in t["boards"]:
            continue
        kind = b["board_kind"] if b["board_kind"] in ("public", "private", "share") else "public"
        args = [f"board_name: {gstr(b['name'])}", f"board_kind: {kind}",
                f"workspace_id: {t['workspace_id']}", "empty: true"]
        if b.get("folder_src_id"):
            fid = t["folders"].get(b["folder_src_id"])
            if fid:
                args.append(f"folder_id: {fid}")
        if b.get("description"):
            args.append(f"description: {gstr(b['description'])}")
        g = f"create_board({', '.join(args)}) {{ id columns {{ id type title }} groups {{ id title }} }}"
        op = put_op(state, alias("b", b["src_id"]), "boards", "create_board", g, {"src": b["src_id"]})
        if op:
            out.append(op)
    return out


def gen_structure(state):
    t = state["target"]
    out = []
    # 1. assign target column ids for all top-level boards (deterministic, persisted)
    for b in replicable_boards(state):
        assign_ids_for_board(state, b["src_id"], t["default_columns"].get(b["src_id"], []))
    # 2. groups (reverse order: create_group inserts at top)
    for b in replicable_boards(state):
        tb = t["boards"][b["src_id"]]
        groups = sorted(b["groups"], key=lambda g: float(g.get("position") or 0))
        existing = t["groups"].get(b["src_id"], {})
        for i, g in enumerate(reversed(groups)):
            args = [f"board_id: {tb}", f"group_name: {gstr(g['title'])}"]
            if existing and g["src_id"] not in existing:
                # delta add: anchor to the previous source group (top-insert trick no longer valid)
                pos = groups.index(g)
                prev = next((existing[x["src_id"]] for x in reversed(groups[:pos]) if x["src_id"] in existing), None)
                nxt = next((existing[x["src_id"]] for x in groups[pos + 1:] if x["src_id"] in existing), None)
                if prev:
                    args += [f"relative_to: {gstr(prev)}", "position_relative_method: after_at"]
                elif nxt:
                    args += [f"relative_to: {gstr(nxt)}", "position_relative_method: before_at"]
            if g.get("color") and str(g["color"]).startswith("#"):
                args.append(f"group_color: {gstr(g['color'])}")
            op = put_op(state, alias("g", b["src_id"], g["src_id"]), "structure", "create_group",
                        f"create_group({', '.join(args)}) {{ id }}", {"board": b["src_id"], "src": g["src_id"]})
            if op:
                out.append(op)
    # 3. columns in dependency order
    ordered, cyclic = topo_columns(state)
    for b, c, st in ordered:
        if st != "structure":
            continue
        op = col_op(state, b, c, "structure")
        if op:
            out.append(op)
    for k in cyclic:
        add_manual(state, k[0], f"Column {k[1]}", "Circular formula/mirror dependency — build manually.")
    # 3b. rename the name (first) column if the source title differs from the target default
    for b in replicable_boards(state):
        src_name = next((c for c in b["columns"] if c["type"] == "name"), None)
        tgt_name = next((d for d in t["default_columns"].get(b["src_id"], []) if d.get("type") == "name"), None)
        if src_name and src_name["title"] != (tgt_name or {}).get("title", "Name"):
            op = put_op(state, alias("rnm", b["src_id"]), "structure", "rename_name_column",
                        f"change_column_title(board_id: {t['boards'][b['src_id']]}, column_id: \"name\", "
                        f"title: {gstr(src_name['title'])}) {{ id }}", {"board": b["src_id"]})
            if op:
                out.append(op)
    # 3c. delta renames (non-destructive)
    for r in state.get("renames", []):
        tb = target_board_id(state, r["board"])
        if not tb:
            continue
        if r["kind"] == "column":
            tid = t["col_ids"].get(r["board"], {}).get(r["src"])
            if not tid:
                continue
            g = f"change_column_title(board_id: {tb}, column_id: {gstr(tid)}, title: {gstr(r['title'])}) {{ id }}"
        else:
            gid = t["groups"].get(r["board"], {}).get(r["src"])
            if not gid:
                continue
            g = (f"update_group(board_id: {tb}, group_id: {gstr(gid)}, group_attribute: title, "
                 f"new_value: {gstr(r['title'])}) {{ id }}")
        op = put_op(state, alias("rc", r["board"], r["src"], r["n"]), "structure", "rename", g, {"board": r["board"]})
        if op:
            out.append(op)
    # 4. placeholder items for boards with subitems
    for b in replicable_boards(state):
        if b.get("subitem_board_src_id") and b["subitem_board_src_id"] in state["blueprint"]["subitem_boards"]:
            tb = t["boards"][b["src_id"]]
            op = put_op(state, alias("p", b["src_id"]), "structure", "create_placeholder",
                        f"create_item(board_id: {tb}, item_name: {gstr(PLACEHOLDER)}) {{ id }}",
                        {"board": b["src_id"]})
            if op:
                out.append(op)
    # 5. delete default columns created by create_board (never 'name')
    for b in replicable_boards(state):
        tb = t["boards"][b["src_id"]]
        for d in t["default_columns"].get(b["src_id"], []):
            if d["id"] == "name" or d.get("type") == "name":
                continue
            op = put_op(state, alias("dc", b["src_id"], d["id"]), "structure", "delete_default_column",
                        f"delete_column(board_id: {tb}, column_id: {gstr(d['id'])}) {{ id }}",
                        {"board": b["src_id"], "col": d["id"]})
            if op:
                out.append(op)
    return out


def add_manual(state, board, item, why):
    row = [str(board), item, why]
    if row not in [list(r) for r in state["manual"]]:
        state["manual"].append(row)


def col_op(state, b, c, stage):
    for db, dc in col_deps(b, c):
        if dc != "name" and dc not in state["target"]["col_ids"].get(db, {}):
            add_manual(state, b["name"], f"Column '{c['title']}' ({c['type']})",
                       f"depends on column '{dc}' that is not replicated — fix reference in UI")
    tb = target_board_id(state, b["src_id"])
    tid = state["target"]["col_ids"][b["src_id"]][c["src_id"]]
    settings = remap_settings(state, b, c)
    args = [f"board_id: {tb}", f"id: {gstr(tid)}", f"title: {gstr(c['title'])}",
            f"column_type: {genum(c['type'], 'column_type')}"]
    if c.get("description"):
        args.append(f"description: {gstr(c['description'])}")
    if settings:
        args.append(f"defaults: {gjson({'settings': settings})}")
    return put_op(state, alias("c", b["src_id"], c["src_id"]), stage, "create_column",
                  f"create_column({', '.join(args)}) {{ id }}",
                  {"board": b["src_id"], "src": c["src_id"], "target_id": tid})


def gen_subitems(state):
    t = state["target"]
    out = []
    for b in replicable_boards(state):
        sid = b.get("subitem_board_src_id")
        if not sid or sid not in state["blueprint"]["subitem_boards"] or sid in t["subitem_boards"]:
            continue
        pid = t["placeholders"].get(b["src_id"])
        if not pid:
            continue
        g = (f"create_subitem(parent_item_id: {pid}, item_name: {gstr(PLACEHOLDER_SUB)}) "
             f"{{ id board {{ id columns {{ id type title }} }} "
             f"parent_item {{ board {{ columns(types: [subtasks]) {{ id title }} }} }} }}")
        op = put_op(state, alias("s", b["src_id"]), "subitems", "create_subitem", g,
                    {"board": b["src_id"], "sub": sid})
        if op:
            out.append(op)
    return out


def gen_finish(state):
    t = state["target"]
    out = []
    # subitem board ids + columns
    for sid in t["subitem_boards"]:
        assign_ids_for_board(state, sid, t["subitem_default_columns"].get(sid, []))
    ordered, _ = topo_columns(state)
    for b, c, st in ordered:
        if st != "finish":
            continue
        if not target_board_id(state, b["src_id"]):
            continue
        op = col_op(state, b, c, "finish")
        if op:
            out.append(op)
    # delete subitem default columns
    for sid, defaults in t["subitem_default_columns"].items():
        tb = t["subitem_boards"][sid]
        for d in defaults:
            if d["id"] == "name" or d.get("type") == "name":
                continue
            op = put_op(state, alias("dsc", sid, d["id"]), "finish", "delete_default_column",
                        f"delete_column(board_id: {tb}, column_id: {gstr(d['id'])}) {{ id }}",
                        {"board": sid, "col": d["id"]})
            if op:
                out.append(op)
    # rename subitems column on parent
    for b in replicable_boards(state):
        sc = t["subtasks_col"].get(b["src_id"])
        src_col = next((c for c in b["columns"] if c["type"] in SUBITEM_TYPES), None)
        if sc and src_col and sc.get("title") != src_col["title"]:
            op = put_op(state, alias("rn", b["src_id"]), "finish", "rename_subtasks",
                        f"change_column_title(board_id: {t['boards'][b['src_id']]}, column_id: {gstr(sc['id'])}, "
                        f"title: {gstr(src_col['title'])}) {{ id }}", {"board": b["src_id"]})
            if op:
                out.append(op)
    # table views
    for b in replicable_boards(state):
        tb = t["boards"][b["src_id"]]
        cmap = t["col_ids"].get(b["src_id"], {})
        gmap = t["groups"].get(b["src_id"], {})
        for v in b["views"]:
            if not is_table_view(v):
                continue
            args = [f"board_id: {tb}", f"name: {gstr(v['name'])}"]
            srt = view_sort(v.get("sort"), cmap)
            if srt:
                args.append(f"sort: {srt}")
            flt = view_filter(v.get("filter"), cmap, gmap)
            if flt:
                args.append(f"filter: {flt}")
            op = put_op(state, alias("v", b["src_id"], v["src_id"]), "finish", "create_view_table",
                        f"create_view_table({', '.join(args)}) {{ id }}", {"board": b["src_id"], "src": v["src_id"]})
            if op:
                out.append(op)
    # delete placeholder items (after subitem board is set up)
    for b in replicable_boards(state):
        pid = t["placeholders"].get(b["src_id"])
        if pid:
            op = put_op(state, alias("dp", b["src_id"]), "finish", "delete_placeholder",
                        f"delete_item(item_id: {pid}) {{ id }}", {"board": b["src_id"]})
            if op:
                out.append(op)
    # delete default groups (only if our groups exist on that board)
    for b in replicable_boards(state):
        if not t["groups"].get(b["src_id"]):
            continue
        tb = t["boards"][b["src_id"]]
        for d in t["default_groups"].get(b["src_id"], []):
            if d["id"] in t["groups"][b["src_id"]].values():
                continue
            op = put_op(state, alias("dg", b["src_id"], d["id"]), "finish", "delete_default_group",
                        f"delete_group(board_id: {tb}, group_id: {gstr(d['id'])}) {{ id }}",
                        {"board": b["src_id"], "group": d["id"]})
            if op:
                out.append(op)
    return out


def view_sort(sort, cmap):
    if not isinstance(sort, list) or not sort:
        return None
    parts = []
    for s in sort:
        cid = s.get("column_id")
        d = str(s.get("direction") or "asc").lower()
        if not cid or d not in ("asc", "desc"):
            return None
        parts.append(f"{{ column_id: {gstr(cmap.get(cid, cid))}, direction: {d} }}")
    return "[" + ", ".join(parts) + "]"


def view_filter(flt, cmap, gmap):
    """Best-effort ItemsQueryGroup literal. Returns None if shape is unfamiliar."""
    if not isinstance(flt, dict) or not flt.get("rules"):
        return None
    rules = []
    for r in flt["rules"]:
        cid, op = r.get("column_id"), r.get("operator")
        if not cid or not op or not ENUM_RE.match(str(op)):
            return None
        cv = r.get("compare_value")
        if cid == "group":
            cv = [gmap.get(str(x), x) for x in (cv or [])]
        rules.append(f"{{ column_id: {gstr(cmap.get(cid, cid))}, operator: {op}, "
                     f"compare_value: {json.dumps(cv, ensure_ascii=False)} }}")
    oper = str(flt.get("operator") or "and").lower()
    if oper not in ("and", "or"):
        return None
    return f"{{ rules: [{', '.join(rules)}], operator: {oper} }}"


GENERATORS = {
    "workspace": gen_workspace, "folders": gen_folders, "boards": gen_boards,
    "structure": gen_structure, "subitems": gen_subitems, "finish": gen_finish,
}


# ----------------------------------------------------------------------------- next-stage logic
def next_stage(state):
    t = state["target"]
    if not t["workspace_id"]:
        return "workspace", "target workspace not created/set"
    if any(f["src_id"] not in t["folders"] for f in state["blueprint"]["folders"]):
        return "folders", "folders pending (repeat until all nested levels exist)"
    if any(b["src_id"] not in t["boards"] for b in replicable_boards(state)):
        return "boards", "boards pending"
    gen = state.setdefault("generated", {})
    st_ops = [o for o in state["ops"].values() if o["stage"] == "structure"]
    if not gen.get("structure") or any(o["status"] != "done" for o in st_ops):
        return "structure", "groups/columns/placeholders pending"
    need_sub = [b for b in replicable_boards(state)
                if b.get("subitem_board_src_id") in state["blueprint"]["subitem_boards"]
                and b["subitem_board_src_id"] not in t["subitem_boards"]]
    if need_sub:
        return "subitems", f"{len(need_sub)} subitem board(s) to spawn"
    fin = [o for o in state["ops"].values() if o["stage"] == "finish"]
    if not gen.get("finish") or any(o["status"] != "done" for o in fin):
        return "finish", "subitem columns / views / cleanup pending"
    return "verify", "all build stages done — run verification"


# ----------------------------------------------------------------------------- render
def lint_graphql(doc):
    """Cheap structural lint: balanced (), {}, [] outside string literals; terminated strings."""
    stack, i, pairs = [], 0, {")": "(", "}": "{", "]": "["}
    while i < len(doc):
        ch = doc[i]
        if ch == '"':
            i += 1
            while i < len(doc) and doc[i] != '"':
                i += 2 if doc[i] == "\\" else 1
            if i >= len(doc):
                raise ValueError("unterminated string literal")
        elif ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if not stack or stack.pop() != pairs[ch]:
                raise ValueError(f"unbalanced '{ch}' at offset {i}")
        i += 1
    if stack:
        raise ValueError(f"unclosed {stack}")


def render_chunks(state, op_ids, chunk):
    docs = []
    op_ids = [o for o in op_ids if o]
    for i in range(0, len(op_ids), chunk):
        part = op_ids[i:i + chunk]
        body = "\n".join(f"  {oid}: {state['ops'][oid]['gql']}" for oid in part)
        doc = "mutation {\n" + body + "\n}\n"
        lint_graphql(doc)
        docs.append((doc, part))
    return docs


# ----------------------------------------------------------------------------- ingest
def ingest(state, stage, paths):
    t = state["target"]
    done = failed = 0
    for p in paths:
        data, errors = unwrap(load_json_loose(p))
        err_by_alias = {}
        for e in errors or []:
            path = e.get("path") or []
            if path:
                err_by_alias[str(path[0])] = e.get("message")
        for oid, res in (data or {}).items():
            op = state["ops"].get(oid)
            if not op:
                continue
            if res is None:
                op["status"] = "failed"
                op["error"] = err_by_alias.get(oid, "null result")
                failed += 1
                continue
            op["status"] = "done"
            op["error"] = None
            op["result"] = res
            done += 1
            apply_result(state, op, res)
        for oid, msg in err_by_alias.items():
            if oid in state["ops"] and state["ops"][oid]["status"] != "done":
                state["ops"][oid]["status"] = "failed"
                state["ops"][oid]["error"] = msg
        if errors and not err_by_alias:
            state["log"].append({"at": now(), "stage": stage, "unattributed_errors": errors})
    state["log"].append({"at": now(), "stage": stage, "done": done, "failed": failed})
    return done, failed


def apply_result(state, op, res):
    t = state["target"]
    k, m = op["kind"], op["meta"]
    if k == "create_workspace":
        t["workspace_id"] = str(res["id"])
    elif k == "create_folder":
        t["folders"][m["src"]] = str(res["id"])
    elif k == "create_board":
        t["boards"][m["src"]] = str(res["id"])
        t["default_columns"][m["src"]] = res.get("columns") or []
        t["default_groups"][m["src"]] = res.get("groups") or []
    elif k == "create_group":
        t["groups"].setdefault(m["board"], {})[m["src"]] = str(res["id"])
    elif k == "create_column":
        if res.get("id") and res["id"] != m["target_id"]:
            t["col_ids"][m["board"]][m["src"]] = res["id"]
    elif k == "create_placeholder":
        t["placeholders"][m["board"]] = str(res["id"])
    elif k == "create_subitem":
        brd = res.get("board") or {}
        t["subitem_boards"][m["sub"]] = str(brd.get("id"))
        t["subitem_default_columns"][m["sub"]] = brd.get("columns") or []
        cols = (((res.get("parent_item") or {}).get("board") or {}).get("columns") or [])
        if cols:
            t["subtasks_col"][m["board"]] = cols[0]
    elif k == "delete_placeholder":
        t["placeholders"].pop(m["board"], None)


# ----------------------------------------------------------------------------- verify / diff
def verify_query(state):
    ids = [v for v in state["target"]["boards"].values()] + [v for v in state["target"]["subitem_boards"].values()]
    ids = ", ".join(str(i) for i in ids)
    return f"""query {{
  boards(ids: [{ids}]) {{
    id name
    columns {{ id title type }}
    groups {{ id title }}
    views {{ id name type }}
  }}
}}"""


def diff(state, path):
    data, _ = unwrap(load_json_loose(path))
    got = {str(b["id"]): b for b in data.get("boards") or []}
    lines, ok = [], True
    pairs = [(b, state["target"]["boards"].get(b["src_id"])) for b in replicable_boards(state)]
    pairs += [(state["blueprint"]["subitem_boards"][s], tid) for s, tid in state["target"]["subitem_boards"].items()]
    for b, tid in pairs:
        tb = got.get(str(tid))
        if not tb:
            lines.append(f"- MISSING board '{b['name']}' (target {tid})")
            ok = False
            continue
        want = {(c["title"], c["type"]) for c in b["columns"]
                if column_class(state, b, c)[0] in ("auto", "verify", "skip", "subitems")}
        have = {(c["title"], c["type"]) for c in tb["columns"]}
        miss = sorted(want - have)
        extra = sorted(have - want)
        gw = {g["title"] for g in b["groups"]}
        gh = {g["title"] for g in tb.get("groups") or []}
        vw = {v["name"] for v in b["views"] if is_table_view(v)}
        vh = {v["name"] for v in tb.get("views") or []}
        status = "OK" if not (miss or extra or gw - gh or gh - gw or vw - vh) else "DIFF"
        ok = ok and status == "OK"
        lines.append(f"## {b['name']} — {status}")
        if miss:
            lines.append(f"  missing columns: {miss}")
        if extra:
            lines.append(f"  extra columns: {extra}")
        if gw - gh:
            lines.append(f"  missing groups: {sorted(gw - gh)}")
        if gh - gw:
            lines.append(f"  extra groups: {sorted(gh - gw)}")
        if vw - vh:
            lines.append(f"  missing table views: {sorted(vw - vh)}")
    return ok, "\n".join(lines)


# ----------------------------------------------------------------------------- delta refresh
def refresh(state, raw_paths):
    """Merge a NEW source extraction into an existing state. Additive only:
    new folders/boards/groups/columns/views are queued; removals and edits of
    already-replicated objects are listed for manual handling (never auto-deleted)."""
    new = build_blueprint(raw_paths, state["meta"]["name"])["blueprint"]
    old = state["blueprint"]
    report = {"added": [], "manual": []}

    def idx(lst):
        return {x["src_id"]: x for x in lst}

    of = idx(old["folders"])
    for f in new["folders"]:
        if f["src_id"] not in of:
            old["folders"].append(f)
            report["added"].append(f"folder {f['name']}")

    def merge_board(ob, nb):
        for key, label in (("groups", "group"), ("columns", "column"), ("views", "view")):
            oi = idx(ob[key])
            ni = idx(nb[key])
            for sid, n in ni.items():
                if sid not in oi:
                    ob[key].append(n)
                    report["added"].append(f"{ob['name']}: {label} {n.get('title') or n.get('name')}")
                else:
                    o = oi[sid]
                    ttl = "title" if key != "views" else "name"
                    if key in ("columns", "groups") and n.get(ttl) != o.get(ttl) and n.get("type") != "subtasks":
                        state.setdefault("renames", []).append(
                            {"kind": label, "board": ob["src_id"], "src": sid, "title": n[ttl],
                             "n": len(state.get("renames", []))})
                        report["added"].append(f"{ob['name']}: rename {label} '{o.get(ttl)}' -> '{n[ttl]}'")
                        o[ttl] = n[ttl]
                    for fld in ("settings", "filter", "sort", "name"):
                        if key == "columns" and fld == "name":
                            continue
                        if fld in n and n.get(fld) != o.get(fld):
                            report["manual"].append(
                                f"{ob['name']}: {label} '{o.get('title') or o.get('name')}' changed ({fld}) — update in client UI")
                            break
            for sid, o in oi.items():
                if sid not in ni:
                    report["manual"].append(
                        f"{ob['name']}: {label} '{o.get('title') or o.get('name')}' removed in source — delete in client UI if intended")

    ob_idx = idx(old["boards"])
    for nb in new["boards"]:
        if nb["src_id"] not in ob_idx:
            old["boards"].append(nb)
            report["added"].append(f"board {nb['name']}")
        else:
            merge_board(ob_idx[nb["src_id"]], nb)
            if nb.get("subitem_board_src_id") and not ob_idx[nb["src_id"]].get("subitem_board_src_id"):
                ob_idx[nb["src_id"]]["subitem_board_src_id"] = nb["subitem_board_src_id"]
    for sid, nb in new["subitem_boards"].items():
        if sid not in old["subitem_boards"]:
            old["subitem_boards"][sid] = nb
        else:
            merge_board(old["subitem_boards"][sid], nb)
    for sid, b in ob_idx.items():
        if sid not in idx(new["boards"]):
            report["manual"].append(f"board '{b['name']}' no longer in source extraction — not touched in client")

    # re-open generation for stages that may now have new ops
    state.setdefault("generated", {})
    for st in ("structure", "finish"):
        state["generated"][st] = False
    # existing boards need a placeholder again only if a subitem board is newly introduced
    for m in report["manual"]:
        add_manual(state, "DELTA", m, "Detected on refresh")
    state["log"].append({"at": now(), "refresh": report})
    return report


# ----------------------------------------------------------------------------- CLI
def cmd_status(state):
    t = state["target"]
    ops = state["ops"].values()
    by = {}
    for o in ops:
        by.setdefault(o["stage"], {"pending": 0, "done": 0, "failed": 0})
        by[o["stage"]][o["status"]] += 1
    print(f"Project: {state['meta']['name']}  | source account: {(state['meta'].get('source_account') or {}).get('slug')}")
    print(f"Target workspace: {t['workspace_id']}  | boards mapped: {len(t['boards'])}/{len(replicable_boards(state))}"
          f"  | subitem boards: {len(t['subitem_boards'])}/{len(state['blueprint']['subitem_boards'])}")
    for s in STAGE_ORDER:
        if s in by:
            print(f"  {s:10s} {by[s]}")
    failed = [(k, o["error"]) for k, o in state["ops"].items() if o["status"] == "failed"]
    for k, e in failed[:20]:
        print(f"  FAILED {k}: {e}")
    ns, why = next_stage(state)
    print(f"Next: {ns} — {why}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("extract-query")
    a.add_argument("--workspace-id")
    a.add_argument("--page", type=int, default=1)
    a.add_argument("--limit", type=int, default=25)
    a.add_argument("--board-ids", nargs="*")

    a = sub.add_parser("blueprint")
    a.add_argument("--source", nargs="+", required=True, help="pasted source JSON file(s)")
    a.add_argument("--name", required=True)
    a.add_argument("--out", required=True, help="state.json path")
    a.add_argument("--sheet", help="manual build sheet .md path")
    a.add_argument("--target-workspace-id", help="use an existing client workspace instead of creating one")

    for nm in ("next", "status", "verify-query"):
        a = sub.add_parser(nm)
        a.add_argument("--state", required=True)

    a = sub.add_parser("stage")
    a.add_argument("--state", required=True)
    a.add_argument("--stage", choices=list(GENERATORS), help="default: next stage")
    a.add_argument("--chunk", type=int, default=20)
    a.add_argument("--outdir", required=True)
    a.add_argument("--force", action="store_true")

    a = sub.add_parser("set-workspace")
    a.add_argument("--state", required=True)
    a.add_argument("--target-workspace-id", required=True)

    a = sub.add_parser("ingest")
    a.add_argument("--state", required=True)
    a.add_argument("--stage", required=True, choices=list(GENERATORS))
    a.add_argument("--response", nargs="+", required=True)

    a = sub.add_parser("override-settings", help="replace a column's target settings (after a schema error)")
    a.add_argument("--state", required=True)
    a.add_argument("--board", required=True, help="SOURCE board id")
    a.add_argument("--column", required=True, help="SOURCE column id")
    a.add_argument("--settings-json", required=True, help="target-shaped settings object (inner, without the 'settings' wrapper)")

    a = sub.add_parser("skip-op", help="mark an op as handled manually (moves it to the manual sheet)")
    a.add_argument("--state", required=True)
    a.add_argument("--op", required=True)
    a.add_argument("--reason", required=True)

    a = sub.add_parser("refresh", help="merge a new source extraction (delta: additive only)")
    a.add_argument("--state", required=True)
    a.add_argument("--source", nargs="+", required=True)

    a = sub.add_parser("sheet", help="(re)write the manual build sheet")
    a.add_argument("--state", required=True)
    a.add_argument("--out", required=True)

    a = sub.add_parser("diff")
    a.add_argument("--state", required=True)
    a.add_argument("--response", required=True)

    args = ap.parse_args()

    if args.cmd == "extract-query":
        if not args.workspace_id and not args.board_ids:
            ap.error("--workspace-id or --board-ids required")
        print(extraction_query(args.workspace_id, args.page, args.limit, args.board_ids))
        return

    if args.cmd == "blueprint":
        state = build_blueprint(args.source, args.name)
        if args.target_workspace_id:
            state["target"]["workspace_id"] = str(args.target_workspace_id)
        save_state(state, args.out)
        if args.sheet:
            write_manual_sheet(state, args.sheet)
        bp = state["blueprint"]
        ncols = sum(len(b["columns"]) for b in bp["boards"])
        buckets = {}
        for b in bp["boards"] + list(bp["subitem_boards"].values()):
            for c in b["columns"]:
                k = column_class(state, b, c)[0]
                buckets[k] = buckets.get(k, 0) + 1
        print(json.dumps({
            "workspace": (bp["workspace"] or {}).get("name"),
            "folders": len(bp["folders"]), "boards": len(bp["boards"]),
            "replicable_boards": len(replicable_boards(state)),
            "subitem_boards": len(bp["subitem_boards"]), "columns_top_level": ncols,
            "column_buckets": buckets,
            "views": sum(len(b["views"]) for b in bp["boards"]),
            "table_views": sum(1 for b in bp["boards"] for v in b["views"] if is_table_view(v)),
            "manual_items": len(state["manual"]),
            "missing_subitem_boards": state["missing_subitem_boards"],
            "next": next_stage(state)[0],
        }, indent=2))
        return

    state = load_state(args.state)

    if args.cmd == "set-workspace":
        state["target"]["workspace_id"] = str(int(args.target_workspace_id))
        save_state(state, args.state)
        print("target workspace set; next: %s — %s" % next_stage(state))
        return

    if args.cmd == "override-settings":
        b = board_by_src(state, args.board)
        c = next((c for c in (b or {}).get("columns", []) if c["src_id"] == args.column), None)
        if not c:
            raise SystemExit("board/column not found in blueprint")
        c["settings_override"] = json.loads(args.settings_json)
        oid = alias("c", args.board, args.column)
        if oid in state["ops"] and state["ops"][oid]["status"] != "done":
            state["ops"][oid]["status"] = "failed"   # forces regeneration with new settings
        save_state(state, args.state)
        print(f"override stored for {args.board}/{args.column}; regenerate the stage")
        return

    if args.cmd == "skip-op":
        op = state["ops"].get(args.op)
        if not op:
            raise SystemExit("unknown op")
        op["status"] = "done"
        op["skipped"] = True
        add_manual(state, op["meta"].get("board", "ALL"), f"Op {args.op} ({op['kind']})", "Skipped: " + args.reason)
        save_state(state, args.state)
        print("skipped; next: %s — %s" % next_stage(state))
        return

    if args.cmd == "refresh":
        rep = refresh(state, args.source)
        save_state(state, args.state)
        print(json.dumps({"added": rep["added"], "needs_manual": rep["manual"],
                          "next": next_stage(state)}, indent=2, ensure_ascii=False))
        return

    if args.cmd == "sheet":
        write_manual_sheet(state, args.out)
        print("written", args.out)
        return

    if args.cmd == "next":
        print("%s — %s" % next_stage(state))
    elif args.cmd == "status":
        cmd_status(state)
    elif args.cmd == "verify-query":
        print(verify_query(state))
    elif args.cmd == "stage":
        nxt = next_stage(state)[0]
        st = args.stage or nxt
        if st != nxt and not args.force:
            raise SystemExit(f"Stage '{st}' requested but next stage is '{nxt}'. Use --force only for regeneration of a completed stage.")
        if st == "verify":
            print("All build stages done. Use verify-query.")
            return
        ops = GENERATORS[st](state)
        state.setdefault("generated", {})[st] = True
        pending = [k for k, o in state["ops"].items() if o["stage"] == st and o["status"] != "done"]
        chunk = min(args.chunk, 35) if st == "boards" else args.chunk
        docs = render_chunks(state, pending, chunk)
        os.makedirs(args.outdir, exist_ok=True)
        files = []
        for i, (doc, part) in enumerate(docs, 1):
            fn = os.path.join(args.outdir, f"{state['meta']['name']}_{st}_part{i}.graphql")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(doc)
            files.append((fn, len(part)))
        save_state(state, args.state)
        print(json.dumps({"stage": st, "ops": len(pending), "files": files,
                          "note": ("boards: >35 boards -> wait 60s between parts (40/min limit)"
                                   if st == "boards" and len(docs) > 1 else "")}, indent=2))
    elif args.cmd == "ingest":
        d, f = ingest(state, args.stage, args.response)
        save_state(state, args.state)
        print(json.dumps({"stage": args.stage, "done": d, "failed": f, "next": next_stage(state)}, indent=2))
        for k, o in state["ops"].items():
            if o["stage"] == args.stage and o["status"] == "failed":
                print(f"FAILED {k}: {o['error']}")
    elif args.cmd == "diff":
        ok, rep = diff(state, args.response)
        print(("VERIFIED — structure matches blueprint\n" if ok else "DIFFERENCES FOUND\n") + rep)


if __name__ == "__main__":
    main()
