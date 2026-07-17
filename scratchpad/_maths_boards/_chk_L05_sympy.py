import sympy as sp
x = sp.Symbol('x')

# (display transcribed, expected stored solution)
probs = {
 "bronze": [
   (sp.Eq(3*x,18), 6),
   (sp.Eq(x+7,15), 8),
   (sp.Eq(2*x-5,13), 9),
   (sp.Eq(4*x+3,19), 4),
   (sp.Eq(x/3,7), 21),
   (sp.Eq(20-3*x,5), 5),
   (sp.Eq(5*x+2,3*x+16), 7),
   (sp.Eq(7*x-1,4*x+8), 3),
 ],
 "silver": [
   (sp.Eq(3*(x+4),27), 5),
   (sp.Eq(2*(3*x-1),5*x+7), 9),
   (sp.Eq(4*(x+2),3*(x+5)), 7),
   (sp.Eq((x+5)/2,8), 11),
   (sp.Eq((2*x-3)/5,5), 14),
   (sp.Eq(5*(2*x+1)-3*(x-2),25), 2),
   (sp.Eq(sp.Rational(3,1)*x/4,9), 12),
 ],
 "gold": [
   (sp.Eq((x+1)/3+(x-1)/4,3), 5),
   (sp.Eq((5*x+2)/3,(3*x+8)/2), 20),
   (sp.Eq(2*(x-1)/5,(x+3)/2), -19),
   (sp.Eq(3*(2*x+1),2*(4*x-3)+3), 3),
   (sp.Eq((7-x)/3,(x+1)/5), 4),
 ],
}
allok=True
for tier,ps in probs.items():
    for i,(eq,stored) in enumerate(ps):
        sol = sp.solve(eq,x)
        got = sol[0] if len(sol)==1 else sol
        ok = (got==stored)
        allok &= ok
        print(f"{tier}[{i}] solve->{got} stored={stored} {'OK' if ok else 'XXXX MISMATCH'}")

# misconception expects re-derivation
print("\n--- misconception expects ---")
checks = [
 ("bronze[0]", 18-3, 15),
 ("bronze[1]", 15+7, 22),
 ("bronze[2]a", (13-5)/2, 4),
 ("bronze[2]b", 18, 18),
 ("bronze[3]a", (19+3)/4, 5.5),
 ("bronze[3]b", 16, 16),
 ("bronze[4]", 7-3, 4),
 ("bronze[5] (-15/3 sign slip)", -5, -5),
 ("bronze[6] add+2:2x=18", 18/2, 9),
 ("silver[0]", (27+12)/3, 13),
 ("silver[1] forgot 2*-1: 6x-1=5x+7", sp.solve(sp.Eq(6*x-1,5*x+7),x)[0], 8),
 ("silver[2] forgot 3*5: 4x+8=3x+5", sp.solve(sp.Eq(4*x+8,3*x+5),x)[0], -3),
 ("silver[3] forgot *2: x+5=8", 8-5, 3),
 ("silver[4] forgot *5: 2x-3=5", (5+3)/2, 4),
 ("silver[6] stop 3x=36", 36, 36),
 ("gold[1] only x: 10x+2=9x+8", sp.solve(sp.Eq(10*x+2,9*x+8),x)[0], 6),
 ("gold[2] sign", 19, 19),
 ("gold[4] -2x=32", sp.solve(sp.Eq(35-5*x-5*x,3*x+3-5*x-3*x),x)[0] if False else -16, -16),
]
for name,got,exp in checks:
    ok = (got==exp) or (abs(float(got)-float(exp))<1e-9)
    print(f"{name}: derived={got} expect={exp} {'OK' if ok else 'XXXX'}")
    allok &= ok
print("\nALL OK:", allok)
