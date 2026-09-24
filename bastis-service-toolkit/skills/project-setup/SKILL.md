---
name: project-setup
description: "Create the shared-drive folder structure for an IC engagement — at whichever level is needed: a brand-new client (root + Client Context + All Calls + first SKU + first project), a new SKU/contract under an existing client, or a new project under an existing SKU. Builds the correct meta.json at each level. For a brand-new client it also runs setup-context to pull calls + account data. Use when the user says 'set up a project', 'new client', 'add a project', 'new SKU/contract', 'scaffold the folders', or points at an empty/new folder. Infers names from existing meta.json or the folder name rather than interrogating."
---

# Project Setup (scaffold the structure)

Create the client → SKU → project folder structure correctly so every other skill
can find and file things. Read `PROJECT-STRUCTURE.md` (in this plugin) for the exact
layout, the three meta.json shapes, and naming. This skill is the *structural*
counterpart to `setup-context` (which pulls calls/account data).

## Step 0 — check what already exists FIRST (mandatory, before creating anything)

This skill is **idempotent**. Re-running it must never duplicate, overwrite, or
re-pull anything that already exists. Before creating anything:

1. **Read local synced files** (the client folder is on disk — read it directly; use
   the Drive connector only as a fallback if something genuinely isn't synced). Check
   only what's relevant to what you're creating — **don't inventory the whole client
   or wander into other projects/SKUs.**
2. **Establish what you're being asked to create** (see Step 1). If it's a new
   project under an existing client, you only need to confirm the client and the
   target SKU exist (read their `meta.json`) and that the project folder doesn't
   already exist — nothing more. You do NOT need to survey every SKU or contract.
3. In every create step below, **only create what's missing.** If a folder or
   `meta.json` already exists, leave it untouched ("already present") — never
   overwrite or "refresh" it. If an existing `meta.json` lacks a field, add only that
   field; don't rewrite the file.
4. Filesystem is case-insensitive — never make a case-variant duplicate.

If everything for the requested scope already exists, do nothing structural and just
report it's already in place.

## Step 1 — figure out what level you're creating, by inference

Look at where you are and what already exists — don't interrogate the user. Resolve
names the way the rest of the toolkit does: **read a `meta.json` if present;
otherwise infer from the folder name and fill in the rest.**

- **Empty/new top-level client folder** (no client `meta.json`) → scaffold a **new
  client** (Step 2A), then its first SKU and project (2B, 2C). Steps 1b/1c (fetch all
  contracts, map all calls) and Step 3 (pull context) apply HERE — this is the only
  scope where the client-wide work is appropriate.
- **Adding a new project under an existing client** → this is the common case (e.g.
  a chat in the client folder, working a project folder like "UKTV"). **Scaffold just
  that one project (Step 2C).** Confirm the client + target SKU exist by reading their
  `meta.json` locally; if the SKU isn't obvious, ask which contract it sits under
  (don't survey them all). **Do NOT re-fetch contracts, do NOT re-pull context, do
  NOT inventory other SKUs/projects.** At most, map *this* project against existing
  calls (Step 1c, scoped to this one project) so it has its context.
- **Adding a new SKU/contract under an existing client** → scaffold that SKU (2B) and
  usually a first project (2C). Don't re-pull context.

If genuinely ambiguous which scope (e.g. a bare folder that could be client or
project), **ask** — don't go inventorying the client folder to infer it.

## Step 1b — (NEW CLIENT ONLY) fetch the contracts and scaffold the whole client

**Only when scaffolding a brand-new client.** Skip this entirely when adding a
project (or SKU) to an existing client — don't re-fetch or re-survey contracts.

The contracts on an account ARE its SKU level — so when setting up a **new client**,

1. Query Kremer: `cco.l3.dim_delivery_solutions` filtered by `pulse_account_id`
   (resolve the account as in setup-context). For each won/active service line pull:
   `product_name`, `product_identifier_sku`, `product_group`, `is_recurring`,
   `service_start_date`, `service_end_date`, `opp_stage`/status, `plan_tier`,
   `platform_type`, and the project-delivery fields (`project_status`,
   `project_kickoff_date`) if present. (Kremer quirks apply: poll
   `check-query-status`; force exact values; if it errors/empty, fall back to asking.)

2. **Scaffold a SKU folder for every contract found** (Step 2B per contract), with
   `engagement_type` derived per contract (`is_recurring`/MS product →
   `managed_services`; one-time implementation/tailored → `professional_services`;
   AI-Transformation/AITP → `aitp`; else `other`). Create an **empty `Projects/`
   folder under every SKU**, ready for projects to be added later.

3. **Infer where work is actually happening from the context we already have.** Use
   the calls (the `All Calls/` inventory + summaries), account overview, and any
   delivery/project fields from the contract data to judge which contract(s) have
   live project work — e.g. recent discovery/build calls tied to a contract, or a
   contract with an open `project_status`. Propose the project(s) accordingly:
   "Calls suggest active work under MS-10 (PMO build) — shall I create that project?"
   Don't force the consultant to place everything by hand when the context already
   implies it. State your inferences and let them confirm/correct.

4. **Ask only for what context genuinely can't supply** — typically the project
   *name* (an internal delivery unit, not a warehouse field), and confirmation of
   ambiguous placement. Don't ask for SKU names, engagement types, or which
   contracts exist — those are fetched. The ideal prompt is: "I've set up all 5
   contracts as SKUs; calls point to active work under <X> — what do you want to
   call that project?"

If the fetch genuinely returns nothing, fall back to inferring SKU/project from the
folder name and asking for the missing pieces.

## Step 1c — MAP calls to the project(s)

For a **new client**: map all the client's calls across the projects just created.
For **adding one project** to an existing client: map only against *that* new project
(tag the calls that serve it; don't re-tag the whole client or touch other projects).
Either way, this is what makes "find the right context for this project" fast — read
the local `call-inventory` and tag, don't re-fetch call content.

1. For each call in `All Calls/` (read the `call-inventory` Sheet — don't re-fetch
   content unnecessarily; the summaries are enough to judge relevance), infer which
   project(s) it serves from: the call's themes/title/summary, participants, and date
   versus each contract's window/kickoff (`service_start_date`/`project_kickoff_date`
   from Step 1b). A call about CRM rollout work maps to the CRM project; a commercial
   renewal call maps to none.
2. **Auto-tag silently** — write your best inference into the `projects` column of
   the `call-inventory` row (and the call file's `projects:` header). A call may map
   to **multiple projects**; a call that serves the relationship broadly or matches
   no project gets `general` (client-level), not left blank. Don't interrogate the
   consultant call-by-call — just tag, and tell them at the end how many calls were
   mapped to each project and that they can correct any.
3. **Every call ends up tagged** — to one or more projects, or `general`. None left
   ambiguous/blank. If a call is genuinely unclear, tag `general` and note it rather
   than guessing a specific project wrongly.
4. This also runs when a **new project is added later** to an existing client: map
   the existing calls (especially recent ones) against the new project too — an old
   call can become relevant to a newly-created project.

The result: a project task can filter `call-inventory` by its project tag and
immediately have the right calls, instead of scanning everything.

## Step 2A — new client

At the client root create: client `meta.json` (`level: client`, name, empty `skus`,
null sync/account fields, empty `call_sources`), `Client Context/`, and `All Calls/`.

## Step 2B — new SKU / contract

Under `SKU level/<SKU name>/` create: SKU `meta.json` and `SKU Context/`, plus an
(empty) `Projects/` folder. Add the SKU name to the client `meta.json` `skus` list.
When scaffolding from fetched contracts (Step 1b), do this once per contract.

Keep SKU `meta.json` **lean — enough to orient, nothing that goes stale.** Include:
`level`, `client_name`, `sku_name`, `sku_code` (the `product_identifier_sku`, e.g.
"MON-V9-PSPRJ"), `engagement_type`, `status` (open/closed), and the contract window
`service_start_date`/`service_end_date`. Do NOT copy volatile figures (hours
remaining, ARR, seat counts) — those drift and would rot in a file; query them fresh
from the warehouse when a skill needs them. A short free-text `note` summarizing what
the contract covers (from `product_name`/`product_group`) is fine.

## Step 2C — new project

Under `SKU level/<SKU>/Projects/<Project name>/` create: project `meta.json`
(`level: project`, `client_name`, `sku_name`, `project_name`) and the three working
folders **`inputs/`, `deliverables/`, `docs/`**. Add the project name to the SKU
`meta.json` `projects` list.

Create folders/files with the file tools (they sync to Drive); the filesystem is
case-insensitive, so don't create case-variant duplicates of an existing folder.

## Step 3 — context (NEW CLIENT ONLY, and only if not already populated)

Run `setup-context` **only when you have just created a brand-new client AND
`All Calls/` is empty / has no `call-inventory` yet** (confirm from Step 0). This is
the expensive step — re-pulling 100+ call summaries on a client that already has
them is exactly the "weird stuff on re-run" to avoid.

- New client, no calls yet → run `setup-context` (pulls all calls + account data).
- Client already has calls (you re-ran this skill, or only added a SKU/project) →
  **do NOT run `setup-context`.** At most run `refresh-check` to catch anything new.
- New SKU or new project under an existing client → never re-pull; the client-level
  calls are shared. The new project claims relevant calls via tagging as its tasks
  run — no re-fetch.

If unsure whether calls exist, check `All Calls/` and the client `meta.json`
`last_context_sync`/`call_sources` before deciding — when in doubt, do NOT re-pull.

## Output

Confirm what was created (which level, the folders + meta.json files), and the one
natural next step — for a new client/project, that's usually pointing the consultant
at `services-help` or the first relevant delivery task. Keep it short. Don't fabricate
account or call data here — Step 3 / setup-context owns that.

## Defensive rules
- **Idempotent (see Step 0):** re-running never duplicates, overwrites, or re-pulls.
  Only create what's missing; leave existing folders/meta untouched.
- Never re-pull context for a client that already has calls.
- If you can't tell which client/SKU a new project belongs under, ask once rather
  than guessing wrong — filing a project in the wrong place is costly.
