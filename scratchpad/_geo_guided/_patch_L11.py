import os, io, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "5f3e3753-de22-40b3-ba5c-65d334e792db"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
pd = json.load(io.open("lesson_L11.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

g = urllib.request.Request(url + "&select=practice_data",
                           headers={"apikey": key, "Authorization": "Bearer " + key})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("identical:", live == pd)
print("keys:", sorted(live.keys()))
print("bronze7 sol:", live["problem_bank"]["bronze"][7]["solutions"])
print("has guided:", "guided" in live, "descs:",
      all(k in live["problem_bank"] for k in ("bronze_description", "silver_description", "gold_description")))
