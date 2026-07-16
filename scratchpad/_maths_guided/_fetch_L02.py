import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.fe5f6191-4452-4313-934d-8e5d16ba1032&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer "+key})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_live_L02.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
