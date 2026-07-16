import os, json, urllib.request

ID = "d9ac5103-221b-441e-81f2-d95e77269ea3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/_CHK_gL04_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("wrote", out)
print("top keys:", list(pd.keys()))

# pre-dump entry
pre = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/_pre_fanout_dump.json"
with open(pre, encoding="utf-8") as f:
    dump = json.load(f)
# find entry
entry = None
if isinstance(dump, dict):
    if ID in dump:
        entry = dump[ID]
    else:
        for k,v in dump.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry=v; break
elif isinstance(dump, list):
    for v in dump:
        if v.get("id")==ID:
            entry=v; break
print("predump found:", entry is not None)
if entry is not None:
    po = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/_CHK_gL04_predump.json"
    with open(po,"w",encoding="utf-8") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
    print("wrote", po)
    print("predump type:", type(entry).__name__, list(entry.keys())[:10] if isinstance(entry,dict) else "")
