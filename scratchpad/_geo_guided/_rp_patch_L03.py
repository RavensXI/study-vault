import os, io, json, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.environ["SUPABASE_SERVICE_KEY"]
ID = "0d2298c0-fb7d-447b-80ee-0cf8468366f2"
pd = json.load(io.open(os.path.join(HERE, "lesson_L03.json"), encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": K, "Authorization": "Bearer " + K,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
print("status", urllib.request.urlopen(req).status)
# verify
r = urllib.request.Request(url + "&select=practice_data",
                           headers={"apikey": K, "Authorization": "Bearer " + K})
live = json.load(urllib.request.urlopen(r))[0]["practice_data"]
print("roundtrip identical:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
