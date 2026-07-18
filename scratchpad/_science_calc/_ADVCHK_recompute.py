import json
pd = json.load(open("_ADVCHK_canon.json", encoding="utf-8"))
errs = []

def close(a, b, tol=0.005):
    return abs(a-b) <= tol

# ---- Bank: fresh solve + expects + box tolerance ----
bank = pd["problem_bank"]
def solve_pct(orig, new):
    return (new-orig)/orig*100

# Fresh solutions computed independently
expected_solutions = {
    ("gold",0): 4000, ("gold",1): 160, ("gold",2): -25,
    ("bronze",0): 5.67, ("bronze",1): 25, ("bronze",2): -20,
    ("bronze",3): 3, ("bronze",4): 150, ("bronze",5): 200,
    ("silver",0): 900, ("silver",1): -25, ("silver",2): 480, ("silver",3): 22.0,
}
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(bank[tier]):
        sol = p["solutions"][0]
        exp = expected_solutions[(tier,i)]
        if not close(sol, exp, 0.005):
            errs.append(f"{tier}[{i}] solution {sol} != fresh {exp}")
        # box tolerance: every guided_steps box answer must be a number
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                errs.append(f"{tier}[{i}].guided_steps[{j}] non-numeric answer {st['answer']!r}")
        # expects outside accept
        acc = p.get("accept", 0.0)
        for k,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is None: continue
            if abs(e - sol) <= acc:
                errs.append(f"{tier}[{i}].misconceptions[{k}] DEAD expect {e} inside accept {acc} of {sol}")

# Recompute specific box chains
def chk(label, got, want):
    if not close(got, want):
        errs.append(f"{label}: computed {want} but box says {got}")

# gold0
g0 = bank["gold"][0]["guided_steps"]
chk("gold0 sum", g0[1]["answer"], 5+3+6+4+5+7+4+6)
chk("gold0 mean", g0[2]["answer"], 40/8)
chk("gold0 quad", g0[3]["answer"], 400/0.5)
chk("gold0 pop", g0[4]["answer"], 5*800)
chk("gold0 dens", g0[6]["answer"], 5/0.5)
chk("gold0 chk", g0[7]["answer"], 10*400)
# gold1
g1 = bank["gold"][1]["guided_steps"]
chk("gold1 change", g1[1]["answer"], 7.8-3)
chk("gold1 div", g1[2]["answer"], 4.8/3)
chk("gold1 x100", g1[3]["answer"], 1.6*100)
chk("gold1 chk", g1[5]["answer"], 1.6*3)
# gold2
g2 = bank["gold"][2]["guided_steps"]
chk("gold2 y1", g2[1]["answer"], 12*800)
chk("gold2 y2", g2[2]["answer"], 9*800)
chk("gold2 chg", g2[3]["answer"], 7200-9600)
chk("gold2 div", g2[4]["answer"], -2400/9600)
chk("gold2 x100", g2[5]["answer"], -0.25*100)
chk("gold2 chk", g2[7]["answer"], (9-12)/12*100)
# bronze0 earthworm
b0 = bank["bronze"][0]["guided_steps"]
chk("bronze0 sum", b0[1]["answer"], 4+7+5+6+4+8)
chk("bronze0 mean", b0[3]["answer"], round(34/6,2))
chk("bronze0 chk", b0[5]["answer"], round(5.67*6,2))
# bronze checks for pct/pop
chk("bronze1 chg", bank["bronze"][1]["guided_steps"][1]["answer"], 250-200)
chk("bronze2 chg", bank["bronze"][2]["guided_steps"][1]["answer"], 240-300)
chk("bronze3 sum", bank["bronze"][3]["guided_steps"][1]["answer"], 3+2+4+3+3)
chk("bronze4 quad", bank["bronze"][4]["guided_steps"][1]["answer"], 50/1)
chk("bronze5 chg", bank["bronze"][5]["guided_steps"][1]["answer"], 15-5)
# silver0
s0 = bank["silver"][0]["guided_steps"]
chk("silver0 sum", s0[1]["answer"], 3+5+4+6+3+5+4+4+6+5)
chk("silver0 mean", s0[2]["answer"], 45/10)
chk("silver0 pop", s0[4]["answer"], 4.5*200)
# silver2
s2 = bank["silver"][2]["guided_steps"]
chk("silver2 sum", s2[1]["answer"], 2+3+1+4+2)
chk("silver2 mean", s2[2]["answer"], 12/5)
chk("silver2 quad", s2[3]["answer"], 100/0.5)
chk("silver2 pop", s2[4]["answer"], 2.4*200)
# silver3
s3 = bank["silver"][3]["guided_steps"]
chk("silver3 chg", s3[1]["answer"], 427-350)
chk("silver3 div", s3[2]["answer"], 77/350)
chk("silver3 x100", s3[3]["answer"], 0.22*100)

# expects recompute
chk("gold0 wrong_area", bank["gold"][0]["misconceptions"][0]["expect"], 5*400)
chk("gold0 forgot_step", bank["gold"][0]["misconceptions"][1]["expect"], 40*800)
chk("gold1 wrong_denom", bank["gold"][1]["misconceptions"][0]["expect"], round(4.8/7.8*100,2))
chk("gold2 wrong_denom", bank["gold"][2]["misconceptions"][0]["expect"], round(-2400/7200*100,2))
chk("bronze1 wrong_denom", bank["bronze"][1]["misconceptions"][0]["expect"], 50/250*100)
chk("bronze2 wrong_denom", bank["bronze"][2]["misconceptions"][0]["expect"], (240-300)/240*100)
chk("bronze5 wrong_denom", bank["bronze"][5]["misconceptions"][0]["expect"], round(10/15*100,2))
chk("silver0 forgot_step", bank["silver"][0]["misconceptions"][0]["expect"], 45*200)
chk("silver1 wrong_denom", bank["silver"][1]["misconceptions"][0]["expect"], round(-60/180*100,2))
chk("silver2 wrong_area", bank["silver"][2]["misconceptions"][0]["expect"], 2.4*100)
chk("silver3 wrong_denom", bank["silver"][3]["misconceptions"][0]["expect"], round(77/427*100,2))

# teach walks
t = pd["guided"]["teach"]
chk("teach.gold spr sum", t["gold"]["steps"][1]["answer"], 2+4+3+5+6)
chk("teach.gold spr mean", t["gold"]["steps"][2]["answer"], 20/5)
chk("teach.gold sum sum", t["gold"]["steps"][3]["answer"], 6+8+7+9+10)
chk("teach.gold sum mean", t["gold"]["steps"][4]["answer"], 40/5)
chk("teach.gold chg", t["gold"]["steps"][5]["answer"], 8-4)
chk("teach.gold pct", t["gold"]["steps"][6]["answer"], 4/4*100)
chk("teach.bronze sum", t["bronze"]["steps"][1]["answer"], 6+9+7+8+10)
chk("teach.bronze mean", t["bronze"]["steps"][3]["answer"], 40/5)
chk("teach.silver quad", t["silver"]["steps"][1]["answer"], 400/0.5)
chk("teach.silver pop", t["silver"]["steps"][2]["answer"], 8*800)
chk("teach.silver dens", t["silver"]["steps"][4]["answer"], 8/0.5)
chk("teach.silver chk", t["silver"]["steps"][5]["answer"], 16*400)

# opener
op = pd["guided"]["opener"]["steps"]
chk("opener share", op[1]["answer"], 30/5)
chk("opener pct", op[3]["answer"], 2/8*100)

# board neutrality
import re
blob = json.dumps(pd, ensure_ascii=False)
for bad in ["AQA","Edexcel","OCR","WJEC","Eduqas","equation sheet","must memorise","on your sheet"]:
    if bad.lower() in blob.lower():
        errs.append(f"BOARD-SPECIFIC term present: {bad}")

# em dash
if "—" in blob:
    errs.append("EM DASH present in student-facing content")

print("ERRORS:" if errs else "ALL CLEAN")
for e in errs: print(" -", e)
