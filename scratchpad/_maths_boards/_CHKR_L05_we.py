import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open('_CHKR_L05_live.json',encoding='utf-8'))
pd=json.load(open('_CHKR_L05_pd.json',encoding='utf-8'))
print('OLD worked_examples questions:')
for w in pd['worked_examples']:
    print(' -',w.get('difficulty'),'|',w.get('question'))
print('NEW worked_examples questions:')
for w in live['worked_examples']:
    print(' -',w.get('difficulty'),'|',w.get('question'))
print()
print('FULL OLD:')
print(json.dumps(pd['worked_examples'],indent=1,ensure_ascii=False))
print('FULL NEW:')
print(json.dumps(live['worked_examples'],indent=1,ensure_ascii=False))
print('method_card in predump?', 'method_card' in pd)
