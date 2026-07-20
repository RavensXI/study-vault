import json,io,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pd=json.load(open("_u12_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
print(type(pb), list(pb.keys()) if isinstance(pb,dict) else len(pb))
for tier in pb:
    print("="*20, tier)
    for i,p in enumerate(pb[tier]):
        print("-"*10, tier, i, "keys:", list(p.keys()))
        print("  type:", p.get("type"))
        print("  Q:", p.get("question"))
        if p.get("options"): print("  options:", p["options"])
        print("  answer:", p.get("answer"), "| solution:", str(p.get("solution"))[:200])
        for k in ("hint","instruction","prompt","stimulus","image","unit","context","display"):
            if k in p: print(f"  {k}:", str(p[k])[:300])
