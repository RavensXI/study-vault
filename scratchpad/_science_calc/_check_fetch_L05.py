import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "5473906a-ccfa-43f0-8230-5b9171181f19",
    "prop1": "132992fc-3fb6-414e-a307-e8c76adf8f00",
    "prop2": "2ce06ae7-bddb-4c8d-a32a-b15cb804f5b4",
}

def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"]

out = {}
for name, rid in ids.items():
    out[name] = fetch(rid)

with open("_live_L05.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)

# byte-identity check via canonical JSON serialization
import hashlib
def h(o): return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
print("canonical hash:", h(out["canonical"]))
print("prop1 hash:    ", h(out["prop1"]))
print("prop2 hash:    ", h(out["prop2"]))
print("prop1 identical:", h(out["canonical"]) == h(out["prop1"]))
print("prop2 identical:", h(out["canonical"]) == h(out["prop2"]))
print("written _live_L05.json")
