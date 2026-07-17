import os,json,urllib.request
ID="dd0172cd-6a81-41c6-ae9b-98de9328eb77"
key=os.environ["SUPABASE_SERVICE_KEY"]
u=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
r=urllib.request.Request(u,headers={"apikey":key,"Authorization":f"Bearer {key}"})
pd=json.load(urllib.request.urlopen(r))[0]["practice_data"]
json.dump(pd,open("_live_after_L10.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("dumped")
