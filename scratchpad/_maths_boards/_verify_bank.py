import sympy as sp
x,y=sp.symbols('x y')
# (display target expr, correct factor form) fresh solve check
checks=[
 ("gold","4*x**2-25","(2*x+5)*(2*x-5)"),
 ("gold","x**2-10*x+25","(x-5)**2"),
 ("gold","3*x**2-12","3*(x+2)*(x-2)"),
 ("gold","x**2-6*x+9-y**2","(x-3+y)*(x-3-y)"),
 ("gold","2*x**3-18*x","2*x*(x+3)*(x-3)"),
 ("bronze","3*x+9","3*(x+3)"),
 ("bronze","8*x-12","4*(2*x-3)"),
 ("bronze","5*x**2+15*x","5*x*(x+3)"),
 ("bronze","6*x*y+9*y","3*y*(2*x+3)"),
 ("bronze","x**2+5*x","x*(x+5)"),
 ("bronze","12*x**2-8*x","4*x*(3*x-2)"),
 ("bronze","x**2-4","(x+2)*(x-2)"),
 ("bronze","x**2-16","(x+4)*(x-4)"),
 ("silver","x**2+7*x+12","(x+3)*(x+4)"),
 ("silver","x**2-5*x+6","(x-2)*(x-3)"),
 ("silver","x**2+2*x-15","(x+5)*(x-3)"),
 ("silver","x**2-x-20","(x-5)*(x+4)"),
 ("silver","x**2-81","(x+9)*(x-9)"),
 ("silver","x**2+3*x-28","(x+7)*(x-4)"),
 ("silver","2*x**2+10*x+12","2*(x+2)*(x+3)"),
]
allok=True
for t,d,f in checks:
    ok=sp.expand(sp.sympify(d)-sp.sympify(f))==0
    allok&=ok
    if not ok: print("MISMATCH",t,d,f)
print("all correct-answer forms verify:",allok)
# incomplete-distractor equal-value check (these are intentional distractors, equal but not full)
dist=[("8x-12 opt1","2*(4*x-6)","8*x-12"),("3x^2-12 opt1","3*(x**2-4)","3*x**2-12"),
      ("3x^2-12 opt2","(3*x+6)*(x-2)","3*x**2-12"),("2x^3-18x opt1","2*x*(x**2-9)","2*x**3-18*x"),
      ("2x^2+10x+12 opt1","(2*x+4)*(x+3)","2*x**2+10*x+12"),("2x^2+10x+12 opt3","(x+2)*(2*x+6)","2*x**2+10*x+12")]
for n,a,b in dist:
    print("dist equal(incomplete):",n, sp.expand(sp.sympify(a)-sp.sympify(b))==0)
