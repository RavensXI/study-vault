import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "fe5f6191-4452-4313-934d-8e5d16ba1032"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_CHK_live_geomL02.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("top keys:", list(pd.keys()))
