# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "7f378aaa-68dc-4420-b952-f56d8349b1ed"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-eduqas_geometry-L08_diagrams.json", encoding="utf-8"))

url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
vu = f"{url}&select=practice_data"
vr = urllib.request.Request(vu, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(vr))[0]["practice_data"]
pb = live["problem_bank"]
print("gold[4] options:", pb["gold"][4]["options"], "sol", pb["gold"][4]["solutions"])
print("gold[3] opt1:", pb["gold"][3]["options"][1])
print("gold[1] opt2:", pb["gold"][1]["options"][2])
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("bronze[0] hint:", pb["bronze"][0].get("hint"))
print("silver[0] display starts svg:", live["problem_bank"]["silver"][0]["display"][:10])
