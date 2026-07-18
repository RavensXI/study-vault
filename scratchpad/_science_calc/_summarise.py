import json, re
pd=json.load(open("_mine330_b2dd6adb.json",encoding="utf-8"))
def strip(s):
    s=re.sub(r"<svg.*?</svg>","[SVG]",s,flags=re.S)
    s=re.sub(r"<[^>]+>"," ",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s
for tier in ["bronze","silver","gold"]:
    print("="*70)
    print("TIER",tier)
    for i,p in enumerate(pd["problem_bank"][tier]):
        print(f"--- {tier}[{i}] ---")
        print("  DISPLAY:", strip(p.get("display","")))
        for k in ["input_type","solutions","unit","accept","calculator","higher_only","equation_hint","options"]:
            if k in p: print(f"  {k}: {p[k]}")
        for m in p.get("misconceptions",[]):
            print(f"  MC[{m.get('pattern')}]: {m.get('message')} | expect={m.get('expect','<none>')}")
print("="*70)
print("worked_examples count:", len(pd.get("worked_examples",[])))
for w in pd.get("worked_examples",[]):
    print("  WE", w.get("difficulty"), "|", strip(w.get("question",""))[:80])
print("related_videos:", pd.get("related_videos"))
print("topic_links:", pd.get("topic_links"))
