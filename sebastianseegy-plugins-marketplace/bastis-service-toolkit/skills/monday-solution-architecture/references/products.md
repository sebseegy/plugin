# Products & features in scope

Establish which monday product(s) and which AI features are in play before
designing — they change the architecture. State the answer in the design's
Overview.

## monday products

- **Work Management (WM)** — the general work platform; the three archetypes
  (project / process / repository) apply directly.
- **monday CRM** — sales product with a canonical board model (below). Don't
  reinvent it; adapt it.
- **monday Dev** — sprints/roadmap/bugs for product teams (sprint boards, etc.).
- **monday Service** — ticketing / service management.

A solution can span products (e.g. CRM post-sales connecting into a WM delivery
process). Note cross-product connections explicitly.

## monday CRM canonical model

CRM is itself an interconnected set of archetypes. The default structure:

- **Leads** (PROCESS-like intake) — new leads enter via web form, item-creation
  form, events, integration, or import; automations assign reps (e.g. by region)
  and score leads. On qualify → create Contact, related Account, and an Opportunity,
  all connected.
- **Contacts** (REPOSITORY) — people; high-level overview of everyone in the
  pipeline.
- **Accounts** (REPOSITORY) — organizations; the detail record per company.
- **Opportunities / Deals** (PROCESS) — groups = stages; the pipeline. Multiple
  products → subitems, a product-catalog repository, or multiple opportunity boards.
- **Activities** (repository/log) — calls, meetings, emails logged from Emails &
  Activities; feeds rep-activity dashboards.
- **Sales Ops / Post-sales** (optional) — client onboarding, invoices & collections,
  often connecting into Work Management delivery processes.

**Scale focus:** Accounts and Contacts are where CRM scale bites — ask volume *and*
anticipated connections per item, and validate against `monday-scaling-watch`.
Workspaces: split per independent sales team.

## AI features — defer selection to aitp-advisor

If AI is in scope, **`aitp-advisor` owns the AI discovery and tool selection.** This
skill's job is only to (a) detect AI is in scope, (b) get the chosen features from
that skill, and (c) reflect them in the board design. For orientation only — the
broad mapping aitp-advisor works from:

- Simple/linear text task → AI Blocks / Sidekick actions
- Multi-step reasoning / orchestration → AI Agents / AI Workflows
- High volume (50+/week) → zero-click automations (not manual buttons)
- Reporting / visibility → AI Board Insights / conversational dashboards
- Context-aware assistant across work → Sidekick
- Turn work into secured apps/portals → Vibe
- No-trigger lead sourcing / ticket triage → Agents (Sales/Service)
- Meeting capture → Notetaker

Where an AI feature lands in the design matters: e.g. a form-fed intake board whose
items an AI Agent triages, an Insights widget on the reporting dashboard, or a Vibe
portal as a secured client view over a repository. Show that placement; leave the
"which feature and why" reasoning to aitp-advisor.
