# -*- coding: utf-8 -*-
import json, io, math
from fractions import Fraction as F

def lcm(a,b): return a*b//math.gcd(a,b)
def simp(n,d):
    g=math.gcd(n,d); return n//g, d//g
def improper(w,n,d): return w*d+n

def SAY(s): return {"say": s}
def BOX(pre, ans, hint, post="", say=None, done=None, phase=None):
    st={"pre":pre, "answer":ans, "hint":hint, "post":post}
    if say is not None: st["say"]=say
    if done is not None: st["done"]=done
    if phase is not None: st["phase"]=phase
    return st

def addsub_walk(a,b,c,d,op,sn,sd):
    L=lcm(b,d); n1=a*(L//b); n2=c*(L//d)
    comb = n1+n2 if op=="+" else n1-n2
    fn,fd = simp(comb,L); assert [fn,fd]==[sn,sd]
    opw = "add" if op=="+" else "subtract"; opsym = "+" if op=="+" else "−"
    steps=[
      SAY("Add and subtract fractions only when the bottoms match. First make them match."),
      BOX(f"The lowest common denominator of {b} and {d} is ", L, f"The smallest number both {b} and {d} divide into."),
      BOX(f"Rewrite \\(\\frac{{{a}}}{{{b}}}\\) over {L}. Its new top is ", n1, f"{a} × {L//b}."),
      BOX(f"Rewrite \\(\\frac{{{c}}}{{{d}}}\\) over {L}. Its new top is ", n2, f"{c} × {L//d}."),
      BOX(f"Now {opw} the tops over {L}: {n1} {opsym} {n2} = ", comb,
          f"Keep the bottom as {L}; only the tops change.", phase="substitute",
          say=f"Bottoms match, so {opw} only the numerators."),
    ]
    if [comb,L]!=[fn,fd]:
        g=math.gcd(comb,L)
        steps.append(BOX(f"Simplify \\(\\frac{{{comb}}}{{{L}}}\\) by dividing top and bottom by {g}. The top becomes ", fn, f"{comb} ÷ {g}."))
        steps.append(BOX("and the bottom becomes ", fd, f"{L} ÷ {g}.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX(f"\\(\\frac{{{comb}}}{{{L}}}\\) is already in lowest terms. The final top is ", fn, f"{fn} and {fd} share no common factor."))
        steps.append(BOX("and the final bottom is ", fd, "It stays the same.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Quick check: \\(\\frac{{{fn}}}{{{fd}}}\\) is the answer, in lowest terms."))
    return steps

def mult_walk(a,b,c,d,sn,sd, intro=None):
    top=a*c; bot=b*d; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    steps=[ SAY(intro or "Multiply straight across: tops together, bottoms together.") ]
    steps.append(BOX(f"Multiply the tops: {a} × {c} = ", top, f"{a} times {c}."))
    steps.append(BOX(f"Multiply the bottoms: {b} × {d} = ", bot, f"{b} times {d}."))
    if [top,bot]!=[fn,fd]:
        g=math.gcd(top,bot)
        steps.append(BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}. The top becomes ", fn, f"{top} ÷ {g}.", phase="substitute", say="Now cancel down to lowest terms."))
        steps.append(BOX("and the bottom becomes ", fd, f"{bot} ÷ {g}.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX(f"\\(\\frac{{{top}}}{{{bot}}}\\) is already simplest. Final top is ", fn, "No common factor.", phase="substitute", say="Check it is in lowest terms."))
        steps.append(BOX("and the final bottom is ", fd, "It stays the same.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\), in lowest terms."))
    return steps

def div_walk(a,b,c,d,sn,sd):
    top=a*d; bot=b*c; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    steps=[ SAY(f"To divide, use Keep, Flip, Change: \\(\\frac{{{a}}}{{{b}}} \\div \\frac{{{c}}}{{{d}}}\\) becomes \\(\\frac{{{a}}}{{{b}}} \\times \\frac{{{d}}}{{{c}}}\\).") ]
    steps.append(BOX(f"Multiply the tops: {a} × {d} = ", top, f"{a} times {d}."))
    steps.append(BOX(f"Multiply the bottoms: {b} × {c} = ", bot, f"{b} times {c}."))
    if [top,bot]!=[fn,fd]:
        g=math.gcd(top,bot)
        steps.append(BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}. Top becomes ", fn, f"{top} ÷ {g}.", phase="substitute", say="Now cancel to lowest terms."))
        steps.append(BOX("and the bottom becomes ", fd, f"{bot} ÷ {g}.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX(f"\\(\\frac{{{top}}}{{{bot}}}\\) is already simplest. Final top is ", fn, "No common factor.", phase="substitute", say="Check lowest terms."))
        steps.append(BOX("and the bottom is ", fd, "It stays.", done=f"So the answer is \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    return steps

def mixed_addsub_walk(w1,n1,d1,w2,n2,d2,op,sn,sd):
    A=improper(w1,n1,d1); B=improper(w2,n2,d2)
    L=lcm(d1,d2); c1=A*(L//d1); c2=B*(L//d2)
    comb=c1+c2 if op=="+" else c1-c2; fn,fd=simp(comb,L); assert [fn,fd]==[sn,sd]
    opw="add" if op=="+" else "subtract"; opsym="+" if op=="+" else "−"
    steps=[
      SAY("Turn the mixed numbers into improper fractions first."),
      BOX(f"\\({w1}\\tfrac{{{n1}}}{{{d1}}}\\) as an improper fraction: top = {w1} × {d1} + {n1} = ", A, f"{w1}×{d1} then + {n1}."),
      BOX(f"\\({w2}\\tfrac{{{n2}}}{{{d2}}}\\): top = {w2} × {d2} + {n2} = ", B, f"{w2}×{d2} then + {n2}."),
      BOX(f"The LCD of {d1} and {d2} is ", L, f"Smallest number both {d1} and {d2} divide into."),
      BOX(f"\\(\\frac{{{A}}}{{{d1}}}\\) over {L}: top = ", c1, f"{A} × {L//d1}."),
      BOX(f"\\(\\frac{{{B}}}{{{d2}}}\\) over {L}: top = ", c2, f"{B} × {L//d2}."),
      BOX(f"{opw.capitalize()} the tops over {L}: {c1} {opsym} {c2} = ", comb, f"Keep the bottom {L}.", phase="substitute", say=f"Bottoms match, so {opw} the tops."),
    ]
    if [comb,L]!=[fn,fd]:
        g=math.gcd(comb,L)
        steps.append(BOX(f"Simplify by dividing by {g}: top = ", fn, f"{comb} ÷ {g}."))
        steps.append(BOX("bottom = ", fd, f"{L} ÷ {g}.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX("Already simplest, so the final top is ", fn, "No common factor."))
        steps.append(BOX("and the final bottom is ", fd, "It stays.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\) fits the whole-number parts."))
    return steps

def mixed_mult_walk(w,n,d,c,e,sn,sd):
    A=improper(w,n,d); top=A*c; bot=d*e; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    steps=[
      SAY(f"Change \\({w}\\tfrac{{{n}}}{{{d}}}\\) to an improper fraction, then multiply."),
      BOX(f"\\({w}\\tfrac{{{n}}}{{{d}}}\\): top = {w} × {d} + {n} = ", A, f"{w}×{d} then + {n}."),
      BOX(f"Multiply the tops: {A} × {c} = ", top, f"{A} times {c}."),
      BOX(f"Multiply the bottoms: {d} × {e} = ", bot, f"{d} times {e}."),
    ]
    if [top,bot]!=[fn,fd]:
        g=math.gcd(top,bot)
        steps.append(BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}: top = ", fn, f"{top} ÷ {g}.", phase="substitute", say="Cancel to lowest terms."))
        steps.append(BOX("bottom = ", fd, f"{bot} ÷ {g}.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX("Already simplest, final top = ", fn, "No common factor.", phase="substitute", say="Check lowest terms."))
        steps.append(BOX("final bottom = ", fd, "Stays.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    return steps

def mixed_div_walk(w,n,d,c,e,sn,sd):
    A=improper(w,n,d); top=A*e; bot=d*c; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    steps=[
      SAY(f"Change \\({w}\\tfrac{{{n}}}{{{d}}}\\) to \\(\\frac{{{A}}}{{{d}}}\\), then Keep, Flip, Change: \\(\\times \\frac{{{e}}}{{{c}}}\\)."),
      BOX(f"\\({w}\\tfrac{{{n}}}{{{d}}}\\): top = {w} × {d} + {n} = ", A, f"{w}×{d} then + {n}."),
      BOX(f"Multiply the tops: {A} × {e} = ", top, f"{A} times {e}."),
      BOX(f"Multiply the bottoms: {d} × {c} = ", bot, f"{d} times {c}."),
    ]
    if [top,bot]!=[fn,fd]:
        g=math.gcd(top,bot)
        steps.append(BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}: top = ", fn, f"{top} ÷ {g}.", phase="substitute", say="Cancel down."))
        steps.append(BOX("bottom = ", fd, f"{bot} ÷ {g}.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    else:
        steps.append(BOX("Already simplest, final top = ", fn, "No common factor.", phase="substitute", say="Check."))
        steps.append(BOX("final bottom = ", fd, "Stays.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    steps.append(SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\), a whole number as expected." if fd==1 else f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\)."))
    return steps

def two_mixed_mult(w1,n1,d1,w2,n2,d2,sn,sd):
    A=improper(w1,n1,d1); B=improper(w2,n2,d2); top=A*B; bot=d1*d2; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    g=math.gcd(top,bot)
    return [
      SAY("Change both mixed numbers to improper fractions, then multiply."),
      BOX(f"\\({w1}\\tfrac{{{n1}}}{{{d1}}}\\): top = {w1} × {d1} + {n1} = ", A, f"{w1}×{d1} then + {n1}."),
      BOX(f"\\({w2}\\tfrac{{{n2}}}{{{d2}}}\\): top = {w2} × {d2} + {n2} = ", B, f"{w2}×{d2} then + {n2}."),
      BOX(f"Multiply the tops: {A} × {B} = ", top, f"{A} times {B}."),
      BOX(f"Multiply the bottoms: {d1} × {d2} = ", bot, f"{d1} times {d2}."),
      BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}: top = ", fn, f"{top} ÷ {g}.", phase="substitute", say="Cancel to lowest terms."),
      BOX("bottom = ", fd, f"{bot} ÷ {g}.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."),
      SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\)."),
    ]

def two_mixed_div(w1,n1,d1,w2,n2,d2,sn,sd):
    A=improper(w1,n1,d1); B=improper(w2,n2,d2); top=A*d2; bot=d1*B; fn,fd=simp(top,bot); assert [fn,fd]==[sn,sd]
    g=math.gcd(top,bot)
    return [
      SAY(f"Change both to improper fractions, then Keep, Flip, Change: \\(\\frac{{{A}}}{{{d1}}} \\times \\frac{{{d2}}}{{{B}}}\\)."),
      BOX(f"\\({w1}\\tfrac{{{n1}}}{{{d1}}}\\): top = {w1} × {d1} + {n1} = ", A, f"{w1}×{d1} then + {n1}."),
      BOX(f"\\({w2}\\tfrac{{{n2}}}{{{d2}}}\\): top = {w2} × {d2} + {n2} = ", B, f"{w2}×{d2} then + {n2}."),
      BOX(f"Multiply the tops: {A} × {d2} = ", top, f"{A} times {d2}."),
      BOX(f"Multiply the bottoms: {d1} × {B} = ", bot, f"{d1} times {B}."),
      BOX(f"Simplify \\(\\frac{{{top}}}{{{bot}}}\\) by dividing by {g}: top = ", fn, f"{top} ÷ {g}.", phase="substitute", say="Cancel down."),
      BOX("bottom = ", fd, f"{bot} ÷ {g}.", done=f"Answer \\(\\frac{{{fn}}}{{{fd}}}\\)."),
      SAY(f"Check: \\(\\frac{{{fn}}}{{{fd}}}\\), a whole number as expected."),
    ]

def three_term_walk():
    L=12; t1=8;t2=9;t3=2; comb=t1+t2-t3; fn,fd=simp(comb,L); assert [fn,fd]==[5,4]; g=math.gcd(comb,L)
    return [
      SAY("Three fractions: put them all over one common bottom."),
      BOX("The LCD of 3, 4 and 6 is ", 12, "Smallest number 3, 4 and 6 all divide into."),
      BOX(r"\(\frac{2}{3}\) over 12: top = ", 8, "2 × 4."),
      BOX(r"\(\frac{3}{4}\) over 12: top = ", 9, "3 × 3."),
      BOX(r"\(\frac{1}{6}\) over 12: top = ", 2, "1 × 2."),
      BOX("Combine the tops over 12: 8 + 9 − 2 = ", comb, "Work left to right.", phase="substitute", say="Bottoms match, so combine the tops."),
      BOX(f"Simplify \\(\\frac{{{comb}}}{{12}}\\) by dividing by {g}: top = ", fn, f"{comb} ÷ {g}."),
      BOX("bottom = ", fd, f"12 ÷ {g}.", done=r"Answer \(\frac{5}{4}\), i.e. \(1\tfrac{1}{4}\)."),
      SAY(r"Check: \(\frac{5}{4}\) is just over 1, which fits the sum."),
    ]

def g4_walk():
    return [
      SAY(r"Order of operations: division before addition. First do \(\frac{5}{6} \div \frac{2}{3}\)."),
      BOX(r"Flip and multiply the tops: 5 × 3 = ", 15, "5 times 3."),
      BOX("Multiply the bottoms: 6 × 2 = ", 12, "6 times 2."),
      BOX(r"Simplify \(\frac{15}{12}\) by dividing by 3: top = ", 5, "15 ÷ 3, giving fifths over four."),
      BOX(r"Now add \(\frac{1}{4}\). Same bottom 4, so add the tops: 5 + 1 = ", 6, "The division gave 5/4; add the 1/4.", phase="substitute", say=r"That division gave \(\frac{5}{4}\). Now add \(\frac{1}{4}\)."),
      BOX(r"Simplify \(\frac{6}{4}\) by dividing by 2: top = ", 3, "6 ÷ 2."),
      BOX("bottom = ", 2, "4 ÷ 2.", done=r"Answer \(\frac{3}{2}\), i.e. \(1\tfrac{1}{2}\)."),
      SAY(r"Check: \(\frac{3}{2}\) is 1.5, which fits \(\frac{5}{4}+\frac{1}{4}\)."),
    ]

def g5_walk():
    return [
      SAY(r"Work left to right. First \(\frac{3}{7} \times \frac{14}{9}\)."),
      BOX("Multiply the tops: 3 × 14 = ", 42, "3 times 14."),
      BOX("Multiply the bottoms: 7 × 9 = ", 63, "7 times 9."),
      BOX(r"Simplify \(\frac{42}{63}\) by dividing by 21: top = ", 2, "42 ÷ 21, giving two thirds."),
      BOX(r"Now divide by \(\frac{2}{3}\): flip and multiply the tops, 2 × 3 = ", 6, "That product is 2/3; divide it by 2/3.", phase="substitute", say=r"So far \(\frac{2}{3}\). Divide by \(\frac{2}{3}\): Keep, Flip, Change to \(\times \frac{3}{2}\)."),
      BOX("Multiply the bottoms: 3 × 2 = ", 6, "3 times 2."),
      BOX(r"Simplify \(\frac{6}{6}\): top = ", 1, "6 ÷ 6."),
      BOX("bottom = ", 1, "6 ÷ 6.", done=r"Answer 1. Any fraction divided by itself is 1."),
      SAY(r"Check: \(\frac{2}{3} \div \frac{2}{3} = 1\). Correct."),
    ]

def prob(display, sols, hint, misc, steps):
    return {"display":display, "solutions":sols, "calculator":False,
            "input_type":"fraction", "hint":hint, "misconceptions":misc, "guided_steps":steps}
def MC(pattern, message, expect): return {"pattern":pattern, "message":message, "expect":expect}

bronze=[
 prob(r"\(\frac{1}{4} + \frac{1}{3}\)", [7,12], "The LCD of 4 and 3 is 12; convert both, then add the numerators.",
   [MC("add_denominators","Do not add the bottoms. Use LCD 12: \\(\\frac{3}{12} + \\frac{4}{12} = \\frac{7}{12}\\). Adding tops and bottoms gives \\(\\frac{2}{7}\\), which is wrong.",[2,7])],
   addsub_walk(1,4,1,3,"+",7,12)),
 prob(r"\(\frac{3}{5} + \frac{1}{10}\)", [7,10], "The LCD is 10; write 3/5 as tenths first.",
   [MC("add_denominators","Do not add the bottoms. Use LCD 10: \\(\\frac{6}{10} + \\frac{1}{10} = \\frac{7}{10}\\). Adding tops and bottoms gives \\(\\frac{4}{15}\\).",[4,15])],
   addsub_walk(3,5,1,10,"+",7,10)),
 prob(r"\(\frac{5}{6} - \frac{1}{3}\)", [1,2], "Use denominator 6 for both, subtract the tops, then simplify.",
   [MC("subtract_denominators","Do not subtract the bottoms. Use LCD 6: \\(\\frac{5}{6} - \\frac{2}{6} = \\frac{3}{6} = \\frac{1}{2}\\). Subtracting tops and bottoms gives \\(\\frac{4}{3}\\).",[4,3]),
    MC("no_simplify","\\(\\frac{3}{6}\\) is correct but not simplified. Divide top and bottom by 3 to get \\(\\frac{1}{2}\\).",[3,6])],
   addsub_walk(5,6,1,3,"-",1,2)),
 prob(r"\(\frac{7}{8} - \frac{1}{4}\)", [5,8], "Convert 1/4 to eighths, then subtract the numerators.",
   [MC("subtract_denominators","Do not subtract the bottoms. Use LCD 8: \\(\\frac{7}{8} - \\frac{2}{8} = \\frac{5}{8}\\). Subtracting tops and bottoms gives \\(\\frac{6}{4}\\).",[6,4])],
   addsub_walk(7,8,1,4,"-",5,8)),
 prob(r"\(\frac{2}{3} \times \frac{3}{5}\)", [2,5], "Multiply the tops, multiply the bottoms, then simplify.",
   [MC("no_simplify","\\(\\frac{6}{15}\\) is correct but not simplified. Divide top and bottom by 3 to get \\(\\frac{2}{5}\\).",[6,15])],
   mult_walk(2,3,3,5,2,5)),
 prob(r"\(\frac{1}{2} \times \frac{4}{7}\)", [2,7], "Multiply straight across, then cancel the common factor of 2.",
   [MC("no_simplify","\\(\\frac{4}{14}\\) is correct but not simplified. Divide top and bottom by 2 to get \\(\\frac{2}{7}\\).",[4,14])],
   mult_walk(1,2,4,7,2,7)),
 prob(r"\(\frac{3}{4} \div \frac{1}{2}\)", [3,2], "Keep the first, flip 1/2 to 2/1, then multiply.",
   [MC("no_flip","To divide, flip the second fraction: \\(\\frac{3}{4} \\times \\frac{2}{1} = \\frac{6}{4} = \\frac{3}{2}\\). Multiplying without flipping gives \\(\\frac{3}{8}\\).",[3,8]),
    MC("no_simplify","\\(\\frac{6}{4}\\) is correct but not simplified. Divide by 2 to get \\(\\frac{3}{2}\\).",[6,4])],
   div_walk(3,4,1,2,3,2)),
 prob(r"\(\frac{2}{5} \div \frac{3}{5}\)", [2,3], "Flip 3/5 to 5/3, multiply, then simplify.",
   [MC("no_flip","To divide, flip the second: \\(\\frac{2}{5} \\times \\frac{5}{3} = \\frac{10}{15} = \\frac{2}{3}\\). Multiplying without flipping gives \\(\\frac{6}{25}\\).",[6,25]),
    MC("no_simplify","\\(\\frac{10}{15}\\) is correct but not simplified. Divide by 5 to get \\(\\frac{2}{3}\\).",[10,15])],
   div_walk(2,5,3,5,2,3)),
]

silver=[
 prob(r"\(\frac{2}{3} + \frac{5}{8}\)", [31,24], "The LCD of 3 and 8 is 24; convert both, then add the numerators.",
   [MC("add_denominators","Do not add the bottoms. Use LCD 24: \\(\\frac{16}{24} + \\frac{15}{24} = \\frac{31}{24}\\). Adding tops and bottoms gives \\(\\frac{7}{11}\\).",[7,11])],
   addsub_walk(2,3,5,8,"+",31,24)),
 prob(r"\(\frac{5}{6} - \frac{3}{8}\)", [11,24], "The LCD of 6 and 8 is 24; convert both, then subtract.",
   [MC("no_scale_numerators","Multiplying the bottoms gives 48, but scale the tops too: \\(\\frac{40}{48} - \\frac{18}{48} = \\frac{22}{48} = \\frac{11}{24}\\). Leaving the tops unchanged gives \\(\\frac{1}{24}\\).",[1,24])],
   addsub_walk(5,6,3,8,"-",11,24)),
 prob(r"\(1\frac{1}{3} + 2\frac{1}{4}\)", [43,12], "Convert to 4/3 and 9/4, then add using LCD 12.",
   [MC("add_improper_both","Convert then use a common denominator: \\(\\frac{4}{3} + \\frac{9}{4} = \\frac{16}{12} + \\frac{27}{12} = \\frac{43}{12}\\). Adding tops and bottoms of the improper fractions gives \\(\\frac{13}{7}\\).",[13,7])],
   mixed_addsub_walk(1,1,3,2,1,4,"+",43,12)),
 prob(r"\(3\frac{1}{2} - 1\frac{2}{3}\)", [11,6], "Convert to 7/2 and 5/3, use denominator 6, then subtract.",
   [MC("split_no_borrow","You cannot subtract the parts as \\(\\frac{2}{3} - \\frac{1}{2}\\). Convert first: \\(\\frac{7}{2} - \\frac{5}{3} = \\frac{21}{6} - \\frac{10}{6} = \\frac{11}{6}\\). Splitting wholes and parts gives \\(2\\frac{1}{6} = \\frac{13}{6}\\), too big.",[13,6])],
   mixed_addsub_walk(3,1,2,1,2,3,"-",11,6)),
 prob(r"\(\frac{3}{4} \times \frac{8}{9}\)", [2,3], "Cancel first (3 with 9, 4 with 8), or multiply across then simplify.",
   [MC("no_simplify","\\(\\frac{24}{36}\\) is correct but not simplified. Divide top and bottom by 12 to get \\(\\frac{2}{3}\\).",[24,36])],
   mult_walk(3,4,8,9,2,3)),
 prob(r"\(2\frac{1}{5} \times \frac{5}{11}\)", [1,1], "Turn 2 1/5 into 11/5 first, then multiply and cancel.",
   [MC("whole_only","Convert first: \\(2\\frac{1}{5} = \\frac{11}{5}\\), so \\(\\frac{11}{5} \\times \\frac{5}{11} = 1\\). Multiplying only the whole number gives \\(\\frac{10}{11}\\).",[10,11])],
   mixed_mult_walk(2,1,5,5,11,1,1)),
 prob(r"\(1\frac{3}{4} \div \frac{7}{8}\)", [2,1], "Convert 1 3/4 to 7/4, flip 7/8 to 8/7, then multiply.",
   [MC("no_flip","Flip the second fraction: \\(\\frac{7}{4} \\times \\frac{8}{7} = \\frac{56}{28} = 2\\). Multiplying without flipping gives \\(\\frac{49}{32}\\).",[49,32]),
    MC("no_convert","Convert 1 3/4 to 7/4 first. Using 3/4 by mistake gives \\(\\frac{6}{7}\\).",[6,7])],
   mixed_div_walk(1,3,4,7,8,2,1)),
]

gold=[
 prob(r"\(\frac{2}{3} + \frac{3}{4} - \frac{1}{6}\)", [5,4], "Convert all three to twelfths, combine the numerators, then simplify.",
   [MC("combine_across","Use LCD 12: \\(\\frac{8}{12} + \\frac{9}{12} - \\frac{2}{12} = \\frac{15}{12} = \\frac{5}{4}\\). Combining tops and bottoms directly gives \\(\\frac{4}{1}\\).",[4,1]),
    MC("no_simplify","\\(\\frac{15}{12}\\) is correct but not simplified. Divide by 3 to get \\(\\frac{5}{4}\\).",[15,12])],
   three_term_walk()),
 prob(r"\(2\frac{2}{3} \times 1\frac{1}{4}\)", [10,3], "Convert to 8/3 and 5/4, multiply across, then simplify.",
   [MC("whole_and_part","Convert first: \\(\\frac{8}{3} \\times \\frac{5}{4} = \\frac{40}{12} = \\frac{10}{3}\\). Multiplying wholes and parts separately gives \\(\\frac{13}{6}\\).",[13,6]),
    MC("no_simplify","\\(\\frac{40}{12}\\) is correct but not simplified. Divide by 4 to get \\(\\frac{10}{3}\\).",[40,12])],
   two_mixed_mult(2,2,3,1,1,4,10,3)),
 prob(r"\(4\frac{1}{5} \div 1\frac{2}{5}\)", [3,1], "Convert to 21/5 and 7/5, flip the second, then multiply.",
   [MC("no_flip","Flip the second fraction: \\(\\frac{21}{5} \\times \\frac{5}{7} = 3\\). Multiplying without flipping gives \\(\\frac{147}{25}\\).",[147,25])],
   two_mixed_div(4,1,5,1,2,5,3,1)),
 prob(r"\(\frac{5}{6} \div \frac{2}{3} + \frac{1}{4}\)", [3,2], "Do the division first (÷ before +): 5/6 ÷ 2/3, then add 1/4.",
   [MC("order_error","Division comes before addition. Do \\(\\frac{5}{6} \\div \\frac{2}{3} = \\frac{5}{4}\\) first, then + \\(\\frac{1}{4} = \\frac{3}{2}\\). Adding \\(\\frac{2}{3} + \\frac{1}{4}\\) first gives \\(\\frac{10}{11}\\).",[10,11])],
   g4_walk()),
 prob(r"\(\frac{3}{7} \times \frac{14}{9} \div \frac{2}{3}\)", [1,1], "Work left to right: multiply 3/7 × 14/9 first (cancels to 2/3), then divide by 2/3.",
   [MC("no_flip","The last step is a division: \\(\\frac{2}{3} \\div \\frac{2}{3} = \\frac{2}{3} \\times \\frac{3}{2} = 1\\). Multiplying without flipping gives \\(\\frac{4}{9}\\).",[4,9])],
   g5_walk()),
]

data={"bronze":bronze,"silver":silver,"gold":gold}
json.dump(data, io.open("_L02_bank.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

def last2(steps):
    b=[s["answer"] for s in steps if s.get("answer") is not None]; return [b[-2],b[-1]]
ok=True
for tier,ps in data.items():
    for i,p in enumerate(ps):
        l=last2(p["guided_steps"]); land=(l==p["solutions"])
        nb=len([s for s in p['guided_steps'] if s.get('answer') is not None])
        if not land: ok=False
        print(f"{tier}[{i}] sol{p['solutions']} last{l} boxes={nb} {'OK' if land else 'FAIL'}")
print("ALL WALKS LAND ON SOLUTIONS" if ok else "LANDING FAILURE")
