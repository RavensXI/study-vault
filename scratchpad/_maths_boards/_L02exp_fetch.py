import os, json, urllib.request
ID="a1bdc834-74b8-41cf-8671-c1e3e5270619"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))[0]
open("_L02exp_live.json","w",encoding="utf-8").write(json.dumps(data,ensure_ascii=False,indent=1))
print("title:",data["title"],"| slug:",data["slug"])
pd=data["practice_data"]
print("top keys:",sorted(pd.keys()))
we=pd.get("worked_examples")
print("num worked_examples:",len(we) if we else 0)
for i,w in enumerate(we or []):
    print(f"  [{i}] {w.get('difficulty')}: {w.get('question')}")
