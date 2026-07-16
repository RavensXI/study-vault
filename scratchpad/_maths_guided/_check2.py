import json
live=json.load(open('_live_L10.json',encoding='utf-8'))
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
LID='ddb5e897-f8ce-4c64-961a-7d6095d41a7c'
entry=None
if isinstance(pre,dict):
    if LID in pre: entry=pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get('id')==LID: entry=v; break
if entry is None and isinstance(pre,list):
    for v in pre:
        if v.get('id')==LID: entry=v; break
pd=entry.get('practice_data',entry)
pw=pd.get('worked_examples'); lw=live.get('worked_examples')
out=[]
out.append("pre count %s live count %s"%(len(pw) if pw else None, len(lw) if lw else None))
def dump(x): return json.dumps(x,sort_keys=True,ensure_ascii=False)
for i in range(max(len(pw or[]),len(lw or[]))):
    a=dump(pw[i]) if pw and i<len(pw) else "<none>"
    b=dump(lw[i]) if lw and i<len(lw) else "<none>"
    out.append("idx %d %s"%(i,"SAME" if a==b else "DIFF"))
    if a!=b:
        out.append("  PRE : %s"%(dump(pw[i]) if pw and i<len(pw) else '-'))
        out.append("  LIVE: %s"%(dump(lw[i]) if lw and i<len(lw) else '-'))
out.append("method_card SAME" if dump(pd.get('method_card'))==dump(live.get('method_card')) else "method_card DIFF (pre had: %s)"%dump(pd.get('method_card'))[:200])
out.append("pre keys: %s"%sorted(pd.keys()))
open('_out.txt','w',encoding='utf-8').write("\n".join(out))
print("done")
