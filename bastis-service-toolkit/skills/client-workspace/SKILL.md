---
name: client-workspace
description: Sets up (or repairs) a Claude Code workspace inside a local client folder under Work/Clients/, so every Claude Code session starts with the client's latest context and knows where earlier chats stopped. Installs a SessionStart hook that injects Client Context/project-state.md plus a list of files changed since the last handoff, a /handoff project skill, and a continuity block in the client CLAUDE.md. Use when Basti says "set up the Claude Code workspace for [client]", "make [client] ready for Claude Code", "session continuity", "where did the other chats stop", "handoff setup", or when starting Claude Code on a new client. Run after local-setup-context. Never overwrites existing files.
---

# client-workspace

Companion to `local-setup-context`. That skill fills the client folder; this one makes the folder a continuity-aware Claude Code workspace. Source docs: code.claude.com/docs/en/memory, /desktop, /hooks-guide.

## How continuity works (and what is not guaranteed)

| Need | Mechanism | Guarantee |
|---|---|---|
| Rules and identity every session | `Clients/CLAUDE.md` + `<Client>/CLAUDE.md` (CLAUDE.md files walk up from the working folder and load in full at launch) | Loaded, but treated as context, not enforced |
| Live state every session | SessionStart hook runs `.claude/hooks/state-inject.sh`; stdout is added to context (fires on startup, resume, clear, compact) | Deterministic, if the hook runs |
| Where chats stopped | `/handoff` writes `Client Context/project-state.md`; hook also lists files modified since that update | Write side depends on running `/handoff`; the activity list does not |
| Other open desktop chats | Ask Claude "what did the other sessions conclude?" (Code tab reads the 20 most recent desktop sessions) | Desktop sessions only, not CLI or cloud |

Not used: auto memory (machine-local, Claude-written, 200-line cap, not in the client structure) and `AGENTS.md` (only needed if another agent tool shares the folder; then `CLAUDE.md` should start with `@AGENTS.md`).

Templates (settings, hook script, /handoff skill, project-state, continuity block) live in this skill's own `templates/` folder.

## Procedure (idempotent; create only what is missing)

1. Read `Clients/CLAUDE.md`, the client `CLAUDE.md`, `Client Context/`. Report what already exists.
2. Create if missing (never overwrite; if present and different, show a diff and ask):
   - `<Client>/.claude/settings.json` from `templates/settings.json`. If one exists, merge only the `SessionStart` entry.
   - `<Client>/.claude/hooks/state-inject.sh` from `templates/hooks/` (chmod +x).
   - `<Client>/.claude/skills/handoff/SKILL.md` from `templates/skills/handoff/`.
   - `<Client>/Client Context/project-state.md` from `templates/project-state.md`, filled only with confirmed facts (SKUs and phase from `CLAUDE.md`, `meta.json`, calls); the rest stays `TODO`.
3. Append `templates/CLAUDE-continuity-block.md` to the client `CLAUDE.md` if "Session continuity" is absent. Check the file stays under 200 lines.
4. Verify (all must pass, report each):
   - `.claude/settings.json` parses as JSON.
   - `bash .claude/hooks/state-inject.sh` exits 0 and prints the state; touch a file under `SKU level/` and confirm the WARNING line appears.
   - `CLAUDE.md` under 200 lines; no existing file changed except the appended block.
5. Tell Basti the two manual steps (cannot be scripted):
   - **Start sessions in the client folder.** In the Code tab, add a saved local environment for `Clients/<Client>/` (current layout: selector in the row under the prompt box, then New environment, Local tab). If the selector sits above the prompt box you have the earlier layout; use the project-folder control instead.
   - **Accept the workspace trust dialog** for the folder; project hooks only run after that.
6. Two-minute test (the only end-to-end check): open a new session in the folder and ask "what state are we in and what changed since the last handoff?" Claude should quote `project-state.md` without reading it. If not, run `claude --debug` and look for hook errors.

## Rules

- Moves and writes follow `Clients/CLAUDE.md`; deliverables already shared are not edited.
- Never invent state. Unknown stays `TODO` or `unconfirmed`.
- Never send client communication.
