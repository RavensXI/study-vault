import json, re

LID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_VER_live_pd.json", encoding="utf-8"))
entry = None
if isinstance(pre, dict):
    entry = pre.get(LID)
else:
    for r in pre:
        if r.get("id") == LID:
            entry = r
            break
ppd = entry.get("practice_data", entry)

def strip_svg(s):
    if not isinstance(s, str): return s
    return re.sub(r'<svg.*?</svg>', '[SVG]', s, flags=re.DOTALL)

for tier in ["bronze","silver","gold"]:
    pb_pre = ppd["problem_bank"].get(tier, [])
    pb_live = live["problem_bank"].get(tier, [])
    print(f"=== {tier}: pre {len(pb_pre)} / live {len(pb_live)} ===")
    for i in range(max(len(pb_pre), len(pb_live))):
        pp = pb_pre[i] if i < len(pb_pre) else {}
        lp = pb_live[i] if i < len(pb_live) else {}
        dpre = strip_svg(pp.get("display",""))
        dlive = strip_svg(lp.get("display",""))
        # extract just the text portion after any [SVG] or div
        def txt(d):
            d = re.sub(r'<[^>]+>','',d).replace('[SVG]','').strip()
            return d
        tp, tl = txt(dpre), txt(dlive)
        spre = pp.get("solutions"); sliv = lp.get("solutions")
        flag = ""
        if tp != tl: flag += " TEXT-CHANGED"
        if spre != sliv: flag += " SOL-CHANGED"
        print(f"[{i}] sol pre={spre} live={sliv}{flag}")
        if tp != tl:
            print(f"     PRE : {tp}")
            print(f"     LIVE: {tl}")
