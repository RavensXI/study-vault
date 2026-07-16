# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
pre = json.load(open('_pre_fanout_dump.json', encoding='utf-8'))
TARGET='1d039d5e-b358-4864-b935-b3334ba90000'
# print actual target from live fetch file
raw=json.load(open('_live_raw.json', encoding='utf-8'))
print('live raw is list of', len(raw), 'row(s)')

def walk(o, path='root'):
    out=[]
    if isinstance(o, dict):
        rid=o.get('id') or o.get('lesson_id')
        if isinstance(rid,str) and '1d039d5e' in rid:
            out.append((rid,o))
        for k,v in o.items(): out+=walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): out+=walk(v,f'{path}[{i}]')
    return out

hits=walk(pre)
print('pre-dump entries with 1d039d5e id:', [(h[0]) for h in hits])
for rid,o in hits:
    pd = o.get('practice_data', o)
    pb = pd.get('problem_bank',{})
    b=pb.get('bronze',[])
    print('id',rid)
    print('  slug/title fields:', {k:o.get(k) for k in ('slug','title','lesson_key','key') if k in o})
    print('  bronze[0] display:', b[0].get('display') if b else None)
    we=pd.get('worked_examples',[])
    print('  worked_examples questions:', [w.get('question') for w in we])
