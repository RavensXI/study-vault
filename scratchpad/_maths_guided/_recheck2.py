import os, json, urllib.request, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(live,open("_live_L07_CHECKER.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)

pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=None
for e in pre:
    if e.get("id")==ID: entry=e
pdp=entry.get("practice_data",entry)
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(pdp.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "preserved:", a==b)
# method_card trim check: pre had method_card too
print("pre method_card keys:", list(pdp.get("method_card",{}).keys()))
print("live method_card keys:", list(live.get("method_card",{}).keys()))
# word count of method_card content
import re
mc=live["method_card"]["content"]
txt=re.sub(r"<[^>]+>","",mc)
print("method_card content words:", len(txt.split()))
print("method_card steps count:", len(live["method_card"]["steps"]))
