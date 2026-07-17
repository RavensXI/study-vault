import json, re
ID = "96f5aef3-e4c8-4faf-ba82-1d587dc4e10e"
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
live = json.load(open("_live_graphsL02.json", encoding="utf-8"))["practice_data"]
entry = next(r for r in pre if r["id"]==ID)
pb_pre = entry["practice_data"]["problem_bank"]
pb_live = live["problem_bank"]

def strip_svg(s):
    return re.sub(r"<svg.*?</svg>", "[svg]", s or "", flags=re.S)

for tier in ["bronze","silver","gold"]:
    pre_t = pb_pre.get(tier, [])
    live_t = pb_live.get(tier, [])
    print(f"=== {tier}: pre {len(pre_t)} live {len(live_t)}")
    for i in range(max(len(pre_t),len(live_t))):
        p = pre_t[i] if i<len(pre_t) else {}
        l = live_t[i] if i<len(live_t) else {}
        dp, dl = strip_svg(p.get("display")), strip_svg(l.get("display"))
        sp, sl = p.get("solutions"), l.get("solutions")
        if dp!=dl or sp!=sl:
            print(f"  [{i}] DISPLAY {'diff' if dp!=dl else 'same'} | SOL pre={sp} live={sl}")
            if dp!=dl:
                print("     PRE :", dp[:200])
                print("     LIVE:", dl[:200])
