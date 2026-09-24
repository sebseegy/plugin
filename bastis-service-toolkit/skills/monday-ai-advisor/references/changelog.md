# monday-ai-advisor — confirmed release changelog

Dated log of confirmed AI feature releases, newest entry first, fed
automatically by `weekly-pulse` each time it runs. Check this before
explaining a feature so the explanation reflects current capability, not
just the static description in SKILL.md.

## 2026-08-24 to 2026-08-31

- **Sidekick** now works over Telegram and WhatsApp, not just in-board chat
  (Released, gradual external rollout). Update the "how it works" pitch:
  Sidekick is no longer confined to the board UI — users can reach it from a
  messaging app they already use daily.
  Source: Slack (https://monday.slack.com/archives/C09MKR01006/p1787210037)
- **Vibe** gained several capabilities this week worth folding into the pitch:
  - Connects to any external API + Bring-Your-Own-Model (Gemini/Claude/OpenAI) — Vibe apps are no longer limited to monday board data or a fixed model.
  - Plan Mode — proposes app structure/flowchart before building, useful to show a client the "planning" step exists.
  - Memory — apps now persist context across sessions.
  - Sketch Your App — generates an app from a drawn/uploaded sketch.
  - Board Editing Subagent — can edit existing boards, not just build new ones from scratch.
  - Full detail/sources: `../monday-vibe/references/changelog.md`.
- **AI in Automations** — formula columns can now feed AI blocks as context
  (Beta, limited access). Update the "AI in Automations" section: AI steps in
  a workflow can now react to a calculated value (e.g. a project health
  score), not just raw column data.
  Source: Slack (https://monday.slack.com/archives/C09PR4UAUDS/p1787666818583319)
