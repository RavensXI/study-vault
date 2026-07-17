import os, json, urllib.request
ID="689bc7ff-0d4c-4f20-a83c-9476935f2ac9"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_ratio-proportion-L03.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url,data=body,method="PATCH",headers={
 "apikey":key,"Authorization":f"Bearer {key}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)
g=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("live keys:",list(back.keys()))
print("guided ok:", "guided" in back and "opener" in back["guided"])
print("tier_guides ok:", set(back.get("tier_guides",{}).keys())=={"bronze","silver","gold"})
b=back["problem_bank"]
print("counts:",len(b["bronze"]),len(b["silver"]),len(b["gold"]))
print("B4 sol:", b["bronze"][4]["solutions"], "G0 sol:", b["gold"][0]["solutions"])
print("worked_examples preserved:", back.get("worked_examples")==pd.get("worked_examples"))
print("topic_links preserved:", back.get("topic_links")==pd.get("topic_links"))
print("svg on S2/G1/G4/opener:", "<svg" in b["silver"][2]["display"], "<svg" in b["gold"][1]["display"], "<svg" in b["gold"][4]["display"], "<svg" in back["guided"]["opener"]["display"])
