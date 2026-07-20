# -*- coding: utf-8 -*-
import json,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pd=json.load(open("_u12_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
UNITS={
 ("bronze",0):"km",
 ("bronze",2):"km",
 ("bronze",5):"km",
 ("bronze",7):"km",
 ("silver",0):"km",
 ("silver",1):"km",
 ("silver",3):"m",
 ("silver",6):"m",
 ("gold",1):"km",
 ("gold",2):"km",
 ("gold",4):"km",
}
n=0
for (tier,i),u in UNITS.items():
    p=pb[tier][i]
    assert p.get("input_type")=="single_value", (tier,i)
    assert "unit" not in p
    p["unit"]=u
    n+=1
# sanity: no MC got a unit
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice":
            assert "unit" not in p
json.dump(pd, open("lesson_L12.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("units added:",n)
