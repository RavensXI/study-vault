# -*- coding: utf-8 -*-
import json, io, sys

sys.stdout.reconfigure(encoding="utf-8")

ID="1422954b-1171-49c2-a0c0-d5a1feb0da0d"
live=json.load(io.open("_CHK_algL08ocr_live.json",encoding="utf-8"))
pre_all=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
pre=None
for e in pre_all:
    if e.get("id")==ID:
        pre=e; break
print("pre found:", pre is not None)
prepd = pre.get("practice_data") if pre else {}

# preservation: related_videos, topic_links, worked_examples
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(prepd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f"PRESERVE {f}: {'UNCHANGED' if same else 'CHANGED'}")
    if not same:
        print("  pre :", json.dumps(prepd.get(f),ensure_ascii=False)[:400])
        print("  live:", json.dumps(live.get(f),ensure_ascii=False)[:400])

# em dash scan
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o
emdash=[(p,s) for p,s in walk(live) if "—" in s]
print("EM DASHES:", len(emdash))

pb=live["problem_bank"]
hintbad=[]
boxbad=[]
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        h=prob.get("hint","")
        if "\\(" in h or "<" in h:
            hintbad.append((tier,i,h))
        for j,st in enumerate(prob.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                boxbad.append((f"{tier}[{i}].guided_steps[{j}]",st["answer"]))
print("HINT non-plain:", len(hintbad), hintbad)
print("NON-NUMERIC boxes:", boxbad)

# tier sizes
print("tier sizes: bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
# pre tier sizes
if prepd.get("problem_bank"):
    ppb=prepd["problem_bank"]
    print("pre tier sizes: bronze", len(ppb.get("bronze",[])), "silver", len(ppb.get("silver",[])), "gold", len(ppb.get("gold",[])))

# check every misconception expect against solution presence
print("\n--- MISCONCEPTIONS ---")
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        sol=prob.get("solutions")
        for m in prob.get("misconceptions",[]):
            print(f"{tier}[{i}] sol={sol} expect={m.get('expect')} pat={m.get('pattern')}")
