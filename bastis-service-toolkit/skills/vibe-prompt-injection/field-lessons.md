# Field lessons — Wren Kitchens and WHSmith

Rules Vibe-generated code broke in production, and the rule that fixed it. Apply them
proactively when writing any prompt that touches the area. Source in brackets.

## Contents
- Data identity and schema
- Write safety
- Access and entry points
- Board ↔ app signalling
- Performance
- Observability
- Working with Vibe itself

---

## Data identity and schema

- **Resolve columns by board ID + column ID + expected type. Titles are display only.** Vibe
  defaulted to exact-title matching; a renamed column ("#Kitchen Specs") became a false
  blocker across a whole site. Fix: one centralized map `{boardId → logicalField → {columnId,
  type}}`, a resolver that type-checks, fails closed naming board/ID/type/what-was-found, and
  never substitutes a similar title. Labels still read live from the resolved column. [Wren]
- **One spelling per field.** `worktopPrivate` vs `worktopsPrivate` made fully stocked pools
  read as empty. One exported definition, plus a startup check that shouts on drift. [Wren]
- **Join records by exact key — never `contains`, `includes`, fuzzy name, or a hardcoded list.**
  `PR215` matched `PR2159`. Zero matches → clear message; two or more → refuse, don't pick the
  first. A hardcoded list of 12 project names blocked project 13. [WHSmith]
- **Blank is not a category.** Blank cost-line pot was counted as External (75 of 76 rows were
  blank → everything looked like external overspend). Exclude blanks and show a notice
  ("N lines have no pot"). [WHSmith]
- **Stated vs inferred.** When a mode field is blank and the app infers it from another column,
  rules may *advise* but never hard-block or write based on the inference. [Wren — Finish
  Choice Mode inferred from Fixed Spec]
- **Clean labels before the app depends on them.** Dropdowns mixing customers with sites
  ("Taylor Wimpy", "Taylor Wimpey - Alresford") broke "used before by this customer". Label
  cleanup is a Sidekick batch job, not a Vibe prompt. [Wren]

## Write safety

- **Write only fields that changed.** Unchanged relations must be absent from the payload.
  A form seed that omitted one field silently blanked it on every unrelated save. [Wren]
- **Inferred state must never clear stated data.** Clearing linked finishes because the mode
  was *inferred* as Site lists was a data-loss bug; clear only when the board *states* it. [Wren]
- **Write → re-read → compare → then update UI.** Never claim success optimistically. Distinct
  outcomes: saved + verified / "written but could not be verified" / "saved, refresh pending".
- **Re-validate at the write, not only at Preview.** A Preview gate passed earlier doesn't hold
  if the catalogue failed while Preview was open; Save must re-run the same gate. [Wren]
- **Advisory vs hard blocks.** For setup/admin apps: completeness = advisory ("Still to do — 3
  items"), saving partial work allowed. Hard blocks only for data safety (unreadable relation
  that would clear live links, label that doesn't exist, wrong-category/retired product).
  Put full strictness at the go-live gate (Mark Live / "Show in portal"). [Wren]
- **Cache must never approve a save.** Paint from cache; require a live read before writes. [Wren]

## Access and entry points

- **UI hiding is not security.** Every read/write re-checks identity server-side. A flag like
  `ENFORCE_PROJECT_PERMISSIONS = false` meant any member could edit every project's money. [WHSmith]
- **Board permissions are the floor.** Any account member can open a published app; the app
  can't elevate board access. Viewers can't open Vibe apps at all; guests need board + app
  access. Users must be Members with access to every connected board they need. [WHSmith]
- **A people column as the access grant makes that column critical data.** When it's empty,
  everyone is refused. Check it's populated before rollout. [WHSmith]
- **Private full-page apps: query parameters are stripped; path segments survive.**
  `…/full-page-app/object?object-id=…&app-feature-id=…&code=PR2159` lost `code`;
  `…/full-page-app/object/v/spend/PR2159?object-id=…&app-feature-id=…` worked. Put the record
  key in the route path (`/spend/$code`) and resolve it server-side by exact match. [WHSmith]
- **`<name>.v.monday.app` only resolves while the app is public.** Making it private killed
  every link built on it ("This app is no longer public"). `/custom_objects/<id>` also drops
  parameters. Never store links with `vibe-auth-token` or any JWT. [WHSmith]
- **Item views scope themselves.** An app pinned as an item view gets the record from monday's
  item context — zero URL needed, and it survives when deep links don't. [WHSmith]
- **Public apps have no per-user layer.** Never make an app public to "fix links" when it has
  server-side role guards — public bypasses them entirely. [WHSmith]
- **External users: build auth from board/Vibe DB data** (token or email + OTP) — see
  `vibe-board-builder` → Building your own authentication. [Wren]

## Board ↔ app signalling

- **Nothing on a board can call into the app, and there are no background jobs.** Pattern:
  the board (button/automation/other app) stamps a date+time column (e.g. "Options Sync
  Requested"); the app compares it to what its cache consumed on the next session open and
  rebuilds if newer. Date-only stamps collide on same-day changes — write date + time in UTC
  and read back both halves. [Wren]
- **Background warm passes run only when someone opens the app**, capped (sites per pass,
  total seconds), and must not let confirmed-empty records consume the budget forever. [Wren]
- **Cross-app contracts must be specified identically in both apps** (stamp format, column ID,
  comparison rule) — each Vibe app only sees its own code. [Wren]

## Performance

Measured on Wren: 8.6s cold open, 6.4s of it one read that most sites didn't need.

- **Skip reads whose result won't be used** (fixed-spec packages never needed the pool read).
- **Cache verdicts, including "confirmed empty"** — otherwise empty sites re-pay the full
  read on every open. Give empty verdicts a short window and mark stale on serve.
- **One shared read per dataset.** Three components each walking the same 500-item pages
  meant three full walks. Lift the hook once and pass state down.
- **By-id lookup for linked records** instead of walking the whole catalogue to name 18 items.
- **Cache and live read in parallel**, not cache-then-live. Late cache never overwrites live.
- **Timeouts that name the board** and stop spinning; Retry reuses the existing refresh.
- **Request generation tokens** on every async hook: stale responses never overwrite newer
  state; restore `alive = true` on each effect setup (React Strict Mode).
- **Pagination cursors must keep the same filter and columns.** A "load more" cursor that
  dropped the where-clause mixed other projects' lines into a 150-line list. [WHSmith]
- **Caps must not hide data silently** (`.slice(0, 8)` left groups 9+ looking healthy). [WHSmith]
- Don't "load only the first 20" when a complete list is required for save validation.

## Observability

- **Deployed server logs can't be read back.** Build an in-app diagnostics screen
  (Housekeeping / Health / Checks) for admins: per-step timings stored per real submission
  (median + worst of last 50), schema report (field / configured ID / live title / type /
  resolved), cache state, warm-pass results. Store timings in Vibe DB. [Wren]
- **Hide diagnostic surfaces from end users**; admins only.
- Ask Basti to paste these panels — they're your only runtime telemetry.

## Working with Vibe itself

- **"Oops, something went wrong" = assume half-applied.** Read-only "what landed" prompt next.
- **Vibe deviates deliberately and says so.** Judge each deviation; it's often right.
- **Vibe adds scope** (new nav items, inspection screens, narrowed permissions). Fence it and
  check every reply for unrequested surface.
- **"Saved to memory" persists rules.** Audit App Memory after rule changes; WHSmith's memory
  still held retired rules (hard-block overspend, Capex/Opex/SAAS, blank pot = External).
- **Queued prompts that touch the same files collide.** Queue only independent prompts.
- **Vibe's change log is chat-only** unless the app has a change-log store — ask for a
  numbered entry (CL-nnn) in the report so you can reference changes later.
- **SDK gaps exist** (WHSmith Portfolio: SDK `.update()` blocked → raw GraphQL). If Vibe
  reports one, record it in the app card so later prompts don't fight it.
- **A Vibe answer that "it's infrastructure, not code"** is not a diagnosis. Change approach
  rather than resending.
