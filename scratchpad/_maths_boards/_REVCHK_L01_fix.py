import json

base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_REVCHK_L01_live.json"
with open(base, encoding="utf-8") as f:
    pd = json.load(f)

s1 = pd["problem_bank"]["silver"][1]
mc = s1["misconceptions"][0]

# sanity: this is the with-replacement P(both blue) problem, correct 4/25
assert s1["solutions"] == [4, 25], s1["solutions"]
assert mc["pattern"] == "without_replacement", mc["pattern"]
assert mc["note"] == "used 4/10*3/9", mc["note"]

# Committing the error 4/10 * 3/9 = 12/90 = 2/15
old_expect = list(mc["expect"])
old_msg = mc["message"]
mc["expect"] = [2, 15]
mc["message"] = ("The ball is replaced, so the second pick is still 4/10: "
                 "4/10 × 4/10 = 4/25. Dropping the total gives 12/90 = 2/15, "
                 "the without-replacement answer.")

print("OLD expect:", old_expect, "-> NEW expect:", mc["expect"])
print("OLD msg:", old_msg)
print("NEW msg:", mc["message"])

# no em dashes in the new message
assert "—" not in mc["message"]

ship = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_probability-statistics-L01.json"
with open(ship, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("WROTE", ship)
