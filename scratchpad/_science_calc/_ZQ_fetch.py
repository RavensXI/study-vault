import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "858929dd-19a3-44ac-8f3e-76541c453b86",
    "prop": "0bdac62a-0fef-4fe1-8d40-0dd833682b0d",
}

for name, i in ids.items():
    url = f"{BASE}?id=eq.{i}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    pd = data[0]["practice_data"]
    out = f"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_ZQ_{name}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    # raw string for byte comparison
    raw = f"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_ZQ_{name}_raw.json"
    with open(raw, "w", encoding="utf-8") as f:
        f.write(json.dumps(pd, ensure_ascii=False, sort_keys=True))
    print(name, i, "len", len(json.dumps(pd, ensure_ascii=False, sort_keys=True)))
