import os,json,urllib.request,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="4aa9afe1-7e47-4f0f-b7e6-da22be472716"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
pd=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})))[0]["practice_data"]
open("_L06_fresh.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
# preservation vs pre-dump
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
pre_pd=[x for x in pre if x["id"]==ID][0]["practice_data"]
for f in ["related_videos","topic_links","worked_examples"]:
    print(f, "IDENTICAL" if pre_pd.get(f)==pd.get(f) else "DIFFERENT")
print("live keys:",list(pd.keys()))
