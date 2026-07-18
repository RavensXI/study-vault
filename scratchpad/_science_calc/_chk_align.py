import json, io
pd=json.load(io.open("_live_canonical.json",encoding="utf-8"))
out=io.open("_align.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps") or []
        firstsay = gs[0].get("say") if gs else None
        lastbox = [s.get("answer") for s in gs if s.get("answer") is not None]
        w(f"{tier}[{i}] DISPLAY={p.get('display')[:60]!r} SOL={p.get('solutions')} UNIT={p.get('unit')}")
        w(f"    walk_first_say={firstsay!r}")
        w(f"    walk_box_answers={lastbox}")
out.close()
print("done")
