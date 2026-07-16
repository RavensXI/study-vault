import json, re
live = json.load(open('_live_geoL01.json', encoding='utf-8'))

def norm(s):
    return s.replace('−','-').replace('×','*').replace('÷','/').replace('°','')

allowed = set('0123456789()+-*/. ')
pat = re.compile(r'([0-9(][0-9()+\-*/. ]*?)=\s*$')

def check(steps, label):
    for i, s in enumerate(steps):
        if 'answer' not in s:
            continue
        pre = norm(s.get('pre', '')).rstrip()
        m = pat.search(pre)
        if m:
            expr = m.group(1).strip()
            if any(c in expr for c in '+-*/') and any(c.isdigit() for c in expr):
                if all(c in allowed for c in expr):
                    try:
                        val = eval(expr)
                        if abs(val - s['answer']) > 1e-9:
                            print(f'MISMATCH {label}[{i}] expr={expr!r} eval={val} answer={s["answer"]}')
                    except Exception as e:
                        print('EVALERR', label, i, expr, e)

pb = live['problem_bank']
for tier in ['bronze', 'silver', 'gold']:
    for j, p in enumerate(pb[tier]):
        if 'guided_steps' in p:
            check(p['guided_steps'], f'{tier}[{j}].gs')
for tier in ['bronze', 'silver', 'gold']:
    check(live['guided']['teach'][tier]['steps'], f'teach.{tier}')
check(live['guided']['opener']['steps'], 'opener')
print('arithmetic check done')
