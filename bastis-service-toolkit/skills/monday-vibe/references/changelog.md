# monday-vibe — confirmed release changelog

Dated log of confirmed Vibe releases, newest entry first, fed automatically by
`weekly-pulse` each time it runs. Treat as *last known good* — this only
covers what weekly-pulse has caught so far, so still confirm anything
stakes-sensitive against support.monday.com and Slack per the main skill
instructions.

## 2026-08-24 to 2026-08-31

- **Vibe apps can connect to any external API** (Released, all tiers) — API
  token auth (GET/POST/PUT), pull data from Jira/Salesforce/Snowflake/etc.
  alongside board data. Also enables Bring-Your-Own-Model (Gemini, Claude,
  OpenAI) for the app's AI logic. 1 credit per API call. No OAuth support yet.
  Source: Slack (https://monday.slack.com/archives/C094ZQJJ8GH/p1787823804802649)
- **Vibe AI Plan Mode** (rolling out, monday.monday now) — toggle "Plan" in
  the prompt box; Vibe proposes app options, features, theme/design
  direction, and a visual flowchart before building. Good opener for scoping
  conversations with clients who aren't sure what to build.
  Source: Docs (https://monday.monday.com/docs/18397954182)
- **Vibe Memory** (gradual release, full release targeted Aug 2026) — apps
  can now remember context/state across sessions instead of resetting each
  time. Reduces repetitive setup for client-facing apps.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12851077762)
- **Vibe Sketch Your App** (fully released) — draw or upload a sketch/
  wireframe/screenshot and Vibe generates a working app from it. Useful live
  in discovery calls.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12801273355)
- **Vibe Board Editing Subagent** (fully released) — Vibe can now edit
  *existing* boards (columns, views, automations) via natural language, not
  just generate new ones from scratch.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12832106502)

**Open questions flagged in Slack this week (unconfirmed, worth checking
before telling a client either way):** whether public Vibe apps require
viewers to log into *some* monday account on mobile even when meant to be
fully public; whether Contributor-level board permissions block item
creation inside a Vibe app the way they do natively; pricing flexibility
below the 25-app package minimum. None of these were resolved in-thread —
verify current behavior before committing to an answer.
