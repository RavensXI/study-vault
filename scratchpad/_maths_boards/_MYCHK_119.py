# -*- coding: utf-8 -*-
# hunt for any plausible error producing 1.119 for gold[1]
x0=2.0
def r3(v): return round(v,3)
cands={}
# formula family (a*x^3 + b)/(c*x^d), iterate to x1 or x2, with optional rounding of x1
import itertools
for a in [1,2]:
    for b in [5]:
        for c in [1,3]:
            for d in [1,2,3]:
                def f(x,a=a,b=b,c=c,d=d):
                    return (a*x**3+b)/(c*x**d)
                try:
                    x1=f(x0)
                    x2=f(x1)
                    for lbl,val in [("x1",x1),("x2",x2),("x2_r",f(round(x1,3)))]:
                        cands[f"a{a}b{b}c{c}d{d}_{lbl}"]=r3(val)
                except Exception: pass
for k,v in cands.items():
    if abs(v-1.119)<0.01:
        print("MATCH", k, v)
print("Any near-1.119 above? (blank = none)")
# also print the described-error value for the record
def wrongA(x): return (x**3+5)/(3*x**2)
print("described error (x^3+5 full):", r3(wrongA(wrongA(x0))))
print("described error keep x1=1.75:", r3((1.75**3+5)/(3*1.75**2)))
