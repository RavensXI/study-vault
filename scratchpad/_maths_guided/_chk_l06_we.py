# -*- coding: utf-8 -*-
import json
live=json.load(open("_CHK_L06_live.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="62194f78-5bda-4cdb-81db-015760b58c7a"
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
pre=find(dump)["practice_data"]
with open("_we_pre_L06.json","w",encoding="utf-8") as f:
    json.dump(pre.get("worked_examples"),f,ensure_ascii=False,indent=2)
with open("_we_live_L06.json","w",encoding="utf-8") as f:
    json.dump(live.get("worked_examples"),f,ensure_ascii=False,indent=2)
# also method_card pre
with open("_mc_pre_L06.json","w",encoding="utf-8") as f:
    json.dump(pre.get("method_card"),f,ensure_ascii=False,indent=2)
print("pre keys:", list(pre.keys()))
print("wrote files")
