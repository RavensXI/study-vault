# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
d = json.load(open("_L05rp_live.json", encoding="utf-8"))
print("=== method_card ==="); print(json.dumps(d.get("method_card"), indent=1, ensure_ascii=False))
print("=== topic_links ==="); print(json.dumps(d.get("topic_links"), ensure_ascii=False))
print("=== related_videos ==="); print(json.dumps(d.get("related_videos"), ensure_ascii=False))
we = d.get("worked_examples")
print("=== worked_examples ==="); print(type(we), len(we) if isinstance(we, list) else "")
print(json.dumps(we, ensure_ascii=False)[:1200] if we else "none")
print("=== sample bronze[0] full ==="); print(json.dumps(d["problem_bank"]["bronze"][0], indent=1, ensure_ascii=False))
print("=== has guided/tier_guides? ==="); print("guided" in d, "tier_guides" in d)
pb = d["problem_bank"]
print("tier_descriptions:", {t: pb.get(t+"_description") for t in ["bronze","silver","gold"]})
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        keys=[k for k in p.keys() if k not in ("display","solutions","input_type","calculator")]
        if keys: print(t,i,"extra keys:",keys)
