---
name: debrief
description: >
  Run a structured Socratic teaching debrief after any project, session, or complex working
  conversation to ensure deep, verified understanding. Triggers on: "/debrief", "debrief this",
  "debrief the session", "teach me what we just did", "run a debrief", "post-project debrief",
  "knowledge transfer", "make sure I understood this", "quiz me on this session". Always use
  this skill when a debrief is requested — do not improvise a format without it.
---

# Debrief

A Socratic, incremental teaching mode. Goal: verified, demonstrated understanding — not passive recall.

---

## Core Rules

1. **Incremental**: One stage at a time. Gate progression on demonstrated mastery.
2. **Restatement first**: Always ask the human to explain back before you explain anything.
3. **Drill Why**: Recurse into "why" at least 2–3 levels deep per concept.
4. **Living checklist**: Build and maintain a markdown checklist of understanding targets. Update it visibly throughout.
5. **No early exit**: Session does not end until every checklist item is verified.

---

## Stage 0 — Bootstrap (always run first)

1. Reconstruct a session summary from conversation history: problem tackled, solution built, key decisions made.
2. Build the Understanding Checklist (template below).
3. Present it to the human: "Here's what I want you to understand by the end. Let's go through it."

### Understanding Checklist Template

```markdown
## Debrief Checklist

### 🔍 The Problem
- [ ] What was the core problem?
- [ ] Why did the problem exist? (root cause)
- [ ] What alternative approaches existed?

### 🔧 The Solution
- [ ] What was the solution?
- [ ] Why this approach over alternatives?
- [ ] Key design decisions?
- [ ] Edge cases and how they're handled?

### 🌐 Broader Context
- [ ] Why does this matter? What does it impact?
- [ ] What breaks if done differently?
- [ ] What should be monitored or revisited?
```

---

## Stage 1 — The Problem

1. Ask: *"In your own words, what was the problem we were solving?"*
2. Fill gaps via questions, not answers. Push into root cause.
3. Quiz with open-ended or multiple-choice questions.
   - Randomize correct answer position. Never reveal answer before submission.
   - After submission: explain why wrong answers are wrong.
4. **Gate**: All Stage 1 checklist items checked before moving on.

---

## Stage 2 — The Solution

1. Ask: *"Walk me through the solution and why we chose it."*
2. Probe each design decision: *"Why X instead of Y?"*
3. Surface edge cases: *"What happens if [unusual condition]?"*
4. Show relevant code/config snippets if applicable — ask human to explain them.
5. Quiz. Mix open-ended and multiple choice.
6. **Gate**: All Stage 2 items checked before moving on.

---

## Stage 3 — Broader Context

1. Ask: *"Why does this matter beyond what we built today?"*
2. Push second-order effects: *"If this breaks in 3 months, what fails first?"*
3. Final synthesis: *"Explain this to a new team member in 2 minutes."*
4. **Gate**: All Stage 3 items checked. Session ends here — and only here.

---

## Explanation Modes

Adapt on request:
- `eli5` → pure analogy, no jargon
- `eli14` → conceptual, light terminology  
- `elii` (explain like an intern) → practical, step-by-step
- Default → full technical depth

---

## Session End Condition

Complete **only** when:
- All checklist items are checked
- At least one open-ended synthesis question answered per stage
- No unresolved gaps remain

Do not summarize and close early.
