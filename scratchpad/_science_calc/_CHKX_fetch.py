import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = {
    "canonical": "fc32b93d-51c8-4260-a199-7268fa33979d",
    "prop": "d2088054-e987-4e06-8480-34549a015d79",
}
def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=id,slug,title,unit_id,practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]

for name, rid in ids.items():
    row = fetch(rid)
    with open(f"_CHKX_{name}.json", "w", encoding="utf-8") as f:
        json.dump(row, f, ensure_ascii=False, indent=2)
    print(name, rid, "slug=", row.get("slug"), "title=", row.get("title"))

# byte-identity comparison of practice_data
c = fetch(ids["canonical"])["practice_data"]
p = fetch(ids["prop"])["practice_data"]
cs = json.dumps(c, sort_keys=True, ensure_ascii=False)
ps = json.dumps(p, sort_keys=True, ensure_ascii=False)
print("PROP_IDENTICAL_sorted:", cs == ps)
# also raw serialization identical (order preserved)
cr = json.dumps(c, ensure_ascii=False)
pr = json.dumps(p, ensure_ascii=False)
print("PROP_IDENTICAL_raw:", cr == pr)
print("len canon:", len(cr), "len prop:", len(pr))
