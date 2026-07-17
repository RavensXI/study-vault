import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "39bdcd12-eb3d-45b1-b0c5-d8e2257610df"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug,unit_id" % LID
req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
data = json.load(urllib.request.urlopen(req))
row = data[0]
json.dump(row["practice_data"], open("_gL03_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", row.get("title"), "| slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t,[])), "| desc:", repr(pb.get(t+"_description")))
