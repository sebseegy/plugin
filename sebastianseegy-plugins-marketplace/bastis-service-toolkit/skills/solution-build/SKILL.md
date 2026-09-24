---
name: solution-build
description: "Orchestrates building a monday.com solution for a project — turns the process map and handover brief into an architecture and (for demos/client workspaces) builds it after explicit approval. Delegates the design method, API discipline, formulas, AI features, scaling checks, and documentation to the craft skills. Use when the user says 'design the solution', 'architecture spec', 'build the monday setup', 'build the demo', 'now build it'. Files outputs into the project's deliverables/ and docs/ folders."
---

# Solution Build (task, orchestrator)

> **First, run `refresh-check`** (lightweight, automatic): it does a cheap ID-only
> check for new calls and pulls summaries for any genuinely new ones before this
> task reads context. It's near-instant when nothing's new and silent unless it
> pulls something. Then proceed.


Drive the build for a project and file its deliverables. Does NOT re-implement the
build method — **delegates to the craft skills**. Read `PROJECT-STRUCTURE.md` for
project resolution and paths.

## Inputs
- `deliverables/process-map.md` (primary), `deliverables/handover-brief.md`,
  `deliverables/internal-gaps.md`, project `inputs/solution-templates/`.
- If the process map is missing, suggest running `discovery-synthesis` first.

## Delegation
1. **Design → `monday-solution-architecture`** (archetypes, one-board-per-unit,
   topology, connections; it pulls `monday-scaling-watch` for limits and
   `aitp-advisor` when AI is in scope). Capture the written design as
   `deliverables/architecture-spec.md`.
2. **AI features → `monday-ai-advisor`** (routes to `monday-agents`,
   `monday-sidekick`, `monday-ai-columns`, `monday-vibe`); reflect choices in the spec.
3. **Formulas → `monday-formulas`.**
4. **Build it (demo/client workspace) → `monday-solution-architecture` build half**,
   under the approval gate below.
5. **Document → `monday-build-docs`** (writes to `docs/`).

## Approval gate (building in a real/demo workspace)
**Propose first, build second — always.** Lay out the plan, wait for explicit
approval ("go"/"build it"), redraft+re-confirm if edited. Build in dependency order
(folders → boards → columns → groups → connect/mirror → items → values → automations
→ dashboards → forms → docs → views). If something fails, stop, show what was built,
ask — don't guess.

## Outputs
- `deliverables/architecture-spec.md` — the written design.
- `deliverables/monday-api.json` — ready-to-run JSON for the first board (verify
  field shapes against the API first).
- `deliverables/risk-log.md` — anything monday can't natively support + scale risks.
- `docs/…` — build documentation/diagrams via monday-build-docs.

## After
Lead the summary with risks and anything not natively supported. (Engagement type
from the SKU meta matters: managed services may skip the formal launch/closure arc.)
