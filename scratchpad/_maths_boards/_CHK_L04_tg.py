# -*- coding: utf-8 -*-
import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
print("### TIER_GUIDES ###")
for tier,tg in pd["tier_guides"].items():
    print(f"\n--- {tier} ---")
    print(json.dumps(tg,ensure_ascii=False,indent=1))
print("\n### METHOD_CARD ###")
print(json.dumps(pd["method_card"],ensure_ascii=False,indent=1))
print("\n### topic_links, related_videos, worked_examples keys ###")
for k in ["topic_links","related_videos","worked_examples"]:
    v=pd.get(k)
    print(k,"=>",type(v).__name__, (len(v) if isinstance(v,(list,dict)) else v))
