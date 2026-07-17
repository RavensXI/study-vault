import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
tg=pd.get("tier_guides",{})
for t in ["bronze","silver","gold"]:
    g=tg.get(t,{})
    print(f"\n=== tier_guide {t}: title={g.get('title')!r}")
    steps=g.get("steps",[])
    wc=sum(len(s.split()) for s in steps)
    print(f"  steps ({wc} words):")
    for s in steps: print("   -",s)
    ex=g.get("example",{})
    print("  example.question:",ex.get("question"))
    for st in ex.get("steps",[]):
        print(f"     [{st.get('label')}] {st.get('content')} isAnswer={st.get('isAnswer')}/{st.get('is_answer')}")
print("\n=== descriptions ===")
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    print(f" {t}:",pb.get(f"{t}_description"))
print("\n=== method_card ===")
mc=pd.get("method_card",{})
print("title:",mc.get("title"))
print("keys:",list(mc.keys()))
import re
print(json.dumps(mc,ensure_ascii=False)[:1500])
