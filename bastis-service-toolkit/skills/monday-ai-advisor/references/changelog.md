# monday-ai-advisor — confirmed release changelog

Dated log of confirmed AI feature releases, newest entry first, fed
automatically by `weekly-pulse` each time it runs. Check this before
explaining a feature so the explanation reflects current capability, not
just the static description in SKILL.md.

## 2026-09-17 to 2026-09-24

- **Agents on permission-restricted boards — limitation REMOVED (Sep 23)** —
  The "item not found" bug on boards with item-level view permissions is fixed.
  Update the "can agents work on sensitive boards?" explanation: yes, with the
  right setup (board owner = sees all; member = tagged items). Column view
  permissions also now supported. Previously had to caveat this heavily for
  Enterprise; that caveat is gone.
  Source: Slack (https://monday.slack.com/archives/C0AR4A570F8/p1790085385603429)
- **Enterprise Agent Org Directory — governance answer added** — Admin controls
  who can publish agents org-wide + require-approval flow. Update the Enterprise
  governance pitch: "build once, deploy org-wide" now has an admin approval
  layer so IT can stay in control. Phase 1 live Sep 22, Phase 2 (sensitive
  accounts) Oct 5. No longer roadmap — live.
  Source: Slack (https://monday.slack.com/archives/C0AR4A570F8/p1789573964699209)
- **Vibe — "who controls what goes live?" now has an answer** — "Request to
  publish" approval flow live: admins can lock publishing, builders request,
  admins approve/decline with one click. Update Enterprise Vibe governance
  framing accordingly.
  Source: Slack #ask-vibe-ai
- **⚠️ Sidekick limitation to flag — multiple Gmail accounts breaks email sends**
  — Active bug: only one Gmail account can be connected at a time. If a client
  plans to send from multiple addresses via Sidekick, that's currently blocked.
  Update the "Sidekick for email" explanation with this caveat until patched.
  Source: Slack (https://monday.slack.com/archives/C09MKR01006/p1789912642892649)
- **EWM Enterprise Reports — update Enterprise pitch** — Portfolio at Scale
  Phase 2 is now in beta (renamed EWM Enterprise Reports). GA Jan 2027.
  ~45 clients by Oct. For Enterprise clients asking "what's beyond the current
  portfolio dashboards?" — this is the answer, with a concrete timeline.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/11335680519)
- **Formula on mirror + connect board columns — now generally available (most
  regions)** — EU/AU/IL 100%, US 50%. Update any answer to "can I formula a
  mirrored column?" from "no, it's a workaround" to "yes, for most accounts."
  Source: Slack (https://monday.slack.com/archives/C08TEAL3RV0/p1789631398255699)

## 2026-09-14 to 2026-09-21

- **Agents — org-wide sharing + Org Directory (major Enterprise pitch update)**
  — Agents can now be shared with the entire org via an Org Agents Directory,
  with admin approval flows. Non-enterprise: live. Enterprise Phase 1
  (non-sensitive): live Sep 17. Enterprise Phase 2 (sensitive): rolling Oct 5.
  Build once, deploy org-wide — the story is now live, not roadmap. Shared
  members can trigger/chat with agents but cannot edit. Privacy review step
  when agents access private boards.
  Source: Slack (https://monday.slack.com/archives/C0BVCD6E01X/p1789573964699209)
  + monday board (https://monday.monday.com/boards/18411697232/pulses/13047529636)
- **Bug: AI Agents fail with item-level view permissions (Enterprise — active)**
  — Boards with item-level view permissions cause agent calls to throw "item not
  found" even when agent is board owner. No confirmed workaround. Cancels out
  two Enterprise differentiators simultaneously. Add to limitations framing for
  any Enterprise build combining both features.
  Source: Slack (https://monday.slack.com/archives/C08TDLN8F1P/p1789423875414219)
- **Agent billing bug resolved (Sep 12–15)** — Streaming engine bug charged
  running totals per turn. Rolled back. Costs down ~34%, failed sessions
  2.8% → 0.9%. If client questions credit burn from that window, it's resolved.
  Source: Slack (https://monday.slack.com/archives/C09R0JABFLH/p1789546103005419)
- **Agent Runner + Builder unified — new layout** — Single backend, centralized
  view (messages + actions + executions together). Update "how agents work"
  explanation: no more switching tabs to troubleshoot. Gradual rollout from Sep 20.
  Source: Slack (https://monday.slack.com/archives/C0AR4A570F8/p1789658859501239)
- **AI Workflows — "if text matches" condition block** — Multi-path branching
  from a text value in one block (no stacked yes/no). Released to all. Update
  AI Workflows explanation accordingly.
  Source: monday board (https://monday.monday.com/boards/183946105/pulses/13068746907)
- **CRM new agent experience → ~30K accounts** — Most CRM paying accounts now
  have the new UI. Enterprise + Lexi batch coming next weeks. Update demo flows.
  Source: Slack (https://monday.slack.com/archives/C0ATP5V1HD1/p1789627763237029)
- **monday MCP live on Google Gemini + full Workspace** — Actions work directly
  from Gmail, Sheets, Slides, Docs, and consumer Gemini. Update MCP/integrations
  explanation: it's now embedded in Google tools clients already use daily.
  Source: Slack (https://monday.slack.com/archives/C0AUP2SHTH7/p1789623103319309)
- **AI Credits one-time top-up — live globally** — Buy credits on demand without
  a plan change. Update commercial/pricing framing: running out mid-month is no
  longer a blocker or upgrade trigger.
  Source: Slack (https://monday.slack.com/archives/C0B9X0MQ6TU/p1789546381744349)
- **Vibe** — Stop Button (fully released), Memory (full release confirmed all
  tiers), AI Image Generation (100% global), duplicate+replace boards, external
  API calls confirmed. Full detail: `../monday-vibe/references/changelog.md`.

## 2026-08-31 to 2026-09-07

- **Vibe password protection** shipped this week (gradual rollout to demo
  accounts), earlier than the "coming in weeks" framing from Sep 6. Update the
  pitch: you can now tell clients it's available today (Growth tier, 25+
  published apps, new left-pane apps only), not just on the roadmap — one
  shared password per app, not per-user (per-user login is a later,
  paid add-on). Source: Slack (https://monday.slack.com/archives/C094ZQJJ8GH/p1788764413056649)
- **Vibe app building now costs AI credits**, not just publishing. Update the
  "how it works" explanation: the 25-app package covers publish quota only —
  building/drafting prompts draw from the AI credit pool depending on model
  chosen. Important when a client asks "is Vibe free to experiment with?" —
  answer is no longer an unqualified yes.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12984613164)
- **AI Workflows can now be built by chatting with Sidekick** (fully
  released, all tiers) — describe the goal in natural language and the
  system plans/configures/validates the workflow for publishing. Update the
  "how do I build a workflow" explanation: drag-and-drop is no longer the
  only entry point. Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965724886)
- **MCP OAuth Block reached full release** — AI Workflows can now
  authenticate to any OAuth-protected third-party app (previously token-auth
  only). Update the integration-capability explanation: OAuth-based services
  like Google and Salesforce connect natively now, no custom middleware
  needed. Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12943761290)
- **Org Agent Directory is live** — agents can be shared org-wide, not just
  used by their creator. Update the "how do agents scale across a team"
  explanation; Enterprise admin governance controls are still coming.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965734623)
- **AI Agents can now see sub-item data** when answering questions — update
  any explanation of agent limitations that still says agents only see
  top-level items. Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12984623213)
- **Data Set now scales to 10M items/board** (Enterprise, full release) and
  **Enterprise Reports** (5K boards / 5M items / <5s load) starts rolling out
  Jan 2027 — both change the answer to "how big can monday scale" for
  Enterprise pitches. Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965715652, https://monday.monday.com/boards/18411697232/pulses/12966069185)

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
