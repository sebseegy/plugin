# monday.com archetype templates

Best-practice starting layout for each of the three solution archetypes. These are
defaults to adapt, not rigid rules — but deviating from them should be a conscious
choice, because each pattern exists to keep one board managing one unit type.

---

## PROJECT board

**What it manages:** the *tasks* of a finite effort with a start and end, driven
toward a deliverable or outcome. One board = one project's tasks (or a single
project template instantiated per project).

- **Groups = phases.** e.g. Plan → Design → Build/Execute → Launch → Close. Items
  are tasks within a phase.
- **Key columns:** Owner (people), Status, Timeline (or Date), Dependency,
  Priority, and an Effort/Estimate if needed. Connect-boards columns to any
  repositories the project consumes.
- **Automations:** dependency-driven date shifts, status-change notifications,
  "when done → notify owner of next task."
- **Reporting:** phase/status battery, timeline/Gantt, workload by owner.

**Keep OFF the task board — give these their own boards and connect:**

| Project sub-unit | Why separate |
|---|---|
| Risks (RAID) | Different lifecycle (likelihood/impact/mitigation), not a task |
| Issues | Tracked and triaged differently from planned tasks |
| Dependencies (cross-project) | Belong at a coordination layer, not inside one task list |
| Assumptions | Reference/log, not actionable work |
| Change requests | Has its own approval lifecycle (a mini PROCESS) |
| Decisions log | Reference record |
| Lessons learned | Reference/knowledge, captured across projects (a REPOSITORY) |
| Stakeholders / RACI | A REPOSITORY of people + roles the project points at |
| Milestones | Sometimes a column, but often a separate roll-up board for portfolios |
| Budget / costs | Financial unit with its own structure |
| Resource allocation | Capacity across projects → coordination board |
| Status reports | Generated/log, not tasks |

When the client runs **many** projects, consider a Portfolio rollup over the
project boards rather than one giant board — and check portfolio/connected-item
limits via `monday-scaling-watch`.

### Project topology: how many boards?

Three layouts, chosen by project size, similarity, and reporting needs:

- **Single board per project.** One project = one board; groups = phases. *Best
  for* medium projects. Strengths: per-project views/automations/data, segmentation
  by project team (each team sees its board), easy project-level reporting, easy
  dependencies. Watch the 50-boards-per-dashboard ceiling for cross-project rollup.
- **Multiple boards per project.** One project spread across boards, each a
  phase/department. *Best for* very large/complex projects needing different data
  per phase. Trade-off: **no cross-board dependencies**, and the dashboard ceiling
  still applies to cross-project reporting.
- **Single board for all projects.** All projects on one board, each project a
  group. *Best for* many small, similar-sized projects. Strengths: everything in
  one place, easy cross-project reporting. Trade-off: no project-level data (only
  task-level), and it's harder to see what stage each project is at.

For portfolios of many projects, pair single-board-per-project with a Portfolio
rollup — and verify portfolio limits via `monday-scaling-watch`.

---

## PROCESS board

**What it manages:** a repeatable pipeline where every item is the *same kind* of
request flowing through the *same stages*. It never finishes; it keeps processing
new arrivals. This is the most common structure and the one most often built wrong
(as a project).

- **The defining feature is the status lifecycle.** Define it explicitly and in
  order, e.g. for a marketing deliverable request:
  `New submission → Reviewing / Scoping → Approved → In progress → Shipped / Complete`
  (with side states like `On hold` or `Rejected` as needed).
- **Groups:** by stage, OR by time period (month/quarter), OR by team — pick based
  on how the team wants to scan the queue. Stage-as-status with groups-by-month is
  a common, scalable combo.
- **Fed by a Form.** The intake form populates the requester fields; the item lands
  in the first status. This keeps requests structured and off email/Slack.
- **Key columns:** Status (the lifecycle), Requester (from form), Request type,
  Priority, Assignee (people), Submitted date, Due/SLA date, and connect columns to
  any repository (e.g. the asset library) or to a project board if approved
  requests spin up project work.
- **Automations:** form submission → assign/notify; status transitions →
  notify/move/date-stamp; SLA breach alerts; on Approved → create connected item on
  the project board.
- **Reporting:** throughput, status battery, time-in-stage, volume by type/requester.

**Watch for:** a process board grows forever. Plan an archive strategy (archived
items don't count toward the board item limit) and verify the item ceiling for the
plan via `monday-scaling-watch`.

### Process topology: Horizontal vs Vertical

A process has two layouts. Choose deliberately — it affects reporting, ownership,
and automation.

- **Horizontal (steps = columns).** The most popular structure. Each stage is a
  status column on a single board. *Strengths:* a different owner/date per stage,
  scalable across many entities, all entities on one board. *Weaknesses:* the board
  gets crowded with columns as steps grow, and it's harder to report on *which
  stage* an entity is currently at. Best when stages have meaningful per-stage data
  (owner, date, files) and the number of steps is modest.
- **Vertical (steps = groups).** The entity moves group → group as it progresses.
  *Strengths:* easy reporting on the current stage, cleaner (fewer columns), and a
  natural "when stage changes → move item to group" automation. *Weaknesses:* no
  separate data point or owner/date per stage (it's one column), and it's harder to
  notify the next stage's owner when the previous finishes. Best for many-step
  pipelines where you mainly care where each entity sits.

---

## REPOSITORY board

**What it manages:** reference / master data — a list of records other boards point
at. Relatively static. The "nouns" of the solution.

- **Examples:** employee directory, digital asset library, client/account register,
  product catalog, register of sold projects, vendor list, location list.
- **Groups = categories** (e.g. asset type, department, region) or a single group
  if the list is flat.
- **Key columns:** the record's attributes (text, status, files, links, people),
  plus **connect-boards columns back to the consumers** so projects/processes can
  reference a record instead of duplicating its data.
- **Automations:** minimal by design — a repository is a source of truth, not a
  workflow. Maybe a "last reviewed" stamp or owner notification.
- **Reporting:** mostly lookups and mirrors *into* other boards rather than charts
  on the repository itself.

**Design tip:** if two boards both need the same reference data (e.g. a campaign
project and a requests process both need the asset library), make it one repository
both connect to — never copy the list onto each board. That's the one-board-per-unit
principle applied to reference data.

---

## Quick classification cues

When you're unsure which archetype a unit is, ask how work *enters, moves, and
ends*:

- Enters via a form, moves through fixed stages, never really ends → **PROCESS**
- A bounded effort with phases and an end date → **PROJECT**
- A list other things look up, mostly edited not "worked" → **REPOSITORY**

A single client solution usually contains all three, connected.
