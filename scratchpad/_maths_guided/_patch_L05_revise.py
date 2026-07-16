import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9f108e0c-d178-4685-8f65-1dc1a370d201"
pd = json.load(open("lesson_ratio-proportion-L05.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# Re-fetch and confirm the three fixes landed
url2 = url + "&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey":key,"Authorization":f"Bearer {key}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
res = []
for t,i,exp in [("gold",0,"Check: 1 × 6² = 1 × 36 = "),
                ("gold",4,"Check: 2 × √36 = 2 × 6 = "),
                ("silver",5,"Check: 0.8 × 5² = 0.8 × 25 = ")]:
    got = live["problem_bank"][t][i]["guided_steps"][5]["pre"]
    res.append(f"{t}[{i}] match={got==exp}")
open("_patch_confirm.txt","w",encoding="utf-8").write(chr(10).join(res))
print("confirmed, see _patch_confirm.txt")
