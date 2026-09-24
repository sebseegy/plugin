# Vibe platform facts

Loaded on demand from `vibe-board-builder`. Re-verify anything stakes-sensitive against the mondayall knowledge base or #ask-vibe-ai before quoting it to a client.

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
  5-board ceiling in practice and required manual escalation to raise it.)* *(Docs disagree too,
  noted 2026-09: the newer support article "monday vibe best practices, features and
  capabilities" says up to 20 connected boards, while "Get started with monday vibe" still says
  5.)* **Net: plan for 5 as
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

**Practical implication for Step 6 (Craft the Vibe Prompt) in SKILL.md:** once a client's brand colors,
logo, tone, or a builder's own standing preferences are already set in Memory, they don't need to
be re-stated in every prompt. Check whether Account/User Memory already covers the app's design
system before padding a fresh prompt with brand details it may already know.

**Vibe also writes App Memory on its own during builds** — replies show "Saved to memory" lines,
and the saved rules persist (observed on WHSmith Portfolio Command, 2026-09: memory held brand,
board IDs, join rules, pot model and submit pipeline). The risk is stale memory: weeks later it
still held retired business rules (hard-block overspend, Capex/Opex/SAAS, blank pot = External)
that fought newer prompts. Audit App Memory after every business-rule change.

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

## Private app access and entry points

Production-validated on WHSmith Portfolio Command (2026-09-22/23), an internal finance app where
management approves and project managers only work on their own project.

**Who can get in**
- Any account member can open a published private app; **board permissions are the floor** —
  the app reads and writes as the viewer and cannot elevate their access. Users need Member
  access to every connected board their screens touch. Viewer seats can't open Vibe apps;
  guests need both the boards and the app object.
- Anything narrower than that is the app's job, and **must be enforced server-side on every
  read and write**. Hidden navigation, a missing button or a `lock=1` URL parameter is not
  security — assume a user can call the server function directly.
- A common grant is "viewer is management, or is named in this record's people column" (e.g.
  Portfolio → Project Manager). That makes the people column critical data: **empty column =
  everyone but management refused**. Check it's populated before rollout, and decide explicitly
  who else (sponsors, heads of delivery) gets in — Vibe narrowed the grant further than asked.
- Never make an app public to solve an access or link problem when it relies on per-user
  guards — public apps have no user identity, so every guard is bypassed.

**How people land on the right screen and record**
- **Unique page URLs** are native: `https://<account>.monday.com/misc/vibe/full-page-app/object/v/<route>?object-id=<id>&app-feature-id=<id>`.
- **The monday host strips extra query parameters on private apps.** `…/object?object-id=…&app-feature-id=…&code=PR2159&project=…&lock=1` reached the app with no `code`/`project`/`lock` and landed on the default screen. **Path segments survive**, so put the record key in the route:
  `…/object/v/spend/PR2159?object-id=…&app-feature-id=…`, resolved server-side by exact match
  (two matches refuse, zero shows a clear "no record with this code").
- **`/custom_objects/<id>` URLs also drop parameters.**
- **`<name>.v.monday.app` resolves only while the app is public.** When the owner made the app
  private, every link built on it showed "This app is no longer public… can't install it anymore."
  Don't store links on that host for a private app.
- **Item views scope themselves.** An app installed as an item view gets the record from monday's
  item context — no URL, nothing to strip. It's the most robust per-record entry, and it kept
  working when deep links didn't. Set it as the item's default view so users land on it.
- Never put `vibe-auth-token` or any JWT in a stored link.
- Test every entry path in a private window, signed in as a non-admin user.

---

## Board → app signalling

Validated on the Wren Contracts portal and Setup Wizard (2026-09).

- **Nothing on a board can call into a Vibe app**, and a job without a monday session can't read
  boards on the app's behalf. There are no background jobs.
- Pattern: whoever changes the source data (a board button, an automation, or another Vibe app)
  **stamps a date+time column** on the relevant record (Wren: "Options Sync Requested" on the site
  row). The app reads the stamp when a session opens, compares it with the stamp its cached copy
  consumed, and rebuilds only if the stamp is newer. Keep a manual Refresh as a fallback.
- **Write date and time, in UTC, and verify both halves on read-back.** A date-only stamp can't
  tell two same-day changes apart.
- When two apps share the stamp, specify its column ID, format and comparison rule identically in
  both apps' prompts — each app only sees its own code.
- "Warm" passes (pre-building caches) only run when someone opens the app; cap them per pass and
  don't let records confirmed empty consume the budget forever.
- For automations that react to another board's status through a **mirror column**, the
  workflow engine behind `create_automation` rejects mirror triggers. The legacy recipe ("when
  mirrored status changes…", with `mirrorColumnConfig`) works but has to be built by hand in the
  UI; it isn't in the public API.

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
  error message is unhelpfully generic (see Verification discipline in SKILL.md) — a failed prompt is
  not a free retry.
- **Observed per-prompt cost (Wren and WHSmith, 2026-09):** 35 credits for a small targeted
  fix, 141–221 for a scoped change, 417–454 for large multi-part prompts. Keep prompts to one job.
- Whether calling `vibe_create`/`vibe_update` via the MCP gateway with a signed JWT on a
  customer's behalf draws from *that customer's* credit pool, and whether internal/system calls
  can be exempted, was also raised as unresolved (2026-08-13).

**Practical implication:** when scoping a build for a client, flag credit consumption as a real
cost variable tied to iteration count, not a one-time fee — and warn that a stuck/erroring build
can burn meaningful credits on repeated fix attempts before it's understood as a platform issue
rather than a prompt-wording issue.

---
