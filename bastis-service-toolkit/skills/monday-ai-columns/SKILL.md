---
name: monday-ai-columns
description: >
  Runs a structured interview with the consultant and produces an optimized configuration for monday.com AI columns and AI-powered automation actions — including AI summarize, AI classify, AI extract, AI generate, and AI-powered formula columns. Use this skill whenever the consultant says "AI column", "AI formula", "magic column", "set up an AI column", "AI automation action", "help me configure the AI column", or any variation of wanting to add AI-powered column logic or automation steps. Also trigger when the consultant describes a use case involving text classification, sentiment detection, field extraction, auto-summarization, or AI-generated content inside a board. If the consultant has an existing AI column prompt she wants improved, use this skill to critique and rewrite it. Always use this skill rather than configuring AI columns freehand.
---

# monday-ai-columns

the consultant configures AI columns and AI automation actions for enterprise clients. This skill produces precise, working configurations through a structured interview.

There are three entry modes:

**Mode A — Interview from scratch**: the consultant wants to add an AI column or AI automation action. Run the interview.
**Mode B — Review & rewrite**: the consultant pastes an existing AI column prompt or automation config. Skip to the Critique section.
**Mode C — Context-aware suggestion**: the consultant is already working on a client project. Use context to suggest which AI column types fit and where.

---

## Monday AI column types — know these before interviewing

| Type | What it does | Best for |
|---|---|---|
| **AI Summarize** | Summarizes text from one or more columns | Long update threads, notes, descriptions |
| **AI Classify** | Assigns a category/label from a predefined list | Request type, priority, sentiment, department routing |
| **AI Extract** | Pulls specific data out of unstructured text | Names, dates, action items, key details from emails |
| **AI Generate** | Creates new text based on column data | Drafting replies, generating descriptions, creating summaries |
| **AI Formula** | Applies custom AI logic with a natural-language instruction | Anything that doesn't fit the above — open-ended AI reasoning |
| **AI in automations** | AI action block inside an automation recipe | Classify on trigger, generate on status change, extract on form submit |

---

## Mode A: Interview

Run ONE question at a time. Ask one follow-up if vague. Skip anything already answered.

**If working on a client project**, pre-fill from existing context and only ask what's missing.

### Interview questions (in order):

1. **The data**: What text or content does this AI column need to work with? Where does that text come from — a form submission, manual updates, another column, an email?

2. **The job**: What should the AI do with that text? (Summarize it? Pull something specific out of it? Classify it into a category? Write something new based on it?)

3. **The output**: What should the result look like? A short label? A sentence? A paragraph? A specific format?

4. **For classify/extract**: What are the categories or fields you want extracted? Be specific — list them. (For classify: what are all the possible labels? For extract: what specific information should it pull out?)

5. **Source columns**: Which column(s) should the AI read from? Are there multiple columns it should combine?

6. **Trigger**: Should this run automatically (when an item is created, when a column changes) or manually when a user clicks?

7. **Edge cases**: What should the AI do if the text is empty, too short, or doesn't contain the information it's looking for?

---

## Writing the AI Column Configuration

Produce a complete, ready-to-configure specification. Be precise — vague AI column prompts produce inconsistent results.

```
## AI Column: [Column name]

**Type:** [Summarize / Classify / Extract / Generate / Formula / Automation action]

**Reads from:** [Column name(s)]

**Instruction prompt:**
[The exact text to enter in the AI column prompt field — specific, clear, under 150 words]

**Expected output:** [What the result should look like — label, sentence, list, etc.]

**Trigger:** [Automatic on [event] / Manual]

**Edge case handling:** [What to output if input is empty or unclear]
```

### Instruction prompt writing rules

These rules apply to the instruction prompt inside the AI column config:

- **Start with the action**: "Summarize...", "Classify...", "Extract...", "Write..."
- **Be specific about format**: "Return only the category label, nothing else." / "Write 2–3 sentences." / "Return a comma-separated list."
- **For classify**: Always list every possible category. "Classify as one of: Bug, Feature Request, Question, Feedback. Return only the label."
- **For extract**: Name every field to extract. "Extract the following from the text: 1. Requester name, 2. Due date, 3. Budget. If a field is missing, return 'Not specified'."
- **Keep it under 150 words** — longer prompts don't improve accuracy and slow processing
- **No ambiguity in the output format** — if it could return two different formats, it will

---

## Mode B: Critique & Rewrite

Evaluate against these failure modes:

| Problem | Signs |
|---|---|
| **Vague action** | "Analyze this text" — analyze how? return what? |
| **No output format specified** | Returns different formats each time |
| **Missing category list** | Classify prompt without listing all options — AI invents categories |
| **Over-long prompt** | >150 words with padding that doesn't add precision |
| **No edge case handling** | Empty cells cause errors or weird outputs |
| **Wrong column type** | Using AI Formula when AI Classify would be cleaner and faster |
| **Ambiguous source** | Doesn't specify which column(s) to read |

Give the consultant a **2–3 line diagnosis**, then rewrite using the format above.

---

## Mode C: Context-Aware Suggestion

**AI columns are a strong fit when:**
- Users are copy-pasting information between fields manually
- A board has long text fields that people rarely read fully
- Classification or routing is done manually based on reading item content
- Form submissions contain unstructured text that needs to be parsed into structured fields
- Items need a drafted response or description based on their data

**AI columns are NOT the right call when:**
- The logic is deterministic (use a regular formula or automation instead)
- The data is already structured (no need for AI to extract what's already in a column)
- The output needs to be 100% consistent and auditable (AI has variance)

Make a **specific recommendation**:
> "For [client]'s [board], an AI Classify column on [source column] would automatically route [type of items] into [categories] instead of someone doing it manually. Want me to write the prompt?"

---

## Anti-patterns to avoid

- Never write "use your judgment" in an AI column prompt — it produces inconsistent output
- Never skip listing categories for a classify column — the AI will invent its own
- Never combine extract + summarize + classify in one column — split into separate columns
- Never forget the output format instruction — it's the most commonly missed thing
- Never use AI columns for data that changes frequently in real time — results won't auto-refresh
