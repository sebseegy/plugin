# monday-vibe — confirmed release changelog

Dated log of confirmed Vibe releases, newest entry first, fed automatically by
`weekly-pulse` each time it runs. Treat as *last known good* — this only
covers what weekly-pulse has caught so far, so still confirm anything
stakes-sensitive against support.monday.com and Slack per the main skill
instructions.

## 2026-09-17 to 2026-09-24

- **Vibe "Request to publish" approval flow — live** — Admins can lock Vibe
  publishing to admins-only. Builders click Publish → admin gets a notification
  → one-click Approve or Decline. Closes the Enterprise governance gap:
  "who controls what goes org-wide in Vibe?" now has an answer.
  (Slack-only this week — not yet logged on IC board.)
  Source: Slack #ask-vibe-ai (https://monday.slack.com/archives/C094ZQJJ8GH/p1788850810482369)
- **Performance issue flagged — multi-page app navigation** — Multiple ICs
  reporting slowness when navigating between pages in a Vibe app. No fix
  announced yet; flag as a known friction point for multi-page builds.
  Source: Slack #ask-vibe-ai (https://monday.slack.com/archives/C094ZQJJ8GH)
- **Vibe webinar on YouTube** — 45 min covering security/permissions model,
  sharing outside accounts, live builds, and common IC questions.
  Source: https://www.youtube.com/watch?v=XeuHr8HmA7E

## 2026-09-14 to 2026-09-21

- **Vibe Stop Button — fully released, all tiers** — Interrupt AI generation
  mid-build, adjust prompt, restart. Saves credits and reduces friction in demos
  and live client build sessions.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/13080566422)
- **Vibe Memory — full release confirmed, all tiers** — Previously gradual/
  targeted; now confirmed 100% across all tiers. Apps remember preferences,
  styles, and design choices across sessions.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12851077762)
- **Vibe AI Image Generation — 100% global rollout** — All regions (US/EU/AU/IL)
  at 100%. Vibe apps generate AI images on the fly from board data. ~<10 credits
  each. Powered by gemini-3.1-flash-lite-image.
  Source: Slack (https://monday.slack.com/archives/C095817BPM5/p1789371907318219)
- **Vibe duplicate + replace boards — fully released, all tiers** — Clone a Vibe
  app to another board with the same structure; replace the underlying board
  connection. IC time-saver for templated builds across clients.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12832609226)
- **Vibe apps → external APIs — confirmed fully released, all tiers** — Sep 20
  board re-confirms global release. Framing: "full integration hubs" not just
  dashboards. Any REST API, any external service.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12928960931)
- **Vibe board editing subagent — full release confirmed** — Sep 17 board
  confirms full release status across all tiers.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12832106502)

**Slack signals this week (unconfirmed — verify before telling clients):**
- Multiple ICs asked in #ask-vibe-ai whether Vibe apps can still be published
  publicly (no-login access). No confirmed answer in-thread — verify current
  public publishing status before promising it to clients.
- Vibe add-on pricing confirmed in channel: 10 apps = $100/mo, 25 apps =
  $250/mo. Enterprise 50+ seats cannot purchase the 10-app bucket (25-app
  minimum). AI credits add-on no longer grants free published app slots.

## 2026-08-31 to 2026-09-07

- **Vibe password protection for public apps — now live, not just "coming
  soon"** (Released, gradual rollout to demo accounts). Board logged it Sep 6
  as roadmap; a Sep 7 Slack post from the Vibe team confirmed it already
  shipped. One shared password per app (not per-user — per-user login planned
  later this year at additional cost), Growth tier only (25+ published apps),
  new left-pane apps only (existing apps/board views not yet supported).
  Sessions last 15 minutes. Kills the "who else can see this" objection on
  client demos. Source: Slack (https://monday.slack.com/archives/C094ZQJJ8GH/p1788764413056649)
- **Vibe app building now consumes AI credits** (Released) — each build
  prompt costs credits depending on model chosen; drafting is no longer free.
  The 25-app package only covers publishing quota, not build-time AI usage.
  Real cost-model shift — factor into Vibe scoping and Enterprise budget
  conversations, not just the publish quota.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12984613164)
- **Vibe Multiple Editors** (coming in 1-2 weeks per Vibe team, still
  unshipped) — currently only the app owner/creator can edit; adding someone
  as "owner" does not grant edit access yet. Set expectations accordingly
  until this lands.
  Source: Slack (https://monday.slack.com/archives/C094ZQJJ8GH/p1788192942962699)

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
