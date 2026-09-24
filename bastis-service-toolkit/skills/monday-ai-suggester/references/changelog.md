# monday-ai-suggester — confirmed release changelog

Dated log of confirmed AI feature releases, newest entry first, fed
automatically by `weekly-pulse` each time it runs. This skill still pulls
fresh data every time it runs (Step 2 in SKILL.md) — this log is a
quick-start baseline, not a replacement for that pull.

## 2026-08-24 to 2026-08-31

**Sidekick**
- Now reachable from Telegram and WhatsApp (Released, gradual external
  rollout). Users connect via a barcode on the Personalization page and chat
  with Sidekick from their messaging app. Good pitch for field/mobile-first
  teams. Source: Slack (https://monday.slack.com/archives/C09MKR01006/p1787210037)

**Vibe**
- Connects to any external API (token auth) + Bring-Your-Own-Model
  (Gemini/Claude/OpenAI). Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12928960931)
- AI Plan Mode — proposes app options/features/flowchart before building.
- Memory — apps retain context across sessions (gradual release).
- Sketch Your App — generates an app from a drawn/uploaded sketch (fully released).
- Board Editing Subagent — can now edit existing boards, not just create new ones (fully released).
- See `../monday-vibe/references/changelog.md` for full detail and sources on all of the above.

**AI in Automations**
- Formula columns are now usable as context for AI blocks (Beta, limited
  access) — AI blocks in workflows can read calculated values, enabling
  automations that react to computed thresholds (e.g. a risk score).
  Source: Slack (https://monday.slack.com/archives/C09PR4UAUDS/p1787666818583319)

**Agents**
- No new feature releases this week — Slack traffic in #ask-ai-agents was
  mostly account-level support questions (enabling AI agents, credit
  visibility, model version rollback), not new capability.
