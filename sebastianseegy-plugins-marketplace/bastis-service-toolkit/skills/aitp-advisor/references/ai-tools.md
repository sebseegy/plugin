# monday.com AI Tools: When to Recommend What

## Sidekick
**What it does:** Conversational AI assistant embedded in monday.com. Takes action, analyzes data, creates content, and speeds up repetitive tasks.

**Recommend when:**
- Users get stuck or waste time on repeated tasks (drafting updates, spotting missing fields, suggesting priorities)
- Coordinators need help reviewing and acting on flagged items without starting from scratch
- Teams want to query their boards or get summaries in natural language
- Users need help building or editing board structures

**Example use:** A supply chain coordinator uses Sidekick to flag missing fields in supplier delay submissions and draft status updates before sending to leadership.

---

## AI Blocks
**What they do:** Configurable AI columns that run automatically on board items. Each block does a specific job.

| Block | What it does | Best for |
|-------|-------------|----------|
| **Categorize** | Classifies items into predefined categories with a confidence score | Risk classification, ticket routing, priority tagging |
| **Extract** | Pulls specific fields from text (emails, forms, updates) into structured columns | Parsing supplier emails, extracting PO numbers, pulling dates |
| **Summarize** | Condenses long text into a concise summary | Executive-ready status updates, meeting notes, email threads |
| **Sentiment** | Detects tone/emotion in text | Customer feedback analysis, support ticket tone |
| **Translate** | Translates text between languages | Global team communication, multilingual support queues |

**Key configuration note:** Always train AI Block prompts with **15–20+ test items** to refine output quality before finalizing the build.

**Recommend when:** Any workflow involves reading, classifying, or summarizing unstructured text (emails, forms, documents, updates).

---

## AI Workflows (Automations with AI)
**What they do:** Trigger-based automations that incorporate AI decisions or outputs — routing, escalating, notifying based on AI-classified results.

**Recommend when:**
- Items need to be routed to different people based on AI classification (e.g., high-risk → procurement manager)
- Automated summaries or digests should be generated on a schedule
- AI output should trigger a notification, status change, or board action

**Scope note:** Tier 1 includes up to 2 AI Workflows, Tier 2 up to 4, Tier 3 up to 6.

---

## Vibe Apps (AI-powered custom applications)
**What they do:** No-code AI-powered applications for workflows that don't fit neatly into standard boards. Enable custom visualization, complex logic, or multi-board aggregation.

**Recommend when:**
- Standard dashboards can't meet the visualization need (e.g., risk heatmaps, scenario planning tools, multi-supplier views)
- Regional managers need drill-down views with AI-generated insights
- A custom intake experience or command center is needed

**Escalation note:** Complex Vibe coding (custom scripts, weighted AI analysis, multi-board aggregation) should be escalated to a Technical Consultant (TC).

---

## AI Agents
**What they do:** Autonomous agents that can take multi-step actions within and across monday.com workflows. More complex than AI Blocks — can reason, plan, and execute a sequence of steps.

**Recommend when:**
- Repetitive multi-step processes need end-to-end automation
- The workflow involves decision-making at multiple points, not just a single classification
- Customer wants proactive monitoring (e.g., scanning for risks and taking action without human initiation)

---

## Quick Mapping: Pain Point → Tool

| Pain Point | Recommended Tool |
|-----------|-----------------|
| Manual email parsing and data entry | AI Blocks (Extract) + email integration |
| Inconsistent priority/risk classification | AI Blocks (Categorize) with confidence scoring |
| Long updates that need short summaries | AI Blocks (Summarize) |
| Weekly reports that take hours to compile | AI Blocks (Summarize) + AI Workflow (auto-generate) |
| Coordinators starting from scratch on every update | Sidekick |
| Routing high-risk items to the right person | AI Workflow with Categorize trigger |
| Custom executive dashboard with drill-downs | Vibe App |
| Multi-step autonomous process execution | AI Agents |
| Multi-language team communication | AI Blocks (Translate) |

---

## Human Oversight Principles (always apply)

- Confidence percentages are **signals**, not decisions — never let teams treat a % as approval
- Critical/high-risk classifications must **always require human sign-off** before triggering actions or reports
- Track **accuracy and override rates from day one**
- Define **rollback thresholds** upfront: if accuracy or adoption misses targets, pause, review, retrain
- Start with the most impactful, lowest-risk AI configuration — expand only once the pilot proves value
