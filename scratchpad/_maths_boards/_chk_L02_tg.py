import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
tg = pd["tier_guides"]
for tier in ["bronze","silver","gold"]:
    g=tg[tier]
    steps=g.get("steps",[])
    wc=sum(len(s.split()) for s in steps)
    print(f"=== {tier}: title={g.get('title')!r}  steps_wordcount={wc}")
    for s in steps: print("   -",s)
    ex=g.get("example",{})
    print("   example.question:", ex.get("question"))
    for st in ex.get("steps",[]):
        print(f"      [{st.get('label')}] {st.get('content')}  isAnswer={st.get('isAnswer')}/{st.get('is_answer')}")
