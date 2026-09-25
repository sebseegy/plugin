# Vibe prompt playbook (for MCP builds)

## Contents
1. Principles · 2. The prompt sequence · 3. Prompt 0 template · 4. Feature prompt
template · 5. Design direction block · 6. Proven prompts (perf, data, fixes,
features) · 7. Anti-patterns · 8. Worked example sequence

## 1. Principles — why small prompts win
- Vibe regenerates code per prompt. Big multi-feature prompts produce collapsed or
  half-implemented work that costs more to fix than to build. One change per prompt,
  verify, continue. A good app takes 20+ prompts.
- Keep each prompt under ~350 words. Plain language, concrete nouns (board names,
  column titles, exact labels).
- Describe *behaviour and data*, not code. Vibe owns implementation.
- Name boards by their monday names ("the 'Supplier Onboarding' board") — the
  connection itself happens via `board_ids`.
- Workflows as "When X happens, do Y".
- Put the persona first: who uses this screen and what they're trying to get done.
- If Vibe asks a clarifying question (visible in `vibe_get` messages), answer it
  before doing anything else.

## 2. The prompt sequence (plan this at Gate 1)
| # | Purpose | Model |
|---|---|---|
| 0 | App shell: purpose, users, nav/pages, design direction, data sources — "Do NOT create any new boards" | Sonnet (Opus if ≥4 pages) |
| 1 | Core screen 1 — read path (list/table/cards) with filters + pagination | Sonnet |
| 2 | Core screen 1 — write path (create/edit), confirm-before-write | Sonnet |
| 3…n | One screen or one feature per prompt | Sonnet |
| n+1 | Integrations/tools (email, export, Vibe DB, API) — one per prompt | Sonnet/Opus |
| n+2 | Hardening pass (see §6 hardening) | Opus |
| n+3 | Polish: copy, empty states, microcopy, colour tweaks | Flash |
| n+4 | Help overlay / onboarding tips | Flash/Sonnet |

For multi-role apps, build one role's journey end-to-end before the next.

## 3. Prompt 0 template (vibe_create)
```
Build me a [app type] for [client/team] that [core purpose in one sentence].

Users: [roles and what each needs to accomplish; seat type if relevant].

Data: Use the connected boards. [Board A] holds [what]; key columns: [titles].
[Board B] holds [what]. Do NOT create any new boards. Reference columns by
their column IDs, never by position.

Pages (build the shell and navigation only for now; each page gets its own URL):
1. [Page] — [one line]
2. [Page] — [one line]
Show a clear placeholder on pages not built yet.

[Design direction block — §5]

For now build only the shell, navigation, and the [Page 1] layout with real data
from [Board A]. We'll add the other pages one by one.
```

## 4. Feature prompt template (vibe_update)
```
On the [Page] page, add [feature].
Who uses it: [role] — they need to [goal].
Behaviour: [When X, do Y]. [Filters/sorting/validation rules.]
Data: read [columns] from [Board]; write [column] on [Board]. Ask me to confirm
before writing to [Board].
Keep everything else unchanged.
```
"Keep everything else unchanged" matters — it reduces collateral rewrites.

## 5. Design direction block (never ship the generic default look)
Theme to the client's brand; absent one, to the industry standard for the app type.
```
Design: [light | dark] theme using semantic theme tokens (bg/fg/border, not raw
white/gray) so light and dark both work. Primary [hex], accent [hex], neutrals
[hex/hex]. Typography: [font or "clean geometric sans-serif"], clear heading
hierarchy. Style: [e.g. spacious enterprise SaaS, 8px grid, rounded-lg cards,
subtle shadows, data-dense tables with sticky headers]. Optimised for
[desktop | mobile-first]. Inspired by [reference app/site].
Keep charts simple; no heavy animations.
```
Industry defaults when no brand is given:
- Client/supplier portal → calm neutral base, one brand accent, generous whitespace,
  clear status pills (Stripe/Linear-like).
- Ops/field app → mobile-first, large tap targets, high contrast, bottom nav.
- Exec dashboard → dark or light slate, KPI tiles top, one chart per insight.
- Retail/luxury (e.g. Selfridges) → editorial typography, restrained palette,
  lots of white space.
Brand reuse: account-level Memory (admins, set in the builder: "Remember our brand
colours are…, logo is…") applies to every future app. Theme-from-URL and design
gallery are UI-only — mention them to the IC as an option.

## 6. Proven prompts (copy-paste; Amichay/Vibe team endorsed unless noted)

**Performance**
- "Help me make this app work faster, explain the tradeoffs." (on Opus — best first move)
- "Cache board data in local storage."
- "Use the aggregation API for statistics."
- "Load only the first 20 items, then more on scroll."
- "Filter items before querying." / "Query fewer columns."
- "Load other pages in the background once the main page is loaded." (slow multi-page nav)
- "Add a short delay between item pages." (per-minute rate limits)
- "Don't stop after 500 items, get all items in the board." (bot tip; pair with pagination)

**Missing / wrong data** (Opus)
- "What is the logic you are using for querying and filtering data?" (ask via
  `vibe_ask` first — cheapest diagnosis)
- "I don't see all the items and subitems from [Board], for example [item] is
  missing [field]. Please troubleshoot and add console logs showing item counts."
- Multi-level boards: "[Board] uses multi-level subitems. Rollups aren't readable —
  calculate [metric] from the subitem values." (bot tip: add `capabilities:
  [CALCULATED]` to calculated-column queries)

**Stuck / regressions**
- Revert via undo on the last good prompt (UI — ask IC), then: "You already tried
  fixing it multiple times, try another approach." + "Add troubleshooting logs." on
  Opus. If still broken: rebuild that page fresh.

**Vibe DB**
- "Use Vibe DB to store [entity]. Keep [other entity] on the [Board] board and link
  each [entity] record to its [board item]." (time-tracking reference pattern)
- "Create separate dev and prod tables in Vibe DB." (Whether draft and live share
  one DB is disputed — test before relying on it.)

**Files to a file column (fullstack)** — Vibe eng pattern: "Read files with
.withAssets(), not .withColumns(). To upload: use the presigned create_upload →
PUT to storage → complete_upload flow, then change_column_value with added_file.
Never JSON-stringify a File object."

**Exports** — "Add an 'Export PDF' button: light theme regardless of app theme,
page breaks between sections, logo top-left." (logo embedding fixed Sep 2026 for
new left-pane apps).

**Email** — "When [action], send an email via Outlook to [column/person] with
[content]." (1 credit per email; low volume only; Vibe will prompt to connect the
account — IC does that in the UI.)

**API integration** — "Connect to the [Service] API using an API key (docs: [URL]).
GET [endpoint] and show [fields] on [Page]. Add troubleshooting logs." Key entry
happens in the UI; warn that app users inherit whatever the key can access.

**Hardening pass** (one Opus prompt, or split if it fails)
```
Review the whole app and harden it:
- paginate all board reads (no 500-item ceiling) and cache boards over 1,000 items;
- reference columns by ID, never by position;
- no hard-coded user IDs — use the current user;
- graceful states for loading, empty, errors, and users without access to a board;
- treat dates as noon local time;
- confirm before any write to production boards;
- make every page responsive down to mobile width.
Explain what you changed.
```

## 7. Anti-patterns
- Pasting board IDs or column schemas into prompt text (unsupported; hard-codes
  logic; breaks duplicate/transfer/public). Use `board_ids`.
- Pre-creating empty boards for Vibe when you intend Vibe to provision them — either
  omit `board_ids` (Vibe auto-creates) or connect real, populated boards.
- Pressuring the AI to "find a way" around a permission limit → it hallucinates.
- Duplicating an old app to gain public/password/Vibe DB — doesn't work; rebuild.
- Stacking fix on fix after two failures — revert and change approach.
- Asking for automations — Vibe can't create them; have it write to a board and let
  a board automation fire.
- Very long prompts via MCP (e.g. pasting large multi-page code) can fail on create —
  split into one page per prompt.
- Promising pixel-level results without a human visual check — you can't see the app.

## 8. Worked example — supplier onboarding portal (object_fullstack, 3 boards)
0. Shell: 4 pages (Dashboard, Suppliers, Documents, Approvals), brand tokens, no
   new boards, build Dashboard layout only. (Sonnet)
1. Suppliers list: table from 'Suppliers' with status filter, search, pagination 25/page. (Sonnet)
2. Supplier detail drawer: fields + linked documents from 'Supplier Docs'. (Sonnet)
3. New-supplier form writing to 'Suppliers', confirm-before-write, validation. (Sonnet)
4. Approvals page: items where Status = 'Pending review', Approve/Reject buttons
   writing status + approver (triggers existing board automation). (Sonnet)
5. Dashboard KPIs via aggregation API: counts by status, avg days to approve. (Sonnet)
6. Hardening pass. (Opus)
7. Microcopy, empty states, help overlay. (Flash)
QA after every step via `vibe_get` messages + `vibe_ask` + board counts.
