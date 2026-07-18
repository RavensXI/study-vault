import json,io
live=json.load(io.open('_live_canonical.json',encoding='utf-8'))
pre=json.load(io.open('_pre_canonical.json',encoding='utf-8'))
def j(x): return json.dumps(x,ensure_ascii=False,sort_keys=True)
for f in ['related_videos','topic_links']:
    print(f, 'UNCHANGED' if j(live.get(f))==j(pre.get(f)) else 'CHANGED')
# exam_context
print('exam_context live:', j(live.get('exam_context')))
print('exam_context pre :', j(pre.get('exam_context')))
# worked_examples: compare questions & answer content (ignore label em-dash edits)
lw=live.get('worked_examples',[]); pw=pre.get('worked_examples',[])
print('worked_examples count live/pre:', len(lw), len(pw))
for i in range(min(len(lw),len(pw))):
    print(' WE',i,'q same:', lw[i].get('question')==pw[i].get('question'))
# problem displays diff
for t in ['bronze','silver','gold']:
    for i,(a,b) in enumerate(zip(live['problem_bank'][t],pre['problem_bank'][t])):
        if a.get('display')!=b.get('display'):
            print('DISPLAY CHANGED',t,i)
            print('  pre :',b.get('display'))
            print('  live:',a.get('display'))
        if a.get('equation_hint')!=b.get('equation_hint'):
            print('EQHINT CHANGED',t,i,'| pre=',b.get('equation_hint'),'| live=',a.get('equation_hint'))
