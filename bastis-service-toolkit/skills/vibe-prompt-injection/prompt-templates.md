# Prompt templates

Copy-ready shapes that worked in production. Replace every `<…>`; delete lines that don't apply.

## Contents
- Change / fix prompt
- Read-only report prompt
- Recovery after "Oops, something went wrong"
- Two-step: print schema, then act
- Removal prompt
- Access-model prompt
- Performance prompt
- Sidekick read-only audit
- Sidekick gated write

---

## Change / fix prompt

```text
<Fix X only. | One change.> Do not restyle screens.

Current defect:
<What happens today, in which file/function, and the visible symptom.>

Required changes:
1. <…>
2. <…>

Do not change <validation severity / mode rules / board writes / other screens / access>.
Do not <connect new boards / add nav items / add runtime AI>.

Verify:
1. <Scenario with real IDs> → <expected>.
2. <Edge case or race> → <expected>.
3. <The thing that must still work> → unchanged.

Report the exact files and functions changed and <the mechanism / before-after timing>.
```

Real example (Wren, data-loss fix):

```text
Critical data-loss fix only.

SpecEditor reads original.splashbackRequirement in useSpecEditor, but EMPTY_FORM and the
setForm seed omit it. Opening an existing option and saving an unrelated change can therefore
stage Splashback Requirement from its stored value to blank.

Required changes:
- Add splashbackRequirement: '' to EMPTY_FORM.
- When original loads, seed: splashbackRequirement: original.splashbackRequirement || ''

Do not change validation, mode rules, relations, labels, or any other field.

Verify:
1. Load an option where Splashback Requirement = Required.
2. Change Lead Time only.
3. Preview must contain no Splashback Requirement change.
4. Save and re-read: Splashback Requirement remains Required.
5. Deliberately changing the requirement must still preview, write, and verify correctly.

Report the exact files and lines changed.
```

---

## Read-only report prompt

Use before building on uncertain state, or to check a claim.

```text
Do not change code yet. Verify and report.

1) <Question about a specific code path — "which branch runs when…">. Say exactly which
   branch. If it is broken, say so — do not fix it yet.
2) <Quote the exact message text shown to <role>.>
3) <Data fact the app can see — populated or empty, counts, not names.>
4) Confirm the app builds and <the N screens> still render for <role>.
```

---

## Recovery after "Oops, something went wrong"

A mid-run error means the change may be half-applied — worse than either end state.

```text
Read-only. Change nothing.

A previous turn began <the change> and failed partway with an error. I need the current state
before continuing.

Report:
1. Does <new module / map / resolver> exist? File path and contents.
2. For each of <consumer A, B, C>: does it use the new path, the old path, or both?
3. List every remaining <old pattern — e.g. exact-title lookup / contains join>, with file and line.
4. Does the app currently build?

Do not fix anything. Report only.
```

Then split the remaining work: "create the new module only" → verify → "switch consumers over".

---

## Two-step: print schema, then act

Never let Vibe guess an ID.

Prompt A:
```text
Read-only. Change no resolution logic.

Board: <name> <board ID>

Add a one-time console print, at the point this board's schema is read, listing every column:
id, title, type. State which column currently resolves as <logical field>, by which route
(exact title / substring / id), and its id and type.

No board writes. Report the full column list so the ids can be verified before they are configured.
```

Prompt B (only after A returns the IDs):
```text
Resolve <board> columns by ID, not title.

Add this board to the centralized column map using the ids confirmed in the schema print.
Do not guess any id; unconfirmed ids stay explicit TODOs and that field stays unresolved.

Rules:
- Find the column by configured ID; verify the actual type matches the expected type.
- Titles are display only. A renamed column must resolve normally and be reported as renamed.
- Never substitute a column with a similar title.
- Absent ID or wrong type fails closed, naming board ID, expected column ID, expected type and what was found.

Do NOT change <classification / save gates / validation / board writes>.

Verify: a mocked rename still resolves; a mocked wrong type blocks with the full reason.
Report every field configured and anything still resolving by title.
```

---

## Removal prompt

For features Vibe added that nobody wanted, or tools that became dangerous.

```text
Remove <feature> completely.

- Remove its route, nav entry, page, components and the server functions only it used.
- Remove imports and files made unused by this removal.
- Do not <write to / clear> <board columns> from the app — we handle those by hand.

Keep exactly as they are: <list of screens, access model, guards, business rules>.

Report what was removed and confirm no code path still <reads board X / writes column Y>.
```

---

## Access-model prompt

UI hiding is not security. Enforce on the server, test through direct calls.

```text
Implement the <two-entry> access model only. Do not restyle screens. Do not change
<finance maths / approvals / board schemas>. Do not make the app public.

<Role A> = <how identified — workspace admins plus named list>.
- <What they can open and do.>

<Role B> = members named on the item's <people column>.
- Enter only through <route / item view>.
- May <actions>. Must not <actions> (UI and server).
- Must not see <screens, pickers, other records>.

Implementation:
1. Every read and write verifies server-side: exact item id AND exact code match, and viewer is
   <Role A> OR named on that item. A changed URL parameter must fail closed.
2. <Role B> opening any other route gets: "<locked notice text>". Load no wider data first.
3. Navigation state (e.g. lock=1) is not authentication. Links carry no tokens.

Verify:
- <Role A> opens root → <landing screen>.
- Named <Role B> opens their link → their record only.
- <Role B> edits the code/ID in the URL → refused.
- Person not on the people column → refused.
- <Role B> calls the approve function directly → refused.

Report every route, access helper and server guard changed. Confirm enforcement is server-side.
```

Board-side checklist to hand Basti with it: people column populated on every record (it's now
the only grant), every user a Member not a Viewer, board permissions sufficient (the app cannot
elevate them).

---

## Performance prompt

Ask for measurement before optimisation when numbers are unknown.

```text
Follow monday vibe performance guidance: cache board data, query fewer columns, filter before
querying. <Do not "load only the first 20 items" — this list must stay complete for <save checks>.>

Problem: <which hook/read, how often it runs, measured time if known>.

Do this:
1. <Single shared read instead of N duplicate reads.>
2. <Paint from cache immediately; live read still required before <save>. Never judge <validity> from cache alone.>
3. <Timeout of Ns on the live read; on timeout stop spinning, name board <ID>, Retry.>
4. <Show stage: cache / schema / page N.>
5. <Resolve only the linked IDs (by-id lookup), not a full board walk.>

Do not <add columns / connect boards / add runtime AI / change save gates>.

Add timing evidence: <per-step timings stored and shown on the diagnostics screen>.
Report before/after timings.
```

---

## Sidekick read-only audit

```text
Read-only. No writes.

Target board ID: <ID>. Do not touch <source board IDs>.

Gold standard (<reference board ID>): <what correct looks like — columns, mirrors, recipes, labels>.

On board <ID> report:
1. Board name and workspace.
2. Every board_relation column: title, ID, linked board IDs. Do not trust display names alone.
3. Every mirror column: title, ID, relation column, displayed column ID, source board ID.
4. <Status column matched by purpose>: title, ID, full label list with indexes.
5. Existing automations: ID, active state, recipe ID, trigger, action. Flag duplicates.

Verdict: READY or NOT READY. If NOT READY, list only the missing pieces.
Do not create columns or automations.
```

## Sidekick gated write

```text
<Create columns only. No automations.> Board ID <ID> only.
Never write to <protected board IDs>.

Preconditions: <what must already exist>. If missing, STOP. Do not guess another board.

Create exactly:
1. <Title / type / settings>

Re-read from the API and report <title, ID, type, settings verbatim>. STOP.
```

Pair with: "Never create, update, activate or delete anything until I write:
APPROVE IMPLEMENT <board ID>." For bulk data fixes, batch (≈10 items) with read-back after
each batch and wait for go-ahead between batches.
