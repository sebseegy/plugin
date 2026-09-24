---
name: "vibe-board-builder"
description: "Architects the full backend for any monday.com Vibe app AND generates the production-ready Vibe prompt to build the UI. Use this skill whenever someone asks to \"set up Vibe boards\", \"build a Vibe app\", \"create a Vibe app structure\", \"scaffold a monday.com Vibe\", \"I need boards for a Vibe\", \"set up my Vibe for [project/event/portal]\", \"write a Vibe prompt\", \"generate a Vibe prompt\", or any variation on creating the data backend OR the UI prompt for a monday.com Vibe app. Also triggers when Basti is preparing a Vibe for a client and needs either the board foundation built, sample data populated, or the Vibe builder prompt crafted. Handles the complete end-to-end workflow: discover → architecture → boards → sample data → SDK file → Vibe prompt → delivery."
---


# Vibe Board Builder — Full Stack

Complete 7-step workflow: boards backend + sample data + SDK + Vibe prompt, plus public-app publishing and authentication guidance.

Facts in this skill were last verified against monday.com's internal mondayall knowledge base, the internal "Vibe DB vs. monday Boards" builder guide (drop-62ff9c42-315.monday-vibe.workers.dev, dated 2026-08-19), and official support docs on 2026-08-21, and cross-checked against live #ask-vibe-ai channel messages spanning 2026-08-12 through 2026-08-21. Vibe changes fast — if something here looks stale or contradicts what you observe live, re-verify via the mondayall knowledge base (`knowledge_search` / `knowledge_get_article`), the drop-page builder guide, or the #ask-vibe-ai Slack channel before trusting this file over direct observation.

---

## What is Monday Vibe?

Vibe is monday.com's AI-powered app builder. It reads structured data from boards (and, as of Aug 2026, a private per-app data store called Vibe DB — see below) and renders it as a custom web experience — portal, event site, knowledge hub, product catalog, calculator, dashboard. Key constraints, verified 2026-08-21:

- **Board limit is app-type-dependent and tier-gated — treat with care.**
  Full-page custom apps (the `OBJECT_FULLSTACK` variant this skill builds — portals, bespoke
  multi-board tools) have been observed hitting a **hard wall at 5 connected boards** on base
  tiers in real production builds. Separately, multiple internal staff independently describe the
  **Vibe Growth package** as unlocking a **20-board** connection ceiling — this is a distinct
  number from Growth's "25 apps" allowance; don't conflate the two. As of 2026-08-13, even
  internal CX staff were still asking each other to confirm this tiering ("is 20 boards only
  available on the Growth package, and everyone else stays at 5 regardless of ENT/Pro tier?"),
  and a "Growth Add-on" was mentioned as potentially required on top of base Growth for some
  accounts. *(Corroborated live 2026-08-18: an account needing a 20-board Vibe app hit an actual
  5-board ceiling in practice and required manual escalation to raise it.)* **Net: plan for 5 as
  the safe default ceiling for full custom apps; 20 is realistically reachable on Growth (possibly
  behind a further add-on) but verify per-account before committing an architecture to it.** Note:
  Vibe DB (below) doesn't count against this limit at all and is often the better home for
  app-internal data anyway.
- **Query/pagination ceiling on board-backed reads, confirmed live 2026-08-17:** a production app
  querying ~3,000 items hit a **500-item (sometimes 200-item) per-query return cap**, and reliable
  **server-side date/timeline filtering was not supported** — filtering had to happen client-side
  after fetching. Budget for this on any board with more than a few hundred items: paginate
  explicitly, move the filtering logic to Vibe DB (proper query operators, AND-only, no joins), or
  keep the board scoped small enough the cap never bites.
- **Anti-pattern, confirmed live 2026-08-19: never paste raw board IDs into prompt text** instead
  of connecting boards via the UI's Boards panel. One customer listed 20+ board IDs directly in a
  prompt; Vibe read the IDs as instructions and queried across all of them instead of the intended
  subset. Always connect boards through the UI first, then reference them by name/ID in the
  prompt — never hand the model a raw ID dump to parse.
- **Resource Planner / Portfolio boards cannot be connected to a Vibe app** — confirmed
  unsupported (live thread + internal mondayAll check, 2026-08-14/16). If a client's data lives on
  a Portfolio-managed board, plan to mirror the relevant fields onto a plain board Vibe can read,
  or scope the app around a different data source entirely.
- **No external APIs** — confirmed still unshipped as of Aug 2026 ("planned future feature," and
  still being actively asked about as recently as 2026-08-18 with no shipped answer). The one
  sanctioned exception: a native **Gmail/Outlook email integration** (see below) — Vibe can
  trigger, receive, and organize email through a connected Gmail/Outlook account without that
  counting as a general external API. Separately, an unresolved internal security question
  (2026-08-16) asks whether Vibe-generated apps pull external open-source libraries (fonts, JS
  charting libs) from npm/GitHub at build time in a way that's sandboxed from the app's own board
  data — no confirmed answer was visible in the channel. **Treat this as an open risk to name, not
  a settled guarantee, on any app handling sensitive data.**
- **No background jobs / scheduled tasks** — apps run only when actively viewed. Unchanged.
  Relatedly: **automated/scheduled agent-triggered Vibe updates are currently unreliable** — see
  the "What NOT to Do" note below.
- **monday.com only** — cannot be embedded or exported externally. "Public-facing sites on a
  dedicated URL" are listed as "coming soon" in some docs, which is in tension with "anyone with
  the link" public apps already being Full Release (see Public Vibe Apps section) — likely two
  different things (custom domain vs. link-sharing). Verify current state before promising either.
  Also flagged live (2026-08-19, unresolved in-thread): one internal question asked whether "public"
  Vibe apps genuinely require no monday login at all, or whether some flows still force a login —
  don't promise zero-login access to a client without confirming on the specific app/account.
- **Permission-bound on boards** — users see only board data they have access to. On **public**
  apps this guarantee disappears entirely (see below) — there is no per-user access model unless
  you build one yourself. Vibe DB has an entirely different visibility model, also covered below.
  **Separately, viewer-license users cannot access Vibe apps at all — by design** (confirmed in a
  live internal thread, 2026-08-20). This is a harder gate than the general public-app caveat: it
  blocks even fully authenticated internal monday users on a Viewer seat, not just external/public
  visitors. If a client's rollout includes viewer-tier internal staff, budget for either upgrading
  their license or building the public/token-based access path instead. Additionally: **guests can
  view a Vibe app on desktop but not on the mobile app** (confirmed live, 2026-08-14) — factor this
  into any rollout where external users are expected to use phones.
- **Board structure = app architecture** — column types, titles, and group names directly drive
  what Vibe renders and how it filters/navigates.
- **Polling** — for real-time updates on board data, apps must poll every 3–5 seconds. Vibe DB
  instead ships real-time hooks natively (`useVibeQuery`, `usePresence`, `useBroadcast`) — no
  manual polling needed for that layer.
- **Only the creator can edit an app** — no multi-editor collaboration yet (still being asked
  about as of 2026-08-19 with no change). Ownership is transferable, and a public template link
  can be shared for others to duplicate — see the Duplicate/Template capability below, which
  makes this less of a limitation in practice than it sounds, though see the caveat on its
  reliability below too.
- **Large boards (10k+ items)** are only supported on apps created from **2025-09-25** onward —
  older apps need to be duplicated/rebuilt to get this, it isn't retroactive.
- **No version control or staging environment for a live app** — confirmed as a live, unresolved
  gap (2026-08-17): there's no way to save/restore a prior stable version distinct from the
  published one, or maintain a separate "Dev" copy while real users are on production. The nearest
  workaround is the Draft-vs-Published split below (safe for incremental prompts) plus manually
  duplicating the whole app before any large or security-relevant change, so you have a rollback
  copy that isn't just "hope the prior version in history is still good."

---

## Vibe DB vs. monday Boards

As of 2026-08-19, Vibe apps have a second first-class data layer beyond boards: **Vibe DB** — a
private, per-app JSON document store (one SQLite database per app, running in a Cloudflare
Durable Object). Deciding between the two is now a real architecture step, not just "always use
boards" — get this wrong and you either blow a board slot on plumbing nobody else needs, or put
real business data somewhere other automations/dashboards can't reach it.

**Official launch specifics, per the product team's own announcement (2026-08-19) and the
internal builder guide (2026-08-19):** headline capacity is **up to 1M items** (marketing framing)
/ **~2M typical-sized records within a 10 GiB storage envelope** (technical framing — not
contradictory, just two lenses on the same ceiling), and Vibe DB is pitched as **30x faster than a
monday board** for app-internal reads/writes, directly solving the old 500-item board query cap.
Enable it either via the prompt box's "+" → Integrations → Advanced → "Create fast database", or
simply by prompting Vibe: *"use Vibe DB to store the data."* It can be retrofitted onto an
existing app, but **only apps created from a specific infra cutoff date support it** (the
announcement cites "Aug 26" as the cutoff without confirming the year — verify live before
assuming an older app qualifies), and only on full left-pane apps, not board-view apps. There's
also a sanctioned **one-time migration** path, distinct from the "never mirror" hard rule below:
you can ask Vibe to *"add a sync option to migrate your data from a board to Vibe DB"* for a
clean one-off cutover. That's different from ongoing mirroring, which remains prohibited. As of
2026-08-19 this was rolling out gradually to monday.monday first — treat availability as
not-yet-universal until confirmed live on the target account.

**Decision order — walk through in sequence, first "yes" wins (matches the internal builder
guide's own framing verbatim):**
1. Does a human need to see and edit this data using monday's own grid/kanban/gantt view, filters, or automations? → **Board**.
2. Do other monday automations, integrations, or dashboards outside this app need to read or write this data? → **Board**.
3. Is the data private to the app — settings, drafts, per-user preferences, computed/cached results, logs — things nobody browsing the board should stumble on? → **Vibe DB**.
4. Does the shape of the data not fit monday's column model well — deeply nested objects, variable schemas, large free-form JSON blobs? → **Vibe DB**.
5. Do you need built-in real-time collaboration primitives (who's online, live cursors, broadcast events) for the app's own UI? → **Vibe DB** — it ships presence/broadcast hooks out of the box.

Rule of thumb: it's not about whether the data "is work" — Vibe DB can hold tasks/requests/records
fine. The question is *where that work gets managed*. If people need monday's native board UI (or
other automations/integrations) to act on it, it's a **board**. If the Vibe app itself is the
surface where it's created, viewed, and acted on end-to-end, it can be **Vibe DB** — board or no
board. Two worked examples from the internal guide: a project-tracking app reads/writes tasks on a
real **Board** (other automations touch that data) while storing its own dashboard-layout prefs,
"recently viewed" list, and a cached weekly summary in **Vibe DB** (none of that needs board
visibility). Contrast a standalone approvals app: even though "approval requests" sound like
classic board items, if the Vibe app itself is the entire surface where they're submitted,
reviewed, and closed — and nothing outside the app needs to touch them — they can live in Vibe DB
directly. The app *is* the work surface.

**The critical gap that affects the authentication pattern below: Vibe DB has no
automation/integration surface.** Only the owning app's server code (and the builder's own "Data"
tab — a full-CRUD grid with CSV export, visible to builders/maintainers only, never to published
end users) can touch it. No monday recipe, automation, or dashboard can see or trigger off a Vibe
DB write. This means the OTP/token authentication pattern documented below, which relies on
writing a code to a **board** column specifically so a native "column changed" automation can fire
the email, **cannot be built the same way against Vibe DB**. Ephemeral auth state (login code,
expiry, throttle timestamp) is arguably the textbook-correct fit for Vibe DB — it's pure
app-internal plumbing nobody else needs to see or touch, and putting it on a real business board
clutters that board's schema for anyone who works in it directly. But moving it there means
switching email delivery to Vibe's native Gmail/Outlook integration called directly from server
code, instead of the automation-relay trick. Both are valid — choose based on whether the account
already has Gmail/Outlook connected for Vibe, and whether keeping the client's board schema free
of implementation plumbing outweighs the extra wiring. (Production-validated: this exact ephemeral
data was migrated from board columns to a Vibe DB collection in the Wren Kitchens Contracts
portal, 2026-08-20 — confirmed via independent code trace, not just a completion message.)

**Hard rule, stated explicitly in the Vibe DB SDK**: "for app (board) data use BoardSDK instead —
never mirror board data into Vibe DB." Copying board data into Vibe DB "for convenience" creates
two sources of truth that drift out of sync the moment the board changes. (This is separate from
the sanctioned one-time migration path above — migrating once and then treating Vibe DB as the new
source of truth is fine; keeping both in sync indefinitely is not.)

**Visibility model is inverted from a board's**: a board is org-wide by default, governed by
monday's normal permissions — anyone with board access can see it, and it's reachable by
automations/integrations/dashboards natively. Vibe DB is private to the app by default: no board,
dashboard, or other app can see it, and it has no automation/integration surface at all — visible
only to (a) end users through whatever custom UI the app builds, and (b) whoever has access to the
app builder's own Data tab. There is no accidental org-wide exposure, but also no "just open it
and look" for anyone outside the app.

**UI cost differs sharply**: a board gets monday's native Table/Kanban/Gantt/Calendar views for
end users automatically, no extra build — the Vibe app typically renders as a custom panel
alongside that native UI. Vibe DB's built-in UI stops at the builder layer: the app builder tool
has a full-CRUD grid per collection (view/add/edit/delete rows, CSV export) but that's a
builder/maintainer tool the app's end users never see once published. Every end-user-facing
screen, list, form, or chart over Vibe DB data has to be custom-built as part of the app —
end-user UI effort scales directly with how much Vibe DB data needs to be visible to the person
using the published app. Budget for that when a data-layer decision leans Vibe DB.

**Scale, if it ever matters:** documented ceiling is a **10 GiB per-app storage quota** (soft
quota — write requests are rejected once exceeded), roughly **2M typical-sized records** at a
few-KB-per-record size (comparable to a monday item's worth of fields) — this and the "up to 1M
items" marketing headline above aren't contradictory, just different framings of the same
underlying capacity. Also, per the SDK's documented technical limits: **256 KB per document hard
cap**; filters are **AND-only, no OR, no cross-collection joins**; query operators supported are
`==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `array-contains`; aggregate functions are `count`, `sum`,
`avg`, `min`, `max`; `in` queries capped at **30 values**; bound parameters capped at **90 per
compiled query**; aggregate queries capped at **1,000 buckets** per grouped aggregate; default
page size **100**, hard max **1,000**; and it's **server-only** — client code gets real-time hooks
(`useVibeQuery`, `usePresence`, `useBroadcast`), never direct queries. Point-in-time restore
available for up to **30 days** back.

**Practical takeaway for the 5-board-limit problem flagged above**: before spending a board slot
on data that's purely app-internal (session state, ephemeral tokens/codes, cached computations,
per-user UI preferences), check whether it needs to be on a board at all — if nothing outside the
app ever needs to read, automate on, or dashboard against it, it likely belongs in Vibe DB
instead, freeing board slots for genuine shared business data. Most non-trivial apps end up using
both: a board for the org's real work data, Vibe DB for everything specific to how the app itself
operates. The internal builder guide is explicit that this hybrid pattern is "the expected
pattern, not an edge case."

---

## Vibe Memory (new, 2026-08-20)

Shipped today, currently in gradual release — a persistent instruction/preference layer, distinct
from Vibe DB (which stores *app data*; Memory stores *builder and account instructions*). Three
levels:

- **App Memory** — instructions specific to one app (e.g. "always auto-save in real time, don't
  ask users to click save").
- **User Memory** — the builder's personal working style, applied across every app they build
  (e.g. "always confirm before making big changes").
- **Account Memory** — brand assets and standards (colors, logo, tone) applied to every app on the
  account — **admin-controlled only**, not settable by individual builders.

Set it via Settings → Memory (type any instruction directly), or just tell Vibe in chat — e.g.
"Remember this is my company logo, use it in every app I build" — and it saves automatically, no
separate settings trip required.

**Practical implication for Step 6 (Craft the Vibe Prompt) below:** once a client's brand colors,
logo, tone, or a builder's own standing preferences are already set in Memory, they don't need to
be re-stated in every prompt. Check whether Account/User Memory already covers the app's design
system before padding a fresh prompt with brand details it may already know.

---

## Public Vibe Apps

Status as of 2026-08-21: **Full Release**, but heavily gated — don't assume it's available by default.

- **Requires the Vibe Growth package** (25-app allowance — a plan entitlement, distinct from the
  20-board connection number discussed above; don't conflate the two). Accounts on other tiers
  don't get it.
- **Admin toggle required, off by default on Enterprise.** Path: Administration → AI governance →
  AI permissions → Vibe permissions → "Publish Vibe apps to the public web." Only admins can turn
  it on; only the board owner can then publish.
- **Not retroactive.** Only apps created *after* the account-level toggle was enabled can be made
  public. An existing app has to be rebuilt from scratch to get the public option — there's no
  in-place upgrade path.
- **Full-page apps only.** Item view, board view, and dashboard widgets are not supported as
  public apps — only the full-page (object) app type this skill's 7-step workflow produces. This
  is flagged internally as "the most likely source of 'why isn't this working?' tickets."
- **Zero native per-user access control.** Quoting the platform's own framing verbatim: "no
  per-user permission layer... anyone with the link can view and edit the connected board data
  according to the app's logic... this is a design decision, not a bug." There is no row-level or
  per-user gate, no login, no SSO, nothing — if you need one, you build it entirely out of board
  (or Vibe DB) data. Public apps read/write directly to the real connected boards, not an
  anonymized copy — an external user's edit goes straight to production board data.
- **Viewer-license users cannot access Vibe apps at all — confirmed by design, not a bug** (live
  internal thread, 2026-08-20). This is a harder, separate gate from the "no per-user access
  model" point above — it applies even to fully authenticated internal monday users on a Viewer
  seat, not just external/public-link visitors.
- **Guests can view on desktop but not on the mobile app** (confirmed live, 2026-08-14) — a real
  rollout constraint if any external audience is phone-first.
- **No IP allow-listing / domain-blocking for public apps**, unlike enterprise account-level IP
  restriction (flagged live, 2026-08-13, unresolved) — if a client expects to restrict a public
  Vibe app the way they restrict normal account access, that parity doesn't exist yet.
- **Open, unresolved security question (2026-08-16):** whether externally-sourced build-time
  libraries (npm/GitHub fonts, JS charting libs, etc.) used by a Vibe app are sandboxed from that
  app's own board data, and whether monday runs any static/dependency scanning on Vibe-generated
  app code. No confirmed answer was visible in the internal channel. Treat this as a named,
  open risk on any public app handling sensitive data — don't assert it's safe without checking
  current status.
- Connected boards show a broadcast-style visibility indicator once the app is public.
- Admins can force-unpublish any public app account-wide at any time.

### Building your own authentication (since the platform has none)

The proven pattern, validated in production (Wren Kitchens Contracts portal, 2026-08-20):

1. Store an identity field on the relevant board — either a static shared token (simplest: one
   secret per group of users, embedded in their unique link) or, for stronger per-person
   assurance, the person's real email address plus three ephemeral fields: a one-time code, its
   expiry timestamp, and a "last requested at" timestamp for throttling. See the Vibe DB section
   above before deciding where those three ephemeral fields should actually live — a board column
   (if you want the automation-relay email pattern below) or Vibe DB (if you'd rather keep them
   off the client's board schema and send email via Vibe's native Gmail/Outlook integration
   instead).
2. **Vibe apps can't send email directly to an arbitrary address via a background process** —
   two sanctioned options: (a) route it through a **native monday automation**: write the code (or
   token) to a *board* column, and a "when this column changes" automation (built via
   `create_automation`, not inside Vibe) sends the email — confirmed working end-to-end, but
   requires the ephemeral state to live on a board, not Vibe DB, since automations can't see Vibe
   DB; or (b) call Vibe's native Gmail/Outlook email integration directly from the app's server
   code — works with either a board or Vibe DB as the backing store, and is the only option if the
   ephemeral state lives in Vibe DB.
3. On login, re-fetch the stored code/token fresh every time you validate it — never compare
   against a cached read from step 1, and always re-check expiry as a real timestamp comparison,
   not a string compare.
4. If one identity should see multiple sites/records (e.g. one contact covering several
   developments), write the ephemeral code to exactly **one** canonical matching record — writing
   it to all of them fires the automation multiple times and sends duplicate emails — but scope
   the resulting session to *all* matching records once validated.
5. Every downstream write (not just the login step) must re-validate server-side that the
   session's identity still matches the target record's owner column. A UI-level gate alone is
   not a write-guard — assume a client can call the write endpoint directly and skip the UI.
6. Keep this fully additive to any existing access path (e.g. a legacy `?token=` URL scheme) —
   don't fork core business logic per auth mode; feed both paths into the same downstream session
   shape so write-guards and attribution logic aren't duplicated.

---

## Recently shipped capabilities worth knowing about

- **Duplicate-and-reconnect-boards, and template links** (2026-08-18) — an app can now be
  **duplicated within the same account and pointed at a different set of boards**, reusing the
  exact same UI/logic for a new project: chevron next to app name → Duplicate → "Duplicate and
  connect to new boards." Separately, **Publish → Copy template link → "Don't include your
  connected boards"** lets you share an app cross-account as a template that recipients populate
  with their own boards, rather than getting a live copy of your data.
  **Reliability caveat, confirmed live just 3 days after this feature shipped (2026-08-21):** a
  report of workspace app templates that embed a Vibe app still fail to re-point to the new
  workspace's boards **around 50% of the time** — the duplicated app keeps referencing the
  original boards instead. Treat the reconnect/template flow as **not yet fully reliable** — after
  duplicating or deploying from a template, explicitly verify (e.g. via `vibe_get`/`vibe_ask`)
  which board IDs the app actually points at before handing it to a client, rather than trusting
  the duplication step silently worked.
  **Separately unresolved (2026-08-13):** for a Vibe app embedded as an item view on a "managed
  template" board with multiple deployed instances, it was unclear even to the person asking
  whether editing the app on one instance updates it everywhere (single shared app definition) or
  only that instance — and there's no documented safe way to duplicate/test/merge changes without
  risking a live, heavily-used build. If you're building a repeatable multi-instance client
  pattern this way, verify this behavior explicitly on a throwaway instance first — don't assume
  either answer.
- **Board editing Subagent** (2026-08-16): Vibe can now add/delete/rename columns, add/delete/
  bulk-update items, delete boards, and import CSV/XLSX directly into an *existing* app (not just
  at app-creation time), all via natural-language request in chat — it asks for explicit approval
  before destructive actions (column/board deletion).
- **Sketch your app** (2026-08-13): draw/annotate directly on the app canvas (free draw, rectangle,
  text tool) and Vibe implements the sketch as a prompt — useful for fast layout iteration without
  writing prose descriptions of positioning.
- **Start an app from a CSV/XLSX/XLS file** instead of describing data in a prompt. Each row
  becomes an item, each column a field, types auto-inferred (falls back to Text if unclear).
  Row cap: **5,000** — extra rows are truncated with a warning. **Always creates a new board** —
  it cannot import into or merge with an existing one.
- **Connect an existing board to a live app at any time**, before or after publishing, with no
  rebuild required — via the Boards panel or by prompting "connect a new board and add its data."
- **Native Gmail/Outlook email integration** — Vibe detects when a prompt needs to send email,
  prompts you to connect Gmail or Outlook (auth happens inside monday.com), and can then send
  HTML-formatted emails with attachments (5MB file cap, must come from a Files column) directly
  from app logic — the only way to send email from an app whose relevant state lives in Vibe DB
  (see above), and a genuine alternative to the automation-relay pattern even for board-backed
  apps.
- **Element selection tool** — click a specific UI element in the Vibe editor to reference it
  directly in your next prompt instead of describing its location in words. Available
  automatically on new apps; appears on existing apps after one more edit.
- **Prompt queueing** — multiple prompts can be sent without waiting for the current build to
  finish; they run in order automatically.
- **Draft vs. published, and Auto Update.** A published app has a live version and can be edited
  further in draft without affecting production. Check `auto_promote` in the app's config (via
  `vibe_get`) before assuming a change is live — if it's off, changes sit in draft until you
  explicitly click "Update changes." This is the closest thing to a safety net given there's no
  real version control (see above) — use it deliberately, and duplicate the whole app before any
  large or security-relevant change as a true rollback copy.
- **Export a screen as PDF** — must be explicitly built in as a feature ("add an Export as PDF
  button"), not available by default.
- **Set a Vibe app as the account homepage** — admin-level setting (Administration → General →
  Account → Account home page).
- **Mobile**: camera-based barcode/QR scanning that maps results to a board item. Full mobile
  app support otherwise still limited — an app-vs-browser behavior discrepancy was reported live
  as recently as 2026-08-19, and guests specifically cannot view a public app on mobile at all
  (see above) — verify before promising a mobile-first build.
- **Performance levers for large boards**, worth prompting for explicitly when a board is slow:
  cache data in local storage with a staleness window, use the aggregation API for stats, load
  only necessary data (date ranges, exclude done items), paginate ("load first 20, fetch more on
  scroll"), and reduce queried columns to only what's rendered. **Caveat learned in production**:
  a local-storage cache with a naive write-guard (e.g. only checking that *some* fields are
  non-empty before caching) can serve stale, partially-empty data for its entire TTL window with
  no user-visible way to force a refresh other than the app's own explicit refresh control —
  browser hard-reload does not clear localStorage. If caching computed/aggregated results that
  can legitimately be empty mid-edit, either keep the TTL very short during active data entry, or
  put that cache in Vibe DB instead (server-side, centrally invalidated) rather than per-browser
  localStorage — see the Vibe DB decision order above.

---

## AI credit charging — what actually costs credits

Recurring source of confusion internally as of 2026-08-13 through 2026-08-21, including at least
one customer describing it as a potential "deal breaker" and another burning ~4,000 credits (95%
of a troubleshooting session) fighting an authorization bug rather than building. Working
understanding from the channel, **not an authoritative billing doc — verify against current
pricing pages before quoting a client:**

- **Build/edit prompts** (anything that makes Vibe generate/change code) consume credits.
- **Routine end-user interaction with a published app** (e.g. 30 people submitting a form daily)
  does **not** consume credits by itself, **unless the app's own logic invokes an AI feature per
  run** (e.g. an AI-generated summary on every submission) — in which case that per-run AI call
  does charge.
- **A grey zone exists** for actions Vibe performs that monday itself can't do natively (e.g.
  exporting to PowerPoint) — whether that's billed as an AI action or a plain automation action
  was an open question as of 2026-08-21, unresolved in-channel.
- **Credits are consumed even on failed builds/deployments**, including retries where Vibe's own
  error message is unhelpfully generic (see Verification discipline below) — a failed prompt is
  not a free retry.
- Whether calling `vibe_create`/`vibe_update` via the MCP gateway with a signed JWT on a
  customer's behalf draws from *that customer's* credit pool, and whether internal/system calls
  can be exempted, was also raised as unresolved (2026-08-13).

**Practical implication:** when scoping a build for a client, flag credit consumption as a real
cost variable tied to iteration count, not a one-time fee — and warn that a stuck/erroring build
can burn meaningful credits on repeated fix attempts before it's understood as a platform issue
rather than a prompt-wording issue.

---

## 7-Step Workflow

### Step 1 — Discover

Ask (or infer from context):
- **App type** — event site, portal, knowledge hub, product catalog, quiz/game, tracker, etc.
- **Main entities/content types** — sessions, resources, products, questions, players...
- **Project name / naming prefix** — e.g. "Sales Kickoff 2026", "WHSmith Portal"
- **Workspace** — call `get_user_context` to find the active workspace, or ask if ambiguous
- **Audience & roles** — who uses the app and what can each role do? If any audience is external
  (no monday account), flag early that you'll need the Public Vibe Apps path and a homegrown
  auth pattern (see above) — this materially changes the architecture, not just the publish step.
  If any audience is internal-but-Viewer-license, flag that too — Vibe apps are blocked for
  Viewer seats regardless of publish status. If any external audience is expected to use mobile,
  flag the guest-desktop-only limitation too.
- **Dynamic vs static** — does the app need real-time updates (scores, status)?
- **Bootstrapping source** — is there an existing spreadsheet/CSV that should seed a board
  instead of hand-authoring sample data? If so, plan to import it directly (see above) rather
  than manually recreating its structure.
- **Board vs. Vibe DB for each entity** — for every entity identified, run it through the
  decision order in the Vibe DB section above before defaulting it onto a board.
- **Expected data volume per board** — if any entity will exceed a few hundred items, flag the
  500/200-per-query pagination cap now, not after the build hits it.

Propose a strawman board architecture immediately. Don't wait for perfect information.

---

### Step 2 — Propose Architecture

Match to a pattern below (A–E). Present each board with its purpose, key columns, and groups
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
items (faster and avoids transcription drift, subject to the 5,000-row cap noted above). Rules
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

Produce a JavaScript constants file that maps all board and column IDs. Prevents hardcoded
IDs in Vibe's generated code and makes the app maintainable.

**Format:**
```javascript
// [App Name] — Vibe SDK
// Generated: [date]
// Boards: [N] | Workspace: [workspace_id]

export const [BoardName]Board = {
  boardId: XXXXXXX,
  columns: {
    name: "name",
    description: "long_text",          // long_text column
    type: "status",                     // "Virtual" | "In-person" | "Hybrid"
    speakerOne: "text0",               // text column
    speakerOneImage: "files",          // file column
    date: "text1",                     // display date string e.g. "Apr 28, 2026"
    site: "status1",                   // "Tel Aviv" | "Global" | "London" | ...
    subitems: "subitems",
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
- Inline comments for status label options and column semantics

---

### Step 6 — Craft the Vibe Prompt

Write a production-ready prompt for the Vibe app builder. This is the most important
deliverable — it must be detailed, technical, and complete. A weak prompt produces a
generic UI; a strong prompt produces a finished product.

Before drafting, check whether Vibe Memory (above) already holds the client's brand
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
- Use the provided SDK constants for all board/column IDs — never hardcode
- Error handling: show [fallback UI] if board fetch fails
- Loading states: skeleton screens for [component]
- Caching: cache board data for [N] seconds before re-fetching

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
- Include exact board IDs and column IDs (from Step 3) — connect boards via the UI first, never
  paste raw board IDs into the prompt body as a substitute for connecting them
- Specify status label strings verbatim — Vibe matches on exact text
- Describe UI behaviour, not just data structure
- Add a concrete example query for each board (what to fetch, how to filter)
- Length: 800–2000 words. Do not pad; do not truncate.

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
  mode before assuming the prompt wording is the problem.
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
- There is no version control or staging environment (see above) — treat "duplicate the whole
  app before a risky change" as a mandatory verification step, not an optional nicety, since
  there's no other way back to a known-good state if a change regresses something.

---

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
2. For each, run the Vibe DB vs. Board decision order above
3. One board per board-bound entity — no mixing
4. Apply column type reference below
5. Name groups as navigation sections or workflow stages
6. Apply consolidation rules if entity count exceeds 5

**Production example (Wren Kitchens Contracts portal, 2026-08-20):** 5 boards fully consumed —
Sites & Customers (curated per-site product pools + auth columns), Kitchen Specs (per-site
packages), Product Options Catalog (shared repository), All Call Offs (plot pipeline), Call-Off
Requests (submission records) — plus a Vibe DB collection for OTP session timing (expiry/throttle
timestamps only; the login code itself stayed on the board because it drives a native
column-changed email automation, which Vibe DB structurally cannot do). This is a real example of
the board ceiling being fully spent by genuine business entities, with only the truly
app-internal ephemeral state pushed to Vibe DB — not a hypothetical.

---

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
- Placeholder column names ("Column 1") — Vibe queries by exact title
- Omit status/dropdown labels — filter UI depends on exact label strings
- Boards in different workspaces — cross-workspace Vibe apps break
- Skip subitem board for sessions — task tracking widget breaks
- Swap `text` ↔ `long_text` — they render differently in Vibe
- Wrong column order in sessions board — Subitems must precede Site
- Date column for display dates — use `text` type
- Hardcode board/column IDs in the Vibe prompt — always reference via SDK constants
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
- Promise a client zero build-time cost for routine end-user usage without checking whether the
  app's own logic invokes a per-run AI feature — that does charge credits even on "normal" use.
- Assume a Vibe app's third-party build-time dependencies are sandboxed from board data by
  default — this was an open, unanswered security question as of 2026-08-16; don't assert safety
  you haven't confirmed.
