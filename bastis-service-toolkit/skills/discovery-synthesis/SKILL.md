---
name: discovery-synthesis
description: "Synthesize multiple discovery calls and consultant notes into a Process Map (current-state workflows, pain points, stakeholders, decision logic, integration needs) plus an internal gaps list — flagging contradictions between stakeholders rather than averaging them out. Use when the user says 'process map', 'synthesize discovery', 'map their workflows'. For mapping a single call in depth, delegates to monday-discovery. Files outputs into the project's deliverables/ folder."
---

# Discovery Synthesis (task)

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


Synthesize everything learned in discovery into a Process Map. Preserve disagreement
rather than average it; separate client-ready content from internal gaps. Read
`PROJECT-STRUCTURE.md` for project resolution and paths.

## Inputs
- Discovery-stage calls from client `All Calls/`, filtered to this project and to
  `project`/`mixed` relevance. **Delegate per-call mapping to `monday-discovery`**
  for any call needing depth (it produces a per-call summary + visual); aggregate
  those into the cross-call map here. When a call defines a workflow/approval/
  integration precisely, deepen it with `pull-gong-transcripts`.
- `deliverables/kickoff-debrief.md` and `deliverables/open-questions.md` if present.
- Project `inputs/` (consultant notes, workshop outputs).

## Outputs
**`deliverables/process-map.md` (client-ready, sections 1–5 shareable):**
1. Current-state workflows (per team, step by step)
2. Pain points per workflow
3. Key stakeholders (owners, blockers, champions)
4. Decision-making logic (approvals, escalation, exceptions)
5. Data & integration needs

**Client-safe HARD RULE:** sections 1–5 draw only from `client-safe`,
project-relevant content; never internal-only/commercial material. Gaps go in the
internal file, not filled from sensitive sources.

**`deliverables/internal-gaps.md` (internal):** open questions and **contradictions
— flag both positions and who said each, never reconcile silently.** Carry forward
unresolved items from `open-questions.md`.

## After
Lead the chat summary with contradictions and the biggest gaps. Never invent
workflow detail — an unknown step is an open question.
