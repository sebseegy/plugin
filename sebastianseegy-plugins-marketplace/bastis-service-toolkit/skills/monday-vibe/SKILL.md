---
name: monday-vibe
description: "Design and prompt monday vibe apps — monday.com's AI-powered no-code app builder at monday.com/vibe. Use whenever the user wants to build an app on monday vibe, mentions 'monday vibe', asks to create a custom app or view inside monday.com, wants to turn a workflow into an app, says 'vibe coding' or 'generate a vibe prompt', or describes a work problem and is a monday user (they may not know vibe exists). Interviews the user, then outputs a ready-to-paste vibe prompt. monday vibe changes fast and the team accumulates internal know-how, so this skill ALWAYS checks current vibe docs on support.monday.com AND searches Slack for internal recommendations before advising — never from memory alone. This is NOT the Vibe Design System (React) or the monday apps developer MCP. If the monday MCP Vibe tools are connected and Claude should build the app itself, use monday-vibe-builder instead."
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
2. **Slack for internal recommendations.** Search for working prompt patterns,
   gotchas, performance tricks, things to avoid (terms: "vibe", "monday vibe",
   "vibe app", plus the app domain). Prefer recent messages and people who own/use
   vibe. Cite the threads you relied on.

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

A single clean prompt to paste into the vibe builder chat. Start with "Build me an
app that…". Specific, concrete, under ~350 words, plain language, name existing
boards explicitly, omit empty sections. Save to plain `.txt` if saving to file
(minimal formatting — no `===`/`---`/`***` separators).

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
- **Server-side calculations** — read pre-calculated values, not client-side compute.
- **Paginate large data** — 50–100 item pages; show initial results fast.
- **Cache large boards** (1,000+ items) in browser local storage for instant reloads.
- **Selective "entry-first" loading** — only load data the user is looking at.
- **Timezone safety** — treat dates as noon local time, not midnight, to avoid
  day-shift from UTC conversion.
- **Theme tokens** — use semantic `bg`/`border`/`fg`, not `white`/`gray-800`, so
  light/dark modes work.
- **Optimistic updates** — update UI immediately, confirm save in background.

## Prompt engineering

vibe responds best to simple clear instructions, **one change at a time** (verify
before continuing), and small steps with checkpoints — don't pack multiple big
changes into one prompt. Structure a prompt around: persona/role, core function,
data entities, workflows (when X → do Y), UI preferences, permissions.

Avoid assuming deep branching logic or complex formulas, that project boards
already exist, or over-engineering the first iteration — get core working, then
refine.

## Platform limitations (confirm current numbers against docs)

| Limitation | Workaround |
|---|---|
| ~5 connected boards max | First 5: "Add connected board". Beyond: query via monday API |
| Complex conditional logic | Break into simpler rules, iterate |
| External integrations | Configure via monday integrations separately |
| Data migration | Export/import with careful field alignment |
| Very large datasets | Design for archiving, efficient schema |
| Formula complexity | Simple calculations, rely on rollups |

## After delivering the prompt

Tell the user: paste it into the vibe builder chat, then refine with follow-ups in
that chat ("add more spacing", "use the accent color for CTAs", "add a status
column"). If they're unsure what vibe is: it's monday's built-in app builder — you
describe what you want and it builds a working app in your workspace, no code.
