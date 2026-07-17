import json, difflib
live = json.load(open("_recheck_rp01_live.json", encoding="utf-8"))
pre = json.load(open("_recheck_rp01_pre.json", encoding="utf-8"))

print("===== METHOD_CARD.content char diff =====")
p=pre["method_card"]["content"]; l=live["method_card"]["content"]
sm=difflib.SequenceMatcher(None,p,l)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag!="equal":
        print(f"  {tag}: PRE[{i1}:{i2}]={p[i1:i2]!r}  LIVE[{j1}:{j2}]={l[j1:j2]!r}")

print("\n===== WORKED_EXAMPLES full char diff per example =====")
for idx,(pe,le) in enumerate(zip(pre["worked_examples"],live["worked_examples"])):
    ps=json.dumps(pe,ensure_ascii=False,sort_keys=True); ls=json.dumps(le,ensure_ascii=False,sort_keys=True)
    if ps==ls: 
        print(f"[{idx}] identical"); continue
    sm=difflib.SequenceMatcher(None,ps,ls)
    print(f"[{idx}] diffs:")
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!="equal":
            print(f"    {tag}: PRE={ps[i1:i2]!r} LIVE={ls[j1:j2]!r}")
