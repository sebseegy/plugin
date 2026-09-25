---
name: status
description: "Report the current status of a project — what's been done and where things stand — by reading the project's deliverables, context, and calls. Use when the user asks for project status, 'where are we', a progress update, or a health check. Reads from the client/SKU/project structure in the shared drive; produces a status read in chat (saves one only if asked)."
---

# Project Status (task)

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


Give a grounded current-state read of a project. Read `PROJECT-STRUCTURE.md` for how
to resolve the project and where things live. This is a read — don't change files
unless asked.

## What to read
1. Resolve the project (ask which if the client has several). Read project →
   SKU (note `engagement_type`) → client `meta.json`.
2. The project's `deliverables/` — whatever exists (handover brief, process map,
   architecture spec, UAT triage, go/no-go, hypercare reports, closure docs). Their
   presence tells you what's been done.
3. The `All Calls/call-inventory` Sheet filtered to this project — recent activity
   and `key_next_steps`. Open individual call files only as needed; summary level is
   usually enough.
4. `Client Context/account-overview.md` for account facts.

## Produce
A concise status: engagement (client, SKU, project, type), where things stand (2–4
sentences), what's been delivered (from the files present), open items / next steps
(from open-questions, UAT blockers, call next-steps), and any risks. Ground every
statement in what you read; if something's unknown because a file is absent, say so.

If the folder isn't a recognizable project, say so and point to `/project-setup`
(client) and the relevant task skills. If context looks stale (old
`last_context_sync`), note it and suggest `/update-context`.

## Output
Present in chat. Save to `deliverables/status-YYYY-MM-DD.md` only if asked.
