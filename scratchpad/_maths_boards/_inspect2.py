import json,io
pd=json.load(io.open("_live_gl01.json",encoding="utf-8"))
pb=pd["problem_bank"]
def show(tier,i):
    p=pb[tier][i]
    print(f"### {tier}[{i}]")
    print(json.dumps(p,ensure_ascii=False,indent=1))
# charts
for t,i in [("bronze",4),("bronze",7),("silver",2)]:
    p=pb[t][i]
    print(f"--- CHART {t}[{i}] sol={p.get('solutions')} ---")
    print("display:",p.get("display"))
    print("chart:",json.dumps(p.get("chart"),ensure_ascii=False))
print("==== MC silver[6] ====")
show("silver",6)
print("==== descriptions ====")
for k in pb:
    if k.endswith("description"): print(k,":",pb[k])
print("==== other top keys ====")
print("method_card:",json.dumps(pd.get("method_card"),ensure_ascii=False)[:600])
print("worked_examples count:",len(pd.get("worked_examples",[])))
print("topic_links:",json.dumps(pd.get("topic_links"),ensure_ascii=False)[:400])
print("related_videos:",json.dumps(pd.get("related_videos"),ensure_ascii=False)[:400])
print("has guided?", "guided" in pd, "has tier_guides?", "tier_guides" in pd)
