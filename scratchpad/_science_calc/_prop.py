import os,json,urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
ids=["1b30cd36-ea7e-4210-baa6-cc9f3f30072a"]
base=json.load(open('_live_L04_f4e0.json'))
b=json.dumps(base,sort_keys=True,ensure_ascii=False)
for i in ids:
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{i}&select=practice_data'
    req=urllib.request.Request(url,headers={'apikey':key,'Authorization':'Bearer '+key})
    d=json.load(urllib.request.urlopen(req))
    same = json.dumps(d[0]['practice_data'],sort_keys=True,ensure_ascii=False)==b
    print(i,'identical' if same else 'DIFF')
print('all_row_ids count:',len(ids),'(propagates to 1 row: only canonical)')
