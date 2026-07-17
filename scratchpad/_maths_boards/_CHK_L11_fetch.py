import json, os, urllib.request

ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L11_live.json"
json.dump(pd, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs = pb.get(t) or pd.get(t)
    if isinstance(probs, list):
        print(t, "->", len(probs), "problems")
