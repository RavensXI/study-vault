import os, json, urllib.request
ID="dd0172cd-6a81-41c6-ae9b-98de9328eb77"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
row=d[0]
print("TITLE:", row["title"], "SLUG:", row.get("slug"))
pd=row["practice_data"]
json.dump(pd, open("_L10ocr_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("KEYS:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("PB KEYS:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr=pb.get(t) or pd.get(t)
    print(t, "n=", len(arr) if arr else 0)
