import os, json, urllib.request

ID = "5ea35085-7e2c-4216-9829-f0eda94acb67"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_gL07_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=2, ensure_ascii=False)
print("title:", data[0].get("title"), "| slug:", data[0].get("slug"))
pd = data[0]["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb.get(t), list) else (pb.get(t,{}).get("problems") if isinstance(pb.get(t),dict) else None)
    print(t, "->", type(pb.get(t)))
