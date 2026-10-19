---
name: weekly-pulse
description: >-
  Basti's weekly claim audit of the toolkit. Re-verifies the load-bearing claims in
  the monday AI and platform skills against primary sources (API schema, MCP tool
  lists, support docs, owner announcements), logs changes, queues unresolved
  questions for named owners, proposes SKILL.md patches for approval, and produces a
  short review. Use when Basti asks "run my pulse", "weekly review", "what's new /
  what did I miss", "audit the skills", "are the skills current" - and automatically
  once a week via the scheduled task. Lens: Enterprise EMEA delivery + AITP / AI
  Champion work. Not for one-off "is X still true" checks (use monday-scaling-watch /
  monday-ai-advisor).
---

# Weekly pulse = weekly claim audit

The goal is not a news digest. It is: **every capability, limitation, pricing or credit
claim the skills rely on is either verified against a primary source this week, or
visibly flagged as unverified.** News is a by-product.

State lives in `references/audit/` (read its `README.md` first): `claims.csv` ledger,
`sources.md` registry + grading, `queue.md`, `snapshots/`, `proposed/`, `evals/`.
Helper: `scripts/audit.py` (`due`, `rotate`, `diff`, `evals`; run with `python3 -I`).

## Source grades (what may change what)

| Grade | Source | May change a SKILL.md body? |
|---|---|---|
| A | Schema introspection, MCP tool lists, behaviour seen live | Yes |
| B | Owner announcement, official docs (with modified date), Release Board card status | Yes |
| C | Human digest: ICs Product Updates board (18411697232), shipping summaries | No - index + changelog line |
| D | Q&A / chat: #ask-*, #ai-workflow-group (many answers are bot-written) | No - changelog line, marked unverified |

Reversing a stated limitation needs two independent A/B sources. Full registry, URLs
and named owners: `references/audit/sources.md`.

## Procedure

### 1. Snapshot raw sources and diff (A/B)
For each snapshot name: `audit.py rotate <name>`, write the fresh snapshot, `audit.py diff <name>`.
- `monday-schema.json` - `get_graphql_schema` / `get_type_details` (normalized, sorted).
- `monday-mcp-tools.txt` - tool names + parameter names of the monday MCP (diff = real capability change, e.g. new `vibe_*` / workflow tools).
- `support-<topic>.txt` - text + modified date of the support articles listed in `sources.md` (agents, Vibe, Workflow Builder, Sidekick, credits).
Only the **changes** drive the rest of the run. First run writes baselines and reports "baseline".

### 2. Use digests only as an index
Read the Product Updates board (window: since last run, default 7 days; board `18411697232`, date column `date_mm32grnh`; columns in `get_board_info`), owner posts in #ai-agents-product-updates / #cco-enablement-updates, News and KB in monday-all - to learn **what to go and check**. For every item that could touch a claim, find the primary source (B or better) before logging it as fact. Cross-check the board's Release Status against its own source text; if they disagree, status = `UNVERIFIED-CONFLICT`.
- The board may exist on only one of several connected monday MCP servers - if "not found", try the other.
- #monday-platform-notifications is often empty bot posts; skip if no text.

### 3. Reconcile the ledger
Run `audit.py due <today>`. For each row returned (expired, never verified, contradicted, stale, conflicted):
1. Look for a grade A/B source. If found: set `status=verified`, `grade`, `verified_on=<today>`, and a new `expires` (A/B: today+14d; time-bound claims: their natural date).
2. If the claim changed: update the row, and write a proposed patch in `references/audit/proposed/<skill>.md` (what line, old, new, evidence, grade). **Never edit a SKILL.md body automatically.**
3. If no A/B source: leave `unverified`, add or refresh the entry in `queue.md` naming the owner from `sources.md`.
4. Add new rows for new load-bearing claims found this week. Prioritise "can't / not supported" claims and look actively for removals, deprecations and expired time-bound statements.
Priority order: CONTRADICTED > time-bound past expiry > "can't" claims > pricing/credits > capabilities.

### 4. Changelogs (auto, grade-tagged)
For each skill with relevant changes, insert a dated section right after the intro of `<skill>/references/changelog.md` (newest first; match existing format; include source links and the grade). Files: monday-vibe, monday-agents, monday-sidekick, monday-ai-columns, monday-ai-advisor, monday-ai-suggester, aitp-advisor, monday-workflow-architect, monday-formulas, monday-solution-architecture, monday-scoping, monday-scaling-watch (platform bugs/incidents only). Skip skills with nothing new - no "nothing new" sections. Grade C/D items go in marked **unverified**.

### 5. Verify before finishing
- Run `audit.py evals`. Run the questions that have answer keys against the skills (ask each question using only the skill text + its changelog) and report pass/fail per question. Answer keys come from grade A/B sources, written by Basti or cited from a primary source - **never write or edit an answer key yourself**, and never grade a question you can't check against its key. Questions without keys are reported as `needs_key`.
- Re-read `claims.csv`: no row may be `verified` without `verified_on` and `expires`.

### 6. Output - the review (2 pages max)
```
# Weekly review - [date range]
Coverage: schema [diff/no change/baseline] · MCP tools [..] · support articles [n changed] · digests used as index [board N items, Slack channels with usable text, monday-all] · sources failed [..]

## Claims changed or reversed (with evidence + grade)
## Proposed SKILL.md patches awaiting your approval  (file paths in references/audit/proposed/)
## Needs an owner (queue.md): [claim -> owner -> question]
## Expired / contradicted claims still open
## Eval results: X/Y with keys passed · N need keys
## Also shipped (graded)  - ranked: AI/AITP first, then Enterprise, then IC Relevance "Most Relevant"
```
Keep it scannable; no filler; no forced client-relevance. If a source errored or was empty, say so in one line and continue.

## Hard rules
- Read-only against monday and Slack. Never post, message, or edit boards.
- Write only inside the plugin repo (locate the connected `sebseegy/plugin` folder; it moves - last seen at `Desktop/Sebastian Seegy /Git/plugin/bastis-service-toolkit`). If not connected, say so and stop writing; the review in chat is still the deliverable.
- No git commands (sandbox leaves lock files). If anything was written, bump the patch version in `.claude-plugin/plugin.json` (minor if the method changed) and end with: "Written, version bumped to X.Y.Z - commit & push from Terminal, then update the marketplace in Cowork."
- SKILL.md bodies change only after Basti approves a patch from `proposed/`.
- Unattended runs: never ask questions; unresolved items go to `queue.md`.

## Cadence
Weekly full run (Mondays). Steps 1 and the `due` check are cheap and can also run ad hoc before client calls: "audit the skills for <topic>".
