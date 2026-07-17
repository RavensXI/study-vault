import json, re
ID = "70586def-170c-4aa7-947b-2b961cfadec2"
live = json.load(open("_CHK_gL03_live.json", encoding="utf-8"))[0]["practice_data"]
pre_all = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
pre = None
for r in pre_all:
    if r.get("id")==ID: pre=r["practice_data"]; break

def strip_svg(s):
    if not isinstance(s,str): return s
    return re.sub(r"<svg.*?</svg>","[SVG]",s, flags=re.S).replace('<span class="figure-caption">Diagram not drawn accurately</span>','').strip()

for tier in ["bronze","silver","gold"]:
    lp = live["problem_bank"][tier]
    pp = pre["problem_bank"].get(tier, [])
    print(f"\n#### {tier}: pre={len(pp)} live={len(lp)}")
    for i in range(max(len(lp),len(pp))):
        L = lp[i] if i<len(lp) else None
        P = pp[i] if i<len(pp) else None
        ld = strip_svg(L.get("display")) if L else None
        pdd = strip_svg(P.get("display")) if P else None
        lsol = L.get("solutions") if L else None
        psol = P.get("solutions") if P else None
        dchg = ld!=pdd
        schg = lsol!=psol
        if dchg or schg:
            print(f" [{i}] DISPLAY_CHG={dchg} SOL {psol}->{lsol}")
            if dchg:
                print(f"     PRE : {pdd}")
                print(f"     LIVE: {ld}")
        else:
            print(f" [{i}] same display, sol={lsol}")
