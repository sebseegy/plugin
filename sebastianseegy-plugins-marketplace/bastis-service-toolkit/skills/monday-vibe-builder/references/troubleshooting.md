# Vibe troubleshooting (verified 2026-09-24)

## Triage order
1. `vibe_get` (status + `messages` limit 10) — is it busy, errored, or did Vibe ask
   a question / report an auto-fix?
2. `vibe_ask` — "What is failing and why? What query/filter logic do you use?"
3. Compare with board data via the monday MCP.
4. One targeted `vibe_update` on Opus. Two failures → revert (UI undo on last good
   prompt, ask IC) and change approach.
5. Escalate: DoW ticket https://wkf.ms/48FOfah with app editor URL, account ID,
   screenshot, the prompt. Check #ask-vibe-ai and #vibe-ai-notifications for an
   active incident first.

## MCP-level errors
| Symptom | Meaning / action |
|---|---|
| `SERVER_GENERATION_DISABLED` 403 on `vibe_create` | Account lacks fullstack. Explain lost capabilities; retry `object` only with approval |
| `APP_BUSY` 409 on `vibe_update` | Still generating. Poll `vibe_get` until `is_busy=false` |
| Board limit error at create | >5 (or >20 on Growth) boards. Reduce boards or confirm package |
| Publish fails | Not deployed yet, quota full, or user lacks publish permission (Enterprise → request-to-publish / admin collaborator) |
| Vibe tools missing from MCP | Transient (seen 2026-09-16); select tools by exact name; reconnect connector |
| Long prompt fails on create | Split (one page per prompt) |
| Status stuck >10 min / deploy error | Stop polling; report; check incident channels (2026-09-09 TLS incident broke all deploys ~2h; retry/rollback failed too) |
| App landed in `<userId>-vibes` workspace | `workspace_id` omitted — move app to the boards' workspace (UI) |

## App behaviour
| Symptom | Likely cause | Fix |
|---|---|---|
| Items/subitems missing | 500-item stop, permissions ("only view assigned items"), viewer seats, query logic | `vibe_ask` for query logic; "don't stop after 500, paginate"; check permissions; rebuild page |
| Works only for the builder | Hard-coded user ID, or others lack board access, or viewers | Opus: "remove hard-coded user IDs, use current user"; check seats/board access |
| Breaks after columns reordered | Columns referenced by position | "Reference columns by ID" |
| Slow / slow page switching | Too many items/columns, no cache | Performance prompts (playbook §6); Vibe DB |
| Users redirected to a deleted board | Deleted connected board | Disconnect it (UI Boards header) |
| "Failed to generate app" (board/item view) | User lacks permission to create board views, or AI disabled | Fix permissions at account/workspace/board |
| Live full-page app stale vs preview | Deploy/caching bug | DoW ticket |
| Public app writes 403 USER_UNAUTHORIZED | Open bug since ~2026-09-20 | Don't rely on public writes; members/guests path |
| Password "incorrect" when correct | Open bug | DoW |
| CORS between cdn and `_serverFn` | Browser calling server fns directly | Revert; "don't call _serverFn from the browser directly" |
| `Board is not a constructor` runtime error | Seen on early MCP builds | Opus fix prompt; rebuild if persistent |
| AI list output shows `[object Object]` | Bullet formatting | "Force markdown '-' bullets in AI responses" |
| Builder stuck loading / Stop greyed | Platform issue (fixed 2026-09-24 instance) | Wait/refresh; revert; DoW |
| Draft data vs live data differ (Vibe DB) | Separate DBs by design | Seed live / migration |
| Guest can't see app | Not invited to app AND every board; or on mobile | Invite to both; verify on desktop |
| Linter error in `src/generated` | Code gen error | Paste the error text into a `vibe_update` |
