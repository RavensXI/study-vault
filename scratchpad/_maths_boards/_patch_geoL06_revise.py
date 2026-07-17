# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "6e4a84ec-b6c4-489b-9d86-0cc1a7fb65b0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-aqa_geometry-L06.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# readback
req2 = urllib.request.Request(url + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
pb = got["problem_bank"]
print("bronze[1] display a/b now:", "a = 12" in pb["bronze"][1]["display"], "b = 9" in pb["bronze"][1]["display"])
print("bronze[1] solutions:", pb["bronze"][1]["solutions"])
print("bronze[4] say:", pb["bronze"][4]["guided_steps"][0]["say"][:55])
print("silver[1] say:", pb["silver"][1]["guided_steps"][0]["say"][:60])
print("bronze[7] say:", pb["bronze"][7]["guided_steps"][0]["say"][:55])
print("readback == shard:", got == pd)
