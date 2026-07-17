import json, os, urllib.request

LID = "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

# Fetch fresh
req = urllib.request.Request(f"{BASE}?id=eq.{LID}&select=practice_data", headers=H)
row = json.load(urllib.request.urlopen(req))[0]
pd = row["practice_data"]

gold1 = pd["problem_bank"]["gold"][1]
print("BEFORE options:", json.dumps(gold1["options"], ensure_ascii=False))
print("BEFORE solutions:", gold1["solutions"])

# Verify the maths from the display: A=(90/360)*200=50, B=(60/360)*300=50 => equal
assert (90/360)*200 == 50 and (60/360)*300 == 50

# Fix: keep option 0 (correct), replace duplicate-correct options 1 & 2 with
# genuine distractors. Keep option 3.
gold1["options"] = [
    "Equal: both have 50 fans",
    "School A has more, by 50",
    "School B has more, by 50",
    "School A has more by 10",
]
gold1["solutions"] = [0]

print("AFTER options:", json.dumps(gold1["options"], ensure_ascii=False))
print("AFTER solutions:", gold1["solutions"])

# Sanity: exactly one correct, all distinct
assert len(set(gold1["options"])) == 4
assert gold1["solutions"] == [0]

# Write shard
shard = "lesson_maths-aqa_probability-statistics-L03.json"
with open(shard, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("WROTE", shard)
