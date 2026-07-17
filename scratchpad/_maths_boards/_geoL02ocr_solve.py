import json, math

pd = json.load(open("_geoL02ocr_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

def r1(x): return round(x,1)

checks = {
 "bronze": [
   ("rect 9x4", 9*4, 36, False),
   ("tri b10 h6", 0.5*10*6, 30, False),
   ("perim rect 8x5", 2*(8+5), 26, False),
   ("para b7 h4", 7*4, 28, False),
   ("trap 6,10 h4", 0.5*(6+10)*4, 32, False),
   ("circ r7", 2*math.pi*7, 44.0, True),
   ("sq 9", 81, 81, False),
   ("perim equi 5", 15, 15, False),
 ],
 "silver": [
   ("area circ r6", math.pi*36, 113.1, True),
   ("circ d14", math.pi*14, 44.0, True),
   ("r from area 50.3", math.sqrt(50.3/math.pi), 4.0, True),
   ("trap 5,11 h8", 0.5*16*8, 64, False),
   ("sector r6 a90 area", (90/360)*math.pi*36, 28.3, True),
   ("arc r10 a72", (72/360)*2*math.pi*10, 12.6, True),
   ("rect-circle r3", 12*8 - math.pi*9, 67.7, True),
 ],
 "gold": [
   ("semicircle d12 area", 0.5*math.pi*36, 56.5, True),
   ("sector r8 a135 arc", (135/360)*2*math.pi*8, 18.8, True),
   ("sector r5 arc10 angle", 10/(2*math.pi*5)*360, 115, True),
   ("ring r3->r5", math.pi*(25-9), 50.3, True),
   ("sector area75 r10 angle", 75/(math.pi*100)*360, 86, True),
 ],
}

for tier, rows in checks.items():
    print(f"=== {tier} ===")
    for i,(name, raw, expected, calc) in enumerate(rows):
        stored = pb[tier][i]["solutions"][0]
        got = r1(raw) if isinstance(expected,float) else round(raw)
        ok = abs(got-stored) < 0.05
        flag = "OK" if abs(got-stored)<0.05 and abs(got-expected)<0.05 else "**MISMATCH**"
        print(f"[{i}] {name}: raw={raw:.4f} rounded={got} stored={stored} {flag}")
