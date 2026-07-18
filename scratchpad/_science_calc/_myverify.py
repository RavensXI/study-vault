# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open('lesson_higher-calculations-L04@57e3210892.json', encoding='utf-8'))
pb = pd['problem_bank']
g = 9.8
errs = []
def ck(name, got, exp, tol=1e-6):
    if abs(got - exp) > tol:
        errs.append("%s: got %s expected %s" % (name, got, exp))

sol = {
 'B0':200/0.04,'B1':2*1000*g,'B2':40000*0.1,'B3':500/0.05,'B4':5*1000*g,
 'B5':600/3000,'B6':29400/(1000*g),'B7':800*0.5,
 'S0':300/(0.2*0.5),'S1':0.8*13600*g,'S2':101000+10*1000*g,'S3':50/(2/10000),
 'S4':34300/(3.5*g),'S5':(8-3)*1000*g,
 'G0':101000+25*1025*g,'G1':(20*g)/(0.2*0.1),'G2':(40*1000*g)*(2*1.5),
 'G3':(50/0.002)*0.04,'G4':round(101000/(800*g),1),'G5':(101000+200*1025*g)/1000,
}
stored={}
for t,pre in (('bronze','B'),('silver','S'),('gold','G')):
    for i,p in enumerate(pb[t]): stored[pre+str(i)]=p['solutions'][0]
for k in sol: ck('solve '+k, sol[k], stored[k], tol=0.05)

ROUND_BOXES = {'h = 101000 ÷ 7840 = '}  # intentional 1 d.p. rounding, stated in post
def eval_pre(pre):
    m = re.search(r'([-−\d,\.\s×÷\+\(\)]+)=\s*$', pre)
    if not m: return None
    expr = m.group(1).replace('×','*').replace('÷','/').replace(',','').replace('−','-').replace('−','-').strip()
    if not re.match(r'^[-\d\.\s\*/\+\(\)]+$', expr): return None
    try: return eval(expr)
    except Exception: return None
def scan_boxes(steps, tag):
    for i,s in enumerate(steps):
        if s.get('answer') is None: continue
        if s.get('pre') in ROUND_BOXES:
            v = eval_pre(s['pre'])
            ck('roundbox %s[%d]'%(tag,i), round(v,1), s['answer'], tol=0.001); continue
        v = eval_pre(s.get('pre',''))
        if v is not None: ck('box %s[%d] pre=%r'%(tag,i,s['pre']), v, s['answer'], tol=0.01)
for t,pre in (('bronze','B'),('silver','S'),('gold','G')):
    for i,p in enumerate(pb[t]): scan_boxes(p.get('guided_steps',[]), '%s%d.gs'%(pre,i))
for tier in ('bronze','silver','gold'): scan_boxes(pd['guided']['teach'][tier]['steps'],'teach.'+tier)
scan_boxes(pd['guided']['opener']['steps'],'opener')

for t,pre in (('bronze','B'),('silver','S'),('gold','G')):
    for i,p in enumerate(pb[t]):
        s0=p['solutions'][0]; acc=p.get('accept',0.011)
        for j,mc in enumerate(p.get('misconceptions',[])):
            e=mc.get('expect')
            if e is None: continue
            ev=e[0] if isinstance(e,list) else e
            if abs(ev-s0)<=max(acc,0.011):
                errs.append("expect too close %s%d.m%d: %s vs sol %s"%(pre,i,j,ev,s0))

exp_checks={
 'B0':[200*0.04],'B1':[2*1000],'B2':[40000/0.1],'B3':[500*0.05],'B4':[5*1000],
 'B5':[600*3000],'B6':[29400/1000],'B7':[800/0.5],
 'S0':[300/1000],'S1':[0.8*1000*g],'S2':[10*1000*g],'S3':[50/(2/100)],
 'S4':[34300/3.5],'S5':[8*1000*g],
 'G0':[25*1025*g,101000+25*1000*g],'G1':[(20*g)/(0.5*0.2),20/(0.2*0.1)],
 'G2':[40*1000*g],'G3':[50/0.002,50*(0.002/0.04)],
 'G4':[101000/800,101000/(1000*g)],
 'G5':[(200*1025*g)/1000,101000+200*1025*g],
}
for t,pre in (('bronze','B'),('silver','S'),('gold','G')):
    for i,p in enumerate(pb[t]):
        key=pre+str(i)
        exps=[(mc['expect'][0] if isinstance(mc['expect'],list) else mc['expect']) for mc in p.get('misconceptions',[]) if mc.get('expect') is not None]
        for w in exp_checks.get(key,[]):
            if not any(abs(w-e)<=0.06 for e in exps):
                errs.append("committed-error expect missing %s: want ~%s have %s"%(key,round(w,3),exps))

# preservation check vs pre-dump
import io as _io
dump=json.load(_io.open('_pre_dump_all.json',encoding='utf-8'))
row=[x for x in dump if x.get('id')=='9941e716-ac52-4486-8f10-a81babbb8cc1'][0]['pd']
if row.get('related_videos')!=pd.get('related_videos'): errs.append('related_videos changed')
if row.get('topic_links')!=pd.get('topic_links'): errs.append('topic_links changed')
# worked_examples: only labels changed (em dash). compare content/question/answer
for a,b in zip(row['worked_examples'],pd['worked_examples']):
    if a['question']!=b['question']: errs.append('worked_example question changed')
    for sa,sb in zip(a['steps'],b['steps']):
        if sa['content']!=sb['content']: errs.append('worked_example content changed: '+sa.get('label',''))

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY PASS: solutions, boxes, expects, preservation all check out")
