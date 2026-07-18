import json, os, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

ids = {
    "canonical": "a5766e06-11a6-46fa-8f5a-f97ee39cb784",
    "prop1": "9c6e0eaf-f962-4771-b629-0e87b77d11a1",
    "prop2": "617bc3d1-57b7-4ee4-ba07-7f5ebd62d461",
    "prop3": "f8582151-399b-415e-af03-2aec3cf7d175",
}

for name, rid in ids.items():
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    pd = data[0]["practice_data"]
    with open("_QA_" + name + ".json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=1)
    print(name, rid, "fetched, keys:", sorted(pd.keys()))
