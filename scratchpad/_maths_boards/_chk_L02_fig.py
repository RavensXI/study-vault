import json,io,sys,re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
# any chart or svg in problems?
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("chart"): print(f"{tier}[{i}] HAS chart")
        if "<svg" in (p.get("display") or ""): print(f"{tier}[{i}] HAS svg")
        # figure-claim words in display
        d=(p.get("display") or "").lower()
        if any(w in d for w in ["triangle","diagram","chart","graph","shown","shape","picture"]):
            print(f"{tier}[{i}] figure-claim words: {p.get('display')}")
print("Problem figures: none above = clean (fractions is textual)")
# opener svg only
print("opener has svg:", "<svg" in pd["guided"]["opener"]["display"])
