# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"]

ids = {
    "canonical": "08e03207-3ecf-4964-81dc-a8b94002b3e2",
    "prop1": "599f6b2c-9f8e-4321-b8b0-7e6036ce1450",
    "prop2": "a19bb97b-86bd-46fd-8623-a309449c8166",
}
out = {}
for name, rid in ids.items():
    pd = fetch(rid)
    out[name] = pd
    with open("_chk32_%s.json" % name, "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)

# byte-identical comparison via canonical json dump
c = json.dumps(out["canonical"], sort_keys=True, ensure_ascii=False)
p1 = json.dumps(out["prop1"], sort_keys=True, ensure_ascii=False)
p2 = json.dumps(out["prop2"], sort_keys=True, ensure_ascii=False)
print("prop1 identical:", p1 == c)
print("prop2 identical:", p2 == c)
print("canonical top keys:", sorted(out["canonical"].keys()))
