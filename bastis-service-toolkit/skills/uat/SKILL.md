---
name: uat
description: "Two modes for UAT. Script mode builds a non-technical UAT test script from the architecture spec and process map. Triage mode categorizes UAT feedback into bug / scope creep / training gap / nice-to-have / blocker with a prioritized fix list and effort estimates. Use when the user says 'UAT script', 'test script', 'triage UAT feedback', 'categorize the UAT results'. Files outputs into the project's deliverables/ folder."
---

# UAT — Script & Triage (task)

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


One task, two modes. Pick from the request; ask if ambiguous. Read
`PROJECT-STRUCTURE.md` for project resolution and paths.

## Inputs
- `deliverables/architecture-spec.md` (primary for script mode),
  `deliverables/process-map.md`, project `inputs/feedback-notes/` (for triage).
- If the architecture spec is missing, suggest running `solution-build` first.

## Script mode → `deliverables/uat-test-script.md`
Per scenario: name + which workflow it covers, who runs it (role/persona),
step-by-step instructions for a **non-technical** user, expected outcome, pass/fail
criteria, edge cases.

## Triage mode → `deliverables/uat-triage.md`
Categorize every feedback item as **Bug · Scope creep · Training gap · Nice-to-have
· Blocker**; prioritized fix list with rough effort and owners.

## After
Triage: lead with blockers and scope-creep (the decisions needing a human). Don't
invent feedback; keep test steps genuinely non-technical.
