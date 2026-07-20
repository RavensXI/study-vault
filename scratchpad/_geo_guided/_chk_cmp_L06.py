import io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
import json
pre=json.load(open("_chk_pre_L06.json",encoding="utf-8"))["pd"]
live=json.load(open("_CHK_L06_live.json",encoding="utf-8"))
print("pre keys",list(pre.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    print(f,"identical:", json.dumps(pre.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True))
print("method_card pre:", json.dumps(pre.get("method_card"),ensure_ascii=False)[:1500])
print()
print("method_card live:", json.dumps(live.get("method_card"),ensure_ascii=False)[:1500])
pb0=pre["problem_bank"]; pb1=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    print("==",t,len(pb0[t]),len(pb1[t]))
    for i,(a,b) in enumerate(zip(pb0[t],pb1[t])):
        d=[]
        if a.get("display")!=b.get("display"): d.append("DISPLAY")
        if a.get("solutions")!=b.get("solutions"): d.append(f"SOL {a.get('solutions')} -> {b.get('solutions')}")
        if a.get("options")!=b.get("options"): d.append(f"OPTIONS {a.get('options')} -> {b.get('options')}")
        if json.dumps(a.get("chart"),sort_keys=True)!=json.dumps(b.get("chart"),sort_keys=True): d.append("CHART")
        if a.get("image")!=b.get("image"): d.append(f"IMAGE {a.get('image')} -> {b.get('image')}")
        if a.get("ruler")!=b.get("ruler"): d.append("RULER")
        if a.get("input_type")!=b.get("input_type"): d.append("INPUT")
        if d: print(" ",t,i,d)
        if "DISPLAY" in d:
            print("    pre :",a.get("display"))
            print("    live:",b.get("display"))
