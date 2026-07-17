import os, json, urllib.request

ID = "0a7ff82d-058f-480c-86fe-63a16ac98dc5"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_L06alg_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"), "| slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t, [])))
    print("  desc:", pb.get(t+"_description"))
print("has guided:", "guided" in pd, "| has tier_guides:", "tier_guides" in pd)
