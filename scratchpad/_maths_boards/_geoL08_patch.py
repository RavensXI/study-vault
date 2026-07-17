# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "47a41e5d-3d22-45fd-a1c0-b29405585d87"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open('lesson_maths-ocr_geometry-L08.json', encoding='utf-8'))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode('utf-8')
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method='PATCH', headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("round-trip equal:", json.dumps(got, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False))
print("live keys:", sorted(got.keys()))
