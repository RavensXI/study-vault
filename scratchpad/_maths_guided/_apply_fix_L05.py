import json

SHARD = "lesson_ratio-proportion-L05.json"
pd = json.load(open(SHARD, encoding="utf-8"))

fixes = [
    ("gold", 0, "Check: 1 × 3² = 1 × 9 = ",
                "Check: 1 × 6² = 1 × 36 = ", 36),
    ("gold", 4, "Check: 2 × √9 = 2 × 3 = ",
                "Check: 2 × √36 = 2 × 6 = ", 12),
    ("silver", 5, "Check: 0.8 × 2² = 0.8 × 4 = ",
                  "Check: 0.8 × 5² = 0.8 × 25 = ", 20),
]

applied = []
for tier, idx, old_pre, new_pre, ans in fixes:
    step = pd["problem_bank"][tier][idx]["guided_steps"][5]
    assert step["pre"] == old_pre, f"{tier}[{idx}][5] pre mismatch: {step['pre']!r}"
    assert step["answer"] == ans, f"{tier}[{idx}][5] answer mismatch: {step['answer']!r}"
    step["pre"] = new_pre
    applied.append((tier, idx, old_pre, new_pre))

json.dump(pd, open(SHARD, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# Recompute-verify: parse the "a * b = c" arithmetic in the new pre and confirm == stored answer == k
def verify(new_pre, ans):
    # new_pre like "Check: 1 × 6² = 1 × 36 = " -> last product "1 × 36"
    body = new_pre.replace("Check:", "").strip().rstrip("= ").strip()
    last = body.split("=")[-1].strip()  # "1 × 36"
    a, b = last.split("×")
    prod = float(a.strip()) * float(b.strip())
    return prod == ans

for tier, idx, old_pre, new_pre in applied:
    ans = pd["problem_bank"][tier][idx]["guided_steps"][5]["answer"]
    ok = verify(new_pre, ans)
    print(f"{tier}[{idx}][5]: {new_pre!r} answer={ans} recompute_ok={ok}")

print("all applied:", len(applied))
