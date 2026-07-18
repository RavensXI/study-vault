# -*- coding: utf-8 -*-
import json, io, re
s = json.load(io.open('lesson_higher-calculations-L05@c023b518a1.json', encoding='utf-8'))
pb = s['problem_bank']
issues = []
OPS = {'+': lambda a, b: a + b, '−': lambda a, b: a - b,
       '×': lambda a, b: a * b, '÷': lambda a, b: a / b}
pat = re.compile(r'([0-9.]+)\s*([+−×÷])\s*([0-9.]+)\s*=\s*\$*\s*$')

def check_boxes(steps, label):
    for j, st in enumerate(steps):
        if 'answer' not in st:
            continue
        m = pat.search(st.get('pre', ''))
        if m:
            a = float(m.group(1)); r = OPS[m.group(2)](a, float(m.group(3)))
            if abs(r - float(st['answer'])) > 1e-6:
                issues.append('%s step%d: %r -> %s != %s' % (label, j, st['pre'], r, st['answer']))

for tier in ('bronze', 'silver', 'gold'):
    for i, p in enumerate(pb[tier]):
        check_boxes(p.get('guided_steps', []), '%s[%d]' % (tier, i))
        acc = p.get('accept', 0.005)
        sol = p['solutions'][0] if p.get('solutions') else None
        for mc in p.get('misconceptions', []):
            e = mc.get('expect')
            if e is not None and isinstance(sol, (int, float)) and abs(e - sol) <= acc:
                issues.append('%s[%d] DEAD expect %s within %s of %s' % (tier, i, e, acc, sol))

check_boxes(s['guided']['opener']['steps'], 'opener')
for t in ('bronze', 'silver', 'gold'):
    check_boxes(s['guided']['teach'][t]['steps'], 'teach.' + t)

def halvings(a0, a1):
    n = 0; v = a0
    while v > a1 + 1e-9:
        v /= 2; n += 1
    return n

print('gold[0] hl=', 52 / halvings(5000, 312.5), 'sol', pb['gold'][0]['solutions'])
print('gold[4] hl=', 120 / halvings(480, 30), 'sol', pb['gold'][4]['solutions'])
print('silver[0] hl=', 20 / halvings(6400, 400), 'sol', pb['silver'][0]['solutions'])
print('silver[1] hl=', 30 / halvings(1200, 150), 'sol', pb['silver'][1]['solutions'])
print('silver[4] left=', 50 * 0.5 ** (15 // 3), 'sol', pb['silver'][4]['solutions'])

blob = json.dumps(s, ensure_ascii=False).lower()
for b in ['aqa', 'edexcel', ' ocr', 'wjec', 'eduqas', 'equation sheet', 'memorise', 'on your sheet']:
    if b in blob:
        issues.append('BOARD/SHEET term: ' + repr(b))

# gold[4] chart consistency: value at t = 120 min should be ~6.25 (=30/480)
g4 = pb['gold'][4]['chart']
L = g4['data']['labels']; D = g4['data']['datasets'][0]['data']
import bisect
k = bisect.bisect_left(L, 120)
lo, hi = k - 1, k
frac = (120 - L[lo]) / (L[hi] - L[lo])
val = D[lo] + frac * (D[hi] - D[lo])
print('gold[4] chart value at t=120min:', round(val, 3), '(want 6.25 = 30/480*100)')
print('gold[4] chart x-title:', g4['options']['scales']['x']['title']['text'], 'span', L[-1])

print('ISSUES:', len(issues))
for x in issues:
    print(' -', x)
