import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "e40e80e4-666f-4cce-a8b3-5f7bb6b5c490"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_live_gl02.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
print("written")
