import json, re

live = json.load(open('_CHK_rpL04_LIVE.json', encoding='utf-8'))
issues = []

# em dash scan across all string values (student-facing). Note internal 'note' exempt.
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'note':
                continue
            walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f'{path}[{i}]')
    elif isinstance(o, str):
        if '—' in o:
            issues.append(f'EM-DASH at {path}: {o[:80]}')
walk(live, 'root')

# Verify guided_steps boxes: parse "a OP b = " in pre, check answer
opmap = {'×': lambda a,b: a*b, '÷': lambda a,b: a/b, '−': lambda a,b: a-b, '+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b, '/': lambda a,b: a/b}
pat = re.compile(r'^\s*([\d.]+)\s*([×÷−+\-*/])\s*([\d.]+)\s*=\s*$')

def check_steps(steps, path):
    for i, s in enumerate(steps):
        if 'answer' not in s:
            continue
        pre = s.get('pre','')
        m = pat.match(pre)
        if m:
            a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
            res = opmap[op](a,b)
            ans = s['answer']
            if abs(res - ans) > 1e-9:
                issues.append(f'BOX MISMATCH {path}[{i}]: {pre!r} => {res} but answer={ans}')
        else:
            # non-arithmetic pre, note it
            pass

pb = live['problem_bank']
for t in ['bronze','silver','gold']:
    for pi, p in enumerate(pb[t]):
        gs = p.get('guided_steps')
        if gs:
            check_steps(gs, f'{t}[{pi}].guided_steps')
        # completion boundary
        phases = [i for i,s in enumerate(gs or []) if s.get('phase')=='substitute']
        if p.get('input_type')!='multiple_choice' and gs:
            if not phases:
                issues.append(f'NO PHASE {t}[{pi}]')
            else:
                pidx = phases[0]
                before = pidx
                after = len(gs)-pidx
                if before < 1 or after < 2:
                    issues.append(f'BOUNDARY {t}[{pi}]: before={before} after={after}')

# teach walks
for t in ['bronze','silver','gold']:
    check_steps(live['guided']['teach'][t]['steps'], f'teach.{t}.steps')
# opener
check_steps(live['guided']['opener']['steps'], 'opener.steps')

print('ISSUES:', len(issues))
for x in issues:
    print(' -', x)
