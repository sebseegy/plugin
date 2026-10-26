# monday-agents — confirmed release changelog

Dated log of confirmed Agent feature releases, newest entry first, fed
automatically by `weekly-pulse` each time it runs. Covers new agent capabilities,
trigger types, skill additions, org-sharing changes, and any confirmed bugs or
regressions that affect agent reliability. For platform incidents that cut across
all AI features, see `../monday-scaling-watch/references/changelog.md`.

## 2026-10-19 to 2026-10-26

All items below are board/Slack digests (grade C/D, unverified); confirm against the Release Board before promising.

- **Agent ownership transfer — released (admins, all tiers)** — Admin can reassign an agent when its builder leaves; no rebuild. Use in handover and governance answers.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13378639779); Release Board (https://monday.monday.com/boards/8084368131/pulses/13184172117)
- **Agent wait and resume — released** — Agents pause mid-task and resume later (follow-ups, reminders, watchdog patterns).
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13333622285)
- **Entity Retrieval sub-agent — UNVERIFIED-CONFLICT** — Board (25 Oct): Beta, 25% of users, heading to GA, ~5% task-completion gain in early evals. Slack #ai-agents-product-updates (20 Oct): "in GR/GA". Do not state GA until the Release Board confirms.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13378709497); Slack #ai-agents-product-updates (2026-10-20)
- **Standalone Brains — UNVERIFIED-CONFLICT** — Board status "Released", but text says available on account 5 (monday.monday.com) only; Slack and Google Drive sources planned. Treat as not GA. One brain, many agents; upload PDF/TXT/MD.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13343952326)
- **Workspace as agent context — GA** — 779 agents created with workspace context in week one (~2% of new agents). context.md launch mentioned; no in-product discovery yet.
  Source: Slack #ai-agents-product-updates (2026-10-22)
- **Interactive UI in chat — Beta (limited)** — Kanban, workload heatmaps, board item lists, daily briefings; 45+ components and canvas mode announced as next.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13333625840)
- **Dedicated Slack apps per agent — Beta, rolling out.**
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13333623381)
- **Suggestion Carousel — released, all tiers** — Board-open suggestions of relevant agents; helps adoption.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13382888531)
- **HubSpot tools for agents — released** — Search/update deals, contacts, companies, tickets; create tasks, notes, segments; human approval required.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13354734126)
- **Reliability** — Tool-request schema validation and smarter rate-limit rejections live; streamed thinking restored to 100% after a bug.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13378680340, https://monday.monday.com/boards/18411697232/pulses/13354738041)
- **Known bug (fix rolled out 25 Oct, post-check pending)** — `update_assets_on_item` reported success while the file column stayed empty; two Ignite flags at 100%.
  Source: Slack #ask-ai-agents (2026-10-25)
- **Not supported** — Dynamic per-item/per-board agent access is not supported and not on the roadmap (workspace-level access is the answer).
  Source: Slack #ask-ai-agents (2026-10-26)

## 2026-10-12 to 2026-10-19

- **Agent admin governance for sharing — released** — Admins control how agents are shared org-wide (approval flows, visibility). Extends the 22 Sep Org Directory work; treat as one governance story, not two features.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13323267895); CCO update (https://monday.monday.com/boards/9970212055/pulses/13320530381)
- **Agents can delete items and respect item viewing restrictions — released** — Previously create/update only. Agents now only access items they are allowed to see.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13323185596); CCO update (https://monday.monday.com/boards/9970212055/pulses/13320493607)
- **Builder UI changes** — Activity tab removed (chats + run history in one view); Brain tab renamed Profile; Instructions renamed Identity. Use the new names when guiding builds.
  Source: Slack #cco-enablement-updates (2026-10-19)
- **Knowledge controls** — Workspace-level knowledge context in one click (public boards/docs only; live on monday.monday, customer rollout from ~week of 19 Oct). Brain board item filtering (group, status, dropdown, tags, people, checkbox, text; auto re-sync). Brain Slack thread filtering by sender/text.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13179355973, https://monday.monday.com/boards/18411697232/pulses/13263116362, https://monday.monday.com/boards/18411697232/pulses/13285480379)
- **Channels** — Facebook Messenger live. Agent Phone v2 (outbound calls; old desktop voice removed) — Slack says phone beta is Israel and US only, so not usable for EMEA yet. Slack @mentions + rich formatting.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13297281776, https://monday.monday.com/boards/18411697232/pulses/13297283824); Slack #ai-agents-product-updates (2026-10-14/15)
- **External apps can send work to agents via API** (personal API token; external runs cannot change agent setup).
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13297282151)
- **Other** — Org-wide agent templates (save/remove); chat uploads up to 35MB PDF / 50MB files, 8 per message; DocuSign MCP available to agents.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13297279328, https://monday.monday.com/boards/18411697232/pulses/13297281550, https://monday.monday.com/boards/18411697232/pulses/13263091187)
- **⚠️ Unverified:** SharePoint/OneDrive for agents is logged "Released" on the board, but its source card is still "in progress" — confirm before promising. Google Drive has no triggers for agents (actions only); fallback is a scheduled agent job that checks for changes.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13225957279); Slack #ask-ai-agents (2026-10-19)
- **⚠️ Bug (active):** Agent CTA buttons can mismatch the reply text (reported 19 Oct, under investigation).
  Source: Slack #ask-ai-agents (2026-10-19)

## 2026-09-21 to 2026-09-28

- **HubSpot integration for AI Agents** (GA on monday AI Platform; broader product rollout TBC) — Agents can now connect to HubSpot as a tool: read/write contacts, companies, deals, sync pipeline stages, coordinate workflows across monday.com and HubSpot. Key AITP pitch: cross-system agentic automation for CRM clients running both tools.
  Source: Slack #cco-enablement-updates (2026-09-27, https://monday.monday.com/boards/9970212055/pulses/13143986867/posts/5581950345)
- **Agent Org Directory governance — Phase 2 (sensitive actions) shipping ~Oct 5** — Phase 1 (publish/require-approval controls) landed Sep 22. Phase 2 adds governance for sensitive agent configurations. Watch #ai-agents-product-updates for confirmation.
  Source: Slack #ai-agents-product-updates (2026-09-22, previously logged)
