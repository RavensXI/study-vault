import json, math
pd = json.load(open("_CHK_gL02ocr_live.json", encoding="utf-8"))["practice_data"]
pi = math.pi

# manually recompute each guided box answer and compare
# format: (path, expected_answer)
B = []
# teach gold: 6x6=36; pi*36->113.1; 113.097/6->18.8; 18.8*6=112.8
B += [("teach.gold[0]",6*6,pd["guided"]["teach"]["gold"]["steps"][0]["answer"]),
      ("teach.gold[1]",round(pi*36,1),pd["guided"]["teach"]["gold"]["steps"][1]["answer"]),
      ("teach.gold[2]",round((pi*36)/6,1),pd["guided"]["teach"]["gold"]["steps"][2]["answer"]),
      ("teach.gold[3]",round(18.8*6,1),pd["guided"]["teach"]["gold"]["steps"][3]["answer"])]
# teach bronze: 8x5=40;40/2=20;0.5*8=4;4*5=20
tb=pd["guided"]["teach"]["bronze"]["steps"]
B += [("teach.bronze[0]",8*5,tb[0]["answer"]),("teach.bronze[1]",40//2,tb[1]["answer"]),
      ("teach.bronze[2]",0.5*8,tb[2]["answer"]),("teach.bronze[3]",4*5,tb[3]["answer"])]
# teach silver: 16/2=8;8*8=64;0.5*pi*64->100.5;100.5*2=201
ts=pd["guided"]["teach"]["silver"]["steps"]
B += [("teach.silver[0]",16//2,ts[0]["answer"]),("teach.silver[1]",8*8,ts[1]["answer"]),
      ("teach.silver[2]",round(0.5*pi*64,1),ts[2]["answer"]),("teach.silver[3]",round(100.5*2),ts[3]["answer"])]
# opener: 6*4=24; 6+4+6+4=20
op=pd["guided"]["opener"]["steps"]
B += [("opener[0]",6*4,op[0]["answer"]),("opener[1]",6+4+6+4,op[1]["answer"])]

# bank guided_steps recompute (only numeric boxes)
def box(path, expr, node):
    B.append((path, expr, node["answer"]))

pb=pd["problem_bank"]
# bronze
gs=pb["bronze"][0]["guided_steps"]; box("bronze[0].gs[1]",4,gs[1]); box("bronze[0].gs[2]",9*4,gs[2]); box("bronze[0].gs[3]",9+9+9+9,gs[3])
gs=pb["bronze"][1]["guided_steps"]; box("bronze[1].gs[1]",10*6,gs[1]); box("bronze[1].gs[2]",60//2,gs[2]); box("bronze[1].gs[3]",30*2,gs[3])
gs=pb["bronze"][2]["guided_steps"]; box("bronze[2].gs[1]",8+5,gs[1]); box("bronze[2].gs[2]",13*2,gs[2]); box("bronze[2].gs[3]",8+8+5+5,gs[3])
gs=pb["bronze"][3]["guided_steps"]; box("bronze[3].gs[1]",7,gs[1]); box("bronze[3].gs[2]",7*4,gs[2]); box("bronze[3].gs[3]",7*4,gs[3])
gs=pb["bronze"][4]["guided_steps"]; box("bronze[4].gs[1]",6+10,gs[1]); box("bronze[4].gs[2]",16//2,gs[2]); box("bronze[4].gs[3]",8*4,gs[3]); box("bronze[4].gs[4]",64//2,gs[4])
gs=pb["bronze"][5]["guided_steps"]; box("bronze[5].gs[1]",2*7,gs[1]); box("bronze[5].gs[2]",round(pi*14),gs[2]); box("bronze[5].gs[3]",round(2*pi*7),gs[3])
gs=pb["bronze"][6]["guided_steps"]; box("bronze[6].gs[1]",9,gs[1]); box("bronze[6].gs[2]",9*9,gs[2]); box("bronze[6].gs[3]",9*9,gs[3])
gs=pb["bronze"][7]["guided_steps"]; box("bronze[7].gs[1]",3,gs[1]); box("bronze[7].gs[2]",3*5,gs[2]); box("bronze[7].gs[3]",5+5+5,gs[3])
# silver
gs=pb["silver"][0]["guided_steps"]; box("silver[0].gs[1]",6*6,gs[1]); box("silver[0].gs[2]",round(pi*36,1),gs[2]); box("silver[0].gs[3]",round((pi*36)/36,1),gs[3])
gs=pb["silver"][1]["guided_steps"]; box("silver[1].gs[1]",14,gs[1]); box("silver[1].gs[2]",round(pi*14),gs[2]); box("silver[1].gs[3]",round(2*pi*7),gs[3])
gs=pb["silver"][2]["guided_steps"]; box("silver[2].gs[1]",round(50.3/pi),gs[1]); box("silver[2].gs[2]",round(math.sqrt(16)),gs[2]); box("silver[2].gs[3]",round(pi*16,1),gs[3])
gs=pb["silver"][3]["guided_steps"]; box("silver[3].gs[1]",5+11,gs[1]); box("silver[3].gs[2]",16//2,gs[2]); box("silver[3].gs[3]",8*8,gs[3]); box("silver[3].gs[4]",128//2,gs[4])
gs=pb["silver"][4]["guided_steps"]; box("silver[4].gs[1]",6*6,gs[1]); box("silver[4].gs[2]",round(pi*36,1),gs[2]); box("silver[4].gs[3]",90/360,gs[3]); box("silver[4].gs[4]",round(0.25*113.1,1),gs[4]); box("silver[4].gs[5]",round(28.3*4,1),gs[5])
gs=pb["silver"][5]["guided_steps"]; box("silver[5].gs[1]",round(2*pi*10,1),gs[1]); box("silver[5].gs[2]",72/360,gs[2]); box("silver[5].gs[3]",round(0.2*62.8,1),gs[3]); box("silver[5].gs[4]",round(12.6*5),gs[4])
gs=pb["silver"][6]["guided_steps"]; box("silver[6].gs[1]",12*8,gs[1]); box("silver[6].gs[2]",round(pi*9,1),gs[2]); box("silver[6].gs[3]",round(96-28.3,1),gs[3]); box("silver[6].gs[4]",round(67.7+28.3),gs[4])
# gold
gs=pb["gold"][0]["guided_steps"]; box("gold[0].gs[1]",12//2,gs[1]); box("gold[0].gs[2]",round(0.5*pi*36,1),gs[2]); box("gold[0].gs[3]",round(56.5*2),gs[3])
gs=pb["gold"][1]["guided_steps"]; box("gold[1].gs[1]",135/360,gs[1]); box("gold[1].gs[2]",round(0.375*(2*pi*8),1),gs[2]); box("gold[1].gs[3]",round(18.8/0.375,1),gs[3])
gs=pb["gold"][2]["guided_steps"]; box("gold[2].gs[1]",round(2*pi*5,1),gs[1]); box("gold[2].gs[2]",round(10/31.416,4),gs[2]); box("gold[2].gs[3]",round(0.3183*360),gs[3]); box("gold[2].gs[4]",round(0.3183*31.416),gs[4])
gs=pb["gold"][3]["guided_steps"]; box("gold[3].gs[1]",25,gs[1]); box("gold[3].gs[2]",9,gs[2]); box("gold[3].gs[3]",25-9,gs[3]); box("gold[3].gs[4]",round(pi*16,1),gs[4]); box("gold[3].gs[5]",round(pi*25,1),gs[5])
gs=pb["gold"][4]["guided_steps"]; box("gold[4].gs[1]",round(pi*100,1),gs[1]); box("gold[4].gs[2]",round(75/314.16,4),gs[2]); box("gold[4].gs[3]",round(0.2387*360),gs[3]); box("gold[4].gs[4]",round(0.2387*314.16),gs[4])

bad=0
for path,comp,stored in B:
    ok = abs(float(comp)-float(stored))<=0.06
    if not ok:
        bad+=1; print(f"BAD {path}: recomputed={comp} stored={stored}")
print(f"\nBoxes checked: {len(B)}  mismatches: {bad}")
