# monday-scaling-watch — recent platform incidents (non-limit)

Separate from `limits.md` and `scaling-themes.md` — this isn't a scaling
limit, it's a running log of transient platform bugs/incidents worth knowing
about for a short window after they happen, fed automatically by
`weekly-pulse` each time it runs, newest entry first. Entries here go stale
fast — check current status before repeating a claim from this file if it's
more than a few weeks old.

## 2026-09-17 to 2026-09-24

- **✅ RESOLVED (Sep 23): AI Agents item view permissions bug** — The bug that
  blocked agents on boards with item-level view permissions (causing ~11,900
  errors/week, flagged last two weeks) is fixed. Column view: full release.
  Item view: gradual rollout. No longer a blocker for Enterprise builds combining
  agents + item-level permissions.
  Source: Slack (https://monday.slack.com/archives/C0AR4A570F8/p1790085385603429)
- **✅ RESOLVED (Sep 24): Agent chat interface incident** — Active incident on
  agent chat Sep 23; fix deployed and confirmed working Sep 24. Short-lived,
  not affecting all accounts.
  Source: Slack #ask-ai-agents (Sep 23–24)
- **⚠️ Active bug: Sidekick email sends fail with multiple Gmail accounts** —
  Only one Gmail account can be connected at a time; >1 causes all email sends
  to fail with a generic error. No workaround beyond disconnecting extras.
  Source: Slack (https://monday.slack.com/archives/C09MKR01006/p1789912642892649)

## 2026-09-14 to 2026-09-21

- **⚠️ Active bug: AI Agents fail with item-level view permissions (Enterprise)**
  — Boards with item-level view permissions cause agent calls to throw "item not
  found" even when the agent is made a board owner. Affects Enterprise accounts
  using both item-level permissions and AI agents — the two features cancel each
  other out. No confirmed workaround as of Sep 15. Flag before any Enterprise
  build combining both.
  Source: Slack (https://monday.slack.com/archives/C08TDLN8F1P/p1789423875414219)
- **Resolved: Agent platform billing bug (Sep 12–15)** — Streaming engine bug
  charged each turn the session's running total instead of just that turn.
  Engine rolled back Sep 15–16. Post-fix: cost per session down ~34%, failed
  sessions 2.8% → 0.9%, budget exhaustion 24% → 17%. If a client reports
  unexpected credit burn from Sep 12–15, it's a known resolved issue.
  Source: Slack (https://monday.slack.com/archives/C09R0JABFLH/p1789546103005419)

## 2026-08-31 to 2026-09-07

- **Notetaker hard-deletes recordings when the source calendar event is
  deleted/cancelled** — confirmed bug, open. Affects 300+ accounts; the
  meeting record (recording, transcript, summary) is permanently deleted, and
  the user sees a misleading "no permission" error instead of being told the
  data is gone. Advise clients not to delete/cancel calendar events after a
  meeting has been recorded until this is fixed — the data cannot be
  recovered. Source: Slack (https://monday.slack.com/archives/C097L5D5WES/p1788445616845229)
- **AI Agent Activity Tab not logging recent runs** — confirmed bug, open.
  Root cause is the new per-tool execution path (run-agent-per-tool-activities
  rollout), which doesn't publish a "running" row to the Activity tab. Agent
  runs are still happening normally — only the tab's logging is broken. If a
  client says their agent "looks dead," check outputs (board changes, sent
  emails, etc.) before assuming an outage.
  Source: Slack (https://monday.slack.com/archives/C0A8K7NDS8L/p1788268809905069)
- **Can't select a specific status label in "create subitem" automations** —
  confirmed bug, open. Only a dynamic value is selectable for the subitem's
  status column, so automations meant to create subitems with a fixed status
  (e.g. "Working on it") are currently broken; fix in progress. Workaround:
  set status manually after creation.
  Source: Slack (https://monday.slack.com/archives/CJBRAUSKT/p1788353753749669)
- **Timeline date picker broken and resolved (same day)** — was
  unresponsive and could silently remove existing timeline dates; declared
  and fixed same day (Sep 4). For contrast with the open bugs above: if a
  client mentioned this specifically in the last few days, it should now be
  resolved — worth a quick follow-up to confirm, and to check whether any
  dates were lost while it was broken.
  Source: Slack (https://monday.slack.com/archives/CJBRAUSKT/p1788441275762379)

## 2026-08-24 to 2026-08-31

- **Two-way sync on connect-boards columns broken since Aug 25** — confirmed
  platform bug (HTTP 500 on every attempt to enable it), traced to a linkage
  microservice deploy that broke account ID resolution. Affects 204+ accounts
  across US/EU/AU as of report time; fix requires the linkage team to roll
  back the deploy. If a client reports this, it's a known server-side issue,
  not something to troubleshoot on their end — and any two-way sync
  configured after Aug 25 may have silently failed.
  Source: Slack (https://monday.slack.com/archives/C01141M8AAC/p1787741552900799)
- **Two automation bugs fixed Aug 25** (for contrast — these are resolved,
  not open): two-way sync settings panel was slow to open on boards with many
  automations (now fixed); automations were silently stopping on link fields
  with descriptive text but no valid URL (now fixed). Both live globally.
  Source: Slack (https://monday.slack.com/archives/C0BSMGV9GP7/p1787723142057639)
