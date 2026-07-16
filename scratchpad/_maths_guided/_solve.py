import json
pd = json.load(open('_live_geometry_L04.json', encoding='utf-8'))
pb = pd['problem_bank']

def clean(o):
    return o.replace('\\(', '').replace('\\)', '').replace('\\', '')

for tier in ['gold', 'bronze', 'silver']:
    for i, p in enumerate(pb[tier]):
        disp = p['display']
        if '<svg' in disp:
            disp = disp[disp.rfind('>') + 1:]
        sol = p['solutions']
        if p['input_type'] == 'multiple_choice':
            print(f"{tier}[{i}] idx={sol[0]} -> {clean(p['options'][sol[0]])}  | {disp[:78]}")
        else:
            print(f"{tier}[{i}] value={sol}  | {disp[:78]}")
