---
name: monday-discovery
description: "Map a customer's current workflows, tools, team structure, pain points, and goals from a call transcript — producing a written discovery summary AND a visual process map. Use whenever the user says 'map this call', 'discovery map', 'analyze this meeting', 'what did we learn from this call', 'pull the notetaker', 'create a discovery summary', or references a discovery/kickoff/first call with a client. Pulls the transcript from monday Notetaker via MCP unless text is pasted. Also use for 'build ideas', 'how would I build this in monday', 'map out the build' — see the build-ideas step. The discovery-synthesis task delegates per-call mapping to this skill, then aggregates across calls."
---

# monday Discovery Mapper

Turn a call transcript into a full discovery map — written summary + visual — so
the consultant walks into the next meeting with total clarity. This is the
per-call craft skill; the **discovery-synthesis** task delegates
the single-transcript mapping method here, then aggregates across calls.

## Step 1 — Get the transcript

If asked to pull from monday Notetaker: use `@monday-mcp-ui:get_notetaker_meetings`
to list recent meetings (filter by client/date if named, else list recent and ask
which). Use `access: ALL` to catch calls run by other consultants. Then fetch the
selected meeting's content. **Avoid `include_action_items: true` on the transcript
fetch — it can crash the response on `due_date`; pull summary/topics, and get
action items separately if needed.** If text is pasted, use it as-is.

## Step 2 — Analyze the transcript

Extract the following; flag what's unclear rather than guessing:

- **Company & context** — name, industry, size; who was on the call (names+roles);
  what prompted them to look at monday now.
- **Current tools & systems** — every tool/platform, what each is for, integrations
  (or lack of), manual workarounds/spreadsheets relied on.
- **Team structure** — teams/departments; who does what today; decision-makers;
  day-to-day users of a new system.
- **Pain points & bottlenecks** — what's broken/slow/frustrating; where things fall
  through the cracks; what they've already tried and why it didn't work.
- **Goals & desired outcomes** — short and long term; what "success" looks like;
  KPIs/metrics they care about.
- **Open questions & gaps** — mentioned-but-unclear; contradictions; missing info;
  assumptions to confirm.
- **What to ask next** — specific follow-ups for the next call/email, ordered by
  priority, in a warm casual voice.

## Step 3 — Write the discovery summary

Structure with the sections above. Warm, practical tone (for the consultant, not
the client). Bold key names/tools/terms; bullets for lists; ⚠️ to flag anything
unclear/assumed; ✅ for confirmed. Never invent details — if it wasn't in the
transcript, say so and flag it as a gap.

## Step 4 — Build the visual map

Pick the format from what the transcript reveals, and render it inline with
`visualize:show_widget` (SVG or interactive HTML):
- Clear step-by-step process → **flowchart** (sequence, who does each step, handoffs)
- Scattered / no clear process → **mind map** (company center → Teams / Tools /
  Processes / Pain Points / Goals)
- Multiple distinct workflows → **swimlane** (one lane per team/department)

Color-code: 🔵 current tools/systems, 🟠 pain points, 🟢 goals/desired state,
🔴 gaps/unclear.

## Step 5 — End with the "Ask Next" list

Always close with **📬 What to follow up on** — 3–7 specific questions in the
consultant's casual voice, e.g. "Can you walk me through what happens when a new
request comes in — who gets it first?"

## Step 6 — Build ideas / build map (only if asked)

Triggers: "give me ideas on how to build this", "how would I build this in monday",
"map out the build", "build map for [client]". When triggered:

- Read `../monday-ai-suggester/references/slack-channels.md` first (shared channel
  source of truth) and follow its "general build inspiration" mode. If that file is
  missing, say so and fall back to baseline monday knowledge.
- For each major thing the client wants, suggest a concrete build approach: which
  boards, column types, automations, integrations. For deeper structure, hand to
  **`monday-solution-architecture`**.
- Where AI features genuinely fit (Sidekick / Agents / Vibe / AI columns /
  Notetaker), name them with a one-line "why this fits" — or hand the whole AI angle
  to **`monday-ai-suggester`** for a live feature-mapped pass.
- Cite real inspiration only if actually found in the channels — never fabricate.
- Match depth to the ask: light by default, deeper on request.

## Tone & style

Warm, casual, no corporate jargon — written as if for the consultant themselves.
Flag uncertainty honestly. Never invent details or consultants.
