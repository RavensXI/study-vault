import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    probs=pb[tier]
    print(f"=== {tier} ({len(probs)} problems) ===")
    for i,p in enumerate(probs):
        disp=p.get("display","")
        has_svg="<svg" in disp
        has_chart="chart" in p
        marker=("[SVG]" if has_svg else "")+("[CHART]" if has_chart else "")
        print(f"  {tier}[{i}] {marker} sol={p.get('solutions')} input={p.get('input_type')}")
        txt=re.sub(r'<svg.*?</svg>','[SVG]',disp,flags=re.S)
        print("     disp:", txt[:300])
