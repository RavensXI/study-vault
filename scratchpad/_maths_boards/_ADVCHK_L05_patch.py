import os, json, io, urllib.request
ID = "2e75898f-577a-42bd-b94e-f1435e89ace3"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("_ADVCHK_L05_fixed.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
print("PATCH status:", urllib.request.urlopen(req).status)

g = urllib.request.Request(f"{url}&select=practice_data", headers={"apikey": key, "Authorization": f"Bearer {key}"})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
st = live["guided"]["opener"]["steps"][1]
print("LIVE step[1] pre:", st["pre"])
print("LIVE step[1] answer:", st["answer"], "| hint:", st["hint"])
# preservation check vs the pre-existing live snapshot
snap = json.load(io.open("_ADVCHK_L05_live.json", encoding="utf-8"))
for f in ("related_videos", "topic_links", "worked_examples", "method_card", "tier_guides", "problem_bank"):
    a = json.dumps(snap.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f, "UNCHANGED" if a == b else "CHANGED")
# teach unchanged
a = json.dumps(snap["guided"].get("teach"), sort_keys=True, ensure_ascii=False)
b = json.dumps(live["guided"].get("teach"), sort_keys=True, ensure_ascii=False)
print("guided.teach", "UNCHANGED" if a == b else "CHANGED")
