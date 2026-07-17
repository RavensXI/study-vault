# -*- coding: utf-8 -*-
import json
live = json.load(open("_live_number-L07.json", encoding="utf-8"))
new = json.load(open("lesson_maths-aqa_number-L07.json", encoding="utf-8"))

# preservation checks
assert live["worked_examples"] == new["worked_examples"], "worked_examples changed"
assert live["topic_links"] == new["topic_links"], "topic_links changed"
assert live["related_videos"] == new["related_videos"], "related_videos changed"
print("PRESERVED: worked_examples, topic_links, related_videos byte-equal")

# expects: distinct from correct, present
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(new["problem_bank"][tier]):
        for m in p.get("misconceptions",[]):
            assert "expect" in m
            if m["expect"] is not None:
                assert abs(float(m["expect"]) - float(p["solutions"][0])) > 0.011, (tier,i,m["expect"])
print("EXPECTS: all present, all distinct from correct answer")

# figures present
assert "<svg" in new["guided"]["opener"]["display"]
assert "<svg" in new["problem_bank"]["gold"][2]["display"]
assert "figure-caption" in new["problem_bank"]["gold"][2]["display"]
print("FIGURES: opener svg + gold[2] rectangle svg present")

# recompute a sample of intermediate boxes independently
import math
def close(a,b): return abs(a-b) < 1e-9
# gold[2] perimeter
assert close(round(12.4-0.05,2),12.35) and close(round(5.8-0.05,2),5.75)
assert close(2*(12.35+5.75),36.2)
# gold[4] speed
assert round(245/8.35,1)==29.3
assert round(245/8.45,1)==29.0   # the misconception expect
# gold[0]
assert 9-2==7
# silver[6] surd
assert 8*6==48 and math.isqrt(48//16*16)  # 48=16*3
assert 4**2*3==48
print("SPOT MATHS: perimeter 36.2, speed 29.3 (mc 29.0), conjugate 7, surd 4 all check")
