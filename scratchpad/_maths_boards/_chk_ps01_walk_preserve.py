# -*- coding: utf-8 -*-
import json, re
from fractions import Fraction as F

pd = json.load(open("_CHK_ps01_LIVE.json", encoding="utf-8"))

print("=== teach walk box values ===")
for tier,walk in pd["guided"]["teach"].items():
    vals=[s.get("answer") for s in walk["steps"] if "answer" in s]
    print(tier, "boxes:", vals, "| display tail:", walk["display"].split("<br>")[-1][:70])

print("\n=== opener boxes ===")
print([s.get("answer") for s in pd["guided"]["opener"]["steps"] if "answer" in s])

# teach expected finals
# gold: 3/5 x 2/4 = 3/10 ; boxes 3,5,2,4,3
# bronze: P(yellow)=5/8 ; boxes 5,8,5,8
# silver: 2/5 x 2/5 = 4/25 ; boxes 2,5,4,25
print("gold teach final P=3/10:", F(3,5)*F(2,4)==F(3,10))
print("silver teach final P=4/25:", F(2,5)*F(2,5)==F(4,25))

print("\n=== tier_guide examples ===")
print("gold ex 2/9+2/9=4/9:", F(2,3)*F(1,3)+F(1,3)*F(2,3)==F(4,9))
print("bronze ex 4/10=2/5:", F(4,10)==F(2,5))
print("silver ex 3/5*2/4=3/10:", F(3,5)*F(2,4)==F(3,10))

# ---------- preservation vs pre-dump ----------
print("\n=== preservation vs pre-dump ===")
dump = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# find this lesson id
ID="aa2fb8d9-f47f-4412-8231-28085ce43740"
entry=None
if isinstance(dump,list):
    for row in dump:
        if row.get("id")==ID: entry=row; break
elif isinstance(dump,dict):
    entry = dump.get(ID) or dump.get("lessons",{}).get(ID)
print("found pre-dump entry:", entry is not None)
if entry:
    pre = entry.get("practice_data", entry)
    for field in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre.get(field),sort_keys=True,ensure_ascii=False)
        b=json.dumps(pd.get(field),sort_keys=True,ensure_ascii=False)
        print(f"{field}: {'UNCHANGED' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE :", a[:300])
            print("  LIVE:", b[:300])
    print("pre-dump top keys:", sorted(pre.keys()))
    print("live    top keys:", sorted(pd.keys()))
