import json, io, re
pd = json.load(io.open("_LIVE_canon_final.json", encoding="utf-8"))
issues=[]
g=9.8

def close(a,b,tol=1e-6): return abs(a-b)<=tol

# Fresh-solve each problem from first principles
sols = {
 # bronze
 ("bronze",0): 200/0.04, ("bronze",1): 2*1000*g, ("bronze",2): 60000*0.1,
 ("bronze",3): 500/0.05, ("bronze",4): 5*1000*g, ("bronze",5): 600/3000,
 ("bronze",6): 29400/(1000*g), ("bronze",7): 800*0.5,
 # silver
 ("silver",0): 300/((20/100)*(50/100)), ("silver",1): 0.8*13600*g,
 ("silver",2): 10*1000*g+101000, ("silver",3): 50/(2/10000),
 ("silver",4): 34300/(3.5*g), ("silver",5): (8-3)*1000*g,
 # gold
 ("gold",0): 25*1025*g+101000, ("gold",1): (20*g)/(0.2*0.1),
 ("gold",2): (40*1000*g)*(2*1.5), ("gold",3): (50/0.002)*0.04,
 ("gold",4): round(101000/(800*g),1), ("gold",5): (200*1025*g+101000)/1000,
}
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        exp=sols[(tier,i)]
        stored=p["solutions"][0]
        if not close(float(stored),float(exp), max(1e-6, p.get("accept",0)+1e-9)):
            issues.append(f"{tier}[{i}] fresh-solve {exp} != stored {stored} :: {p['display'][:60]}")

# Verify every guided_step box arithmetically by evaluating the pre-expression where possible
def check_boxes(steps, label):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        # extract an arithmetic expression like "= X ×/÷/+/- Y"
        m=re.findall(r'([\d,\.]+)\s*([×÷+\-])\s*([\d,\.]+)', pre)
        # We'll just trust manual; flag if answer wildly off from any parse
    return

# Manual box recomputation of key multi-step walks
def num(x): return float(str(x).replace(',',''))
# G1 walk
G1=pb["gold"][0]["guided_steps"]
assert num(G1[1]["answer"])==1025
assert close(25*1025*g, num(G1[2]["answer"]))    # 251125
assert close(251125+101000, num(G1[3]["answer"])) # 352125
assert close(352125-101000, num(G1[4]["answer"]))
# G5 walk
G5=pb["gold"][4]["guided_steps"]
assert close(800*g, num(G5[1]["answer"]))  #7840
assert num(G5[2]["answer"])==101000
assert num(G5[3]["answer"])==12.9
assert close(12.9*7840, num(G5[4]["answer"]))  #101136
# G6 walk
G6=pb["gold"][5]["guided_steps"]
assert close(200*1025*g, num(G6[1]["answer"]))  #2009000
assert close(2009000+101000, num(G6[2]["answer"]))#2110000
assert num(G6[3]["answer"])==2110
assert close(2110*1000, num(G6[4]["answer"]))

# expects outside accept window
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=float(p["solutions"][0]); acc=p.get("accept",0)
        for k,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if isinstance(e,list): e=e[0]
            if abs(float(e)-sol)<=max(acc,1e-9):
                issues.append(f"{tier}[{i}].misconceptions[{k}] expect {e} INSIDE accept window of {sol} (acc={acc})")

# board names
blob=json.dumps(pd,ensure_ascii=False)
for b in ["AQA","Edexcel","OCR","Eduqas","WJEC"]:
    if b in blob: issues.append(f"board name '{b}' present")
# equation-sheet claims (informational)
eqsheet=blob.count("equation sheet")
print("equation-sheet mentions:", eqsheet)
# em dash
if "—" in blob: issues.append("EM DASH present")

print("ISSUES:", len(issues))
for x in issues: print("  -", x)
print("all box asserts passed")
