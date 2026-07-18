import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = ["e68bcd00-8b3f-47d3-9a5b-e327a9ddde48", "3848d92a-26c5-4ebf-a4d4-7f55b392e888"]

def fetch(id_):
    url = f"{BASE}?id=eq.{id_}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

out = {i: fetch(i) for i in IDS}

with open("_live_canonical.json", "w", encoding="utf-8") as f:
    json.dump(out[IDS[0]], f, ensure_ascii=False, indent=1)
with open("_live_row2.json", "w", encoding="utf-8") as f:
    json.dump(out[IDS[1]], f, ensure_ascii=False, indent=1)

a = json.dumps(out[IDS[0]], sort_keys=True, ensure_ascii=False)
b = json.dumps(out[IDS[1]], sort_keys=True, ensure_ascii=False)
print("PROPAGATION_IDENTICAL:", a == b)
print("canonical len:", len(a), "row2 len:", len(b))
print("top keys:", sorted(out[IDS[0]].keys()))
