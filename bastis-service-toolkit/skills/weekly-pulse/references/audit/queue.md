# Open questions for owners (newest first)

Rule: an item leaves this queue only when a grade A/B source answers it. Ask via Slack (Basti sends; the audit never posts).

## Seeded 2026-10-19
1. **C004 vs C005 - do failed Vibe prompts charge credits?** Two skills say opposite things. Check Vibe FAQ credits section; else ask Amichay Even Chen.
2. **C003 - viewer read-only access for Growth, "~end Oct 2026"?** Expires 31 Oct. Shipped, slipped, or drop the claim? Ask Amichay Even Chen.
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
