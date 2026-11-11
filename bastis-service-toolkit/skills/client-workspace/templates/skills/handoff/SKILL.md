---
name: handoff
description: Write the end-of-session handoff for this client. Use when Basti says "handoff", "wrap up", "save where we are", "update the state", before closing a session, switching chat, or after finishing a milestone. Updates Client Context/project-state.md so the next session starts exactly where this one stopped.
---

# handoff

1. Read `Client Context/project-state.md` and the "Files modified since last state update" list injected at session start (or run `find . -type f -newer "Client Context/project-state.md"`).
2. Update the file in place (never replace it wholesale):
   - Refresh **Last updated** (date, this session's title).
   - Rewrite **Where we stopped** and **Next steps** from what actually happened in this session. Only facts from this session, files, or calls; mark the rest `unconfirmed`.
   - Move resolved items out of **Open questions**; add new blockers with owner and date.
   - Prepend one row to the **Handoff log**; when it exceeds 8 rows, move the oldest to `Client Context/handoff-archive.md`.
3. Copy any durable decision to `Client Context/decisions-log.md` (date, decision, who, source).
4. Say in one line what changed. Do not message the client or anyone else.
