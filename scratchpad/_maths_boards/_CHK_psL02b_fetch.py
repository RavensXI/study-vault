import os, json, urllib.request

ID = "1a8441e6-115c-473e-a9b7-a2276e5b7faa"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=id,slug,title,practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_CHK_psL02b_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, ensure_ascii=False, indent=2)
print("slug:", row["slug"])
print("title:", row["title"])
pd = row["practice_data"]
print("pd keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
