import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = {
    "canon": "5bcd7990-52a4-49b0-8e2e-f3d0344df114",
    "prop":  "37bd5221-58cb-47ff-8411-b45c3589c868",
}
def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

out = {}
for k, rid in ids.items():
    pd = fetch(rid)
    out[k] = pd
    with open(f"_ADVCHK_{k}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)

# byte-identity check via canonical JSON
c = json.dumps(out["canon"], sort_keys=True, ensure_ascii=False)
p = json.dumps(out["prop"], sort_keys=True, ensure_ascii=False)
print("PROP byte-identical (sorted):", c == p)
print("canon len", len(c), "prop len", len(p))
