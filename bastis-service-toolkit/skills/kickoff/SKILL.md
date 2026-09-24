---
name: kickoff
description: "Two modes for a client kickoff. Prep mode builds a tailored kickoff-call agenda from the handover brief. Debrief mode (after the call) reconciles what was learned against what was expected and updates the open-questions list. Use when the user says 'kickoff agenda', 'prep the kickoff', 'kickoff debrief', 'what did we learn at kickoff'. Files agenda and debrief into the project's deliverables/ folder."
---

# Kickoff — Prep & Debrief (task)

> **First, run `refresh-check`** (lightweight, automatic): it does a cheap ID-only
> check for new calls and pulls summaries for any genuinely new ones before this
> task reads context. It's near-instant when nothing's new and silent unless it
> pulls something. Then proceed.


One task, two modes. Pick from the request; ask if ambiguous. Read
`PROJECT-STRUCTURE.md` to resolve the project and paths.

## Inputs
- `deliverables/handover-brief.md` — primary input (if missing, suggest running the
  handover-brief task first; can proceed from context if needed).
- For debrief: the kickoff call in client `All Calls/` (suggest `/update-context` if
  it isn't pulled yet).

## Prep mode → `deliverables/kickoff-agenda.md`
Ask 60 or 90 minutes if unstated. Tailor to THIS client from the handover brief:
icebreaker framing, alignment check (goals/pain points), stakeholder mapping, 5–8
smart questions drawn from the brief's open questions/red flags, next steps.
Time-box to the chosen duration.

## Debrief mode → `deliverables/kickoff-debrief.md` + `deliverables/open-questions.md`
Compare expected (handover brief) vs learned (the call): confirmed/corrected
assumptions, new info, new risks. Update `open-questions.md` (living list) — resolve
answered, add new.

## After
Prep: lead with the smart questions. Debrief: lead with corrected assumptions and
new risks. Don't invent what was said; if the call is summary-only and thin, say so.
