import os, json, urllib.request

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["3c4aa292-cf3a-4cda-876d-25b030880bb5", "36c7ea77-c3be-464d-b057-4e7baf5754f5"]

def fetch(i):
    url = BASE + "?id=eq." + i + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

for i in ids:
    pd = fetch(i)
    with open("_live_%s.json" % i[:8], "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    print("wrote", i[:8], "keys:", list(pd.keys()))

# propagation byte-identity check
import hashlib
a = json.dumps(fetch(ids[0]), sort_keys=True, ensure_ascii=False)
b = json.dumps(fetch(ids[1]), sort_keys=True, ensure_ascii=False)
print("CANONICAL sha:", hashlib.sha256(a.encode()).hexdigest()[:16])
print("PROPAGATE sha:", hashlib.sha256(b.encode()).hexdigest()[:16])
print("IDENTICAL (canonicalised):", a == b)
