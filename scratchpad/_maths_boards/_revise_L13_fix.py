# Revise algebra-L13 (maths-eduqas): fix figure viewBox clip + silver[2] duplicate distractor
import json

SRC = "_eduqas_L13_live.json"   # freshest live fetch
OUT = "lesson_maths-eduqas_algebra-L13.json"

pd = json.load(open(SRC, encoding="utf-8"))

# ---- Defect 1 (fatal): bronze teach SVG clips its 7th dot of pattern 3 ----
bd = pd["guided"]["teach"]["bronze"]["display"]
assert 'viewBox="0 0 285 78"' in bd, "viewBox anchor not found"
bd2 = bd.replace('viewBox="0 0 285 78"', 'viewBox="0 0 300 78"')
# 7th dot cx=288 r=5 spans x=283..293 -> now inside 300-wide viewBox
assert 'cx="288.0"' in bd2, "7th dot missing"
pd["guided"]["teach"]["bronze"]["display"] = bd2

# ---- Defect 2 (minor): silver[2] options[1] and options[2] were identical (20-3n) ----
s2 = pd["problem_bank"]["silver"][2]
assert s2["options"] == ["\\(23 - 3n\\)", "\\(20 - 3n\\)", "\\(-3n + 20\\)", "\\(3n + 20\\)"], s2["options"]
# Replace the duplicate (-3n+20 == 20-3n) with a genuinely distinct distractor.
# 17-3n = adding d to the first term instead of subtracting to find the constant:
#   wrong constant = 20 + (-3) = 17 (should be 20 - (-3) = 23). At n=1 gives 14, not 20. Distinct value.
s2["options"][2] = "\\(17 - 3n\\)"
# Diagnose the new distractor honestly (expect = its option index 2).
s2["misconceptions"].append({
    "check": "common",
    "expect": 2,
    "message": "To find the constant, take first term minus d = 20 − (−3) = 23, not first term plus d = 17. Check n = 1: 23 − 3 = 20. The rule is 23 − 3n.",
    "pattern": "added_d_to_first_term",
})

# sanity: all four options now distinct
opts = s2["options"]
assert len(set(opts)) == 4, opts
# solution still index 0 (23-3n)
assert s2["solutions"] == [0]

json.dump(pd, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
print("options now:", opts)
print("misconception expects:", [m["expect"] for m in s2["misconceptions"]])
