#!/usr/bin/env python3
"""Helpers for the monday Developer Center (API playground) workflow.

Claude never calls the client API and never holds the token. Two ways to get
responses into JSON files:
  A. the consultant runs queries in the client's playground and pastes responses;
  B. the consultant runs `run` below in his OWN terminal with his API token in the
     shell environment (never in chat, never in a file).
Either way, the other commands turn those files into analysis Claude can reason over.

Commands
  whoami     (mode B) check the token reaches the expected client account; sends nothing else
  run        (mode B) execute .graphql files against the client API and save each response
             as a numbered JSON file. Read-only unless --apply (+ typed confirmation).
  new        create empty JSON files for the consultant to paste responses into
  usage      per-board, per-column fill rates (+ top values) from structure + items responses
  diff       structure diff between two structure responses (before / after)
  automations  readable summary of a board_automations response; flags references
             to columns that no longer exist and legacy triggers on missing status labels

All commands are stdlib-only and read-only on the input files.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request


# ---------- loading ----------

def load(path):
    with open(path) as f:
        txt = f.read().strip()
    if not txt:
        sys.exit(f"{path} is empty - paste the playground response into it first.")
    # tolerate a pasted response that has text around the JSON
    start, end = txt.find("{"), txt.rfind("}")
    d = json.loads(txt[start:end + 1])
    if d.get("errors"):
        print(f"NOTE {os.path.basename(path)} contains errors:", file=sys.stderr)
        for e in d["errors"]:
            print("   ", e.get("path"), e.get("message"), file=sys.stderr)
    return d.get("data", d)


def structure_boards(data):
    """Collect every board object that has `columns` from a structure response (any alias)."""
    boards = {}
    for key, val in data.items():
        if isinstance(val, list):
            for b in val:
                if isinstance(b, dict) and "columns" in b and b.get("id"):
                    boards[str(b["id"])] = b
    return boards


def label_map(col):
    """Return {id: name} for status / dropdown columns, else {}."""
    try:
        s = json.loads(col.get("settings_str") or "{}")
    except ValueError:
        return {}
    labels = s.get("labels")
    if isinstance(labels, dict):
        return {str(k): v for k, v in labels.items()}
    if isinstance(labels, list):
        return {str(l.get("id")): l.get("name") for l in labels if isinstance(l, dict)}
    return {}


# ---------- new ----------

def cmd_new(args):
    for p in args.paths:
        if os.path.exists(p) and os.path.getsize(p) > 0 and not args.force:
            print(f"skip {p} (exists and is not empty; use --force to blank it)")
            continue
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        open(p, "w").close()
        print(f"created {p}")


# ---------- usage ----------

def filled(cv):
    if cv.get("linked_item_ids"):
        return True
    for k in ("text", "display_value"):
        v = cv.get(k)
        if v not in (None, "", "0", "false", "[]", "{}"):
            return True
    return False


def value_text(cv):
    return (cv.get("text") or cv.get("display_value") or "").strip()


def iter_item_boards(data, alias_map):
    """Yield (board_id, board_name, items) for every items_page in an items response."""
    for key, val in data.items():
        if key == "complexity" or not isinstance(val, list):
            continue
        for b in val:
            if not isinstance(b, dict) or "items_page" not in b:
                continue
            bid = str(b.get("id") or alias_map.get(key) or key)
            yield bid, b.get("name") or key, b["items_page"].get("items", [])


def cmd_usage(args):
    sboards = structure_boards(load(args.structure))
    alias_map = dict(a.split("=", 1) for a in (args.alias or []))
    out = []
    for path in args.items:
        for bid, bname, items in iter_item_boards(load(path), alias_map):
            sb = sboards.get(bid)
            cols = {c["id"]: c for c in sb["columns"]} if sb else {}
            name = sb["name"] if sb else bname
            n = len(items)
            counts = collections.Counter()
            values = collections.defaultdict(collections.Counter)
            seen = []
            for it in items:
                for cv in it.get("column_values", []):
                    cid = cv["id"]
                    if cid not in seen:
                        seen.append(cid)
                    if filled(cv):
                        counts[cid] += 1
                        values[cid][value_text(cv)[:40]] += 1
            out.append(f"\n## {name} ({bid}): {n} items\n")
            if not sb:
                out.append(f"_Board {bid} not in the structure file; titles unknown. "
                           f"Add `id name` to the items query or pass --alias {bid if bid.isdigit() else '<alias>'}=<board_id>._\n")
            out.append("| Filled | Column | Type | Title | Top values / note |")
            out.append("|---|---|---|---|---|")
            for cid in seen:
                c = cols.get(cid, {})
                typ, title = c.get("type", "?"), c.get("title", "?")
                k = counts[cid]
                note = ""
                if typ in ("status", "dropdown", "color") and k:
                    note = " · ".join(f"{v} ×{c_}" for v, c_ in values[cid].most_common(5))
                if typ == "mirror" and k == 0:
                    note = "⚠ mirror: the API often returns blanks (esp. mirrors of formulas), check in the UI"
                if typ in ("subtasks", "unsupported") and k == 0:
                    note = "text not returned by the API; not a usage signal"
                flag = "∅ " if k == 0 else ""
                out.append(f"| {flag}{k}/{n} | `{cid}` | {typ} | {title} | {note} |")
            if sb:
                missing = [c for c in sb["columns"] if c["id"] not in seen]
                if missing:
                    out.append("\nNot in the items response (limit to column_values ids?): "
                               + ", ".join(f"`{c['id']}` {c['title']}" for c in missing))
    text = "\n".join(out)
    if args.out:
        with open(args.out, "w") as f:
            f.write(f"# Column usage\n\nSource: {args.structure} + {', '.join(args.items)}\n" + text + "\n")
        print(f"wrote {args.out}")
    else:
        print(text)


# ---------- diff ----------

def cmd_diff(args):
    old_d, new_d = load(args.old), load(args.new)
    old, new = structure_boards(old_d), structure_boards(new_d)
    lines = []
    for bid in sorted(set(old) | set(new)):
        o, n = old.get(bid), new.get(bid)
        if not o:
            lines.append(f"+ BOARD {bid} {n['name']}")
            continue
        if not n:
            lines.append(f"- BOARD {bid} {o['name']} (missing in new, deleted, archived or outside the query)")
            continue
        oc = {c["id"]: c for c in o["columns"]}
        nc = {c["id"]: c for c in n["columns"]}
        ch = []
        for cid in nc:
            if cid not in oc:
                ch.append(f"  + col `{cid}` {nc[cid]['title']} ({nc[cid]['type']})")
        for cid in oc:
            if cid not in nc:
                ch.append(f"  - col `{cid}` {oc[cid]['title']}")
        for cid in nc:
            if cid in oc:
                a, b = oc[cid], nc[cid]
                if a["title"] != b["title"]:
                    ch.append(f"  ~ title `{cid}`: {a['title']} → {b['title']}")
                if (a.get("description") or "") != (b.get("description") or "") and "description" in b:
                    ch.append(f"  ~ description `{cid}` {b['title']}")
                if a.get("settings_str") != b.get("settings_str") and "settings_str" in b:
                    la, lb = label_map(a), label_map(b)
                    if la != lb:
                        added = {k: v for k, v in lb.items() if la.get(k) != v}
                        removed = {k: v for k, v in la.items() if k not in lb}
                        ch.append(f"  ~ labels `{cid}` {b['title']}: +{added} -{removed}")
                    else:
                        ch.append(f"  ~ settings `{cid}` {b['title']}")
        for key, fmt in (("views", lambda v: v["name"]), ("groups", lambda g: g["title"])):
            if key in o and key in n:
                a, b = [fmt(x) for x in o[key]], [fmt(x) for x in n[key]]
                if a != b:
                    ch.append(f"  ~ {key}: {a} → {b}")
        if o.get("items_count") != n.get("items_count") and "items_count" in n:
            ch.append(f"  ~ items {o.get('items_count')} → {n.get('items_count')}")
        if o.get("name") != n.get("name"):
            ch.append(f"  ~ name {o['name']} → {n['name']}")
        if (o.get("description") or "") != (n.get("description") or "") and "description" in n:
            ch.append("  ~ board description changed")
        if o.get("board_folder_id") != n.get("board_folder_id") and "board_folder_id" in n:
            ch.append(f"  ~ folder {o.get('board_folder_id')} → {n.get('board_folder_id')}")
        if ch:
            lines.append(f"\n{bid} {n['name']}")
            lines.extend(ch)
    of = {f["id"]: f for f in old_d.get("folders", []) or []}
    nf = {f["id"]: f for f in new_d.get("folders", []) or []}
    for fid in set(of) | set(nf):
        if fid not in nf:
            lines.append(f"- FOLDER {of[fid]['name']} ({fid})")
        elif fid not in of:
            lines.append(f"+ FOLDER {nf[fid]['name']} ({fid})")
        elif of[fid].get("name") != nf[fid].get("name"):
            lines.append(f"~ FOLDER {fid}: {of[fid]['name']} → {nf[fid]['name']}")
    print("\n".join(lines) if lines else "No structural differences.")


# ---------- automations ----------

COL_ID = re.compile(r"^[a-z][a-z0-9_]*$")


def _walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k, v
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def cmd_automations(args):
    data = load(args.file)
    sboards = structure_boards(load(args.structure)) if args.structure else {}
    alias_map = dict(a.split("=", 1) for a in (args.alias or []))
    for key, val in data.items():
        if not isinstance(val, dict) or ("items" not in val and "legacy_automations" not in val):
            continue
        bid = alias_map.get(key)
        sb = sboards.get(bid) if bid else None
        cols = {c["id"]: c for c in sb["columns"]} if sb else {}
        print(f"\n## {key}" + (f" → {sb['name']} ({bid})" if sb else ""))
        for it in val.get("items", []) or []:
            state = "ON " if it.get("active") else "OFF"
            desc = (it.get("description") or "").replace("\n", " ").strip()
            print(f"- NEW {it['id']} [{state}] {desc[:160] or it.get('title', '')[:120]}")
            blocks = sorted(it.get("workflow_blocks") or [], key=lambda b: b.get("workflowNodeId", 0))
            if blocks:
                print("    blocks: " + " > ".join(b.get("title", "?") for b in blocks))
            cfg = []
            for w in it.get("workflow_variables") or []:
                c = w.get("config") or {}
                if w.get("sourceKind") == "user_config" and c.get("title"):
                    v = c.get("value")
                    if isinstance(v, dict):
                        v = v.get("name") or v.get("id")
                    cfg.append(f"{c['title']}={v}")
                    # column pickers carry an icon; operators such as "is_any_of" don't
                    if isinstance(c.get("value"), str) and cols and COL_ID.match(c["value"]) \
                            and "icon" in c and c["value"] not in cols:
                        print(f"    ⚠ references column `{c['value']}` ({c['title']}), which is not on the board")
                if w.get("sourceKind") == "node_results":
                    key_ = (w.get("sourceMetadata") or {}).get("outboundFieldKey", "")
                    if key_.startswith("item.") and cols:
                        ref = key_.split(".")[1]
                        if ref not in cols and ref not in ("name", "$groupName"):
                            print(f"    ⚠ reads item.{ref}, which is not on the board")
            if cfg:
                print("    config: " + "; ".join(dict.fromkeys(cfg)))
        leg = val.get("legacy_automations") or {}
        for a in (leg.get("automations") if isinstance(leg, dict) else []) or []:
            state = "ON " if a.get("active") else "OFF"
            print(f"- LEGACY {a['id']} [{state}] {a.get('description') or a.get('source') or ''} (recipe {a.get('recipeId')})")
            conf = a.get("config") or {}
            refs, idx = set(), []
            for k, v in _walk(conf):
                if k == "columnId":
                    cid = v.get("columnId") if isinstance(v, dict) else v
                    if isinstance(cid, str):
                        refs.add(cid)
                if k == "statusColumnValue" and isinstance(v, dict):
                    idx.append(v.get("index"))
            if "pulseMapping" in conf:
                for cid, cv in conf["pulseMapping"].get("columnValues", {}).items():
                    refs.add(cid)
                    if isinstance(cv, dict) and "index" in cv:
                        idx.append(cv["index"])
            print(f"    columns: {sorted(refs)}  status label ids: {idx}")
            if cols:
                for cid in refs:
                    if cid not in cols:
                        print(f"    ⚠ references column `{cid}`, which is not on this board "
                              f"(deleted, or a field of the linked/target board)")
                stage_cols = [c for c in refs if c in cols and cols[c]["type"] == "status"]
                for sc in stage_cols:
                    labels = label_map(cols[sc])
                    for i in idx:
                        if i is not None and str(i) not in labels:
                            print(f"    ⚠ status label id {i} does not exist on `{sc}` (labels: {labels})")
                        elif i is not None:
                            print(f"    label {i} = {labels[str(i)]}")


# ---------- run / whoami (API-key mode; the consultant runs these, Claude never does) ----------

API_URL = "https://api.monday.com/v2"
ID_QUERY = "query { me { name account { slug name } } }"


def _token(client):
    """Token comes only from the shell environment: MONDAY_TOKEN_<CLIENT>, else MONDAY_API_TOKEN.
    Never from a CLI argument, a file or chat, so it can't land in history, logs or the repo."""
    names = []
    if client:
        names.append("MONDAY_TOKEN_" + re.sub(r"[^A-Za-z0-9]+", "_", client).strip("_").upper())
    names.append("MONDAY_API_TOKEN")
    for n in names:
        v = os.environ.get(n, "").strip()
        if v:
            return v
    sys.exit("No token in the environment. In your own terminal run (the token never goes in chat or a file):\n"
             f"  read -s {names[0]}; export {names[0]}")


def _post(token, query, version):
    req = urllib.request.Request(
        API_URL, data=json.dumps({"query": query}).encode(),
        headers={"Authorization": token, "API-Version": version,
                 "Content-Type": "application/json", "User-Agent": "devcenter-skill/1"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code == 429 and attempt == 1:
                wait = int(e.headers.get("Retry-After", "10") or 10)
                print(f"rate limited, retrying once in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            try:
                return e.code, json.loads(body)
            except ValueError:
                return e.code, {"errors": [{"message": body[:300]}]}
        except urllib.error.URLError as e:
            sys.exit(f"Network error: {e.reason}")


def _has_mutation(q):
    # deliberately blunt: the word anywhere (even in a comment) counts, so a write can never slip through as a read
    return re.search(r"\bmutation\b", q, re.I) is not None


def _identity(token, version, expect):
    status, d = _post(token, ID_QUERY, version)
    me = ((d.get("data") or {}).get("me")) or {}
    slug = (me.get("account") or {}).get("slug")
    if status != 200 or not slug:
        sys.exit(f"Identity check failed (HTTP {status}): {[e.get('message') for e in d.get('errors', [])] or d}")
    if slug != expect:
        sys.exit(f"WRONG ACCOUNT: token belongs to '{slug}', expected '{expect}'. Nothing was run.")
    print(f"identity ok: {slug} ({me['account'].get('name')})")
    return slug


def cmd_whoami(args):
    _identity(_token(args.client), args.api_version, args.expect_slug)


def cmd_run(args):
    token = _token(args.client)
    queries = []
    for p in args.files:
        with open(p) as f:
            q = f.read()
        if not q.strip():
            sys.exit(f"{p} is empty")
        queries.append((p, q))
    mutating = [(p, q) for p, q in queries if _has_mutation(q)]
    if mutating and not args.apply:
        sys.exit("REFUSED: these files contain a write and this run is read-only. Nothing was sent.\n  "
                 + "\n  ".join(p for p, _ in mutating)
                 + "\nReview them, then re-run with --apply if you approve.")
    slug = _identity(token, args.api_version, args.expect_slug)
    if mutating:
        if not sys.stdin.isatty():
            sys.exit("Writes need an interactive confirmation; run this from your terminal. Nothing was sent.")
        for p, q in mutating:
            print(f"\n=== WRITE: {p} ===\n{q.strip()}\n")
        if input(f"Type the account slug '{slug}' to apply these writes to the LIVE account: ").strip() != slug:
            sys.exit("Not confirmed. Nothing was sent.")
    failed = False
    for p, q in queries:
        status, d = _post(token, q, args.api_version)
        out_dir = args.out_dir or os.path.dirname(os.path.abspath(p))
        os.makedirs(out_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(p))[0]
        out, n = os.path.join(out_dir, stem + ".json"), 1
        while os.path.exists(out) and os.path.getsize(out) > 0:       # never overwrite a response
            n += 1
            out = os.path.join(out_dir, f"{stem}_run{n}.json")
        with open(out, "w") as f:
            json.dump(d, f, indent=2)
        errs = d.get("errors") or []
        failed = failed or status != 200 or bool(errs)
        print(f"{'OK ' if status == 200 and not errs else 'ERR'} {p} -> {out} (HTTP {status}, {len(errs)} errors)")
        for e in errs[:5]:
            print("   ", e.get("message"))
        with open(os.path.join(out_dir, "runs.log"), "a") as lg:       # no token, no response data
            lg.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "file": p,
                                 "query_sha1": hashlib.sha1(q.encode()).hexdigest()[:10],
                                 "api_version": args.api_version, "account": slug,
                                 "write": _has_mutation(q), "http": status, "errors": len(errs),
                                 "saved_as": out}) + "\n")
    sys.exit(1 if failed else 0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("whoami"); s.add_argument("--client"); s.add_argument("--expect-slug", required=True)
    s.add_argument("--api-version", default="dev"); s.set_defaults(fn=cmd_whoami)
    s = sub.add_parser("run"); s.add_argument("files", nargs="+"); s.add_argument("--client")
    s.add_argument("--expect-slug", required=True); s.add_argument("--api-version", default="dev")
    s.add_argument("--out-dir"); s.add_argument("--apply", action="store_true", help="allow files containing writes (asks for typed confirmation)")
    s.set_defaults(fn=cmd_run)
    s = sub.add_parser("new"); s.add_argument("paths", nargs="+"); s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_new)
    s = sub.add_parser("usage"); s.add_argument("--structure", required=True); s.add_argument("--items", nargs="+", required=True)
    s.add_argument("--alias", nargs="*", help="alias=board_id for items blocks queried without `id`"); s.add_argument("--out")
    s.set_defaults(fn=cmd_usage)
    s = sub.add_parser("diff"); s.add_argument("--old", required=True); s.add_argument("--new", required=True)
    s.set_defaults(fn=cmd_diff)
    s = sub.add_parser("automations"); s.add_argument("--file", required=True); s.add_argument("--structure")
    s.add_argument("--alias", nargs="*", help="alias=board_id, e.g. a_opp=1234567890"); s.set_defaults(fn=cmd_automations)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
