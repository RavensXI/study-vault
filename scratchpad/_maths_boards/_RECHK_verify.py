import json, math

live = json.load(open('_RECHK_live.json', encoding='utf-8'))
pre_list = json.load(open('_pre_dump_maths-ocr.json', encoding='utf-8'))
ID='2d827ad4-80ab-4327-81f8-a2e5cec4f50a'
pre = next((r for r in pre_list if r['id']==ID), None)
print("pre found:", pre is not None, "| pre title:", pre['title'] if pre else None)

fails=[]
def r1(x): return round(x,1)
def r2(x): return round(x,2)

pb = live['problem_bank']

# ---- fresh solve each problem ----
def check_sol(tier, i, computed, disp_dp=None):
    sol = pb[tier][i]['solutions'][0]
    ok = abs(computed - sol) < 1e-6
    if not ok:
        fails.append(f"{tier}[{i}] solution mismatch: stored {sol}, computed {computed} | {pb[tier][i]['display'][:60]}")
    return ok

# GOLD
check_sol('gold',0, math.sqrt(8**2+6**2))          #10
check_sol('gold',1, math.sqrt(10**2-6**2))         #8
check_sol('gold',2, math.sqrt(3**2+4**2+12**2))    #13
check_sol('gold',3, math.sqrt(9**2+12**2))         #15
check_sol('gold',4, r1(50*math.tan(math.radians(32)))) #31.2
# BRONZE
check_sol('bronze',0, math.sqrt(6**2+8**2))        #10
check_sol('bronze',1, math.sqrt(13**2-5**2))       #12
check_sol('bronze',2, math.sqrt(5**2+12**2))       #13
check_sol('bronze',3, math.sqrt(10**2-6**2))       #8
check_sol('bronze',4, math.sqrt(9**2+12**2))       #15
# bronze[5] MC index0 sin -> opposite&hyp -> SOH sin. correct
if pb['bronze'][5]['solutions'][0]!=0: fails.append("bronze[5] MC wrong index")
check_sol('bronze',6, math.sqrt(8**2+15**2))       #17
check_sol('bronze',7, math.sqrt(25**2-7**2))       #24
# SILVER
check_sol('silver',0, r1(math.degrees(math.atan(5/12))))  #22.6
check_sol('silver',1, r1(10*math.tan(math.radians(40))))  #8.4
check_sol('silver',2, r1(7/math.sin(math.radians(30))))   #14
check_sol('silver',3, r1(math.degrees(math.acos(8/10))))  #36.9
check_sol('silver',4, math.sqrt(5**2-3**2))               #4
check_sol('silver',5, r1(15*math.cos(math.radians(50))))  #9.6
check_sol('silver',6, r1(math.degrees(math.asin(7/25))))  #16.3

print("\n--- after solutions ---")
for f in fails: print("SOLFAIL:", f)

# ---- expects reproduce ----
exp_fail=[]
def cexp(tier,i,val,computed):
    if val is None: return
    if abs(computed-val)>0.05:
        exp_fail.append(f"{tier}[{i}] expect {val} but committing error gives {computed}")

cexp('gold',0,14, 8+6)
# gold1 expect null
cexp('gold',2,5, math.sqrt(3**2+4**2))
cexp('gold',3,21, 9+12)
cexp('gold',4,26.5, r1(50*math.sin(math.radians(32))))
cexp('bronze',0,14, 6+8)
cexp('bronze',1,13.9, r1(math.sqrt(13**2+5**2)))
cexp('bronze',2,17, 5+12)
cexp('bronze',3,11.7, r1(math.sqrt(10**2+6**2)))
cexp('bronze',4,21, 9+12)
cexp('bronze',6,23, 8+15)
cexp('bronze',7,26.0, r1(math.sqrt(25**2+7**2)))
cexp('silver',0,67.4, r1(math.degrees(math.atan(12/5))))
cexp('silver',1,6.4, r1(10*math.sin(math.radians(40))))
cexp('silver',2,3.5, r1(7*math.sin(math.radians(30))))
cexp('silver',3,53.1, r1(math.degrees(math.asin(8/10))))
cexp('silver',4,5.8, r1(math.sqrt(5**2+3**2)))
cexp('silver',5,11.5, r1(15*math.sin(math.radians(50))))
cexp('silver',6,73.7, r1(math.degrees(math.acos(7/25))))
print("\n--- expects ---")
for f in exp_fail: print("EXPFAIL:", f)
fails.extend(exp_fail)

# ---- preservation ----
print("\n--- preservation ---")
for k in ['related_videos','topic_links','worked_examples']:
    same = json.dumps(pre['practice_data'].get(k),sort_keys=True)==json.dumps(live.get(k),sort_keys=True)
    print(f"{k}: preserved={same}")
    if not same and k!='worked_examples':
        fails.append(f"{k} changed vs pre-dump")
# report worked_examples detail
print("pre worked_examples:", json.dumps(pre['practice_data'].get('worked_examples'))[:200])

print("\nTOTAL FAILS:", len(fails))
