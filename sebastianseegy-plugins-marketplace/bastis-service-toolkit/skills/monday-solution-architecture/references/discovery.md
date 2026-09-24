# Discovery readiness checklist

Use this to confirm you have what you need before recommending a design. Ask the
user to fill gaps; if they say proceed anyway, design with stated assumptions for
the unknowns. Running discovery from scratch is `monday-scoping`'s job — this is a
*readiness check* on the inputs a good design requires.

## The six core questions (always)

These come straight from the build methodology and are the minimum:

1. Is this a **project or a process**, and what is the **entity** (the unit moving
   through the board)?
2. **How many entities** will be managed? (volume / scale — drives topology and
   limit checks)
3. What are the **steps** in the workflow?
4. Do all entities **always go through the same steps**? (consistent → process;
   varies → may be projects or branching logic)
5. What **information must be captured at each step**?
6. What **insights / reports** does the team need out of it?

## Intake / Manage / Report / Permissions (always)

- **Intake:** How does work enter today (form, email, word of mouth, integration
  from Salesforce/Jira)? Is there an approval before work starts?
- **Manage:** What tools manage it now? How many steps to completion, how long, and
  are there different request types (same tasks or different)? Who are the
  stakeholders? Volume per week/month/year? What happens when work completes?
- **Report:** Reporting needs, historical/trend vs live data, stakeholder reporting.
- **Permissions:** Who owns the process? Permission requirements? Guest/Viewer
  access needed?

## Deep-dive categories (when the workflow is non-trivial)

Scale/volume · user management & user types · decision points · owner responsible
per step · tools & integrations (replace or integrate?) · data flow between teams ·
communication & notifications (in-monday vs email/Slack/Teams) · permissions level
(account/workspace/board) · standardization (managed templates?) · reporting in
detail.

## Use-case specific banks

### PMO / project work
- PM method (waterfall / agile / hybrid); different project types?
- How many projects (total / per team / per PM); size & complexity.
- Do all projects need their own board? Repeatable vs unique? How many templates?
- Data to roll up from project boards to Portfolio.
- Maintenance/archive process for completed projects.
- Other project processes: risk/issue/change management, RAID log vs individual
  boards, project docs (charter, RACI/WBS), resource allocation & time entry.

### Marketing
- How requests arrive (intake form, email, word of mouth); who requests content.
- What a campaign *is* to them; average timeline; how many per quarter/year.
- Team structure & roles; everyone licensed?; external freelancers/vendors as guests?
- Current tools; archive old process?; parallel tools kept?
- Content types (video, events, social, etc.); biggest pains; migrate or start fresh.
- Reporting/tracking needs; digital-asset storage & security (monday vs other repo);
  how campaign performance is measured and where.

### CRM (sales)
- How many CRM workspaces (separate independent sales teams?).
- Leads board? intake source (web form, item-creation form, events, integration,
  import).
- Accounts/Contacts boards? how many of each — **scale matters: ask volume and
  anticipated connections per item**.
- Opportunities board? sell multiple products (subitems / product catalog /
  multiple opp boards)?
- Work with Legal & Security? Sales Ops boards? Post-sales boards (connect to Work
  Management processes)?
- Workflow: where leads come from; when contact/account is created; when an
  opportunity begins (auto vs manual); repeat business for existing accounts.

## Reframing a use-case (keep it specific)

A use-case is a *workflow*, not a department or system. Good: "event management for
the marketing team", "project intake & approval", "employee onboarding", "sales
pipeline". Too broad/vague: "Marketing department", "Project management", "CRM".
If the user gives a broad one, narrow it before designing.
