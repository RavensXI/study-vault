import json
d=json.load(open('_live_ps_L03.json',encoding='utf-8'))[0]['practice_data']
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,path+'['+str(i)+']')
    elif isinstance(o,str):
        yield path,o
EM=chr(0x2014); EN=chr(0x2013)
hits=[]
for p,s in walk(d):
    if EM in s or EN in s:
        if p.endswith('.note'):
            continue
        hits.append((p,s))
print("EM/EN dash hits (student-facing):", len(hits))
for p,s in hits:
    print(' ',p, repr(s[:90]))
print("\nDistinct non-ASCII:")
chars={}
for p,s in walk(d):
    for c in s:
        if ord(c)>127:
            chars[c]=chars.get(c,0)+1
for c,n in sorted(chars.items(), key=lambda x:-x[1]):
    print('  U+%04X %r x%d'%(ord(c),c,n))
