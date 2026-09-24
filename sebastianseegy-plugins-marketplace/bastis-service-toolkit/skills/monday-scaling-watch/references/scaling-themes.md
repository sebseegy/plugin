# monday.com scaling themes — live baseline

**Snapshot date: 2026-06-02.** These are the moving initiatives. Each entry gives
the baseline (what was true at snapshot), who owns it, and **what to search Slack
for** to detect a change. When you confirm a change, update the entry and bump the
snapshot date.

---

## 1. mondayDB 3.0 + 1M-item scale

**Baseline:** DB 3.0 backend performance improvements were **fully released to all
customers, including ENT** (announced ~May 27–28, 2026, #cco-enablement-updates by
Lizabet Pakin). The headline **1M items per board is BETA-ONLY and lives in the
new "Data Set" feature** — not on regular boards. The Data Set feature has its own
limitations that must be understood before registering clients. Beta sign-up runs
through Oded Keret / #ask-monday-db.

**Watch out:** DB 3.0 auto-rolled out to at least one ENT account (Qantas Loyalty)
and broke dashboards interacting with multi-level boards; a dev disabled it for the
account. Still being stabilized for MLS + dashboards. Open question in-field: the
date when DB 3.0 becomes the *default* for all new ENT accounts (no firm answer at
snapshot).

**Check Slack for:** `mondayDB 3.0`, `mdb 3.0`, `1M items beta`, `data set feature`,
`db 3.0 default ent` in #cco-enablement-updates and #ask-monday-db. A change looks
like: 1M moving from beta to gradual/GA, Data Set limitations changing, or a
default-rollout date being announced.

## 2. Portfolio at Scale (PAS)

**Baseline:** Active Voice-of-Customer effort to support portfolios of **up to
5,000 projects** (announced ~May 14–19, 2026; owners include Keren Sharabi,
Christian Harzl, Joshua Rechtschaffen, Nathanel Mori). GA scope being finalized.
Field-confirmed prioritization at snapshot:
1. Drill-down on dashboards + work-surface widgets (List, Gantt, Workload, Calendar)
2. Seamless migration (portfolios; regular→MLS projects; templates→Managed Templates)
3. Formula roll-up on portfolio + reporting widgets
4. Task management at scale
5. Dynamic project assignments via People columns

**Tie-in to limits:** the **750 connected items per project board** and **20,000
total per portfolio** caps (see limits.md) are the constraints PAS is working
around. Watch for these numbers changing as PAS ships.

**Check Slack for:** `portfolio at scale`, `PAS`, `5000 projects`, `portfolio
limit`, `750 portfolio` in #ask-projects, #cco-enablement-updates, #emea-services.
For project-specific limit questions the field is routed to Nathanel Mori.

## 3. Vibe app connected-board limit

**Baseline:** A Vibe app can connect **5 boards** today; confirmed **increasing to
20 "soon," then 50 by end of 2026** (Amichay Even Chen, #ask-vibe-ai, late May
2026). Connecting a Portfolio gives Vibe only the portfolio board's own data; to
read project data you must connect each project board. Known constraints: API
doesn't support formula-over-mirror; viewers may need full ENT licenses (a
customer cited this as a reason to drop Vibe).

**Check Slack for:** `vibe board limit`, `vibe connect boards`, `vibe 20 boards`,
`vibe 50 boards` in #ask-vibe-ai. A change looks like the 5→20 increase actually
shipping, or the 50 timeline firming up.

## 4. Dashboard & performance at scale

**Baseline:** Large-ENT complaints at snapshot: dashboards becoming sluggish /
"wait" messages, and inconsistent filtering between dashboard-level and
widget-level filters. DB 3.0 is the intended fix but introduced MLS+dashboard
regressions for some accounts (see theme 1).

**Check Slack for:** `dashboard slow`, `dashboard performance`, `dashboard filter
widget`, `db 3.0 dashboard` in #ask-dashboards-widgets and #platform-performance.

## 5. Infra reality behind "scale"

**Baseline:** Single large accounts repeatedly overwhelm shared infrastructure
(e.g. one account generating ~87K asset sub-jobs during a board duplication and
monopolizing all workers; recurring Sidekiq queue saturation). Strategically,
monday folded EWM + Enterprise under the data/infra/foundations org (Daniel
Lereya, #monday, May 5 2026) because scale, performance, governance, and AI-agent
query load are foundational. Practical takeaway for scoping: bulk operations
(mass duplication, large imports, heavy automation fan-out) can hit real
processing ceilings even when no documented limit is exceeded.

**Check Slack for:** `sidekiq queue`, `board duplication`, `performance incident`,
`account overwhelming` in #platform-performance. Mostly context, not a quotable
limit — but useful when a customer plans a bulk operation.

---

## Quick channel map

| Topic | Primary channel(s) |
|---|---|
| Official scale announcements / beta sign-ups | #cco-enablement-updates |
| mondayDB scale Q&A | #ask-monday-db |
| Board item/column/connection limits | #ask-boards |
| Portfolio / project board limits | #ask-projects |
| Dashboard limits + performance | #ask-dashboards-widgets |
| Vibe app board limits | #ask-vibe-ai |
| Plan-tier item limits / upgrades | #ask-work-management |
| Workflow blocks / complexity / agent limits | #ask-ai-workflows, #ask-ai-agents |
| Infra incidents revealing practical ceilings | #platform-performance |
