# monday-workflow-architect — confirmed release changelog

Dated log of confirmed Workflow Builder and Automations releases, newest entry
first, fed automatically by `weekly-pulse` each time it runs. Covers new
workflow blocks (condition, action, AI, delay, HTTP/MCP), changes to trigger
types, new automation recipes, changes to automation limits or caps, and
confirmed bugs or regressions in workflow execution.

## 2026-10-20 to 2026-10-23

- **Resolved: "revisit limitations" flag from 12-19 Oct.** Webhook-in (Get Webhook Data / "When a webhook is received") is a Workflow Builder item; it does **not** change the classic-Automation limits. The Workflow Builder claim that changed is the trigger list: **"When person assigned" is now listed** (planner, grade A, 2026-10-23). One root trigger / one board per workflow re-confirmed.
  Source: invoke_process_planner (2026-10-23); see `blocks-catalog.md`
- **Blocks confirmed by the planner:** webhook trigger, manual trigger, Categorize with AI + if text matches, Code, HTTP request, Run any MCP action, Wait for duration, loop pair, email send-and-wait (Gmail/Outlook; no Slack).
  Source: invoke_process_planner (2026-10-23)
- **New MCP tools not in the skill before:** run_workflow_once, get_workflow_run_once_status, stop_workflow_run_once, get_run_once_trigger_entities, get_workflow_editor_link. Behaviour of the run-once tools unverified.
  Source: monday MCP tool list (2026-10-23)
- **Field reports (grade D, mostly unanswered):** archive of trigger item deactivates the workflow; Find Matching Item column bug; code-block intermittent failures; Chat-to-Build condition with phantom cases; SharePoint/OneDrive/Salesforce-search block instability; Platform API 2026-10 may break the builder's mention picker. Detail in `limits-and-failure-modes.md`.
  Source: Slack #ask-ai-workflows (https://monday.slack.com/archives/C050HR7DV46), 7-23 Oct
- **Developer release notes 2026-10 (page modified 2026-10-13):** no Workflow Builder entries. Relevant API items: `board_automations` query + `delete_board_automation`, activity-log `triggering_flow_id`/`triggering_flow_type`, AI column mutations, `run_prompt`.
  Source: https://developer.monday.com/api-reference/docs/release-notes#2026-10

## 2026-10-12 to 2026-10-19

- **Get Webhook Data block — released** — External systems can trigger AI workflows via webhook. Revisit the "no data beyond trigger" and "smaller trigger catalog" limitations in SKILL.md (verify before editing).
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13319899275)
- **Categorize with AI block — released, all tiers** — classify text and route to downstream branches.
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13319899553)
- **Block search by intent — fully released, all tiers.**
  Source: board (https://monday.monday.com/boards/18411697232/pulses/13285518619)
- **Single-user draft experience — live on account 5 only** — one user/one tab can edit a workflow at a time. Not yet confirmed for customers.
  Source: Slack #ai-workflow-group (2026-10-18)
