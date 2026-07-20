import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
pre=json.load(open('_CHK_L03_pre.json',encoding='utf-8'))['pd']
live=json.load(open('_CHK_L03_live.json',encoding='utf-8'))
pw,lw=pre['worked_examples'],live['worked_examples']
print('type',type(pw),len(pw),len(lw))
for i,(a,b) in enumerate(zip(pw,lw)):
    if a!=b:
        print('WE',i,'DIFF')
        print(' PRE :',json.dumps(a,ensure_ascii=False)[:900])
        print(' LIVE:',json.dumps(b,ensure_ascii=False)[:900])
# scan for em dashes and check:wrong
s=json.dumps(live,ensure_ascii=False)
print('check-wrong count:', s.count('"check"'))
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+'.'+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+'['+str(i)+']')
    elif isinstance(o,str):
        if '—' in o or '–' in o: print('DASH',path,':',o[:160])
        if re.search(r'&[a-z]+;',o): print('ENTITY',path,':',o[:120])
walk(live)
print('--- tier_guides ---')
print(json.dumps(live['tier_guides'],ensure_ascii=False,indent=1))
