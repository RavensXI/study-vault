import os,urllib.request,json
key=os.environ['SUPABASE_SERVICE_KEY']
ID='a5bc928e-98eb-4dcb-ae0f-b5003a4397d6'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug'
req=urllib.request.Request(url,headers={'apikey':key,'Authorization':'Bearer '+key})
row=json.load(urllib.request.urlopen(req))[0]
pd=row['practice_data']
json.dump(pd,open('_CK_live.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
print("TITLE:",row.get('title'),"SLUG:",row.get('slug'))
print("method_card title:",pd['method_card']['title'])
print("keys:",list(pd.keys()))
# em dash
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if '—' in o: print("EM DASH:",path)
walk(pd)
print("---phase/box audit---")
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        it=p.get('input_type'); gs=p.get('guided_steps')
        if it=='multiple_choice':
            print(f"{tier}[{i}] MC sol={p.get('solutions')}"); continue
        if not gs:
            print(f"{tier}[{i}] NO gs skip={p.get('guided_skip_reason')}"); continue
        ph=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if ph:
            f=ph[0]
            b=[s for s in gs[:f] if 'answer' in s]; a=[s for s in gs[f:] if 'answer' in s]
            print(f"{tier}[{i}] sol={p.get('solutions')} unit={p.get('unit')} accept={p.get('accept')} ho={p.get('higher_only')} before={len(b)} atafter={len(a)}")
        else:
            print(f"{tier}[{i}] sol={p.get('solutions')} NO PHASE boxes={sum(1 for s in gs if 'answer' in s)}")
