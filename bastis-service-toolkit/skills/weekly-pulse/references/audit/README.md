# Audit workspace for weekly-pulse

Files here are the persistent state of the weekly claim audit. Method lives in `../../SKILL.md`.

- `claims.csv`      Ledger of load-bearing claims in the skills. One row per claim.
- `sources.md`      Registry of primary sources, grades, and named owners (DRIs).
- `queue.md`        Open questions for named owners. Items leave only with a grade A/B source.
- `snapshots/`      Latest raw snapshots (schema, MCP tool lists, support articles). Overwritten each run; previous kept as `*.prev`.
- `proposed/`       Proposed SKILL.md patches (`<skill>.md`) awaiting Basti's approval. Never auto-applied.
- `evals/`          Fixed client-question set. Answer keys come from grade A/B sources, filled by Basti or cited from a primary source - never by the model that edits the skills.

Status values in claims.csv: `verified` (A/B source, in date) · `unverified` · `STALE` (known outdated) · `CONTRADICTED` (two skills or a source disagree) · `UNVERIFIED-CONFLICT` (a digest says X, its own source says Y) · `expired` (past `expires`, needs re-check).
