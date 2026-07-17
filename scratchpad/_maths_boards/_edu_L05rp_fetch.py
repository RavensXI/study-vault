import os, json, urllib.request

SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "93469b0d-2704-499c-a20b-587a84c2e214"

url = f"{SUPA}/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

pd = data[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_edu_L05rp_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze", "silver", "gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier} ({len(probs)}) ===")
    for i, p in enumerate(probs):
        print(f"[{i}] input_type={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("     display:", p.get("display","")[:160])
print("\nhas guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd)
