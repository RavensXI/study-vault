import json
ID="90c8606a-f24d-4140-91ff-20adf463a3f0"
live=json.load(open("_CHK_algL07ocr_live.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# find entry
def find(pre):
    if isinstance(pre,dict):
        if ID in pre: return pre[ID]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get('id')==ID: return v
        # maybe list under key
    if isinstance(pre,list):
        for e in pre:
            if isinstance(e,dict) and e.get('id')==ID: return e
    return None
entry=find(pre)
print("pre-dump type:", type(pre).__name__, "top keys sample:", list(pre.keys())[:5] if isinstance(pre,dict) else len(pre))
print("entry found:", entry is not None)
if entry:
    print("entry keys:", list(entry.keys()))
