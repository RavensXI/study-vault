import os, json, urllib.request, io
ID="e15d6925-608b-4c05-aa82-c4782d1657b3"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
with io.open("_live_L06.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
print("bank tiers:", {t: len(pd.get("problem_bank",{}).get(t,[])) for t in ("bronze","silver","gold")})
