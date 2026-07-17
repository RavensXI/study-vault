import json, re
ID="bba25423-da94-4b3e-8415-2e9161014760"
live=json.load(open("_CHK_L02_live.json",encoding="utf-8"))
# find pre-dump entry
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
def findpre(pre):
    if isinstance(pre,list):
        for e in pre:
            if isinstance(e,dict) and e.get("id")==ID: return e
    elif isinstance(pre,dict):
        if ID in pre: return pre[ID]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: return v
    return None
pe=findpre(pre)
print("pre type:",type(pre).__name__, "| found pre entry:", pe is not None)
if pe is not None:
    pd = pe.get("practice_data", pe)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pd.get(f),ensure_ascii=False,sort_keys=True)
        b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
        print(f, "PRESERVED" if a==b else "CHANGED")
        if a!=b:
            print("  PRE :",a[:300])
            print("  LIVE:",b[:300])
# em dash scan on student-facing text
s=json.dumps(live,ensure_ascii=False)
print("em dash count (—):", s.count("—"))
# check every problem solutions index valid and count problems
for tier in ["bronze","silver","gold"]:
    probs=live["problem_bank"][tier]
    print(tier, "n=",len(probs))
