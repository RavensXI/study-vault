import os, json, urllib.request

SID = "1a8441e6-115c-473e-a9b7-a2276e5b7faa"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}&select=practice_data,slug,title,unit_id"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_psL02ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"))
print("slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs = pb.get(t)
    if isinstance(probs, list):
        print(f"{t}: {len(probs)} problems")
