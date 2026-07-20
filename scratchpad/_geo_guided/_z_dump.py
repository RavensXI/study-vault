import json,sys
p=json.load(open('_CHK_L09_live.json',encoding='utf-8'))
out=[]
def w(s=''): out.append(s)
w("=== TOP KEYS ==="+str(list(p.keys())))
w("\n=== METHOD CARD ===\n"+json.dumps(p['method_card'],ensure_ascii=False,indent=1))
w("\n=== TIER GUIDES ===\n"+json.dumps(p['tier_guides'],ensure_ascii=False,indent=1))
w("\n=== GUIDED (opener+teach) ===\n"+json.dumps(p['guided'],ensure_ascii=False,indent=1))
pb=p['problem_bank']
w("\n=== PB KEYS ==="+str(list(pb.keys())))
for t in ['bronze','silver','gold']:
    for i,pr in enumerate(pb.get(t,[])):
        w("\n\n##### %s[%d] #####"%(t,i))
        w(json.dumps(pr,ensure_ascii=False,indent=1))
for k in ['topic_links','related_videos','worked_examples']:
    w("\n=== %s ===\n"%k+json.dumps(p[k],ensure_ascii=False,indent=1))
open('_z_L09_dump.txt','w',encoding='utf-8').write("\n".join(out))
print("lines",len("\n".join(out).split("\n")))
