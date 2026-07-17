import os, json, urllib.request

ID = "2d827ad4-80ab-4327-81f8-a2e5cec4f50a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_geometry-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify readback
u2 = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r2 = urllib.request.Request(u2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(r2))[0]["practice_data"]
d = live["guided"]["teach"]["gold"]["display"]
print("live rise 2 m label:", ">2 m</text>" in d)
print("live aria rise 2 m:", "rise 2 m" in d)
print("live rise unknown gone:", "rise unknown" not in d)
print("live single '?':", d.count("?") == 1)
print("live theta kept:", ">θ = ?</text>" in d)
# preservation spot-check
print("has related_videos:", bool(live.get("related_videos")))
print("has topic_links:", bool(live.get("topic_links")))
print("has worked_examples:", bool(live.get("worked_examples")))
