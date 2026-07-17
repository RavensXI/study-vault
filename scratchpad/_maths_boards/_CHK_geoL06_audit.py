import json

live = json.load(open("_CHK_geoL06_live.json", encoding="utf-8"))["practice_data"]

print("=== SAY-STEP FORMULA AUDIT ===")
pb = live["problem_bank"]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        disp = p.get("display","")
        # strip svg
        import re
        txt = re.sub(r"<svg.*?</svg>","[svg]",disp,flags=re.S)
        for j,st in enumerate(p.get("guided_steps",[])):
            say = st.get("say","")
            bad=[]
            if "\\frac{b}{\\sin A} = \\frac{b}{\\sin B}" in say: bad.append("sine b/sinA=b/sinB")
            if "a^2 = a^2 + b^2" in say: bad.append("cosine a^2=a^2+b^2")
            if bad:
                print(f"{tier}[{i}].guided_steps[{j}].say -> {bad}")
                print("   display:", txt.strip()[:90])
                print("   say:", say[:140])

# silver[1] mislabel check
print("\n=== silver[1] say ===")
print(pb["silver"][1]["guided_steps"][0]["say"])
print("display:", re.sub(r'<svg.*?</svg>','[svg]',pb['silver'][1]['display'],flags=re.S).strip())

print("\n=== PRESERVATION vs pre-dump ===")
pre_all = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# find this lesson id
ID="6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0"
pre=None
if isinstance(pre_all,list):
    for row in pre_all:
        if row.get("id")==ID: pre=row.get("practice_data"); break
elif isinstance(pre_all,dict):
    if ID in pre_all: pre=pre_all[ID]
    elif "practice_data" in pre_all: pre=pre_all["practice_data"]
    else:
        for k,v in pre_all.items():
            if isinstance(v,dict) and v.get("id")==ID: pre=v.get("practice_data")
print("pre found:", pre is not None, "| type of predump:", type(pre_all).__name__)
if isinstance(pre_all,dict): print("predump keys sample:", list(pre_all.keys())[:5])
if pre:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f"  {f}: {'UNCHANGED' if same else 'CHANGED'}")
