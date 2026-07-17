import json
ID="9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=[e for e in pre if e.get("id")==ID][0]
ppd=entry.get("practice_data") or entry
live=json.load(open("_live_L06.json",encoding="utf-8"))
print("PRE keys:",sorted(ppd.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE:",json.dumps(ppd.get(f),ensure_ascii=False)[:400])
        print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:400])
# check method_card presence pre vs live
print("pre has method_card:", "method_card" in ppd, "| pre has problem_bank:", "problem_bank" in ppd)
# compare problem displays & solutions preserved
def bank(pd): return pd.get("problem_bank",{})
pb_pre=bank(ppd); pb_live=bank(live)
for tier in ["bronze","silver","gold"]:
    a=pb_pre.get(tier,[]); b=pb_live.get(tier,[])
    print(f"{tier}: pre {len(a)} live {len(b)}")
    for i in range(max(len(a),len(b))):
        da=a[i].get("display") if i<len(a) else None
        db=b[i].get("display") if i<len(b) else None
        sa=a[i].get("solutions") if i<len(a) else None
        sb=b[i].get("solutions") if i<len(b) else None
        flag = "" if (da==db and sa==sb) else "  <<< DIFF"
        if flag:
            print(f"  [{i}] soln pre={sa} live={sb}{flag}")
            print(f"       disp pre: {da}")
            print(f"       disp liv: {db}")
