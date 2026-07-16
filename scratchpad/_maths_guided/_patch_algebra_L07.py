import os, json, io, urllib.request
ID="5cb3f019-6030-4136-8917-af379ab9e503"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_algebra-L07.json",encoding="utf-8"))
body=json.dumps({"practice_data":pd},ensure_ascii=False).encode("utf-8")
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req=urllib.request.Request(url,data=body,method="PATCH",headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
r=urllib.request.urlopen(req)
print("PATCH status",r.status)

# read back and confirm
req2=urllib.request.Request(url+"&select=practice_data",headers={"apikey":key,"Authorization":f"Bearer {key}"})
back=json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:", "guided" in back, "| has tier_guides:", "tier_guides" in back)
print("bronze b0 misconceptions:", [m["pattern"] for m in back["problem_bank"]["bronze"][0]["misconceptions"]])
print("gold g1 misconceptions:", [m["pattern"] for m in back["problem_bank"]["gold"][1]["misconceptions"]])
# confirm no not_rearranged anywhere
pats=[m["pattern"] for t in ("bronze","silver","gold") for p in back["problem_bank"][t] for m in (p.get("misconceptions") or [])]
print("not_rearranged remaining:", pats.count("not_rearranged"))
print("worked_examples preserved count:", len(back["worked_examples"]))
print("related_videos preserved count:", len(back["related_videos"]))
