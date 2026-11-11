#!/usr/bin/env bash
# SessionStart hook: injects the client's live state into every session (startup, resume, clear, compact).
# stdout is added to Claude's context. Read-only. Safe if files are missing.
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
STATE="$ROOT/Client Context/project-state.md"
MAX_LINES=150
STALE_DAYS=3

echo "## Live client state (injected at session start from Client Context/project-state.md)"
if [ -f "$STATE" ]; then
  head -n "$MAX_LINES" "$STATE"
  [ "$(wc -l < "$STATE")" -gt "$MAX_LINES" ] && echo "... (truncated at $MAX_LINES lines; read the full file)"
else
  echo "NO project-state.md yet. Create it from the template before doing project work."
fi

# Mechanical activity trace: files changed since the state file was last written (independent of the log).
echo
echo "## Files modified since last state update (excluding All Calls)"
if [ -f "$STATE" ]; then
  find "$ROOT" -type f -newer "$STATE" \
    -not -path "*/All Calls/*" -not -path "*/.claude/*" -not -path "*/_archive/*" \
    -not -name ".DS_Store" -not -name "project-state.md" 2>/dev/null | head -n 12 | sed "s#^$ROOT/##"
  NEWER=$(find "$ROOT" -type f -newer "$STATE" -not -path "*/All Calls/*" -not -path "*/.claude/*" -not -path "*/_archive/*" -not -name ".DS_Store" 2>/dev/null | wc -l | tr -d ' ')
  MT=$(stat -c %Y "$STATE" 2>/dev/null || stat -f %m "$STATE" 2>/dev/null || echo 0)
  AGE_DAYS=$(( ( $(date +%s) - MT ) / 86400 ))
  if [ "$NEWER" -gt 0 ]; then
    echo "WARNING: $NEWER file(s) changed after the last state update ($AGE_DAYS day(s) ago). The state may be stale: verify against these files, then update project-state.md."
  elif [ "$AGE_DAYS" -ge "$STALE_DAYS" ]; then
    echo "Note: state last updated $AGE_DAYS day(s) ago, no file changes since."
  else
    echo "(none: state is current)"
  fi
fi
exit 0
