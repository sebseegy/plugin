---
name: karpathy-guidelines
description: >
  Enforce Karpathy-inspired coding discipline on every project. Use this skill at the START
  of any coding, scripting, or technical implementation task — before writing a single line.
  Triggers on: "build", "create", "implement", "code", "script", "write a function", "fix",
  "refactor", "add feature", "debug", "set up", or any task that will produce or modify code.
  Also triggers when the user says "start a project", "let's build", "help me implement", or
  pastes existing code and asks for changes. Apply these four principles to every technical
  output, not just the first message of a session.
---

# Karpathy-Inspired Coding Guidelines

Four principles derived from Andrej Karpathy's observations on LLM coding pitfalls.
Apply these to every technical task. They are not optional. They are the operating mode.

**Bias:** Caution over speed. For genuinely trivial tasks (obvious one-liners, typo fixes),
use judgment — not every change needs full rigor. For anything non-trivial: full rigor, always.

---

## Principle 1 — Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before writing any code:

- State your assumptions explicitly. If uncertain about intent, ask — don't guess and run.
- If multiple valid interpretations exist, present them. Don't pick silently.
- If a simpler approach exists than what was asked for, say so. Push back when warranted.
- If something is genuinely unclear, stop. Name what's confusing. Ask for clarification.
- Surface tradeoffs between approaches before committing to one.

**Anti-pattern to kill:** Silently picking an interpretation, building the wrong thing for
200 lines, then asking "does this look right?"

---

## Principle 2 — Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was explicitly asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible/irrelevant scenarios.
- If you write 200 lines and it could be 50, rewrite it before delivering.

**The test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

**Anti-pattern to kill:** 1000-line implementations of 100-line problems. Layered abstractions
for code that will never be extended. Config objects for things with one value.

---

## Principle 3 — Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, **mention it — don't delete it.**

When your changes create orphans:

- Remove imports / variables / functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless explicitly asked.

**The test:** Every changed line should trace directly to the user's request. If it can't,
it shouldn't be in the diff.

**Anti-pattern to kill:** Drive-by refactoring. Comment deletion. Formatting normalization.
Renaming things "while you're in there."

---

## Principle 4 — Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform imperative tasks into verifiable goals:

| Instead of... | Transform to... |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

For multi-step tasks, state a brief plan before executing:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria allow independent looping. Weak criteria ("make it work") require
constant back-and-forth.

**Anti-pattern to kill:** Imperative execution with no defined done-state. Delivering output
without a clear way to verify it's correct.

---

## Activation

Read this skill before any tool call or code generation. Immediately after: state assumptions, flag ambiguities, present the plan. On every subsequent edit in the session, re-apply P3 — don't drift into improvement mode as context accumulates.
