import os, io, json, urllib.request

ID = "2ce07c9f-af5f-4162-ae95-544d91a71830"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd = json.load(io.open("lesson_maths-aqa_graphs-L08.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vurl = URL + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
back = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("keys back:", list(back.keys()))
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back)
print("bronze[7] sol:", back["problem_bank"]["bronze"][7]["solutions"])
print("charts present:", sum(1 for t in ("bronze","silver","gold") for p in back["problem_bank"][t] if "chart" in p))
print("svg figures:", sum(1 for t in ("bronze","silver","gold") for p in back["problem_bank"][t] if "<svg" in p.get("display","")) + ("<svg" in back["guided"]["opener"]["display"]))
