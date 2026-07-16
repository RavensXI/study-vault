import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
a=json.load(open('_maths_audit/_audit_result.json',encoding='utf-8'))
KEY_HINTS=['ratio','proportion','bc1ac13e']
def rel(e):
    s=json.dumps(e,ensure_ascii=False).lower()
    return any(h in s for h in KEY_HINTS)
for k in ['issues','unconfirmed','confirmed']:
    print("="*10,k)
    for e in a[k]:
        if rel(e):
            print(json.dumps(e,ensure_ascii=False)[:600])
