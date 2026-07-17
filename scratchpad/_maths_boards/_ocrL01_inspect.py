import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]

def fetch(lid):
    url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{lid}&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

pd = json.load(io.open("_ocrL01_live.json", encoding="utf-8"))
print("=== OCR live full bronze[0] ===")
print(json.dumps(pd["problem_bank"]["bronze"][0], ensure_ascii=False, indent=1))
print("\n=== top-level keys ===", list(pd.keys()))
print("method_card keys:", list(pd.get("method_card", {}).keys()))
print("guided present?", "guided" in pd, "tier_guides?", "tier_guides" in pd)
# Fetch shipped AQA sibling
aqa = fetch("f4f1368e-d7c2-41f1-8459-de2c0d500c3b")
json.dump(aqa, io.open("_aqaL01_shipped.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n=== AQA shipped keys ===", list(aqa.keys()))
