import json,re
live=json.load(open("_LIVE_eduqas_probstat_L02.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
ID="7f417926-0bef-4875-a7ad-7eb71bd15506"
row=[r for r in pre if r.get("id")==ID][0]
prb_pre=row["practice_data"]["problem_bank"]
prb_live=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    lp=prb_live[tier]; pp=prb_pre[tier]
    print(f"=== {tier}: pre={len(pp)} live={len(lp)}")
    for i,(a,b) in enumerate(zip(pp,lp)):
        stxt=lambda d: re.sub(r'<svg.*?</svg>','[SVG]',d.get('display',''),flags=re.S)
        if a.get('solutions')!=b.get('solutions') or stxt(a)!=stxt(b):
            print(f"  [{i}] sol pre={a.get('solutions')} live={b.get('solutions')}")
            print(f"      disp pre: {stxt(a)[:120]}")
            print(f"      disp liv: {stxt(b)[:120]}")
