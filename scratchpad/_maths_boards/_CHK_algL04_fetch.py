import os, json, urllib.request

ID = "431cf470-df7f-4654-8c83-df7aeb1e0322"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_algL04_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("OK keys:", list(pd.keys()))
print("problem_bank tiers:", list(pd.get("problem_bank",{}).keys()) if isinstance(pd.get("problem_bank"),dict) else "n/a")
