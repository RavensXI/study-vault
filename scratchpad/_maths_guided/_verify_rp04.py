# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open("lesson_ratio-proportion-L04.json",encoding="utf-8"))
src=json.load(io.open("_RP_L04_predump_entry.json",encoding="utf-8"))["practice_data"]
errs=[]

# 1. Fresh-solve every bank problem (independent), compare to stored solution & expects
def approx(a,b): return abs(float(a)-float(b))<1e-9
# hand-derived correct answers keyed by display substring
checks={
 "3 pizzas":35,"8 litres of fuel":60,"6 identical bars":1500,"6 pancakes":300,
 "2 workers take 8 hours":4,"3 pumps empty":6,"12 sweets":3,"3 taps fill":9,
 "x = 3\), \(y = 15":35,"x = 4\), \(y = 6\). Find \(y\) when \(x = 8":3,
 "8 identical tiles":4200,"journey takes 6 hours at 40":4,
 "x = 6\), \(y = 21":14,"x = 3\), \(y = 12\). Find \(x\) when \(y = 4":9,
 "12 workers finish a job in 8 days":16,
 "x = 5\), \(y = 8":20,"gear with 20 teeth":100,"12 workers 15 days":15,
 "x = 2\), \(y = 18":3,"x = 8\), \(y = 6\). Find \(x\) when \(y = 12":16,
}
# expected misconception values (committed error), None => must be null
expmis={
 "3 pizzas":7,"8 litres":12,"6 identical bars":150,"6 pancakes":30,
 "2 workers take 8 hours":16,"3 pumps empty":54,"12 sweets":0.15,"3 taps fill":25,
 "x = 3\), \(y = 15":19,"y = 6\). Find \(y\) when \(x = 8":12,"8 identical tiles":300,
 "journey takes 6 hours at 40":9,"y = 21":171.5,"y = 12\). Find \(x\) when \(y = 4":1,
 "12 workers finish a job in 8 days":9,
 "x = 5\), \(y = 8":None,"gear with 20 teeth":225,"12 workers 15 days":22.5,
 "y = 18":108,"y = 6\). Find \(x\) when \(y = 12":9,
}
for tier in ("bronze","silver","gold"):
    for p in pd["problem_bank"][tier]:
        d=p["display"]
        # match a check key
        key=[k for k in checks if k in d]
        if not key: errs.append("no check key for: "+d[:50]); continue
        exp=checks[key[0]]
        if not approx(p["solutions"][0],exp):
            errs.append("SOLN %s stored %s != hand %s"%(d[:40],p["solutions"],exp))
        # misconception expect
        mk=[k for k in expmis if k in d]
        want=expmis[mk[0]] if mk else "??"
        got=p["misconceptions"][0]["expect"]
        if want is None:
            if got is not None: errs.append("MISC %s expect should be null, is %s"%(d[:40],got))
        elif want=="??":
            errs.append("no expmis key for "+d[:40])
        else:
            if got is None or not approx(got,want):
                errs.append("MISC %s expect stored %s != hand %s"%(d[:40],got,want))
        # last guided box lands on solution
        boxes=[s for s in p["guided_steps"] if s.get("answer") is not None]
        # continuity already asserted at build; re-check final answer-of-interest present
        vals=[b["answer"] for b in boxes]
        if p["solutions"][0] not in vals:
            errs.append("WALK %s solution %s not among boxes %s"%(d[:40],p["solutions"][0],vals))

# 2. opener boxes
op=pd["guided"]["opener"]["steps"]
if op[0]["answer"]!=24: errs.append("opener box0 !=24")
if op[1]["answer"]!=3: errs.append("opener box1 !=3")
# 6 cakes £12 -> 12 cakes £24 (double); 4 builders 6 days -> 8 builders 3 days (half). OK.

# 3. teach walks recompute
tb=pd["guided"]["teach"]["bronze"]["steps"]
assert [s["answer"] for s in tb if s.get("answer") is not None]==[2.5,25,8,15], "teach bronze"
ts=pd["guided"]["teach"]["silver"]["steps"]
assert [s["answer"] for s in ts if s.get("answer") is not None]==[2.5,15,8,10], "teach silver"
tg=pd["guided"]["teach"]["gold"]["steps"]
assert [s["answer"] for s in tg if s.get("answer") is not None]==[24,4,24,12], "teach gold"
# verify teach maths: bronze 15/6=2.5, 2.5*10=25, 20/2.5=8, 2.5*6=15 OK
# silver 10/4=2.5, 2.5*6=15, 20/2.5=8, 2.5*4=10 OK
# gold 3*8=24, 24/6=4, 4*6=24, 24/2=12 OK

# 4. preservation vs pre-dump
if pd["related_videos"]!=src["related_videos"]: errs.append("related_videos changed")
if pd["topic_links"]!=src["topic_links"]: errs.append("topic_links changed")
if pd["method_card"]!=src["method_card"]: errs.append("method_card changed")
# worked_examples: only em-dash->colon in labels; questions must be identical
for a,b in zip(pd["worked_examples"],src["worked_examples"]):
    if a["question"]!=b["question"]: errs.append("worked_example question changed: "+b["question"][:30])
    for sa,sb in zip(a["steps"],b["steps"]):
        if sa["content"]!=sb["content"]: errs.append("we content changed")
# topic identity: method_card title must be proportion, not substitution
if "Proportion" not in pd["method_card"]["title"]: errs.append("method_card wrong topic")
if "substitut" in json.dumps(pd["problem_bank"]).lower(): errs.append("substitution leaked into bank")

print("VERIFY:", "ALL CLEAN" if not errs else "PROBLEMS:")
for e in errs: print("  -",e)
