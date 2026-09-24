# monday-vibe — confirmed release changelog

Dated log of confirmed Vibe releases, newest entry first, fed automatically by
`weekly-pulse` each time it runs. Treat as *last known good* — this only
covers what weekly-pulse has caught so far, so still confirm anything
stakes-sensitive against support.monday.com and Slack per the main skill
instructions.

## Catch-up, added manually 2026-09-24

Releases weekly-pulse hadn't logged, confirmed via Company Brain and the support
best-practices article on 2026-09-24.

- **Vibe DB** (Full release, all Vibe tiers per the Aug 2026 Product Updates deck) —
  per-app database, ~10 GB / ~1M items, 256 KB per record, no images, no
  automations/dashboards on the data, no draft/live split. Left-pane apps created
  from ~26 Aug 2026 only. Enable via `+` → Integrations → Advanced → "Create fast
  database", or ask "use Vibe DB to store the data".
  Source: Company Brain (Aug 2026 Product Updates deck, #ask-vibe-ai)
- **Up to 20 connected boards** — the support article now states "You can connect
  up to twenty boards at a time". Internal packaging still lists 5 by default and 20
  on Vibe Growth or Custom/Enterprise; confirm per account.
  Source: Docs (https://support.monday.com/hc/en-us/articles/34101891654034, modified 2026-09-22); Company Brain (packaging SOT monday.monday.com/docs/18411930424)
- **Unique page URLs** (since June 2026) — every page can have its own URL with
  working back/forward. Extra query parameters are not reliably forwarded into the
  app on private apps; put record keys in the route path or use item views.
  Source: Company Brain (#ask-vibe-ai, June 2026); confirmed in production on WHSmith, 2026-09-23
- **Board editing from the chat, element selection tool, image generation,
  chat images as app assets** — all listed in the current best-practices article.
  Source: Docs (https://support.monday.com/hc/en-us/articles/34101891654034)

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
