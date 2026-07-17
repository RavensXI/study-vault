import json, io, os, urllib.request

ID = "cdee2760-731b-4056-9231-cfd7327b0ed4"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
pd = row["practice_data"]
json.dump(pd, io.open("_MYCHK_gL08ocr_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("TITLE:", row.get("title"), "SLUG:", row.get("slug"))
print("LIVE saved. top keys:", list(pd.keys()))

# pre-dump (OCR)
for fn in ["_pre_dump_maths-ocr.json"]:
    try:
        d = json.load(io.open(fn, encoding="utf-8"))
        found=False
        for x in d:
            if x.get("id") == ID:
                json.dump(x["practice_data"], io.open("_MYCHK_gL08ocr_pre.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
                print("PRE saved from", fn, "keys:", list(x["practice_data"].keys()))
                found=True
        if not found: print("ID not found in", fn)
    except FileNotFoundError:
        print("missing", fn)
