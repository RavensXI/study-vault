import json
ID="d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
live=json.load(open("_live_L03.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
entry=[e for e in dump if e.get("id")==ID][0]
pre=entry["practice_data"]
print("PRE keys:", sorted(pre.keys()))
print("LIVE keys:", sorted(live.keys()))
# Preservation-critical fields per spec section 9
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if a==b else 'CHANGED'}")
# problem counts + displays + solutions preserved?
for tier in ["bronze","silver","gold"]:
    pb_pre=pre.get("problem_bank",{}).get(tier,[])
    pb_live=live.get("problem_bank",{}).get(tier,[])
    print(f"\n{tier}: pre={len(pb_pre)} live={len(pb_live)}")
    for i in range(max(len(pb_pre),len(pb_live))):
        pp=pb_pre[i] if i<len(pb_pre) else {}
        pl=pb_live[i] if i<len(pb_live) else {}
        ds_pre=pp.get("display",""); ds_live=pl.get("display","")
        sol_pre=pp.get("solutions"); sol_live=pl.get("solutions")
        # strip svg for display compare
        import re
        d_pre=re.sub(r'<svg.*?</svg>','[SVG]',ds_pre,flags=re.S).strip()
        d_live=re.sub(r'<svg.*?</svg>','[SVG]',ds_live,flags=re.S).strip()
        flag=""
        if sol_pre!=sol_live: flag+=f" SOL {sol_pre}->{sol_live}"
        if d_pre!=d_live: flag+=f" DISPLAY-TEXT-CHANGED"
        print(f"  [{i}] sol_pre={sol_pre} sol_live={sol_live}{flag}")
        if d_pre!=d_live:
            print(f"       PRE : {d_pre[:120]}")
            print(f"       LIVE: {d_live[:120]}")
