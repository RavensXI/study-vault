import json,io,re
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_gs.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
def sv(s): return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S) if isinstance(s,str) else s
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        w(f"\n===== {tier}[{i}] it={p.get('input_type')} sol={p.get('solutions')}")
        w("  DISP:",sv(p.get("display")))
        gs=p.get("guided_steps")
        if gs is None:
            w("  NO guided_steps; skip_reason:",p.get("guided_skip_reason"))
            continue
        for k,s in enumerate(gs):
            if "say" in s and "answer" not in s:
                w(f"   [{k}] SAY: {s['say']}")
            else:
                ph=f" PHASE={s['phase']}" if 'phase' in s else ""
                w(f"   [{k}] pre='{s.get('pre')}' post='{s.get('post')}' ANS={s.get('answer')}{ph} done={s.get('done')}")
out.close()
print("ok")
