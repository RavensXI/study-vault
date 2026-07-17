import json
ID = "4fd08300-e0fe-44c5-93cd-76b6d900c72d"
predump = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
print("type", type(predump))
if isinstance(predump, dict):
    print("top keys sample", list(predump.keys())[:5])
    # maybe keyed by id or by lesson key
    entry = None
    if ID in predump:
        entry = predump[ID]
    elif "number-L05" in predump:
        entry = predump["number-L05"]
    else:
        for k,v in predump.items():
            if isinstance(v,dict) and (v.get("id")==ID):
                entry=v; print("found by id under",k); break
    if entry is None:
        print("NOT FOUND directly; dumping structure")
        for k in list(predump.keys())[:20]:
            print(k, type(predump[k]))
    else:
        pd = entry.get("practice_data", entry)
        json.dump(pd, open("_CHKR_L05_pd.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
        print("saved predump pd; keys", list(pd.keys()))
elif isinstance(predump, list):
    for e in predump:
        if e.get("id")==ID:
            pd=e["practice_data"]
            json.dump(pd, open("_CHKR_L05_pd.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
            print("saved from list; keys", list(pd.keys()))
            break
