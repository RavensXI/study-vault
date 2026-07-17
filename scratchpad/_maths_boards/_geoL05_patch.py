import os, io, json, urllib.request
ID = "1ee92530-13a8-48bd-901d-f8c28e6bf899"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_geometry-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify roundtrip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": f"Bearer {key}"})
got = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live keys:", sorted(got.keys()))
print("bronze n:", len(got["problem_bank"]["bronze"]), "silver n:", len(got["problem_bank"]["silver"]), "gold n:", len(got["problem_bank"]["gold"]))
print("has guided.opener:", bool(got.get("guided", {}).get("opener")))
print("has tier_guides:", bool(got.get("tier_guides")))
print("related_videos:", got.get("related_videos"))
print("B8 sol:", got["problem_bank"]["bronze"][7]["solutions"], "| G3 sol:", got["problem_bank"]["gold"][2]["solutions"], "| G5 sol:", got["problem_bank"]["gold"][4]["solutions"])
print("MATCH file == live:", got == pd)
