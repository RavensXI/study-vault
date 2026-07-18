import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data,slug,title"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]
ids=["b2dd6adb-eb4b-4251-a9fd-3305d8493c16","ffdd38c1-b37c-4a37-83a2-12c4a58d9157"]
for rid in ids:
    row=get(rid)
    json.dump(row["practice_data"], open(f"_mine330_{rid[:8]}.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    pd=row["practice_data"]
    print(rid[:8], "title:", row.get("title"), "| mc.title:", pd.get("method_card",{}).get("title"))
    pb=pd.get("problem_bank",{})
    print("  b/s/g:", len(pb.get("bronze",[])), len(pb.get("silver",[])), len(pb.get("gold",[])))
    print("  has guided:", "guided" in pd, "| top keys:", list(pd.keys()))
# byte-identical check
a=json.dumps(get(ids[0])["practice_data"],sort_keys=True,ensure_ascii=False)
b=json.dumps(get(ids[1])["practice_data"],sort_keys=True,ensure_ascii=False)
print("BYTE-IDENTICAL canonical vs row2:", a==b)
