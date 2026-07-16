import json
live = json.load(open("_CHK_geomL08_live.json", encoding="utf-8"))
pre = json.load(open("_CHK_geomL08_predump.json", encoding="utf-8"))

def norm(o): return json.dumps(o, sort_keys=True, ensure_ascii=False)

for k in ["related_videos","topic_links","worked_examples","method_card"]:
    same = norm(live.get(k))==norm(pre.get(k))
    print(f"{k}: {'UNCHANGED' if same else 'CHANGED'}")

# Compare problem displays/solutions/input_type per tier
for tier in ["bronze","silver","gold"]:
    lp = live["problem_bank"].get(tier,[])
    pp = pre["problem_bank"].get(tier,[])
    print(f"\n=== {tier}: live {len(lp)} pre {len(pp)} ===")
    for i in range(max(len(lp),len(pp))):
        l = lp[i] if i<len(lp) else {}
        p = pp[i] if i<len(pp) else {}
        d_same = l.get("display")==p.get("display")
        s_same = norm(l.get("solutions"))==norm(p.get("solutions"))
        it_same = l.get("input_type")==p.get("input_type")
        flag = "" if (d_same and s_same and it_same) else "  <<< DIFF"
        print(f" [{i}] disp={'=' if d_same else 'X'} sol={'=' if s_same else 'X'} it={'=' if it_same else 'X'}{flag}")
        if not d_same:
            print(f"     PRE : {p.get('display')}")
            print(f"     LIVE: {l.get('display')}")
        if not s_same:
            print(f"     PRE sol : {p.get('solutions')}  LIVE sol: {l.get('solutions')}")
