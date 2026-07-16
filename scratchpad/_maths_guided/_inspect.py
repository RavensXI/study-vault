import json,io
pd=json.load(open("_geomL07_LIVE_NOW.json",encoding="utf-8"))
pb=pd["problem_bank"]
out=io.open("_inspect_out.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
for tier,idxs in (("gold",[1]),("silver",[5])):
    for idx in idxs:
        p=pb[tier][idx]
        w("="*80); w(f"{tier}[{idx}]")
        w("solutions:", p.get("solutions"))
        w("input_type:", p.get("input_type"))
        w("hint:", p.get("hint"))
        w("--- display ---"); w(p.get("display"))
        w("--- guided_steps ---")
        for s in p.get("guided_steps",[]):
            w("  ", json.dumps({k:v for k,v in s.items() if k in ("say","pre","post","answer","phase","done")},ensure_ascii=False))
        w("--- misconceptions ---")
        for m in p.get("misconceptions",[]):
            w("  ", json.dumps(m,ensure_ascii=False))
out.close()
print("done")
