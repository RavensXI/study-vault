import json, io

live = json.load(io.open("_ADVCHK_L05_live.json", encoding="utf-8"))
st = live["guided"]["opener"]["steps"][1]

# BEFORE
assert st["pre"] == "Halfway between the middle two of those (6 and 8) is ", repr(st["pre"])
assert st["answer"] == 7, st["answer"]
assert st["hint"] == "The value exactly between 6 and 8.", repr(st["hint"])

# Lower half of 3,5,6,8,10,12,15,18,20 is {3,5,6,8}; Q1 = median = (5+6)/2 = 5.5.
# The middle two of the lower four are 5 and 6, NOT 6 and 8.
st["pre"] = "Halfway between the middle two of those (5 and 6) is "
st["answer"] = 5.5
st["hint"] = "The value exactly between 5 and 6."

json.dump(live, io.open("_ADVCHK_L05_fixed.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("FIXED step[1]:", json.dumps({k: st.get(k) for k in ("pre", "answer", "hint")}, ensure_ascii=False))
print("step[2] reveal unchanged:", live["guided"]["opener"]["steps"][2]["say"][:60], "...")
