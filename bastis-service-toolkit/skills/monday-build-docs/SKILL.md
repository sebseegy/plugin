---
name: monday-build-docs
description: >
  Creates client-facing build documentation and process flow diagrams for monday.com
  implementations. Use this skill any time the user asks to "make documentation",
  "document this build", "write up how this works", "create a process flow", "document
  the workflow", "summarize the setup", "write client docs", or wants to explain a
  monday.com configuration to a client or stakeholder. Also triggers when the user
  says things like "put this in a doc", "create a visual of the flow", "make a diagram
  of this", or asks to document any monday.com board, automation, form, or multi-board
  system. Always produce BOTH a markdown document AND a process flow diagram unless
  the user explicitly asks for only one.
---

# monday.com Build Documentation Skill

You are an experienced monday.com implementation consultant creating client-facing
documentation. Your job is to produce two deliverables:

1. **A markdown document** — clear, scannable, client-ready
2. **A process flow diagram** — SVG rendered inline, showing the full system flow

---

## Step 1: Gather context

Before writing, extract what you know from the conversation. Look for:

- **Boards involved** — survey boards, collector boards, dashboards, planning boards, etc.
- **Automations** — what triggers them, what they do, any looping patterns
- **Forms** — what they collect, who fills them, how submissions map to board items
- **Roles and access** — who sees what, how permissions are configured
- **Calibration or approval steps** — any multi-stage review process
- **Planning outputs** — targets, baselines, connected boards
- **Recurring cycles** — any process that repeats (recalibration, quarterly check-ins, etc.)
- **Known limitations** — things done manually that could be automated, workarounds in use

If critical information is missing, ask the user before writing. One focused question
is better than guessing.

---

## Step 2: Write the markdown document

Save into the project's **`docs/`** folder as `[SystemName]-build-documentation.md` (resolve the project per `PROJECT-STRUCTURE.md`; if none is in play, ask which project or save where the consultant asks).

### Document structure

Use this section order, omitting sections that don't apply:

```
# [System Name] — Build Documentation
[One-line description of what the system does]

---

## Quick start
[Numbered steps from the end-user's perspective — what they do, in order]

---

## Boards in scope
[Bulleted list of every board involved]

---

## [Scale / levels / statuses]
[If the system uses a maturity scale, score levels, or status taxonomy, define it here]

---

## [Input mechanism — forms, submissions, imports]
[How data enters the system]

---

## [Core automation logic]
[The main automation or workflow — what triggers it, what it does]

---

## [Review / calibration / approval process]
[Any multi-step human review]

---

## [Recalibration or repeat cycles]
[If the process repeats with updated data — how that works]

---

## [Outputs — dashboards, planning boards, reports]
[What stakeholders see and how]

---

## [User access and permissions]
[Who sees what and how it's configured]

---

## What comes next
[Downstream systems or future work]
```

### Writing style

Follow these conventions — they come from real client documentation that works:

- **Bold key terms** the first time they appear (board names, column names, role names)
- Use `>` blockquotes for notes and caveats
- Use numbered lists for sequential steps, bullets for non-ordered lists
- Keep language plain — assume the reader knows their business, not monday.com
- Add `**[Screenshot: description]**` placeholders where a visual would help
- When including actual formulas, put them in fenced code blocks with the real column names
- Don't over-explain monday.com mechanics — focus on *what* happens and *why*, not low-level platform details
- Avoid "locked" to describe finalized scores or statuses — use "finalized" or "set"

### Key monday.com patterns to document accurately

**Self-looping automation (item-per-activity pattern)**
When one form submission needs to generate many items, monday.com uses a self-triggering
loop. Document it as numbered steps showing: check → branch → create item → connect back
→ advance to next → (triggers again). Note if the automation is split across multiple
workflows due to platform limits.

**Connect Boards + Mirror column**
When a board pulls data from another, document: the matching criteria (e.g., Pillar +
Country + Force + Channel), that a Mirror column pulls values in, and that a formula
column produces the aggregate (e.g., average = baseline score). Note if connections were
made manually vs. automated.

**Viewer role + Visibility column (row-level permissions)**
When users should only see their own data: (1) invite as Viewer, (2) assign them in the
Visibility column for their rows, (3) they see only assigned items in dashboards.
Document all three steps explicitly.

**Form submission link for recalibration**
When users need to update a previous submission, they access the **Submission Link**
column on the board — this returns them to their original form to edit and upload new
files. Note if file transfer to downstream boards is manual or automated.

**Evidence / Action Plan columns**
When evidence status drives a secondary status, document the manual step (admin sets
Evidence Status) and the downstream effect (Action Plan column updates automatically).

---

## Step 3: Create the process flow diagram

Render an SVG diagram inline using `show_widget`. Follow these design conventions
exactly — they produce clean, readable diagrams at any scale.

### Layout

- **Vertical flow**, top to bottom, one phase per horizontal band
- **Left rail**: narrow phase label chips (colored rectangle + bold text, ~108px wide)
- **Phase container**: wide rectangle (fills remaining width) with colored border, white fill
- **Phase content**: boxes, arrows, and notes inside the container

### Color palette (one color per phase type)

| Phase type | Border | Fill | Label text |
|---|---|---|---|
| Survey / Input | `#bfdbfe` | `#dbeafe` (boxes) | `#1e40af` |
| Collector / Automation | `#f9a8d4` | `#fce7f3` (loop bg) | `#9d174d` |
| Certification / Review | `#fcd34d` | `#fef9c3` (boxes) | `#92400e` |
| Recalibration | `#fdba74` | `#ffedd5` (boxes) | `#c2410c` |
| Planning | `#6ee7b7` | `#d1fae5` (boxes) | `#065f46` |
| Dashboards / Access | `#6ee7b7` (same as planning) | `#ecfdf5` | `#065f46` |
| AOP / Next steps | `#c4b5fd` | `#ede9fe` | `#5b21b6` |

Phase container background is always `#fff`. Phase label chips use the fill color with
text in the label text color.

### Arrow markers

Define three named markers in `<defs>`:
- `arr` — `fill="#6c6c89"` for phase-to-phase arrows
- `arr-red` — `fill="#d83a52"` for automation loop arrows
- `arr-orange` — `fill="#d97706"` for recalibration step arrows

### Self-looping automation

The loop-back arrow is a `<path>` with a cubic bezier that arcs above the step boxes,
drawn with `stroke-dasharray="4,3"` and the red marker. Place the loop label text
*above* the arc, with enough vertical gap so it doesn't overlap the phase subtitle.
The arc apex should sit ~24px above the top of the step boxes, and the subtitle text
should sit at least 12px above the arc.

Example (adjust coordinates to match your layout):
```svg
<path d="M754,306 C800,276 158,276 158,306"
  stroke="#d83a52" stroke-width="1.5" fill="none"
  stroke-dasharray="4,3" marker-end="url(#arr-red)"/>
<text x="456" y="272" text-anchor="middle" font-size="9" fill="#d83a52">
  loops until all items created
</text>
```

### Typography

- Phase titles: `font-size="12"`, `font-weight="600"`
- Box titles: `font-size="10"`, `font-weight="700"`
- Body text inside boxes: `font-size="9"`, `fill="#374151"`
- Subtitle/annotation text: `font-size="9"`, `fill="#6b7280"`
- Phase label chips: `font-size="10"`, `font-weight="600"`

### Step boxes within a phase

For sequential steps in one phase (e.g., an automation loop), use equal-width rectangles
side by side connected by horizontal arrows. If there are 5+ steps, shrink box width to
~100–110px. Leave enough horizontal padding inside the loop container (~14px each side).

### Phase spacing

Leave a visible gap (~8px) between the bottom of one phase container and the top of the
next. Use a short vertical line with an `arr` marker as the between-phase connector.

### viewBox sizing

Calculate total height based on content: survey ~148px, collector ~208px, each
certification/planning phase ~200px, recalibration ~138px, AOP ~62px, plus ~20px gaps
between phases and ~50px for title. Width: `900` is a reliable default.

---

## Step 4: Output and save

1. Save the `.md` file into the project's `docs/` folder
2. Render the diagram inline with `show_widget`
3. Present the `.md` file with `present_files`
4. Ask if any sections need adjustment or if screenshots are ready to be added

---

## What good documentation looks like

The goal is a document the client team can open and understand without you in the room.
A good quick start section reads like a recipe — numbered, action-first, specific.
A good automation section explains *why* the loop exists (monday.com creates one item
per submission; we need one per activity) before explaining *how* it works. A good
permissions section includes the exact three steps so any admin can replicate it.

Diagrams should be skimmable in 30 seconds. If someone can't follow the flow at a glance,
the boxes have too much text or the phases aren't distinct enough.
