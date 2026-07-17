import json
ID = "9e521b4c-a8d3-47d8-ac6b-1ce35dabf977"
pre = json.load(open('_pre_dump_maths-eduqas.json', encoding='utf-8'))
live = json.load(open('_chk_nL03_live.json', encoding='utf-8'))
row = [r for r in pre if r['id']==ID][0]
pd = row['practice_data']
print("PRE keys:", sorted(pd.keys()))
print("LIVE keys:", sorted(live.keys()))
# Preserve fields
for f in ['related_videos','topic_links','worked_examples']:
    same = pd.get(f) == live.get(f)
    print(f, "preserved:", same)
    if not same:
        print("  PRE :", json.dumps(pd.get(f), ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f), ensure_ascii=False)[:400])
# Compare displays & solutions of the problem bank
prepb = pd.get('problem_bank',{})
livepb = live.get('problem_bank',{})
for t in ['bronze','silver','gold']:
    pre_probs = prepb.get(t,[])
    live_probs = livepb.get(t,[])
    print(f"\n== {t}: pre {len(pre_probs)} live {len(live_probs)}")
    for i,lp in enumerate(live_probs):
        pp = pre_probs[i] if i < len(pre_probs) else {}
        dchg = pp.get('display') != lp.get('display')
        schg = pp.get('solutions') != lp.get('solutions')
        ichg = pp.get('input_type') != lp.get('input_type')
        cchg = pp.get('calculator') != lp.get('calculator')
        flag = ' <-- CHANGED' if (dchg or schg) else ''
        print(f" [{i}] disp_chg={dchg} sol_chg={schg} it_chg={ichg} calc_chg={cchg}{flag}")
        if dchg:
            print("     PRE disp:", pp.get('display'))
            print("     LIVE disp:", lp.get('display'))
        if schg:
            print("     PRE sol:", pp.get('solutions'), "LIVE sol:", lp.get('solutions'))
