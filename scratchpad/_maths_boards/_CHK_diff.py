import json
pre=json.load(open("_CHK_pre_graphsL03.json",encoding="utf-8"))
live=json.load(open("_CHK_graphsL03_LIVE.json",encoding="utf-8"))
for f in ["related_videos","topic_links","worked_examples"]:
    same = pre.get(f)==live.get(f)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
print("--- method_card ---")
print(" same:", pre.get("method_card")==live.get("method_card"))
# problem bank displays/solutions
pb_pre=pre["problem_bank"]; pb_live=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    ap=pb_pre.get(t,[]); al=pb_live.get(t,[])
    print(f"=== {t}: pre {len(ap)} live {len(al)} ===")
    for i in range(max(len(ap),len(al))):
        p=ap[i] if i<len(ap) else {}
        l=al[i] if i<len(al) else {}
        dp=p.get("display"); dl=l.get("display")
        sp=p.get("solutions"); sl=l.get("solutions")
        flag=""
        if dp!=dl: flag+=" DISPLAY-CHANGED"
        if sp!=sl: flag+=" SOL-CHANGED"
        if flag:
            print(f" [{i}]{flag}")
            if dp!=dl:
                print("    preD:",dp)
                print("    livD:",dl)
            if sp!=sl:
                print("    preS:",sp," livS:",sl)
        else:
            print(f" [{i}] ok  sol={sl}  {dl[:60] if dl else ''}")
