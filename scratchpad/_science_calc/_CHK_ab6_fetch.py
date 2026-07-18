import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["72ac6bb2-a0ff-4955-98f0-7ead3e2b7423", "7cb0647a-2614-4a1b-ae2f-4598bfa47c96"]
out = {}
for i in ids:
    url = f"{BASE}?id=eq.{i}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    out[i] = data[0]

d = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/"
with open(d+"_CHK_ab6_canon.json","w",encoding="utf-8") as f:
    json.dump(out[ids[0]]["practice_data"], f, ensure_ascii=False, indent=1)
with open(d+"_CHK_ab6_prop.json","w",encoding="utf-8") as f:
    json.dump(out[ids[1]]["practice_data"], f, ensure_ascii=False, indent=1)

# byte-identical check on canonical JSON serialization
c = json.dumps(out[ids[0]]["practice_data"], sort_keys=True, ensure_ascii=False)
p = json.dumps(out[ids[1]]["practice_data"], sort_keys=True, ensure_ascii=False)
print("PROPAGATION byte-identical:", c == p)
print("canon len:", len(c), "prop len:", len(p))
