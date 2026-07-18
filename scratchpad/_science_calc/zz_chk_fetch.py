import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "235062c3-62a6-47ea-8337-2d59bed86884",
    "prop1": "0813c54e-be49-43c3-a6d5-75b0ee61344d",
    "prop2": "fae4f450-c4b1-4687-98ef-8e1df8f66563",
    "prop3": "1461ee2f-8387-4bd9-afb4-9afa19daecd4",
}

def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"]

out = {}
for name, rid in ids.items():
    pd = fetch(rid)
    out[name] = pd
    with open(f"zz_chk_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)

canon_s = json.dumps(out["canonical"], sort_keys=True, ensure_ascii=False)
for name in ["prop1", "prop2", "prop3"]:
    s = json.dumps(out[name], sort_keys=True, ensure_ascii=False)
    print(name, "IDENTICAL" if s == canon_s else "MISMATCH")

print("canonical keys:", sorted(out["canonical"].keys()))
