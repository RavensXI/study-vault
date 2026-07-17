import os, json, urllib.request

ID="7f417926-0bef-4875-a7ad-7eb71bd15506"
key=os.environ.get("SUPABASE_SERVICE_KEY")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
with open("_LIVE_eduqas_probstat_L02.json","w",encoding="utf-8") as f:
    json.dump(pd,f,ensure_ascii=False,indent=2)
print("keys:",list(pd.keys()))
print("written")
