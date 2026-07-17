# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("_ps03e_shard.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
