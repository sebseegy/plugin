# Vibe platform facts (verified 2026-09-24)

Status legend: **GA** full release · **GR** gradual release · **RM** roadmap · **BUG**
open bug · **?** unconfirmed. Re-verify anything client-facing that's >3 weeks old.
Primary sources: #ask-vibe-ai (C094ZQJJ8GH), #vibe-mcp (C0B4W9FR9KM), monday.monday
Vibe FAQ (https://monday.monday.com/docs/18397954182), 2026 Release Board
(8084368131), support.monday.com Vibe articles (updated Sep 2026).

## Contents
1. MCP capabilities · 2. Surfaces/variants · 3. Packages & tiers · 4. Credits ·
5. Access model · 6. Public & password · 7. Governance · 8. Capabilities status ·
9. Hard "not supported" list · 10. Known contradictions

## 1. MCP capabilities
- GA for all customers since ~2026-07-05. Tools: `vibe_create`, `vibe_update`,
  `vibe_get`, `vibe_ask`, `vibe_publication`, `vibe_list`, `vibe_delete`,
  `vibe_rename` (new 2026-09-23).
- Prompt proxy only: no code access, no view of the rendered app. Same credit cost
  as prompting in the UI.
- Not exposed as tools (yet): connect/disconnect boards (MCP backlog 2026-09-22),
  Vibe DB toggle, tools menu (Gmail/Outlook/export…), Plan mode, Memory, public
  link/password settings, auto-update toggle, duplicate, ownership transfer.
  Workaround: request Vibe DB / tools in the prompt text ("use Vibe DB to store…",
  "send the email via Outlook").
- Board-limit violations surface only as an error at call time.
- Model enum: `GEMINI_3_7_FLASH | CLAUDE_5_SONNET | CLAUDE_OPUS_5`; omit for
  auto-select. Model param needs model selection enabled on the account. The model
  choice governs the builder orchestrator only; runtime AI inside the app uses
  Vibe's internal model (BYOM via API integration if a stronger runtime model is
  needed).
- Deferred-tool discovery quirk: vague searches can miss the Vibe tools — select by
  exact name.

## 2. Surfaces / variants
| Variant | Surface | Boards | Public / password / Vibe DB / API server fns |
|---|---|---|---|
| `object_fullstack` | Left-pane full-page app, workspace-hosted, TanStack + server functions | multi (5 / 20) | Yes (new apps only) |
| `object` | Left-pane app; maps to fullstack on accounts with server generation (since 2026-07-19) | multi | Only if it resolved to fullstack |
| `board_view` | Board view tab | single host | No |
| `vibe_item_view` / `item_view` | Item page view/widget | single | No — difference between the two undocumented |
| `vibe_dashboard_widget` | Widget in a board's dashboard view (not full dashboards) | single; needs `view_id` | No; billing counts 1 app regardless of widget count |
| `monday_campaigns` | Campaigns surface, Campaigns SDK | ? | Experimental; Vibe not included with Campaigns — build costs credits, publish needs add-on |

- Only left-pane apps can: connect/disconnect boards post-build, go public, become
  public templates, be set as account homepage or mobile experience.
- Cannot convert an app between surfaces. Workaround to show a left-pane app on an
  item/dashboard: "Embed everything" widget (shows same data on every item; doesn't
  auto-bind to dashboard boards).
- Eligibility cutoffs for new capabilities are per-feature and by creation date
  (public: apps created since ~Aug; Vibe DB: since ~Aug 26; password: since Sep).
  Rule: create fresh as `object_fullstack` today.
- Portfolio boards: connecting reads only data mirrored onto the portfolio board,
  not its project boards (whole-portfolio connect RM, no ETA). Resource
  Planner/Capacity Manager data is not readable.

## 3. Packages & tiers (Vibe add-on = publishing)
| Bucket | Price/mo | Boards/app | Public apps + password | Notes |
|---|---|---|---|---|
| 10 apps ("Starter") | $100 | 5 | No (business decision) | Not available to Enterprise 50+ seats |
| 25 apps ("Growth") | $250 | 20 | Yes | Viewer read-only access coming here first |
| 50 / 100 / 250 / 500 | $500 / $1k / $2.5k / $5k | 20 | Yes | Same features as Growth |
- Board limit cannot be raised (higher limits in dev, no ETA, maybe not this year).
- Quota counts **published** apps only (internal or public). Drafts free of quota;
  unpublish/delete frees a slot. Duplicates/template copies count once published.
- Free-app promo ended 2026-06-18 (no-touch) / contracts after 2026-07-31 (touch);
  existing free slots removed at renewal. Don't promise free apps.
- Trials: 7 days (no-touch) / 14 days (touch); unlock publishing only, no credits;
  apps revert to draft when trial ends. AM/CSM can extend +7d in BigBrain → Admin tab
  → Extend vibe trial.
- Vibe discounts forbidden; AI credit discounts CRO-approval only.
- Demo accounts: ask in #ask-vibe-ai to be upgraded to Growth (20 boards).

## 4. Credits (AI credits = building + runtime AI; $0.01/credit list)
| Action | Credits |
|---|---|
| Build prompt — Gemini Flash | ~10–20 |
| Build prompt — Claude Sonnet (default) | ~30–50 |
| Build prompt — Claude Opus | ~50–500 (FAQ says up to 1,000+) |
| Plan mode | "a bit more" than a plain build prompt, often fewer prompts overall |
| Runtime AI action (summarize, translate, web search, chatbot answer) | 8 per call |
| File/PDF/image extraction | 8 per file |
| Integration trigger (email, calendar) | 1 |
| API request | 1 per call — each page of a paginated response counts |
| Image generation (runtime) | <10 per image |
| Viewing app, board reads/writes, exports | Free |
- **Failed prompts — disputed:** the pricing SOT says failed/error prompts are free;
  production builds (Wren, WHSmith, Aug–Sep 2026) saw credits consumed on failed
  runs and retries. Budget as if they're charged. Stop charges up to the stop point.
- Observed per prompt in real builds: ~35 small targeted fix · 141–221 scoped change ·
  417–454 large multi-part prompt. One customer burned ~4,000 credits fighting an
  authorization bug — escalate platform issues early instead of re-prompting.
- Apps keep working at 0 credits unless they use runtime AI.
- Medium app ≈ 2,000 build credits (Amichay, 2026-09-09) — wide variance.
- Demo accounts and monday.monday don't meter credits → can't measure POC cost there.
- No runtime credit cap per app (backlog). Admin → AI governance → Credit Usage /
  Usage Limits (account/feature/user) and Vibe apps tab show build vs runtime spend.
- Per-seat credit model (MIDAS) rolling out from 2026-09-24 to no-touch non-ENT
  accounts; consumption rates unchanged.

## 5. Access model
- Apps run with the **viewing user's** permissions. Board/item/column access in
  monday = access in Vibe. Exception: public apps (no user) and apps using an API
  token integration (token's permissions, not the user's).
- Drafts: owner (and editors) only.
- **Members**: full use with board access.
- **Guests**: "anything except building" — must be invited to the app AND every
  connected board. Guests: desktop yes; mobile guest access was reported not to work
  (Aug) — verify before promising.
- **Viewers**: cannot open Vibe apps (technical limitation). RM: read-only viewer
  access, Growth only, ~end Oct 2026 (ETAs have shifted repeatedly).
- Same-domain users can't be made guests to avoid seats (by design).
- Mobile: apps run in the monday mobile app; admins can set a Vibe app as a user
  group's mobile home (Admin → Mobile apps → Create mobile experience). No offline
  mode. Building on the desktop app not supported (browser/mobile web OK).

Options for large non-licensed populations (e.g. 700+ staff logging time):
| Option | Identity | Cost | Caveat |
|---|---|---|---|
| Members | Yes | Highest | Cleanest |
| Guests | Yes | Guest seats | Invite to app + all boards |
| Public app (+password) | None | Growth pkg | No "current user"; write bug (below) |
| "External Users for Vibe" (invite by email, magic link, 7-day session) | Yes | Per-user price TBD (internal proposals ~$5/user/mo or buckets — never quote) | RM — tech design v0.6 (2026-09-16); internal ETA "1–2 months" in #vibe-external-users-payment; ships only after all apps are on Cloudflare WFP; V1 no read-only/row scoping |
| WorkForms for intake + internal Vibe app for staff | Form = none; app = members | Free forms | Proven pattern when outsiders only need to *submit* (incl. file upload) — sidesteps public-write bug and data exposure |
| monday code | Custom | Rebuild | Out of Vibe |

Guest seats are for external-domain users; putting employees on personal emails
as guests to dodge seats is a licensing issue — don't propose it.

## 6. Public apps & password
- GA (Jul 2026). Growth+ only, left-pane fullstack only, new apps only.
- Enterprise admin permission "Publish Vibe apps to the public web" is off by default;
  admins can unpublish any public app. Only the app's board owner can publish public.
- "Anyone with the link", no login/SSO, embeddable externally. No per-user
  permissions, no row-level control. Connected boards get a public indicator.
- Password protection GA/GR (Sep 2026): one shared password, 15-min sessions, apps
  created in Sep+ only; multiple passwords = duplicate app per password.
- monday.monday blocks public apps → demo from monday-demo-eu1/us1 with public data
  only.
- **BUG (open 2026-09-24):** public fullstack apps fail ALL server-side writes
  (`create_item`, `create_subitem`, `change_multiple_column_values`) with 403
  USER_UNAUTHORIZED since ~2026-09-20; reads fine. Don't promise public write-back.
- **BUG:** "incorrect password" on correct password (2026-09-11, DoW open).
- No IP allow-listing or domain restriction for public apps (account IP restrictions
  don't apply). If a client needs one, public is the wrong model.
- Open security question (Aug 2026, unanswered): whether build-time external
  libraries (npm fonts, chart libs) are sandboxed from app data. Name it as an open
  risk on any public app with sensitive data.
- Building your own login for public apps (OTP/token pattern, Wren portal):
  `../../vibe-board-builder/references/platform-facts.md` → "Building your own
  authentication". It depends on public writes, so it's blocked while the 403 bug is open.
- RM: per-user login for public apps (end of year, extra cost), custom domain (no
  ETA), SSO for non-monday users (further out), "Powered by monday vibe" watermark.

## 7. Governance (Enterprise)
- Permissions: "Create/edit Vibe apps", "Publish Vibe apps to the account",
  "Generate public Vibe templates", "Publish Vibe apps to the public web". Default:
  admins create+publish, members create only. Pro and below: everyone can build and
  publish.
- **Request to publish** (2026-09-22, GR): when publish permission is off, builder
  requests → admin approves in Admin → AI governance → Vibe apps → Pending approval.
  One request per app per day. Pre-feature workaround: add an admin as collaborator.
- Collaborative building GA 2026-09-13: Editors prompt/publish/add editors;
  Collaborators review only; Owner alone can unpublish/delete/transfer. Unpublished
  apps allow only 1 editor; unpublishing removes all collaborators.
- Admins can list/delete/transfer/unpublish any app but can't open a draft without
  transferring it to themselves.
- AI features must be enabled (Admin → Customization → Features / AI governance).
- External agents via MCP need the account permission for external AI access.

## 8. Capability status
| Capability | Status | Date |
|---|---|---|
| Connect up to 20 boards (Growth) | GA | 2026-06-08 |
| Add / disconnect boards on existing app | GA | 2026-06-15 / 07-15 |
| CSV/XLSX import → new board (≤5,000 rows) | GA | 2026-06-15 |
| Multi-level subitems (read/create/update, 3rd–4th level) | GA | 2026-07-21 |
| Element selection / chat attachments (img 3.5MB, video 50MB, PDF 5MB, 5 files) | GA | 2026-07-01 |
| Vibe MCP (external agents) | GA | 2026-07-05/21 |
| Stop auto-publish / manual update | GA | 2026-03 / 07-21 |
| Public apps + share link | GA | 2026-07-28/30 |
| Tools menu (Gmail, Outlook, GCal, exports, QR, AI text, PDF/image analysis, web search, Notetaker, CRM emails, Campaigns, Resource Mgmt) | GA/GR | 2026-08-20 |
| Sketch your app / Board editing subagent / Duplicate + replace boards | GA | 2026-08-24 |
| Plan mode / Memory (app, user, account) / API Requests + BYOM | GA | 2026-08-30 |
| Vibe DB | GA | 2026-09-13 |
| Password protection / Multi-editor | GA (GR rollout) | 2026-09-13 |
| Stop button | GA | 2026-09-18 |
| Runtime AI image generation | GR 100% | 2026-09-14 |
| Request to publish (ENT) | GR | 2026-09-22 |
| Viewer read-only (Growth) | RM | ~end Oct 2026 |
| 50 boards/app, OAuth for API Requests, scheduled jobs, pre-deploy QA agent, faster API, external user seats, direct code edit | RM | — |

## 9. Not supported (don't design around these)
- Background/scheduled jobs — nothing runs unless the app is open (email "sync"
  loops included). Use board automations triggered by Vibe writes.
- Creating automation recipes.
- OAuth APIs (API-key auth only; GET/POST/PUT). Anyone who opens the app sees what
  the key can access.
- Direct code editing / code export / pushing code (paste snippets into chat).
- Rollup columns; formulas depending on mirrors; Capacity Manager data; filtering by
  mirror column in API.
- File storage in Vibe DB (use file columns or external storage via API).
- Bulk email (works for "a dozen", not thousands; app must stay open; no
  attachments reported).
- Offline mode.
- Starting a fresh chat on the same app (long chats lag → duplicate, or consolidate
  into one prompt for a new app).
- Restoring deleted apps.

## 10. Known contradictions (state the uncertainty)
- Opus credit range 50–500 vs 50–1,000+.
- Viewer access ETA: "no ETA" → "end of year" → "end of Oct" / "couple of weeks".
- Legacy grandfathering (pre-May 6 purchasers exempt from build credits) ended
  2026-08-10 per the pricing SOT; older Slack/FAQ answers still claim it — don't
  tell clients building is free.
- Public FAQ (Aug 16) still says 5 boards, no duplicate, no external APIs, owner-only
  editing — all superseded.
- Vibe DB quota: marketed 10 GB, code enforces 1 GiB.
- Public write-back: "can in some cases" (Jul) vs open 403 bug (Sep).
