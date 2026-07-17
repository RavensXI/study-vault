import json, re
live = json.load(open('_CHK_gL04_live.json', encoding='utf-8'))
pd = live['practice_data']
s = json.dumps(pd, ensure_ascii=False)

print('EM DASH count:', s.count('—'))
for m in re.finditer('.{25}—.{25}', s):
    print('  ctx:', m.group(0))

# hint plain-text check
bad = []
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'hint' and isinstance(v, str):
                if ('\\' in v) or ('$' in v) or ('<' in v) or ('\\(' in v):
                    bad.append((path + '/hint', v))
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '[' + str(i) + ']')
walk(pd)
print('non-plain hints:', bad)

# check every misconception message uses unicode minus not hyphen-in-subtraction (informational)
# check numeric-only box answers
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pd['problem_bank'][tier]):
        for j,st in enumerate(p.get('guided_steps',[])):
            if 'answer' in st and not isinstance(st['answer'], (int,float)):
                print('NON-NUMERIC box', tier, i, j, st['answer'])
# teach + opener
for t in ('bronze','silver','gold'):
    for j,st in enumerate(pd['guided']['teach'][t]['steps']):
        if 'answer' in st and not isinstance(st['answer'],(int,float)):
            print('NON-NUMERIC teach', t, j)
for j,st in enumerate(pd['guided']['opener']['steps']):
    if 'answer' in st and not isinstance(st['answer'],(int,float)):
        print('NON-NUMERIC opener', j)
print('numeric box check done')
