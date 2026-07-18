import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "adf9527f-6097-41a2-be07-ed5ddf16405a",
    "prop1": "c03fa3a5-9dc1-4fbf-9266-4a86b26ddd02",
    "prop2": "cd1fab69-60be-440b-9d80-60cd6b7f03fd",
    "prop3": "2df67b6a-0efc-44cb-99c5-b8365480dfc4",
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
    with open(f"_ADV_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    print(name, rid, "bytes:", len(json.dumps(pd, ensure_ascii=False, sort_keys=True)))

# propagation identity
canon = json.dumps(out["canonical"], ensure_ascii=False, sort_keys=True)
for name in ["prop1", "prop2", "prop3"]:
    other = json.dumps(out[name], ensure_ascii=False, sort_keys=True)
    print(f"{name} identical to canonical:", other == canon)
