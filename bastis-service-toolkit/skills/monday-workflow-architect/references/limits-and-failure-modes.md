# Workflow limits, pricing, and failure modes

Snapshot date: August 2026, with two live verification passes layered on top
of the original monday-all Knowledge Base article: `#ask-ai-workflows`
(Aug 27, 2026, Workflow Builder-focused) and `#ask-automation-builder`
(same week, classic Automations-focused). Sections below are marked either
from the KB article (older, already-stale rollout timeline) or from a live
Slack pass (current as of the dates above). **Always verify current numbers
via `monday-scaling-watch` before quoting one to a client** — even the
live-verified figures here will drift; this file just gives you a much better
starting point than guessing.

**Table of contents**
- [Active workflow limits by tier](#active-workflow-limits-by-tier) — Standard/Pro/Enterprise numbers, CRM-Pro caveat, Enterprise exceptions, the separate-quota nuance
- [Structural limitations of Workflow Builder itself](#structural-limitations-of-workflow-builder-itself) — single-board/single-trigger, mirror columns, missing triggers, MLS bugs
- [AI credit consumption](#ai-credit-consumption-last-confirmed)
- [Failure modes worth designing around](#failure-modes-worth-designing-around) — disabling vs. silent vs. archiving, creator single-point-of-failure, same-trigger race condition
- [Classic Automations — additional live-verified limitations](#classic-automations--additional-live-verified-limitations-aug-2026-ask-automation-builder) — builder-UI regressions, template carryover, ownership friction, audit gaps
- [Where to check for movement](#where-to-check-for-movement)

## Active workflow limits by tier

| Tier | Active workflows included | Source |
|---|---|---|
| Standard | 3 | KB article (unverified live) |
| Pro | **20** (bumped up from 5 on Aug 10, 2026) | Live Slack — multiple threads confirm the rollout, though at least one customer reported the bump not landing on schedule, so treat "20" as the target, not a guarantee for every account |
| Trial / NGO | 20 | KB article (unverified live) |
| Enterprise | **250**, confirmed still current and actively enforced | Live Slack — several live tickets this week about accounts hitting exactly this ceiling |

**CRM Pro is a separate case.** At least one live thread shows CX being unable
to find internal documentation for why **Pro accounts under monday CRM cannot
get the same 5→20 workflow limit increase that Work Management Pro accounts
got.** If a client is on CRM Pro specifically (not WM Pro), do not assume the
20-workflow bump applies — confirm their exact plan/product combination before
scoping, and flag this as a genuine open question if it matters to the
engagement.

**Exceptions to the 250 Enterprise cap exist but are not durable.** Strategic
accounts have gotten temporary exclusions from the cap during an active
support issue (e.g. to allow duplicating workflows while migrating), and at
least one case shows an account's exception being **silently removed at
renewal**, re-triggering the same limit problem. Never tell a client an
exception is permanent — if one is granted, say explicitly that it may need
to be re-requested at renewal.

Add-on bundles (KB article, **verify before quoting**): Enterprise +100
workflows / $5,000/year. Pro yearly +20 workflows / $2,500/year. Pro monthly
+20 workflows / $250/month. Both tiers can purchase multiple bundles. Add-on
purchase is not self-serve — routed through the account owner (touch accounts)
or CX Billing payment link (no-touch accounts).

Classic board Automations run on a separate quota and don't compete with the
active-workflow cap — that's one more reason to prefer a classic Automation
when Gate 0 says a simple trigger→action pattern will do. Note the reverse
risk too, seen live this week: a client running everything through classic
Automations hit **"your account is experiencing delays based on the total
number of automations running"** — the separate quota is real, but it isn't
infinite either, and heavy automation use can degrade performance in ways a
migration to Workflow Builder can relieve (worth raising if a client is
already automation-heavy and complaining about lag).

**Correction — there may be more than one limiting mechanism, not just
active-workflow count.** A live thread shows CX confirming, for a **monday
Service, seat-based** customer, a distinct **automation quota that resets
monthly** (the customer asked to be reassured it would reset "on the 1st").
That's a genuinely different mechanism from the active-workflow-count cap
described above, and it appears tied to product (Service) and seat count
rather than a flat per-tier number. Don't assume every account's automation
limit works the same way — when scoping, ask which product the automations
live under (WM / CRM / Service / Dev) and whether the client has ever hit an
automation-limit message, rather than reasoning purely from the
active-workflow table above.

## Structural limitations of Workflow Builder itself

Gate 0 in the main skill focuses on what classic Automations can't do — but
Workflow Builder has its own real ceilings, confirmed live in `#ask-ai-workflows`
as of Aug 27, 2026. Don't oversell it as a strict upgrade; check these before
promising a design will work as described:

- **One workflow triggers from exactly one board — no multi-board trigger.**
  A live example: a client needed the same logic ("when Editor status changes
  to staffed, send the item to a master board") across 7 producer boards, and
  had to hand-build ~15 near-identical workflows (items + subitems per board)
  because a single workflow can't listen across boards. No roadmap commitment
  to fix this was found in the thread. **If a design needs identical logic
  across many boards, tell the client upfront that today's answer is N
  near-duplicate workflows maintained by hand** (or a board-consolidation
  redesign, which is a `monday-solution-architecture` conversation) — don't
  quietly discover this mid-build.
- **One workflow supports one trigger at a time**, not multiple trigger types
  feeding the same flow. This was flagged as a roadmap item months ago and, as
  of this scan, is still not shipped — treat "multiple triggers, one workflow"
  as not currently possible.
- **Mirror columns are not usable as inputs inside workflow blocks at all**,
  and any **formula column that references another formula, a mirror, or a
  creation-log column** is not selectable in workflow blocks either (only
  "plain" formulas, and only "convert text to number" on formula outputs that
  meet that same restriction). This is a significant real-world blocker
  because mirror columns are extremely common on boards that roll data up
  across connections — check for mirror dependency early, not after the block
  won't let you select the column.
- **The "when person is assigned" trigger does not exist in Workflow Builder**
  as of this scan, even though it exists in classic Automations — Workflow
  Builder is not a strict superset of Automation triggers. Always check both
  the Automations trigger list and `references/blocks-catalog.md` for the
  *specific* trigger a design needs rather than assuming Workflow Builder can
  do anything Automations can, only more.
- **No Slack "wait for response" block** — Teams has one, Slack doesn't yet.
  If a client wants a Slack-based human-in-the-loop/approval pattern, the
  documented workaround is the email-based wait block, not a native Slack
  equivalent.
- **Loop blocks have inconsistent column-type support**, confirmed live on two
  separate column types: changing a **Number** column across all subitems
  inside a loop wouldn't let the column be mapped, and changing a **Timeline**
  column on a subitem inside a loop left the Value field greyed out and
  unselectable. Don't promise a loop-based bulk-update design until you've
  confirmed the specific column type works inside a loop for that account.
- **Multi-Level Subitem (MLS) boards have live correctness bugs**, not just
  limitations: a status-change trigger with a "change item name" or
  status-label action was reported firing correctly on the trigger but
  applying the *action* to the top-level parent item instead of the actual
  triggered (sub-)item. Treat MLS boards as **higher-risk and needing extra
  test coverage** — verify the action actually landed on the item you expect,
  not just that the workflow ran without error.
- **No loop-detection guardrail at creation time.** monday doesn't currently
  warn you if a workflow you're building could create an infinite loop —
  that's on you to reason through and test for, `validate_workflow` doesn't
  catch it structurally.
- **AI credit consumption isn't visible per-workflow in a self-serve way.**
  Customers have asked for a breakdown of exactly how many AI credits a
  specific AI-powered workflow consumed and there's no clean answer as of this
  scan — don't promise a client granular self-serve credit reporting per flow.

## AI credit consumption (last confirmed)

Each AI-powered block (translate, improve, custom, smart condition, search the
web, call agent) drew **8 AI credits per execution of that specific block**,
charged only when the workflow actually reaches and executes it — a block
skipped by an earlier condition or stopped by an error isn't charged. A flow
with two AI blocks in sequence draws credits for each independently. Verify the
current per-block rate before estimating a client's AI spend; credit pricing
models change more often than the block catalog itself.

## Failure modes worth designing around

This section is drawn from internal engineering discussion (Slack), not public
docs — treat it as operational folklore that's proven reliable, and re-confirm
anything load-bearing for a client commitment.

**Disabling errors vs. silent errors vs. archiving.** Not every failure behaves
the same way, and the difference matters for how defensively you design:

- **Disables the flow + notifies the creator (not every listed owner):** the
  failure class is one that will recur on every run and can't self-resolve —
  e.g. a referenced column, group, board, or workspace no longer exists; a
  referenced status label was deactivated; a formula-to-mirror configuration
  isn't supported; the account hit a board-size or connected-items ceiling;
  the flow isn't authorized against a board anymore. Guard against these by
  adding "if column is empty" / "if item is in this group" checks around
  anything that assumes a resource a client might delete or rename still
  exists — clients reorganizing their own boards is the single most common
  way a working flow silently stops working. **Confirmed live:** the failure
  notification goes to the workflow's *creator* specifically — other users
  added as workflow *owners* are not notified. A strategic account (PepsiCo)
  raised exactly this as a gap. If a build has multiple stakeholders, tell
  them explicitly that only the creator gets pinged on failure, and consider
  who that should be.
- **The "Fix it here" link on a deactivated-status-label error is currently
  broken** — it's been reported across multiple accounts as leading to a 404
  instead of the fix flow. Don't tell a client to click it; walk them through
  manually reactivating or remapping the status label instead.
- **A single unconfigured block can silently kill an entire workflow's other,
  working triggers.** A real traced bug: an "Every time period" block that a
  user added but never finished configuring threw an unhandled error during
  listener setup, and because that setup runs as one sequential pass with no
  per-block isolation, it prevented the workflow's *other*, fully-configured
  trigger from ever firing — with no obvious error pointing at the real cause.
  Takeaway: don't leave half-configured blocks sitting in a workflow "for
  later," even ones that look inert — `validate_workflow` is meant to catch
  this, but confirm zero unconfigured blocks remain before publishing, not
  just that validation returned clean once.
- **Some blocks have been observed disappearing from a saved workflow shortly
  after being configured**, breaking a setup that worked minutes earlier with
  no warning (seen on a Gmail "wait for response" block). Areas of the
  catalog that are newer or beta-flagged are more prone to this — re-verify a
  build is still intact immediately before a client demo or go-live, don't
  assume yesterday's working state persisted untouched.
- **A workflow's *creator* being deactivated breaks all of that person's
  workflows even if other users are listed as owners** — confirmed live, and
  reactivating the creator brings the workflows back active but **wipes their
  run/activity history** in the process. This is a real single-point-of-failure
  risk for any business-critical build tied to a named individual. Recommend
  building under a dedicated service/admin account as the creator for
  anything business-critical, decided **before** build, not discovered when
  someone leaves the company.
- **Multiple workflows sharing an identical trigger, differentiated only by
  condition, can race and fire the wrong one.** A live report: ~10 workflows
  all triggered on "when column changes" with different dropdown-label
  conditions; triggering one correctly-matching event instead fired a
  *different* workflow with a different condition on the same trigger. This
  directly affects this skill's own "decompose into named flows" advice —
  **when several candidate flows would share the exact same trigger type on
  the same board, prefer one workflow with multi-branch conditions over
  several separate workflows on that trigger**, specifically to avoid this
  race condition, not just for readability.
- **Disables the flow + prompts to reconnect:** credential-expiry classes
  (Slack token revoked, Gmail/Outlook grant invalidated, Salesforce/Jira/Zendesk
  auth expired). These recover once the user reconnects the account — nothing
  to defend against in the design itself, but worth mentioning in a handover so
  the client's admin knows what a "reconnect account" prompt means.
- **Disables silently, no notification:** deprecated recipe types, a board the
  creator no longer has access to, an unauthenticated creator. These are the
  most dangerous for a client relationship because nobody gets told — if you're
  handing off a build, make sure the client knows to periodically check the
  Autopilot hub / automation center rather than assuming "no error email" means
  "still running."
- **Auto-disables after volume, not a specific error:** a flow or automation
  that racks up too many failed runs in a short window (last confirmed
  threshold: roughly 200 failures/hour) gets disabled as a platform safety
  valve, independent of what's causing the failures. If a flow is high-volume
  and even a small per-run failure rate is expected (e.g. an external API that
  occasionally times out), this is a real risk — design retry/backoff or a
  dead-letter path rather than letting failures accumulate silently toward that
  ceiling.
- **Archives instead of disabling:** connection revoked or the creator's
  account deactivated — this cascades to the whole account's automations in the
  legacy automation engine, but only the single flow in the newer
  workflow-builder path. Worth knowing which engine a client is on before
  promising "if one person leaves, only their flows are affected."

**Sharing a workflow that uses someone's personally-connected tool** (their own
Slack/Gmail/Salesforce connection) requires that person's explicit consent
before the flow can be shared with other users — as of recent platform changes
this is now supported (previously a tool-connected flow couldn't be shared at
all), but it's a real approval step in the build sequence, not a formality. If
your design depends on a specific person's personal integration, flag it in the
"Dependencies & risks" section of the design doc so it doesn't surface as a
surprise blocker at go-live.

## Classic Automations — additional live-verified limitations (Aug 2026, `#ask-automation-builder`)

These are specific to the classic Automations engine and go beyond the
structural "no branching / no external reach" limitations in the main skill's
Gate 0 — they're things that can break a build that otherwise clears Gate 0
cleanly.

- **The current automation-builder UI has quietly dropped capabilities the
  older UI had — don't assume feature parity with a pattern that used to
  work.** Two confirmed live regressions: the "create subitem" action can no
  longer set a **fixed/static status label** on the new subitem (only
  board/parent-item values are offered now), which broke at least two client
  builds that used static subitem labels as a deliberate "tag" to drive
  further automation logic; and the "create from template" action lost the
  ability to pick a **destination folder** when configured from a
  status-change trigger. If a design leans on either pattern, verify it's
  still available in the account's current builder before promising it —
  and if a client says "this used to work," believe them and check for a
  builder-version regression before assuming user error.
- **Formula columns referencing a creation-log column are blocked from
  automation recipes too**, not just Workflow Builder — confirmed live: a
  formula using a creation-log column as a variable can no longer be mapped
  into a "change column value" action. Whether a formula can be used to
  *trigger* a recipe directly is unclear/unconfirmed as of this scan — verify
  rather than assume it works.
- **Multi-Level Subitem (MLS) boards have the same item-vs-parent bug in
  classic Automations that Workflow Builder has** (see the MLS note in
  `references/blocks-catalog.md`) — this is a systemic engine issue, not
  specific to one builder. Two additional MLS-specific findings live: setting
  an item **date** via automation on an MLS board can report success in the
  run history while **silently not applying the change at all** — don't trust
  a green run-history entry as proof the value actually changed on an MLS
  board, spot-check the item; and dependency-cascade automations ("when
  status changes to X, change its dependency's status to Y") are **not
  currently available for Multi-Level boards** at all.
- **Legacy automations can silently stop resolving merge fields after a
  platform infra migration**, with no auto-migration and no error. A live
  example: automations built before a recent infra release kept "triggering
  successfully" per the run history, but the actual email sent showed
  unresolved placeholder text (literally `{employee's Name}'s hello
  {employee's Case Manager}`) instead of real values — fixed only by manually
  re-opening and re-saving the recipe. If you're inheriting or auditing a
  client's older automations, don't trust "still triggering" as proof the
  output is still correct; spot-check actual delivered output, especially
  after monday ships a builder infra update.
- **App-created and managed-template-baked automations have real ownership
  friction.** A webhook/API automation created by an app cannot simply be
  reassigned to a new owner — it has to be rebuilt, which matters a lot when
  a client's technical champion leaves. Separately, an automation baked into
  a **Managed Template** forces its original creator to remain listed as
  owner on **every board spawned from that template**, with no confirmed way
  to avoid it. If you're building automation into a template that will be
  reused across a client's account, decide up front whose name that should
  be under — ideally a service/admin account, per the same reasoning as the
  workflow-creator single-point-of-failure note above — because unwinding it
  later is not straightforward.
- **Self-service audit trails have real gaps.** There's no way to see *who
  deleted* an automation (only the original creator shows). Subitem
  automations aren't listed as visibly as parent-item automations in the
  Automation Center, making them easy to lose track of. And feedback from an
  Enterprise customer (echoed internally) describes the Autopilot hub /
  connections view as "half complete" — it can say an app is used on a board
  when the board's own automation list shows nothing, with no way to tell
  whether that's stale metadata or something leadership set up historically
  that's risky to touch. **Practical takeaway: don't rely on monday's own
  admin views as the system of record for what a client has built — keep
  your own documentation** (this is exactly what `monday-build-docs` is for)
  so a client isn't left guessing what's safe to delete years later.
- **Mirror-column support in Automations is a partial, staged rollout, not a
  flat yes/no.** Live threads show mirror columns becoming available as
  automation *conditions* for some accounts before others, and a mirrored
  email column becoming usable as a *send-email* target for some accounts
  before others — both mid-rollout as of this scan. Check the specific
  account rather than assuming mirror support based on what worked
  yesterday for a different client.
- **AI-related costs and limits are more varied than a single flat rate:**
  different AI-powered actions can draw different credit amounts depending on
  what they do (e.g. a web-search/enrichment action vs. a simpler text
  action) — don't quote the "~8 credits" figure elsewhere in this file as a
  universal constant across every AI action. Separately, **some automation
  actions require purchasing AI credits to even enable them**, regardless of
  whether the action is obviously "AI-branded" in the UI — a real, current
  source of client confusion worth pre-empting in a proposal. The AI-block
  instruction/prompt length limit was recently raised from 1,000 to 3,000
  characters (per an internal engineering fix landed Aug 3, 2026) — verify
  the current limit before designing a long AI-block prompt around the old
  number.
- **No documented execution-order/priority when multiple recipes could act on
  the same field.** A live question ("if two automations both change project
  health based on different status/percentage conditions, which one wins?")
  went unanswered with a clear rule in the thread — treat overlapping
  automations on the same target field as **undefined behavior** and design
  to avoid the overlap (consolidate into one recipe or one Workflow Builder
  multi-branch condition) rather than relying on an assumed precedence order.
- **Automations attached to a board template don't reliably carry over to
  boards created from that template.** A live report shows a template's only
  automation simply not appearing on a new board created from it. If a design
  relies on "create board from template" carrying its automations along
  (the Closed-Won → onboarding-project pattern elsewhere in this skill is a
  good example), **verify the automation actually exists on the newly created
  board** as an explicit test-plan step — don't assume it inherited cleanly.
- **Outlook calendar sync automations pull every event with no category
  filter.** The native Outlook→monday calendar integration recipe has no way
  to filter which events become items before they're created — it's all or
  nothing. If a client wants selective sync (e.g. excluding personal/internal
  events from a shared board), that's a known gap with no native recipe-level
  fix as of this scan; the honest answer is "not currently possible natively,"
  not a configuration you haven't found yet.
- **Link column automations overwrite the configured display text.** An
  automation that sets a Link column's value always sets "Text to Display" to
  the raw URL, ignoring whatever default display text was configured on the
  column — a small but concrete gotcha worth testing for if a design touches
  Link columns via automation.

## Where to check for movement

`monday-scaling-watch` already knows how to sweep Slack for changes to
platform limits; point it at this file's specific numbers (active-workflow
caps, add-on pricing, AI credit rate) rather than re-deriving a search strategy
here.
