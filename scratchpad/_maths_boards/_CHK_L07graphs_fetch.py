import os, json, urllib.request

ID = "660796ad-070d-4a2d-af11-900e5a5af1c1"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L07graphs_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    if t in pb:
        print(t, "count:", len(pb[t]))
