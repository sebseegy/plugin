---
name: solution-card
description: "Capture reusable learnings from a finished engagement — a Solution Card for the shared Solution Library and a short Claude Context Update that makes future similar projects smarter. Use when the user says 'solution card', 'capture learnings', 'add to the solution library', 'context update'. Reads the project's full history; files outputs into the project's deliverables/ folder (and notes where to file them in the shared library)."
---

# Solution Card & Learnings (task)

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


Distill the finished engagement into reusable knowledge. Read `PROJECT-STRUCTURE.md`
for project resolution and paths.

## Inputs
The project's full `deliverables/` and `docs/`, and the closure package if present.
Anonymize client specifics when output is destined for shared libraries (ask). Never
carry raw `commercial`-tagged terms (pricing, contract specifics) into shared outputs.

## Outputs
**`deliverables/solution-card.md`** (for the shared Solution Library): industry/
company profile (anonymized if needed), use case in one sentence, workflows solved,
monday architecture summary (boards, key automations, integrations), what made it
complex/unique, what worked (reusable patterns), what to avoid, delivery complexity
Low/Medium/High.
**`deliverables/claude-context-update.md`** (for the Services Hub KB): a 200–300 word
paragraph framed "When you see a client that looks like X, here's what matters…"

## After
Point to where both outputs should be filed (Solution Library and Services Hub KB).
Base the card on what actually happened; mark anything generalized as such.
