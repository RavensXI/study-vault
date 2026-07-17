import json, re

pd = json.load(open("_chk_L12_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# em dash scan across student-facing strings
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note": continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash = []
for p,s in walk(pd):
    if "—" in s:
        emdash.append((p,s))
print("EM DASHES:", len(emdash))
for p,s in emdash: print("  ", p, repr(s[:80]))

# check number-line SVG dot positions programmatically
def check_numberline(svg, lo, hi, openpts, filledpts, tag):
    # extract circles
    circs = re.findall(r'<circle cx="([\d.]+)" cy="[\d.]+" r="([\d.]+)"([^>]*)/>', svg)
    # ticks map: text labels
    texts = re.findall(r'<text x="([\d.]+)"[^>]*>(-?\d+)</text>', svg)
    tickmap = {int(v): float(x) for x,v in texts}
    errs=[]
    # verify open (r=4, has stroke fill bg) vs filled (r=3.5 fill #3b82f6)
    opens=[]; filled=[]
    for cx,r,rest in circs:
        cx=float(cx)
        if 'faf8f5' in rest or 'sv-bg' in rest:
            opens.append(cx)
        elif '#3b82f6' in rest:
            filled.append(cx)
    # map back to values
    def val_of(px):
        best=None;bd=99
        for val,x in tickmap.items():
            if abs(x-px)<bd: bd=abs(x-px);best=val
        return best if bd<1.0 else f"?{px}"
    ov=sorted(val_of(c) for c in opens)
    fv=sorted(val_of(c) for c in filled)
    print(f"{tag}: open={ov} filled={fv} (expect open={sorted(openpts)} filled={sorted(filledpts)})")
    if ov!=sorted(openpts): errs.append(f"{tag} open mismatch")
    if fv!=sorted(filledpts): errs.append(f"{tag} filled mismatch")
    return errs

allerr=[]
# S5 number line
s5 = pb["silver"][4]["display"]
allerr+=check_numberline(s5, -3,6,[-2,5],[-1,0,1,2,3,4],"silver[4] numberline")
# G5 number line
g5 = pb["gold"][4]["display"]
allerr+=check_numberline(g5, 0,6,[1,5],[2,3,4],"gold[4] numberline")
print("SVG errs:", allerr)
