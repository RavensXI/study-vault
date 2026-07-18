import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
BASE="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rid):
    url=f"{BASE}?id=eq.{rid}&select=practice_data"
    req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]
pd=get("2dc58e27-b4f5-42e5-9d45-0e632c9a2371")
json.dump(pd, open("_canon_215be42800.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("title:", pd.get("method_card",{}).get("title"))
pb=pd["problem_bank"]
print("bronze/silver/gold:", len(pb.get("bronze",[])), len(pb.get("silver",[])), len(pb.get("gold",[])))
print("gold displays:", [x["display"][:35] for x in pb["gold"]])
