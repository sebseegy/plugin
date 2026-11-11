# monday-workflow-specialist - changelog

Newest first. Fed by weekly-pulse for advanced-block changes (webhook, Code, HTTP, MCP, JSON, loops, manual trigger).
For general Workflow Builder / Automations releases outside advanced blocks (tiers, limits, native triggers/conditions, AI blocks, build sequence) see `monday-workflow-architect/references/changelog.md` - the two changelogs together are the full release feed; claims for both skills share one ledger at `weekly-pulse/references/audit/claims.csv`.

## 2026-11-11 - Step 1b intake gate, Code block fact corrections, #ai-workflows-product-updates sweep
- Added "Step 1b - Code intake" gate (12-question checklist) before any Code block is written.
- Corrected input auto-naming claim (was `code_output_<field>`, now `<field label>_<step number>`, fallback `input_1` for non-Latin labels, B - ledger #23) in SKILL.md and code-block-cookbook.md.
- Added real platform caps not previously recorded: 30 inputs / 30 outputs per Code block, 20,000-line editor cap, no secrets storage, no state between runs (B, uploaded Code Block guide - ledger #22, #24).
- Added psutil/ipython to the preinstalled-package list (ledger #25); added a known-working `create_item` mutation pattern to the cookbook (ledger #27).
- Corrected an implied Loop iteration cap: the Loop block has none, the 500-item cap applies only to "Get all..." blocks (B, 3 Nov - ledger #28, C062).
- Added "Run any monday action" MCP block (126424196) full-release detail (ledger #29, C063), "Run step" single-step testing (ledger #30, C064), subitem-level trigger/wait parity (ledger #31, C065), and HTTP domain allowlisting as an unverified, account-limited claim (ledger #32, C066).
- Fixed a weekly-pulse pipeline gap: this skill was missing from weekly-pulse's own changelog auto-update list, so future findings will land here automatically.

## 2026-10-23 - skill created
- Webhook body now delivered to workflows (6 Oct), Code block egress and auth clarified, HTTP Credentials-app auth documented, 4 KB truncation incident (13-14 Oct, fixed), planner catalog snapshot. Details: evidence-ledger.md.

## 2026-10-23 - DaPulse source pass (read-only)
- Code block: runtime, limits and egress confirmed from source (A). Webhook: delivery semantics, reactivation fix (24 Sep), 12 h pending URL TTL. Block not retried. Evidence ledger items 11, 18-21.

## 2026-10-23 - handover-first design stance
- Added "Design stance: built to be handed over": durability ranking (native > native+AI/parse > Code > MCP/OAuth > HTTP+token), token rule, N-simple-workflows vs 1-clever-webhook trade-off, runbook and ownership requirements.
