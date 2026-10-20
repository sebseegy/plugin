---
name: deepen
description: Rewrites a task prompt to be deeper (not bigger) using the field-expert method and Felix Rieseberg's ambition framework (Depth, plus Altitude and Range when warranted), then executes the rewritten prompt immediately. Use whenever the user says "deepen this prompt", "make this deeper", "/deepen", "rewrite my prompt like a top pro would", "level up this prompt", "be more ambitious with this", or hands over a task and wants it done at expert depth. Also use when a previous output felt shallow, generic, or pre-digested. Asks clarifying questions only if blocked, shows the rewritten prompt, then runs it without waiting.
---

# Deepen

Take the user's task, rewrite it so a field-leading expert would recognize the approach, then run the rewrite. Deeper means better methods, rawer inputs, and independent verification on the same task. It does not mean more deliverables.

Source logic: the user's four-question depth method plus the "How to be more ambitious" tutorial (Rieseberg, Oct 2026). Axes: Speed (skip, it's solved), Altitude (goal beyond the goal), Depth (expert-grade method and data), Range (other fields' methods). Depth is always applied. Altitude and Range are gated (below).

## Step 0: Get the task and clarify only if blocked

The task is whatever the user pasted or pointed at; if none, use their latest task prompt. Ask via AskUserQuestion (max 3 questions, only blockers) when any of these holds:
- The goal or deliverable is ambiguous in a way that changes the method.
- The rawest source needs access you can't confirm (which account, which client, which dataset).
- Success has no checkable definition and the user must supply one.

Otherwise do not ask. Pick defaults and state them in one line. After the answers, proceed straight through. Do not ask permission to run the rewrite.

## Step 1: Depth analysis (always)

Answer concretely for this task and field. Generic answers ("be rigorous", "research thoroughly") are noise.

1. **Pro move:** What would a top professional do here that the prompt doesn't ask for? Name the move. Surface assumptions baked into the ask and challenge the ones a pro would test ("We believe X. Try to reproduce it from raw data").
2. **Rawest material:** What would they start from instead of what's been digested for the user? Transcripts over summaries, activity logs over dashboards, row-level data over aggregates, primary docs over write-ups. Name the actual source and how to reach it with tools in this session (MCP, API, SQL, files).
3. **Methods and tools:** Name the specific instruments the best practitioners use. When the default is a markdown table or a prose opinion, replace it with the real instrument (a database query, a statistical test, a simulation, a reconciliation). Vocabulary swaps without method swaps don't count. If a method needs something unavailable, say so and name the fallback.
4. **External check:** What, other than Claude or the user, shows the result is right? It must be independent: a test or script that runs, a query against the system of record, a primary source, a reconciliation to a known total, held-out data, a named human with veto. Do not let the model grade itself. If nothing external exists, say so and name the weakest-link assumption.

Then apply two Depth techniques from the article where they fit:
- **Measurable stretch target:** set a hard, specific, checkable target instead of "do your best" (e.g. "reconcile to 100% of rows", "predict held-out cases", "cut X to Y"). Require the report to state what was hit and what wasn't. Never ask the executor to assume success or claim confidence it can't back.
- **Produce new knowledge:** once deep in the raw data, ask for the one blind spot or earliest signal the user doesn't already know, validated on data not used to find it. Include only if the data supports it.

## Step 2: Gated axes (apply only if the test passes)

- **Altitude test:** Is there a real downstream outcome the task serves (a decision, a meeting, a recurring chore) and can the executor reach what's needed to act on it? If yes, add one line to the prompt naming the outcome beyond the task (e.g. "end with the 3 most urgent decisions and for/against for each"). If the task is creative or the outcome is the user's alone to define, skip.
- **Range test:** Would a second field change the method, not just the voice? Convert the noun to a verb ("a quarterly deck" becomes "get busy people to decide under uncertainty in 30 minutes"), then ask which fields do that verb best. If yes, add the field's technique as an instruction (a red-team step: do what a forensic accountant does, i.e. reconcile totals). Never role-play ("write like a short seller"). Add the technique, not the persona.

Flag every gated addition in the delta so the user can cut it. If neither passes, say so in one line.

## Step 3: Rewrite

- Keep the original goal, audience, deliverable, tone, and constraints. Change how the work is done and checked.
- Bake in: raw sources to pull first, named methods, the stretch target, the external check as an executed step with a pass condition, and "report what could not be verified".
- If a source or tool isn't confirmed accessible: "use X if available; otherwise say so and fall back to Y". The executor must not silently substitute the digested version.
- Preserve safeguards. Never drop approval gates or "don't send anything" rules.
- Cut anything the deeper version makes redundant.

## Step 4: Output, then execute immediately

Print in this order, tight:

```
## Depth
1. Pro move: ...
2. Rawest material: ...
3. Methods/tools: ...
4. External check: ...
(Altitude: applied/skipped, why. Range: applied/skipped, why.)

## Rewritten prompt
<single fenced block>

## Delta
- What got deeper (2-4 bullets)
- Gated additions (if any)
- Assumptions/defaults I picked
```

Then run the rewritten prompt right away, in the same turn, following its steps literally, including the external check. Do not ask "should I proceed?". End with the result, what the check showed, and what stayed unverified.

## Execution limits (these override "execute immediately")

- Never send, post, or finalize communication to clients or other real people. Draft only, and say it's a draft.
- Don't modify code/logic or frontend behavior, delete data, or change a live client account without explicit approval. Read-only analysis and drafts proceed; writes stop and ask.
- If the external check fails or can't run, report that as the headline, not a footnote.
