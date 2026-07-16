import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
a=json.load(open("_maths_audit/_audit_result.json",encoding="utf-8"))
for s in ['confirmed','unconfirmed','issues']:
    items=a.get(s,[])
    for x in items:
        blob=json.dumps(x,ensure_ascii=False)
        if '007f6c38' in blob or 'number-l04' in blob.lower() or ('l04' in blob.lower()):
            print(f"[{s}]", blob[:500])
