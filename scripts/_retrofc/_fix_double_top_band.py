"""Mark schemes that label two different bands "Top band" (a template fault; 413 found 18 Sep 2026):
the second, lower-range "Top band" becomes "Middle band". Run with --dry-run first.
  python scripts/_retrofc/_fix_double_top_band.py [--dry-run]"""
import os, sys, io, json, re, datetime, requests
H = {'apikey': os.environ['SUPABASE_SERVICE_KEY'], 'Authorization': 'Bearer ' + os.environ['SUPABASE_SERVICE_KEY'], 'Content-Type': 'application/json', 'Prefer': 'return=minimal'}
U = os.environ['SUPABASE_URL']; dry = '--dry-run' in sys.argv
rows = []; start = 0
while True:
    r = requests.get(U + '/rest/v1/lessons?select=id,practice_questions&status=eq.live&offset=%d&limit=1000' % start, headers=H).json(); rows += r; start += 1000
    if len(r) < 1000: break
pat = re.compile(r'Top band \((\d+)\s*[-–]\s*(\d+)\)')
backup = {}; fixed = 0; lessons = 0
for l in rows:
    pq = l.get('practice_questions') or []; changed = False
    for q in pq:
        if not isinstance(q, dict): continue
        s = q.get('marks') or ''; ms = list(pat.finditer(s))
        if len(ms) < 2: continue
        # keep the highest-range "Top band"; rename the others "Middle band"
        top = max(ms, key=lambda m: int(m.group(2)))
        out = s
        for m in reversed(ms):
            if m is top: continue
            out = out[:m.start()] + 'Middle band (' + m.group(1) + '-' + m.group(2) + ')' + out[m.end():]
        if out != s:
            backup.setdefault(l['id'], json.loads(json.dumps(pq))); q['marks'] = out; changed = True; fixed += 1
    if changed:
        lessons += 1
        if not dry: requests.patch(U + '/rest/v1/lessons?id=eq.' + l['id'], headers=H, json={'practice_questions': pq}).raise_for_status()
if not dry: io.open('scripts/_deleted/double_top_band_backup_%s.json' % datetime.date.today().isoformat(), 'w', encoding='utf-8').write(json.dumps(backup, ensure_ascii=False))
print('schemes fixed', fixed, 'lessons', lessons, '(dry run)' if dry else '')
