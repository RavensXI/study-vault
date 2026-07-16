import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
wl=json.load(open("_worklist.json",encoding="utf-8"))
items=wl if isinstance(wl,list) else wl.get("lessons",wl.get("worklist",[]))
for it in (items if isinstance(items,list) else []):
    if isinstance(it,dict) and it.get("id")=="9f108e0c-d178-4685-8f65-1dc1a370d201":
        print(json.dumps(it,ensure_ascii=False))
