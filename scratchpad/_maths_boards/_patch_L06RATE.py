# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "e15d6925-608b-4c05-aa82-c4782d1657b3"
SHARD = "lesson_maths-aqa_ratio-proportion-L06.json"
key = os.environ["SUPABASE_SERVICE_KEY"]
base = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"

pd = json.load(io.open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(base, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# Re-fetch and verify the fix landed
req2 = urllib.request.Request(base + "&select=practice_data", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
g1 = live["problem_bank"]["gold"][1]
m = g1["misconceptions"][0]
print("live gold[1].solutions:", g1["solutions"])
print("live misc expect:", m["expect"], "pattern:", m["pattern"])
print("live misc message:", m["message"])
assert m["expect"] == -3.625, m["expect"]
assert "−3.625" in m["message"], m["message"]
# preservation spot-check
print("topic_links:", json.dumps(live.get("topic_links")))
print("related_videos:", json.dumps(live.get("related_videos")))
print("worked_examples count:", len(live.get("worked_examples") or []))
print("VERIFIED")
