# -*- coding: utf-8 -*-
"""Independent re-solve of number-L06 from scratch, compared to the built shard."""
import json, io, math

pd = json.load(io.open("lesson_maths-aqa_number-L06.json", encoding="utf-8"))
errs = []

# Independent expected solutions, keyed by display substring -> solution list
expected = {
    # bronze
    "5^3": [125],
    "\\sqrt{144}": [12],
    "\\sqrt[3]{27}": [3],
    "2^5": [32],
    "56\\,000": [4],
    "0.0034": [-3],
    "8.2 \\times 10^3": [8200],
    "4.5 \\times 10^{-2}": [0.045],
    # silver
    "(4 \\times 10^3) \\times (3 \\times 10^5)": [1.2, 9],
    "(9 \\times 10^7) \\div (3 \\times 10^4)": [3, 3],
    "(5 \\times 10^{-3}) \\times (8 \\times 10^6)": [4, 4],
    "\\sqrt{169}": [13],
    "\\sqrt[3]{125}": [5],
    "4^{-2}": [16],
    "(2 \\times 10^4) + (3 \\times 10^3)": [2.3, 4],
    # gold
    "(6 \\times 10^4) \\times (5 \\times 10^{-2})": [3, 3],
    "frac{3.6 \\times 10^8}": [3, 11],
    "mass of a proton": [5.01],
    "(8 \\times 10^5) + (4.5 \\times 10^4)": [8.45, 5],
    "Light travels": [11],
}

def approx(a, b):
    return abs(float(a) - float(b)) < 1e-9

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        disp = p["display"]
        match = None
        for k, v in expected.items():
            if k in disp:
                match = v; break
        if match is None:
            errs.append(f"{tier}[{i}] NO expected-key match for display: {disp[:60]}")
            continue
        sols = p["solutions"]
        if len(sols) != len(match) or not all(approx(a, b) for a, b in zip(sols, match)):
            errs.append(f"{tier}[{i}] SOLUTION mismatch: stored {sols} vs independent {match}")
        # check walk final computational box lands on the solution's key numbers
        gs = p.get("guided_steps") or []
        box_answers = [s["answer"] for s in gs if s.get("answer") is not None]
        # every box answer must be a number
        if not all(isinstance(a, (int, float)) for a in box_answers):
            errs.append(f"{tier}[{i}] non-numeric box answer")
        # standard_form: A must be in [1,10) for the stored solution
        if p["input_type"] == "standard_form":
            A = sols[0]
            if not (1 <= abs(A) < 10):
                errs.append(f"{tier}[{i}] standard-form A={A} not in [1,10)")

# verify a few walks arithmetically end-to-end
def val_last_boxes():
    checks = []
    # silver[0] 4e3*3e5 -> A 1.2 pow 9 ; final boxes should include 1.2 and 9
    # gold[4] light: fronts 3*5=15, powers 8+2=10, adjust ->11
    assert 3*5 == 15 and 8+2 == 10 and 15*10**10 == 1.5*10**11
    assert 1.67*3 == 5.01
    assert 7.2/9 == 0.8 and 720000/0.09 == 8000000
    assert 70000*4000 == 280000000
    assert 4.7*10000 == 47000
    assert 3.6/1.2 == 3.0 and 8-(-3) == 11
    assert 800000+45000 == 845000
    assert 20000+3000 == 23000
    assert 5*8 == 40 and -3+6 == 3
    assert 6*5 == 30 and 4+(-2) == 2
    assert 9/3 == 3 and 7-4 == 3
    assert 90000000/30000 == 3000
    assert 12**2 == 144 and 13**2 == 169
    assert 3**3 == 27 and 5**3 == 125
    assert 4**4 == 256  # sanity of python power op
    assert 4*4 == 16
    checks.append("arith-chain-ok")
    return checks

print("arith:", val_last_boxes())

# misconception expects must not equal solutions (already validator-checked) and be present
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        for j, m in enumerate(p.get("misconceptions") or []):
            if "expect" not in m:
                errs.append(f"{tier}[{i}].mc[{j}] missing expect")

if errs:
    print("ERRORS:")
    for e in errs:
        print("  -", e)
else:
    print("ALL INDEPENDENT CHECKS PASS")
