# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_edu_L05rp_live.json", encoding="utf-8"))

# ---- preserved byte-for-byte ----
topic_links = live["topic_links"]
related_videos = live["related_videos"]
# worked_examples preserved, but em dashes in step labels ("Step 1 — Equation")
# violate the hard no-em-dash rule; replace with a colon (minimal, content intact).
worked_examples = live["worked_examples"]
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d

def say(s):
    return {"say": s}

# ============ BRONZE ============
bronze = [
 { # B0
  "display": r"\(y \propto x^2\). When \(x = 2\), \(y = 12\). Find \(y\) when \(x = 5\).",
  "solutions": [75], "calculator": False, "input_type": "single_value",
  "hint": "Find k first (12 ÷ 2²), then use it with x = 5.",
  "misconceptions": [
   {"pattern": "used_direct", "expect": 30, "message": "y = kx², not kx. k = 12 ÷ 2² = 3, then y = 3 × 25 = 75."},
   {"pattern": "forgot_square_new", "expect": 15, "message": "Square the new x too: 5² = 25, then y = 3 × 25 = 75."}],
  "guided_steps": [
   say("y ∝ x² means y = kx². Find k from x = 2, y = 12."),
   box("2² = ", 4, "2 × 2."),
   box("k = 12 ÷ 4 = ", 3, "Divide y by the squared x."),
   box("Now x = 5: 5² = 25, so y = 3 × 25 = ", 75, "k times the new x².", phase="substitute"),
   box("Check: 75 ÷ 25 = ", 3, "y ÷ x² gives k again.", done="Same k = 3 from both pairs, so y = 75 is right.")]},
 { # B1
  "display": r"\(y \propto x^2\). When \(x = 3\), \(y = 45\). Find \(k\).",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Square the x (3² = 9), then divide y by it.",
  "misconceptions": [
   {"pattern": "divided_by_x", "expect": 15, "message": "Divide by x², not x: 45 ÷ 3² = 45 ÷ 9 = 5."}],
  "guided_steps": [
   say("y ∝ x² means y = kx². Put the pair in to find k."),
   box("3² = ", 9, "3 × 3."),
   box("k = 45 ÷ 9 = ", 5, "Divide y by the squared x."),
   box("Check: 5 × 9 = ", 45, "k times x² rebuilds y.", phase="substitute"),
   box("If x = 2, y = 5 × 2² = 5 × 4 = ", 20, "Use y = 5x².", done="Rebuilds y = 45 at x = 3, so k = 5 is right.")]},
 { # B2
  "display": r"\(y = 4x^2\). Find \(y\) when \(x = 3\).",
  "solutions": [36], "calculator": False, "input_type": "single_value",
  "hint": "Square the 3 first, then multiply by 4.",
  "misconceptions": [
   {"pattern": "mult_then_square", "expect": 144, "message": "Square only x: 3² = 9, then 4 × 9 = 36, not (4 × 3)²."},
   {"pattern": "forgot_square", "expect": 12, "message": "Square x first: 3² = 9, then 4 × 9 = 36."}],
  "guided_steps": [
   say("y = 4x² already gives k = 4. Put x = 3 in."),
   box("3² = ", 9, "3 × 3."),
   box("y = 4 × 9 = ", 36, "Multiply 4 by the squared x."),
   box("Check: 36 ÷ 4 = ", 9, "y ÷ 4 returns x².", phase="substitute"),
   box("√9 = ", 3, "Square root of 9.", done="Back to x = 3, so y = 36 is right.")]},
 { # B3
  "display": r"\(y \propto x^2\). When \(x = 4\), \(y = 48\). Find \(y\) when \(x = 6\).",
  "solutions": [108], "calculator": False, "input_type": "single_value",
  "hint": "Find k (48 ÷ 4²), then use it with x = 6.",
  "misconceptions": [
   {"pattern": "used_direct", "expect": 72, "message": "y = kx², not kx. k = 48 ÷ 16 = 3, then y = 3 × 36 = 108."},
   {"pattern": "forgot_square_new", "expect": 18, "message": "Square the new x: 6² = 36, then y = 3 × 36 = 108."}],
  "guided_steps": [
   say("y = kx². Find k from x = 4, y = 48."),
   box("4² = ", 16, "4 × 4."),
   box("k = 48 ÷ 16 = ", 3, "Divide y by the squared x."),
   box("Now x = 6: 6² = 36, y = 3 × 36 = ", 108, "k times the new x².", phase="substitute"),
   box("Check: 108 ÷ 36 = ", 3, "y ÷ x² gives k again.", done="Same k = 3 from both pairs, so y = 108 is right.")]},
 { # B4
  "display": r"\(y \propto x^2\). When \(x = 5\), \(y = 50\). Find \(x\) when \(y = 32\).",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Find k (50 ÷ 5²), then solve 32 = kx² and square root.",
  "misconceptions": [
   {"pattern": "forgot_root", "expect": 16, "message": "x² = 16 means x = √16 = 4, not 16."},
   {"pattern": "divided_by_x", "expect": None, "message": "k = 50 ÷ 5² = 2, not 50 ÷ 5. Then 32 = 2x², x = 4."}],
  "guided_steps": [
   say("y = kx². Find k from x = 5, y = 50."),
   box("5² = ", 25, "5 × 5."),
   box("k = 50 ÷ 25 = ", 2, "Divide y by the squared x."),
   box("Now 32 = 2x², so x² = 32 ÷ 2 = ", 16, "Divide the new y by k."),
   box("Square root: x = √16 = ", 4, "What squares to 16?", phase="substitute"),
   box("Check: 2 × 4² = 2 × 16 = ", 32, "k times x² rebuilds y.", done="Rebuilds y = 32, so x = 4 is right.")]},
 { # B5
  "display": r"\(y \propto \sqrt{x}\). When \(x = 9\), \(y = 6\). Find \(y\) when \(x = 25\).",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Find k (6 ÷ √9), then multiply by √25.",
  "misconceptions": [
   {"pattern": "forgot_root_new", "expect": 50, "message": "Use √25 = 5, not 25. Then y = 2 × 5 = 10."}],
  "guided_steps": [
   say("y ∝ √x means y = k√x. Find k from x = 9, y = 6."),
   box("√9 = ", 3, "What number times itself is 9?"),
   box("k = 6 ÷ 3 = ", 2, "Divide y by the root."),
   box("Now x = 25: √25 = 5, y = 2 × 5 = ", 10, "k times the new root.", phase="substitute"),
   box("Check: 10 ÷ 5 = ", 2, "y ÷ √x gives k.", done="Same k = 2, so y = 10 is right.")]},
 { # B6  (CHANGED y=75 -> y=108 so answer 6, not duplicate 5)
  "display": r"\(y = 3x^2\). Find \(x\) when \(y = 108\).",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Divide y by 3 to get x², then square root.",
  "misconceptions": [
   {"pattern": "forgot_root", "expect": 36, "message": "x² = 36 means x = √36 = 6, not 36."}],
  "guided_steps": [
   say("y = 3x², so k = 3. Put y = 108 in and solve for x."),
   box("x² = 108 ÷ 3 = ", 36, "Divide y by 3."),
   box("Square root: x = √36 = ", 6, "What squares to 36?", phase="substitute"),
   box("Check: 3 × 6² = 3 × 36 = ", 108, "3 times x² rebuilds y.", done="Rebuilds y = 108, so x = 6 is right.")]},
 { # B7  (CHANGED y=40 -> y=56 so answer 7, not duplicate 5)
  "display": r"\(y \propto x^3\). When \(x = 2\), \(y = 56\). Find \(k\).",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Cube the x (2³ = 8), then divide y by it.",
  "misconceptions": [
   {"pattern": "divided_by_x", "expect": 28, "message": "Divide by x³, not x: 56 ÷ 2³ = 56 ÷ 8 = 7."},
   {"pattern": "squared_not_cubed", "expect": 14, "message": "x is cubed: 2³ = 8, not 4. Then k = 56 ÷ 8 = 7."}],
  "guided_steps": [
   say("y ∝ x³ means y = kx³. Cube x, then find k."),
   box("2³ = 2 × 2 × 2 = ", 8, "Multiply three 2s."),
   box("k = 56 ÷ 8 = ", 7, "Divide y by the cubed x."),
   box("Check: 7 × 8 = ", 56, "k times x³ rebuilds y.", phase="substitute"),
   box("If x = 1, y = 7 × 1³ = ", 7, "Use y = 7x³.", done="Rebuilds y = 56 at x = 2, so k = 7 is right.")]},
]

# ============ SILVER ============
silver = [
 { # S0
  "display": r"\(y \propto \frac{1}{x^2}\). When \(x = 2\), \(y = 5\). Find \(y\) when \(x = 4\).",
  "solutions": [1.25], "calculator": False, "input_type": "single_value",
  "hint": "k = y × x² = 5 × 2² = 20. Then divide by 4².",
  "misconceptions": [
   {"pattern": "used_direct", "expect": 20, "message": "Inverse: k = y × x² = 20, not y ÷ x². Then y = 20 ÷ 16 = 1.25."},
   {"pattern": "forgot_square_new", "expect": 5, "message": "Square the new x: 4² = 16, then y = 20 ÷ 16 = 1.25."}],
  "guided_steps": [
   say("Inverse square: y = k/x², so k = y × x². Use x = 2, y = 5."),
   box("2² = ", 4, "2 × 2."),
   box("k = 5 × 4 = ", 20, "y times x² for inverse."),
   box("Now x = 4: 4² = 16, y = 20 ÷ 16 = ", 1.25, "k ÷ the new x².", phase="substitute"),
   box("Check: 1.25 × 16 = ", 20, "y times x² rebuilds k.", done="Same k = 20, so y = 1.25 is right.")]},
 { # S1
  "display": r"\(y \propto x^3\). When \(x = 2\), \(y = 40\). Find \(y\) when \(x = 3\).",
  "solutions": [135], "calculator": False, "input_type": "single_value",
  "hint": "k = 40 ÷ 2³ = 5, then multiply by 3³.",
  "misconceptions": [
   {"pattern": "squared_not_cubed", "expect": 90, "message": "Cube, do not square: k = 40 ÷ 2³ = 5, then y = 5 × 3³ = 135."},
   {"pattern": "scaled_linear", "expect": 60, "message": "Use y = 5x³: 5 × 27 = 135, not 40 × (3 ÷ 2)."}],
  "guided_steps": [
   say("Cubic: y = kx³. Find k from x = 2, y = 40."),
   box("2³ = ", 8, "2 × 2 × 2."),
   box("k = 40 ÷ 8 = ", 5, "Divide y by the cubed x."),
   box("Now x = 3: 3³ = 27, y = 5 × 27 = ", 135, "k times the new x³.", phase="substitute"),
   box("Check: 135 ÷ 27 = ", 5, "y ÷ x³ gives k.", done="Same k = 5, so y = 135 is right.")]},
 { # S2
  "display": r"\(y \propto \frac{1}{x}\). When \(x = 3\), \(y = 8\). Find \(x\) when \(y = 4\).",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "k = x × y = 24. Then x = k ÷ y.",
  "misconceptions": [
   {"pattern": "mult_not_div", "expect": 96, "message": "After k = 24, divide: x = 24 ÷ 4 = 6, not 24 × 4."},
   {"pattern": "used_direct", "expect": 1.5, "message": "Inverse: if y halves, x doubles. k = 24, x = 24 ÷ 4 = 6."}],
  "guided_steps": [
   say("Inverse: y = k/x, so k = x × y. Find k from x = 3, y = 8."),
   box("k = 3 × 8 = ", 24, "Multiply the pair for inverse."),
   box("Now y = 4: x = 24 ÷ 4 = ", 6, "Divide k by the new y.", phase="substitute"),
   box("Check: 6 × 4 = ", 24, "x times y should give k again.", done="Same k = 24, so x = 6 is right.")]},
 { # S3
  "display": r"\(y \propto \sqrt{x}\). When \(x = 16\), \(y = 12\). Find \(y\) when \(x = 100\).",
  "solutions": [30], "calculator": False, "input_type": "single_value",
  "hint": "k = 12 ÷ √16 = 3, then multiply by √100.",
  "misconceptions": [
   {"pattern": "used_x", "expect": 75, "message": "Use √x: k = 12 ÷ √16 = 3, then y = 3 × √100 = 30."},
   {"pattern": "forgot_root_new", "expect": 300, "message": "Root the new x: √100 = 10, then y = 3 × 10 = 30."}],
  "guided_steps": [
   say("Root: y = k√x. Find k from x = 16, y = 12."),
   box("√16 = ", 4, "What number times itself is 16?"),
   box("k = 12 ÷ 4 = ", 3, "Divide y by the root."),
   box("Now x = 100: √100 = 10, y = 3 × 10 = ", 30, "k times the new root.", phase="substitute"),
   box("Check: 30 ÷ 10 = ", 3, "y ÷ √x gives k.", done="Same k = 3, so y = 30 is right.")]},
 { # S4  (multiplier: single_value numeric answer 9)
  "display": r"\(y \propto x^2\). When \(x\) is tripled, \(y\) is multiplied by:",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "Tripling x multiplies x² by 3², so find 3².",
  "misconceptions": [
   {"pattern": "linear", "expect": 3, "message": "y depends on x², so tripling x multiplies y by 3² = 9, not 3."},
   {"pattern": "used_cube", "expect": 27, "message": "It is x² not x³: tripling multiplies y by 3² = 9, not 3³."}],
  "guided_steps": [
   say("y = kx². If x triples, x² is multiplied by 3²."),
   box("3² = ", 9, "3 × 3."),
   box("Take k = 1 and x = 2: y = 1 × 2² = ", 4, "1 × 4."),
   box("Triple x to 6: y = 1 × 6² = ", 36, "1 × 36.", phase="substitute"),
   box("36 ÷ 4 = ", 9, "New y ÷ old y.", done="y multiplied by 9, matching 3².")]},
 { # S5
  "display": r"\(y \propto \frac{1}{x^2}\). When \(x = 1\), \(y = 36\). Find \(x\) when \(y = 4\).",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "k = y × x² = 36. Then 4 = 36 ÷ x², solve and square root.",
  "misconceptions": [
   {"pattern": "forgot_root", "expect": 9, "message": "x² = 9 means x = √9 = 3, not 9."},
   {"pattern": "mult_not_div", "expect": 12, "message": "4 = 36 ÷ x² gives x² = 9, so x = 3, not √(36 × 4)."}],
  "guided_steps": [
   say("Inverse square: y = k/x², so k = y × x². Use x = 1, y = 36."),
   box("k = 36 × 1² = ", 36, "36 × 1."),
   box("Now 4 = 36 ÷ x², so x² = 36 ÷ 4 = ", 9, "Divide k by the new y."),
   box("Square root: x = √9 = ", 3, "What squares to 9?", phase="substitute"),
   box("Check: 36 ÷ 3² = 36 ÷ 9 = ", 4, "k ÷ x² rebuilds y.", done="Rebuilds y = 4, so x = 3 is right.")]},
 { # S6
  "display": r"The force \(F\) between two magnets is inversely proportional to \(d^2\). When \(d = 2\), \(F = 20\). Find \(F\) when \(d = 4\).",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "k = F × d² = 20 × 2² = 80. Then divide by 4².",
  "misconceptions": [
   {"pattern": "used_direct", "expect": 40, "message": "Inverse: as d doubles, F is quartered. F = 80 ÷ 16 = 5."},
   {"pattern": "halved", "expect": 10, "message": "Inverse square: doubling d divides F by 2² = 4. F = 20 ÷ 4 = 5."}],
  "guided_steps": [
   say("Inverse square: F = k/d², so k = F × d². Use d = 2, F = 20."),
   box("2² = ", 4, "2 × 2."),
   box("k = 20 × 4 = ", 80, "F times d² for inverse."),
   box("Now d = 4: 4² = 16, F = 80 ÷ 16 = ", 5, "k ÷ the new d².", phase="substitute"),
   box("Check: 5 × 16 = ", 80, "F times d² rebuilds k.", done="Same k = 80, so F = 5 is right.")]},
]

# ============ GOLD ============
gold = [
 { # G0  KEEP multiple_choice (answer is an expression 9b)
  "display": r"\(y \propto x^2\). When \(x = a\), \(y = b\). Find \(y\) in terms of \(b\) when \(x = 3a\).",
  "options": [r"\(9b\)", r"\(3b\)", r"\(6b\)", r"\(27b\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Tripling x multiplies y by 3² = 9, so y = 9b.",
  "misconceptions": [
   {"pattern": "linear", "expect": 1, "message": "y = kx². Tripling x multiplies y by 3² = 9, so y = 9b, not 3b."},
   {"pattern": "used_cube", "expect": 3, "message": "It is x² not x³: the multiplier is 3² = 9, giving 9b, not 27b."}]},
 { # G1
  "display": r"\(y \propto \frac{1}{\sqrt{x}}\). When \(x = 4\), \(y = 10\). Find \(y\) when \(x = 16\).",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "k = y × √x = 10 × √4 = 20. Then divide by √16.",
  "misconceptions": [
   {"pattern": "used_direct", "expect": 1.25, "message": "Inverse: k = y × √x = 20, not y ÷ √x. Then y = 20 ÷ 4 = 5."}],
  "guided_steps": [
   say("Inverse root: y = k/√x, so k = y × √x. Use x = 4, y = 10."),
   box("√4 = ", 2, "What number times itself is 4?"),
   box("k = 10 × 2 = ", 20, "y times the root for inverse."),
   box("Now x = 16: √16 = 4, y = 20 ÷ 4 = ", 5, "k ÷ the new root.", phase="substitute"),
   box("Check: 5 × 4 = ", 20, "y times √x rebuilds k.", done="Same k = 20, so y = 5 is right.")]},
 { # G2
  "display": r"The intensity \(I\) of light is inversely proportional to \(d^2\). At \(d = 3\), \(I = 100\). Find \(d\) when \(I = 25\).",
  "solutions": [6], "calculator": True, "input_type": "single_value",
  "hint": "k = I × d² = 100 × 9 = 900. Then d² = k ÷ 25 and square root.",
  "misconceptions": [
   {"pattern": "forgot_root", "expect": 36, "message": "d² = 36 means d = √36 = 6, not 36."},
   {"pattern": "wrong_k", "expect": None, "message": "k = I × d² = 900, not I ÷ d². Then d² = 900 ÷ 25 = 36, d = 6."}],
  "guided_steps": [
   say("Inverse square: I = k/d², so k = I × d². Use d = 3, I = 100."),
   box("3² = ", 9, "3 × 3."),
   box("k = 100 × 9 = ", 900, "I times d²."),
   box("Now 25 = 900 ÷ d², so d² = 900 ÷ 25 = ", 36, "Divide k by the new I."),
   box("Square root: d = √36 = ", 6, "What squares to 36?", phase="substitute"),
   box("Check: 900 ÷ 6² = 900 ÷ 36 = ", 25, "k ÷ d² rebuilds I.", done="Rebuilds I = 25, so d = 6 is right.")]},
 { # G3  REWORDED to a numeric single_value: find denominator n of the multiplier 1/n
  "display": r"\(y \propto x^3\). When \(x\) is halved, \(y\) is multiplied by \(\frac{1}{n}\). Find \(n\).",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Halving x multiplies y by (1/2)³. Find the denominator.",
  "misconceptions": [
   {"pattern": "linear", "expect": 2, "message": "y depends on x³: halving x multiplies y by (1/2)³ = 1/8, so n = 8, not 2."},
   {"pattern": "used_square", "expect": 4, "message": "It is x³: halving gives (1/2)³ = 1/8, so n = 8, not 4."}],
  "guided_steps": [
   say("y = kx³. Halving x multiplies x³ by (1/2)³."),
   box("Take k = 1, x = 2: y = 2³ = ", 8, "2 × 2 × 2."),
   box("Halve x to 1: y = 1³ = ", 1, "1 cubed."),
   box("y went from 8 to 1, multiplied by 1 ÷ 8, so n = ", 8, "8 becomes 1, a factor of one eighth.", phase="substitute"),
   box("Check: 2³ = ", 8, "The denominator of (1/2)³.", done="y multiplied by 1/8, so n = 8.")]},
 { # G4
  "display": r"\(T \propto \sqrt{L}\). When \(L = 25\), \(T = 10\). Find \(L\) when \(T = 14\).",
  "solutions": [49], "calculator": True, "input_type": "single_value",
  "hint": "k = T ÷ √L = 10 ÷ 5 = 2. Then √L = T ÷ k, and square it.",
  "misconceptions": [
   {"pattern": "forgot_square", "expect": 7, "message": "√L = 7 means L = 7² = 49, not 7."},
   {"pattern": "used_L", "expect": 1225, "message": "Use √L: k = 10 ÷ √25 = 2, then √L = 7, L = 49."}],
  "guided_steps": [
   say("Root: T = k√L. Find k from L = 25, T = 10."),
   box("√25 = ", 5, "What number times itself is 25?"),
   box("k = 10 ÷ 5 = ", 2, "Divide T by the root."),
   box("Now 14 = 2√L, so √L = 14 ÷ 2 = ", 7, "Divide the new T by k."),
   box("Square both sides: L = 7² = ", 49, "7 × 7.", phase="substitute"),
   box("Check: T = 2 × √49 = 2 × 7 = ", 14, "k times √L rebuilds T.", done="Rebuilds T = 14, so L = 49 is right.")]},
]

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Use y = kxⁿ once: find k, or put a value in (square, cube or root x first).",
 "silver_description": "Two stages: find k from the first pair, then use it for a new value, sometimes working backwards.",
 "gold_description": "Reason about powers: inverse roots, multipliers, halving and letters.",
}

tier_guides = {
 "bronze": {
  "title": "Bronze: find k, or use the equation once",
  "steps": [
   "Direct: <strong>y = kxⁿ</strong>. Inverse: <strong>y = k/xⁿ</strong>. Always square, cube or root the x value before you use it.",
   "To find <strong>k</strong>: put the given pair in and solve. To find <strong>y</strong>: put x into the full equation."],
  "example": {"question": "y ∝ x². When x = 2, y = 20. Find k.",
   "steps": [{"label": "Set up", "content": "y = kx²"},
             {"label": "Substitute", "content": "20 = k × 4"},
             {"label": "Check", "content": "5 × 4 = 20 ✓"},
             {"label": "Answer", "content": "k = 5", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: find k, then use it for a new value",
  "steps": [
   "Two stages: use the first pair to find <strong>k</strong>, then use k with the new x (or y).",
   "<strong>Inverse:</strong> y = k/xⁿ, so k = y × xⁿ. <strong>Direct:</strong> k = y ÷ xⁿ.",
   "Working backwards from y? Put y in, then undo the power with a root."],
  "example": {"question": "y ∝ x². When x = 3, y = 27. Find y when x = 5.",
   "steps": [{"label": "Find k", "content": "27 ÷ 9 = 3"},
             {"label": "Use it", "content": "y = 3 × 25 = 75"},
             {"label": "Check", "content": "75 ÷ 25 = 3 ✓"},
             {"label": "Answer", "content": "y = 75", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: reason about powers and multipliers",
  "steps": [
   "<strong>Multiplier:</strong> multiplying x by a factor f multiplies y by fⁿ. Squaring, cubing or rooting sets n.",
   "<strong>In terms of letters:</strong> keep k·xⁿ as a block and scale it.",
   "Roots count as powers: √x is x to the power a half."],
  "example": {"question": "y ∝ x². When x doubles, y is multiplied by:",
   "steps": [{"label": "Set up", "content": "factor = 2²"},
             {"label": "Work it", "content": "2² = 4"},
             {"label": "Check", "content": "double x, ×4 ✓"},
             {"label": "Answer", "content": "×4", "isAnswer": True, "is_answer": True}]}},
}

method_card = {
 "title": "Proportion with Powers & Roots",
 "steps": [
  "Direct to a power: y ∝ xⁿ means y = kxⁿ.",
  "Inverse to a power: y ∝ 1/xⁿ means y = k/xⁿ.",
  "Substitute the known pair to find k, then write the full equation.",
  "Put the new value in. Square, cube or root before multiplying."],
 "content": "<p>Higher tier proportion uses powers and roots. Read the statement, then build an equation with a constant k.</p><p><strong>Direct:</strong> y ∝ x² gives y = kx²; y ∝ √x gives y = k√x. <strong>Inverse:</strong> y ∝ 1/x² gives y = k/x².</p><p>Find k from the pair you are given, then substitute the new value. Always apply the power or root to x before multiplying by k.</p>",
 "example": "<p><strong>y ∝ x². When x = 3, y = 45. Find y when x = 4.</strong></p><p>y = kx² → 45 = k(9) → k = 5.</p><p>y = 5(4²) = 5(16) = 80.</p>",
}

opener_svg = (
 '<svg viewBox="0 0 240 120" role="img" aria-label="A small square of side 3 tiles beside a larger square of side 6 tiles">'
 '<rect x="20" y="70" width="34" height="34" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<text x="37" y="118" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">side 3</text>'
 '<rect x="120" y="36" width="68" height="68" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<text x="154" y="118" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">side 6</text>'
 '</svg><span class="figure-caption">Not drawn accurately</span><br>'
 'Two square trays are filled with the same square tiles. The small tray is 3 tiles along each side, the big one is 6 tiles along each side. How many times more tiles does the big tray hold?'
)

guided = {
 "opener": {
  "display": opener_svg,
  "steps": [
   box("The small tray holds 3 × 3 = ", 9, "Side times side.", post=" tiles"),
   box("The big tray holds 6 × 6 = ", 36, "Side times side.", post=" tiles"),
   say("The side doubled (3 → 6) but the tiles went ×4 (9 → 36), because 2² = 4. Tiles are proportional to side <strong>squared</strong>: write <strong>A = k·s²</strong>. Every question here is the same idea: find k, then use the equation, squaring, cubing or rooting before you multiply.")]},
 "teach": {
  "bronze": {
   "display": r"\(y \propto x^2\). When \(x = 2\), \(y = 20\). Find k, then find y when x = 6.",
   "steps": [
    say("y ∝ x² means y = kx². Find k first, then reuse it."),
    box("Square x: 2² = ", 4, "2 × 2."),
    box("k = 20 ÷ 4 = ", 5, "Divide y by the squared x."),
    box("Check: 5 × 4 = ", 20, "k times x² rebuilds y."),
    box("Now x = 6: 6² = 36, so y = 5 × 36 = ", 180, "k times the new x²."),
    box("Check the new pair: 180 ÷ 36 = ", 5, "y ÷ x² gives k again.", done="Same k = 5 from both pairs. That is the whole method.")]},
  "silver": {
   "display": r"\(F \propto \frac{1}{x^2}\). When \(x = 2\), \(F = 50\). Find F when x = 5.",
   "steps": [
    say("Inverse square: F = k/x², so k = F × x². Find k first."),
    box("Square x: 2² = ", 4, "2 × 2."),
    box("k = 50 × 4 = ", 200, "F times x² for inverse proportion."),
    box("Now x = 5: 5² = 25, F = 200 ÷ 25 = ", 8, "k ÷ the new x²."),
    box("Check: 8 × 25 = ", 200, "F times x² rebuilds k."),
    box("First pair: 50 × 4 = ", 200, "Same k both ways.", done="k = 200 both times. Square, then divide.")]},
  "gold": {
   "display": r"\(y \propto x^n\). When \(x\) doubles, \(y\) is multiplied by 32. Work out n.",
   "steps": [
    say("y ∝ xⁿ. Multiplying x by a factor f multiplies y by fⁿ. Here f = 2 and y grows ×32, so 2ⁿ = 32."),
    box("Try n = 4: 2⁴ = ", 16, "2 × 2 × 2 × 2."),
    box("Too small. Try n = 5: 2⁵ = ", 32, "2 × 2 × 2 × 2 × 2."),
    box("That matches 32, so n = ", 5, "The power that gives 32."),
    box("Check: doubling x multiplies y by 2⁵ = ", 32, "2⁵ again.", done="×32 matches, so n = 5. Match the power, do not divide.")]},
 }
}

pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-eduqas_ratio-proportion-L05.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
# diagrams shard is identical (opener SVG is the only figure this textual lesson warrants)
out2 = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-eduqas_ratio-proportion-L05_diagrams.json"
with io.open(out2, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
