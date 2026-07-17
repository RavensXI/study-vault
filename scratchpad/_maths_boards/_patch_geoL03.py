import json, os, io, urllib.request
ID="28c3fccf-544d-4e44-a03f-635e88222391"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-aqa_geometry-L03.json", encoding="utf-8"))
body=json.dumps({"practice_data": pd}).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey":key,"Authorization":f"Bearer {key}",
  "Content-Type":"application/json","Prefer":"return=minimal"})
resp=urllib.request.urlopen(req)
print("PATCH status", resp.status)
# verify readback
url2=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req2=urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", sorted(back.keys()))
print("bronze", len(back["problem_bank"]["bronze"]), "gold has guided_steps:", "guided_steps" in back["problem_bank"]["gold"][0])
print("opener boxes:", sum(1 for s in back["guided"]["opener"]["steps"] if s.get("answer") is not None))
print("related_videos preserved:", len(back["related_videos"]), "worked_examples:", len(back["worked_examples"]))
