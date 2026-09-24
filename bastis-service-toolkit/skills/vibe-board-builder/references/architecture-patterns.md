# Architecture patterns

Loaded on demand from `vibe-board-builder` Step 2.

## Architecture Patterns

### Pattern A — Event / Conference ✅ Production-proven

Use for: internal SKOs, team events, training weeks, conference portals.

Reference: "Company Agentic Week 2026" (workspace 14873780) — boards
18408716935 / 18408716892 / 18408899840 / 18408715924.

Follow exactly unless materially different. Column order is renderer-sensitive.

**Board 1 — `[Prefix] - general`**

| # | Title | Type | Notes |
|---|---|---|---|
| 1 | Name | name | default |
| 2 | Long text | long_text | Homepage copy, FAQ answers, rich descriptions |
| 3 | Status | status | Labels: "Working on it", "Done", "Stuck" |
| 4 | Photo | file | Image assets |
| 5 | Video | file | Video assets |
| 6 | Link | link | External URLs |

Groups: **General** → **Homepage** → **FAQ**

**Board 2 — `[Prefix] - competition`**

| # | Title | Type |
|---|---|---|
| 1 | Name | name |
| 2 | Text | text |
| 3 | Link | link |
| 4 | Photo | file |

Groups: **Links**

**Board 3 — `[Prefix] - resources`**

| # | Title | Type | Notes |
|---|---|---|---|
| 1 | Name | name | |
| 2 | Description | long_text | |
| 3 | Type | dropdown | Labels 1–15 below |
| 4 | Link | link | |

Type dropdown labels: Module, Brief, Podcast, Videos, Walkthrough, 1:1, Support,
Product feedback, Deck, Session deck, Recordings, Re-watch, Use cases, Portal, Playbook

Groups: **Trainings**

**Board 4 — `[Prefix] - sessions`** ← create last among content boards

| # | Title | Type | Notes |
|---|---|---|---|
| 1 | Name | name | |
| 2 | Description | long_text | |
| 3 | Speaker 1 | text | |
| 4 | Speaker 1 image | file | |
| 5 | Speaker 2 | text | |
| 6 | Speaker 2 image | file | |
| 7 | Date | **text** | Display string e.g. "Apr 28, 2026" — NOT a date column |
| 8 | Type | status | Labels: "Virtual", "In-person", "Hybrid" |
| 9 | Subitems | subtasks | Auto-creates linked subitem board |
| 10 | Site | status | Labels: "Tel Aviv", "Global", "London", "Brazil", "APJ", "EMEA", "New York" |

> ⚠️ Column order critical: `Subitems` (col 9) must precede `Site` (col 10).

Groups: **The strategy layer** → **The build layer** → **Agenda at a glance**

**Subitem board** (auto-created — verify these columns exist):

| Title | Type |
|---|---|
| Name | name |
| Owner | people |
| Status | status (labels: "Working on it", "Done", "Stuck") |
| Date | date ← real date column here, unlike parent board |

**Board 5 — `Resources for vibe`** *(optional pipeline board, no prefix)*

| # | Title | Type | Notes |
|---|---|---|---|
| 1 | Name | name | |
| 2 | POC | people | |
| 3 | Status | status | Labels: "to explore", "Ready to upload", "To check back", "Working on it" |
| 4 | Type | dropdown | Labels: "Recorded session", "Module", "Article", "Podcast" |
| 5 | Link | link | |
| 6 | Subtitle | text | |
| 7 | Description | text | Short — text type, NOT long_text |

Groups: **Ideas to explore** → **Ready to add to vibe**

---

### Pattern B — Knowledge Hub / Portal

Use for: internal wikis, documentation portals, L&D hubs, resource libraries.

| Board | Purpose | Key columns |
|---|---|---|
| `[Prefix] - articles` | Main content | Name, Body (long_text), Category (status/dropdown), Author (people), Published (date), Photo (file) |
| `[Prefix] - authors` | People profiles | Name, Bio (long_text), Photo (file), Role (text) |
| `[Prefix] - resources` | Downloads & tools | Name, Description (long_text), Type (dropdown), Link (link), File (file) |
| `[Prefix] - faq` | Q&A pairs | Name (question), Answer (long_text), Category (status) |
| `[Prefix] - feedback` *(optional)* | User submissions | Name, Type (dropdown), Status (status), Description (long_text) |

Groups: content categories ("Onboarding", "Product", "HR") or stages ("Draft", "Published").

---

### Pattern C — Product Catalog

Use for: internal product directories, marketplace listings, inventory portals.

| Board | Purpose | Key columns |
|---|---|---|
| `[Prefix] - products` | Product items | Name, Description (long_text), Category (status/dropdown), Price (numbers), Photo (file), Link (link) |
| `[Prefix] - categories` | Taxonomy | Name, Description (long_text), Banner (file) |
| `[Prefix] - inventory` | Stock/availability | Name, Status (status), Quantity (numbers), Location (text) |
| `[Prefix] - reviews` | Testimonials | Name, Rating (numbers), Body (long_text), Reviewer (text) |

---

### Pattern D — Quiz / Game App

Use for: live quiz events, training assessments, competitive scoring apps.

Key consolidation: merge "active game state" + "session history" into one board using
a Status column — primary 5-board strategy for quiz apps. Consider Vibe DB for live-round
scratch state (current answer buffers, per-player timers) if it never needs to be visible
outside the app itself.

| Board | Purpose | Key columns |
|---|---|---|
| `[Prefix] - questions` | Question bank | Name (question text), Option A/B/C/D (text), Correct Answer (text), Difficulty (status: "Easy"/"Medium"/"Hard"), Category (dropdown) |
| `[Prefix] - themes` | Visual themes | Name, Primary Color (text hex), Secondary Color (text), Background (file), Font (text), Preview (file) |
| `[Prefix] - sessions` | Live + history | Name (session code), Status (status: "Lobby"/"Active"/"Completed"), Current Question (numbers), Host (text), Theme (text), Created (date) |
| `[Prefix] - players` | Participant stats | Name, Session Code (text), Score (numbers), Rank (numbers), Status (status: "Active"/"Finished"), Correct (numbers), Wrong (numbers) |

Polling: Sessions and Players boards polled every 3–5 seconds when Status = "Active" (or use
Vibe DB's native presence/broadcast hooks if that state doesn't need to be board-visible).

---

### Pattern E — Custom Architecture

When no pattern fits:

1. Identify 2–5 primary entities
2. For each, run the Vibe DB vs. Board decision order (platform-facts.md)
3. One board per board-bound entity — no mixing
4. Apply the column type reference in SKILL.md
5. Name groups as navigation sections or workflow stages
6. Apply consolidation rules if entity count exceeds 5

**Production example (Wren Kitchens Contracts portal, 2026-08-20; board names as of 2026-09):**
5 boards fully consumed — Active Sites & Portal Logins `5102782955` (curated per-site finish pools,
tenures, portal auth columns, "Options Sync Requested" stamp), Kitchen Spec Templates (by
Customer) `5102782960` (per-site packages and templates), Product & Finish Catalog `5102782958`
(shared repository), Master Plot Tracker (All Sites) `5102782959` (plot pipeline), Incoming
Call-Off Requests (submission records, written as text) — plus a Vibe DB collection for OTP session
timing (expiry/throttle timestamps only; the login code itself stayed on the board because it
drives a native column-changed email automation, which Vibe DB structurally cannot do), and Vibe
DB for cached per-site option snapshots and submit timings. This is a real example of the board
ceiling being fully spent by genuine business entities, with only the truly app-internal state
pushed to Vibe DB — not a hypothetical.

A **second Vibe app** (the Setup Wizard / Options Picker) edits the same boards for Wren staff:
site setup, option templates, finish pools, Mark Live. The two apps coordinate only through the
board stamp (platform-facts → Board → app signalling). Name the target app in every prompt; each
app only sees its own code.

---

### Pattern F — Role-based internal operations app ✅ Production-proven

Use for: finance/approval desks, PMO reporting, internal portals where one group approves and
another group submits for their own records only.

Reference: WHSmith "Portfolio Command" (IT PMO, 2026-09) — Portfolio, Project Cost Tracker,
Portfolio Financials Tracker, Monthly Finance Update and Monthly Status Reports.

Shape:
- **One key joins everything** — the project code. Portfolio code = Cost Tracker project
  reference = Financials Tracker project reference, exact match only (`PR215` must never open
  `PR2159`). No hardcoded project lists.
- **Two entry models** — management (admins + named finance owners) opens the full app and
  lands on the approval desk; project managers enter only their own project via the Portfolio
  **item view** or a per-project link with the code in the path (`/spend/PR2159`,
  `/report/PR2159`), and see only those two screens.
- **Access grant = the record's people column** (Project Manager), checked server-side on every
  read and write. Approvals are management-only on the server, not just hidden in the UI.
- **Provisioning is not in the app.** "Intake approved → create Portfolio item + Financials row"
  is a monday workflow; the app only works on projects that already exist.
- **Money rules stated once, as rules** — e.g. Internal and External pots ring-fenced, blank pot
  counted in neither and flagged, over-budget flags rather than blocks.

Checks before rollout: people column filled on every live record, every PM a Member with access
to the connected boards, entry links tested in a private window as a PM.

---
