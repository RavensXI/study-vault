import json
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad"
pre = json.load(open(base + r"\_geo_audit\_pre_dump_all.json", encoding="utf-8"))
print(type(pre))
if isinstance(pre, dict):
    ks = list(pre.keys())
    print(ks[:5], len(ks))
    ent = pre.get("2aeee60b-5e2f-4781-8455-e81739317bf9")
    if ent is None:
        # search
        for k, v in pre.items():
            s = json.dumps(v)[:200]
            print(k, s[:120])
            break
    else:
        json.dump(ent, open(base + r"\_geo_guided\_CHK_L09_pre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote pre", list(ent.keys())[:10])
else:
    print(len(pre))
    for e in pre:
        if isinstance(e, dict) and e.get("id") == "2aeee60b-5e2f-4781-8455-e81739317bf9":
            json.dump(e, open(base + r"\_geo_guided\_CHK_L09_pre.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("wrote pre", list(e.keys()))
