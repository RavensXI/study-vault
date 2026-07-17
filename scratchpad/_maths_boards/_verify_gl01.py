import json, io
pd=json.load(io.open("lesson_maths-eduqas_graphs-L01.json",encoding="utf-8"))
pb=pd["problem_bank"]
prob=[]
# fresh independent solves keyed to displays
solve={
 ("bronze",0):(9-1)/(4-0), ("bronze",1):6, ("bronze",2):3, ("bronze",3):2*4+1,
 ("bronze",4):8, ("bronze",5):(19-7)/(3-0), ("bronze",6):-2, ("bronze",7):-3,
 ("silver",0):(1-9)/(5-1), ("silver",1):-3*4+7, ("silver",2):-1, ("silver",3):4*5-3,
 ("silver",4):0.5*8+3, ("silver",5):(14-2)/(3-(-1)), ("silver",6):2,
 ("gold",0):(8-(-7))/(2-(-3)), ("gold",1):7-4*2, ("gold",2):-2, ("gold",3):(-5-13)/(2-(-4)),
 ("gold",4):10/2,
}
bad=[]
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[t]):
        sol=p["solutions"]
        exp=solve[(t,i)]
        if p.get("input_type")=="multiple_choice":
            # sol is option index; verify option text
            optidx=sol[0]; opt=p["options"][optidx]
            if "ndefined" not in opt: bad.append(f"{t}[{i}] MC option idx {optidx}='{opt}' not undefined")
        else:
            if abs(float(sol[0])-float(exp))>1e-9:
                bad.append(f"{t}[{i}] stored {sol} != fresh {exp}")
            if p.get("input_type")!="multiple_choice":
                key=tuple(sol)
                if key in seen: bad.append(f"{t}[{i}] dup {sol} with {t}[{seen[key]}]")
                seen[key]=i
        # expect != solution
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(sol[0]))<1e-9:
                bad.append(f"{t}[{i}] expect==sol {e}")
        # last non-say guided box lands on solution (single_value)
        gs=p.get("guided_steps")
        if gs and p.get("input_type")!="multiple_choice":
            boxes=[s for s in gs if s.get("answer") is not None]
            # verify at least the designated answer box equals solution somewhere
            vals=[s["answer"] for s in boxes]
            if float(sol[0]) not in [float(v) for v in vals]:
                bad.append(f"{t}[{i}] solution {sol} not reached in walk boxes {vals}")
# chart point checks
def chk_chart(t,i,eq,label):
    pts=pb[t][i]["chart"]["data"]["datasets"][0]["data"]
    for pt in pts:
        if abs(eq(pt["x"])-pt["y"])>1e-9: bad.append(f"{t}[{i}] chart pt {pt} off {label}")
chk_chart("bronze",4,lambda x:3*x+2,"y=3x+2")
chk_chart("bronze",7,lambda x:9-3*x,"y=9-3x")
chk_chart("silver",2,lambda x:4*x-1,"y=4x-1")
# specific reads: bronze4 y at x=2 ; silver2 intercept ; bronze7 gradient
if 3*2+2!=8: bad.append("b4 read")
print("SOLUTIONS:", {f"{t}[{i}]":pb[t][i]['solutions'] for t in pb if isinstance(pb[t],list) for i in range(len(pb[t]))} if False else "")
for t in ("bronze","silver","gold"):
    print(t, [pb[t][i]["solutions"] for i in range(len(pb[t]))])
print("PROBLEMS BAD:", len(bad))
for b in bad: print("  -",b)
# preservation check vs live
live=json.load(io.open("_live_gl01.json",encoding="utf-8"))
for k in ("related_videos","topic_links"):
    print("preserved",k,":", json.dumps(pd.get(k))==json.dumps(live.get(k)))
print("worked_examples count same:", len(pd.get("worked_examples",[]))==len(live.get("worked_examples",[])))
