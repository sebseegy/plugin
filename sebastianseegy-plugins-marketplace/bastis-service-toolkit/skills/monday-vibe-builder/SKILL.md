---
name: monday-vibe-builder
description: "Build monday vibe apps END-TO-END through the monday MCP (vibe_create, vibe_update, vibe_get, vibe_ask, vibe_publication, vibe_list, vibe_rename) — variant selection, board prep, sequenced build prompts, async polling, QA, publish and client handover. Use whenever Claude should actually build, extend, fix, speed up, rebuild or publish a Vibe app rather than just hand over a prompt: 'build the vibe for [client]', 'create a vibe app via MCP', 'spin up a vibe portal', 'make this vibe public', 'our vibe app is slow / missing items', 'rebuild this board-view vibe as a full app', 'duplicate this vibe for another client', or any client use case where a custom monday app is the answer and the MCP is connected. Also use when scoping or estimating a Vibe build for a client (variant, package tier, credits, effort), since the same platform constraints drive the plan. Prefer this over monday-vibe (which only writes a paste-ready prompt) whenever the monday MCP Vibe tools are available. Not the Vibe React design system."
---

# monday vibe builder (via MCP)

You are building a production Vibe app for an Enterprise client on behalf of an
Implementation Consultant. The MCP gives you full lifecycle control, but it is
**prompt-only**: `vibe_create`/`vibe_update` send a chat message to the Vibe
builder exactly like the UI does. You cannot read or edit code, and you cannot
see the rendered app. Every build prompt consumes the target account's AI credits.
World-class output therefore comes from three things: getting the architecture
right *before* the first prompt, sequencing small verifiable prompts, and using
`vibe_ask` + board data to QA what you can't see.

Platform facts move weekly. Figures below were verified 2026-09-24 against
#ask-vibe-ai, #vibe-mcp, the monday.monday Vibe FAQ / release board and
support.monday.com. Before stating a limit, price or release status to a client,
skim `../monday-vibe/references/changelog.md` (fed weekly by weekly-pulse) and, if
it's stakes-sensitive, re-check Slack #ask-vibe-ai. Trust human Vibe team answers
(Amichay Even Chen — PM, Omer Pessach — MCP owner, Yoni Braslaver, Waseem Abu Leil)
over the in-channel "vibe support bot", which is often wrong.

## Reference files — read when the phase needs them

| File | Read it when |
|---|---|
| `references/platform-facts.md` | Any claim about limits, tiers, pricing, credits, access, release status |
| `references/prompt-playbook.md` | Writing the prompt sequence; proven fix/perf prompts; anti-patterns |
| `references/data-layer.md` | Choosing boards vs Vibe DB, >500 items, subitems, files, sync |
| `references/troubleshooting.md` | Anything fails, stalls, errors, shows wrong/missing data |
| `references/delivery-playbook.md` | Scoping effort, dev→prod, client handover, credit exemptions |

## Non-negotiable guardrails

These exist because the actions are billable, client-visible, or irreversible.

1. **Confirm the account first.** Two or more monday connectors may be loaded
   (e.g. monday.monday internal vs a demo/trial vs the client). Call
   `get_user_context` on the connector you'll use and state the account name back.
   Building on the wrong account burns the wrong credits and puts client IP in the
   wrong tenant. monday.monday cannot host public apps and doesn't meter credits —
   demo accounts are for demos, client accounts for delivery.
2. **Approval gate before the first `vibe_create`.** Show the build brief (variant,
   boards, workspace, prompt sequence, model per prompt, credit estimate) and wait
   for an explicit yes. Subsequent `vibe_update`s within the approved plan can
   proceed; anything outside the plan needs a new yes.
3. **Approval gate before `vibe_publication`.** Publishing consumes a paid app slot
   and exposes the app to users (or the internet). State who will see it and what
   data it exposes. Never publish public on the user's behalf without an explicit
   "yes, publish public".
4. **Never `vibe_delete`** unless the user names the app and says delete. Deleted
   apps are not restorable.
5. **Never contact the client.** Draft handover notes; the IC sends them.

## Workflow

```
0 Ground → 1 Brief & architecture → 2 Board prep → [GATE] → 3 Create → 4 Poll
→ 5 QA → 6 Iterate (loop 4–6) → 7 Harden → [GATE] → 8 Publish → 9 Handover
```

### Phase 0 — Ground

- `get_user_context` → confirm account, tier, user. Note if Enterprise (permissions
  gate who can create/publish).
- `vibe_list` (search_term = client/app name) → avoid building a duplicate; find the
  app to extend.
- If extending an existing app: `vibe_get` with `include: {messages: {limit: 30}}`
  to read the build history — it's the only view you have of what Vibe did.

### Phase 1 — Brief & architecture

Extract (from the conversation, discovery notes, or by asking — one question at a
time, only for what's missing): the problem, users and their seat types, data
sources and volumes, screens and actions, who must see it (internal / guests /
external), mobile needs, brand, and deadline.

Then decide these five things. Each is a common failure point.

**a) Variant** — the most consequential choice, because only some surfaces get
new capabilities and you cannot convert between them later.

| Need | Variant | Why |
|---|---|---|
| Multi-board app, portal, anything that may ever be public, password-protected, use Vibe DB, call APIs or be templated | `object_fullstack` (default) | Only variant with server functions; every new capability lands here. `object` now maps to fullstack on accounts that have it |
| Lens on ONE board, lives as a board view tab, never public | `board_view` | Single host board; no public/password/Vibe DB |
| Per-item UI on the item page (quote, intake detail) | `vibe_item_view` (try first) or `item_view` | Single board. The difference between the two is undocumented — if one errors, try the other and note the result |
| Richer widget inside a board's dashboard view | `vibe_dashboard_widget` | One board only; needs `view_id` + its `board_id`; board-view dashboards only, not full dashboards |
| Campaigns-surface app | `monday_campaigns` | Built for the Campaigns SDK; needs the Campaigns context; treat as experimental |

If `object_fullstack` returns `SERVER_GENERATION_DISABLED` (403), the account
lacks server generation — tell the user what they lose (public, Vibe DB, API)
before falling back to `object`.

**b) Package tier fit** — boards per app: 5 on the 10-app package, 20 on Growth
(25-app). Cannot be raised. Public apps, password protection and (upcoming) viewer
read-only access are Growth-only. Enterprise with 50+ seats must buy Growth
anyway. If the design needs >5 boards or external access, flag the Growth
requirement now, not at publish time.

**c) Access model** — the app runs with the *viewing* user's permissions. Viewers
cannot open Vibe apps at all today (read-only for Growth expected ~end Oct 2026,
unconfirmed). Guests work if invited to the app AND every connected board. Public
apps have no user identity (one shared password at most) and — as of 2026-09-24 —
public fullstack apps have an open bug where all server-side writes fail 403. If
outsiders only need to *submit* data (intake, uploads), a WorkForm feeding the
boards + an internal Vibe app is usually the stronger design today. For large
unlicensed populations see the options table in `platform-facts.md` (incl. the
upcoming "External Users for Vibe").

**d) Data layer** — boards when the data needs automations, agents, dashboards,
forms or mirrors; Vibe DB (fullstack only) for high-volume app-owned data. Board
reads run ~3s per 100 items and initial loads stop around 500 unless told to
paginate. Rollup columns and formula-on-mirror are not readable. Details and the
hybrid pattern: `references/data-layer.md`.

**e) Workspace** — pass `workspace_id` = the workspace holding the boards.
Otherwise object apps land in the builder's personal `<userId>-vibes` workspace,
and apps in a different workspace from their boards can fail to render for others.

### Phase 2 — Board prep (before any Vibe prompt)

Board structure *is* the app architecture — column titles, types and groups drive
what Vibe renders. Use the monday MCP (and `monday-solution-architecture` for
non-trivial schemas) to:

- Create or validate boards with clear column titles and correct types
  (status/date/people/numbers — not text for everything).
- Seed realistic sample data (10–30 items) so Vibe has something to reason about;
  if subitems matter, create at least one subitem manually — Vibe only discovers
  the subitem board once one exists.
- Replace rollups with values Vibe can calculate from subitems; avoid formulas that
  depend on mirror columns.
- For client delivery, prefer: build against sandbox/mock boards → swap to live
  boards later (Boards header) or duplicate-and-connect.

### ⛔ GATE 1 — build brief

Present, compactly: account · variant · workspace · board_ids (names + IDs) · data
layer · access model + tier requirement · the numbered prompt sequence with model per
prompt · credit estimate (see below) · known risks. Wait for explicit approval.

Credit estimate: Flash ~10–20, Sonnet ~30–50, Opus ~50–500+ per prompt; a
medium app is typically ~2,000 credits over 20+ prompts. Failed prompts are free;
stopped prompts are charged up to the stop. If the IC is building on a client
account, remind them of the BigBrain "Internal AI Build" exemption
(`delivery-playbook.md`) so the client's credits aren't burned.

### Phase 3 — Create

```
vibe_create(
  prompt      = <Prompt 0 — shell only, see playbook>,
  variant     = <from 1a>,
  board_ids   = [<ids>],          # connect via param — NEVER paste IDs/schemas in prompt text
  workspace_id= <from 1e>,
  view_id     = <dashboard widgets only>,
  model       = <omit for auto, or CLAUDE_5_SONNET for the shell>
)
```

Immediately give the user the returned `editor_link` so they can watch generation
live. Never hand the raw `*.mondayvibe.app` deployment URL to a client.

Pasting board IDs or column schemas into the prompt is unsupported: it hard-codes
logic, degrades performance and breaks duplication, ownership transfer and making
the app public. The `board_ids` param is the only correct way.

### Phase 4 — Poll

Generation is async with no progress signal. Poll `vibe_get` (status defaults on):

- First check ~60s after the call, then every ~30–45s. Typical builds take a few
  minutes; complex Opus builds longer.
- Proceed only when `is_busy` is false and status is `ready`.
- Never send `vibe_update` while busy — it returns `APP_BUSY` (409).
- If status is stuck (no change for ~10 min) or a deploy error appears, stop
  polling, report status + editor_link, and follow `troubleshooting.md`. Don't
  retry blindly — the 2026-09-09 incident showed retry/rollback failing the same way.

### Phase 5 — QA (you can't see the app, so interrogate it)

After each meaningful step:

1. `vibe_get` with `include: {messages: {limit: 5}}` → read Vibe's own summary of
   what it built, auto-fix notes, and any questions it asked. If Vibe asked a
   question, answer it in the next `vibe_update`.
2. `vibe_ask` (read-only — changes no code; credit cost not documented, assume it
   uses some) with targeted checks:
   - "List every page/screen, which boards and column IDs each reads or writes."
   - "What is the logic you use for querying, filtering and paginating data? What
     is the max number of items you load?"
   - "Which columns do you reference by position instead of ID?"
   - "What happens for a user who can't see board X?"
3. Cross-check data: read the same board via the monday MCP and compare counts/
   fields against what `vibe_ask` says the app shows.
4. Ask the IC for a 60-second visual pass via `editor_link` on anything
   layout/brand-related — state exactly what to look at.

### Phase 6 — Iterate

One change per `vibe_update`, then poll and QA again. Pick the model per prompt:
Flash for copy/colour tweaks, Sonnet for features, Opus for multi-page work,
performance, persistent bugs and rebuilds. If two fixes fail, revert-and-rethink
(see troubleshooting) rather than stacking patches. The full prompt sequence
template, design-direction block and proven prompts are in
`references/prompt-playbook.md`.

### Phase 7 — Harden before anyone else uses it

Run these as explicit prompts/asks where relevant (details in playbook):
pagination beyond 500 items · caching for 1,000+ items · column IDs not positions ·
behaviour for users with partial board access · empty/error/loading states ·
mobile layout if field users · no hard-coded user IDs · noon-local dates ·
dark/light theme tokens · confirm-before-write on production data.

### ⛔ GATE 2 — publish

State: publish scope (account vs public link), who will see it, what data is
exposed, the app-slot it consumes, and — for public — the open write bug and
"anyone with the link" reality. Wait for explicit approval, then
`vibe_publication(app_id, "publish")`. Publishing requires the app to be deployed
and within the account's published-app quota. For dev/prod, recommend turning Auto
Update off after first publish (UI) so builder edits don't hit live users.
Public link + password are set in the UI publish menu (not exposed via MCP).

### Phase 8–9 — Handover

Produce a build record (save to the project's `deliverables/` if one exists):
app name/ID, editor link, variant, boards + workspace, access model, prompt log
(prompt → model → outcome), known limitations, credit spend estimate, and next-step
recommendations. Then point to `monday-build-docs` for client-facing documentation.
Ownership transfer to the client and adding client editors happen in the UI.

## Commands for other lifecycle asks

- **Extend/fix an existing app** → Phase 0 history read, then Phase 5 QA to locate
  the issue, then Phase 6.
- **Rename** → `vibe_rename` (no gate needed; tell the user).
- **"Make this public" on a board view / item view / widget / old app** → cannot be
  converted or duplicated into eligibility. Rebuild as a new `object_fullstack` app:
  ask the IC to copy the code from the builder, paste it into Prompt 0 of a new app,
  build on Opus (multi-page apps: one page per prompt). Gate 1 applies.
- **Duplicate for another client / board set** → UI only (Duplicate → connect new
  boards, or public template link cross-account). Explain the steps.
- **Connect/disconnect boards on an existing app** → not an MCP tool yet; UI Boards
  header or ask in a `vibe_update`.

## When to hand off instead

- Paste-ready prompt only, no MCP → `monday-vibe`.
- Board schema design → `monday-solution-architecture`; formulas → `monday-formulas`.
- Automations/workflows the app should trigger (Vibe cannot create automations —
  it writes to a board and a board automation fires) → `monday-workflow-architect`.
- Effort/SOW → `monday-scoping` (with the Vibe effort benchmarks from
  `delivery-playbook.md`).
- Client docs → `monday-build-docs`.
