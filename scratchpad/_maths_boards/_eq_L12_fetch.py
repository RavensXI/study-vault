import os, json, urllib.request

ID = "66a1ec53-d20f-4b82-b436-1b31fc88e998"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_eq_L12_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    arr = pb.get(tier, [])
    print(f"\n=== {tier} ({len(arr)}) ===")
    for i,p in enumerate(arr):
        print(i, "|", p.get("input_type"), "| calc=", p.get("calculator"), "| sol=", p.get("solutions"))
        print("    disp:", p.get("display"))
