import os, json, urllib.request

ID = "0334612d-1b10-4495-8d37-21ef41d3a925"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(URL, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))[0]
out = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_G4_live.json"
json.dump(data, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
pd = data["practice_data"]
print("title:", data["title"], "slug:", data.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()) if isinstance(pb,dict) else type(pb))
for t in ("bronze","silver","gold"):
    probs = None
    if isinstance(pb,dict): probs = pb.get(t)
    if probs is None: probs = pd.get(t)
    if isinstance(probs, list):
        print(t, "->", len(probs), "problems")
