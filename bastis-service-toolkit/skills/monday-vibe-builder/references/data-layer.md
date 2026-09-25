# Vibe data layer (verified 2026-09-24)

## Decision: boards vs Vibe DB vs hybrid
| Use boards when | Use Vibe DB when |
|---|---|
| Data needs automations, agents, dashboards, forms, mirrors, integrations | High-volume, app-owned data (entries, logs, votes, comments, sessions) |
| Other teams work the data natively in monday | Speed matters (>1–2k records, realtime) |
| Permissions must follow monday board permissions | App-level access is acceptable (no row-level security — filter by createdBy yourself) |
Hybrid reference (Amichay): master records on a board (projects), transactional
records in Vibe DB (time entries) linked by item ID.

## Boards
- Connected boards per app: 5 (10-app pkg) / 20 (Growth+). Left-pane apps only for
  >1 board; board/item views and widgets are single-board.
- Boards can come from other workspaces/products; put the app in the same workspace
  as its boards to avoid render/access issues.
- Speed: ~3s per 100 items/subitems read (1k ≈ 30s, 10k ≈ 6 min). Performance
  degrades with more boards/items before any hard limit.
- Page sizes: legacy path 100/page; new query-api path 500/page (behind flag, API
  2027-01); MCP-only path 2,000. Boards with files, time-tracking history, doc,
  item_assignees, progress, auto_number or linked-item columns fall back to the slow
  path — query fewer columns.
- Initial load stops ~500 items unless told to paginate. Bulk create capped at 200
  items per call.
- API quota: Vibe has its own per-minute quota; daily limit (25k on Enterprise)
  reportedly shared with other non-marketplace apps (partly unconfirmed). One client
  app hit ~90k calls in days — cache and aggregate.
- Supported: formula, mirror, connect-board columns, subitems, multi-level subitems
  (create 3rd/4th level), historical board aggregates, Notetaker data, file
  extraction (8 credits/file), account users/teams, current user.
- Not supported: rollups (calculate instead), formulas depending on mirrors,
  filtering by mirror in API, Capacity Manager data, portfolio project-board data
  (only what's mirrored onto the portfolio board).
- Subitems: at least one manually created subitem must exist for Vibe to discover
  the subitem board.
- Board editing subagent: Vibe can add/rename/delete columns, bulk-update items,
  create boards from CSV, delete boards — with an approval step before destructive
  actions. Via MCP this means a `vibe_update` can change client boards: say
  explicitly in the prompt when board structure must NOT be modified.
- Deleted connected board → other users redirected to it. Fix: disconnect it.
- Swapping boards: build on mock boards, then swap to live via Boards header (UI).

## Vibe DB (fullstack left-pane apps created since ~2026-08-26)
- Enable: prompt "use Vibe DB to store the data" or + → Integrations → Advanced →
  Create fast database (UI).
- One SQLite-backed Durable Object per app; schemaless collections; browser never
  talks to DB directly — server functions only; realtime via WebSocket invalidation.
- Limits: ~1M records; quota marketed 10 GB, code enforces 1 GiB; 256 KB max per
  record (no blobs/images); batch ≤500 ops; query limit 1,000 (default 100); `in`
  ≤30 values; 90 bound params; 20 indexes (extra silently skipped); 1,000 aggregate
  buckets; 100 concurrent WebSockets per app; broadcast ≤4 KB. "Dozens, not
  hundreds" of concurrent editors.
- Query: `== != < <= > >= in array-contains`, AND only (no OR/NOT), one orderBy,
  cursor pagination; `search()` = substring over JSON; aggregates count/sum/avg/
  min/max with one groupBy.
- Gotchas: **draft vs live data is disputed** — the Vibe PM (Amichay, #ask-vibe-ai
  2026-08-27) and Company Brain say draft and live share ONE database (so testing in
  the draft writes real data); the internal Vibe DB playbook says they're separate.
  Test it on the account before relying on either; for real dev/prod separation,
  duplicate the app or ask Vibe for separate dev/prod tables. Schema changes are
  additive only; a typo in a collection name silently creates a new collection;
  soft-delete retains 30 days; point-in-time restore 30 days; duplicating an app can
  copy data; builder "Data" tab to inspect/edit records.
- No file storage — use board file columns or external storage (e.g. Cloudinary)
  via API integration.
- No board↔Vibe DB sync. Custom sync only runs while the app is open, is slow for
  thousands of items, and needs explicit conflict/delete rules. Vibe automations RM.
  A board automation's API block can write to Vibe DB via GraphQL (`db_*`) but risks
  duplicates.
- Not exposed via MCP — request it in prompt text.

## Sizing heuristics for the brief
| Volume per app view | Approach |
|---|---|
| <300 items | Boards, no special handling |
| 300–1,000 | Boards + pagination + filter-before-query |
| 1,000–10,000 | Boards + cache + aggregation API + lazy tabs; or Vibe DB |
| >10,000 or realtime multi-user | Vibe DB (hybrid if automations needed) |
| >20 boards | Out of Vibe's range — consolidate boards, mirror onto fewer, or monday code |
