import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "5ff3e1eb-2284-4096-af06-4bcb6754b0e1"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug" % ID
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
data = json.load(urllib.request.urlopen(req))
open("_L09_live_fresh.json","w",encoding="utf-8").write(json.dumps(data[0], ensure_ascii=False, indent=1))
pd = data[0]["practice_data"]
print("title:", data[0].get("title"), "slug:", data[0].get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    ps = pb.get(t,[])
    print("---",t,"n=",len(ps))
    for i,p in enumerate(ps):
        print("  ",i,repr(p.get("display")),"sol=",p.get("solutions"),"it=",p.get("input_type"),"calc=",p.get("calculator"))
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
