import os, json, urllib.request

ID = "04953988-ada8-4eb2-bbd4-401fb67247ff"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_CHKL11_live.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("saved live. top keys:", list(pd.keys()))
