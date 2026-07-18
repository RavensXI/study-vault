import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "9733399d-1134-4649-8166-74c5b738c4a3",
    "prop1": "c49b71fa-ab62-4285-81eb-9ad075aec3c6",
    "prop2": "e9831803-7f3f-4d55-8185-0214e8c30fe0",
}

for name, rid in ids.items():
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    data = json.load(urllib.request.urlopen(req))
    pd = data[0]["practice_data"]
    with open(f"_CK03_{name}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    print(name, rid, "written")
