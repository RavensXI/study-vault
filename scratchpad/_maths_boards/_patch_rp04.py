import os, json, urllib.request
ID="6f3f98f9-e772-40d9-8e54-b76a2ed3e8c7"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(open("lesson_maths-aqa_ratio-proportion-L04.json",encoding="utf-8"))
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
print("bronze n:",len(back["problem_bank"]["bronze"]),"silver:",len(back["problem_bank"]["silver"]),"gold:",len(back["problem_bank"]["gold"]))
print("descs:", all(back["problem_bank"].get(t+"_description") for t in ("bronze","silver","gold")))
print("silver[5] chart present:", "chart" in back["problem_bank"]["silver"][5])
print("worked_examples preserved:", back.get("worked_examples")==pd.get("worked_examples"))
print("related_videos preserved:", back.get("related_videos")==pd.get("related_videos"))
print("topic_links preserved:", back.get("topic_links")==pd.get("topic_links"))
