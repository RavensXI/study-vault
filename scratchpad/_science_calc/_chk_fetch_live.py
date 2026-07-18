import os, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
    return json.load(urllib.request.urlopen(req))[0]['practice_data']
ids=["adf9527f-6097-41a2-be07-ed5ddf16405a",
"c03fa3a5-9dc1-4fbf-9266-4a86b26ddd02",
"cd1fab69-60be-440b-9d80-60cd6b7f03fd",
"b508e272-cc00-4e75-9ce6-dc4d3b8d740e",
"8590dc8c-2894-40ce-a047-bcbf45b73e85",
"eb043cb0-025f-41cf-8179-2d6c15b62de9",
"2df67b6a-0efc-44cb-99c5-b8365480dfc4"]
canon=get(ids[0])
json.dump(canon, open('_CHK_canon_live.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
cs=json.dumps(canon,sort_keys=True,ensure_ascii=False)
print("canonical fetched, len bytes:", len(cs))
for rid in ids[1:]:
    pd=get(rid)
    same = json.dumps(pd,sort_keys=True,ensure_ascii=False)==cs
    print(rid, "IDENTICAL" if same else "DIFFERENT")
