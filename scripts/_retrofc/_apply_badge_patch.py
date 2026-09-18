"""Apply a badge/scheme patch file from the fleet mark-label review (18 Sep 2026).
  python scripts/_retrofc/_apply_badge_patch.py scripts/_retrofc/_badges/<group>_patch.json [--dry-run]
Each entry: lesson_id, i, expect_type, new_type|null, expect_marks_head, new_marks|null, reason.
Verifies the live values before writing; backs up every touched lesson's practice_questions to scripts/_deleted/."""
import os, sys, io, json, datetime, requests
H = {'apikey': os.environ['SUPABASE_SERVICE_KEY'], 'Authorization': 'Bearer ' + os.environ['SUPABASE_SERVICE_KEY'], 'Content-Type': 'application/json', 'Prefer': 'return=minimal'}
U = os.environ['SUPABASE_URL']
path = sys.argv[1]; dry = '--dry-run' in sys.argv
patch = json.load(io.open(path, encoding='utf-8'))
by = {}
for e in patch: by.setdefault(e['lesson_id'], []).append(e)
backup = {}; applied = skipped = 0
for lid, entries in by.items():
    row = requests.get(U + '/rest/v1/lessons?id=eq.%s&select=practice_questions' % lid, headers=H).json()[0]
    pq = row['practice_questions']; backup[lid] = json.loads(json.dumps(pq)); changed = False
    for e in entries:
        q = pq[e['i']] if e['i'] < len(pq) else None
        if not q or q.get('type') != e['expect_type'] or not (q.get('marks') or '').startswith((e.get('expect_marks_head') or '')[:40]):
            print('  SKIP', lid[:8], e['i'], 'live value differs'); skipped += 1; continue
        if e.get('new_type'): q['type'] = e['new_type']
        if e.get('new_marks'): q['marks'] = e['new_marks']
        changed = True; applied += 1
    if changed and not dry:
        r = requests.patch(U + '/rest/v1/lessons?id=eq.' + lid, headers=H, json={'practice_questions': pq}); r.raise_for_status()
tag = os.path.basename(path).replace('_patch.json', '')
if not dry:
    io.open('scripts/_deleted/badge_patch_backup_%s_%s.json' % (tag, datetime.date.today().isoformat()), 'w', encoding='utf-8').write(json.dumps(backup, ensure_ascii=False))
print('%s: applied %d, skipped %d, lessons %d%s' % (tag, applied, skipped, len(by), ' (dry run)' if dry else ''))
