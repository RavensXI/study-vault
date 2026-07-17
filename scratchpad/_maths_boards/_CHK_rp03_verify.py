import json, math

live = json.load(open("_CHK_rp03_live.json", encoding="utf-8"))
pd = live["practice_data"]
errs = []

def approxeq(a, b, tol=0.05):
    return abs(a-b) <= tol

# ---- G2 cylinder ----
vol = math.pi * 9 * 7
print("63pi =", round(vol,4), "-> stored 197.92 ok?", approxeq(vol,197.92,0.01))
dens = 594/vol
print("594/vol =", round(dens,5), "-> round 1dp =", round(dens,1), "stored sol 3")
# radius not squared
volns = math.pi*3*7
print("radius not squared vol =", round(volns,4), "dens =", round(594/volns,4), "expect 9")
# check 3*197.92
print("3*197.92 =", 3*197.92)

# ---- S4 72/3.6 ----
print("72/3.6 =", 72/3.6, "72*3.6 =", 72*3.6)
# ---- S5 600/0.02 ----
print("600/0.02 =", 600/0.02, "600/0.04 =", 600/0.04)
# ---- S6 2h24 ----
print("50*2.4 =", 50*2.4, "50*2.24 =", 50*2.24, "50*2 =", 50*2)
# ---- S7 alloy ----
print("300/10 =", 300/10, "400/8 =", 400/8, "sum", 30+50)
# ---- silver cube ----
print("5^3 =", 5**3, "750/125 =", 750/125, "750/5 =", 750/5, "750/25 =", 750/25)
# ---- G1 ----
print("180/90 =", 180/90, "120/40 =", 120/40, "300/5 =", 300/5, "(90+40)/2 =", (90+40)/2)
# ---- gold teach ----
print("60/60 =", 60/60, "90/45 =", 90/45, "150/3 =", 150/3, "(60+45)/2 =", (60+45)/2)
# ---- silver teach ----
print("200/25 =", 200/25, "8*3.6 =", 8*3.6, "28.8/3.6 =", 28.8/3.6, "8*60 =", 8*60)
# ---- opener ----
print("120/2 =", 120/2)
# ---- G4 ----
print("500/1 =", 500/1, "500/2 =", 500/2)

# programmatic full sweep of every numeric box in guided_steps + solutions
print("\n=== systematic box eval ===")
def check_bank(tier):
    for i, p in enumerate(pd["problem_bank"][tier]):
        sols = p.get("solutions")
        gs = p.get("guided_steps", [])
        boxes = [s for s in gs if "answer" in s]
        if boxes:
            last = boxes[-1]["answer"]
        # report solution
        print(f"{tier}[{i}] sol={sols} boxes={[b['answer'] for b in boxes]}")
for t in ["bronze","silver","gold"]:
    check_bank(t)
