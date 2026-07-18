import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = [
    "539110f5-5600-4dde-bee7-54fb60554f18",  # canonical
    "06772e71-a44d-47fa-967d-7ae17524126b",
    "550f4c75-d1fa-4f6e-a2de-2a0f0b317bd8",
    "d8149466-9dcb-46b2-9599-bfe559f3bd36",
    "87deed73-6660-4019-bb2a-57f708b45ed8",
    "b18f7be8-c8d8-44e6-ac6d-4246b0a7fc27",
    "1cc093ed-5247-4a15-b162-fcc764763d2b",
]

def fetch(i):
    url = f"{BASE}?id=eq.{i}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

outdir = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc"
canon = fetch(ids[0])
with open(outdir + "/_live_canon_L08.json", "w", encoding="utf-8") as f:
    json.dump(canon, f, indent=1, ensure_ascii=False)

canon_str = json.dumps(canon, sort_keys=True, ensure_ascii=False)
print("Canonical fetched. keys:", list(canon.keys()))
for i in ids[1:]:
    pd = fetch(i)
    match = json.dumps(pd, sort_keys=True, ensure_ascii=False) == canon_str
    print(f"{i}: byte-identical={match}")
