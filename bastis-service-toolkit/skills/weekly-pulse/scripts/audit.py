#!/usr/bin/env python3
"""Helper for the weekly claim audit. Stdlib only. Run: python3 -I audit.py <cmd> [args]

  due [YYYY-MM-DD]        List claims that are expired, contradicted, stale, conflicted, or never verified.
  rotate <file>           Move snapshots/<file> to snapshots/<file>.prev (call before writing a fresh snapshot).
  diff <file>             Unified diff of snapshots/<file>.prev vs snapshots/<file>; prints 'NO CHANGE' if equal.
  evals                   Count eval questions still lacking an answer key.
"""
import csv, os, sys, difflib, datetime
AUD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references', 'audit')
def rows(p):
    with open(os.path.join(AUD, p), newline='') as f: return list(csv.DictReader(f))
def due(today):
    out = []
    for r in rows('claims.csv'):
        why = []
        if r['status'] in ('CONTRADICTED', 'STALE', 'UNVERIFIED-CONFLICT'): why.append(r['status'])
        if r['expires'] and r['expires'] < today: why.append('expired ' + r['expires'])
        if r['status'] == 'unverified' and not r['verified_on']: why.append('never verified')
        if r['status'] == 'verified' and not r['expires']: why.append('no expiry set')
        if why: out.append((r['id'], r['skill'], '; '.join(why), r['claim'][:90]))
    for o in out: print('\t'.join(o))
    print(f'-- {len(out)} claims need attention as of {today}')
def rotate(f):
    p = os.path.join(AUD, 'snapshots', f)
    if os.path.exists(p): os.replace(p, p + '.prev'); print('rotated', f)
    else: print('no current snapshot to rotate')
def diff(f):
    a = os.path.join(AUD, 'snapshots', f + '.prev'); b = os.path.join(AUD, 'snapshots', f)
    if not os.path.exists(b): print('MISSING current snapshot'); return
    if not os.path.exists(a): print('NO PREVIOUS SNAPSHOT (baseline)'); return
    A = open(a).read().splitlines(); B = open(b).read().splitlines()
    d = list(difflib.unified_diff(A, B, 'prev', 'current', lineterm='', n=1))
    print('\n'.join(d) if d else 'NO CHANGE')
def evals():
    q = rows('evals/questions.csv'); n = [x['id'] for x in q if not x['answer_key'].strip()]
    print(f'{len(q)-len(n)}/{len(q)} questions have answer keys; missing: {", ".join(n)}')
if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'due': due(sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat())
    elif c == 'rotate': rotate(sys.argv[2])
    elif c == 'diff': diff(sys.argv[2])
    elif c == 'evals': evals()
    else: print(__doc__)
