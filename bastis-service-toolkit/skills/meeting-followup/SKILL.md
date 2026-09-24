---
name: meeting-followup
description: "Drafts and saves a post-meeting follow-up email to Gmail drafts using the monday.com AI notetaker summary, with automatic fallback to Gong email summaries (from do-not-reply@gong.io) if notetaker notes are absent. Trigger this skill whenever the user mentions an external meeting has ended, a notetaker summary is available, they want to send a follow-up, or says anything like \"follow up on that meeting\", \"draft a follow-up\", \"meeting just ended\", \"notetaker summary is in\", or \"write a follow-up email\". Also trigger proactively if the user pastes or references a meeting summary and hasn't yet sent a follow-up."
---

# Meeting Follow-Up Email Skill

Turns a monday.com AI notetaker meeting summary into a warm, professional follow-up email saved as a Gmail draft — ready for the sender to review and send.

> **Configure the sender once:** replace `[your-monday-email]` with your monday.com
> address and `[Your name]` with your name (or set these in user preferences) so
> the draft is addressed and signed correctly.

---

## Workflow

### Step 1 — Fetch the meeting summary

**Primary source: monday.com notetaker**

Call `monday.com:get_notetaker_meetings` with:
```
limit: 5
include_summary: true
include_action_items: true
include_topics: true
access: OWN
```

- If the user named a specific meeting, use `search` to find it
- Otherwise, present the most recent 1–3 meetings and ask which one to use
- Confirm before proceeding if it's ambiguous
- Note the meeting **title** and **start_time** — you'll need these to find the calendar event in Step 2

**Fallback: Gong email summary (if notetaker notes are absent)**

If the matched meeting has no summary content (empty or missing `summary`, `action_items`, and `topics`), or if no notetaker meeting is found at all:

1. Cross-reference Google Calendar first (Step 2) to confirm a meeting took place
2. If a calendar event is confirmed, search Gmail for a Gong summary email:
   - Call `Gmail:search_threads` with query: `from:do-not-reply@gong.io` + meeting title keywords or date
   - Target: most recent matching email at or after the meeting's `start_time`
   - Extract: call summary, key topics, action items, and any recording link (Gong links are in the format `https://app.gong.io/call?id=...`)
3. Use the Gong email content as the meeting summary source — treat it the same as notetaker output for Steps 3–5
4. Add a note in Step 6 confirmation: `📧 Summary sourced from Gong email (no notetaker notes found)`

If neither notetaker notes nor a Gong email are found:
- Tell the user both sources were checked and returned nothing
- Ask them to paste the summary manually or confirm whether notes exist elsewhere

### Step 2 — Cross-reference Google Calendar for full invite list

Call `GoogleCalendar:list_events` (or equivalent) with:
```
timeMin: [meeting start_time - 15 minutes, ISO 8601]
timeMax: [meeting start_time + 2 hours, ISO 8601]
singleEvents: true
orderBy: startTime
```

Match the calendar event to the notetaker meeting by title and time. From the matched event, extract:
- `attendees[]` — full list of all invited people, including those who did not join
- Each attendee has: `email`, `displayName` (if present), `responseStatus` (`accepted`, `declined`, `tentative`, `needsAction`)

If the Calendar tool is unavailable or returns no match:
- Skip this step
- Add the following line at the top of the draft body, directly under the greeting: `[CHECK: Google Calendar unavailable — could not verify full invite list. Please add any no-shows to CC manually before sending.]`
- Continue with notetaker participants only

### Step 3 — Build the full recipient list

Cross-reference the notetaker participants (who actually joined) against the calendar attendees (everyone invited):

| Role | Gmail field | Logic |
|---|---|---|
| Client attendees who **joined** (non-@monday.com) | `to` | Non-@monday.com emails in notetaker participants list |
| Client invitees who **did not join** (non-@monday.com) | `cc` | In calendar attendees but not in notetaker participants, and non-@monday.com |
| monday.com CSM / AM / team (joined or invited) | `cc` | All @monday.com emails from both sources, excluding [your-monday-email] |
| the sender ([your-monday-email]) | exclude | This is the sender |
| Calendar resource emails (e.g. `@resource.calendar.google.com`) | exclude | These are room/resource bookings, not people |

**Gmail API constraint:** `to` cannot be empty. If no external client emails are found, use `[your-monday-email]` as a placeholder and note it clearly.

### Step 4 — Write the email

**Tone:** Warm and friendly — confident, direct, no fluff. monday.com brand voice. Active voice. No filler openers ("Hope this finds you well", "Just wanted to..."), no jargon.

**Subject line format:** `Follow up | [Client] <> Monday.com | [Date DD Month YYYY]`
- Example: `Follow up | VM02 TCX <> Monday.com | 28 April 2026`

**Structure — match this format exactly:**

```
Hi [first name(s) of To recipients],

[One warm, direct opener sentence]

**Key Topics**
- [Decision — past tense: "Aligned on...", "Confirmed that...", "Agreed to..."]
- [repeat for all meaningful decisions; 3–8 bullets typical]

**Action Items**
1. **[Owner first name]:** [Action — specific and actionable]
2. **[Owner]:** [Action]
[number list formatting each; bold owner; include all owners including the sender]

** Recording:**[gong link]

**Next Session**
Our next session will be [Date and time if known, or "TBC".], where we will cover ...

Kind regards,
[Your name]
```

**Section headers:** Bold, no colons — `**Key Decisions**`, `**Action Items**`, `**Next Session**`

**Opener by meeting type:**
- Post-kickoff: "Thank you again for your time today."
- Regular stand-up: "Here are my notes from today's session."
- Longer/strategic: "Thanks for your time today — here are the key points from our meeting and next steps."

**Sign-off:** `Kind regards,
[Your name]` only — no "Best regards"

### Step 5 — Save to Gmail drafts

Call `Gmail:create_draft` with:
- `subject`: formatted subject line
- `body`: plain text version
- `htmlBody`: lightly formatted HTML (bold section headers, clean numbered/bullet lists, no heavy styling)
- `to`: client attendees who joined (non-@monday.com)
- `cc`: client no-shows (non-@monday.com, invited but didn't join) + all @monday.com team excluding the sender

### Step 6 — Confirm to the user

Reply with:
- ✅ Draft saved to Gmail
- Subject line
- **To:** [list names]
- **CC:** [list names, noting any flagged as no-shows]
- Any `[CHECK]` flags — missing recipients, calendar match failure, ambiguous roles
- Brief preview of action items pulled in

---

## Edge Cases

| Situation | Behaviour |
|---|---|
| No meetings found | Check Gmail for Gong summary email; if also not found, tell the user both sources were checked and ask them to paste the summary manually |
| Notetaker meeting found but no notes | Check Gmail for Gong summary from do-not-reply@gong.io; use Gong content if found, flag source in Step 6 |
| Multiple recent meetings | List them, ask which one |
| No action items in summary | Omit that section; don't invent actions |
| Meeting is internal only | Note it looks internal, confirm with the sender before proceeding |
| Calendar event not found | Skip Step 2, flag `[CHECK: add any no-shows manually]`, proceed with notetaker participants only |
| Client name is sensitive/confidential | If the client must not be named, use "our recent session" or ask the sender what to write |
| All participants are @monday.com | Treat as internal, confirm before drafting external-style follow-up |

---

## Notes

- Never send the email — only save to drafts
- Never commit to timelines or deliverables not in the notetaker summary
- If the summary is sparse, produce a shorter email — don't pad
- Always flag anything inferred or uncertain with `[CHECK]`