---
name: monday-vibe
description: "Design and prompt monday vibe apps — monday.com's AI-powered no-code app builder at monday.com/vibe. Use whenever the user wants to build an app on monday vibe, mentions 'monday vibe', asks to create a custom app or view inside monday.com, wants to turn a workflow into an app, says 'vibe coding' or 'generate a vibe prompt', or describes a work problem and is a monday user (they may not know vibe exists). Interviews the user, then outputs a ready-to-paste vibe prompt. monday vibe changes fast and the team accumulates internal know-how, so this skill ALWAYS checks current vibe docs on support.monday.com AND searches Slack for internal recommendations before advising — never from memory alone. This is NOT the Vibe Design System (React) or the monday apps developer MCP."
---

# monday vibe App Design & Prompting

**monday vibe** (monday.com/vibe) is monday.com's no-code AI app builder. Describe
what you want in plain language and it generates a working app — data schema, UI,
workflows, permissions — inside monday.com, no code. This is NOT the Vibe Design
System (React components) or the monday apps MCP (developer tooling).

Your job: interview the user, ground yourself in current docs + internal knowledge,
then output a ready-to-paste vibe prompt.

**Quick baseline first:** skim `references/changelog.md` — a dated log of confirmed
vibe releases fed automatically by `weekly-pulse` each week. It's a fast starting
point, not a replacement for the live check below on anything stakes-sensitive.

## Ground yourself before advising — always check docs AND Slack

vibe is fast-moving, and the team's best practices live as much in Slack as in the
docs. Before giving specific guidance, prompts, or claiming what vibe can/can't do,
do both and fold what you find in:

1. **Latest vibe docs.** Run `site:support.monday.com vibe <topic>` (and check
   monday.com/vibe). Confirm current capabilities, limits, supported patterns, and
   stated best practices rather than assuming — the static guidance below may lag
   the product. If a page is a JS-rendered shell, retry to read snippets or open
   with browser tools. Surface sources as links.
   The FAQ/troubleshooting article is often blocked by a bot check when fetched
   automatically — use Company Brain (below) to reach it.
2. **Slack for internal recommendations.** Search for working prompt patterns,
   gotchas, performance tricks, things to avoid (terms: "vibe", "monday vibe",
   "vibe app", plus the app domain). Prefer recent messages and people who own/use
   vibe. Cite the threads you relied on.
3. **Company Brain** (`company-brain-agent`, poll with `check-status`) answers from the
   CS knowledge base, CX Genie, Sales knowledge and #ask-vibe-ai in one query —
   the fastest way to get limits, packaging and pricing with sources. Ask it to cite
   sources and dates, and treat anything it marks uncertain as unconfirmed.

When internal advice and docs conflict, surface both and note the tension. If
something isn't documented and no one's covered it, say so rather than inventing.

## The interview

Run as a real conversation — **one question at a time**, wait for the full answer,
one follow-up if vague, skip what's already answered.

1. **The problem** — what task or pain are you solving? (describe what's broken/slow
   today, not the app yet)
2. **The users** — who uses it (you, team, roles)? What must they be able to do?
3. **The data** — what information must it work with? (fields, categories, statuses,
   dates, names, numbers)
4. **The structure** — what should it show? Dashboard? Form? Table? Timeline?
   Charts? **Any wireframe/screenshot to base layout on? Share it now.**
5. **The actions** — what can users do? (create, update, submit, filter, approve,
   export)
6. **Existing boards** — does it connect to monday boards/data already set up?
7. **Constraints** — must-haves, must-nots, specific fields, permissions?
8. **Visual reference** — brand colors or a screenshot/website/app to match? Share now.
9. **Device** — mostly desktop or mobile?

Handling vague answers: "track things" → track what, for whom, what's a good
outcome? "Like a dashboard" → what's on it, who reads it? "Keep it simple" → note
it but still get specifics. "Don't care about design" → skip Q8, default desktop.

## Output: the vibe prompt

A single clean **foundation prompt** to paste into the vibe builder chat. monday's
official guidance is to cover four things: **what** you're building, **who** it's for,
the **tasks** it performs, and how it should **look and feel** — there's no length
limit. For a simple standalone app, aim for under ~350 words, start with "Build me an
app that…", plain language, omit empty sections. Save to plain `.txt` if saving to
file (minimal formatting — no `===`/`---`/`***` separators).

Pick the right path first:
- **Scope still fuzzy?** Tell the user to turn on **Plan mode** (the "Plan" toggle in
  the prompt box): vibe proposes features, a design direction and a flowchart before
  building. The first prompt may cost more credits but saves iterations.
- **App reads/writes several monday boards, has roles, or goes to a client?** Use
  the `vibe-board-builder` skill — it designs the boards and writes a longer,
  ID-based build prompt.
- **App already exists and needs changes or fixes?** Use `vibe-prompt-injection`.

```
Build me an app that [core purpose].

Users: [who uses it and what they need to do]

Data fields: [key fields/columns needed]

Views/screens: [what each screen/section shows — if a structural reference was shared, describe the layout it implies]

Actions: [create, update, filter, submit, etc.]

Board connections: [existing monday boards to pull from or write to]

Constraints: [must / must not]

Design: [light/dark/mixed]. Colors: [brand colors or direction]. Typography: [fonts or "clean sans-serif"]. Style: [spacious, editorial, bold headings, rounded buttons…]. Optimized for: [desktop/mobile]. Inspired by: [visual reference — omit if none].
```

## Design & performance best practices (fold in, confirm against docs)

- **Batch API calls** — combine queries; avoid one call per entity.
- **Keep UI simple** — no complex charts, animations, decorative high-perf elements.
- **Server-side calculations** — read pre-calculated values; use the **aggregation
  API** for counts and totals instead of fetching every item.
- **Load only what's needed** — query fewer columns (e.g. just name + status), filter
  by date range, skip items marked done, and **lazy-load** secondary boards only when
  the user opens that tab.
- **Paginate large data** — 50–100 item pages; show initial results fast. Board
  queries cap at ~500 items per call. Don't paginate a list that must be complete for
  a validation or save check.
- **Cache large boards** (1,000+ items) in browser local storage for instant reloads,
  with a staleness window and a visible Refresh — a bad fetch cached in local storage
  is served for the whole window and a browser reload doesn't clear it. Cache may
  paint the screen; it must never approve a save.
- **Timezone safety** — treat dates as noon local time, not midnight, to avoid
  day-shift from UTC conversion.
- **Theme tokens** — use semantic `bg`/`border`/`fg`, not `white`/`gray-800`, so
  light/dark modes work.
- **Optimistic updates only for visual state** (toggles, expand/collapse). For data
  writes, save → re-read → then show success; never claim a save that wasn't verified.
- **Columns by ID** — have vibe resolve board columns by column ID and type, not by
  title; renamed columns otherwise break the app.

## Prompt engineering

vibe responds best to simple clear instructions, **one change at a time** (verify
before continuing), and small steps with checkpoints — don't pack multiple big
changes into one prompt. Structure a prompt around: persona/role, core function,
data entities, workflows (when X → do Y), UI preferences, permissions.

Avoid assuming deep branching logic or complex formulas, that project boards
already exist, or over-engineering the first iteration — get core working, then
refine.

Builder tools worth telling the user about:
- **Element selection tool** — click an element in the editor to reference it in the
  prompt instead of describing where it is (appears on existing apps after one more edit).
- **"undo this"** in the chat reverts the last edit.
- **Auto Update off** after publishing keeps new changes in draft until "Update changes".
- **Prompt queueing** — prompts run in order; only queue prompts that change different
  parts of the app, or they can collide.
- **Upload a sketch, screenshot or CSV/XLSX** (up to 5,000 rows; always creates a new
  board) instead of describing layout or data in words.

## Platform limitations (confirm current numbers against docs)

| Limitation | Workaround |
|---|---|
| Connected boards | Support docs (Sep 2026): up to 20 at a time. Internal packaging: 5 by default, 20 on Vibe Growth or Custom/Enterprise. Plan for 5 unless the account is confirmed; move app-internal data to Vibe DB |
| Complex conditional logic | Break into simpler rules, iterate |
| External APIs | **API Requests integration** (`+` → Integrations → API Requests): API-token auth only (no OAuth), GET/POST/PUT, token stored securely and never in app code, 1 credit per call (each page counts). Email via the Gmail/Outlook integration |
| No background jobs | Apps run only while someone has them open; board-triggered work belongs in monday automations |
| Data migration | CSV/XLSX import (5,000 rows, new board), or export/import with careful field alignment |
| Very large or app-internal data | **Vibe DB**: ~10 GB / ~1M items, 256 KB per record, no images, no automations; left-pane apps created from ~26 Aug 2026; no draft/live split (draft testing writes real data) |
| Permissions | Board permissions are the floor — the app can't elevate them. Viewer seats can't open vibe apps. Public apps (Growth, admin toggle) have no per-user access control |
| Credits | Every build prompt charges, depending on complexity and the chosen model; in-app AI actions ~8 credits per run; failed prompts still charge |
| Formula complexity | Simple calculations, rely on rollups |

## After delivering the prompt

Tell the user: paste it into the vibe builder chat, then refine with follow-ups in
that chat ("add more spacing", "use the accent color for CTAs", "add a status
column"). If they're unsure what vibe is: it's monday's built-in app builder — you
describe what you want and it builds a working app in your workspace, no code.

Standing preferences (brand colors, logo, "always ask before big changes") can go in
**Vibe Memory** — Settings → Memory, or "Remember…" in chat — instead of every prompt.
Memory holds instructions, not data.
