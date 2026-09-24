---
name: monday-ai-advisor
description: >
  Explains monday.com AI features clearly, helps the consultant understand when to use each one, and acts as a decision guide when she's unsure which AI tool fits a situation. Use this skill whenever the consultant asks "what's the difference between X and Y", "when should I use an agent vs sidekick", "explain how AI columns work", "can monday AI do X", "what are the limits of", "how do I pitch this AI feature", "which AI feature is best for", or any question about understanding, comparing, or explaining monday.com AI capabilities. Also trigger when the consultant is preparing to demo or pitch AI to a client and needs a clear, jargon-free way to explain it. This skill explains and advises — it does not build. For building, it hands off to the right builder skill.
---

# monday-ai-advisor

the consultant is an IC who needs to understand monday.com AI features deeply — both to build with them and to explain them to clients who have never used AI in a work tool before.

This skill does three things:
1. **Explains** a feature clearly — what it is, how it works, what it can and can't do
2. **Compares** features when the consultant isn't sure which fits a situation
3. **Helps pitch** — translates technical capability into plain client language

This skill does NOT build prompts or configurations. When the consultant is ready to build, it hands off to the right skill.

Before explaining a feature, check `references/changelog.md` — a dated log of confirmed releases fed automatically by `weekly-pulse` each week — so the explanation reflects the latest confirmed capability, not just the static map below.

---

## The monday.com AI feature map

### Agents
**What it is:** An autonomous AI worker that monitors boards and takes action when triggered.
**How it works:** You define a trigger (event, schedule, or another agent), give it skills (actions it can take), and point it at knowledge sources (boards, columns, docs). It runs in the background without anyone clicking anything.
**Best for:** Repetitive multi-step workflows — routing, triage, status syncing, notifications based on data patterns.
**Not for:** Tasks that require human judgment, relationship context, or unpredictable logic.
**Plan tier:** Check current availability — has been rolling out progressively.
**Client pitch:** "Instead of someone manually checking the board every morning and moving things around, the agent does it automatically. It's like giving your team a new colleague who only does the boring, repetitive stuff."

---

### Sidekick
**What it is:** An in-context AI helper that lives inside a board or workspace and answers questions, drafts content, and helps users work with what they're looking at.
**How it works:** Configured with a prompt that tells it its role, what data to focus on, and how to behave. Users interact with it via a chat interface on the board.
**Best for:** Summarizing long update threads, drafting replies or status updates, answering "what's the state of X" questions, helping new team members navigate a complex board.
**Not for:** Taking automated actions (that's agents). Sidekick responds to questions; it doesn't act on its own.
**Client pitch:** "It's like having a smart colleague sitting next to you who has read every update on every item. You can ask it to catch you up, draft a message, or explain what's happening — without digging through everything yourself."

---

### Vibe
**What it is:** AI that turns a plain-English description into a fully working app inside monday.com — no code needed.
**How it works:** You write a prompt describing what you want (purpose, users, data, layout, actions), paste it into the Vibe builder, and it generates the app. You can iterate with follow-up prompts.
**Best for:** Building custom-feeling apps fast — client portals, intake forms, dashboards, trackers — especially when the client wants something that doesn't look like a standard board.
**Not for:** Complex multi-board logic, automations, or anything requiring precise data connections across many boards (better to build manually).
**Client pitch:** "Instead of months of development, we describe what you need and the platform builds it. We can have a working prototype in an hour that we then refine together."

---

### AI Columns
**What it is:** Columns that use AI to process text and produce a result — summarize, classify, extract, or generate content.
**How it works:** You configure the column with an instruction prompt, point it at source columns, and it processes each item's data to produce an output. Can run automatically or on demand.
**Types:**
- **Summarize** — condenses long text into a short summary
- **Classify** — assigns a label from a list you define
- **Extract** — pulls specific fields out of unstructured text
- **Generate** — creates new text based on item data
- **Formula** — open-ended AI reasoning for anything else
**Best for:** Structuring unstructured data (form submissions, emails, notes), routing based on content, auto-generating descriptions or replies.
**Not for:** Deterministic logic (use regular formulas), data that needs to be 100% consistent and auditable.
**Client pitch:** "Every time a form comes in, the AI reads it and automatically categorizes it, pulls out the key details, and routes it to the right team — instead of someone doing that manually for every submission."

---

### AI in Automations
**What it is:** AI action blocks inside monday.com's automation recipes — same AI capabilities as columns, but triggered by automation events and able to feed results into subsequent automation steps.
**How it works:** Add an AI action step inside an automation recipe. It can classify, extract, summarize, or generate, and pass the result to the next step (update a column, notify someone, create an item).
**Best for:** Connecting AI processing to a workflow — e.g. "when a form is submitted, AI classifies the request type, then routes it to the right group, then notifies the right person."
**Not for:** Standalone AI output that doesn't feed into further automation steps (use AI columns instead).
**Client pitch:** "When a request comes in, the system reads it, understands what kind of request it is, and automatically sends it to the right place — no human triage needed."

---

## Decision guide — which feature fits?

Use this when the consultant isn't sure what to recommend:

| Situation | Best fit |
|---|---|
| Repetitive manual monitoring + action on a board | Agent |
| Multi-step workflow triggered by an event | Agent |
| Users need to ask questions about board data | Sidekick |
| Users need to draft updates or messages | Sidekick |
| Client needs a custom-feeling app fast | Vibe |
| Unstructured text needs to be classified or parsed | AI Column (Classify / Extract) |
| Long text fields nobody reads | AI Column (Summarize) |
| Auto-generate descriptions from item data | AI Column (Generate) |
| AI output needs to trigger further automation steps | AI in Automations |
| "I want AI but I don't know where" | Run monday-ai-suggester |

---

## Comparing features side by side

When the consultant asks "what's the difference between X and Y", use this framework:

1. **What triggers it** — event/user/schedule?
2. **What it reads** — which data?
3. **What it does** — passive answer vs. active action vs. content generation?
4. **Who sees the result** — the user, the board, an automation?
5. **Does it act on its own or wait to be asked?**

The clearest split:
- **Agent** = acts on its own, triggered by events
- **Sidekick** = waits to be asked, responds in context
- **AI columns** = processes data at the item level, produces a field value
- **Vibe** = builds the interface itself

---

## Pitching AI to clients — principles

- **Lead with the pain, not the feature.** Don't say "we can add an AI column." Say "right now someone on your team is reading every form submission and manually copying the requester name into a field — we can eliminate that entirely."
- **Show one thing at a time.** Showing three AI features in one demo is overwhelming. Pick the highest-impact one first.
- **Use their language.** If they call it "case routing", call it case routing. Don't introduce AI jargon.
- **Set honest expectations.** AI outputs have variance. Classify columns aren't 100% accurate. Agents can misfire on edge cases. Say so upfront — clients who discover limitations themselves lose trust. Clients who were told upfront trust you more.
- **The wow moment matters.** Find the one thing the AI does that makes them say "wait, it does that automatically?" and lead with it.

---

## Handing off to builder skills

When the consultant is ready to build, point her to the right skill:

- Building an agent → **monday-agents** ("say 'build an agent' and I'll walk you through it")
- Setting up Sidekick → **monday-sidekick** ("say 'sidekick prompt' and I'll run the interview")
- Configuring AI columns → **monday-ai-columns** ("say 'AI column' and we'll configure it together")
- Building a Vibe app → **monday-vibe** ("say 'vibe prompt' and I'll interview you")
- Finding AI opportunities in a client case → **monday-ai-suggester** ("say 'AI ideas for [client]' and I'll pull the latest features and map them to the case")
