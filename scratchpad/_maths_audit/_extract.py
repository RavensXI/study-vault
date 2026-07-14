import json, io, sys
from collections import Counter
sys.stdout.reconfigure(errors="replace")
raw = io.open(r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\tasks\wgw0o7u99.output", encoding="utf-8").read()
i = raw.find('{"audited":48')
if i < 0:
    i = raw.find('"audited": 48') - 1
depth = 0; j = i; instr = False; esc = False
while j < len(raw):
    c = raw[j]
    if instr:
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == '"': instr = False
    else:
        if c == '"': instr = True
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                j += 1
                break
    j += 1
res = json.loads(raw[i:j])
io.open('scratchpad/_maths_audit/_audit_result.json', 'w', encoding='utf-8').write(json.dumps(res, ensure_ascii=False, indent=1))
print('audited:', res['audited'], '| confirmed wrong:', len(res['confirmed']), '| rejected disputes:', len(res['unconfirmed']), '| issues:', len(res['issues']))
print('issue types:', Counter(x['type'] for x in res['issues']))
print('progression:', Counter(p['verdict'] for p in res['progression']))
for p in [p for p in res['progression'] if p['verdict'] in ('flat', 'inverted')][:8]:
    print('  ', p['key'], p['verdict'], '-', p['note'][:90])

def is_data_error(d):
    t = (d.get('working', '') + ' ' + d.get('claimed_correct', '') + ' '.join(d.get('verifier_notes', []))).lower()
    return ('data error' in t) or ('/' in d['claimed_correct']) or ('√' in d['claimed_correct']) or ('no integer' in d['claimed_correct'].lower())

sol = [d for d in res['confirmed'] if not is_data_error(d)]
rep = [d for d in res['confirmed'] if is_data_error(d)]
print('solution-value fixes:', len(sol), '| problem-repair needed:', len(rep))
for d in sol:
    print('  SOL', d['key'], d['tier'], d['index'], ':', d['stored_solution'], '->', d['claimed_correct'][:48])
for d in rep:
    print('  REP', d['key'], d['tier'], d['index'], ':', d['display'][:74])
json.dump({'sol': sol, 'rep': rep}, io.open('scratchpad/_maths_audit/_confirmed_split.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
