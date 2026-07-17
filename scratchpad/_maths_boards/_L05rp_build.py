# -*- coding: utf-8 -*-
import json, io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

pd = json.load(open("_L05rp_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---- helpers -------------------------------------------------------------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mis(pattern, message, expect):
    return {"pattern": pattern, "message": message, "expect": expect}

# ---- 1. MINIMAL BANK EDITS (break duplicate solutions within tier) -------
# bronze had three [3] (idx 0,4,6); keep [0]=3, retune [4] and [6].
pb["bronze"][4]["display"] = r"\(y \propto \sqrt{x}\). When \(x = 4\), \(y = 14\). Find \(k\)."
pb["bronze"][4]["solutions"] = [7]          # 14 = k*2  -> k = 7
pb["bronze"][6]["display"] = r"\(y \propto x^3\). When \(x = 2\), \(y = 40\). Find \(k\)."
pb["bronze"][6]["solutions"] = [5]          # 40 = k*8  -> k = 5
# gold had two [4] (idx 3,4); keep [3]=4, retune [4].
pb["gold"][4]["display"]  = r"\(T \propto \sqrt{L}\). When \(L = 100\), \(T = 2\). Find \(T\) when \(L = 900\)."
pb["gold"][4]["solutions"] = [6]            # k=0.2 ; T=0.2*30 = 6

# ---- 2. tier descriptions ------------------------------------------------
pb["bronze_description"] = "Direct proportion with a power: form y = k×(power of x), find k, then substitute the new x."
pb["silver_description"] = "Inverse powers and reversing: find k by multiplying, find x from y, or scale when x changes."
pb["gold_description"]   = "Cube and root laws in real contexts: reverse through the matching root, or use k in a formula."

# ---- 3. per-problem hint + misconceptions + guided_steps -----------------
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# bronze[0]  y∝x², x=2,y=12, find k=3
B[0]["hint"] = "Write y = k×x², put in the pair, then divide y by the squared x."
B[0]["misconceptions"] = [
    mis("forgot_square", "Divide by x², not x. Here x² = 4, so k = 12 ÷ 4 = 3, not 12 ÷ 2 = 6.", 6),
    mis("mult_instead", "To find k you divide y by x², you do not multiply: k = 12 ÷ 4 = 3.", 48),
]
B[0]["guided_steps"] = [
    sayonly("y ∝ x² means y = k×x². Put in the pair x = 2, y = 12."),
    box("2² = ", 4, "Square the x value: 2 × 2.", post=""),
    box("So 12 = k × 4. k = 12 ÷ 4 = ", 3, "k is 12 divided by the squared x.", phase="substitute"),
    box("Check: k × 2² = 3 × 4 = ", 12, "Multiply your k back by 4.", done="Back to the given y = 12, so k = 3."),
]

# bronze[1]  y∝x², k=5, find y when x=4 -> 80
B[1]["hint"] = "y = 5×x². Square x, then multiply by 5."
B[1]["misconceptions"] = [
    mis("forgot_square", "x² means x times x (16), not x times 5. y = 5 × 16 = 80.", 20),
    mis("double_x", "x² is 4 × 4 = 16, not 4 × 2 = 8. y = 5 × 16 = 80.", 40),
]
B[1]["guided_steps"] = [
    sayonly("k is already 5, so y = 5×x². Use x = 4."),
    box("4² = ", 16, "Square the x value: 4 × 4.", post=""),
    box("y = 5 × 16 = ", 80, "Multiply k by the squared x.", phase="substitute"),
    box("Check: y ÷ 4² = 80 ÷ 16 = ", 5, "Divide your answer by 16.", done="Back to k = 5, so y = 80 is right."),
]

# bronze[2]  y∝x², x=3,y=45, find y when x=2 -> 20
B[2]["hint"] = "Find k from the first pair (÷ x²), then use it with the new x."
B[2]["misconceptions"] = [
    mis("linear_scale", "y follows x², not x. Do not scale y by 2/3. Find k = 5 first, then y = 5 × 2² = 20.", 30),
    mis("forgot_square", "Square the new x: 2² = 4, so y = 5 × 4 = 20, not 5 × 2 = 10.", 10),
]
B[2]["guided_steps"] = [
    sayonly("y = k×x². Use the pair x = 3, y = 45 to find k."),
    box("3² = ", 9, "Square the first x: 3 × 3.", post=""),
    box("k = 45 ÷ 9 = ", 5, "Divide y by the squared x.", post=""),
    box("Now the new x = 2. 2² = ", 4, "Square the new x: 2 × 2.", phase="substitute"),
    box("y = 5 × 4 = ", 20, "Multiply k by the new squared x.", done=None),
    box("Check: y ÷ 2² = 20 ÷ 4 = ", 5, "Divide by 4 to recover k.", done="Same k = 5 as the given pair, so y = 20."),
]

# bronze[3]  y∝x², x doubles 3->6, y was 18 -> 72
B[3]["hint"] = "Double x means y multiplies by 2² = 4."
B[3]["misconceptions"] = [
    mis("doubled_y", "y follows x², so doubling x makes y ×4, not ×2. 18 × 4 = 72, not 18 × 2 = 36.", 36),
]
B[3]["guided_steps"] = [
    sayonly("x goes from 3 to 6. Work out how many times bigger x is."),
    box("6 ÷ 3 = ", 2, "Divide the new x by the old x.", post=""),
    box("y ∝ x², so y multiplies by 2² = ", 4, "Square the x multiplier.", post=""),
    box("New y = 18 × 4 = ", 72, "Multiply the old y by 4.", phase="substitute"),
    box("Check with k: k = 18 ÷ 3² = 2, then 2 × 6² = 2 × 36 = ", 72, "Multiply 2 by 36.", done="Both methods give 72."),
]

# bronze[4]  y∝√x, x=4, y=14, find k=7  (EDITED)
B[4]["hint"] = "y = k×√x. Work out √x, then divide y by it."
B[4]["misconceptions"] = [
    mis("forgot_root", "Divide by √x, not x. √4 = 2, so k = 14 ÷ 2 = 7, not 14 ÷ 4 = 3.5.", 3.5),
    mis("mult_instead", "To find k you divide y by √x: k = 14 ÷ 2 = 7, not 14 × 2.", 28),
]
B[4]["guided_steps"] = [
    sayonly("y ∝ √x means y = k×√x. Put in x = 4, y = 14."),
    box("√4 = ", 2, "Which number times itself gives 4?", post=""),
    box("14 = k × 2, so k = 14 ÷ 2 = ", 7, "Divide y by the square root.", phase="substitute"),
    box("Check: k × √4 = 7 × 2 = ", 14, "Multiply your k by 2.", done="Back to y = 14, so k = 7."),
]

# bronze[5]  y∝x², k=2, find y when x=5 -> 50
B[5]["hint"] = "y = 2×x². Square x, then multiply by 2."
B[5]["misconceptions"] = [
    mis("forgot_square", "x² is 5 × 5 = 25, not 5. y = 2 × 25 = 50, not 2 × 5 = 10.", 10),
    mis("double_x", "x² is 25, not 5 × 2 = 10. y = 2 × 25 = 50.", 20),
]
B[5]["guided_steps"] = [
    sayonly("k is 2, so y = 2×x². Use x = 5."),
    box("5² = ", 25, "Square the x value: 5 × 5.", post=""),
    box("y = 2 × 25 = ", 50, "Multiply k by the squared x.", phase="substitute"),
    box("Check: y ÷ 5² = 50 ÷ 25 = ", 2, "Divide by 25 to recover k.", done="Back to k = 2, so y = 50 is right."),
]

# bronze[6]  y∝x³, x=2, y=40, find k=5  (EDITED)
B[6]["hint"] = "y = k×x³. Cube x, then divide y by it."
B[6]["misconceptions"] = [
    mis("used_square", "Divide by x³ = 8, not x² = 4. k = 40 ÷ 8 = 5, not 40 ÷ 4 = 10.", 10),
    mis("forgot_power", "x³ = 8, so k = 40 ÷ 8 = 5, not 40 ÷ 2 = 20.", 20),
]
B[6]["guided_steps"] = [
    sayonly("y ∝ x³ means y = k×x³. Put in x = 2, y = 40."),
    box("2³ = ", 8, "Cube the x value: 2 × 2 × 2.", post=""),
    box("40 = k × 8, so k = 40 ÷ 8 = ", 5, "Divide y by the cubed x.", phase="substitute"),
    box("Check: k × 2³ = 5 × 8 = ", 40, "Multiply your k by 8.", done="Back to y = 40, so k = 5."),
]

# bronze[7]  y∝x², x=1,y=7, find y when x=3 -> 63
B[7]["hint"] = "When x = 1, k equals y. Then use the new x."
B[7]["misconceptions"] = [
    mis("forgot_square", "Square the new x: 3² = 9, so y = 7 × 9 = 63, not 7 × 3 = 21.", 21),
]
B[7]["guided_steps"] = [
    sayonly("y = k×x². When x = 1, x² = 1, so k = y = 7. Now use the new x = 3."),
    box("3² = ", 9, "Square the new x: 3 × 3.", post=""),
    box("y = 7 × 9 = ", 63, "Multiply k by the squared x.", phase="substitute"),
    box("Check: y ÷ 3² = 63 ÷ 9 = ", 7, "Divide by 9 to recover k.", done="Back to k = 7, so y = 63 is right."),
]

# silver[0]  y∝1/x², x=2,y=5, find y when x=5 -> 0.8 (calc)
S[0]["hint"] = "Inverse square: k = y × x². Find k, then divide by the new x²."
S[0]["misconceptions"] = [
    mis("treated_direct", "This is inverse: y = k ÷ x². k = y × x² = 20, so y = 20 ÷ 25 = 0.8.", 31.25),
    mis("forgot_square", "Use x², not x. k = 5 × 2² = 20, so y = 20 ÷ 25 = 0.8.", 2),
]
S[0]["guided_steps"] = [
    sayonly("Inverse square: y = k ÷ x². Find k by multiplying: k = y × x²."),
    box("2² = ", 4, "Square the first x: 2 × 2.", post=""),
    box("k = 5 × 4 = ", 20, "Multiply y by the squared x.", post=""),
    box("New x = 5. 5² = ", 25, "Square the new x: 5 × 5.", phase="substitute"),
    box("y = 20 ÷ 25 = ", 0.8, "Divide k by the new squared x.", done=None),
    box("Check: k ÷ 2² = 20 ÷ 4 = ", 5, "Divide k by 4 to recover the first y.", done="Back to y = 5, so y = 0.8 is right."),
]

# silver[1]  y∝√x, x=9,y=15, find y when x=25 -> 25
S[1]["hint"] = "y = k×√x. Find k with √9, then multiply by √25."
S[1]["misconceptions"] = [
    mis("forgot_root", "Multiply by √x, not x. y = 5 × √25 = 5 × 5 = 25, not 5 × 25 = 125.", 125),
]
S[1]["guided_steps"] = [
    sayonly("y = k×√x. Use x = 9, y = 15 to find k."),
    box("√9 = ", 3, "Which number times itself gives 9?", post=""),
    box("k = 15 ÷ 3 = ", 5, "Divide y by the square root.", post=""),
    box("New x = 25. √25 = ", 5, "Which number times itself gives 25?", phase="substitute"),
    box("y = 5 × 5 = ", 25, "Multiply k by the new root.", done=None),
    box("Check: k × √9 = 5 × 3 = ", 15, "Multiply k by 3.", done="Back to y = 15, so y = 25 is right."),
]

# silver[2]  y∝x³, x=2,y=40, find y when x=3 -> 135
S[2]["hint"] = "Cube law: find k with ÷ x³, then multiply by the new x³."
S[2]["misconceptions"] = [
    mis("used_square", "Use x³ = 8, not x² = 4. k = 40 ÷ 8 = 5, so y = 5 × 27 = 135.", 90),
    mis("forgot_cube", "Cube the new x: 3³ = 27, so y = 5 × 27 = 135, not 5 × 3 = 15.", 15),
]
S[2]["guided_steps"] = [
    sayonly("y = k×x³. Use x = 2, y = 40 to find k."),
    box("2³ = ", 8, "Cube the first x: 2 × 2 × 2.", post=""),
    box("k = 40 ÷ 8 = ", 5, "Divide y by the cubed x.", post=""),
    box("New x = 3. 3³ = ", 27, "Cube the new x: 3 × 3 × 3.", phase="substitute"),
    box("y = 5 × 27 = ", 135, "Multiply k by the new cubed x.", done=None),
    box("Check: k × 2³ = 5 × 8 = ", 40, "Multiply k by 8.", done="Back to y = 40, so y = 135 is right."),
]

# silver[3]  y∝x², x=4,y=48, find x when y=75 -> 5
S[3]["hint"] = "Find k, then reverse: divide y by k and take the square root."
S[3]["misconceptions"] = [
    mis("forgot_sqrt", "x² = 25, so x = √25 = 5. Do not stop at 25, take the square root.", 25),
]
S[3]["guided_steps"] = [
    sayonly("y = k×x². Use x = 4, y = 48 to find k first."),
    box("4² = ", 16, "Square the given x: 4 × 4.", post=""),
    box("k = 48 ÷ 16 = ", 3, "Divide y by the squared x.", post=""),
    box("Reverse: 75 = 3×x², so x² = 75 ÷ 3 = ", 25, "Divide the new y by k.", phase="substitute"),
    box("x = √25 = ", 5, "Take the square root of 25.", done=None),
    box("Check: 3 × 5² = 3 × 25 = ", 75, "Multiply k by 25.", done="Back to y = 75, so x = 5 is right."),
]

# silver[4]  y∝1/x², x triples, y was 36, new y -> 4
S[4]["hint"] = "Inverse square: tripling x divides y by 3² = 9."
S[4]["misconceptions"] = [
    mis("forgot_square", "Inverse square divides by 3² = 9, not 3. 36 ÷ 9 = 4, not 36 ÷ 3 = 12.", 12),
    mis("treated_direct", "Inverse means divide, not multiply. y = 36 ÷ 9 = 4, not 36 × 9 = 324.", 324),
]
S[4]["guided_steps"] = [
    sayonly("Inverse square: y = k ÷ x². See how x changes."),
    box("x triples, a multiplier of ", 3, "Tripling means times 3.", post=""),
    box("Inverse square, so y divides by 3² = ", 9, "Square the multiplier; inverse means divide.", post=""),
    box("New y = 36 ÷ 9 = ", 4, "Divide the old y by 9.", phase="substitute"),
    box("Check: if y really ÷ 9, then 4 × 9 = ", 36, "Multiply the new y back by 9.", done="Back to the old y = 36, so new y = 4."),
]

# silver[5]  y∝√x, x=16,y=20, find y when x=100 -> 50
S[5]["hint"] = "y = k×√x. Find k with √16, then multiply by √100."
S[5]["misconceptions"] = [
    mis("forgot_root", "Divide by √x, not x. k = 20 ÷ √16 = 5, so y = 5 × 10 = 50, not 1.25 × 100 = 125.", 125),
    mis("forgot_root_new", "Multiply by √100 = 10, not 100. y = 5 × 10 = 50, not 5 × 100 = 500.", 500),
]
S[5]["guided_steps"] = [
    sayonly("y = k×√x. Use x = 16, y = 20 to find k."),
    box("√16 = ", 4, "Which number times itself gives 16?", post=""),
    box("k = 20 ÷ 4 = ", 5, "Divide y by the square root.", post=""),
    box("New x = 100. √100 = ", 10, "Which number times itself gives 100?", phase="substitute"),
    box("y = 5 × 10 = ", 50, "Multiply k by the new root.", done=None),
    box("Check: k × √16 = 5 × 4 = ", 20, "Multiply k by 4.", done="Back to y = 20, so y = 50 is right."),
]

# silver[6]  y∝x², x=5,y=100, find y when x=10 -> 400
S[6]["hint"] = "Find k (÷ 5²), then multiply by 10²."
S[6]["misconceptions"] = [
    mis("doubled_y", "x doubles (5 to 10), so y goes ×2² = ×4. 100 × 4 = 400, not 100 × 2 = 200.", 200),
    mis("forgot_square", "Square the new x: 10² = 100, so y = 4 × 100 = 400, not 4 × 10 = 40.", 40),
]
S[6]["guided_steps"] = [
    sayonly("y = k×x². Use x = 5, y = 100 to find k."),
    box("5² = ", 25, "Square the given x: 5 × 5.", post=""),
    box("k = 100 ÷ 25 = ", 4, "Divide y by the squared x.", post=""),
    box("New x = 10. 10² = ", 100, "Square the new x: 10 × 10.", phase="substitute"),
    box("y = 4 × 100 = ", 400, "Multiply k by the new squared x.", done=None),
    box("Check: k × 5² = 4 × 25 = ", 100, "Multiply k by 25.", done="Back to y = 100, so y = 400 is right."),
]

# gold[0]  y∝x³, x=3,y=54, find x when y=16 -> 2
G[0]["hint"] = "Find k, then reverse: divide y by k and take the cube root."
G[0]["misconceptions"] = [
    mis("forgot_root", "x³ = 8, so x = ∛8 = 2. Do not stop at 8, take the cube root.", 8),
]
G[0]["guided_steps"] = [
    sayonly("y = k×x³. Use x = 3, y = 54 to find k first."),
    box("3³ = ", 27, "Cube the given x: 3 × 3 × 3.", post=""),
    box("k = 54 ÷ 27 = ", 2, "Divide y by the cubed x.", post=""),
    box("Reverse: 16 = 2×x³, so x³ = 16 ÷ 2 = ", 8, "Divide the new y by k.", phase="substitute"),
    box("x = ∛8 = ", 2, "Take the cube root of 8.", done=None),
    box("Check: 2 × 2³ = 2 × 8 = ", 16, "Multiply k by 8.", done="Back to y = 16, so x = 2 is right."),
]

# gold[1]  y∝1/√x, x=4,y=10, find y when x=16 -> 5
G[1]["hint"] = "Inverse root: k = y × √x. Find k, then divide by the new root."
G[1]["misconceptions"] = [
    mis("treated_direct", "This is inverse: y = k ÷ √x. k = y × √x = 20, so y = 20 ÷ 4 = 5, not 20.", 20),
    mis("forgot_root", "Use √x, not x. k = 10 × √4 = 20, so y = 20 ÷ 4 = 5, not 40 ÷ 16 = 2.5.", 2.5),
]
G[1]["guided_steps"] = [
    sayonly("Inverse root: y = k ÷ √x. Find k by multiplying: k = y × √x."),
    box("√4 = ", 2, "Which number times itself gives 4?", post=""),
    box("k = 10 × 2 = ", 20, "Multiply y by the square root.", post=""),
    box("New x = 16. √16 = ", 4, "Which number times itself gives 16?", phase="substitute"),
    box("y = 20 ÷ 4 = ", 5, "Divide k by the new root.", done=None),
    box("Check: k ÷ √4 = 20 ÷ 2 = ", 10, "Divide k by 2 to recover the first y.", done="Back to y = 10, so y = 5 is right."),
]

# gold[2]  y∝x², y=32 when x=4, find y when x=6 -> 72
G[2]["hint"] = "Find k (÷ 4²), then multiply by 6²."
G[2]["misconceptions"] = [
    mis("linear_scale", "y follows x², not x. Do not scale by 6/4. Find k = 2, then y = 2 × 6² = 72.", 48),
    mis("forgot_square", "Square the new x: 6² = 36, so y = 2 × 36 = 72, not 2 × 6 = 12.", 12),
]
G[2]["guided_steps"] = [
    sayonly("y = k×x². Use x = 4, y = 32 to find k."),
    box("4² = ", 16, "Square the given x: 4 × 4.", post=""),
    box("k = 32 ÷ 16 = ", 2, "Divide y by the squared x.", post=""),
    box("New x = 6. 6² = ", 36, "Square the new x: 6 × 6.", phase="substitute"),
    box("y = 2 × 36 = ", 72, "Multiply k by the new squared x.", done=None),
    box("Check: k × 4² = 2 × 16 = ", 32, "Multiply k by 16.", done="Back to y = 32, so y = 72 is right."),
]

# gold[3]  P∝1/V, V=5,P=200, find V when P=250 -> 4
G[3]["hint"] = "Inverse: k = P × V. Find k, then divide k by the new P."
G[3]["misconceptions"] = [
    mis("treated_direct", "This is inverse: P = k ÷ V. k = P × V = 1000, so V = 1000 ÷ 250 = 4, not 6.25.", 6.25),
    mis("divide_wrong", "Divide k by P, not P by k. V = 1000 ÷ 250 = 4, not 250 ÷ 1000 = 0.25.", 0.25),
]
G[3]["guided_steps"] = [
    sayonly("Inverse: P = k ÷ V, so k = P × V. Use V = 5, P = 200."),
    box("k = 200 × 5 = ", 1000, "Multiply P by V to get k.", post=""),
    box("Now 250 = 1000 ÷ V, so V = 1000 ÷ 250 = ", 4, "Divide k by the new P.", phase="substitute"),
    box("Check: k ÷ V = 1000 ÷ 4 = ", 250, "Divide k by your V.", done="Back to P = 250, so V = 4 is right."),
]

# gold[4]  T∝√L, L=100,T=2, find T when L=900 -> 6  (EDITED)
G[4]["hint"] = "T = k×√L. Find k with √100, then multiply by √900."
G[4]["misconceptions"] = [
    mis("forgot_root", "Multiply by √L, not L. k = 2 ÷ √100 = 0.2, so T = 0.2 × 30 = 6, not 0.02 × 900 = 18.", 18),
    mis("forgot_root_new", "Multiply by √900 = 30, not 900. T = 0.2 × 30 = 6, not 0.2 × 900 = 180.", 180),
]
G[4]["guided_steps"] = [
    sayonly("T = k×√L. Use L = 100, T = 2 to find k."),
    box("√100 = ", 10, "Which number times itself gives 100?", post=""),
    box("k = T ÷ √L = 2 ÷ 10 = ", 0.2, "Divide T by the square root.", post=""),
    box("New L = 900. √900 = ", 30, "Which number times itself gives 900?", phase="substitute"),
    box("T = 0.2 × 30 = ", 6, "Multiply k by the new root.", done=None),
    box("Check: k × √100 = 0.2 × 10 = ", 2, "Multiply k by 10.", done="Back to T = 2, so T = 6 is right."),
]

# ---- preserved worked_examples: fix pre-existing em dashes in labels -----
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---- 4. method_card: trim steps to <=4 (keep title/content/example) ------
pd["method_card"]["steps"] = [
    "Write the proportion as an equation with k, e.g. y = kx²",
    "Substitute the known pair to find k",
    "Put k back in, then substitute the new value",
    "Shortcut: y ∝ x² means ×2 on x gives ×4 on y; y ∝ 1/x² means ÷4",
]

# ---- 5. tier_guides ------------------------------------------------------
pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: direct proportion with a power",
    "steps": [
      r"A power law like \(y \propto x^2\) means \(y = kx^2\). The <strong>k</strong> is a fixed number you find first.",
      r"Put the given pair into the equation and solve for k: divide y by the <strong>power of x</strong> (here x², not x).",
      "Now the equation is complete. Substitute the new x, work out its power, and multiply by k.",
    ],
    "example": {
      "question": r"\(y \propto x^2\). When \(x = 2\), \(y = 20\). Find \(y\) when \(x = 3\).",
      "steps": [
        {"label": "Find k", "content": r"<p>\(20 = k × 2^2 = 4k\), so \(k = 5\).</p>"},
        {"label": "Substitute", "content": r"<p>\(y = 5 × 3^2 = 5 × 9\)</p>"},
        {"label": "Check", "content": r"<p>\(5 × 2^2 = 20\) ✓</p>"},
        {"label": "Answer", "content": r"<p>\(y = 45\)</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "silver": {
    "title": "Silver: inverse powers and reversing",
    "steps": [
      r"Inverse square, \(y \propto \frac{1}{x^2}\), means \(y = \frac{k}{x^2}\). Find k by <strong>multiplying</strong>: \(k = y × x^2\).",
      "To find x from a given y, reverse the steps: divide y by k, then take the matching root (square root for x², cube root for x³).",
      "For a scaling question, square (or cube) the x-multiplier; inverse laws divide by it instead of multiplying.",
    ],
    "example": {
      "question": r"\(y \propto \frac{1}{x^2}\). When \(x = 2\), \(y = 5\). Find \(y\) when \(x = 5\).",
      "steps": [
        {"label": "Find k", "content": r"<p>\(k = y × x^2 = 5 × 4 = 20\)</p>"},
        {"label": "Substitute", "content": r"<p>\(y = \frac{20}{5^2} = \frac{20}{25}\)</p>"},
        {"label": "Check", "content": r"<p>\(\frac{20}{2^2} = 5\) ✓</p>"},
        {"label": "Answer", "content": r"<p>\(y = 0.8\)</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "gold": {
    "title": "Gold: cube and root laws in context",
    "steps": [
      r"Gold mixes cubes \(y \propto x^3\), inverse roots \(y \propto \frac{1}{\sqrt{x}}\), and real formulas (\(P \propto \frac{1}{V}\), \(T \propto \sqrt{L}\)).",
      "The method never changes: form the equation, find k from the given pair, then substitute or reverse for the unknown.",
      "Reversing through a power needs the matching root: cube root for x³, square root for x².",
    ],
    "example": {
      "question": r"\(y \propto x^3\). When \(x = 3\), \(y = 54\). Find \(x\) when \(y = 16\).",
      "steps": [
        {"label": "Find k", "content": r"<p>\(k = 54 ÷ 3^3 = 54 ÷ 27 = 2\)</p>"},
        {"label": "Reverse", "content": r"<p>\(16 = 2x^3\), so \(x^3 = 8\)</p>"},
        {"label": "Root", "content": r"<p>\(x = \sqrt[3]{8}\)</p>"},
        {"label": "Answer", "content": r"<p>\(x = 2\)</p>", "isAnswer": True, "is_answer": True},
      ],
    },
  },
}

# ---- 6. guided (opener + teach walks) ------------------------------------
# opener SVG: two square patios, 2x2 (4 slabs) and 4x4 (16 slabs)
def grid_svg():
    cells = []
    # small 2x2 grid, cell 22, origin (18,30)
    for r in range(2):
        for c in range(2):
            x = 18 + c*22; y = 30 + r*22
            cells.append(f'<rect x="{x}" y="{y}" width="22" height="22" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>')
    # big 4x4 grid, cell 22, origin (150,30)
    for r in range(4):
        for c in range(4):
            x = 150 + c*22; y = 30 + r*22
            cells.append(f'<rect x="{x}" y="{y}" width="22" height="22" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>')
    rects = "".join(cells)
    svg = (
      '<svg viewBox="0 0 260 140" role="img" '
      'aria-label="A 2 by 2 square patio of 4 slabs beside a 4 by 4 square patio of 16 slabs" '
      'style="max-width:280px;width:100%;height:auto">'
      + rects +
      '<text x="40" y="20" font-family="Inter,sans-serif" font-size="12" fill="currentColor" text-anchor="middle">2 m</text>'
      '<text x="194" y="20" font-family="Inter,sans-serif" font-size="12" fill="currentColor" text-anchor="middle">4 m</text>'
      '</svg>'
    )
    return svg

pd["guided"] = {
  "opener": {
    "label": "Before any algebra",
    "display": grid_svg() + "<br>Two square patios, paved with 1 m² slabs.",
    "steps": [
      box("Small patio (2 m side): slabs = ", 4,
          "It is a 2 by 2 square: count them, or 2 × 2.", post=""),
      box("Big patio (4 m side): slabs = ", 16,
          "A 4 by 4 square: count them, or 4 × 4.", post="",
          done="The side doubled (2 → 4) but the slabs went ×4, not ×2."),
      sayonly("Slabs = side × side = side². So the slabs are proportional to the side <strong>squared</strong>: N ∝ s². Double the side and you get 4 times the slabs. That squared link is the whole lesson: \\(y \\propto x^2\\)."),
    ],
  },
  "teach": {
    "bronze": {
      "display": r"\(y \propto x^2\). When \(x = 3\), \(y = 18\). Find \(y\) when \(x = 5\).",
      "label": "Together: your first square law",
      "steps": [
        {"say": "y ∝ x² means y = k×x². First find k from the pair x = 3, y = 18.",
         "pre": "3² = ", "post": "", "answer": 9, "hint": "Square the given x: 3 × 3."},
        {"pre": "k = 18 ÷ 9 = ", "post": "", "answer": 2,
         "hint": "Divide y by the squared x.", "done": "k = 2. That fixed number stays for every new x."},
        {"say": "Now use k = 2 with the new x = 5.", "phase": "substitute",
         "pre": "5² = ", "post": "", "answer": 25, "hint": "Square the new x: 5 × 5."},
        {"pre": "y = 2 × 25 = ", "post": "", "answer": 50,
         "hint": "Multiply k by the squared x."},
        {"say": "Check it lands back on the given pair:",
         "pre": "2 × 3² = 2 × 9 = ", "post": "", "answer": 18,
         "done": "Matches y = 18, so k = 2 is right and y = 50."},
      ],
    },
    "silver": {
      "display": r"\(y \propto \frac{1}{x^2}\). When \(x = 3\), \(y = 8\). Find \(y\) when \(x = 6\).",
      "label": "Together: the inverse-square twist",
      "steps": [
        {"say": "Inverse square: y = k ÷ x². The new move is finding k by MULTIPLYING, k = y × x².",
         "pre": "3² = ", "post": "", "answer": 9, "hint": "Square the given x: 3 × 3."},
        {"pre": "k = 8 × 9 = ", "post": "", "answer": 72,
         "hint": "Multiply y by the squared x.", "done": "Inverse laws multiply to find k, they do not divide."},
        {"say": "Now use k = 72 with the new x = 6.", "phase": "substitute",
         "pre": "6² = ", "post": "", "answer": 36, "hint": "Square the new x: 6 × 6."},
        {"pre": "y = 72 ÷ 36 = ", "post": "", "answer": 2,
         "hint": "Divide k by the new squared x."},
        {"say": "Check it lands back on the given pair:",
         "pre": "72 ÷ 3² = 72 ÷ 9 = ", "post": "", "answer": 8,
         "done": "Matches y = 8, so k = 72 is right and y = 2."},
      ],
    },
    "gold": {
      "display": r"\(y \propto x^3\). When \(x = 2\), \(y = 40\). Find \(x\) when \(y = 135\).",
      "label": "Together: reverse through a root",
      "steps": [
        {"say": "y = k×x³. Find k first, then the new move is reversing to find x with a cube root.",
         "pre": "2³ = ", "post": "", "answer": 8, "hint": "Cube the given x: 2 × 2 × 2."},
        {"pre": "k = 40 ÷ 8 = ", "post": "", "answer": 5,
         "hint": "Divide y by the cubed x.", "done": "k = 5."},
        {"say": "Now reverse: 135 = 5×x³.", "phase": "substitute",
         "pre": "x³ = 135 ÷ 5 = ", "post": "", "answer": 27, "hint": "Divide the target y by k."},
        {"pre": "x = ∛27 = ", "post": "", "answer": 3,
         "hint": "Take the cube root: which number cubed is 27?"},
        {"say": "Check it lands on the target y:",
         "pre": "5 × 3³ = 5 × 27 = ", "post": "", "answer": 135,
         "done": "Matches y = 135, so x = 3 is right."},
      ],
    },
  },
}

# ---- 7. VERIFY final boxes land on solutions & recompute everything ------
errs = []
def approx(a, b, tol=1e-6): return abs(a-b) <= tol

# Fresh-solve each bank problem's solution independently.
fresh = {
  ("bronze",0):[3],("bronze",1):[80],("bronze",2):[20],("bronze",3):[72],
  ("bronze",4):[7],("bronze",5):[50],("bronze",6):[5],("bronze",7):[63],
  ("silver",0):[0.8],("silver",1):[25],("silver",2):[135],("silver",3):[5],
  ("silver",4):[4],("silver",5):[50],("silver",6):[400],
  ("gold",0):[2],("gold",1):[5],("gold",2):[72],("gold",3):[4],("gold",4):[6],
}
for (t,i),sol in fresh.items():
    if pb[t][i]["solutions"] != sol:
        errs.append(f"{t}[{i}] stored {pb[t][i]['solutions']} != fresh {sol}")

# every misconception expect != solution
for t in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[t]):
        s=tuple(p["solutions"])
        if s in seen: errs.append(f"DUP solution {s} in {t}[{i}]")
        seen.add(s)
        for m in p.get("misconceptions",[]):
            if "expect" not in m: errs.append(f"{t}[{i}] mis missing expect")
            e=m.get("expect")
            if e is not None and approx(float(e), float(p["solutions"][0]), 0.011):
                errs.append(f"{t}[{i}] expect {e} == solution")
        # last solution-bearing check: the phase box answer or a box equals solution somewhere
        gs=p.get("guided_steps",[])
        boxvals=[st["answer"] for st in gs if st.get("answer") is not None]
        if not any(approx(float(v),float(p["solutions"][0]),0.011) for v in boxvals):
            errs.append(f"{t}[{i}] no guided box equals solution {p['solutions']}")

print("BUILD CHECKS:", "OK" if not errs else "FAIL")
for e in errs: print("  -", e)

json.dump(pd, open("lesson_maths-ocr_ratio-proportion-L05.json","w",encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("wrote lesson_maths-ocr_ratio-proportion-L05.json")
