import json

SID = "d8a78aa2-a642-4dcd-9cb0-1aa5990761e7"
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_algL01ocr_live.json", encoding="utf-8"))
dump = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-ocr.json", encoding="utf-8"))

# dump structure?
print("dump type:", type(dump))
if isinstance(dump, list):
    print("len", len(dump), "sample keys", list(dump[0].keys())[:6] if dump else None)
    entry = None
    for e in dump:
        if e.get("id")==SID:
            entry=e; break
    print("found by id:", entry is not None)
elif isinstance(dump, dict):
    print("keys sample:", list(dump.keys())[:5])
    entry = dump.get(SID)
    print("found by id key:", entry is not None)

pre = entry.get("practice_data") if entry and "practice_data" in entry else entry
if pre is None:
    print("NO PRE ENTRY")
else:
    print("\npre top keys:", list(pre.keys()))
    print("live top keys:", list(live.keys()))
    # preservation fields
    for fld in ("related_videos","topic_links","worked_examples"):
        import json as J
        same = J.dumps(pre.get(fld),sort_keys=True,ensure_ascii=False)==J.dumps(live.get(fld),sort_keys=True,ensure_ascii=False)
        print(f"{fld}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE :", J.dumps(pre.get(fld),ensure_ascii=False)[:300])
            print("  LIVE:", J.dumps(live.get(fld),ensure_ascii=False)[:300])
    # compare problem_bank displays & solutions & options (content preserved / repaired?)
    print("\n=== problem_bank display/options/solutions diff ===")
    for tier in ("bronze","silver","gold"):
        preb = pre.get("problem_bank",{}).get(tier,[])
        livb = live.get("problem_bank",{}).get(tier,[])
        print(f"-- {tier}: pre {len(preb)} live {len(livb)}")
        for i in range(max(len(preb),len(livb))):
            pp = preb[i] if i<len(preb) else None
            lp = livb[i] if i<len(livb) else None
            if pp is None or lp is None:
                print(f"  [{i}] MISSING one side"); continue
            for f in ("display","options","solutions"):
                if json.dumps(pp.get(f),ensure_ascii=False)!=json.dumps(lp.get(f),ensure_ascii=False):
                    print(f"  [{i}].{f} CHANGED")
                    print(f"     pre : {pp.get(f)}")
                    print(f"     live: {lp.get(f)}")
