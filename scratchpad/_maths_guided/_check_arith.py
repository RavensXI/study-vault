import json, re
live = json.load(open('_live_fresh.json', encoding='utf-8'))
bad = 0
OPRE = re.compile(r'(-?\d+\.?\d*)\s*([×x÷+−])\s*(-?\d+\.?\d*)\s*=\s*\$?\$?\s*\Z')

def check_walk(steps, label):
    global bad
    for j, st in enumerate(steps):
        if 'answer' not in st:
            continue
        pre = st.get('pre', '')
        m = OPRE.findall(pre)
        if m:
            a, op, b = m[-1]
            a = float(a); b = float(b)
            r = {'×': a*b, 'x': a*b, '÷': a/b, '+': a+b, '−': a-b}[op]
            if abs(r - float(st['answer'])) > 1e-9:
                print('ARITH MISMATCH', label, j, repr(pre[-45:]), '=> expected', r, 'stored', st['answer'])
                bad += 1

pb = live['problem_bank']
for tier in pb:
    if tier.endswith('_description'):
        continue
    for i, p in enumerate(pb[tier]):
        gs = p.get('guided_steps')
        if gs:
            check_walk(gs, f'{tier}[{i}]')
            finals = [s['answer'] for s in gs if 'answer' in s]
            if p.get('input_type') != 'multiple_choice':
                sol = p['solutions'][0]
                if sol not in finals:
                    print('SOLUTION not hit', tier, i, 'sol', sol, 'answers', finals)
                    bad += 1
for t in ['bronze', 'silver', 'gold']:
    check_walk(live['guided']['teach'][t]['steps'], 'teach.' + t)
check_walk(live['guided']['opener']['steps'], 'opener')
print('arith sweep done, mismatches:', bad)
