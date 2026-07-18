import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ID = "123bb55f-1fc8-41fd-9b44-759bc466b766"

url = f"{BASE}?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

row = data[0]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_myL04_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(row, f, indent=1, ensure_ascii=False)
print("title:", row["title"], "| slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t, [])))
    for i,p in enumerate(pb.get(t,[])):
        print(f"  {t}[{i}] it={p.get('input_type')} sol={p.get('solutions')} unit={p.get('unit')} acc={p.get('accept')} ho={p.get('higher_only')} calc={p.get('calculator')}")
        print("     ", p.get("display","")[:160])
