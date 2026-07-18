import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=id,practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]

ids = [
    "e6963758-b327-488c-87b4-177b336f29e9",  # canonical
    "07e5d6c1-74ac-4da9-9942-7f440105e339",
    "5d2257b8-5623-4832-8653-d33cbc36e417",
    "60250fe9-465d-4667-9e15-4a601759e100",
    "17bbd05b-fda5-4bde-9932-fe62b9670913",
    "3dfe27ee-0fe0-4042-91f6-023c5d626e5b",
    "ca3b27a3-d2a5-4735-bb3e-507167e7ff77",
]

rows = {}
for rid in ids:
    row = fetch(rid)
    rows[rid] = row
    json.dumps(row["practice_data"])  # sanity

canon = rows[ids[0]]
json.dump(canon["practice_data"], open("_chk_canon_pd.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("canonical subject:", canon.get("id"))

# propagation: compare serialized practice_data
import hashlib
def h(pd): return hashlib.sha256(json.dumps(pd, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
canon_h = h(canon["practice_data"])
print("PROPAGATION CHECK (sha256 of practice_data, sort_keys):")
for rid in ids:
    hh = h(rows[rid]["practice_data"])
    print(f"  {rid[:8]} {rows[rid].get("id"):36s} {'MATCH' if hh==canon_h else 'MISMATCH'}")
