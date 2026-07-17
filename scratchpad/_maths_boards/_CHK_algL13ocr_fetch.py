import os, json, urllib.request, io
ID="44ac4c68-828c-4d38-888a-37758fefde57"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
print("TITLE:", data[0].get("title"), "SLUG:", data[0].get("slug"))
with io.open("_CHK_algL13ocr_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
