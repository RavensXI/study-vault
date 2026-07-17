import os, json, urllib.request
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?slug=eq.probability-basics-and-tree-diagrams&select=id,title,practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
for r in data:
    pd=r.get("practice_data") or {}
    has_guided = "guided" in pd
    print(r["id"], "guided="+str(has_guided))
    if has_guided and r["id"]!="a28fddf4-3ee1-48dc-b138-aa17facad15d":
        open("_ES_sibling_"+r["id"][:8]+".json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))
        print("  saved sibling")
