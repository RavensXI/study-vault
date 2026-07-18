import json
d=json.load(open('_live_L04_f4e0.json'))
s=json.dumps(d,ensure_ascii=False)
for term in ['AQA','Edexcel',' OCR','Eduqas','WJEC','equation sheet','memorise','memorize','on your sheet','on the sheet','you are given']:
    if term.lower() in s.lower():
        print('FOUND TERM:', repr(term))
print('EM DASH' if '—' in s else 'no em dash')
def check(tier,probs):
    for i,p in enumerate(probs):
        sol=p.get('solutions'); acc=p.get('accept',0)
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is None: continue
            if sol and isinstance(sol[0],(int,float)) and abs(e-sol[0])<=acc:
                print(f'DEAD EXPECT {tier}[{i}] expect={e} sol={sol[0]} acc={acc}')
for t in ['bronze','silver','gold']:
    check(t,d['problem_bank'][t])
print('done')
