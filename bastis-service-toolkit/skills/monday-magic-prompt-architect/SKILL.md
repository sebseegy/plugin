---
name: monday-magic-prompt-architect
description: >
  Generates production-ready Monday Magic prompts from a client use-case description. Use this skill
  whenever Basti says "write a monday magic prompt", "build a magic prompt", "magic prompt for [client/use case]",
  "generate a monday magic setup", or any variation on creating a prompt for monday.com's AI workspace builder.
  Also triggers when Basti pastes a client brief and asks to turn it into a Monday Magic input. The output
  is a complete, copy-pasteable Magic prompt — not a plan, not a template, the actual prompt.
---

# Monday Magic Prompt Architect

Generates production-ready Monday Magic prompts. Output must be immediately copy-pasteable into Monday Magic
with zero discovery mode — Magic should build, not ask questions.

---

## Step 0: Assess Input Completeness

Before writing anything, scan the brief against the **Minimum Viable Spec** below.

### Minimum Viable Spec (must know before generating)

| Dimension | Required Detail |
|---|---|
| Boards | Names (exact), purpose, what one item represents |
| Columns | Name, type, all allowed values (Status/Dropdown), required/optional |
| Groups | Names, what triggers movement between them |
| Forms | Which board, which group, question→column mapping, internal/external |
| Automations | Trigger + condition + action (no vague "notify someone") |
| Dashboards | Audience, metric definitions, widget type |
| Permissions | Who owns, who edits, who views, form access |
| Board relations | Which boards connect, link column, what mirrors |

**If gaps exist:** Flag them explicitly with `⚠️ MISSING:` before proceeding. Propose sensible defaults
for non-critical gaps (Basti can override). Do NOT generate a prompt with placeholders — either fill the
gap with a reasonable default and flag it, or ask for the missing info.

**If context is sufficient:** Skip straight to generation. Don't recap the brief back.

---

## Step 1: Evaluate the Architecture

Before writing the prompt, briefly validate the proposed setup:

- Are the board boundaries correct? (one board per entity type, not one board per team)
- Are Status values covering the full lifecycle? No gaps, no overlaps?
- Will automations actually close the loop, or are there handoff gaps?
- Are mirror columns needed that weren't specified?
- Is any requested capability outside Magic's scope? (AI blocks, complex formulas, Slack bots, historical imports)

Surface any structural issues as **`⚠️ ARCHITECTURE NOTE:`** with a recommendation. Then proceed.

---

## Step 2: Generate the Prompt

Output a single fenced code block (` ```markdown `) containing the complete Magic prompt.
Structure it exactly as follows — no deviation:

```
# [WORKSPACE NAME] - Workspace Setup via Monday Magic

## Overview
[1-2 sentences: what the workspace does and what business outcome it drives]

## Workspace Details
- **Workspace Name:** [Exact]
- **Privacy Level:** [Open / Closed / Private]
- **Primary Users:** [Roles]
- **Key Outcome:** [What "done" looks like]

## Board [N]: [EXACT BOARD NAME]

**Purpose:** [Why this board exists + what job it does]
**Item Represents:** [The unit of work — e.g., "A client contract", "A support ticket"]

### Columns
| Column Name | Type | Values / Format | Required | Default | Notes |
|---|---|---|---|---|---|
| [exact name] | [Status/People/Date/Text/Numbers/Dropdown/Relation/Email/Phone/Link] | [all values or format] | Yes/No | [value or —] | [example data] |

### Groups
| Group Name | Purpose | Move Rule |
|---|---|---|
| [exact name] | [why] | [when items move here] |

### Forms (if applicable)
**Form Name:** [Exact]
**Target Board:** [Exact board name]
**Target Group:** [Exact group name]
**Access:** [Internal / External / Public]

| Question (exact) | Maps to Column | Type | Required |
|---|---|---|---|
| [question text] | [column name] | [type] | Yes/No |

**Submission Behavior:**
- Default status: [value]
- Auto-assign to: [role/person or none]
- Notification on submit: [yes → who / no]

[Repeat Board section for each board]

## Board Connections
| From Board | To Board | Relationship | Link Column | Mirrored Fields |
|---|---|---|---|---|
| [Board A] | [Board B] | [1:many / many:many] | [column name] | [field names or none] |

## Dashboards

### [EXACT DASHBOARD NAME]
**Audience:** [Who views this]
**Source Boards:** [Which boards feed it]

| Widget | Type | Metric Definition |
|---|---|---|
| [widget name] | [Number Card / Bar Chart / Pie Chart / Timeline / Table] | [exact formula or count logic] |

[Repeat for each dashboard]

## Automations

[For each automation:]
**[Automation Name]**
- Trigger: [specific event — status changes to X / date arrives on column Y / new item created]
- Condition: [if Z / always]
- Action: [exact action — move to group, notify @role, assign to person, create item in board]

## Governance
- **Board Owners:** [Roles]
- **Team Members (edit):** [Roles + scope]
- **Viewers:** [Roles]
- **Form Access:** [Public / Internal / Closed]

## Key Success Indicators
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]
```

---

## Step 3: Post-Prompt Flags

After the code block, output a short section:

### ⚠️ Manual Add-Ons Required
List anything specified that Magic cannot build automatically:
- AI Block columns
- Complex formula columns (describe what formula logic is needed)
- External integrations (Slack, webhooks, etc.)
- Historical data import

### ✅ Defaults Applied
List any gaps you filled with defaults so Basti can override quickly.

---

## Magic Capability Reference

**Magic CAN build:**
Boards (names, privacy, purpose) · Columns (Status, People, Date, Text, Numbers, Dropdown, Relation, Email, Phone, Link) · Groups · Default views · WorkForms (with column mapping, routing, submission behavior) · Dashboards (charts, number cards, timelines, KPI widgets) · Automations (status triggers, date triggers, new item triggers → move, notify, assign, create) · Board relations + mirror columns

**Magic CANNOT build (manual required):**
AI Block columns · Complex formula columns · Multi-layer nested automations · Slack/webhook integrations · Historical data imports · Custom UI/branding beyond standard Monday options · Editing existing automations post-generation

**Discovery Mode Prevention:**
Magic enters question mode when: board names are vague, column values are missing, workflow is ambiguous, form targets are unspecified. This prompt format prevents that by design — but only if every field is filled with real values, never placeholders.

---

## Quality Gate

Before outputting, self-check:
- [ ] Every Status/Dropdown column has all values listed (no "TBD")
- [ ] Every form maps to an exact board + group
- [ ] Every automation has trigger + condition + action (no partial specs)
- [ ] Board relations specify the link column and mirror fields (or explicitly "none")
- [ ] Permissions cover owners, editors, viewers, and form access
- [ ] No placeholders in the output prompt — only real names and values
- [ ] Anything outside Magic's scope is flagged as manual add-on
