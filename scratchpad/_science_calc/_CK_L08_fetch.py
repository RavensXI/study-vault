import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "af432bd7-94b6-4601-a30d-4356767061bb",
    "prop1": "578cc26a-c6ab-4e1f-b87d-f818dd50e901",
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
    pd = fetch(rid)
    out[name] = pd
    with open(f"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_CK_L08_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)

# byte-identity check via canonical serialization
c = json.dumps(out["canonical"], sort_keys=True, ensure_ascii=False)
p = json.dumps(out["prop1"], sort_keys=True, ensure_ascii=False)
print("PROP IDENTICAL:", c == p)
print("canonical len:", len(c), "prop1 len:", len(p))
