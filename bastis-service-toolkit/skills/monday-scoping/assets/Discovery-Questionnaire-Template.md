# Discovery Questionnaire — Template

> Reusable blank questionnaire for scoping a monday.com workflow build. Fill in one copy per
> project (or per team/workstream). The answers feed directly into the **Scope Spec** — the
> notes in `>` blockquotes flag what each answer drives in scoping.
>
> **Project:** _______________  **Client/Team:** _______________  **Date:** _______________

---

## Part 1: The Vision & The Goal

**Project title:** What is a simple name for this workflow? (e.g. "Marketing Content Calendar," "Client Onboarding," "IT Support Tickets")

Your Answer:

**The "Why":** What is the primary business reason for building this? What problem are you solving or opportunity are you seizing?

Your Answer:

**Measuring success:** How will we know this is a success? List 2–3 key success metrics (e.g. "cut manual data entry 50%," "100% visibility on active projects").

Your Answer:

**Intended go-live date:** When does this need to be operational?

Your Answer:

---

## Part 2: The People

**The team:** Who uses this workflow daily? List names, roles, and email addresses.

Your Answer:

**The stakeholders:** Who has a vested interest but may not use it daily (department heads, executives)?

Your Answer:

**The end "customer":** Who is the ultimate beneficiary of this process?

Your Answer:

> Scoping note: counts of daily users vs. view-only stakeholders drive **permissions** scope. If
> people should see only their own rows, that implies a Viewer + Visibility-column setup — call
> it out in the spec rather than assuming everyone sees everything.

---

## Part 3: The Current State & Pain Points

**Current tools:** What are you using today (Excel, email chains, another PM tool, whiteboards)?

Your Answer:

**Key pain points:** Biggest frustrations causing delays, errors, or stress?

Your Answer:

**What works well?** Anything in the current process you want to keep or replicate?

Your Answer:

---

## Part 4: The Workflow — From Start to Finish

Describe the journey of a single work item from beginning to end. If the current process isn't working, describe what *should* happen.

**How does work BEGIN?** What triggers the process? (contract signed, form submitted, weekly meeting, email arrives)

Your Answer:

**What are the key STAGES?** List the major steps a work item goes through (e.g. New Request → In Progress → Awaiting Review → Approved → Complete).

Your Answer:

**How is work VALIDATED or approved?** Are there checkpoints where someone must approve before the next stage? Who approves what?

Your Answer:

> Scoping note: each distinct approval checkpoint is its own automation + notification path. Who
> gets notified and on what status change determines the **approval-process** line in the spec.

**How is work DELIVERED?** What does "done" mean, and what is the final output?

Your Answer:

**Data points:** What key information must be tracked per work item? (Due Date, Owner, Priority, Budget, Client, Status, etc.)

Your Answer:

---

## Part 5: Volume & Structure

> This section isn't in the classic discovery script, but it's where most scope estimates come
> from. On the TITANs/PSP build, the biggest cost driver was the **number of activities per
> playbook** (ranging from 19 to 84) — that's what determined form size and how many items each
> automation had to create. Capture the equivalent numbers here.

**Repeating units:** Does this workflow repeat across multiple teams, regions, brands, "forces," or categories? List them.

Your Answer:

**Volume per unit:** Roughly how many items / activities / records flow through each unit per cycle? (A rough range is fine — it sizes the forms and automations.)

Your Answer:

**Intake method:** Should work enter via a **form**, manual item creation, import, or integration? One intake per unit, or shared?

Your Answer:

> Scoping note: one form per repeating unit is the usual pattern. If a single submission must
> generate many items (one per activity), that's a **self-looping automation** — flag it, since
> it's more effort than a simple "create item" automation.

**Connected/related data:** Does this workflow need to pull from or push to other boards (mirrors, connect-boards, rollups)? Which ones?

Your Answer:

---

## Part 6: Reporting

**Reporting audiences:** Who needs reports or dashboards? (Team members, PMs, department heads/executives, clients)

Your Answer:

**Audience needs:** For each audience above, what are the most critical questions they need answered at a glance? *(This is the single most important input for designing the right dashboards.)*

Your Answer:

---

## Part 7: Constraints & Logistics

**Hard deadlines or phasing:** Any fixed dates, or parts of the scope that depend on data you'll provide later?

Your Answer:

> Scoping note: TITANs phased delivery by **data readiness** — three forces started immediately,
> two waited on client-finalized activity lists. Capture anything similar so the spec can phase
> the work instead of blocking on the slowest input.

**Integrations:** Any external systems this must connect to (email, CRM, Slack, file storage, SSO)?

Your Answer:

**Known limitations / non-negotiables:** Anything off the table, or any platform constraints you're already aware of?

Your Answer:

---

*When complete, hand this to the consultant. It maps section-by-section onto the Scope Spec template.*
