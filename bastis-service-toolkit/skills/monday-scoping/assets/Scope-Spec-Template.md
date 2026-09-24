# Scope Spec — Template

> Reusable scope document for a monday.com build. Fill from the completed **Discovery
> Questionnaire**. Keep it short and concrete — this is what the client signs off on.
> `>` blockquote tips are scoping guidance drawn from the TITANs/PSP build; delete them before
> sending to the client.
>
> **Project:** _______________  **Client/Team:** _______________  **Prepared by:** _______________  **Date:** _______________

---

## Summary

_One paragraph: what we're building, for whom, and the headline numbers (how many forms/boards/automations, total estimate, target dates)._

> Tip: lead with the shape of the work and a single total, e.g. *"One form per force for all 5
> forces, plus item-creation automations onto a collector board and an approval process; ~59
> hours."* Specifics live below.

---

## Timeline & phasing

_Key dates and what's ready when._

> Tip: phase by **data readiness**, not just calendar. On TITANs, workstreams with finalized
> activity lists started immediately; those awaiting client input were sequenced after a named
> hand-off date. State which parts can start now and which are blocked on what.

---

## In scope

> Tip: use a workstream per build block below. Delete any that don't apply, add ones that do.
> Keep each item a checkable line so the client can see progress. Hours are left blank — fill
> per project. The TITANs rules of thumb are noted only as starting points; adjust to the build.

### 1. Boards & structure

- [ ] _Board(s) to create or restructure, groups, key columns._

> Tip: name the repeating unit (team / region / brand / force). If many submissions feed one
> place, a **collector board** is usually the hub.

### 2. Forms / intake (one per unit)

- [ ] _Form per repeating unit; what each captures; how submissions map to items._

> Tip: form effort scales with field count and activity list. TITANs averaged ~3h/form across
> playbooks of 19–84 activities — use as a loose anchor, not a guarantee.

### 3. Automations

- [ ] _Per-form automation: what triggers it, what it creates/updates, where._

> Tip: a simple "create item on submit" is light. A **self-looping, one-item-per-activity**
> automation (one submission → many items) is heavier and may need splitting across workflows due
> to platform limits — scope it separately from simple automations.

### 4. Approval / review process

- [ ] _Approval checkpoints, who is notified, on what status change._

> Tip: one line per distinct approval path. TITANs scoped owner auto-notification on the
> collector board as its own workstream.

### 5. Permissions & access

- [ ] _Who sees/edits what; any row-level visibility._

> Tip: "see only your own rows" = Viewer role + Visibility column + per-row assignment. Call it
> out; it's three explicit steps, not a default.

### 6. Dashboards & reporting

- [ ] _Dashboards per audience and the key questions each answers._

> Tip: scope from the questionnaire's "audience needs" answers — one view per audience question,
> not one giant dashboard.

### 7. Discovery & design

- [ ] _Requirements, field/question wording, form-to-board mapping._ _(Mark complete if done.)_

### 8. Meetings & alignment

- [ ] _Recurring time for design, automation logic, testing, sign-off._

> Tip: reserve a standing weekly hour across the build window (e.g. 1h/wk × N weeks) rather than
> ad-hoc — it covers requirements, demos, UAT, and change requests.

### 9. Documentation & handoff

- [ ] _Runbook: how each form/automation works and how to duplicate or change them._

### 10. Contingency

- [ ] _Buffer for rework, edge cases, UAT fixes, platform limits._

> Tip: ~10% of delivery work is a reasonable default buffer.

---

## Out of scope / assumptions

_What this engagement explicitly does **not** cover, and what we're assuming (client provides X by date Y, access granted, etc.)._

> Tip: where the monday UI exposes something the API/automation can't replicate, state it as a
> known limitation here rather than implying parity.

---

## Time summary

| Workstream | Unit estimate | Units | Total hours |
|---|---|---|---|
| Boards & structure |  |  |  |
| Forms / intake |  |  |  |
| Automations |  |  |  |
| Approval process |  |  |  |
| Permissions & access |  |  |  |
| Dashboards & reporting |  |  |  |
| Discovery & design |  |  |  |
| Meetings & alignment |  |  |  |
| Documentation & handoff |  |  |  |
| Contingency |  |  |  |
| **Total** |  |  |  |

---

## Sign-off

_Approver name, role, date. Note what approval authorizes (start of build, this scope and estimate)._
