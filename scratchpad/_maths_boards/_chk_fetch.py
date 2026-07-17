import json, os, urllib.request

ID = "e58f9467-dd87-4589-9b18-b603c1966291"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_chk_live_numberL01.json","w"), indent=1)
print("LIVE keys:", list(pd.keys()))
print("saved")
