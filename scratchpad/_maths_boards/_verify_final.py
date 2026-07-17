import json,io
live=json.load(io.open("_live_algebra-L03.json",encoding="utf-8"))
pd=json.load(io.open("lesson_maths-aqa_algebra-L03.json",encoding="utf-8"))
ok=True
# 1 expects never equal correct (0) and in range
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        for m in p.get("misconceptions",[]):
            e=m["expect"]
            if e==0 or e not in (1,2,3): ok=False;print("BAD expect",t,i,e)
# 2 opener boxes recompute
op=pd["guided"]["opener"]["steps"]
assert op[0]["answer"]==2+5 and op[1]["answer"]==3*7, "opener"
# 3 teach recompute
tb=pd["guided"]["teach"]["bronze"]["steps"]
assert [s.get("answer") for s in tb if "answer" in s]==[3,2,5,21,21]
ts=pd["guided"]["teach"]["silver"]["steps"]
assert [s.get("answer") for s in ts if "answer" in s]==[15,8,15,8,24,24]
tg=pd["guided"]["teach"]["gold"]["steps"]
assert [s.get("answer") for s in tg if "answer" in s]==[3,4,-7,-7]
# verify teach maths: 6x+15=3(2x+5); x=1 ->3*7=21, 6+15=21 ✓
# x^2+8x+15=(x+3)(x+5); x=1 ->4*6=24, 1+8+15=24 ✓
# 9x^2-16=(3x+4)(3x-4); x=1 ->7*-1=-7, 9-16=-7 ✓
# 4 preservation
assert pd["related_videos"]==live["related_videos"], "related_videos changed"
assert pd["topic_links"]==live["topic_links"], "topic_links changed"
assert pd["worked_examples"]==live["worked_examples"], "worked_examples changed"
assert pd["method_card"]["title"]==live["method_card"]["title"]
assert pd["method_card"]["example"]==live["method_card"]["example"]
# problem displays/options/solutions unchanged
for t in ("bronze","silver","gold"):
    for i,(a,b) in enumerate(zip(pd["problem_bank"][t],live["problem_bank"][t])):
        assert a["display"]==b["display"], (t,i,"display")
        assert a.get("options")==b.get("options"), (t,i,"options")
        assert a["solutions"]==b["solutions"], (t,i,"sol")
print("expects ok, boxes recompute, teach maths verified, preservation intact:",ok)
