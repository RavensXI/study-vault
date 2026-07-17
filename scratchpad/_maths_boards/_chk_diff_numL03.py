import json
pre = json.load(open("_pre_numL03_pd.json",encoding="utf-8"))
live = json.load(open("_live_ocr_numberL03.json",encoding="utf-8"))
print("PRE keys:", sorted(pre.keys()))
print("LIVE keys:", sorted(live.keys()))
for f in ("related_videos","topic_links","worked_examples"):
    same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED:", same)
    if not same:
        print("  PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
# Also check pre problem_bank displays/solutions to see if solutions changed
prpb = pre.get("problem_bank",{})
lvpb = live.get("problem_bank",{})
for tier in ("bronze","silver","gold"):
    pr=prpb.get(tier,[]); lv=lvpb.get(tier,[])
    print(f"--- {tier}: pre {len(pr)} vs live {len(lv)}")
    for i in range(max(len(pr),len(lv))):
        pd=pr[i] if i<len(pr) else {}
        ld=lv[i] if i<len(lv) else {}
        if pd.get("display")!=ld.get("display") or pd.get("solutions")!=ld.get("solutions"):
            print(f"  [{i}] DISP pre={pd.get('display')} sol={pd.get('solutions')}")
            print(f"       DISP liv={ld.get('display')} sol={ld.get('solutions')}")
