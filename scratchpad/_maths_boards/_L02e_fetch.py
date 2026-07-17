import os, json, urllib.request
ID = "09c2b39e-ac37-4058-8de3-22b163764aa7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_L02e_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pre = json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
for row in pre:
    if row.get("id")==ID:
        json.dump(row["practice_data"], open("_L02e_pre.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
        print("pre keys:", list(row["practice_data"].keys()))
        break
