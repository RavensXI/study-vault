import os, json, urllib.request

ID = "8cea4310-541d-499d-a7e6-a8d82348cffd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

pd = data[0]["practice_data"]
outp = os.path.join(os.path.dirname(__file__), "_checker_live_L02.json")
with open(outp, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("wrote", outp)
print("top keys:", list(pd.keys()))
