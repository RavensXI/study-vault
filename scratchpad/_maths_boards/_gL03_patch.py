import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "39bdcd12-eb3d-45b1-b0c5-d8e2257610df"
pd = json.load(open("lesson_maths-eduqas_graphs-L03.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify round-trip
u2 = url + "&select=practice_data"
req2 = urllib.request.Request(u2, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("live tier_guides?", "tier_guides" in live, "| guided.opener boxes?", sum(1 for s in live["guided"]["opener"]["steps"] if s.get("answer") is not None))
print("bronze[5] sol", live["problem_bank"]["bronze"][5]["solutions"], "| bronze[7] sol", live["problem_bank"]["bronze"][7]["solutions"])
print("silver[0] has chart?", "chart" in live["problem_bank"]["silver"][0])
