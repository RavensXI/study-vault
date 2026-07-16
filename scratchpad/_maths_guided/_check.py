import json, math
d=json.load(open('_live_L06.json',encoding='utf-8'))

def arcsin(x): return math.degrees(math.asin(x))
def arccos(x): return math.degrees(math.acos(x))

print("=== FRESH SOLVES ===")
# gold
g=d['problem_bank']['gold']
print("G0 area30,8,11:", round(arcsin(60/88),1), "stored", g[0]['solutions'])
print("G1 c 7,9,120:", round(math.sqrt(49+81-2*7*9*math.cos(math.radians(120))),1), g[1]['solutions'])
print("G2 largest 5,6,7:", round(arccos((25+36-49)/60),1), g[2]['solutions'])
print("G3 obtuse B 10,14,30:", round(180-arcsin(14*0.5/10),1), g[3]['solutions'])
print("G4 pgram 8,12,65:", round(8*12*math.sin(math.radians(65)),1), g[4]['solutions'])
b=d['problem_bank']['bronze']
print("B0:", round(0.5*6*10*math.sin(math.radians(30)),1), b[0]['solutions'])
print("B1:", round(0.5*8*5*math.sin(math.radians(40)),1), b[1]['solutions'])
print("B2 b=10sin90/sin30:", round(10*math.sin(math.radians(90))/math.sin(math.radians(30)),1), b[2]['solutions'])
print("B3:", round(0.5*7*12*math.sin(math.radians(45)),1), b[3]['solutions'])
print("B4 b=6*0.8/0.5:", round(6*0.8/0.5,2), b[4]['solutions'])
print("B5:", round(0.5*9*9*math.sin(math.radians(60)),1), b[5]['solutions'])
print("B6 a2=25+49-70cos60:", round(25+49-70*math.cos(math.radians(60)),1), b[6]['solutions'])
print("B7:", round(0.5*10*14*math.sin(math.radians(55)),1), b[7]['solutions'])
s=d['problem_bank']['silver']
print("S0 b 40,75,8:", round(8*math.sin(math.radians(75))/math.sin(math.radians(40)),1), s[0]['solutions'])
print("S1 c 5,7,50:", round(math.sqrt(25+49-70*math.cos(math.radians(50))),1), s[1]['solutions'])
print("S2 A 10,8,6:", round(arccos((64+36-100)/96),1), s[2]['solutions'])
print("S3 B 12,40,15:", round(arcsin(15*math.sin(math.radians(40))/12),1), s[3]['solutions'])
print("S4 area 11,13,52:", round(0.5*11*13*math.sin(math.radians(52)),1), s[4]['solutions'])
print("S5 C 9,11,14:", round(arccos((81+121-196)/198),1), s[5]['solutions'])
print("S6 a 35,80,10:", round(10*math.sin(math.radians(35))/math.sin(math.radians(80)),1), s[6]['solutions'])

print("\n=== EXPECTS ===")
print("G0 no half 30/88:", round(arcsin(30/88),1))
print("G1 cos+0.5:", round(math.sqrt(130-63),1))
print("G2 opp 5:", round(arccos((36+49-25)/84),1))
print("G4 one tri:", round(0.5*8*12*math.sin(math.radians(65)),1))
print("B0 no half:", round(6*10*math.sin(math.radians(30)),1))
print("B1 no half:", round(8*5*math.sin(math.radians(40)),1))
print("B2 swap:", round(10*math.sin(math.radians(30))/math.sin(math.radians(90)),1))
print("B7 no half:", round(10*14*math.sin(math.radians(55)),1))
print("S0 inv:", round(8*math.sin(math.radians(40))/math.sin(math.radians(75)),1))
print("S1 sqrt74:", round(math.sqrt(74),1))
print("S3 swap:", round(arcsin(12*math.sin(math.radians(40))/15),1))
print("S5 sign:", round(arccos(-6/198),1))
print("S6 inv:", round(10*math.sin(math.radians(80))/math.sin(math.radians(35)),1))
print("Bronze4 inv:", round(6*0.5/0.8,2))

print("\n=== TEACH ===")
print("gold sinB 12sin25/8:", round(12*math.sin(math.radians(25))/8,4), "acute", round(arcsin(12*math.sin(math.radians(25))/8),1))
print("silver c:", round(math.sqrt(136-60),1))

print("\n=== EM DASH SCAN ===")
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+f"[{i}]")
    elif isinstance(o,str):
        if '—' in o or '–' in o: print("DASH at",path,":",o[:60])
walk(d)
print("scan done")
