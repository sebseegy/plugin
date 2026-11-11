## Session continuity
- Live state is injected at every session start from `Client Context/project-state.md` (hook). If no "Live client state" appears in context, read that file first.
- Before stopping, run `/handoff`. Chat history is not memory; the state file and `decisions-log.md` are.
- Treat the injected "Files modified since last state update" list as ground truth over the written log when they disagree.
- Never send or finalize client communication; drafts only.
