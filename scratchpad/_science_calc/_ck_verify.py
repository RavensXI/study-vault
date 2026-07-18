import json,re
pd=json.load(open('_ck_canonical_live.json',encoding='utf-8'))

def walk_strings(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from walk_strings(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk_strings(v,path+f"[{i}]")
    elif isinstance(o,str):
        yield path,o

# em dash scan
print("=== EM DASH (\u2014) ===")
for p,s in walk_strings(pd):
    if '—' in s:
        print("EMDASH",p,repr(s[:80]))

# board name scan (student-facing)
print("=== BOARD NAMES / equation sheet ===")
for p,s in walk_strings(pd):
    low=s.lower()
    for term in ['aqa','edexcel','ocr','eduqas','wjec','equation sheet','on your sheet','memorise','must memorise','you must memor']:
        if term in low:
            print("TERM",term,"|",p,"|",repr(s[:100]))

# unit conversions / accept sanity + expects reproduction handled manually
pb=pd['problem_bank']
print("=== higher_only field presence ===")
for t in ('bronze','silver','gold'):
    for i,pr in enumerate(pb[t]):
        print(t,i,"higher_only=",pr.get('higher_only','MISSING'),"unit=",pr.get('unit','-'),"accept=",pr.get('accept','-'),"sol=",pr.get('solutions'))
