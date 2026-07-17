import os, json, io, urllib.request

LID = "1422954b-1171-49c2-a0c0-d5a1feb0da0d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_algebra-L08.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# read back and confirm
rurl = f"{url}&select=practice_data"
rr = urllib.request.Request(rurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
back = json.load(urllib.request.urlopen(rr))[0]["practice_data"]
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back)
print("bronze n:", len(back["problem_bank"]["bronze"]),
      "silver n:", len(back["problem_bank"]["silver"]),
      "gold n:", len(back["problem_bank"]["gold"]))
print("bronze[0] has guided_steps:", "guided_steps" in back["problem_bank"]["bronze"][0])
print("opener has svg:", "<svg" in back["guided"]["opener"]["display"])
print("worked_examples preserved:", len(back.get("worked_examples", [])))
