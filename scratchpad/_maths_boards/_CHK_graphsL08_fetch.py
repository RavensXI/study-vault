import json, io, os, urllib.request

ID = "2ce07c9f-af5f-4162-ae95-544d91a71830"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, io.open("_CHK_graphsL08_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("LIVE saved. top keys:", list(pd.keys()))

# predump
d = json.load(io.open("_pre_dump_maths-aqa.json", encoding="utf-8"))
for x in d:
    if x.get("id") == ID:
        json.dump(x["practice_data"], io.open("_CHK_graphsL08_pre.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
        print("PRE saved. top keys:", list(x["practice_data"].keys()))
