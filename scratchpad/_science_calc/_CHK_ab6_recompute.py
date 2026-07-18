import json
d = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/"
pd = json.load(open(d+"_CHK_ab6_canon.json", encoding="utf-8"))

errs = []

def chk(label, got, exp):
    ok = got == exp
    if not ok:
        errs.append(f"{label}: computed {got} != stored {exp}")
    return ok

# ---- solutions independently ----
# gold0 N2+3H2->2NH3 945,436,391
chk("gold0", 945+3*436 - 6*391, pd["problem_bank"]["gold"][0]["solutions"][0])
# gold1 CH4+2O2->CO2+2H2O 412,498,743,463
chk("gold1", (4*412+2*498)-(2*743+4*463), pd["problem_bank"]["gold"][1]["solutions"][0])
# gold2 out = 1200-300
chk("gold2", 1200-300, pd["problem_bank"]["gold"][2]["solutions"][0])
# bronze0 break reactants 436+243
chk("bronze0", 436+243, pd["problem_bank"]["bronze"][0]["solutions"][0])
# bronze1 made 2*432
chk("bronze1", 2*432, pd["problem_bank"]["bronze"][1]["solutions"][0])
# bronze2 679-864
chk("bronze2", 679-864, pd["problem_bank"]["bronze"][2]["solutions"][0])
# bronze3 500-720
chk("bronze3", 500-720, pd["problem_bank"]["bronze"][3]["solutions"][0])
# bronze4 endo=2
chk("bronze4", 2, pd["problem_bank"]["bronze"][4]["solutions"][0])
# silver0 2*436+498
chk("silver0", 2*436+498, pd["problem_bank"]["silver"][0]["solutions"][0])
# silver1 4 O-H
chk("silver1", 2*2, pd["problem_bank"]["silver"][1]["solutions"][0])
# silver2 4*463
chk("silver2", 4*463, pd["problem_bank"]["silver"][2]["solutions"][0])
# silver3 1370-1852
chk("silver3", 1370-1852, pd["problem_bank"]["silver"][3]["solutions"][0])

# ---- expects (commit the error) ----
# gold0 forgot_coefficient: made=3*391=1173 -> 2253-1173
chk("gold0.mc0_expect", (945+3*436)-3*391, pd["problem_bank"]["gold"][0]["misconceptions"][0]["expect"])
# gold0 wrong_sign: 2346-2253
chk("gold0.mc1_expect", 6*391-(945+3*436), pd["problem_bank"]["gold"][0]["misconceptions"][1]["expect"])
# gold1 wrong_count one C=O: made=743+1852=2595 -> 2644-2595
chk("gold1.mc0_expect", (4*412+2*498)-(743+4*463), pd["problem_bank"]["gold"][1]["misconceptions"][0]["expect"])
# gold1 wrong_sign 3338-2644
chk("gold1.mc1_expect", (2*743+4*463)-(4*412+2*498), pd["problem_bank"]["gold"][1]["misconceptions"][1]["expect"])
# gold2 wrong_rearrange add: 1200+300
chk("gold2.mc0_expect", 1200+300, pd["problem_bank"]["gold"][2]["misconceptions"][0]["expect"])
# bronze0 wrong_count add H-Cl: 436+243+432
chk("bronze0.mc0_expect", 436+243+432, pd["problem_bank"]["bronze"][0]["misconceptions"][0]["expect"])
# bronze1 forgot_coeff: 432
chk("bronze1.mc0_expect", 432, pd["problem_bank"]["bronze"][1]["misconceptions"][0]["expect"])
# bronze2 wrong_sign 864-679
chk("bronze2.mc0_expect", 864-679, pd["problem_bank"]["bronze"][2]["misconceptions"][0]["expect"])
# bronze3 wrong_sign 720-500
chk("bronze3.mc0_expect", 720-500, pd["problem_bank"]["bronze"][3]["misconceptions"][0]["expect"])
# bronze4 wrong_sign expect 1
chk("bronze4.mc0_expect", 1, pd["problem_bank"]["bronze"][4]["misconceptions"][0]["expect"])
# silver0 forgot_coeff one H-H: 436+498
chk("silver0.mc0_expect", 436+498, pd["problem_bank"]["silver"][0]["misconceptions"][0]["expect"])
# silver1 forgot_coeff: 2
chk("silver1.mc0_expect", 2, pd["problem_bank"]["silver"][1]["misconceptions"][0]["expect"])
# silver2 wrong_count 2*463
chk("silver2.mc0_expect", 2*463, pd["problem_bank"]["silver"][2]["misconceptions"][0]["expect"])
# silver3 wrong_sign 1852-1370
chk("silver3.mc0_expect", 1852-1370, pd["problem_bank"]["silver"][3]["misconceptions"][0]["expect"])

# ---- teach walk final answers ----
# bronze H2+Br2->2HBr 436,193,366
chk("teach.bronze", (436+193)-2*366, pd["guided"]["teach"]["bronze"]["steps"][-1]["answer"])
# silver N2+O2->2NO 945,498,630
chk("teach.silver", (945+498)-2*630, pd["guided"]["teach"]["silver"]["steps"][-1]["answer"])
# gold 2CO+O2->2CO2 1077,498,805
chk("teach.gold", (2*1077+498)-4*805, pd["guided"]["teach"]["gold"]["steps"][-1]["answer"])

# ---- opener ----
chk("opener.box1", 864-679, pd["guided"]["opener"]["steps"][1]["answer"])
chk("opener.box2", 720-500, pd["guided"]["opener"]["steps"][3]["answer"])

# expects distinct from solutions (dead-expect check, no accept fields => exact)
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        acc = p.get("accept")
        for j,mc in enumerate(p.get("misconceptions",[])):
            e = mc.get("expect")
            if e is None: continue
            win = acc if acc is not None else 0
            if abs(e - sol) <= win:
                errs.append(f"DEAD EXPECT {tier}[{i}].mc[{j}]: expect {e} within accept({win}) of sol {sol}")

print("ERRORS:", len(errs))
for e in errs: print("  ", e)
print("ALL CLEAN" if not errs else "FAILURES ABOVE")
