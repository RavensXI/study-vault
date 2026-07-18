import json
with open("_live_48cb4395.json",encoding="utf-8") as f:
    pd=json.load(f)
json.dump(pd,open("_live_canonical_wrapped.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
