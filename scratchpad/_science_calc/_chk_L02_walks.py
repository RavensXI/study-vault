import json, io
pd=json.load(io.open("_L02_6e6b_live.json",encoding="utf-8"))
out=io.open("_L02_6e6b_walks.txt","w",encoding="utf-8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
def dump(steps,label):
    w("### "+label)
    for i,s in enumerate(steps):
        if s.get("answer") is not None:
            w(f"  [{i}] BOX pre={s.get('pre')!r} post={s.get('post')!r} ans={s.get('answer')} phase={s.get('phase')} hint={s.get('hint')!r} done={s.get('done')!r}")
        else:
            w(f"  [{i}] SAY {s.get('say')!r} done={s.get('done')!r}")
g=pd["guided"]
w("OPENER display:",g["opener"].get("display"))
dump(g["opener"]["steps"],"opener")
for t in ("bronze","silver","gold"):
    tt=g["teach"][t]
    w("TEACH",t,"display:",tt.get("display"))
    dump(tt["steps"],"teach."+t)
# tier guides
w("\n==== TIER GUIDES ====")
for t in ("bronze","silver","gold"):
    tg=pd["tier_guides"][t]
    w(t,"title:",tg.get("title"))
    w("  steps:",tg.get("steps"))
    ex=tg.get("example",{})
    w("  example.q:",ex.get("question"))
    for s in ex.get("steps",[]):
        w("    -",s.get("label"),"::",s.get("content"),"ans?",s.get("is_answer") or s.get("isAnswer"))
w("\n==== METHOD CARD ====")
w(json.dumps(pd.get("method_card"),ensure_ascii=False)[:900])
w("\n==== exam_context ====",json.dumps(pd.get("exam_context"),ensure_ascii=False))
w("==== related_videos ====",json.dumps(pd.get("related_videos"),ensure_ascii=False))
w("==== topic_links ====",json.dumps(pd.get("topic_links"),ensure_ascii=False))
w("==== worked_examples count ====",len(pd.get("worked_examples") or []))
out.close()
print("done")
