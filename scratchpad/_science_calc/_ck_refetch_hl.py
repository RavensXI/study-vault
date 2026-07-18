import json, os, urllib.request, io
key=os.environ.get('SUPABASE_SERVICE_KEY')
cid="c0b4f7b9-4bc5-4dcb-af9f-b3bea7be7151"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=id,title,practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
row=data[0]
pd=row['practice_data']
io.open('_ck_refetch_hl.json','w',encoding='utf-8').write(json.dumps(pd,ensure_ascii=False,indent=1))
# fingerprint the content: look at first bronze display + method_card title
print("row title:", row.get('title'))
print("method_card title:", pd['method_card']['title'])
print("bronze0 display:", pd['problem_bank']['bronze'][0]['display'][:90])
print("bronze0 unit:", repr(pd['problem_bank']['bronze'][0].get('unit')))
print("opener display:", pd['guided']['opener']['display'][:80])
