---
name: hypercare-report
description: "Produce a weekly hypercare/support report — scans the week's support tickets, Slack threads, check-in notes, and issue logs to surface issue patterns, classify root causes, read adoption signals, and recommend actions — in both an internal version and a client-safe version. Use when the user says 'hypercare report', 'weekly support report', 'how is adoption going'. Files outputs into the project's deliverables/ folder. Well-suited to managed-services engagements."
---

# Hypercare / Weekly Support Report (task)

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


Weekly post-launch (or ongoing managed-services) support synthesis. Read
`PROJECT-STRUCTURE.md` for project resolution and paths.

## Inputs
Project `inputs/weekly-logs/`, `inputs/slack-exports/`, `inputs/ticket-exports/`
(read exports via the Drive connector), plus any check-in calls in client
`All Calls/` tagged for this project. Process the past week (ask the range if unclear).

## Outputs
**`deliverables/hypercare-internal.md`:** issue patterns (3+ users on the same
problem = flagged pattern), root-cause classification (Product bug · Config error ·
Training gap · Process change · User error), adoption signals, recommended actions
(owner + urgency), week-over-week trend.
**`deliverables/hypercare-client-summary.md`:** concise client-safe version for the
sponsor. **Client-safe HARD RULE:** exclude internal-only/commercial content and the
internal root-cause/risk framing.

## After
Lead with flagged patterns and escalations. Only flag a pattern with real repetition
in the data; don't infer adoption from absence of data without saying so.
