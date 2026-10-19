# Source registry and grading

| Grade | Meaning | Can change SKILL.md body? | Examples |
|---|---|---|---|
| A | Machine or live truth | Yes | GraphQL schema introspection; monday MCP tool lists/params; behaviour observed in a sandbox account |
| B | Owner announcement or official docs | Yes | Post by the shipping team in #ai-agents-product-updates / #cco-enablement-updates; CCO Knowledge Updates board (9970212055); support.monday.com article (with modified date); 2026 Release Board card status |
| C | Human-curated digest | No (index + changelog line only) | ICs Product Updates board 18411697232 (workspace 15557960); weekly shipping summaries |
| D | Q&A / chat | No (changelog line, marked unverified) | #ask-vibe-ai, #ask-ai-agents answers (many are bot-written), #ai-workflow-group chatter |

Reversing a stated limitation needs two independent A/B sources.

## Primary sources to snapshot or query
- GraphQL schema: `get_graphql_schema`, `get_type_details` (monday MCP). Save a normalized JSON; diff vs `.prev`.
- MCP tool catalog: list of tool names + parameter names for the monday MCP (diff = real capability change, e.g. new vibe_* / workflow tools).
- Support articles (fetch text, record modified date): Vibe best practices (support.monday.com/hc/en-us/articles/34101891654034); agents builder / Agent Factory; Workflow Builder; Sidekick; AI credits.
- Internal docs: Vibe FAQ (monday.monday.com/docs/18397954182); Vibe packaging SOT (monday.monday.com/docs/18411930424).
- Boards: 2026 Release Board 8084368131 (read the card's own status); R&D Captain's Log 183946105; CCO Knowledge Updates 9970212055; ICs Product Updates 18411697232 (index only).
- Slack owner posts: #ai-agents-product-updates (C0AR4A570F8), #cco-enablement-updates, #ask-vibe-ai (C094ZQJJ8GH) - only messages authored by owners, not Q&A replies.
- Demand side: Gong/Notetaker transcripts (pull-gong-transcripts) for real client questions.

## Named owners (DRIs) seen in sources - ask via queue.md
- Vibe: Amichay Even Chen (#ask-vibe-ai).
- Agents releases: Tsemach Lifshitz (#ai-agents-product-updates); Ran Eldan, Yonatan Chocron (#ask-ai-agents).
- Workflows: Eyal Mutzary, Amir Matalon (#ai-workflow-group).
- ICs Product Updates board: Vera Metzner (board owner).

## Environment notes
- The Product Updates board is visible on only one of the connected monday MCP servers; try the other if "not found".
- #monday-platform-notifications is often only empty bot (sphera) posts.
- Many #ask-* answers are bot-written: grade D even if they cite a source - follow the cited source.

## Confirmed support articles (found 2026-10-19 via monday.monday knowledge tools)
- Get started with monday vibe - support.monday.com/hc/en-us/articles/28451758349842 (viewers; boards per app = 5)
- monday vibe: best practices, features, and capabilities - .../34101891654034 (5,000-row import; check board-limit text)
- monday vibe: Permissions and Pricing - .../32833842348178 (credit ranges)
- monday vibe: FAQs and Troubleshooting - .../32833743243282 (external APIs 'not yet' - likely stale)
- Make your Vibe app public - .../37168858812306
- monday vibe: manage apps and data with agents - .../37230283024530
- AI Credits - .../29544502265746 ; AI Models and Credits - .../36207944364434
- Bring your external agent into monday.com - .../36885999990930
- monday-all Guru CX article 'monday vibe' - mondayall.com/knowledge/JQ4e5Y83a8hPFb43MFwR (updated 2026-07-21; internally inconsistent, grade C)
- monday.monday docs: monday vibe FAQ 2026 = 18397954182; duplicate 18432534567; old FAQ 18009241402 and 18396978637; Vibe Feature Requests 18427764053; Vibe packaging 'aligned to the current 5 limit' 18407550717; monetization overview 18394321826

## Tool recipes that work (and traps)
- monday.monday knowledge Q&A: `get_monday_knowledge(kind="general", query=...)` on the monday MCP that can see board 18411697232. Returns an AI answer + snippets with support URLs. Retrieved answers are generated from snippets: always read the snippets, not just the answer. It does NOT expose article modified dates, so freshness stays unproven (grade stays B at most, mark 'date unknown').
- Doc search: `search(searchType="DOCUMENTS", searchTerm=...)` returns doc ids + highlights.
- `read_docs` rejected its `ids` argument in this connection (array arrives as string) - use search highlights or the other monday MCP.
- AI Brain retriever (bigbrain): `agentic-retriever(question=..., messages=[])` - needs BOTH fields. Index is mostly workplace/office content; no Vibe FAQ found.
- monday-all: `knowledge_search` finds Guru-migrated cards; `knowledge_get_article` can return 70k chars - save-to-file then grep with `-o` and a bounded regex.
- `web_fetch` only works on URLs the user pastes in chat or that came from a prior search/fetch result.
