import json
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
tg=pd["tier_guides"]
for tier in ["bronze","silver","gold"]:
    t=tg[tier]
    words=sum(len(s.split()) for s in t.get("steps",[]))
    print(f"\n===== tier_guides {tier} =====  title={t.get('title')!r} step_words={words}")
    for s in t.get("steps",[]): print("  step:",s)
    ex=t.get("example",{})
    print("  example.question:",ex.get("question"))
    for st in ex.get("steps",[]):
        print("    exstep:",json.dumps(st,ensure_ascii=False))
print("\n\n===== METHOD CARD =====")
mc=pd["method_card"]
print("title:",mc.get("title"))
print("keys:",list(mc.keys()))
import re
def wc(x):
    if isinstance(x,str): return len(re.sub('<[^>]+>','',x).split())
    return 0
print(json.dumps(mc,ensure_ascii=False,indent=1)[:2500])
