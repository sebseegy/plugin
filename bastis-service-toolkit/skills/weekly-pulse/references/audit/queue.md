# Open questions for owners (newest first)

Rule: an item leaves this queue only when a grade A/B source answers it. Ask via Slack (Basti sends; the audit never posts).

## Seeded 2026-10-19
1. **C004 vs C005 - do failed Vibe prompts charge credits?** Support docs are silent (checked 2026-10-19). Patch proposed to say "not documented". Still ask Amichay Even Chen for the real behaviour, or test one failed run and read the credit display.
2. **C003 - viewer read-only access for Growth, "~end Oct 2026"?** No support doc mentions it. Expires 31 Oct. Ask Amichay Even Chen, else drop the claim (patch P2).
3. **C023 - SharePoint/OneDrive for agents: released or in progress?** Board item says Released, source Release Board card (13210452165) says in progress. Ask Vera Metzner / check the card status.
4. **C028 - Org Agent Directory Enterprise Phase 2 (5 Oct): landed?** Check #ai-agents-product-updates owner post.
5. **C033 - Vibe multiple editors (promised 1-2 weeks on 31 Aug): shipped?**
6. **C026 - Sidekick multi-Gmail send bug: fixed?** (flagged 24 Sep)
7. **C008 - public fullstack apps 403 on server writes: fixed?** (flagged 24 Sep)
8. **C034/C035 - limits.md dated 2026-06-02, sourced from a Guru card.** Re-verify "moves" items against current monday-all/support content.
9. **C022 - Agent Phone: which countries after IL/US?**

## Build-run notes 2026-10-19
- Could not verify any claim in the build run: `web_fetch` refuses URLs not supplied in a user message (give it the verbatim support URLs once, or run the audit with WebSearch), and `read_docs` for Vibe FAQ doc 18397954182 rejected the `ids` argument via this connection. First scheduled run must establish baseline snapshots and retry these.
- All 37 ledger rows start `unverified` on purpose; nothing has been promoted to `verified`.

## Added 2026-10-19 (verification pass)
10. **C007 - boards per Vibe app: 5 or 20?** Support "Get started" (28451758349842) says 5; best-practices (34101891654034) reportedly says 20 (modified 2026-09-22); Guru CX article says both. Need article modified dates or owner answer (Amichay Even Chen).
11. **C032 - Vibe external APIs:** support "FAQs and Troubleshooting" (32833743243282) still says "not yet"; board/Slack say released Aug 2026. Is the support article stale? Need its modified date.
12. **C039 - new:** agents can manage Vibe apps (support 37230283024530). Decide whether monday-agents / vibe-builder should mention it (patch P4).
13. **Method gap:** monday knowledge tools hide article modified dates, so support text can never reach "fresh" status without a pasted URL for web_fetch. Paste the Vibe support URLs from sources.md into chat once so the scheduled run's first fetch is allowed.

## Added 2026-10-26 (weekly run)
14. **Vibe daily API limit: still 25k on Enterprise?** Board (20 Oct, SwissAI briefing, grade C) says Vibe API calls are excluded from the account daily API limit. Contradicts `monday-vibe-builder/references/data-layer.md` line 25. Owner: Vibe team (#ask-vibe-ai). Need an A/B source; do not patch data-layer.md until then.
15. **Entity Retrieval sub-agent: Beta 25% or GA?** Board (25 Oct) says Beta/limited; #ai-agents-product-updates (20 Oct) says GA. Owner: Kangan Malik / agents team.
16. **Standalone Brains: account 5 only or GA?** Board status "Released" vs text "available on account 5". Owner: agents team.
17. **Self-serve credit numbers** (wire 20,000 min net-30; card 500 min; 1.5x; expiry) come from a Slack session (grade D). Need the pricing/support page before quoting to clients.
18. **Proposed patch (not applied):** `monday-workflow-architect/references/limits-and-failure-modes.md` line ~131 says AI credit consumption isn't visible per-workflow; board says per-block visibility released. Needs B source (support article) first.
