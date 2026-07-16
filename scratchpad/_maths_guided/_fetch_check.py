import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "aee11210-c33f-4e61-a25e-1ef101e95ab3"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_live_geometry-L07.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
