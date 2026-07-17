import json
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_chk_live_numL01.json", encoding="utf-8"))
SID = "06eb8087-b07f-4bfa-8bc2-af97e3e06ebf"
row = None
for r in pre:
    if r.get("id") == SID:
        row = r; break
if row is None:
    print("row keys of first:", list(pre[0].keys()))
    print("NOT FOUND by id")
else:
    pd = row.get("practice_data") or row
    print("pre keys:", list(pd.keys()))
    for f in ["related_videos","worked_examples","topic_links"]:
        same = json.dumps(pd.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f))[:400])
            print("  NOW:", json.dumps(live.get(f))[:400])
    prepb = pd.get("problem_bank", {})
    for tier in ["bronze","silver","gold"]:
        pretier = prepb.get(tier,[])
        for i,p in enumerate(live["problem_bank"][tier]):
            pp = pretier[i] if i < len(pretier) else {}
            ds = pp.get("display")==p.get("display")
            ss = pp.get("solutions")==p.get("solutions")
            if not ds or not ss:
                print(f"{tier}[{i}] disp_same={ds} sol_same={ss} preDisp={pp.get('display')!r} preSol={pp.get('solutions')} nowDisp={p.get('display')!r} nowSol={p.get('solutions')}")
        print(f"{tier}: pre_count={len(pretier)} now_count={len(live['problem_bank'][tier])}")
