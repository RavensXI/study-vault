import json,re,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live.json",encoding="utf-8"))
# parse "\(LHS = RHS\)" into poly ax^2+bx+c, verify each stored solution root
def parse_side(s):
    s=s.replace("−","-").replace(" ","")
    # tokens
    a=b=c=0
    for m in re.finditer(r'([+-]?\d*)x\^2|([+-]?\d*)x(?!\^)|([+-]?\d+)',s):
        if m.group(1) is not None:
            v=m.group(1); a+= int(v+"1" if v in("","+","-") else v)
        elif m.group(2) is not None:
            v=m.group(2); b+= int(v+"1" if v in("","+","-") else v)
        elif m.group(3) is not None:
            c+= int(m.group(3))
    return a,b,c
bad=0
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        d=p["display"].replace("\(","").replace("\)","")
        L,R=d.split("=")
        la,lb,lc=parse_side(L); ra,rb,rc=parse_side(R)
        A,B,C=la-ra,lb-rb,lc-rc
        for sol in p["solutions"]:
            val=A*sol*sol+B*sol+C
            if val!=0:
                bad+=1; print(f"FAIL {tier}[{i}] {p['display']} sol={sol} -> {val} (A{A} B{B} C{C})")
        # last guided box should be 0 (check step)
        gs=p["guided_steps"]
        boxes=[s for s in gs if "answer" in s]
        if boxes[-1]["answer"]!=0:
            print(f"NOTE {tier}[{i}] last box not 0: {boxes[-1]['answer']}")
print("substitution failures:",bad)
