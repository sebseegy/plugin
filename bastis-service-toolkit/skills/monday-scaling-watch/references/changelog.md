# monday-scaling-watch — recent platform incidents (non-limit)

Separate from `limits.md` and `scaling-themes.md` — this isn't a scaling
limit, it's a running log of transient platform bugs/incidents worth knowing
about for a short window after they happen, fed automatically by
`weekly-pulse` each time it runs, newest entry first. Entries here go stale
fast — check current status before repeating a claim from this file if it's
more than a few weeks old.

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
