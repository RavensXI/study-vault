import json,re
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
bank=pd['problem_bank']
# y-from-line functions per problem (same as verify2)
yf={
 ('gold',0):lambda x:2*x+1,('gold',1):lambda x:5-x,('gold',2):lambda x:x-1,('gold',3):lambda x:3-x,('gold',4):lambda x:7-x,
 ('bronze',0):lambda x:x,('bronze',1):lambda x:2*x,('bronze',2):lambda x:3,('bronze',3):lambda x:x+2,('bronze',4):lambda x:10,('bronze',5):lambda x:x+6,('bronze',6):lambda x:-x,('bronze',7):lambda x:4*x,
 ('silver',0):lambda x:x+3,('silver',1):lambda x:2-x,('silver',2):lambda x:2*x-1,('silver',3):lambda x:x+1,('silver',4):lambda x:3*x,('silver',5):lambda x:x,('silver',6):lambda x:5-2*x,
}
errs=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        f=yf[(tier,i)]
        for st in p['guided_steps']:
            pre=st.get('pre','')
            m=re.match(r'At x = (-?\d+\.?\d*): y =',pre)
            if m and 'answer' in st:
                xv=float(m.group(1)); want=f(xv)
                if abs(want-st['answer'])>1e-9:
                    errs.append(f"{tier}[{i}] '{pre}' answer {st['answer']} != {want}")
print("Y-BOX errors:", len(errs))
for e in errs: print("  ",e)
# check-boxes: last box 'answer' should equal what 'done' asserts; just confirm numeric consistency already validated by solutions.
print("done.")
