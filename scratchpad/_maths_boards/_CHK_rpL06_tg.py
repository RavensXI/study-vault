import json,io
pd=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
out=io.open("_CHK_rpL06_tg.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
tg=pd.get("tier_guides",{})
for tier in ["bronze","silver","gold"]:
    t=tg.get(tier,{})
    wc=sum(len(s.split()) for s in t.get("steps",[]))
    w(f"\n=== tier_guides.{tier} (steps wordcount={wc}) title={t.get('title')}")
    for s in t.get("steps",[]): w("  STEP:",s)
    ex=t.get("example",{})
    w("  EXAMPLE q:",ex.get("question"))
    for st in ex.get("steps",[]): w("    ",st.get("label"),"|",st.get("content"),"| isAnswer=",st.get("isAnswer"),st.get("is_answer"))
w("\n=== method_card ===")
mc=pd.get("method_card",{})
w(json.dumps(mc,ensure_ascii=False,indent=1))
out.close()
print(open("_CHK_rpL06_tg.txt",encoding="utf-8").read())
