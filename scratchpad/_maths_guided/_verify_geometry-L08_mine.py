import json, io
live=json.load(io.open("_live_geometry_L08.json",encoding="utf-8"))
new=json.load(io.open("lesson_geometry-L08.json",encoding="utf-8"))

# 1. Preservation: related_videos identical; topic_links identical
assert live["related_videos"]==new["related_videos"], "related_videos changed!"
assert live["topic_links"]==new["topic_links"], "topic_links changed!"
# worked_examples: identical except em-dash->colon in two labels
lwe=json.dumps(live["worked_examples"],ensure_ascii=False).replace("—",":").replace(" : "," :")
# simpler: compare after replacing em dash with colon variants
def norm(s): return s.replace("Step 1 — Find AB","Step 1: Find AB").replace("Step 2 — Midpoint","Step 2: Midpoint")
assert norm(json.dumps(live["worked_examples"],ensure_ascii=False))==json.dumps(new["worked_examples"],ensure_ascii=False), "worked_examples differ beyond em-dash fix"
print("PRESERVATION OK (related_videos, topic_links, worked_examples[em-dash only])")

# 2. Final-box lands on solution for single_value/fraction; check no em dash
def last_boxes(gs):
    return [s for s in gs if s.get("answer") is not None]

pb=new["problem_bank"]
report=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps",[])
        boxes=last_boxes(gs)
        finals=[b["answer"] for b in boxes]
        sol=p["solutions"]
        # the solution value(s) must appear among box answers
        ok=all(any(abs(float(s)-float(fa))<0.011 for fa in finals) for s in sol)
        report.append((tier,i,sol,finals[-3:],ok))
for r in report:
    print(r)
bad=[r for r in report if not r[4]]
print("PROBLEMS WHERE SOLUTION NOT REACHED BY ANY BOX:", bad)
