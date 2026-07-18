import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = ["3b138666-ea0d-44c6-aaf7-55600dfb2244",
       "1370e525-105d-4889-a872-c664b71dec7e"]

pd = json.load(open("lesson_chemistry-calculations-L02@5b02ac14f2.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for rid in IDS:
    req = urllib.request.Request(BASE + "?id=eq." + rid, data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)

# verify propagation: fetch both, compare to file
def fetch(rid):
    req = urllib.request.Request(BASE + "?id=eq." + rid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

target = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for rid in IDS:
    live = json.dumps(fetch(rid), sort_keys=True, ensure_ascii=False)
    print("byte-identical to file:", rid, live == target)
