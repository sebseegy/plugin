---
name: monday-sidekick
description: >
  Runs a structured interview with the consultant and produces an optimized monday.com Sidekick instruction prompt — specific, grounded in the board context, and ready to configure. Use this skill whenever the consultant says "sidekick prompt", "configure sidekick", "write sidekick instructions", "set up sidekick for", "sidekick for this board", or any variation of wanting to set up or improve a Sidekick configuration for a board or workspace. Also trigger when the consultant describes a use case where a user needs an in-context AI helper inside a board — drafting updates, summarizing threads, answering questions about items, suggesting next steps. If the consultant already has a Sidekick prompt she wants reviewed, use this skill to critique and rewrite it. Always use this skill rather than writing Sidekick instructions freehand.
---

# monday-sidekick

the consultant configures monday.com Sidekick for enterprise clients. This skill produces a focused, board-specific Sidekick instruction prompt through a structured interview.

There are three entry modes:

**Mode A — Interview from scratch**: the consultant wants to set up Sidekick for a board or workspace. Run the interview.
**Mode B — Review & rewrite**: the consultant pastes an existing Sidekick prompt. Skip to the Critique section.
**Mode C — Context-aware suggestion**: the consultant is already working on a client project. Use context to suggest where Sidekick fits and what it should do.

---

## What makes a great Sidekick prompt

Sidekick is an in-context AI helper that lives inside a board or workspace. It answers questions, drafts content, and helps users work with the data they're looking at.

A great Sidekick prompt has:

1. **A clear role** — who Sidekick is in this context (not just "AI assistant", but "intake coordinator for the marketing team" or "status summarizer for the ops board")
2. **Grounded knowledge** — which columns, groups, or fields it should focus on when answering questions
3. **Specific use cases** — the 3–5 things users will actually ask it to do
4. **Tone and language** — how it should communicate (formal? casual? short answers? detailed?)
5. **Guardrails** — what it should NOT do or answer, to avoid hallucinating outside its scope

---

## Mode A: Interview

Run ONE question at a time. Wait for a full answer. Ask one follow-up if vague, then move on. Skip anything already answered.

**If working on a client project**, pre-fill from context and only ask what's missing.

### Interview questions (in order):

1. **The board**: What board or workspace is this Sidekick for? What does the board track or manage?

2. **The users**: Who will use Sidekick on this board — what are their roles, and what do they struggle with or spend time on?

3. **The main jobs**: What are the 3–5 things users will most commonly ask Sidekick to do? (Examples: "summarize this item's updates", "draft a status update", "tell me which items are overdue", "suggest a next step for this request")

4. **Tone**: How should Sidekick communicate — formal or casual? Short and direct, or more detailed? Should it ask clarifying questions or just give its best answer?

5. **Data focus**: Which columns or fields matter most for this board? Which ones should Sidekick always reference when answering questions?

6. **Guardrails**: What should Sidekick NOT do — topics to avoid, actions it shouldn't suggest, scope it should stay within?

7. **Language**: Does the client work in a language other than English, or use specific internal terminology Sidekick should know?

---

## Writing the Sidekick Prompt

Once questions are answered, produce a clean Sidekick instruction prompt. Keep it **specific, grounded, and under 300 words**. No fluff. Write it as if you're briefing Sidekick directly.

```
You are [role name] for [team/board name].

Your job is to help [user roles] work with [what the board tracks].

The most important things users will ask you:
- [Task 1]
- [Task 2]
- [Task 3]
- [Task 4 if applicable]

When answering questions about items, always look at: [key columns/fields].

Tone: [how to communicate — formal/casual, short/detailed, proactive/reactive]

[Internal terminology to know, if any]

Do not: [guardrails — what to avoid or stay out of]

If you're unsure about something, say so clearly rather than guessing.
```

---

## Mode B: Critique & Rewrite

Evaluate against these failure modes:

| Problem | Signs |
|---|---|
| **Too generic** | "You are a helpful AI assistant" — no board context, no specific jobs |
| **No data grounding** | Doesn't tell Sidekick which columns to reference — leads to vague answers |
| **Too many jobs** | Lists 10+ tasks — Sidekick loses focus |
| **No guardrails** | Sidekick answers anything, including things it shouldn't |
| **No tone direction** | Users get inconsistent communication style |
| **Missing terminology** | Client uses internal terms Sidekick won't recognize |

Give the consultant a **2–3 line diagnosis**, then rewrite using the format above.

---

## Mode C: Context-Aware Suggestion

**Sidekick is a strong fit when:**
- Users spend time looking up item status, history, or updates
- Board has lots of text fields (updates, notes, descriptions) that need summarizing
- Team members frequently need to draft updates or messages based on item data
- Users need to answer "what's the state of X" questions regularly

**Sidekick is NOT the right call when:**
- The need is for automated actions (use an Agent instead)
- The board is simple and users rarely need to ask questions about it
- The client isn't on a plan tier that includes Sidekick

Make a **specific recommendation**:
> "For [client]'s [board], Sidekick would be great for [specific job]. Users could ask it to [example task] instead of manually reviewing updates. Want me to write the prompt?"

---

## Anti-patterns to avoid

- Never start the prompt with "You are a helpful, knowledgeable AI" — that's the default, not a useful instruction
- Never list more than 5–6 core jobs — pick the highest-value ones
- Never skip the guardrails — without them, Sidekick will try to answer things it shouldn't
- Never use vague verbs like "assist", "support", "handle" — describe the actual action
