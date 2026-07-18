import os, json, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
base="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def get(rowid):
    url=f"{base}?id=eq.{rowid}&select=id,practice_data"
    req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
    return json.load(urllib.request.urlopen(req))
row=get("9941e716-ac52-4486-8f10-a81babbb8cc1")
json.dump(row[0], open("_CHKR_canon_live.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("fetched", row[0]['id'])
print("keys:", list(row[0]['practice_data'].keys()))
