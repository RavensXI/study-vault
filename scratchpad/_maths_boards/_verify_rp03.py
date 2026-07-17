# -*- coding: utf-8 -*-
import json, io, re, math
pd = json.load(io.open("lesson_maths-aqa_ratio-proportion-L03.json", encoding="utf-8"))
errs = []

# independent fresh-solve of every bank problem
def solve():
    B = pd["problem_bank"]
    checks = {
     ("bronze",0): 240/4, ("bronze",1): 80*3, ("bronze",2): 30/15, ("bronze",3): 200/25,
     ("bronze",4): 1.4*50, ("bronze",5): 120/4, ("bronze",6): 600/3, ("bronze",7): 50*6,
     ("silver",0): 90/1.5, ("silver",1): 400/50, ("silver",2): 750/(5**3), ("silver",3): 72/3.6,
     ("silver",4): 600/0.02, ("silver",5): 50*2.4, ("silver",6): 300/10+400/8,
     ("gold",0): 300/5, ("gold",1): round(594/(63*math.pi),1), ("gold",2): 60/0.75,
     ("gold",4): 200/40,
    }
    for (t,i),v in checks.items():
        sol = B[t][i]["solutions"][0]
        if abs(sol - v) > 0.011:
            errs.append("SOLVE %s[%d] stored %s != computed %s" % (t,i,sol,v))
    # gold[3] fraction 1/2
    if B["gold"][3]["solutions"] != [1,2]:
        errs.append("gold[3] fraction not [1,2]")

# recompute every guided_steps box
def walk(steps, path):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        # evaluate arithmetic embedded in pre where possible is manual; just record
    return

# manual box ledger: every box answer verified by expression in pre
def check_boxes():
    B = pd["problem_bank"]
    # explicit recompute of each box's stated arithmetic
    ledger = []
    def gs(t,i): return B[t][i]["guided_steps"]
    # bronze
    assert gs("bronze",0)[1]["answer"]==240/4
    assert gs("bronze",0)[2]["answer"]==60*4
    assert gs("bronze",0)[3]["answer"]==60*5
    assert gs("bronze",1)[1]["answer"]==80*3 and gs("bronze",1)[2]["answer"]==240/3 and gs("bronze",1)[3]["answer"]==80*5
    assert gs("bronze",2)[1]["answer"]==30/15 and gs("bronze",2)[2]["answer"]==15*2 and gs("bronze",2)[3]["answer"]==45/15
    assert gs("bronze",3)[1]["answer"]==200/25 and gs("bronze",3)[2]["answer"]==8*25 and gs("bronze",3)[3]["answer"]==8*50
    assert gs("bronze",4)[1]["answer"]==1.4*50 and abs(gs("bronze",4)[2]["answer"]-70/50)<1e-9 and gs("bronze",4)[3]["answer"]==1.4*100
    assert gs("bronze",5)[1]["answer"]==120/4 and gs("bronze",5)[2]["answer"]==30*4 and gs("bronze",5)[3]["answer"]==120/6
    assert gs("bronze",6)[1]["answer"]==600/3 and gs("bronze",6)[2]["answer"]==3*200 and gs("bronze",6)[3]["answer"]==900/3
    assert gs("bronze",7)[1]["answer"]==50*6 and gs("bronze",7)[2]["answer"]==300/6 and gs("bronze",7)[3]["answer"]==50*10
    # silver
    assert gs("silver",0)[1]["answer"]==1.5 and gs("silver",0)[2]["answer"]==90/1.5 and gs("silver",0)[3]["answer"]==60*1.5
    assert gs("silver",1)[1]["answer"]==400/50 and gs("silver",1)[2]["answer"]==8*50 and gs("silver",1)[3]["answer"]==8*75
    assert gs("silver",2)[1]["answer"]==5**3 and gs("silver",2)[2]["answer"]==750/125 and gs("silver",2)[3]["answer"]==6*125
    assert gs("silver",3)[1]["answer"]==72/3.6 and gs("silver",3)[2]["answer"]==20*3.6 and gs("silver",3)[3]["answer"]==20*60
    assert gs("silver",4)[1]["answer"]==600/0.02 and gs("silver",4)[2]["answer"]==30000*0.02 and gs("silver",4)[3]["answer"]==600/0.04
    assert gs("silver",5)[1]["answer"]==2.4 and gs("silver",5)[2]["answer"]==50*2.4 and gs("silver",5)[3]["answer"]==120/2.4
    assert gs("silver",6)[1]["answer"]==300/10 and gs("silver",6)[2]["answer"]==400/8 and gs("silver",6)[3]["answer"]==80 and gs("silver",6)[4]["answer"]==50*8
    # gold
    assert gs("gold",0)[1]["answer"]==180/90 and gs("gold",0)[2]["answer"]==120/40 and gs("gold",0)[3]["answer"]==300/5 and gs("gold",0)[4]["answer"]==60*5
    assert gs("gold",1)[1]["answer"]==3**2 and abs(gs("gold",1)[2]["answer"]-63*math.pi)<0.01 and gs("gold",1)[3]["answer"]==3 and gs("gold",1)[4]["answer"]==594
    assert gs("gold",2)[1]["answer"]==0.75 and gs("gold",2)[2]["answer"]==60/0.75 and gs("gold",2)[3]["answer"]==80*0.75
    assert gs("gold",3)[1]["answer"]==2 and gs("gold",3)[2]["answer"]==0.5 and gs("gold",3)[3]["answer"]==500/2
    assert gs("gold",4)[1]["answer"]==5*4*2 and gs("gold",4)[2]["answer"]==200/40 and gs("gold",4)[3]["answer"]==5*40

# expects reproduce the committed error
def check_expects():
    B = pd["problem_bank"]
    exp = {
     ("bronze",0): 240*4, ("bronze",2): 15/30, ("bronze",3): 25/200, ("bronze",5): 120*4, ("bronze",6): 600*3,
     ("silver",0,0): 90/1, ("silver",1,0): 50/400, ("silver",2,0): 750/5, ("silver",2,1): 750/25,
     ("silver",3,0): 72*3.6, ("silver",4,0): 600*0.02, ("silver",4,1): 600/2, ("silver",5,0): 50*2.24, ("silver",5,1): 50*2,
     ("gold",0,0): (90+40)/2, ("gold",1,0): 594/(9*math.pi*7/9*9)  # placeholder
    }
    # gold1 radius not squared: V=pi*3*7=21pi, 594/(21pi)=9
    assert abs(594/(21*math.pi)-9)<0.02
    # verify listed expects match
    def ex(t,i,j=0): return B[t][i]["misconceptions"][j]["expect"]
    assert ex("bronze",0)==240*4
    assert ex("bronze",2)==15/30
    assert ex("bronze",3)==25/200
    assert ex("bronze",5)==120*4
    assert ex("bronze",6)==600*3
    assert ex("silver",0)==90
    assert ex("silver",1)==50/400
    assert ex("silver",2,0)==750/5
    assert ex("silver",2,1)==750/25
    assert abs(ex("silver",3)-72*3.6)<1e-9
    assert ex("silver",4,0)==600*0.02
    assert ex("silver",4,1)==600/2
    assert abs(ex("silver",5,0)-50*2.24)<1e-6
    assert ex("silver",5,1)==50*2
    assert ex("gold",0)==(90+40)/2
    assert ex("gold",1)==9
    assert ex("gold",4)==200/20  # one face 5x4=20 -> 200/20=10
    assert ex("gold",3)==[2,1]

# duplicate check within tier
def dup():
    for t in ("bronze","silver","gold"):
        seen=set()
        for i,p in enumerate(pd["problem_bank"][t]):
            k=tuple(p["solutions"])
            if k in seen: errs.append("DUP %s %s"%(t,k))
            seen.add(k)

solve(); check_boxes(); check_expects(); dup()
if errs:
    print("FAIL"); [print(" -",e) for e in errs]
else:
    print("VERIFY PASS: all solutions, boxes, expects, no dupes")
