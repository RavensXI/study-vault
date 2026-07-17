# -*- coding: utf-8 -*-
import json, os, io, urllib.request
ID="1e9d6465-1ec1-40a3-8138-958197366837"
key=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open("lesson_maths-eduqas_geometry-L03.json",encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey":key,"Authorization":f"Bearer {key}",
    "Content-Type":"application/json","Prefer":"return=minimal"})
resp=urllib.request.urlopen(req)
print("PATCH status:", resp.status)
# verify
vurl=f"{url}&select=practice_data"
vreq=urllib.request.Request(vurl, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
pbl=live["problem_bank"]
print("live tiers:", {t:len(pbl[t]) for t in ("bronze","silver","gold")})
print("b0 input_type:", pbl["bronze"][0]["input_type"], "sol:", pbl["bronze"][0]["solutions"])
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("svg count:", json.dumps(live).count("<svg"))
