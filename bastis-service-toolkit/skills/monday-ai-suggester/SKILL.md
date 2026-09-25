---
name: monday-ai-suggester
description: Suggests how monday.com AI features (Agents, Sidekick, Vibe, AI-powered automations) could solve a specific client's workflow problems. Use this skill whenever the consultant says "AI ideas", "AI use cases", "AI suggestions", "how can AI help here", "map AI to this", "AI angle on this case", or any variation about applying monday AI to a client situation. Also auto-trigger when the consultant runs monday-discovery AND mentions "we'll use AI for this case" (or similar) — append AI suggestions to the discovery output. Always pulls live AI release info from Slack, the monday AI tracking boards, and the ICs Product Updates board before suggesting, so recommendations reflect the latest features. Default to LIGHT depth (just the idea + which feature) — go deeper only when she asks.
---

# monday-ai-suggester

Take a client's situation (call transcript, discovery map, or summary of what they want) and suggest how monday.com's AI features could solve their problems.

The whole point of this skill: **the platform is shifting hard toward AI and the consultant is moving into AI implementation work**. Suggestions need to reflect what's actually shipping right now, not what was around 6 months ago. So the skill always pulls fresh data before suggesting.

## Step 1: Get the client context

the consultant will provide one of:
- **Pasted transcript or summary** — work with what she gave you.
- **Discovery map output** — chained from `monday-discovery`, just take the previous output as input.
- **Reference to a Notetaker meeting** — fetch it with `get_meetings_content(ids: [uuid], include_summary: true, include_topics: true)` on the monday.monday connector (same flow as `monday-discovery`); find ids with `explore_meetings(query, access: ALL)`.

If the input is unclear or she just said "AI ideas" without context, ask which client/call she means. Don't guess.

## Step 2: Pull current AI feature knowledge — never skip this

The platform's AI surface area changes weekly. Stale knowledge means stale suggestions, and the consultant will catch it.

Before the live pull, skim `references/changelog.md` — a dated log of confirmed releases fed automatically by `weekly-pulse` each week. It's a quick baseline, not a substitute for the pull below — weekly-pulse only catches what it caught, and this skill needs the full current picture.

### From Slack

The full channel list lives in `references/slack-channels.md` — read that file first, then follow its instructions. It's a shared reference used by both this skill and `monday-discovery`, so when channels change, only one file needs updating.

**For this skill specifically (AI feature research):**
- **Tier 1 (AI feature channels)** — read recent messages in full via `Slack:slack_read_channel` (limit 100, last 30 days)
- **Tier 2 & 3 (product + IC/team channels)** — search via `Slack:slack_search_public_and_private` with AI keywords scoped per channel: `Sidekick OR Agent OR Vibe OR "Magic AI" OR MCP OR Notetaker` and `in:#channel-name`

Run all channel queries in parallel — don't serialize, it's slow.

**What to look for:**
- Feature announcements and releases (often have 🎉, "now live", "shipping", "GA", "beta")
- New capabilities (Sidekick, Agents, Vibe, Magic AI, Notetaker, Kremer)
- Plan tier info
- Known limitations or gotchas other consultants flagged
- Use cases other consultants built — gold for inspiration

Skip user troubleshooting threads unless they reveal a new feature or limitation.

If a channel returns an error or has nothing relevant, note it in "Sources pulled" and move on. Don't block the whole run on one bad channel.

### From monday boards
These three boards track AI releases. Pull recent items from each via `monday.com:get_board_items_page`. If the column structure isn't familiar, run `monday.com:get_board_info` first to understand what's there.

- Board ID **8084368131** (view 173755196) — primary AI release tracker
- Board ID **183946105**
- Board ID **9970212055**
- Board ID **18411697232** ("Product Updates", workspace 15557960) — the newer, IC-curated release log used by `weekly-pulse`. Filter to `dropdown_mm32k9yh` (AI Type) set for AI-only items, or pull broadly if the client situation touches non-AI features too.

For each item, capture: feature name, status (in dev / beta / GA), description, target audience or plan tier.

### If pulls fail
If a Slack search or board fetch returns nothing or errors, note it in the output's "Sources pulled" line and proceed with what you have. Better to give the consultant 80% of the picture than block on a missing source.

## Step 3: Cross-reference client situation with AI capabilities

For each pain point or workflow in the client context, ask: **"Which current monday AI feature could touch this?"**

Don't force matches. If a pain point doesn't map cleanly to anything AI does well today, say so honestly. the consultant would rather hear "AI doesn't fit here yet, flag for later" than a stretched suggestion that wastes a client's time.

The four buckets to consider:
- **Agents** — autonomous task-doers triggered by board events, schedules, or other agents. Good for: routing, triage, multi-step workflows that used to need a human.
- **Sidekick** — in-context AI helper inside boards/items. Good for: drafting updates, summarizing threads, suggesting next steps, answering questions about board data.
- **Vibe** — AI-driven generation of boards, apps, or workflows from natural language. Good for: rapid prototyping, getting clients started without a heavy build.
- **AI in automations / formulas** — AI-powered building blocks inside existing automation recipes. Good for: classification, sentiment, summarization, extraction inside flows the client already has.

(Confirm and update these descriptions from the live Slack/board pull — features evolve.)

## Step 4: Produce the output — Option D structure

Always use this exact structure. the consultant asked for all three angles in one doc.

```
# AI suggestions — [client name or "this case"]

**Sources pulled:** Slack channels (last 30d): [list which channels actually returned data]. Boards: 8084368131 / 183946105 / 9970212055 / 18411697232 ([date]). [Note any channel or board that failed or was empty.]

## Flat list
- **[Suggestion 1]** — [Agent | Sidekick | Vibe | Automation+AI]
- **[Suggestion 2]** — [tag]
- ...

## By client pain point
**[Pain point 1 from the call]**
- AI angle: [which feature, one-line idea]

**[Pain point 2]**
- AI angle: ...

[If a pain point has no fit: "AI doesn't have a clean angle here yet — flag for later."]

## By AI feature
**Agents**
- [Where this client's workflow could use one]

**Sidekick**
- [Where Sidekick fits]

**Vibe**
- [Where Vibe fits, or "no clear fit yet"]

**AI in automations**
- [Where AI-powered automation blocks fit]
```

## Step 5: Depth — light by default, deeper on request

**Light (default):** One-line ideas. Just the suggestion + which feature.

**Medium (when she asks "go deeper" / "what would this look like"):** Add which boards/columns/automation recipes the build would need.

**Heavy (when she asks for a build plan):** Rough plan another consultant could pick up — board structure, column types, automation triggers, agent prompts if relevant.

Don't pre-emptively go deep. She'll ask.

## Chaining with monday-discovery

If the consultant ran `monday-discovery` in the same conversation **and** said something like "we'll use AI for this case", "let's add AI ideas", "AI angle on this", or similar — automatically run this skill against the discovery map output. Append the AI suggestions section to the existing discovery doc; don't replace it.

If she didn't signal AI, don't chain. Discovery-mapper standalone is the default.

## Style — match the consultant's preferences

- Simple literal English. No corporate fluff ("circle back", "synergy", "leverage", "unlock value", etc.).
- Bold for emphasis, bullets and clear headers for scannability.
- If a Slack/board pull returned nothing useful for a topic, say so plainly: "Couldn't find recent updates on [X], working from baseline knowledge."
- Never invent features. If unsure whether a capability exists, flag it: "Worth checking — I think there's a Sidekick option for this but couldn't confirm in today's pull."
- If a pain point genuinely doesn't fit any AI feature, say so: "AI doesn't have a clean angle here yet."
- Numbers and units stay as plain text — no LaTeX.
