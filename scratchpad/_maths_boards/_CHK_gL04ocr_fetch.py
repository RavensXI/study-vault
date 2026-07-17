import os, json, urllib.request

ID = "9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_gL04ocr_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("rows", len(data))
pd = data[0]["practice_data"]
print("title", data[0].get("title"))
print("top keys", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb and isinstance(pb[t], list):
        print(t, "problems", len(pb[t]))
