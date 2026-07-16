import json
try:
    a=json.load(open("../_maths_audit/_audit_result.json",encoding="utf-8"))
    def scan(node,label):
        for it in node:
            s=json.dumps(it)
            if "algebra-L10" in s or "algebra/10" in s or "ddb5e897" in s or ("L10" in s and "algebra" in s.lower()):
                print(label, json.dumps(it)[:500])
    if isinstance(a,dict):
        for k in ("issues","unconfirmed"):
            if k in a: scan(a[k],k)
    print("audit scanned")
except Exception as e:
    print("audit err",e)
# changes log
try:
    c=json.load(open("changes_algebra-L10.json",encoding="utf-8"))
    print("CHANGES:", json.dumps(c)[:800])
except Exception as e:
    print("changes err",e)
