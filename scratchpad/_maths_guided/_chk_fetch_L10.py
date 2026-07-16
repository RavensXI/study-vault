import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "ddb5e897-f8ce-4c64-961a-7d6095d41a7c"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_CHK_L10_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("keys:", list(pd.keys()))
