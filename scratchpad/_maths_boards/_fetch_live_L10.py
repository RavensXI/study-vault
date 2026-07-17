import os, json, urllib.request

lid = "dd0172cd-6a81-41c6-ae9b-98de9328eb77"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{lid}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_maths-ocr_algebra-L10.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("wrote", out)
print("top keys:", list(pd.keys()))
