import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "498fd544-0137-4fe2-be55-f4861c72723f"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_geoL01_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, indent=1, ensure_ascii=False)
pd = row["practice_data"]
print("title:", row.get("title"), "slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"[{i}] it={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("    ", p.get("display","")[:200])
