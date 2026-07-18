import json, os, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
CID = "b4864848-f50f-4481-9af7-983e8f3d20d8"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % CID
req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
pd = json.loads(urllib.request.urlopen(req).read())[0]["practice_data"]
open("_mine_L03.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("title:", pd["method_card"]["title"])
for t in ("bronze","silver","gold"):
    print(t, [p["solutions"] for p in pd["problem_bank"][t]])
