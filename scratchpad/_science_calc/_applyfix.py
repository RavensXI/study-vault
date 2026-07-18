import json, io
pd=json.load(io.open('_live_canon_fresh.json',encoding='utf-8'))

# Fix 1: board-neutrality on prerequisites[1]
old = pd['topic_links']['prerequisites'][1]
assert old == "Required Practical 9: Sampling with quadrats", repr(old)
pd['topic_links']['prerequisites'][1] = "Sampling with quadrats and transects (fieldwork practical)"

# Fix 2: float-noise box answers -> clean
b3 = pd['problem_bank']['bronze'][3]['guided_steps']
assert b3[1]['answer'] == 0.7999999999999998
b3[1]['answer'] = 0.8
assert b3[2]['answer'] == 0.3999999999999999
b3[2]['answer'] = 0.4
assert b3[3]['answer'] == 39.99999999999999
b3[3]['answer'] = 40
assert b3[5]['answer'] == 0.7999999999999998
b3[5]['answer'] = 0.8

s1 = pd['problem_bank']['silver'][1]['guided_steps']
assert s1[1]['answer'] == -2.8000000000000007
s1[1]['answer'] = -2.8
assert s1[3]['answer'] == -33.300000000000004
s1[3]['answer'] = -33.3

with io.open('lesson_biology-data-skills-L03@40fdb75726.json','w',encoding='utf-8') as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print('shard written. prereqs:', pd['topic_links']['prerequisites'])
# confirm no long-repr floats remain
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f'{path}.{k}')
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f'{path}[{i}]')
    else: yield path,o
noisy=[(p,v) for p,v in walk(pd) if isinstance(v,float) and len(repr(v))>8]
print('remaining noisy floats:', noisy)
