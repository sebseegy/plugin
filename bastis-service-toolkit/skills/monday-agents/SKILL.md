---
name: monday-agents
description: "Design, instruct, and build monday.com native AI Agents (Agent Factory / the AI Agent builder — digital workforce, monday service AI, CRM AI Sales Agent). Use whenever the user wants to build a monday agent, write or fix an agent's instructions/prompt, choose a trigger/activation, decide what to delegate to an agent, or asks 'how do I make a monday agent do X', 'why isn't my agent behaving', 'what should I put in the instructions'. Runs a structured interview to produce a ready-to-build configuration, or critiques and rewrites an existing one. monday's agent platform changes fast, so this skill ALWAYS verifies capabilities against support.monday.com before giving specifics — never answer from memory alone. Use this rather than writing agent instructions freehand."
---

# monday.com AI Agents

Help the user design and prompt monday.com's **native AI agents** (built in Agent
Factory / the monday AI Agent builder) — not external LLM prompts, not the
developer API. These agents live in the account, read and write boards and docs,
can search the web, and run on triggers. Turn a workflow idea into a well-scoped
agent with clear instructions that does what they want.

Three entry modes:
- **Mode A — Interview from scratch:** an idea but no design yet. Run the interview.
- **Mode B — Review & rewrite:** existing instructions or a rough description pasted.
  Go to Critique.
- **Mode C — Context-aware suggestion:** already on a client project — assess fit,
  pre-fill from context, make a specific recommendation.

---

## Always verify against support first — this is the point of the skill

monday's agent platform is new and changes frequently — capabilities, builder UI,
triggers, tools, and limits shift between releases. **Before stating any specific
capability, UI step, trigger name, tool, or limit, search support.monday.com for
the current state.** Don't answer about monday agents from training memory alone —
you'll be confidently wrong about a moving target.

1. Search `site:support.monday.com <topic>` (e.g. "monday AI Agent builder
   triggers", "Agent Factory instructions", "monday agent web search tool").
2. Lean on the support **AI section**, "Get started with the monday AI Agent
   builder", and "Create a Digital Workforce with Agent Factory".
3. If a fetch returns a JS-rendered shell, retry to read snippets or open with
   browser tools — don't guess.
4. If a capability isn't documented, say it's **not currently supported /
   documented** rather than inventing it; state the platform default instead.
5. Note when something looks version-dependent so the user re-checks in their account.
6. Surface sources as links.

Also confirm before committing: the current builder name/entry flow (Agent Factory
vs AI Agent builder), which triggers/activations exist now, which tools the agent
can use, any limits (connected boards, actions, schedule), and whether the user's
product (Work Management, monday service, monday CRM) already ships a prebuilt
agent that does what they want.

---

## What makes a great agent (five things)

1. **A clear trigger** — the event or schedule that kicks it off (item created,
   status changed, column updated, scheduled time, another agent).
2. **A focused job** — one main thing, not five. Agents that do everything do
   nothing well.
3. **The right knowledge** — which boards, columns, docs it reads from (name them
   exactly).
4. **Specific skills/actions** — what it may do (create item, update column, notify,
   post update, draft reply, call another agent).
5. **A grounded persona + boundaries** — tone, what to flag vs handle silently,
   when to escalate, and what to do on missing/ambiguous data. Most misbehaving
   agents are underspecified here.

How monday agents work: you describe the outcome in plain language, review the
generated **Instructions**, refine, then set an **activation** (trigger). Agents
are good at small, repetitive, judgment-light work (intake/triage, research+
summarize, routing, drafting follow-ups, record-keeping, cross-board coordination);
weaker at deep branching logic, complex formulas, high-judgment decisions — design
around that.

---

## Mode A — Interview

Run ONE question at a time. Wait for a full answer. One follow-up if vague, then
move on. Skip anything already answered. If on a client project, pre-fill from
context (board structure, workflow, roles, pain points), say what you're
pre-filling, and ask only what's missing.

1. **The problem** — what workflow/task should this own? What happens manually now,
   or not at all because no one has time?
2. **Trigger** — what kicks it off? (status change? item created? column value?
   schedule? another agent?)
3. **The job** — what exactly does it do when triggered? Walk through the steps as
   if briefing a new team member.
4. **Boards and data** — which boards does it read from / write to? Which columns?
5. **Actions** — what should it be able to *do*?
6. **Edge cases** — what if something's missing or unclear (flag a field? notify?
   skip?)
7. **Persona** — tone for updates/messages; explain reasoning or act silently;
   when to escalate to a human.
8. **Who sees it** — which roles interact with or are affected by it.

## Writing the configuration

When all questions are answered, produce a complete config. **Specific, concrete,
under 400 words. No fluff. Omit empty sections.** Use the user's real board/column/
doc names; keep it copy-paste ready and free of decorative markdown the builder
won't need.

```
## Agent: [Name — short, functional, not cutesy]

**Purpose:** [one sentence — the problem it solves]

**Trigger:**
[exact trigger — event type, board, column, value, or schedule]

**Job (step by step):**
1. [first thing]
2. [second]
3. [etc.]

**Knowledge sources:**
- Board: [name / ID] — reads [which columns]
- Board: [name / ID] — writes to [which columns]

**Skills needed:**
- [action 1]
- [action 2]

**Edge case handling:**
- If [X]: [what it does]
- If [Y]: [what it does]

**Persona:**
[tone, reasoning style, act silently vs explain, when to escalate]

**Affected users/roles:**
[who this touches]
```

Writing principles for the instructions: state the **role/persona** and **outcome**
(not step-by-step plumbing), name **inputs/sources** and **actions** exactly, give
**tone** for anything stakeholder-facing, and spell out **boundaries** (what not to
do, when to ask a human, how to handle missing data). One behavior at a time when
iterating in the builder; define outcomes not mechanics; be concrete about names;
always give a fallback rule; start small then grow; test with real (and messy) items.

## Mode B — Critique & rewrite

Evaluate against these failure modes, give a 2–3 line diagnosis, then rewrite in
the format above:

| Problem | Signs |
|---|---|
| Trigger too broad | "when anything changes" — fires constantly |
| Job too vague | "handle requests" without saying what handling means |
| Too many jobs | routes, summarizes, notifies AND creates items |
| No edge cases | nothing for missing/ambiguous data |
| Persona generic | "be helpful and professional" — no real direction |
| No knowledge sources | doesn't say which boards/columns it reads |
| Actions not scoped | doesn't list what it may do vs leave to humans |

## Mode C — Context-aware suggestion

**Strong fit:** someone manually monitoring a board and repeating an action; a
routing/triage step; a clear trigger + predictable response; multiple boards
kept in sync on status change.
**Not the call:** logic changes every time; needs genuine human judgment; a simple
automation recipe would do it; the client's plan tier doesn't support agents.

Make a specific recommendation, not a question:
> "Based on [client]'s [workflow], an agent fits [specific task] — it triggers when
> [X] and [does Y]. Want me to write the full configuration?"

## Anti-patterns in the final config

- Never "the agent will try to…" — be definitive.
- Never leave edge cases blank.
- Never name it "AI Assistant"/"Smart Helper" — use a functional name ("Intake
  Router", "Status Sync Agent").
- Never combine more than 3 distinct jobs — split into separate agents.
- Never skip the persona.

## Activation and output

After instructions are right, set the activation/trigger (event- or schedule-based;
the available set depends on agent type and release — **check support live**). Match
the trigger to the work (intake/triage fires on new items; digests run on a
schedule). Deliver: (1) what the agent does + which trigger fits, grounded in a
fresh support check; (2) ready-to-paste instruction text; (3) a short note on what
to verify in their account and any limits found.
