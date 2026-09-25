# monday-ai-suggester — confirmed release changelog

Dated log of confirmed AI feature releases, newest entry first, fed
automatically by `weekly-pulse` each time it runs. This skill still pulls
fresh data every time it runs (Step 2 in SKILL.md) — this log is a
quick-start baseline, not a replacement for that pull.

## 2026-09-17 to 2026-09-24

**Agents**
- **Item view + column view permissions — FIXED (Sep 23)** — Resolves the bug
  flagged last week. Column view: full release. Item view: gradual rollout.
  ~11,900 blocked runs/week eliminated. Agent as board owner = sees all items;
  as member = tagged items only.
  Source: Slack #ai-agents-product-updates (https://monday.slack.com/archives/C0AR4A570F8/p1790085385603429)
- Enterprise Agent Org Directory governance: admin controls for who can publish
  to the org directory, require-approval flow. Phase 1 (non-sensitive) Sep 22,
  Phase 2 (sensitive) Oct 5.
  Source: Slack #ai-agents-product-updates (https://monday.slack.com/archives/C0AR4A570F8/p1789573964699209)
- Agent audit log: 11 agent lifecycle events (create/edit/delete/activate)
  now in Enterprise Audit Log, queryable via `custom_agents` on dev API.
  Source: Slack #ask-ai-agents RanDow thread (Sep 24)
- **⚠️ Incident (resolved):** Agent chat interface down Sep 23; fix deployed
  and confirmed Sep 24.

**Sidekick**
- **⚠️ Bug (active): Email sends fail when multiple Gmail accounts connected.**
  No sender picker; generic error. Workaround: one Gmail account only until fix.
  Source: Slack (https://monday.slack.com/archives/C09MKR01006/p1789912642892649)

**Vibe**
- "Request to publish" approval flow live (admin-controls publishing).
  See `../monday-vibe/references/changelog.md` for detail.

**AI in Automations**
- Outlook Human-in-the-Loop block available — matches Gmail HitL (internal
  only, not yet client-facing). Slack + WhatsApp HitL planned next.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/13123555706)

**Enterprise / Scale**
- EWM Enterprise Reports beta open (~45 clients by Oct, GA Jan 2027).
  Advanced portfolio reporting beyond current dashboards.
  Source: monday board (https://monday.monday.com/boards/8084368131/pulses/11335680519)

## 2026-09-14 to 2026-09-21

**Agents**
- Org Agents Directory live for non-enterprise; Enterprise Phase 1 (non-sensitive)
  live Sep 17, Phase 2 (sensitive) rolling Oct 5. Build once, share org-wide
  with admin approval. Source: Slack (https://monday.slack.com/archives/C0BVCD6E01X/p1789573964699209)
- Agent Runner + Builder unified; new centralized layout. Gradual rollout Sep 20.
  Source: Slack (https://monday.slack.com/archives/C0AR4A570F8/p1789658859501239)
- CRM new agent experience expanded to ~30K paying accounts. Enterprise batch next.
  Source: Slack (https://monday.slack.com/archives/C0ATP5V1HD1/p1789627763237029)
- **⚠️ Bug (active):** Agents fail with "item not found" on boards with item-level
  view permissions, even when agent is board owner. Enterprise accounts. No workaround.
  Source: Slack (https://monday.slack.com/archives/C08TDLN8F1P/p1789423875414219)
- Agent billing bug resolved: Sep 12–15 overcharge fixed. Sessions back to normal.
  Source: Slack (https://monday.slack.com/archives/C09R0JABFLH/p1789546103005419)

**Vibe**
- Stop Button — fully released, all tiers.
- Memory — full release confirmed all tiers.
- AI Image Generation — 100% global (US/EU/AU/IL). ~<10 credits per image.
- Duplicate + replace boards — fully released, all tiers.
- External API calls — confirmed fully released, all tiers.
- See `../monday-vibe/references/changelog.md` for full detail and sources.

**AI in Automations**
- "if text matches" condition block released to all — multi-path routing in one
  block, no stacked yes/no conditions.
  Source: monday board (https://monday.monday.com/boards/183946105/pulses/13068746907)

**General AI / Commercial**
- AI Credits one-time top-up live globally (non-US first, US following).
  Source: Slack (https://monday.slack.com/archives/C0B9X0MQ6TU/p1789546381744349)
- monday MCP live on Google Gemini (consumer + Workspace) and all Google apps.
  Source: Slack (https://monday.slack.com/archives/C0AUP2SHTH7/p1789623103319309)

## 2026-08-31 to 2026-09-07

**Agents**
- Sub-item retrieval now works — agents can finally see and reason over
  sub-item data (previously invisible to them). Relevant for any client demo
  with parent/sub-item structures (CRM activities, task breakdowns, tickets).
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12984623213)
- Org Agent Directory is live — agents shareable org-wide instead of stuck on
  one person's account; rolling to non-Enterprise accounts this week,
  Enterprise admin controls (permissions/approval) coming soon. Good
  governance answer for Enterprise prospects worried about agent sprawl.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965734623)
- "Unified Engine" backend consolidation (setup + run merged into one system)
  rolling out to customers this week — no visible UX change expected, but a
  likely explanation if a client reports subtly different agent responses.
  Source: Slack (https://monday.slack.com/archives/C0A8K7NDS8L/p1788254617784019)

**Sidekick**
- No new feature releases this week — Telegram/WhatsApp access (logged last
  week) is still the latest.

**Vibe**
- Password protection for public apps is now live (not just roadmap), app
  building now consumes AI credits, and multi-editor support is still 1-2
  weeks out. See `../monday-vibe/references/changelog.md` for full detail and
  sources.

**AI in Automations**
- AI Workflows Chat-to-Build via Sidekick — fully released, all tiers.
  Describe a workflow goal in natural language; Sidekick/MCP plans,
  configures, and validates it. Strong AITP demo for non-technical
  stakeholders. Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965724886)
- MCP OAuth Block for AI Workflows — full release. Workflows can now
  authenticate to any OAuth-protected third-party app (Google, Salesforce,
  etc.), not just token-auth services. Opens native-integration demos for
  security-conscious Enterprise clients on SSO stacks.
  Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12943761290)
- AI Workflow Manual Trigger and Workflows Code Block also reached full
  release this week (on-demand triggering; custom code inside workflows for
  edge cases). Source: monday board (https://monday.monday.com/boards/18411697232/pulses/12965763141, https://monday.monday.com/boards/18411697232/pulses/12965763065)

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
