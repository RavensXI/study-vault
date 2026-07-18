import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

canon = "3b138666-ea0d-44c6-aaf7-55600dfb2244"
other = "1370e525-105d-4889-a872-c664b71dec7e"
pc = fetch(canon)
po = fetch(other)
with open("_canon_5b02.json", "w", encoding="utf-8") as f:
    json.dump(pc, f, ensure_ascii=False, indent=1)
print("canon keys:", list(pc.keys()))
print("byte-identical canon vs other:", json.dumps(pc, sort_keys=True, ensure_ascii=False) == json.dumps(po, sort_keys=True, ensure_ascii=False))
pb = pc.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])), "desc:", bool(pb.get(t+"_description")))
print("has guided:", "guided" in pc, "has tier_guides:", "tier_guides" in pc)
print("top-level:", sorted(pc.keys()))
