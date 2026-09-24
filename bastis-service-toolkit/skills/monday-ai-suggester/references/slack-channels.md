# Slack channel reference (single source of truth)

Shared by `monday-ai-suggester` and `monday-discovery` (build-ideas mode). When the
channel list changes, update this file only.

> These channel names are a starting baseline drawn from team usage. Verify they
> exist in the current Slack workspace; if a channel errors or is renamed, note it
> in "Sources pulled" and continue — never block the whole run on one channel.

## Tier 1 — AI feature channels (read recent messages in full)

Use `Slack:slack_read_channel` (limit ~100, last 30 days) on these — they carry the
highest-signal AI release news:

- `#cco-enablement-updates` — official enablement announcements (releases, betas, limit changes)
- `#ask-ai-workflows` — AI workflow blocks and capabilities
- `#ask-ai-agents` — agents / digital workforce
- `#ask-vibe-ai` — monday vibe

## Tier 2 — product channels (search with AI keywords)

Use `Slack:slack_search_public_and_private`, scoped per channel, query shape:
`Sidekick OR Agent OR Vibe OR "Magic AI" OR MCP OR Notetaker in:#channel-name`

- `#ask-boards`, `#ask-dashboards-widgets`, `#ask-work-management`,
  `#ask-monday-db`, `#ask-projects`

## Tier 3 — IC / team channels (search for build inspiration)

- `#emea-services`, and your regional services / IC channels

## Modes

- **AI feature research** (monday-ai-suggester): run Tier 1 in full + Tier 2/3
  keyword search. Look for announcements (🎉, "now live", "GA", "beta"), new
  capabilities, plan-tier info, limitations other consultants flagged, and use
  cases others built. Skip user troubleshooting unless it reveals a feature/limit.
- **General build inspiration** (monday-discovery build-ideas): search Tier 3 +
  relevant product channels for comparable client builds; cite the channel and
  person only if actually found — never fabricate.

Run channel queries in parallel where possible. If a pull fails or is empty, record
it in "Sources pulled" and proceed with what you have.
