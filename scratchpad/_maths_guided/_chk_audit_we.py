import json
# audit findings for this lesson
try:
    a = json.load(open("../_maths_audit/_audit_result.json", encoding="utf-8"))
    LID="0b095025-37bb-49e4-94da-6f898ad6f3e7"
    def dump(lst,name):
        hits=[x for x in lst if LID in json.dumps(x) or 'geometry' in json.dumps(x).lower() and ('L08' in json.dumps(x) or "'8'" in json.dumps(x) or 'lesson_8' in json.dumps(x).lower())]
        print(f"--- {name}: {len(hits)} raw geometry-ish, scanning by id ---")
    for key in ["issues","unconfirmed"]:
        lst=a.get(key,[]) if isinstance(a,dict) else []
        hits=[x for x in lst if LID in json.dumps(x)]
        print(f"{key}: {len(hits)} by id")
        for h in hits: print("   ", json.dumps(h)[:300])
    # also try matching key 'geometry-L08'
    for key in ["issues","unconfirmed"]:
        lst=a.get(key,[]) if isinstance(a,dict) else []
        hits=[x for x in lst if 'geometry' in json.dumps(x).lower() and 'L08' in json.dumps(x)]
        print(f"{key} by geometry-L08 str: {len(hits)}")
        for h in hits: print("   ", json.dumps(h)[:300])
except Exception as e:
    print("audit err", e)

print("\n=== worked_examples diff ===")
live=json.load(open("_CHK_geomL08_live.json",encoding="utf-8"))["worked_examples"]
pre=json.load(open("_CHK_geomL08_predump.json",encoding="utf-8"))["worked_examples"]
print("live count",len(live),"pre count",len(pre))
print(json.dumps(pre,ensure_ascii=False)==json.dumps(live,ensure_ascii=False))
import difflib
lp=json.dumps(pre,indent=1,ensure_ascii=False).splitlines()
ll=json.dumps(live,indent=1,ensure_ascii=False).splitlines()
for line in difflib.unified_diff(lp,ll,lineterm="",n=1):
    print(line)
