# Proposed patches for monday-vibe/SKILL.md (awaiting approval; NOT applied)
Evidence date 2026-10-19. Grades per sources.md.

## P1 - Credits row (SKILL.md ~L161) [claims C004, C006, C041]
Old: `Every build prompt charges, depending on complexity and the chosen model; in-app AI actions ~8 credits per run; failed prompts still charge`
New: `Every build prompt consumes credits by model (Flash 10-20, Sonnet 30-50, Opus 50-500; cost shown at the end of each run). In-app file extraction costs 8 credits per file. Whether failed prompts charge is not documented - check the credit display after a failed run before telling a client.`
Evidence: B - support 32833842348178 (ranges, display); C - Guru CX article (8 credits per file extraction). Absence of failed-prompt statement confirmed in 2 support articles.

## P2 - Permissions row (~L160) [C002]
Old: `Viewer seats can't open vibe apps.`
New: `Viewer seats can't open vibe apps that display board information (even with board access); members and guests can, with access to the connected boards.`
Evidence: B - support 28451758349842.

## P3 - Import row (~L158) [C011] - no change needed (verified, B).

## Do NOT change yet
- Board limit (C007): two B sources disagree (5 vs 20). Resolve via article modified dates or owner first.
- External APIs (C032): a support article still says "not yet"; owner posts/board say released. Resolve before touching text.
