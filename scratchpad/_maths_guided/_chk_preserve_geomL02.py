import json
LID="fe5f6191-4452-4313-934d-8e5d16ba1032"
KEY="geometry-L02"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# pre_fanout_dump structure?
print("type", type(pre))
if isinstance(pre,dict):
    print("keys sample", list(pre.keys())[:5])
