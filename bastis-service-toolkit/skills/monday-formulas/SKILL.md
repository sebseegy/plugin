---
name: monday-formulas
description: "Write, fix, and explain monday.com Formula column formulas using only officially supported functions. Use whenever the user mentions a monday formula — writing a new one, fixing an invalid-formula error, checking if a column contains text, comparing dropdown/label values, handling blanks, asking why a formula returns nothing, or how to calculate something inside a board (even without the word 'formula'). Also triggers on FormulaLanguage, SEARCH, IF, AND, OR, SUBSTITUTE, LEN, SWITCH in a monday context. Uses only the official monday function library — no Excel/Sheets functions, no math symbols for arithmetic. Always use this skill rather than writing monday formulas freehand."
---

# monday.com Formulas

Write, fix, and explain monday.com Formula column formulas using **only officially
supported functions**. Read `references/functions.md` before writing anything — it
is the complete verified function library with syntax rules and ready patterns.
Never invent a function that isn't in that file.

Three modes:
- **Mode A — Build from scratch:** the user describes a calculation. Ask clarifying
  questions, then write it.
- **Mode B — Fix:** the user pastes a broken formula. Diagnose and correct it.
- **Mode C — Explain:** the user wants to understand a formula or function.

---

## CRITICAL RULES — read before writing any formula

Non-negotiable. Every formula follows all of them.

1. **NEVER use math symbols for operations.** `+`, `-`, `*`, `/` are never used for
   arithmetic in monday formulas. Use the function: addition → `SUM(a,b)`,
   subtraction → `MINUS(a,b)`, multiplication → `MULTIPLY(a,b)`, division →
   `DIVIDE(a,b)`. (`>`, `<`, `=`, `>=`, `<=` ARE allowed inside conditions.)
2. **NEVER invent functions.** If it isn't in `references/functions.md`, it doesn't
   exist in monday. Never use: `VLOOKUP`, `SUMIF`, `COUNTIF`, `INDEX`, `MATCH`,
   `IFERROR`, `ISBLANK`, `DATEDIF`, `NETWORKDAYS`, `EDATE`, `EOMONTH`, `COUNTA`,
   `SUMPRODUCT`, `INDIRECT`, `OFFSET`, array formulas, regex.
3. **Column names in curly braces, exactly as they appear** — `{Column Name}`,
   case-sensitive, by **display name** not API column id.
4. **Text and status labels in double straight quotes** — never smart quotes.
5. **Decimals need a leading zero** — `MULTIPLY({Revenue},0.25)` not `.25`.
6. **Every open parenthesis must close.** Count them.
7. **No cross-board / cross-row reads.** Formulas operate on the current item only;
   no VLOOKUP equivalent. Use mirror columns or linked board columns instead.
8. **`TEXT()`/`FORMAT_DATE()` output is text, not a number.** Wrapping a result in
   them makes the column summary show N/A — use for display only, never when the
   value feeds a further calculation.

---

## Referencing columns

| Column type | Syntax | Notes |
|---|---|---|
| Any column | `{Column Name}` | Case-sensitive, exact match |
| Label / Dropdown | `{Column Name#Labels}` | Returns the selected label as text |
| Status | `{Column Name#Labels}` | Same pattern |
| People | `{Column Name#DisplayValue}` | Returns name as text |
| Date | `{Column Name}` | Returns ISO date string |
| Numbers / Formula | `{Column Name}` | Numeric / computed value |

**Without `#Labels`, a label/dropdown column returns an internal ID, not the
visible text.** Always use `#Labels` when comparing against text like `"OT"`.
When you pull column structure via the API, use the `title` field, not the `id`,
for formula references.

---

## The "Contains" pattern (IFERROR-free)

`IFERROR` doesn't exist and `SEARCH` throws an error when text isn't found. Use
`LEN + SUBSTITUTE` to safely test if one string contains another:

```
LEN({Column}) - LEN(SUBSTITUTE({Column}, "search term", "")) > 0
```

`SUBSTITUTE` removes all occurrences; if the result is shorter, the term was
present.

Example — flag if a text column contains a fixed word:
```
IF(LEN({Notes}) - LEN(SUBSTITUTE({Notes}, "urgent", "")) > 0, "🔴 Urgent", "")
```

Example — check if PSP Group contains the Channel value, only for OT/TT:
```
IF(
  AND(
    OR({Channel#Labels}="OT", {Channel#Labels}="TT"),
    LEN({PSP Group}) - LEN(SUBSTITUTE({PSP Group}, {Channel#Labels}, "")) > 0
  ),
  "✅",
  "❌"
)
```

## Guarding blanks

```
IF({Column} = "", "", <your formula here>)
```
For numeric columns that might be blank/zero:
```
IF({Number Column} = 0, "", DIVIDE({Number Column}, {Other Column}))
```

## Common patterns

Label equals one of several values:
```
IF(OR({Status#Labels}="Done", {Status#Labels}="Approved"), "Complete", "Pending")
```
Nested IF (prefer SWITCH at 3+ values):
```
IF({Priority#Labels}="High","🔴",IF({Priority#Labels}="Medium","🟡",IF({Priority#Labels}="Low","🟢","")))
```
Concatenate:
```
CONCATENATE("Owner: ", {Assignee#DisplayValue}, " | Due: ", {Due Date})
```
Case-insensitive compare (comparisons are case-sensitive by default):
```
IF(LOWER({Channel#Labels}) = "ot", "✅", "❌")
```
Range check:
```
IF(AND({Score} >= 80, {Score} <= 100), "Pass", "Fail")
```

---

## Mode A — Build from scratch

Ask these (skip what's answered):
1. What do you want to calculate or show? (number? label? date? flag?)
2. Which columns does it read from? (exact names and types)
3. Any conditions? (only if status X; only when date is past; different results per value)
4. What should it show when data is missing or the condition isn't met?

Then write it, show it in a code block, explain each part in plain language, flag
assumptions about column names, and note limitations (e.g. "TEXT() wraps the output
so the column summary shows N/A").

## Mode B — Fix a broken formula

| Check | What to look for |
|---|---|
| Math symbols | `+ - * /` for arithmetic → SUM/MINUS/MULTIPLY/DIVIDE |
| Unsupported functions | Anything not in `references/functions.md` |
| Missing curly braces | Column names without `{}` |
| Smart quotes | Curly `"` instead of straight `"` — must retype in builder |
| Missing leading zero | `.25` instead of `0.25` |
| Unmatched parentheses | Count opens vs closes |
| Wrong column type | Mirror/Tags and other unsupported types |
| Case mismatch | Status label doesn't exactly match the board |
| TEXT() on a number used elsewhere | Output treated as text breaks downstream |

Give a 2-line diagnosis, the corrected formula in a code block, and what changed.

## Mode C — Explain

Plain language, no jargon; show a simple example with made-up column names; break a
complex pasted formula down from the inside out; flag gotchas.

---

## Gotchas to proactively flag

- **DAYS(end, start)** / **WORKDAYS(end, start)** — end date is the FIRST argument;
  reversing gives a negative.
- **HOURS_DIFF** compares Hour column values, not Date columns.
- **SEARCH()/FIND()** return a position number and **error when not found** — for a
  true/false result, use the LEN+SUBSTITUTE pattern instead. (SEARCH is
  case-insensitive, FIND is case-sensitive.)
- **IF nesting** maxes out around ~5 levels before unreadable/length limits — use
  **SWITCH** for multi-value status logic.
- **Status labels are case-sensitive** — `"done"` ≠ `"Done"`.
- **No vertical aggregation** — can't sum a whole column or reference other rows.
- **Mirror columns aren't supported** in formulas — referencing one fails.

---

## Debugging checklist (invalid formula / returns nothing)

1. Column name casing — `{PSP Group}` ≠ `{psp group}`
2. Add `#Labels` to dropdown/status columns when comparing text
3. Remove `IFERROR` — use blank guards or LEN+SUBSTITUTE
4. Check quote style — only straight `"` work
5. Test subexpressions — simplify to isolate the failing part
6. Replace error-prone SEARCH with LEN+SUBSTITUTE
7. Nested-IF length — consider SWITCH

## Reference

- `references/functions.md` — complete verified function library (logic, text,
  math, date), syntax rules, examples, ready patterns. Read before writing.
