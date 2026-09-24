---
name: "monday-ai-changelog"
description: "Dated log of confirmed monday.com AI/Vibe/platform releases and incidents, built from weekly-pulse runs. Use this whenever Basti asks \"what shipped recently\", \"what's new with Vibe/Sidekick/Agents\", wants a quick baseline before explaining or pitching an AI feature, or wants to check whether a specific release (Vibe Plan Mode, Vibe Memory, Sidekick on Telegram/WhatsApp, AI blocks reading formula columns, etc.) has landed and what tier/status it's at. Also check this before answering monday-ai-advisor / monday-ai-suggester / monday-vibe / monday-scaling-watch style questions, since it holds the most recent confirmed findings pending a live Slack/board check."
---

# monday.com AI/platform changelog

A running, dated log of confirmed monday.com releases and incidents relevant to
Basti's work as an Enterprise EMEA Implementation Consultant and the Delivery
org's AI Champion. Entries come from `weekly-pulse` runs (which sweep the ICs
Product Updates board, Slack, and monday-all) or from ad-hoc findings Basti
asks to have recorded.

**How to use this:** treat every entry as *last known good*, not gospel — it
reflects what was confirmed as of the dated entry, not necessarily what's true
today. For anything stakes-sensitive (a client deliverable, a scoping
decision, a claim about current behavior), verify against support.monday.com
or Slack before repeating it as current fact. This log exists to save you from
re-deriving the same baseline every time, not to replace a fresh check when it
matters.

**How to add to this:** new entries go at the top, newest first, dated as a
range (e.g. "2026-08-24 to 2026-08-31") matching the weekly-pulse window they
came from. Keep the same grouping style (by product area) so entries stay
scannable over time. If an old entry is confirmed superseded or reversed, add
a short note next to it rather than deleting history — it's useful to see how
something evolved.

---

## 2026-08-24 to 2026-08-31

### Sidekick
- **Now reachable via Telegram and WhatsApp** (Released, gradual external
  rollout). Connect through a barcode on the Personalization page. Currently
  open to monday.monday, rolling to external users. Good differentiator pitch
  for field/mobile-first teams — no need to open the monday app.
  Source: Slack #ask-sidekick-ai (https://monday.slack.com/archives/C09MKR01006/p1787210037)

### Vibe
- **Connects to any external API** (Released, all tiers) — API token auth
  (GET/POST/PUT), pull data from Jira/Salesforce/Snowflake/etc. alongside
  board data. 1 credit per call. No OAuth support yet. Also enables
  **Bring-Your-Own-Model** — connect Gemini, Claude, or OpenAI as the app's
  underlying model.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12928960931), Slack #ask-vibe-ai (https://monday.slack.com/archives/C094ZQJJ8GH/p1787823804802649)
- **AI Plan Mode** (rolling out, monday.monday now) — toggle "Plan" in the
  prompt box; Vibe proposes app options, features, theme/design direction,
  and a visual flowchart before building anything. Good opener for scoping
  conversations with clients who aren't sure what to build.
  Source: Vibe Plan Mode FAQ (https://monday.monday.com/docs/18397954182)
- **Memory** (gradual release, full release targeted Aug 2026) — apps can now
  remember context/state across sessions instead of resetting each time.
  Reduces repetitive setup for client-facing apps.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12851077762)
- **Sketch Your App** (fully released) — draw or upload a sketch/wireframe/
  screenshot and Vibe generates a working app from it. Useful live in
  discovery calls when a client can't articulate requirements verbally.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12801273355)
- **Board Editing Subagent** (fully released) — Vibe can now edit *existing*
  boards (columns, views, automations) via natural language, not just
  generate new ones from scratch.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12832106502)
- **Open questions flagged in Slack, unconfirmed** — whether public Vibe apps
  require viewers to log into some monday account on mobile even when meant
  to be fully public; whether Contributor-level board permissions block item
  creation inside a Vibe app the way they do natively; pricing flexibility
  below the 25-app package minimum. Not resolved in-thread — verify current
  behavior before committing to an answer with a client.

### AI in Automations / Workflows
- **Formula columns now usable as AI block context** (Beta, limited access) —
  AI blocks in workflows/automations can now read formula column results,
  enabling automations that react to computed thresholds (e.g. a project
  health score or risk score), not just raw column data.
  Source: Slack #ask-ai-blocks (https://monday.slack.com/archives/C09PR4UAUDS/p1787666818583319)

### Agents
- No new capability releases this week. Slack traffic in #ask-ai-agents was
  mostly account-level support (enabling AI agents on an account, credit
  visibility per agent, reverting an agent's model version) rather than new
  features.

### Platform (non-AI, worth knowing)
- **BUG — two-way sync on connect-boards columns broken since Aug 25**
  (open as of this entry) — confirmed platform bug (HTTP 500 on every attempt
  to enable it), traced to a linkage microservice deploy that broke account
  ID resolution. Affects 204+ accounts across US/EU/AU. Fix requires the
  linkage team to roll back the deploy. If a client reports this, it's a
  known server-side issue, not user error — and any two-way sync configured
  after Aug 25 may have silently failed. Check current status before
  repeating this claim.
  Source: Slack #ask-boards (https://monday.slack.com/archives/C01141M8AAC/p1787741552900799)
- **Two automation bugs fixed Aug 25** (resolved, for contrast with the item
  above): the two-way sync settings panel was slow/unresponsive on boards
  with many automations (now fixed); automations were silently stopping on
  link fields with descriptive text but no valid URL (now fixed). Both live
  globally.
  Source: Slack (https://monday.slack.com/archives/C0BSMGV9GP7/p1787723142057639)
- **Data Over Time widget fully released** (Pro+/Enterprise) — dashboard
  widget for visualizing trends over time without exporting to Excel.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/12820382483)
- **CX Channel Health fully released** (monday Service) — visibility into
  support channel performance/bottlenecks.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/11888147089)
- **CRM Sequences show enrollment progress** — per-contact visibility into
  where each contact stands in a multi-step outreach sequence.
  Source: monday.com/whats-new

