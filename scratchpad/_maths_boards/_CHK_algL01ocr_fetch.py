import os, json, urllib.request

SID = "d8a78aa2-a642-4dcd-9cb0-1aa5990761e7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
print("slug:", data[0].get("slug"), "title:", data[0].get("title"))
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_algL01ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ("bronze","silver","gold"):
    v = pb.get(t) if isinstance(pb, dict) else None
    if isinstance(v, list):
        print(t, "count", len(v))
print("wrote", out)
