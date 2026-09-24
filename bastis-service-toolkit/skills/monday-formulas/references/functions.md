# monday.com Formula Column — Complete Function Reference

Source: https://support.monday.com/hc/en-us/articles/360001276465

---

## CRITICAL RULES (never break these)

1. **No math symbols for operations** — NEVER use `+`, `-`, `*`, `/` for math. Use functions instead: `SUM()`, `MINUS()`, `MULTIPLY()`, `DIVIDE()`
   - ❌ `{Revenue} - {Cost}`
   - ✅ `MINUS({Revenue},{Cost})`
   - ❌ `{Hours} * {Rate}`
   - ✅ `MULTIPLY({Hours},{Rate})`
   - NOTE: `>`, `<`, `=`, `>=`, `<=` ARE allowed inside conditions (e.g. `IF({Number}>100,...)`)

2. **Column names in curly braces** — always `{Column Name}` exactly as it appears on the board, case-sensitive

3. **Text and status labels in double quotes** — `IF({Status}="Done","Yes","No")`

4. **Decimals need a leading zero** — `0.25` not `.25`

5. **Every open parenthesis must close** — count them

6. **Comma is dynamic** — in `SUM(a,b)` the comma means addition; in `MULTIPLY(a,b)` it means multiplication; in `IF(condition,true,false)` it separates components. This is just how monday works.

7. **No VLOOKUP, no cross-board reads** — the formula column reads horizontally within one item only

8. **No copy-paste from a text editor** — "smart quotes" break formulas. Always type directly in the formula builder.

---

## Compatible column types

✅ Check, Country, Creation Log, Date, Dependency, Dropdown, Email, Formula, Hour, Item ID, Last Updated, Connect Boards, Long Text, Numbers, Person, Phone, Rating, Status, Text, Timeline, Time Tracking, Vote, World Clock, Subitem Names, Count of Subitems

❌ NOT supported: Autonumber, Color Picker, Files, Link, Location, Mirror, Progress Tracking, Tags, Week

---

## TEXT FUNCTIONS

| Function | What it does | Example |
|---|---|---|
| `CONCATENATE(a,b,...)` | Joins text values | `CONCATENATE("Hello "," ",{Name})` |
| `LEFT(text,n)` | First N characters | `LEFT({Name},3)` |
| `RIGHT(text,n)` | Last N characters | `RIGHT({Code},4)` |
| `LEN(text)` | Number of characters | `LEN({Description})` |
| `LOWER(text)` | Lowercase | `LOWER({Name})` |
| `UPPER(text)` | Uppercase | `UPPER({Name})` |
| `TRIM(text)` | Remove extra spaces | `TRIM({Notes})` |
| `REPLACE(text,start,n,new)` | Replace N chars from position | `REPLACE("Monday",1,3,"Fri")` |
| `SUBSTITUTE(text,old,new)` | Replace by matching | `SUBSTITUTE({Name},"Inc","LLC")` |
| `SEARCH(find,in,start)` | Find string position | `IF(SEARCH("urgent",{Notes},1)>0,"Flag","")` |
| `TEXT(value,format)` | Format number as text | `TEXT({Revenue},"$#,##0.00")` |
| `REPT(text,n)` | Repeat a string | `REPT("★",{Rating})` |

---

## LOGICAL FUNCTIONS

| Function | What it does | Example |
|---|---|---|
| `IF(condition,true,false)` | Conditional | `IF({Status}="Done","✓","✗")` |
| `AND(a,b,...)` | All conditions true | `IF(AND({Budget}>0,{Status}="Active"),"Go","Hold")` |
| `OR(a,b,...)` | Any condition true | `IF(OR({Priority}="High",{Urgent}="Yes"),"Rush","Normal")` |
| `XOR(a,b)` | Exactly one true | `XOR({A}>0,{B}>0)` |
| `EXACT(a,b)` | Exact match check | `EXACT({Status},{Expected})` |
| `SWITCH(val,"v1","r1","v2","r2",default)` | Multi-value switch | `SWITCH({Priority},"High",3,"Medium",2,"Low",1,0)` |
| `TRUE` | Logical true | Used in conditions |
| `FALSE` | Logical false | Used in conditions |

**Nested IF pattern:**
```
IF({Status}="Done","Complete",IF({Status}="In Progress","Active","Pending"))
```

---

## NUMERIC FUNCTIONS

| Function | What it does | Example |
|---|---|---|
| `SUM(a,b,...)` | Add numbers | `SUM({Q1},{Q2},{Q3},{Q4})` |
| `MINUS(a,b)` | Subtract | `MINUS({Budget},{Spent})` |
| `MULTIPLY(a,b)` | Multiply | `MULTIPLY({Hours},{Rate})` |
| `DIVIDE(a,b)` | Divide | `DIVIDE({Revenue},{Units})` |
| `ABS(n)` | Absolute value | `ABS(MINUS({Target},{Actual}))` |
| `ROUND(n,decimals)` | Round to decimal places | `ROUND({Score},2)` |
| `ROUNDUP(n,decimals)` | Always round up | `ROUNDUP({Hours},0)` |
| `ROUNDDOWN(n,decimals)` | Always round down | `ROUNDDOWN({Hours},0)` |
| `MOD(n,divisor)` | Remainder | `MOD({Week},2)` |
| `SQRT(n)` | Square root | `SQRT({Area})` |
| `POWER(base,exp)` | Exponent | `POWER({Rate},2)` |
| `LOG(n,base)` | Logarithm | `LOG(16,2)` |
| `MAX(a,b,...)` | Largest value | `MAX({Q1},{Q2},{Q3})` |
| `MIN(a,b,...)` | Smallest value | `MIN({Q1},{Q2},{Q3})` |
| `AVERAGE(a,b,...)` | Average | `AVERAGE({Q1},{Q2},{Q3})` |
| `COUNT(a,b,...)` | Count numeric items | `COUNT({A},{B},{C})` |
| `PI()` | π value | `MULTIPLY(PI(),POWER({Radius},2))` |

---

## DATE & TIME FUNCTIONS

| Function | What it does | Example |
|---|---|---|
| `TODAY()` | Current date | `DAYS({Due Date},TODAY())` |
| `NOW()` | Current date + time | `HOUR(NOW())` |
| `DATE(year,month,day)` | Create a date | `DATE(2025,12,31)` |
| `DAY(date)` | Day of month (1–31) | `DAY({Created At})` |
| `MONTH(date)` | Month (1–12) | `MONTH({Due Date})` |
| `YEAR(date)` | Year | `YEAR({Start Date})` |
| `HOUR(time)` | Hour (0–23) | `HOUR(NOW())` |
| `MINUTE(time)` | Minute (0–59) | `MINUTE(NOW())` |
| `SECOND(time)` | Second (0–59) | `SECOND(NOW())` |
| `DAYS(end,start)` | Days between two dates | `DAYS({Due Date},{Start Date})` |
| `WORKDAYS(end,start)` | Working days between dates | `WORKDAYS({Due Date},{Start Date})` |
| `ADD_DAYS(date,n)` | Add N days | `ADD_DAYS({Start Date},14)` |
| `SUBTRACT_DAYS(date,n)` | Subtract N days | `SUBTRACT_DAYS({Due Date},7)` |
| `WORKDAY(date,n)` | Add N working days | `WORKDAY({Start Date},10)` |
| `FORMAT_DATE(date,format?)` | Format a date as text | `FORMAT_DATE(TODAY(),"YYYY-MM-DD")` |
| `WEEKNUM(date)` | Week number of year | `WEEKNUM({Created At})` |
| `HOURS_DIFF(end,start)` | Difference between two hour columns | `HOURS_DIFF({End},{Start})` |

**FORMAT_DATE format tokens:**
- `YYYY` = 4-digit year, `MM` = month, `DD` = day
- `dddd` = full weekday name, `MMMM` = full month name
- Default (no format arg): "Feb 16, 2020"

---

## COMMON PATTERNS (ready to adapt)

**Days until due date:**
```
ROUND(DAYS({Due Date},TODAY()),0)
```

**Days overdue (positive = overdue):**
```
ROUND(DAYS(TODAY(),{Due Date}),0)
```

**Budget remaining:**
```
MINUS({Budget},{Spent})
```

**Percentage of total:**
```
ROUND(MULTIPLY(DIVIDE({Sold},{Total}),100),2)
```

**Percentage change between two values:**
```
MULTIPLY(DIVIDE(MINUS({New},{Old}),{Old}),100)
```

**Status-based commission:**
```
IF({Rate}="Tier 1",MULTIPLY(0.25,{Sales}),IF({Rate}="Tier 2",MULTIPLY(0.20,{Sales}),0))
```

**Over/under budget check:**
```
IF(SUM({Cost A},{Cost B},{Cost C})>6500,"Over Budget","Within Budget")
```

**Formatted date result:**
```
FORMAT_DATE(ADD_DAYS({Start Date},15))
```

**Hours worked minus break:**
```
IF(HOURS_DIFF({Break End},{Break Start})>"0",HOURS_DIFF(HOURS_DIFF({End},{Start}),HOURS_DIFF({Break End},{Break Start})),HOURS_DIFF({End},{Start}))
```

**Nested IF for status labels:**
```
IF({Status}="Done","Complete",IF({Status}="In Progress","Active",IF({Status}="Stuck","Blocked","Not Started")))
```
