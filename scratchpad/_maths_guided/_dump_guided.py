import json,re
pd=json.load(open("_live_algebra_L10.json",encoding="utf-8"))
g=pd.get("guided",{})
out=[]
op=g.get("opener",{})
out.append("OPENER keys: "+str(list(op.keys())))
out.append(json.dumps(op,indent=1,ensure_ascii=False))
out.append("="*50+" TEACH")
for tier,walk in g.get("teach",{}).items():
    out.append("--- "+tier)
    out.append(json.dumps(walk,indent=1,ensure_ascii=False)[:1500])
# search whole practice_data for figure-claim words
blob=json.dumps(pd,ensure_ascii=False)
for w in ["diagram","triangle","chart","graph","figure","Here is","shown","sketch","Picture","circle"]:
    idxs=[m.start() for m in re.finditer(w, blob)]
    if idxs: out.append(f"WORD '{w}': {len(idxs)} occurrences")
open("_guided_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
