# -*- coding: utf-8 -*-
import os, json, urllib.request

SID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}"

# 1. Fetch FRESH
req = urllib.request.Request(BASE + "&select=practice_data",
                             headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    pd = json.load(r)[0]["practice_data"]

MINUS = "−"  # U+2212 proper minus

# ---- Edit A: gold[1].misconceptions pattern 'used_total' (expect 2 = £24) ----
gold1 = pd["problem_bank"]["gold"][1]
assert "Amy" in gold1["display"] and "5 : 3" in gold1["display"], gold1["display"]
matches = [m for m in gold1["misconceptions"] if m.get("pattern") == "used_total"]
assert len(matches) == 1, matches
mA = matches[0]
assert mA["expect"] == 2, mA
mA["pattern"] = "difference_as_share"
mA["message"] = (
    "You treated the £40 as Amy's whole share and divided by her 5 parts: "
    "40 ÷ 5 = £8, then Beth = 3 × £8 = £24. But £40 is the "
    f"difference, worth 5 {MINUS} 3 = 2 parts, so one part = £20 and Beth = "
    "3 × £20 = £60."
)
# reproduce check: 40/5=8, 3*8=24 -> option index 2 == expect
assert (40 // 5) * 3 == 24 and gold1["options"][2] == "\\(\\pounds24\\)"

# ---- Edit B: silver[5].misconceptions pattern 'forgot_total' (expect 3 = 14 kg) ----
silver5 = pd["problem_bank"]["silver"][5]
assert "cement" in silver5["display"] and "1 : 2 : 4" in silver5["display"], silver5["display"]
matches = [m for m in silver5["misconceptions"] if m.get("pattern") == "forgot_total"]
assert len(matches) == 1, matches
mB = matches[0]
assert mB["expect"] == 3, mB
mB["pattern"] = "left_out_own_part"
mB["message"] = (
    "You added only the other parts, 1 + 4 = 5, leaving sand's own 2 out of the "
    "total. Every part counts: 1 + 2 + 4 = 7, so one part = 5 kg and sand = "
    "2 × 5 = 10 kg."
)
# reproduce check: total wrongly 1+4=5, 35/5=7, sand 2*7=14 -> option index 3
assert (35 // (1 + 4)) * 2 == 14 and silver5["options"][3] == "14 kg"

# 2. Write shard
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_ratio-proportion-L01.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("shard written:", out)
print("A new pattern:", mA["pattern"], "| expect", mA["expect"])
print("A msg:", mA["message"])
print("B new pattern:", mB["pattern"], "| expect", mB["expect"])
print("B msg:", mB["message"])
