---
name: handover-brief
description: "Produce an internal Handover Brief that synthesizes pre-sales artifacts and sales-call context — surfacing promises, pain points, red flags, budget/timeline signals, and open questions before the first client call. Use when the user says 'handover brief', 'parse the sales handover', 'what did sales promise', or is taking over a newly-sold engagement. Files the brief into the project's deliverables/ folder."
---

# Handover Brief (task)

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


Turn everything known from the sales process into one structured internal brief.
Read `PROJECT-STRUCTURE.md` for how to resolve the project and where things live.

## Resolve & read
1. Resolve the project (ask which if ambiguous). Read its `meta.json` → SKU
   `meta.json` (note `engagement_type`) → client `meta.json`.
2. Read sales-stage calls from client `All Calls/`, filtered to this project (or
   untagged client-level sales calls) and to `project`/`mixed` relevance — treat
   `commercial`/`internal` as background. Deepen a pivotal call with
   `pull-gong-transcripts` only if exact commitments matter.
3. Read `Client Context/account-overview.md` and anything in the project `inputs/`
   (CRM export, email threads, opportunity summary — read binaries via the Drive
   connector).

## Write `deliverables/handover-brief.md` (internal)
1. **Client snapshot** — company, industry, size, key contacts and roles.
2. **Promises made by sales** — committed, implied, or demoed; cite the call/email.
3. **Pain points** — what they need to fix, in their words.
4. **Red flags** — unrealistic expectations, scope ambiguity, political dynamics.
5. **Budget & timeline signals.**
6. **Open questions** — what sales didn't answer, to raise at kickoff.

Be direct; flag conflicts between promises and what's realistic. Internal only.

## After
Short chat summary leading with red flags and open questions. Never invent promises
or contacts — unknowns become open questions.
