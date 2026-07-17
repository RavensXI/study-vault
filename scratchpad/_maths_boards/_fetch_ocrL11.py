import os, json, urllib.request
ID="04953988-ada8-4eb2-bbd4-401fb67247ff"
key=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug"%ID
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":"Bearer "+key})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_ocrL11_live.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=1))
print("title:",data[0]["title"],"slug:",data[0]["slug"])
print("top keys:",list(pd.keys()))
pb=pd.get("problem_bank",{})
for t in ("bronze","silver","gold"):
    ps=pb.get(t,[])
    print("==",t,len(ps),"problems; desc:",repr(pb.get(t+"_description")))
    for i,p in enumerate(ps):
        print(" ",t,i,"|it=",p.get("input_type"),"|calc=",p.get("calculator"),"|sol=",p.get("solutions"))
        print("     disp:",p.get("display"))
        if p.get("options"): print("     opts:",p.get("options"))
