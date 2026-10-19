# Proposed patches for monday-vibe-builder/SKILL.md (awaiting approval; NOT applied)
Evidence date 2026-10-19.

## P1 - Credit estimate (~L148) [C005, C041]
Old: `Failed prompts are free; stopped prompts are charged up to the stop.`
New: `Failed prompts: not documented - verify via the credit display on a real failed run; stopped prompts are charged up to the stop (unverified, Slack only).`
Evidence: B - no support article states "failed prompts are free". Model ranges (Flash 10-20, Sonnet 30-50, Opus 50-500) match support 32833842348178 - keep.

## P2 - Access model (~L106) [C002, C003]
Old: `Viewers cannot open Vibe apps at all today (read-only for Growth expected ~end Oct 2026, unconfirmed).`
New: `Viewers cannot open Vibe apps that display board information (support 28451758349842). A planned read-only viewer option is not documented in support; treat as unconfirmed.` (Claim expires 2026-10-31 anyway.)

## P3 - Public apps (~L100) [C014, C038]
Add: `Public apps need the Growth package, the board owner to publish, and the admin permission "Publish Vibe apps to the public web" (off by default; only ENT admins can enable). Board views and dashboard widgets are not supported; only apps created after the permission was enabled.`
Evidence: B - support 37168858812306.

## P4 - Agents can manage Vibe apps [C039] - NEW capability to mention in Phase 0/handover
`monday agents and external agents can read Vibe app data, create/update/delete items, ask read-only questions and manage publications (all plans).` Evidence: B - support 37230283024530.

## Do NOT change yet
- Board limit text "5 on 10-app, 20 on Growth" (C007): unresolved conflict between support articles; internal packaging SOT supports the current wording.
