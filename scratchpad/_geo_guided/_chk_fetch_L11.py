import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "5f3e3753-de22-40b3-ba5c-65d334e792db"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
d = json.load(urllib.request.urlopen(req))
pd = d[0]["practice_data"]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_CHK_L11_live.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("ok", len(json.dumps(pd)))
