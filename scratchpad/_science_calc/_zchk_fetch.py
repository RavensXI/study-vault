import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = [
    "08e03207-3ecf-4964-81dc-a8b94002b3e2",
    "599f6b2c-9f8e-4321-b8b0-7e6036ce1450",
    "9d4bd9f1-eed4-4293-bc3e-1d92c305d7ac",
    "30f59090-f7ba-45e5-a2e4-47efa34fd2bd",
    "37227c2b-ee4d-4132-8dc6-39dda152d21a",
    "6134dce2-77b2-4bb5-8e24-7ec8a0e7f5b2",
    "a19bb97b-86bd-46fd-8623-a309449c8166",
]

def fetch(i):
    url = f"{BASE}?id=eq.{i}&select=practice_data,slug,title"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]

canon = fetch(ids[0])
with open("_zchk_canon.json", "w", encoding="utf-8") as f:
    json.dump(canon["practice_data"], f, ensure_ascii=False, indent=1)

canon_pd = json.dumps(canon["practice_data"], sort_keys=True, ensure_ascii=False)
for i in ids[1:]:
    row = fetch(i)
    pd = json.dumps(row["practice_data"], sort_keys=True, ensure_ascii=False)
    print(i, "IDENTICAL" if pd == canon_pd else "DIFFERENT", "len", len(pd))

print("canon title:", canon.get("title"), "| slug:", canon.get("slug"), "| subject:", canon.get("subject_slug"))
print("canon_pd len", len(canon_pd))
