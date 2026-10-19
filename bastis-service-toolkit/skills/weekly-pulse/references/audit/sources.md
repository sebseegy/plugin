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
