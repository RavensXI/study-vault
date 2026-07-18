import json, io
pd=json.load(io.open("_live_canonical.json",encoding="utf-8"))
out=io.open("_dump.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    w("="*70)
    w("TIER",tier,"  desc:",pb.get(tier+"_description"))
    for i,p in enumerate(pb[tier]):
        w("-"*50)
        w(f"{tier}[{i}] display:",p.get("display"))
        w("  input_type:",p.get("input_type"),"solutions:",p.get("solutions"),"accept:",p.get("accept"),"unit:",p.get("unit"),"higher_only:",p.get("higher_only"),"calc:",p.get("calculator"))
        if p.get("options"): w("  options:",p["options"])
        w("  equation_hint:",p.get("equation_hint"))
        w("  hint:",p.get("hint"))
        for j,m in enumerate(p.get("misconceptions") or []):
            w(f"  misc[{j}] pattern={m.get('pattern')} expect={m.get('expect')} msg={m.get('message')}")
out.close()
print("done")
