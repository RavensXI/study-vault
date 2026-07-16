# -*- coding: utf-8 -*-
import json, io
pd=json.load(io.open('lesson_graphs-L04.json',encoding='utf-8'))
pb=pd['problem_bank']
prob=[]

# fresh-solve expected answers (computed independently here)
expected={
 'gold':[125,180,24,2.5,200],
 'bronze':[0.25,15,6,3,5,0,90,30],   # index5 is MC (answer index 0)
 'silver':[500,100,40,5,48,8,1],     # index6 is MC (answer index 1)
}
mc_idx={'bronze':[5],'silver':[6]}
ok=True
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        sol=p['solutions']
        exp=expected[t][i]
        if abs(float(sol[0])-float(exp))>1e-9:
            print("MISMATCH",t,i,"stored",sol,"expected",exp); ok=False
        # expect != solution
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is not None and not isinstance(e,list) and abs(float(e)-float(sol[0]))<0.011:
                print("EXPECT==SOL",t,i,e); ok=False
        # walk lands on solution (non-MC)
        if p.get('input_type')!='multiple_choice':
            gs=p['guided_steps']
            boxvals=[st['answer'] for st in gs if st.get('answer') is not None]
            if float(sol[0]) not in [float(x) for x in boxvals]:
                print("WALK-NO-SOL",t,i,sol,boxvals); ok=False
            # verify continuity: substitute boundary present, >=2 live after
            subi=next((k for k,st in enumerate(gs) if st.get('phase')=='substitute'),None)
            live=sum(1 for st in gs[subi:] if st.get('answer') is not None) if subi is not None else 0
            if subi is None or subi<1 or live<2:
                print("BOUNDARY",t,i,subi,live); ok=False

# chart-reading spot checks
def series(p): return p['chart']['data']
# B0 cyclist: labels/data; at 20 -> 5
b0=series(pb['bronze'][0]); assert b0['datasets'][0]['data'][b0['labels'].index(20)]==5, "B0"
# B1 walker: flat 4 from 20..35
b1=series(pb['bronze'][1]); d=b1['datasets'][0]['data']; L=b1['labels']
assert d[L.index(20)]==4 and d[L.index(35)]==4 and d[L.index(45)]!=4, "B1 flat"
# B2 jogger: 25->5, 30->6
b2=series(pb['bronze'][2]); d=b2['datasets'][0]['data']; L=b2['labels']
assert d[L.index(25)]==5 and d[L.index(30)]==6, "B2"
# G2 delivery: final 60 at 2.5
g2=series(pb['gold'][2]); d=g2['datasets'][0]['data']; L=g2['labels']
assert d[-1]==60 and L[-1]==2.5, "G2"
# S0 speed-time: labels 0,10,30 data 0,20,20 -> tri 100 + rect 400 = 500
s0=series(pb['silver'][0]); assert s0['datasets'][0]['data']==[0,20,20] and s0['labels']==[0,10,30], "S0"
# S4 conversion: 5->8, 30->48
s4=series(pb['silver'][4]); d=s4['datasets'][0]['data']; L=s4['labels']
assert d[L.index(5)]==8 and d[L.index(30)]==48, "S4"
print("chart checks OK")
print("ALL OK" if ok else "FAILURES ABOVE")
