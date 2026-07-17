# -*- coding: utf-8 -*-
import json
live = json.load(open("_RP06_live.json", encoding="utf-8"))
new = json.load(open("lesson_maths-eduqas_ratio-proportion-L06.json", encoding="utf-8"))
print("topic_links preserved:", live["topic_links"] == new["topic_links"])
print("related_videos preserved:", live["related_videos"] == new["related_videos"])
# worked_examples: identical except em-dash label repair
lw, nw = live["worked_examples"], new["worked_examples"]
same = True
for a,b in zip(lw,nw):
    if a["question"]!=b["question"] or a.get("difficulty")!=b.get("difficulty"): same=False
    for sa,sb in zip(a["steps"],b["steps"]):
        if sa.get("content")!=sb.get("content"): same=False
        la, lb = sa.get("label",""), sb.get("label","")
        if la.replace(" — ",": ").replace("—",":") != lb: same=False
print("worked_examples content preserved (labels de-dashed):", same and len(lw)==len(nw))
