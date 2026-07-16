import json
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
dump=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
# figure structure
if isinstance(dump,list):
    entry=[e for e in dump if e.get('id')==ID]
    entry=entry[0] if entry else None
elif isinstance(dump,dict):
    entry=dump.get(ID)
    if entry is None:
        # maybe keyed by something else; search values
        for k,v in dump.items():
            if isinstance(v,dict) and v.get('id')==ID:
                entry=v; break
print("found:", entry is not None)
if entry:
    pd = entry.get('practice_data', entry)
    json.dump(pd, open('_pre_ratio_L01.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
    print("pre keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
