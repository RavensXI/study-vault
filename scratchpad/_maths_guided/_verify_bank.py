# -*- coding: utf-8 -*-
import json, re, sys
from math import gcd

def parse_quad(disp):
    # Factorise \(A x^2 + B x + C\)
    s = disp.replace("\\(","").replace("\\)","").replace(" ","")
    s = s.replace("Factorise","")
    # normalize
    m = re.search(r'([+-]?\d*)x\^2([+-]\d*)x([+-]\d+)', s)
    if not m: return None
    def co(t, default=1):
        if t in ("","+"): return 1
        if t=="-": return -1
        return int(t)
    A=co(m.group(1)); B=co(m.group(2)); C=int(m.group(3))
    return (A,B,C)

def parse_opt(opt):
    # \((p x + q)(r x + s)\)  brackets may be (q)(rx+s)? all are (px+q)(rx+s) or (x+q)(rx+s)
    s = opt.replace("\\(","").replace("\\)","").replace(" ","")
    brs = re.findall(r'\(([^)]*)\)', s)
    if len(brs)!=2: return None
    def parse_lin(b):
        # forms: px+q  or x+q or -x+q etc, or px-q
        mm = re.match(r'([+-]?\d*)x([+-]\d+)$', b)
        if not mm: return None
        p = mm.group(1)
        if p in ("","+"): p=1
        elif p=="-": p=-1
        else: p=int(p)
        q=int(mm.group(2))
        return (p,q)
    l1=parse_lin(brs[0]); l2=parse_lin(brs[1])
    if not l1 or not l2: return None
    return (l1,l2)

def expand(l1,l2):
    (p,q),(r,s)=l1,l2
    return (p*r, p*s+q*r, q*s)

def reducible(l1,l2):
    flags=[]
    for (a,b),name in [(l1,'br1'),(l2,'br2')]:
        g=gcd(abs(a),abs(b)) if b!=0 else abs(a)
        if b!=0 and g>1:
            flags.append(name)
    return flags

def main(fn):
    pd=json.load(open(fn,encoding='utf-8'))
    pb=pd['problem_bank']
    for tier in ['bronze','silver','gold']:
        print(f"\n===== {tier} =====")
        for i,p in enumerate(pb[tier]):
            disp=p['display']; A,B,C=parse_quad(disp)
            opts=p['options']; sol=p['solutions'][0]
            print(f"[{i}] {disp}  -> A={A} B={B} C={C}  sol_idx={sol}")
            correct_idx=[]
            for j,o in enumerate(opts):
                po=parse_opt(o)
                if not po:
                    print(f"     opt{j} PARSE FAIL: {o}"); continue
                ex=expand(*po)
                red=reducible(*po)
                ok = (ex==(A,B,C))
                if ok: correct_idx.append(j)
                tag = "  <== CORRECT" if ok else ""
                redtag = f"  REDUCIBLE:{red}" if red else ""
                print(f"     opt{j} {o} -> {ex}{tag}{redtag}")
            if correct_idx!=[sol]:
                print(f"     !!! solution mismatch: expands-correct={correct_idx} stored={sol}")
            # check misconception expects
            for m in p.get('misconceptions',[]):
                e=m.get('expect')
                if e is not None:
                    if e==sol: print(f"     !!! misconception {m.get('pattern')} expect==solution ({e})")

if __name__=='__main__':
    main(sys.argv[1])
