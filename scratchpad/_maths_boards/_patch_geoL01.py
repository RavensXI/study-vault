import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "498fd544-0137-4fe2-be55-f4861c72723f"
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_geometry-L01_maths-ocr.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify readback
r2 = urllib.request.Request(f"{url}&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(r2))[0]["practice_data"]
pbk = live["problem_bank"]
print("bronze n:", len(pbk["bronze"]), "silver n:", len(pbk["silver"]), "gold n:", len(pbk["gold"]))
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("bronze[6] sol:", pbk["bronze"][6]["solutions"], "display has svg:", "<svg" in pbk["bronze"][0]["display"])
print("worked_examples preserved:", len(live.get("worked_examples", [])), "related_videos:", live.get("related_videos"))
print("bronze_description present:", bool(pbk.get("bronze_description")))
