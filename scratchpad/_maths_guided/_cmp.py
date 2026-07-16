import json
ID="68997180-8486-4551-ab42-0a1b98384336"
live=json.load(open("_live_L01.json",encoding="utf-8"))
# find key in worklist
wl=json.load(open("_worklist.json",encoding="utf-8"))
def find(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if v==ID or (isinstance(v,str) and ID in str(v)): return o
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for x in o:
            r=find(x)
            if r: return r
    return None
print("WORKLIST ENTRY:", json.dumps(find(wl)))
