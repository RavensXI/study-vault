import os,json,io,urllib.request
ID="c8bc060f-c094-4b04-abec-5577523f8667"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_live_verify_L03.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
