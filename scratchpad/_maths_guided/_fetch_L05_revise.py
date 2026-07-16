import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9f108e0c-d178-4685-8f65-1dc1a370d201"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_revise_L05_live.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))

# Inspect the three broken steps
for tier, idx in [("gold",0),("gold",4),("silver",5)]:
    prob = pd["problem_bank"][tier][idx]
    print("\n===", tier, idx, "===")
    print("display:", prob.get("display"))
    print("solutions:", prob.get("solutions"))
    steps = prob.get("guided_steps", [])
    for i, s in enumerate(steps):
        mark = " <<<" if i == 5 else ""
        print(f"  [{i}] {json.dumps(s, ensure_ascii=False)}{mark}")
