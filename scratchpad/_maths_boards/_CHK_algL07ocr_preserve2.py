import json
ID="90c8606a-f24d-4140-91ff-20adf463a3f0"
live=json.load(open("_CHK_algL07ocr_live.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=[e for e in pre if e.get('id')==ID][0]
ppd=entry['practice_data']
print("PRE keys:", sorted(ppd.keys()))
print("LIVE keys:", sorted(live.keys()))
# Preservation targets
for f in ['related_videos','topic_links','worked_examples','method_card']:
    same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}  (pre-present={f in ppd})")
# Show pre worked_examples/method_card if changed
import difflib
for f in ['worked_examples','method_card','topic_links']:
    if json.dumps(ppd.get(f),sort_keys=True)!=json.dumps(live.get(f),sort_keys=True):
        print(f"--- {f} PRE ---"); print(json.dumps(ppd.get(f),indent=1,ensure_ascii=False)[:1500])
# Check pre problem count vs live (were problems added/removed?)
for tier in ['gold','bronze','silver']:
    pb_pre=ppd.get('problem_bank',{}).get(tier,[])
    pb_live=live.get('problem_bank',{}).get(tier,[])
    print(f"{tier}: pre={len(pb_pre)} live={len(pb_live)}")
    # compare displays & solutions
    for i in range(max(len(pb_pre),len(pb_live))):
        dp=pb_pre[i]['display'] if i<len(pb_pre) else None
        sp=pb_pre[i].get('solutions') if i<len(pb_pre) else None
        dl=pb_live[i]['display'] if i<len(pb_live) else None
        sl=pb_live[i].get('solutions') if i<len(pb_live) else None
        if dp!=dl or sp!=sl:
            print(f"  [{i}] DISPLAY/SOL CHANGED pre=({dp},{sp}) live=({dl},{sl})")
