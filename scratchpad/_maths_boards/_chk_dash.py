import json
d=json.load(open('_live_ps_L03.json'))[0]['practice_data']
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,path+'['+str(i)+']')
    elif isinstance(o,str):
        yield path,o
emdash=[]
for p,s in walk(d):
    if '—' in s or '–' in s:
        emdash.append((p,s))
print("EM/EN DASH hits:", len(emdash))
for p,s in emdash:
    print(' ',p, repr(s[:100]))
