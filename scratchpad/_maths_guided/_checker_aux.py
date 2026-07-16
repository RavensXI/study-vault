import json
# audit findings for this lesson
key_candidates = ["algebra-L02","algebra-l02","algebra/2"]
aud = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_audit_result.json",encoding="utf-8"))
def scan(obj, kws):
    hits=[]
    def rec(o,path):
        if isinstance(o,dict):
            for k,v in o.items(): rec(v,path+"."+k)
        elif isinstance(o,list):
            for i,v in enumerate(o): rec(v,f"{path}[{i}]")
        else:
            s=str(o)
            if any(kw.lower() in s.lower() for kw in kws): hits.append((path,s))
    rec(obj,"")
    return hits
print("=== AUDIT keys ===", list(aud.keys()) if isinstance(aud,dict) else type(aud))
for sec in ["issues","unconfirmed"]:
    if isinstance(aud,dict) and sec in aud:
        print(f"--- {sec} entries mentioning L02 ---")
        for e in aud[sec]:
            es=json.dumps(e)
            if "L02" in es or "algebra/2" in es or "1c2aa03c" in es or ("algebra" in es and '"2"' in es):
                print(json.dumps(e,ensure_ascii=False))
