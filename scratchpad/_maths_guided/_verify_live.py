import os,json,io,urllib.request,math
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_geomL07_LIVE_VERIFY.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
g=pd["problem_bank"]["gold"][1]["display"]
s=pd["problem_bank"]["silver"][5]["display"]
print("gold has ? at D bottom, 28 at C top:", ('y="64.00"' in g and "28°" in g), "sol", pd["problem_bank"]["gold"][1]["solutions"])
print("silver C on minor arc (166), 125 target:", ('y="166.00"' in s or 'cy="166.00"' in s), "sol", pd["problem_bank"]["silver"][5]["solutions"])
print("live matches local file:", json.dumps(pd,ensure_ascii=False)==json.dumps(json.load(io.open("lesson_geometry-L07_diagrams.json",encoding="utf-8")),ensure_ascii=False))
