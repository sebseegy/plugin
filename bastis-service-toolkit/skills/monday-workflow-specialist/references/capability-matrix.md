# Capability matrix - Workflow Builder blocks

Source: `invoke_process_planner` block catalog, read-only, 2026-10-23 (grade A for existence, IDs, kind). "Use" column is an IC angle, grade D unless stated. Re-run the planner probe to refresh: ask it to "list every block you know exists, grouped by category, and say explicitly when a block does not exist".

Kinds: trigger, wait-trigger (mid-flow wait), action, condition, search.

## Triggers from outside monday
| Block | ID | Notes |
|---|---|---|
| When a webhook is received | 22970502 | Body arrives as one JSON string (B). Emits payload itself; no separate "Get webhook data" action (A). |
| When email received (Gmail / Outlook) | 17449803 / 18044240 | |
| Teams: message received in channel | 18241079 | |
| Slack: message received / group mentioned | 20441455 / 20441456 | |
| Salesforce: object created or updated | 11703601 | |
| Jira (+DC): issue created / created or updated | 17978201 / 17978202 / 11857651 / 12181641 | |
| GitLab merge request events | 11018280, 11018682, 11018733, 11018751, 11018867 | on-prem variants exist |
| SharePoint: list item updated | 124799975 | |
| Google Calendar: event created | 18398156 | |
| SuperForm submitted | 12094438 | |
| Notetaker meeting ended | 11840114 | |
| Sequences / Campaigns events | see planner | CRM-side |
| AI Sales Agent call events, Harmony call ends | 14199018, 18611968, 125653275, 126884209 ... | |
| Manual trigger (run now) | 23620468 | Test before publish; callable from chat/MCP (B). |

## Read data
| Block | ID | Notes |
|---|---|---|
| Get item data | 10380144 | |
| Get all items | 121568574 | Multi-condition filters (B). Field report: filter fields saving as null (D). |
| Find item by column value | 11855018 (search) / 10572006 | Name-column behaviour: returns an ID even with no match (D). Guard. |
| Find connected item / subitem | 11994142 / 11994143 | Board and connect column fixed in UI (C). Not usable for N differing boards. |
| Get all connected items | 22245590 | |
| Get all subitems / matching subitems | 17788542 / 122353390 | |
| Get latest update / all item's updates | 12164525 / 15544443 | |
| Get all boards / groups / members | 23766247 / 24019284 / 24178399 | |
| Search emails / Find email | Gmail 16536043, 16536042; Outlook 17589630, 17589631 | |
| Salesforce Search objects / Get object data | 18962152 / 11703603 | Field reports of instability (D). |
| Google Drive search / get file content | 23953458 / 23953456 | |
| OneDrive search / find / get content | 123859840 / 125913507 / 123859841 | |
| SharePoint find doc / get content | 123860076 / 124799967 | |
| Slack search messages / thread | 20441451 / 20441452 | |
| Teams search chat/channel | 18241077 / 18241078 | |

## Transform and compute
| Block | ID | Use |
|---|---|---|
| Code (Python) | 23557427 | Anything native cannot do; monday API + MCP only. |
| JSON Parser (JSONata) | 20264061 | Candidate for splitting the webhook body without Code. Untested on webhook body (C). |
| Concat two strings / Text Appender | 120809043 / 120807736 | |
| Extract item link from text | 10973055 | |
| Convert Text To Date / Number | 11572720 / 11572649 | |
| Set/Declare variable | does not exist (A) | Pass values as outputs of earlier steps or compute in Code. |

## AI blocks
Categorize with AI 124966296; Text summarizer 11105348; Text translator 11081174; Text improver 11081594; Information extractor 11120548; Search the web 14724015; Content writer 10984696; Sentiment analyzer 11081194; Custom prompt 10984657; Call Sidekick 12164606; Smart condition 13698140; AI Agent 14717877; Trigger an agent 12399524; Trigger Sphera agent 15829835; Trigger Agentic Cycle 122256675. Credits: see `monday-workflow-architect/references/limits-and-failure-modes.md`.

## External calls
| Block | ID | Notes |
|---|---|---|
| HTTP request and API call | 15947681 | GET/POST/PUT; Credentials-app token via `{{token}}`; public URLs only (B). |
| Run any MCP action (core) | 22629575 | |
| Run any monday action (MCP) | 126424196 | |
| Run any GitHub / Slack / Google Drive / HubSpot / QuickBooks / Confluence / Canva / Dropbox action (MCP) | 121687315 / 121623798 / 126314877 / 122038413 / 122175285 / 121886346 / 122898916 / 121873659 | |

## Write / create
Create board 10528550; Duplicate board 10528536; Create from template 11614493; Move item to board 11545995; Create Doc 11983431; Add content to Doc 11983454; Jira create/update issue 17978213 / 17978214; Slack notify channel/users/reply/react 11407937 / 11407939 / 20441449 / 20441450; Salesforce create/update object 11703610 / 11703612; Drive create folder/upload/share/delete 13820247 / 13820246 / 13820251 / 13820253; SharePoint upload/create folder/move/copy/list item/start approval 124799968-124799974.
Do not exist (A): create workspace, create/move board folder, move board, duplicate/move doc, DocuSign, Set variable. For these, use Code (monday API) - see cookbook - and check the schema first.

## Human in the loop and waits
Wait until button clicked 10512879; Wait until status changes 10512352; Wait until column changes 10512205; Wait until update created 10869390; Wait for duration 10380177; Send email and wait for response Gmail 123941304 / Outlook 124356611 (recipient need not have a monday account; timeout path, B); Teams notify with button 15988054 (companion wait 15988055 is root-trigger only, A).

## Gaps that push you to Code or HTTP
1. Create/move workspaces and folders.
2. Teams (user groups) create and membership.
3. Per-event dynamic target board.
4. Parsing nested JSON, arrays, math across items.
5. Non-monday HTTP verbs (DELETE, PATCH not offered, B).
6. Read-modify-write guards (undo an edit, notify editor).
