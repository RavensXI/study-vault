import json, math

live=json.load(open('_CHK_gL05_live.json',encoding='utf-8'))['practice_data']
LID="2d827ad4-80ab-4327-81f8-a2e5cec4f50a"
pre=[e for e in json.load(open('_pre_dump_maths-ocr.json',encoding='utf-8')) if e['id']==LID]
pre=pre[0]['practice_data'] if pre else None

print("=== PRESERVATION vs pre-dump ===")
if pre:
    for k in ['related_videos','topic_links','worked_examples']:
        same = json.dumps(pre.get(k),sort_keys=True)==json.dumps(live.get(k),sort_keys=True)
        print(f"{k}: {'UNCHANGED' if same else 'CHANGED'}")
    print("pre keys:", list(pre.keys()))
else:
    print("no pre entry")

print("\n=== MISCONCEPTION EXPECT recompute ===")
def r1(x): return round(x,1)
checks=[]
# gold
checks.append(('gold[0]',8+6,14))
checks.append(('gold[2]',math.sqrt(3**2+4**2),5))  # =5
checks.append(('gold[3]',9+12,21))
checks.append(('gold[4] sin32',50*math.sin(math.radians(32)),26.5))
# bronze
checks.append(('bronze[0]',6+8,14))
checks.append(('bronze[1] add',math.sqrt(13**2+5**2),13.9))
checks.append(('bronze[2]',5+12,17))
checks.append(('bronze[3] add',math.sqrt(10**2+6**2),11.7))
checks.append(('bronze[4]',9+12,21))
checks.append(('bronze[6]',8+15,23))
checks.append(('bronze[7] add',math.sqrt(25**2+7**2),26.0))
# silver
checks.append(('silver[0] 12/5',math.degrees(math.atan(12/5)),67.4))
checks.append(('silver[1] sin',10*math.sin(math.radians(40)),6.4))
checks.append(('silver[2] mult',7*math.sin(math.radians(30)),3.5))
checks.append(('silver[3] sininv',math.degrees(math.asin(0.8)),53.1))
checks.append(('silver[4] add',math.sqrt(5**2+3**2),5.8))
checks.append(('silver[5] sin',15*math.sin(math.radians(50)),11.5))
checks.append(('silver[6] cosinv',math.degrees(math.acos(0.28)),73.7))
for name,val,exp in checks:
    rv=r1(val)
    print(f"{name}: computed={val:.4f} ->{rv}  expect={exp}  {'OK' if abs(rv-exp)<0.05 else 'MISMATCH'}")

print("\n=== SOLUTIONS recompute (key ones, calc) ===")
sols=[
 ('gold[4]',50*math.tan(math.radians(32)),31.2),
 ('bronze[7]',math.sqrt(25**2-7**2),24),
 ('silver[0]',math.degrees(math.atan(5/12)),22.6),
 ('silver[1]',10*math.tan(math.radians(40)),8.4),
 ('silver[2]',7/math.sin(math.radians(30)),14),
 ('silver[3]',math.degrees(math.acos(0.8)),36.9),
 ('silver[5]',15*math.cos(math.radians(50)),9.6),
 ('silver[6]',math.degrees(math.asin(7/25)),16.3),
]
for name,val,exp in sols:
    print(f"{name}: {val:.4f} ->{r1(val)} vs stored {exp} {'OK' if abs(r1(val)-exp)<0.05 else 'MISMATCH'}")

print("\n=== INTERMEDIATE 2dp boxes ===")
ib=[
 ('gold teach tan32? no', None,None),
 ('gold[4] tan32 2dp',math.tan(math.radians(32)),0.62),
 ('silver[0] 5/12 2dp',5/12,0.42),
 ('silver[0] check tan22.6',math.tan(math.radians(22.6)),0.42),
 ('silver[1] tan40 2dp',math.tan(math.radians(40)),0.84),
 ('silver[3] check cos36.9',math.cos(math.radians(36.9)),0.80),
 ('silver[5] cos50 2dp',math.cos(math.radians(50)),0.64),
 ('silver[6] check sin16.3',math.sin(math.radians(16.3)),0.28),
 ('teachgold 2/9 2dp',2/9,0.22),
 ('teachgold tan12.5 2dp',math.tan(math.radians(12.5)),0.22),
 ('teachgold sqrt85',math.sqrt(2**2+9**2),9.2),
 ('teachgold atan(2/9)',math.degrees(math.atan(2/9)),12.5),
 ('teachsilver atan0.75',math.degrees(math.atan(0.75)),36.9),
 ('teachsilver tan36.9',math.tan(math.radians(36.9)),0.75),
]
for name,val,exp in ib:
    if val is None: continue
    print(f"{name}: {val:.5f} ->2dp {round(val,2)} vs {exp} {'OK' if abs(round(val,2)-exp)<0.005 else 'CHK'}")
