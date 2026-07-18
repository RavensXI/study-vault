import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "2dc58e27-b4f5-42e5-9d45-0e632c9a2371",
    "prop1": "a6d04da2-b3f8-439b-bd35-1fe691f4d37d",
    "prop2": "6b4930c0-ab0c-42b9-a107-f71ada9b89b4",
    "prop3": "eac3d993-5c56-4ed3-834e-0ebd6ce733b2",
}

def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

out = {}
for name, rid in ids.items():
    pd = fetch(rid)
    out[name] = pd
    with open(f"_ckL03_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    print(name, rid, "bytes(canonical order):", len(json.dumps(pd, ensure_ascii=False, sort_keys=True)))

# byte-identity check
import hashlib
def h(pd):
    return hashlib.sha256(json.dumps(pd, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
ch = h(out["canonical"])
for name in ["prop1", "prop2", "prop3"]:
    print(name, "identical:", h(out[name]) == ch)
