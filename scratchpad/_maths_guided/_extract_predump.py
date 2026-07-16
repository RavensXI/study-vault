import json
LID="0b5aef96-fa58-45be-a8fe-6d63c2baf002"
# worklist
try:
    wl=json.load(open("_worklist.json",encoding="utf-8"))
    for e in (wl if isinstance(wl,list) else wl.get("lessons",wl.get("items",[]))):
        if isinstance(e,dict) and e.get("id")==LID:
            print("WORKLIST ENTRY:", json.dumps(e))
except Exception as ex:
    print("worklist err", ex)

dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# dump could be list or dict keyed by id
entry=None
if isinstance(dump,dict):
    if LID in dump: entry=dump[LID]
    else:
        for k,v in dump.items():
            if isinstance(v,dict) and v.get("id")==LID:
                entry=v; break
elif isinstance(dump,list):
    for v in dump:
        if isinstance(v,dict) and v.get("id")==LID:
            entry=v; break
print("FOUND ENTRY:", entry is not None)
if entry is not None:
    pd = entry.get("practice_data", entry)
    open("_predump_geometry-L04.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
    print("predump keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
