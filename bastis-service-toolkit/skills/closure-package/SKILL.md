---
name: closure-package
description: "Produce a three-part project closure package — a client-facing closure report, an internal delivery retrospective (scope changes, timeline vs plan, risks that materialized), and a Customer Success handover brief with relationship context. Use when the user says 'close the project', 'closure package', 'wrap up the project'. Reads the project's full deliverables history; files outputs into the project's deliverables/ folder. (Professional-services task; managed services rarely closes.)"
---

# Closure Package (task)

> **First, run `refresh-check`** (lightweight, automatic): it does a cheap ID-only
> check for new calls and pulls summaries for any genuinely new ones before this
> task reads context. It's near-instant when nothing's new and silent unless it
> pulls something. Then proceed.
>
> **Environment guard — before judging any build progress:** read `build.stage` in
> the project `meta.json`. If it's `transferred`, `client_build` or `live` and the
> client account has no MCP access, do NOT call anything "not done" or "missing"
> because it isn't in the Spaces/demo account — that workspace is a stale snapshot.
> Use Notetaker calls, deliverables and Basti's confirmation instead, and mark
> board-level facts "unverified — in <client> account". If `build.stage` is missing
> or `unknown`, ask once where the build lives and save the answer. Details:
> "monday environments" in PROJECT-STRUCTURE.md.


Produce the closure package from the project's full history. Read
`PROJECT-STRUCTURE.md` for project resolution and paths.

## Inputs
The project's `deliverables/` (handover brief, process map, architecture spec, UAT
triage, go/no-go, hypercare reports), its `docs/`, and relevant client `All Calls/`.
Read binaries via the Drive connector; don't assume a mount listing is complete.

## Outputs — three documents
**`deliverables/client-closure-report.md`:** what was built vs original goals,
milestones/dates, training & adoption summary, recommended follow-on work.
**Client-safe HARD RULE** — exclude internal-only/commercial content.
**`deliverables/internal-delivery-summary.md`:** scope changes (grew/dropped),
hours/timeline vs plan if data exists, risks that materialized + handling, what to
do differently.
**`deliverables/cs-handover-brief.md`:** relationship context (who to talk to/avoid,
sensitive topics), known risks/watch items, expansion opportunities.

## After
Lead with scope changes and expansion opportunities. For polished client build docs,
delegate to `monday-build-docs`. Distinguish documented facts from inference; if
timeline/hours data doesn't exist, say so rather than estimating.
