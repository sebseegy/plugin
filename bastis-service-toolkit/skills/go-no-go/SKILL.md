---
name: go-no-go
description: "Produce a Go/No-Go launch assessment — checks everything built against the original requirements, lists open UAT blockers and go-live risks, assesses training status, delivers a GO/NO-GO verdict — then drafts a client-facing launch email and an internal CS handover note. Use when the user says 'go/no-go', 'launch assessment', 'are we ready to launch', 'launch email'. Files outputs into the project's deliverables/ folder."
---

# Go / No-Go (task)

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


Decide readiness and prepare launch communications. Read `PROJECT-STRUCTURE.md` for
project resolution and paths. (Typically a professional-services task; managed
services may not use it.)

## Inputs
`deliverables/handover-brief.md` (original requirements), `architecture-spec.md`
(what was built), `uat-triage.md` (open blockers), `process-map.md`.

## Outputs
**`deliverables/go-no-go-report.md`:** requirements coverage (each Done · Partial ·
Missing), open UAT blockers, go-live risks + mitigations, training status, VERDICT
(GO/NO-GO + one-paragraph rationale).
**`deliverables/launch-email.md`** — client-facing. **Client-safe HARD RULE:** only
client-safe, project-relevant content; no internal risk language or commercial terms.
**`deliverables/cs-handover-note.md`** — internal, account state for Customer Success.

## After
Lead the summary with the verdict and any Missing/Partial requirements. Base coverage
on documented requirements vs documented build; flag unknowns rather than assuming Done.
