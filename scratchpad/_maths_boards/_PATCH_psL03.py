import json, os, urllib.request

LID = "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

pd = json.load(open("lesson_maths-aqa_probability-statistics-L03.json", encoding="utf-8"))

body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(
    f"{BASE}?id=eq.{LID}",
    data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"},
)
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# Re-fetch to confirm live
req2 = urllib.request.Request(f"{BASE}?id=eq.{LID}&select=practice_data",
                              headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
g1 = live["problem_bank"]["gold"][1]
print("LIVE options:", json.dumps(g1["options"], ensure_ascii=False))
print("LIVE solutions:", g1["solutions"])
assert g1["options"] == ["Equal: both have 50 fans", "School A has more, by 50",
                         "School B has more, by 50", "School A has more by 10"]
assert g1["solutions"] == [0]
print("LIVE CONFIRMED")

changes = {
    "key": "probability-statistics-L03",
    "problems_fixed": [{
        "tier": "gold", "index": 1,
        "what": "Degenerate multiple choice: options 0,1,2 all stated the same correct conclusion (both schools equal at 50 fans) but only solutions=[0] was keyed, so a student picking equally-true option 1 or 2 was wrongly marked wrong. Replaced options 1 and 2 with genuine distractors.",
        "old": ["Equal: both have 50 fans", "School A has 50, School B has 50, they are equal", "School B has 50 vs School A's 50, they are equal", "School A has more by 10"],
        "new": ["Equal: both have 50 fans", "School A has more, by 50", "School B has more, by 50", "School A has more by 10"],
    }],
    "issues_resolved": 1,
    "opener_concept": "unchanged",
    "notes": "Revision-only pass. Maths verified: School A=(90/360)x200=50, School B=(60/360)x300=50, equal; option 0 remains the sole correct answer. All other verified-clean items (20 solutions, all boxes/expects, figures, preservation) untouched; only gold[1].options/solutions changed. Validator PASS; PATCHed practice_data only; live re-fetch confirmed.",
}
with open("changes_maths-aqa_probability-statistics-L03.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, ensure_ascii=False, indent=2)
print("WROTE changes file")
