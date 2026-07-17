import os, json, urllib.request

ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=*"
req = urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
print("ALL COLS:", [k for k in row.keys()])
for k in ("title","subject_slug","unit_slug","lesson_number","slug","subject","unit"):
    if k in row: print(k,"=",row[k])
with open("_live_ocr_numberL03.json","w",encoding="utf-8") as f:
    json.dump(row.get("practice_data"), f, indent=2, ensure_ascii=False)
pd = row.get("practice_data") or {}
print("PD keys:", list(pd.keys()))
