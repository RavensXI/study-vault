import json, io
pd=json.load(io.open("_live_canonical.json",encoding="utf-8"))
out=io.open("_walks.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")

def dump_steps(steps,label):
    w("### "+label)
    for i,s in enumerate(steps):
        if s.get("answer") is not None:
            w(f"  [{i}] BOX pre={s.get('pre')!r} post={s.get('post')!r} answer={s.get('answer')} phase={s.get('phase')} hint={s.get('hint')!r} done={s.get('done')!r} say={s.get('say')!r}")
        else:
            w(f"  [{i}] SAY say={s.get('say')!r} done={s.get('done')!r}")

g=pd["guided"]
w("========= OPENER =========")
w("display:",g["opener"].get("display"))
dump_steps(g["opener"]["steps"],"opener")
for tier in ("bronze","silver","gold"):
    t=g["teach"][tier]
    w("========= TEACH",tier,"=========")
    w("display:",t.get("display"))
    dump_steps(t["steps"],"teach."+tier)

pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if gs: dump_steps(gs, f"{tier}[{i}].guided_steps  (sol={p.get('solutions')})")
out.close()
print("done")
