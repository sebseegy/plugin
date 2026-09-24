---
name: "vibe-prompt-injection"
description: "Co-pilots the iterative prompt loop on a live monday.com Vibe app: Basti describes what he needs, this skill writes the exact prompt to paste into Vibe (or Sidekick, or a workflow spec when Vibe is the wrong tool), then reads Vibe's pasted reply back, judges whether it really landed, and writes the next prompt. Use whenever Basti says \"write the vibe prompt\", \"what should I prompt next\", \"here is vibe's reply/answer\", \"Vibe said\", \"prompt injection\", \"write the prompts to fix\", pastes a Vibe change log or \"App ready\" / \"Oops, something went wrong\" output, drops a Vibe code export folder (e.g. Downloads/src N), or asks why a Vibe app is slow, broken or insecure. Use vibe-board-builder instead for a greenfield app (boards + first build prompt); hand over to this skill once the app exists."
---

# Vibe Prompt Injection

Basti operates the Vibe builder; you are the engineer behind him. You never see the app
directly — you see what he pastes (replies, screens, audit panels) and, when he provides one,
the exported source. Every prompt you write goes through him, so each one must be
copy-paste-ready, scoped to one job, and verifiable from what he can paste back.

Platform facts (board limits, Vibe DB, public apps, credits, Memory) live in
`vibe-board-builder` — read its relevant section before asserting a platform capability, and
re-verify anything stakes-sensitive against the mondayall knowledge base or #ask-vibe-ai.
This skill holds the *loop* and the production lessons.

## The loop

```
Task Progress:
- [ ] 1. App card: know which app, boards, state, source
- [ ] 2. Route: Vibe, Sidekick, workflow, or manual board work?
- [ ] 3. Ground: read the code export / board schema, not Vibe's self-description
- [ ] 4. Write prompt(s): one job each, fenced, with Verify + Report
- [ ] 5. Hand off: target app, mode, order, what to hold
- [ ] 6. Judge the reply: landed? in scope? deviations? regressions?
- [ ] 7. Verify for real: runtime test script or read-only report prompt
- [ ] 8. Log it, then next prompt
```

### 1. App card

Before the first prompt of a session, establish (ask only for what's missing):

- **Which app** — name and full-page URL (`/misc/vibe/full-page-app/object?object-id=…&app-feature-id=…`).
  Clients often have more than one Vibe app (Wren: Call-Off portal *and* the Setup Wizard /
  Options Picker). Every prompt names its target app; Vibe has answered "there is no Setup
  Wizard in this codebase" when a prompt meant for one app went to the other.
- **Connected boards** — board IDs and the column IDs the change touches.
- **State** — published? Auto Update on or off (changes may sit in draft)? Plan or Discuss mode
  on? Vibe DB in use (no draft/live split — draft tests write real data)?
- **Source** — latest code export path, and which prompt it predates ("src 5 = before the last prompt").
- **App Memory** — what Vibe has "Saved to memory". Stale memory re-imposes old rules.
- **Who uses it** — roles, license types (Viewers can't open Vibe apps), internal vs public.

If a project folder exists, keep the card and the prompt log in
`<Project>/docs/vibe-prompt-log.md` so the next session starts from facts, not recall.

### 2. Route — is this a Vibe prompt at all?

| Need | Right tool | Why |
|---|---|---|
| App UI, app logic, server functions, in-app diagnostics | **Vibe** | Only Vibe edits the app |
| Read/audit/fix board data or schema in an account you can't reach via MCP | **Sidekick** (read-only first, then gated writes) | Sidekick sees the account; Vibe only sees connected boards |
| "When X happens on a board, create/link items" (provisioning, cross-board create) | **monday workflow/automation** | Native, event-driven; Vibe has no background jobs |
| Call an external service (REST API) | **Vibe**, via the API Requests integration | API-token auth only (no OAuth), GET/POST/PUT, 1 credit per call and per page. Basti adds the token in the integration; the prompt never contains the key and the code must never hardcode it |
| Trigger on a mirror column | **Legacy recipe built by hand in the UI** | `create_automation` (workflow engine) rejects mirror triggers; the legacy recipe with `mirrorColumnConfig` works but isn't in the public API |
| New board columns | **Sidekick / MCP / by hand first**, then a Vibe prompt that resolves them by ID and halts if missing | Keeps schema changes verifiable and out of app code (Wren pattern); Vibe's board-editing subagent exists but wasn't relied on |
| Duplicating managed templates / creating boards | Workflow or manual | Not what the app layer is for; keep it native and reversible |

Red flag: Vibe proposing a temporary screen to "inspect" an unconnected board (WHSmith Intake).
That is a detour — the answer is a Sidekick read-only audit, not new app surface.

### 3. Ground before writing

- **Code export beats chat.** When Basti drops a `src` folder, read the actual files: name
  functions, files and lines in the prompt. Vibe's own summary of its code has been wrong.
- **Board schema from the live API** (MCP if the account is reachable, else a Sidekick
  read-only prompt returning title / ID / type / labels). Never infer IDs from titles.
- **Check whether it's already built** before asking for it again — Basti queues prompts, and
  replies arrive out of order.
- **Search prior prompts** in the log/transcripts so a new prompt doesn't undo a previous fix.

### 4. Write the prompt

Default anatomy (full templates in [prompt-templates.md](prompt-templates.md)):

```text
<Scope line: "Fix X only." / "One change." / "Read-only. Change nothing.">

<Current behaviour / defect — concrete: file, function, the wrong rule, the observed symptom>

Required changes:
1. …
2. …

Do not <fence 1>. Do not <fence 2>. <Name adjacent systems that must stay untouched.>

Verify:
1. <concrete scenario with real item/site/project IDs → expected result>
2. <the regression you're most afraid of → must still hold>

Report <files changed / guards touched / exact mechanism / anything you could not verify>.
```

Rules for every prompt:

- **One job per prompt.** Split "read → act" into two prompts when IDs or state are unknown
  (Prompt A: print the schema; Prompt B: act on the confirmed IDs). Never let Vibe guess an ID —
  unconfirmed IDs stay explicit TODOs.
- **Fence the blast radius.** List what must not change (validation severity, write paths,
  other screens, access rules, finance maths). Vibe widens scope when not fenced — it narrowed
  WHSmith's access grant to PMs only, and removed Sponsors, without being asked.
- **State the rule, not just the fix.** "A project is identified by its exact code — never
  contains, includes, fuzzy name or a hardcoded list" survives future prompts; "change contains
  to equals in loadTracker" does not.
- **Concrete Verify cases** with real IDs (Alresford `3228063530`, PR215 vs PR2159). Include the
  race/edge case: "start A+B, switch to B+C, let A+B finish last → state is B+C only".
- **Demand a Report** that proves mechanism: files changed, guard names, before/after timings.
- **Plain words, exact labels.** Quote status/dropdown labels verbatim (including client typos
  like "Call Off Recieved").
- **Credits are real.** Cost depends on complexity and the AI model chosen in Vibe; observed
  35–454 credits per prompt. Large multi-part prompts cost most and failed prompts still charge.
  Don't spend a prompt on cosmetics while correctness is open.
- **Point, don't describe, for UI changes.** Tell Basti to click the element with the element
  selection tool and keep the prompt to what should change.

Apply the production lessons in [field-lessons.md](field-lessons.md) — they're the
rules Vibe-generated code has repeatedly broken (title-based column lookup, `contains` joins,
blank-as-default, inferred-state writes, UI-only permissions, query-param deep links).

### 5. Hand off

Tell Basti in one short block:

- **Target app** and **mode**: "Paste into the Call-Off App, Plan and Discuss off, then Build."
  Use **Plan mode** when you want Vibe to propose an approach before building. Discuss mode is
  limited/unreliable as of 2026-09 — for answers without code, send a "Read-only. Change
  nothing. Report…" Build prompt instead.
- **Order and holds**: "Send 1 now. Hold 2 until 1 reports ready — both edit
  `SitePoolsPanel.jsx`." Only queue prompts that touch disjoint files; queued prompts that
  overlap produced half-applied, uncertain states on Wren.
- **What to paste back**: the full reply, plus a specific screen or audit panel if needed.

### 6. Judge the reply

Run this checklist on every pasted Vibe reply before writing anything new:

| Check | Look for |
|---|---|
| **Did it finish?** | "App ready" vs **"Oops, something went wrong"** mid-run → assume half-applied. Next prompt is read-only: "report what actually landed, does it build". If it landed but is simply wrong, "undo this" reverts the last edit — cheaper than a corrective prompt. |
| **Scope** | Files changed vs files expected. Any new route, nav item, screen, board read, or narrowed permission you didn't ask for? |
| **Deviations** | Vibe often says "that's my deviation, on purpose". Evaluate each one explicitly — accept with reason or reject with a corrective prompt. Many were right (e.g. refusing to treat an empty column as stale). |
| **Claims vs evidence** | "Verified" in chat is a code trace, not a runtime test. The fixed footer ("turn off Discuss mode…") means nothing. |
| **Contradictions with prior fixes** | Does this reply reintroduce a title lookup, a `contains`, a default-to-External, an optimistic write? |
| **Memory** | "Saved to memory" lines → what rule got saved? Old rules in App Memory will fight new prompts. |
| **Board prerequisites** | Did the change create a new dependency (e.g. the Project Manager column is now the only access grant, and it's empty)? |
| **Credits** | Note the spend; flag if iteration is burning credits on a platform problem, not a prompt problem. |

Then give Basti a verdict first ("Landed clean — one deviation worth accepting", "Half-applied
— don't send anything else yet"), then the next action.

### 7. Verify for real

- **Runtime test script** for Basti: numbered, observable, ending with the one test that
  matters (e.g. "open the PR2159 link in a private window as the named PM — Spend log, no
  Approve buttons"). Use a private window to see what a non-admin sees.
- **Read-only report prompt** to Vibe when you need code facts ("Do not change code yet.
  Verify and report: which branch of resolveEntry runs when…").
- **Sidekick read-only audit** for board facts after app writes (records landed, links set,
  labels correct).
- **Fresh code export** after a series, to diff against what was claimed.
- After every security-relevant change, re-run the access tests — later prompts regress earlier
  guarantees silently.

### 8. Log and continue

Append to the prompt log: number, target app, one-line intent, status
(`sent` / `landed` / `half-applied` / `rejected` / `verified live`), credits, open follow-ups.
Close each turn with the single next step, not a menu — unless a decision is genuinely Basti's
or the client's (then name who decides: "Kim's call").

## Sidekick prompts inside the loop

When the fact lives on a board you can't read, write a Sidekick prompt with the same
discipline (template in [prompt-templates.md](prompt-templates.md)):

- Start **read-only**; match boards and columns **by ID**, never by title alone.
- Ask for a **READY / NOT READY** verdict and only the missing pieces.
- Gate writes behind an explicit phrase (`APPROVE IMPLEMENT <board ID>`), one board at a time.
- Batch bulk edits (e.g. 11 items per batch) with read-back after each batch.
- Run it at the scope that can see everything needed (workspace-level if several boards).

## Talking to Basti

Lead with the verdict, then the prompt in a ```text block, then the hold/next line. Keep
analysis short; he wants the paste-ready artifact. Prompts are English and imperative; keep
client vocabulary (plots, call-offs, tenures, pots, CR slots) exactly as the client uses it.

## Additional resources

- [prompt-templates.md](prompt-templates.md) — copy-ready templates per prompt type, with real examples
- [field-lessons.md](field-lessons.md) — production rules learned on Wren and WHSmith
- `vibe-board-builder` — platform facts, Vibe DB vs boards, public-app auth, greenfield workflow
