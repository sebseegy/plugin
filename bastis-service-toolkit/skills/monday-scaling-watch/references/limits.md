# monday.com hard limits (baseline snapshot)

**Snapshot date: 2026-06-02.** Source: monday CX Guru card "Is there a limit?"
(Boards Core FAQs). Most values below are durable. Lines marked **(moves)** are
tied to mondayDB scale and should be re-verified in Slack before quoting in a
client deliverable — see `scaling-themes.md`.

> Even when no single hard limit is hit, a *combination* of soft limits can
> degrade board/dashboard performance well before a hard cap. See monday's
> "Board Performance Guidance" card.

## Items, subitems, connections

- **Items per board (moves):** 10,000 on non-ENT plans; **100,000** on CRM Pro
  and all ENT plans (via mondayDB 2.0 scale). Cumulative across items + subitems.
  Archived items don't count; only active items do. On Free, subitems don't count.
  At the limit, the owner is notified and new items are blocked.
- **Subitems per item:** 500. (A process to lower to 100 was never enforced.)
- **Item connections in a board (moves):** 10k (excluding subitems) on all plans
  except ENT; separate 10k limit at subitem level. **100k** (including subitems +
  dependencies) via mondayDB 2.0 scale.
- **Connected items per individual cell:** 750.
- **MLS / multi-level subitem project board:** 5,000 items.

## Connected / linked boards

- **Linked boards in one Connect Boards column, by tier:** Free 1, Basic 1,
  Standard 5, Trial/Pro 20, ENT 60.
- **Linked boards per board (total), by tier:** Basic 5, Standard 20, Pro 100,
  ENT 200. ENT 200 is a hard cap — cannot be exceeded regardless of column count.
  The same board connected via multiple columns counts each time.
- **Connect board columns per board:** 60 (all tiers, cannot increase).

## Columns, groups, views

- **Columns per board:** 500. Undocumented backend grace mechanism exists (inject
  hidden "junk" columns to push higher, e.g. to 600) — but active column count
  must stay above 500 or the cap re-engages. Engineering-only workaround.
- **Groups per board:** no limit.
- **Items per group:** no limit, BUT cannot move groups >10k items+subitems
  between boards, and cannot delete groups >10k items+subitems (batch-delete 500
  at a time to get under).
- **Views per board:** 100.
- **Status labels per column:** fixed, cannot increase.
- **Dropdown options:** 1,000 per column; 20,000 per board.

## Text / character limits

- **Item name:** 255 chars. **Group name:** 255 chars. **Board description:** 1,000.
- **Long text column:** 2,000 chars (cannot increase). **Text column:** no limit.
- **Update:** 46,000 chars. **Updates per item:** 1,000. **Replies per update:** 500.
- **Formula builder:** 10,000 chars.

## Subscribers / ownership / teams

- **Direct subscribers per board:** up to 400 users (incl. guests). Prefer
  subscribing Teams (governs/scales better).
- **Teams per board:** up to 100. **Boards a team can subscribe to:** 13k.
  **Boards a user can subscribe to:** 13k.
- **Boards a single user can own:** 10,000.
- **Teams per account:** 6,000. **Workspaces per account:** no limit.
- **Archived boards:** no limit.

## Files / storage

- **Files per board:** 20,000 (cannot increase). **Max file size:** 500 MB.
- **File storage by tier (not currently enforced):** Basic 5 GB, Standard 20 GB,
  Pro 100 GB, ENT 1,000 GB. Archived items count; recycle-bin items count until
  truly deleted.

## Batch / volume / 24h

- **Batch action:** 500 items at once; 500 subitems (200 for convert-to-item).
- **Items created per account / 24h:** 500,000.

## Excel import / export

- **Import (non-CRM):** up to 100 columns × 8,000 rows. **CRM import:** 100
  columns × 10,000 rows. Board-from-scratch import takes only first 50 columns.
- **Export:** 10,000 items + 10,000 connected items (incl. ENT). TSE can raise to
  a max of 40k — route increase requests to TSE.
- **Skip/overwrite on import** not always available — see mondayDB 2.0 known
  limitation in `scaling-themes.md`.

## Dashboards

- **Widgets per dashboard:** 30 (excluding text widgets).
- **Connect boards per dashboard, by tier:** Free 1, Basic 1, Standard 5, Pro 20,
  ENT 50. (Pricing page says Pro 10 for sales reasons; actual is 20.)
- **Items per dashboard (moves):** 20,000 (all plans, and ENT not yet on mondayDB
  2.0 scale).
- **Linked boards per dashboard:** 1,000 (distinct from connected boards;
  tier-independent).
- **Items in reporting widgets (Chart/Battery/Numbers):** Pro 200,000; ENT 500,000.

## Portfolio (moves)

- **Portfolios per account:** ENT unlimited; legacy Pro 20.
- **Connected projects per portfolio:** ENT 200; legacy Pro 20.
- **Total connected items per portfolio:** 20,000 across all projects; **750 per
  individual project board** (can hit the per-project 750 before the 20k total).

## Activity log, search, forms, workflow

- **Activity log:** 10,000 items; Excel export max 10,000 (column-value changes
  only).
- **Board search "all columns":** 50 columns; TSE can grant 100 or 200 textual
  search (only after validating the use case).
- **Form questions:** as many as columns allowed by plan.
- **People per person column:** no limit unless set in settings.
- **Workflow builder:** 1,000 delayed actions running at once per workflow; **200
  blocks per workflow** (introduced March 2026).
