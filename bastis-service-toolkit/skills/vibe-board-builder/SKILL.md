---
name: "vibe-board-builder"
description: "Architects the full backend for any monday.com Vibe app AND generates the production-ready Vibe prompt to build the UI. Use this skill whenever someone asks to \"set up Vibe boards\", \"build a Vibe app\", \"create a Vibe app structure\", \"scaffold a monday.com Vibe\", \"I need boards for a Vibe\", \"set up my Vibe for [project/event/portal]\", \"write a Vibe prompt\", \"generate a Vibe prompt\", or any variation on creating the data backend OR the UI prompt for a monday.com Vibe app. Also triggers when Basti is preparing a Vibe for a client and needs either the board foundation built, sample data populated, or the Vibe builder prompt crafted. Handles the complete end-to-end workflow: discover → architecture → boards → sample data → SDK file → Vibe prompt → delivery. For change prompts on an app that already exists, or evaluating Vibe's replies, use vibe-prompt-injection instead."
---


# Vibe Board Builder — Full Stack

Complete 7-step workflow for a **new** app: boards backend + sample data + SDK + first Vibe prompt, plus public-app publishing and authentication guidance. Once the app exists and you're iterating on it (change prompts, reading Vibe's replies, fixing bugs), switch to the `vibe-prompt-injection` skill.

Facts in this skill were last verified against monday.com's internal mondayall knowledge base, the internal "Vibe DB vs. monday Boards" builder guide (drop-62ff9c42-315.monday-vibe.workers.dev, dated 2026-08-19), and official support docs on 2026-08-21, and cross-checked against live #ask-vibe-ai channel messages spanning 2026-08-12 through 2026-08-21. Production lessons were added from the Wren Kitchens Contracts portal and WHSmith Portfolio Command builds (through 2026-09-23). Vibe changes fast — if something here looks stale or contradicts what you observe live, re-verify via the mondayall knowledge base (`knowledge_search` / `knowledge_get_article`), the drop-page builder guide, or the #ask-vibe-ai Slack channel before trusting this file over direct observation.

---

## Platform essentials (read before designing)

Full detail, dates and sources: [references/platform-facts.md](references/platform-facts.md). Read the
relevant section there before asserting a capability to a client.

- **Board ceiling** — plan for **5** connected boards as the safe default. The support
  best-practices article (modified 2026-09-22) says "up to twenty boards at a time"; internal
  packaging lists 5 by default and 20 on Vibe Growth or Custom/Enterprise. Verify per account
  before relying on more than 5.
- **Vibe DB** — private per-app document store; doesn't count against the board ceiling; no
  automation/dashboard surface. Decision order: platform-facts → "Vibe DB vs. monday Boards".
- **Query cap** — board reads return ~500 (sometimes 200) items per query; paginate, filter
  server-side where possible, or use Vibe DB.
- **External APIs** — supported via the API Requests integration (API-token auth only, no
  OAuth, GET/POST/PUT, 1 credit per call and per page). Email via Gmail/Outlook.
- **No background jobs** — apps run only while open. Nothing on a board can call into the app —
  see "Board → app signalling" in platform-facts.
- **Access** — board permissions are the floor and the app cannot elevate them. Viewer seats
  can't open Vibe apps. Public apps have no per-user layer. Private-app access and deep links:
  platform-facts → "Private app access and entry points".
- **Memory** — Vibe saves App Memory on its own during builds; audit it after rule changes.
  Memory holds instructions, never data.
- **Credits** — build/edit prompts charge by complexity and chosen model (observed 35–454 per
  prompt), failed ones too; in-app AI actions ~8 credits per run.
- **Plan mode** — the "Plan" toggle proposes features, design and a flowchart before building;
  Discuss mode is now described internally as limited/unreliable.
- **No version control / staging** — duplicate the app before risky changes.

## 7-Step Workflow

### Step 1 — Discover

Ask (or infer from context):
- **App type** — event site, portal, knowledge hub, product catalog, quiz/game, tracker, etc.
- **Main entities/content types** — sessions, resources, products, questions, players...
- **Project name / naming prefix** — e.g. "Sales Kickoff 2026", "WHSmith Portal"
- **Workspace** — call `get_user_context` to find the active workspace, or ask if ambiguous
- **Audience & roles** — who uses the app and what can each role do? If any audience is external
  (no monday account), flag early that you'll need the Public Vibe Apps path and a homegrown
  auth pattern (platform-facts → Public Vibe Apps) — this materially changes the architecture,
  not just the publish step. If any audience is internal-but-Viewer-license, flag that too — Vibe
  apps are blocked for Viewer seats regardless of publish status. If any external audience is
  expected to use mobile, flag the guest-desktop-only limitation too.
- **Role gates and entry points (internal apps)** — if roles see different things (e.g.
  management approves, PMs only enter their own project), identify the **people column** that
  grants access per record and check it's actually populated — it becomes the only grant. Decide
  how each role enters: full app, **item view** (scopes itself to the item, no URL needed), or a
  per-record link. Private apps strip query parameters, so per-record links must carry the key in
  the route path (platform-facts → Private app access and entry points).
- **Record identity** — what exact key joins records across boards (project code, site ID)?
  Every join must be exact-match on that key; flag duplicates or missing keys now.
- **Right tool per requirement** — Vibe is the app layer only. "When X happens, create/link
  items across boards" belongs in a monday workflow; board audits and data fixes in Sidekick.
  Don't design Vibe screens for provisioning.
- **Dynamic vs static** — does the app need real-time updates (scores, status)?
- **Bootstrapping source** — is there an existing spreadsheet/CSV that should seed a board
  instead of hand-authoring sample data? If so, plan to import it directly (platform-facts →
  Recently shipped capabilities) rather
  than manually recreating its structure.
- **Board vs. Vibe DB for each entity** — for every entity identified, run it through the
  decision order in platform-facts → "Vibe DB vs. monday Boards" before defaulting it onto a board.
- **Expected data volume per board** — if any entity will exceed a few hundred items, flag the
  500/200-per-query pagination cap now, not after the build hits it.

Propose a strawman board architecture immediately. Don't wait for perfect information.

---

### Step 2 — Propose Architecture

Match to a pattern in [references/architecture-patterns.md](references/architecture-patterns.md)
(A–F). Present each board with its purpose, key columns, and groups
before creating anything. Confirm naming prefix and structure with the user. Call out separately
which entities, if any, are going into Vibe DB instead of a board, and why.

**5-board consolidation rules** (when entity count exceeds limit for a full-page/OBJECT_FULLSTACK app):
- Move genuinely app-internal data (settings, caches, session state, ephemeral tokens) to Vibe DB instead of a 6th board
- Merge live + historical state into one board (use a Status column to distinguish)
- Combine related small entities (e.g. FAQ rows on the general board as a group)
- Use subitems for nested entities instead of a separate board

---

### Step 3 — Create Boards in Sequence

All boards in the same workspace. Create in order; capture board IDs as you go.

For each board:
- `workspace_id`: confirmed in Step 1
- `board_kind`: `public` (unless specified otherwise)
- Pass status labels and dropdown options **explicitly** — defaults will not match
- Create every column the app needs **here**, via MCP (or Sidekick in accounts you can't reach),
  not by asking Vibe later — then read the schema back so Step 5 uses real IDs
- Keep dropdown labels clean from day one: one concept per column (e.g. customers, not a mix
  of customers and sites), spelled correctly — the app will group and filter on them

**Status column settings JSON:**
```json
{ "labels": { "0": "Label A", "1": "Label B", "2": "Label C" } }
```

**Dropdown column settings JSON:**
```json
{ "labels": [{ "id": 1, "name": "Option 1" }, { "id": 2, "name": "Option 2" }] }
```

After all boards are created, output a summary table:

| Board | ID | URL |
|---|---|---|
| [Prefix] - general | xxxxxxx | https://monday.monday.com/boards/xxxxxxx |

---

### Step 4 — Populate Sample Data

Use `create_item` to add 5–10 realistic items per board — or, if the user has a source
spreadsheet, import it directly as a CSV/XLSX inside the Vibe builder instead of hand-authoring
items (faster and avoids transcription drift, subject to the 5,000-row import cap). Rules
for hand-authored data:
- Data must be domain-specific — no "Item 1", "Test", lorem ipsum
- Cover varied states: multiple status values, different groups, some with files/links missing
- For event apps: include realistic speaker names, session titles, dates in correct format
- For quiz apps: include 10–15 questions across at least 3 difficulty levels
- For product catalogs: include varied categories, prices, statuses

This data serves two purposes: (1) validates the board schema works, (2) gives Vibe's AI
meaningful context when generating the UI.

---

### Step 5 — Generate SDK File

Produce a JavaScript constants file that maps every logical field to its **board ID + column ID
+ expected type**. This is the app's single column map: Vibe-generated code must resolve columns
through it, by ID, and treat titles as display metadata only.

Why (production, Wren): Vibe defaulted to matching columns by exact title. Renaming one column
("#Kitchen Specs") turned into a false blocker across a whole site, and two spellings of one field
(`worktopPrivate` vs `worktopsPrivate`) made fully stocked lists read as empty. The fix was
exactly this map plus a type-checking resolver.

**Format:**
```javascript
// [App Name] — Vibe column map
// Generated: [date]
// Boards: [N] | Workspace: [workspace_id]
// Resolve by columnId + type. Titles are display only; never match by title.

export const [BoardName]Board = {
  boardId: XXXXXXX,
  columns: {
    name:            { id: "name",      type: "name" },
    description:     { id: "long_text", type: "long_text" },
    type:            { id: "status",    type: "status" },   // "Virtual" | "In-person" | "Hybrid"
    speakerOne:      { id: "text0",     type: "text" },
    speakerOneImage: { id: "files",     type: "file" },
    date:            { id: "text1",     type: "text" },     // display string e.g. "Apr 28, 2026"
    site:            { id: "status1",   type: "status" },   // "Tel Aviv" | "Global" | "London" | ...
    subitems:        { id: "subitems",  type: "subtasks" },
  }
};

// Helper functions
export const getActiveItems = (items) =>
  items.filter(i => i.column_values.find(c => c.id === "status")?.text === "Active");

export const getItemsByGroup = (items, groupTitle) =>
  items.filter(i => i.group?.title === groupTitle);
```

Naming conventions:
- PascalCase for board exports: `SessionsBoard`, `ResourcesBoard`
- camelCase for column keys: `speakerOneImage` not `speaker_one_image`
- One spelling per logical field, exported once and imported everywhere
- Inline comments for status label options and column semantics
- Only IDs read back from the live API go in the map; anything unconfirmed is an explicit TODO,
  never a guess

---

### Step 6 — Craft the Vibe Prompt

Write a production-ready prompt for the Vibe app builder. This is the most important
deliverable — it must be detailed, technical, and complete. A weak prompt produces a
generic UI; a strong prompt produces a finished product.

Before drafting, check whether Vibe Memory (platform-facts → Vibe Memory) already holds the client's brand
colors/logo/tone or the builder's standing preferences — if so, don't re-state them; reference
that they're already set instead.

**Vibe Prompt Template:**

```
## App Overview
[1–2 sentences: what the app is, who uses it, what it does]

## Core Features
### Navigation & Layout
- [Primary nav structure]
- [Key views/pages]

### [Feature Category 1]
- [Specific UI behaviour]
- [Filtering/sorting logic]

### [Feature Category 2]
...

## User Roles
- **[Role]**: [What they can see and do]

## Data Sources
Board data comes from monday.com boards; app-internal data (if any) lives in Vibe DB. Use the
following board and column IDs exactly, and list Vibe DB collections separately.

**[BoardName] Board** (ID: XXXXXXX)
- `name` → [what it represents]
- `long_text` → [what it represents]
- `status` → filter values: "[Label A]", "[Label B]", "[Label C]"
- `files` → [hero image / thumbnail / gallery]
- Example query: fetch items where status = "Active", sort by name
- Expected volume: [N items] — [note pagination strategy if > ~300]

**[BoardName2] Board** (ID: XXXXXXX)
...

**Vibe DB collection: [name]** *(if used)*
- Fields: [list]
- Why it's here and not a board: [one line — settings/cache/session/etc.]

## UI/UX Requirements
- Layout: [grid / list / card deck / table]
- Color palette: [primary, accent, background, text]
- Typography: [font family, heading scale]
- Responsive: [mobile-first / desktop-first]
- Empty states: [what to show when no data]

## Real-Time / Dynamic Behaviour
- Poll [BoardName] every [3–5] seconds for [field]
- Show live [score / status / count] in [component]

## Technical Notes
- Put all board/column IDs in ONE column map module (from the provided SDK file) and import it
  everywhere — no IDs scattered through components
- Resolve every column by board ID + column ID and check its type. Titles are display only; a
  renamed column must still resolve. Never substitute a column with a similar title. A missing ID
  or wrong type fails closed, naming board ID, expected column ID, expected type and what was found
- Read status/dropdown labels live from the resolved column's settings; never hard-code label indexes
- Join records across boards by exact [key, e.g. project code] — never contains/includes, fuzzy
  names or hardcoded lists. Zero matches → clear message; two or more → refuse, don't pick the first
- Blank values are not a category — exclude them from totals and show a notice, don't default them
- Writes: send only fields that changed, re-read after writing, and only then show success. Report
  "saved but not verified" honestly. Never clear stored data based on an inferred value
- Permissions [if roles differ]: enforce on the server for every read and write; hiding UI is not
  security. [Role] may only [actions] on records where they're named in [people column]
- Pagination: "load more" keeps the same filter and columns as the first page; no silent caps
- Error handling: show [fallback UI] if board fetch fails; timeouts name the board and offer Retry
- Loading states: skeleton screens for [component]; never print a verdict ("not found", "empty")
  before the read that decides it has answered
- Caching: cache board data for [N] seconds before re-fetching; cache may paint the screen but
  never approves a save
- Diagnostics [production apps]: an admin-only screen showing per-step timings and the column
  map resolution, since server logs can't be read back

## Design Style
- Visual reference: [describe aesthetic — clean corporate / vibrant game UI / minimal portal]
- Card design: [shadow / border / hover state]
- Status indicators: colour mapping for each label
- Accessibility: WCAG AA contrast, keyboard nav on all interactive elements

## Success Criteria
- [ ] All [N] boards connected and rendering data
- [ ] Filtering by [key dimension] works correctly
- [ ] [Dynamic feature] updates without page reload
- [ ] Mobile layout renders without horizontal scroll
- [ ] Empty and error states handled gracefully
```

**Prompt quality rules:**
- Connect the boards via the UI Boards panel **first**. Then include exact board and column IDs
  (from Step 3) in Data Sources as the column map Vibe must resolve against — the IDs document
  connected boards, they never substitute for connecting them
- Specify status label strings verbatim, including client typos (e.g. "Call Off Recieved")
- Describe UI behaviour, not just data structure
- Add a concrete example query for each board (what to fetch, how to filter)
- State rules, not just features ("a project is identified by its exact code") — rules survive
  later prompts
- Say what NOT to build (no extra screens, no nav items beyond the list) — Vibe adds scope when
  it isn't fenced
- Length: 800–2000 words for this first build. Every later change is a short, single-job prompt —
  use the `vibe-prompt-injection` skill for those.

---

### Step 7 — Deliver Package

Present in this order:
1. **Board summary table** — names, IDs, URLs
2. **SDK file** — in a code block, ready to copy
3. **Vibe prompt** — in a code block, ready to paste into Vibe builder
4. **Next steps** — "Open Vibe builder → New App → Connect these boards → Paste the prompt"

If the app needs public/external access: add a step covering the account-level admin toggle
(not settable via API — the user must do this themselves in Administration), and note that if
the app already existed before the toggle was enabled, it must be rebuilt, not just republished.

If roles need per-record entry, add: test links in a private window as a non-admin user before
sharing them, and fill the access people column on every record first.

Then hand over to the `vibe-prompt-injection` skill for everything after the first build:
reading Vibe's reply, verifying what landed, and writing the follow-up prompts.

---

## Verification discipline (learned the hard way)

Vibe's own chat replies are not reliable self-reports. Observed failure modes in production:

- A completion message claiming a feature works can be wrong even when the code trace requested
  in the same conversation is accurate — always ask for an actual code trace against concrete
  test cases ("what happens when X is entered") rather than accepting a description of intended
  behavior.
- Every `vibe_ask` reply ends with a fixed footer ("turn off Discuss mode and hit Build...")
  regardless of whether anything was actually built or is still just discussed — this is UI
  boilerplate, not a signal either way. If you need to know whether code is actually live, ask a
  direct yes/no question ("is this actually deployed right now, BUILT or NOT BUILT") and look for
  corroborating specific detail (references to other real, previously-built parts of the app) —
  don't infer state from the footer text.
- **Discuss mode is a genuine, separate platform toggle in the Vibe editor UI** (not just a footer
  string) — when it's on, `vibe_ask`/`vibe_update` calls will only produce conversational/planning
  output and never write code, even when the instruction explicitly says "build this now." If
  repeated build-intent prompts produce no code changes, check whether the app is stuck in Discuss
  mode before assuming the prompt wording is the problem. As of 2026-09 Discuss mode is described
  internally as limited/unreliable; for "plan before building" use **Plan mode** instead, and for
  code questions send a Build prompt that says "Read-only. Change nothing. Report…".
- **"undo this"** in the chat reverts the last edit — try it before writing a corrective prompt
  when a change simply went wrong.
- Before re-asking Vibe to build something, check whether it was already built earlier in the
  same conversation — Vibe itself has been observed re-verifying its own prior work on disk rather
  than assuming, and finding the work already done. Don't skip that same check yourself.
- Re-verify security/access-control logic with fresh, concrete test cases after every change,
  not just once at the start — a later unrelated prompt can silently regress earlier guarantees.
- **Vibe's own self-diagnosis on failure is sometimes just "infrastructure-related, not a code
  problem"** with no further detail (observed live, 2026-08-18) — a genuinely unhelpful dead end
  that still consumes credits on the retry. Don't treat that message as diagnostic; escalate or
  try a materially different prompt/approach rather than repeatedly retrying the identical one.
- **A recurring CORS failure pattern has been independently reported by two unrelated
  builders** (2026-08-13 and 2026-08-19): preflight failures between the app's CDN origin
  (`*.cdn2.monday.app`) and its server-function domain (`*.usv2.monday.app`) block real board-data
  fetches, silently falling back to demo/placeholder data instead of erroring loudly. If a
  published app appears to be showing plausible-but-wrong data, check the network tab for CORS
  errors on these specific domain patterns before assuming it's a logic bug in the prompt.
- There is no version control or staging environment — treat "duplicate the whole
  app before a risky change" as a mandatory verification step, not an optional nicety, since
  there's no other way back to a known-good state if a change regresses something.
- **"Oops, something went wrong" mid-build means the change may be half-applied** (seen on
  both Wren and WHSmith). Send nothing else until a read-only prompt has reported what actually
  landed and whether the app builds.
- **Vibe deviates from prompts on purpose and says so** ("that's my deviation"). Judge each
  deviation explicitly; several were right. It also **adds scope nobody asked for** — a
  temporary inspection screen, a narrowed access grant (WHSmith Sponsors lost access). Check
  every reply for new routes, nav items, board reads or permission changes.
- **"Saved to memory" lines persist rules in App Memory.** WHSmith's memory still held retired
  rules weeks later. Audit App Memory after any business-rule change.
- **Queued prompts that edit the same files collide.** Queue only independent prompts.
- **The code export is the source of truth.** When Basti downloads the app source, review it
  against the requirements — that's how the `contains` joins, dropped pagination filters and
  blank-as-External totals were found on WHSmith, none of which Vibe reported.

---

## Architecture patterns

Patterns A–F (event, knowledge hub, catalog, quiz, custom, role-based internal ops) with board
layouts and production examples: [references/architecture-patterns.md](references/architecture-patterns.md).

## Column Type Reference

| Use case | Type | Notes |
|---|---|---|
| Headlines / titles | name | One per board (required) |
| Body copy, rich text | long_text | Renders as formatted text blocks |
| Short labels, metadata | text | Speaker names, subtitles |
| Display dates (no logic) | text | e.g. "Apr 28, 2026" |
| Date logic / sorting | date | Use when Vibe needs to sort or filter |
| Category / stage / type | status | Labels become filter tags |
| Multi-select classification | dropdown | Enables filtering and grouping |
| Photos, images, banners | file | Galleries, hero images, thumbnails |
| Videos | file | Separate column from photos |
| External links, CTAs | link | Renders as clickable buttons |
| Authors, owners, POCs | people | Profile cards with avatars |
| Scores, quantities, rankings | numbers | Numeric display and sorting |
| Nested tasks / variants | subtasks | Auto-creates linked subitem board |

**Status label rule:** Always semantic and human-readable. "Virtual" not "Option 1".
The Vibe filter UI displays label text verbatim — it's user-facing copy.

---

## What NOT to Do

- Single board for everything — Vibe requires separate boards per entity
- Placeholder column names ("Column 1") — Vibe uses titles to understand the data, and users see them
- Let Vibe resolve columns by title — resolve by board ID + column ID + type via one column map
- Omit status/dropdown labels — filter UI depends on exact label strings
- Boards in different workspaces — cross-workspace Vibe apps break
- Skip subitem board for sessions — task tracking widget breaks
- Swap `text` ↔ `long_text` — they render differently in Vibe
- Wrong column order in sessions board — Subitems must precede Site
- Date column for display dates — use `text` type
- Scatter board/column IDs through the app's code — they live in one column map module
- Vague Vibe prompt ("make it look good") — specify layout, colours, filter logic, empty states
- Assume a public app has any access control by default — it doesn't; build it yourself
- Assume a Viewer-license user can access any Vibe app, public or not — they can't, by design
- Assume a guest can view a public app on mobile — desktop-only, confirmed
- Trust a Vibe completion message about security/access logic without an independent code trace
- Trust a generic "infrastructure-related" failure message as an actual diagnosis — it's often a
  dead end that still burns credits on repeated identical retries
- Assume "5 boards" or "20 boards" applies universally — check which app type and tier you're
  actually building on before you plan the architecture around either number
- Paste raw board IDs into prompt text instead of connecting boards via the UI — Vibe may parse
  the IDs as instructions rather than a data source
- Mirror board data into Vibe DB "for convenience" — read it live via the Board SDK instead
  (a sanctioned one-time migration is fine; ongoing dual-write mirroring is not)
- Put app-internal plumbing (settings, session state, ephemeral tokens) on a board by default
  without first checking whether it belongs in Vibe DB instead
- Design a Vibe-DB-backed automation trigger — it doesn't exist; automations only see boards
- Assume an agent-triggered or scheduled automated Vibe update will work reliably — as of
  2026-08-20, both `vibe_update_on_behalf` and `update_generative_ui_surface` were reported
  failing every time on automated/scheduled runs (vs. interactive, chat-driven prompting, which
  remains reliable). Verify live before building a workflow that depends on unattended Vibe
  updates.
- Cache computed/aggregated app data in per-browser localStorage with a naive "some fields
  present" write-guard — a partially-empty fetch can get cached and served stale for the full TTL
  with no user-facing way to force a refresh short of the app's own explicit refresh control.
- Assume a duplicated/templated app correctly re-points to the new set of boards without checking
  — a ~50% failure rate on exactly this was reported live days after the reconnect feature shipped.
- Assume a board with more than a few hundred items will return everything in one query — plan
  for the ~500/200-item pagination ceiling and the lack of reliable server-side date filtering.
- Assume Vibe apps can connect to Resource Planner / Portfolio-managed boards — confirmed
  unsupported.
- Join records with `contains` or fuzzy names — `PR215` matched `PR2159` on WHSmith
- Count blank values as a default category — blank cost-line pots became "External" overspend
- Let an inferred value drive a destructive write — Wren lost linked finishes that way
- Treat hidden navigation or a `lock=1` parameter as access control — enforce on the server
- Build per-record links on query parameters for a private app — the host strips them; put the
  key in the route path, or use an item view
- Store links on `<name>.v.monday.app` — it only resolves while the app is public
- Make an app public to "fix" links when it relies on per-user server guards — public bypasses them
- Design a board button or automation that "calls the app" — nothing can; stamp a date+time
  column and let the app act on it at the next session
- Build provisioning (create items/boards on approval) inside Vibe — that's a monday workflow
- Expect a legacy mirror-column status trigger to be created via `create_automation` — the
  workflow engine rejects mirror triggers; build that recipe by hand in the UI
- Promise a client zero build-time cost for routine end-user usage without checking whether the
  app's own logic invokes a per-run AI feature — that does charge credits even on "normal" use.
- Assume a Vibe app's third-party build-time dependencies are sandboxed from board data by
  default — this was an open, unanswered security question as of 2026-08-16; don't assert safety
  you haven't confirmed.
