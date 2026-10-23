# Webhook patterns

## What changed (grade B, owner posts 6 and 15 Oct 2026)
Until 6 Oct the trigger only started a run. Now the JSON body of the request is passed into the workflow as one string. Fields are not auto-split. Parse with Code or JSON Parser.

## Delivery semantics (A, source)
- Public route returns 200 right away and hands the event to a queue. Success of the POST says nothing about the run.
- Inactive, expired or unknown URL: dropped silently, still 200. If nothing runs, check the workflow is active and the URL matches the trigger.
- If the trigger fires but the platform call fails, a failed run appears in the activity log.
- No auth, HMAC or per-URL rate limit. Treat the URL as a secret; rotate by creating a new trigger.
- Sender retries can double-fire. Dedupe on an event id in the payload.

## Inbound uses
| Sender | Pattern |
|---|---|
| External system (monitoring, CRM, form tool, Harmony.ai) | POST JSON -> parse -> Get item data / create item -> notify |
| monday board webhook recipe on N boards | N senders -> 1 workflow (below) |
| Make/Zapier/n8n | Same; URL is the credential |
| Agents | An agent or MCP caller can POST to start a flow (D, untested) |

## N boards -> 1 workflow
```
[sender recipe per board] --webhook--> [1 workflow]
 1. When a webhook is received          (body: JSON string)
 2. Code: parse                          (outputs: ok, relevant, ids, labels - all strings)
 3. Condition ok = "true"                no -> notify (parse failed)
 4.   Condition relevant = "true"        no -> end
 5.     Code: act via monday API         (lookup, create_update, create_notification)
 6. Optional: posted_count = "0" or error not empty -> notify
```
Rules: filter at sender if possible, always in the workflow too. Sender recipes per board are still needed - script them. Board templates reportedly do not carry automations (D). Verify column IDs identical on all N boards (duplicated boards share IDs, A in one test; query and diff). For subitem events `boardId` is the subitem board, parent in `parentItemBoardId`. `previousValue` can be a null object, guard with `or {}`. `isRetry`/`triggerUuid` allow dedupe.

## Parse snippet (owner-documented, B)
```python
import json
def extract(json_string):
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None

d = extract(input["body"]) or {}
return {"ok": str(bool(d)).lower(), "name": str(d.get("name", ""))}
```

## Pre-flight checklist
- [ ] Real payload captured per sender type
- [ ] Activate, deactivate, reactivate, then send a live POST (reactivation fix 24 Sep, A in code, not field-verified)
- [ ] Response code vs actual run: HTTP 200 does not prove a run started; check Run history
- [ ] Activate in the same session the URL was generated (pending URL TTL 12 h)
- [ ] Retry policy decided (`isRetry`, `triggerUuid`)
- [ ] Service user is creator; URL kept out of docs
- [ ] Failure path notifies on `ok=false`
- [ ] Old workflows paused, not deleted
- [ ] Non-actor test user for notifications
- [ ] Run quota/AI-credit and 250 active-workflow cap checked via monday-workflow-architect Gate 1
