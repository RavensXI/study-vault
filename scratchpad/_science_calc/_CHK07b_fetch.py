import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = [
 "48cb4395-c42b-4faa-9a71-44653a691790",
 "ed42ef31-93ef-465b-a9b5-009c966c0b66",
 "bae7087c-4546-4cd2-b85a-d7e216a94f98",
 "3a671657-d72f-489b-ba36-8cb670215487",
 "64c70c8e-f859-49b3-a446-8447b78507c1",
 "9abf7f7e-b30f-4d37-b31e-7f6edb030f68",
 "9e971a6c-dc13-4a14-ab6c-11cbd4d7b3fd",
]
def fetch(i):
    url = f"{BASE}?id=eq.{i}&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

canon = fetch(ids[0])
with open("_CHK07b_canon.json","w",encoding="utf-8") as f:
    json.dump(canon, f, ensure_ascii=False, indent=1)
cs = json.dumps(canon, ensure_ascii=False, sort_keys=True)
print("canonical bytes:", len(cs))
for i in ids[1:]:
    pd = fetch(i)
    match = json.dumps(pd, ensure_ascii=False, sort_keys=True) == cs
    print(i, "MATCH" if match else "DIFFER")
