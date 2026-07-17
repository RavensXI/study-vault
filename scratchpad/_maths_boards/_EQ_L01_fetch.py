import os, json, urllib.request

LID = "7e5e6d1a-aa08-4fbf-8094-760926f7e56c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = f"{BASE}?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_EQ_L01_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("LIVE fetched. Top keys:", list(pd.keys()))

# pre-dump extract
with open("_pre_dump_maths-eduqas.json", encoding="utf-8") as f:
    dump = json.load(f)
# find entry
def find(d):
    if isinstance(d, dict):
        if d.get("id") == LID or d.get("lesson_id") == LID:
            return d
        for v in d.values():
            r = find(v)
            if r: return r
    elif isinstance(d, list):
        for v in d:
            r = find(v)
            if r: return r
    return None
print("dump type:", type(dump), "keys" , list(dump.keys())[:5] if isinstance(dump,dict) else len(dump))
