---
name: monday-scoping
description: >-
  Scopes monday.com implementation work — runs discovery and turns the answers into a
  client-ready scope spec with workstreams, phasing, and effort estimates. Use this skill
  whenever the user wants to scope a build, "write a scope", "estimate this project",
  "put together a SOW / statement of work", "create a discovery questionnaire", "what
  questions should I ask the client", "how many hours is this", "break this into
  workstreams", or is planning a monday.com engagement (forms, boards, automations,
  approvals, dashboards) and needs to define and size it. Also triggers when a completed
  discovery questionnaire needs to be converted into a scope document, or when the user
  asks for help estimating monday build effort. Produces a discovery questionnaire and/or
  a filled scope spec, grounded in real delivery patterns rather than guesswork.
---

# monday.com Scoping

You help an implementation consultant scope a monday.com build: first **discovery** (asking
the right questions), then a **scope spec** (workstreams, phasing, and effort estimates the
client signs off on). The goal is a scope that's concrete, honestly estimated, and phased
around what's actually ready — not an optimistic guess.

Two bundled templates drive the output (in `assets/`):
- `Discovery-Questionnaire-Template.md` — blank questionnaire to send the client.
- `Scope-Spec-Template.md` — the scope document scaffold with ten workstreams + a time table.

## Step 0 — Figure out where the user is

Scoping is a pipeline; meet the user at their stage:

- **No requirements yet** → produce a filled-in copy of the **discovery questionnaire** for the
  user to send. Tailor the examples to their domain if you know it.
- **Has discovery answers** (a completed questionnaire, a transcript, or notes) → produce a
  **scope spec**. This is the main job.
- **Has a rough idea, wants a ballpark** → draft the scope spec from what's known, marking
  assumptions clearly and listing the open questions that would tighten the estimate.

If you're handed raw answers, read them fully before scoping. If a critical input is missing —
especially **volume** (see below) — ask one focused question rather than guessing.

## The single most important input: volume and repeating units

Most monday builds repeat across some unit — teams, regions, brands, categories, or "forces."
The cost is driven by **how many of those units** there are and **how many items/activities
flow through each**. On a real reference build (TITANs/PSP), the dominant cost driver was the
number of activities per playbook (ranging 19–84), because that set form size and how many
items each automation had to create. Always pin down:

1. How many repeating units? (list them)
2. Roughly how many items/activities per unit per cycle? (a range is fine)
3. Does one intake (e.g. a form submission) need to create **many** items? (this is heavier —
   see automations below)

Without these three numbers, an estimate is a guess. Get them, or state explicitly that the
estimate is provisional pending volume.

## Building the scope spec

Work through the template's ten workstreams. Include only what applies; add anything that
doesn't fit. For each included workstream, state what's being built and an estimate.

**Map discovery answers → workstreams:**

| Discovery answer | Drives |
|---|---|
| Repeating units + volume | Forms/intake count, automation size, boards |
| "How work begins" | Intake method (form / manual / import / integration) |
| Stages | Board groups, status columns |
| Validation/approval checkpoints | Approval-process workstream (one path per checkpoint) |
| Data points | Columns; connected-board/mirror needs |
| Who sees what | Permissions workstream (row-level = explicit setup) |
| Reporting audiences + their questions | Dashboards (one view per audience question) |
| Deadlines / data readiness | Phasing |

## Estimation heuristics (anchors, not promises)

These come from delivered work. Treat them as **starting points** and adjust to the actual
build; never present them as fixed prices.

- **Forms:** ~3h per form as a loose anchor; scales with field count and activity list length.
- **Automations (simple):** a basic "create item on submit" is light.
- **Automations (self-looping):** one submission → many items (one per activity) is materially
  heavier and may need splitting across multiple workflows due to platform limits. Scope and
  estimate these separately from simple automations, and flag the risk.
- **Approval process:** estimate per distinct approval/notification path, not per board.
- **Permissions (row-level):** "see only your own rows" = Viewer role + Visibility column +
  per-row assignment — three explicit steps, not a default. Don't treat it as free.
- **Dashboards:** estimate per audience, derived from the "audience needs" answers.
- **Discovery & design:** account for it even if partly done (mark completed portions).
- **Meetings:** reserve a standing weekly hour across the build window (e.g. 1h/wk × N weeks)
  rather than ad-hoc — covers requirements, demos, UAT, change requests.
- **Documentation/handoff:** a short runbook per system.
- **Contingency:** ~10% of delivery work is a reasonable buffer; apply it explicitly.

Always fill the **time-summary table** so the total is transparent (unit estimate × units per
workstream). If you've marked the estimate provisional, say so above the table.

## Phasing — sequence by readiness, not just the calendar

Phase the work by **what's ready**, not only by dates. On the reference build, workstreams with
finalized inputs started immediately while those awaiting client-provided specs were sequenced
after a named hand-off date. State plainly which parts can start now and which are blocked on
what (and by when), so the client sees the critical path.

## Recommended monday patterns to bake into scope

When the discovery answers fit these shapes, name the pattern in the spec so the build approach
is explicit:

- **Collector board** — many submissions/sources feeding one hub board.
- **Self-looping automation** — one submission generating one item per activity.
- **Connect-boards + mirror + formula** — pulling values across boards and aggregating.
- **Viewer + Visibility column** — row-level "see only yours" access.
- **Submission link for re-entry** — letting users edit a prior form submission.

## Honesty and limitations

- Where the monday UI exposes something the API/automation can't replicate, record it as a
  **known limitation / assumption** rather than implying parity.
- Keep assumptions and out-of-scope items explicit — they protect both sides at sign-off.
- If you don't have enough to estimate a workstream, say so and list what you'd need.

## Output

Deliver the questionnaire and/or scope spec as **Markdown** by default, built from the bundled
templates, saved into the project's **`deliverables/`** folder (resolve the project per
`PROJECT-STRUCTURE.md`; if no project is in play, ask which one or save where the consultant
asks). Offer a polished **.docx** version for client delivery
(use the docx skill). Before sending to a client, remove the `>` scoping-tip blockquotes from
the templates — they're internal guidance. End by flagging any open questions that would
materially change the estimate.
