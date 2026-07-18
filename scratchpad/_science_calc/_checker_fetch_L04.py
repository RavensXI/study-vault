import os, json, urllib.request
key = os.environ['SUPABASE_SERVICE_KEY']
cid = "9941e716-ac52-4486-8f10-a81babbb8cc1"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=id,slug,title,practice_data"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
json.dump(data[0], open('_CHECK_live_L04.json','w'), indent=2)
print("slug", data[0]['slug'], "title", data[0]['title'])
pd = data[0]['practice_data']
print("keys", list(pd.keys()))
