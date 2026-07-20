import json,re
live=json.load(open('_CHK_L01_live.json',encoding='utf-8'))
pre=json.load(open('_CHK_L01_pre.json',encoding='utf-8'))
s=json.dumps(live,ensure_ascii=False)
print('em/en dash count:', s.count('—'), s.count('–'))
print('check wrong:', s.count('"check"'))
print('urls live:', set(re.findall(r'https?://[^"\ ]+', s)))
print('urls pre:', set(re.findall(r'https?://[^"\ ]+', json.dumps(pre,ensure_ascii=False))))
print('html entities:', set(re.findall(r'&[a-z]+;', s)))
# numeric check
bad=[]
for t in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][t]):
        for j,st in enumerate(p.get('guided_steps',[])):
            if 'answer' in st and not isinstance(st['answer'],(int,float)):
                bad.append(f'{t}[{i}].guided_steps[{j}]')
            if 'answer' in st and not ('pre' in st):
                bad.append('nopre '+f'{t}[{i}].guided_steps[{j}]')
        for j,m in enumerate(p.get('misconceptions',[])):
            if 'check' in m: bad.append('CHECK '+f'{t}[{i}].misconceptions[{j}]')
            if 'expect' not in m: bad.append('NOEXPECT '+f'{t}[{i}].misconceptions[{j}]')
        if not p.get('hint'): bad.append('NOHINT '+f'{t}[{i}]')
        if not p.get('guided_steps') and 'guided_skip_reason' not in p: bad.append('NOGS '+f'{t}[{i}]')
for grp in ['opener']:
    for j,st in enumerate(live['guided'][grp]['steps']):
        if 'answer' in st and not isinstance(st['answer'],(int,float)): bad.append('opener'+str(j))
for tt,w in live['guided']['teach'].items():
    for j,st in enumerate(w['steps']):
        if 'answer' in st and not isinstance(st['answer'],(int,float)): bad.append(f'teach.{tt}[{j}]')
print('BAD:',bad)
# tier guide word counts
for t,g in live['tier_guides'].items():
    words=sum(len(re.sub('<[^>]+>','',x).split()) for x in g['steps'])
    print(t,'title:',g['title'],'| steps words:',words,'| nsteps',len(g['steps']))
print('method_card words:', len(re.sub('<[^>]+>',' ',live['method_card']['content']).split()))
