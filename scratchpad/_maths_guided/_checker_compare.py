import json
ID="a43f9613-dd40-45e2-b692-00ac9c01fb92"
raw=json.load(open("_live_L04.json",encoding="utf-8"))
def unwrap(x):
    while isinstance(x,list): x=x[0]
    if isinstance(x,dict) and "practice_data" in x: return x["practice_data"]
    return x
live=unwrap(raw)
print("live keys:", list(live.keys()))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
print("dump type:", type(dump).__name__)
if isinstance(dump,dict): print("dump top keys sample:", list(dump.keys())[:5])
if isinstance(dump,list): print("dump len:", len(dump), "sample keys:", list(dump[0].keys())[:10] if dump else None)
