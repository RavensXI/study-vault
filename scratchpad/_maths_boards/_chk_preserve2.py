import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LID = '7f991a30-4b90-4e0e-8cf8-f37a3210006e'
live = json.load(open('_live_L04.json', encoding='utf-8'))[0]['practice_data']
pre_all = json.load(open('_pre_dump_maths-aqa.json', encoding='utf-8'))
pre = None
for row in pre_all:
    if row['id'] == LID:
        pre = row['practice_data']
        break
print('pre found:', pre is not None)
print('pre keys:', sorted(pre.keys()))
print('live keys:', sorted(live.keys()))

for f in ['related_videos', 'topic_links', 'worked_examples']:
    a = pre.get(f); b = live.get(f)
    same = json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False)
    print(f, 'PRESERVED:', same)
    if not same:
        print('  PRE :', json.dumps(a, ensure_ascii=False)[:500])
        print('  LIVE:', json.dumps(b, ensure_ascii=False)[:500])

print('\n=== problem_bank diff vs pre (svg stripped) ===')
pb_pre = pre.get('problem_bank', {}); pb_live = live.get('problem_bank', {})
for t in ['bronze', 'silver', 'gold']:
    lp = pb_live.get(t, []); pp = pb_pre.get(t, [])
    print('---', t, 'pre=', len(pp), 'live=', len(lp))
    for i in range(max(len(lp), len(pp))):
        a = pp[i] if i < len(pp) else None
        b = lp[i] if i < len(lp) else None
        if a is None or b is None:
            print('  [', i, '] MISSING one side'); continue
        da = re.sub(r'<svg.*?</svg>\s*', '', a.get('display', ''), flags=re.S)
        db = re.sub(r'<svg.*?</svg>\s*', '', b.get('display', ''), flags=re.S)
        if da != db:
            print('  [', i, '] DISPLAY changed:'); print('     pre :', da); print('     live:', db)
        if a.get('options') != b.get('options'):
            print('  [', i, '] OPTIONS: pre=', a.get('options'), 'live=', b.get('options'))
        if a.get('solutions') != b.get('solutions'):
            print('  [', i, '] SOLUTIONS: pre=', a.get('solutions'), 'live=', b.get('solutions'))
