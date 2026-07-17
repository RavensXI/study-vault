import os, json, urllib.request
ID="ec35471d-bdb2-419a-9f86-1b8b85d6d5a7"
sk=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=title,slug,practice_data"%ID
req=urllib.request.Request(url, headers={"apikey":sk,"Authorization":"Bearer "+sk})
d=json.load(urllib.request.urlopen(req))
row=d[0]
print("title:", row["title"], "| slug:", row["slug"])
pd=row["practice_data"]
open("_live_ps02.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("top keys:", list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    print(t, "n=", len(pb.get(t,[])))
