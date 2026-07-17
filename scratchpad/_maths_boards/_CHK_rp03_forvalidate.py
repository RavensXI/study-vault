import json
live = json.load(open("_CHK_rp03_live.json", encoding="utf-8"))
json.dump(live["practice_data"], open("_CHK_rp03_pd.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

# diff method_card and problem_bank displays/solutions vs pre
ID = "689bc7ff-0d4c-4f20-a83c-9476935f2ac9"
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id")==ID: entry=r; break
ppd = entry.get("practice_data", entry)
print("=== method_card pre vs live ===")
print("PRE :", json.dumps(ppd.get("method_card"), ensure_ascii=False)[:300])
print("LIVE:", json.dumps(live["practice_data"].get("method_card"), ensure_ascii=False)[:300])
print("\n=== problem_bank display/solutions pre vs live ===")
for tier in ["bronze","silver","gold"]:
    pb_pre = ppd.get("problem_bank",{}).get(tier,[])
    pb_live = live["practice_data"]["problem_bank"][tier]
    print(f"-- {tier}: pre {len(pb_pre)} live {len(pb_live)}")
    for i in range(max(len(pb_pre),len(pb_live))):
        sp = pb_pre[i]["solutions"] if i<len(pb_pre) else "MISSING"
        sl = pb_live[i]["solutions"] if i<len(pb_live) else "MISSING"
        dp = (pb_pre[i]["display"] if i<len(pb_pre) else "")
        dl = (pb_live[i]["display"] if i<len(pb_live) else "")
        # strip svg for compare
        import re
        dp2 = re.sub(r'<svg.*?</svg>','[SVG]',dp,flags=re.S)
        dl2 = re.sub(r'<svg.*?</svg>','[SVG]',dl,flags=re.S)
        flag = "" if (sp==sl and dp2==dl2) else "  <-- CHANGED"
        print(f"   [{i}] sol {sp} -> {sl}{flag}")
        if flag:
            print("       PRE :", dp2[:120])
            print("       LIVE:", dl2[:120])
