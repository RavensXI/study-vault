import os, json, urllib.request, urllib.error
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = BASE + "?id=eq.d9384cf5-c3b4-4d2d-8f46-346f2c9a8ac6&select=practice_data,title,slug,unit_slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
try:
    with urllib.request.urlopen(req) as r:
        d = json.load(r); print("OK", len(d))
except urllib.error.HTTPError as e:
    print("HTTP", e.code); print(e.read().decode())
