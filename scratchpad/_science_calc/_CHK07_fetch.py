import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "3c4aa292-cf3a-4cda-876d-25b030880bb5",
    "prop1": "36c7ea77-c3be-464d-b057-4e7baf5754f5",
}

out = {}
for name, rid in ids.items():
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    data = json.load(urllib.request.urlopen(req))
    pd = data[0]["practice_data"]
    out[name] = pd
    with open(f"_CHK07_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(name, rid, "written")

# byte-identical check via canonical JSON serialization
a = json.dumps(out["canonical"], ensure_ascii=False, sort_keys=True)
b = json.dumps(out["prop1"], ensure_ascii=False, sort_keys=True)
print("PROP_IDENTICAL:", a == b)
