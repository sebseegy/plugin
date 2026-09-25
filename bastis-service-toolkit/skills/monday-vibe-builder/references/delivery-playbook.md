# Vibe delivery playbook for ICs (verified 2026-09-24)

## Before you build on a client account
- Loop in the AM/CSM — AI pricing and legal may already be in negotiation.
- Check: AI features enabled; Vibe add-on bucket (10 vs 25+) and published-app
  headroom; AI credit balance; Enterprise Vibe permissions (who can create/publish,
  public web toggle).
- **Internal AI Build exemption** — build without burning client credits:
  BigBrain → Subscription Management → Credit Usage → Add Exemption. Account scope
  (user search was buggy), 6 hours, renewable. Account must still have credits;
  needs CSM-level BigBrain permissions. Docs:
  https://mondayall.com/knowledge/4PpBcGA4lR3flh2S7SZ9
- Trial: extend +7 days in BigBrain → Admin tab → Extend vibe trial. Trial apps
  revert to draft when it ends.

## Scoping & effort (MS Flex Menu roundtable, 2026-08-31)
- Menu item "Vibe Implementation" = 6 points (24 exec + 6 D&S hrs). ICs consider it
  too low as a single price point.
- Observed: 2–3 h simple dashboard-substitute · ~30–60 h resource-management app ·
  35 h typical single app · 100–200 h enterprise app. Rule of thumb ≈ 2× the
  equivalent native build.
- Time sinks: data validation, endless UI feedback loops, re-renders collapsing
  earlier work. Lock requirements and screens up front; cap feedback rounds in SOW.
- Where clients only use the Vibe app (never the boards), sell the Vibe item, not a
  Build item. Hand off via `monday-scoping`.

## Environment pattern (dev → prod)
1. Build on sandbox/mock boards in a demo or the client's sandbox workspace.
2. Keep the dev app as a draft (free of quota); publish prod only.
3. After first publish, turn Auto Update off so builder edits don't hit live users.
4. Go-live: swap to live boards (Boards header) or Duplicate → connect to new
   boards. Cross-account: public template link (no boards carried; Enterprise needs
   "Generate public Vibe templates").
5. Vibe DB: whether draft and live share data is disputed — test on the account.

## Demos
- monday.monday can't host public apps and doesn't meter credits — use
  vibe-demo-account / monday-demo-eu1/us1 (request Growth upgrade in #ask-vibe-ai).
- Demo Mode pattern (Jim's play): toggle that writes only to demo columns + "Reset
  demo outputs" button.
- Amichay's advice for client enthusiasm: don't explain Vibe, send the link /
  webinar https://www.youtube.com/watch?v=XeuHr8HmA7E.

## Handover
- Build record (app ID, editor link, variant, boards, access model, prompt log,
  limitations, credit estimate) → project `deliverables/`.
- Transfer ownership to the client owner (UI V menu or admin panel) or add client
  Editors (multi-editor GA). Only Owner can unpublish/delete/transfer.
- Client-facing docs via `monday-build-docs`. Name the upcoming changes that affect
  them (viewer access, per-user public login) as roadmap, not promises.
- Growth upsell triggers to flag to the AM: >5 boards, public/external users,
  password portals, viewer access need.

## Escalation & expertise
- #ask-vibe-ai (C094ZQJJ8GH) — product Qs; #vibe-mcp (C0B4W9FR9KM) — MCP;
  #vibe-ai-notifications — rollouts/incidents; #vibe-data-performance — scale;
  #monday-vibe-examples — templates; #ask-ai-pricing — CPQ/pricing.
- DoW bug form https://wkf.ms/48FOfah (non-R&D: note you're from Delivery).
- Amichay offers a single 30-min session for complex builds; otherwise tickets.
