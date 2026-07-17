import json, os, urllib.request

ID = "d2ed09e5-eea7-4e13-a9b6-2437ace7f664"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
pd = row["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_LIVE_L05.json"
json.dump(pd, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", row.get("title"), "| slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) or pb.get(t+"_problems") or []
    if isinstance(probs, dict): probs=probs.get("problems",[])
    print(f"  {t}: {len(probs) if isinstance(probs,list) else 'n/a'} problems")
