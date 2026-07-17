# -*- coding: utf-8 -*-
import json, io, math, importlib.util
from fractions import Fraction as F

# reuse walk helpers from _buildL02
spec=importlib.util.spec_from_file_location("b","_buildL02.py")
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

live=json.load(io.open("_live_number-L02.json",encoding="utf-8"))
bank=json.load(io.open("_L02_bank.json",encoding="utf-8"))

SAY=b.SAY; BOX=b.BOX

# -------- opener SVG: 12-square chocolate bar, 3 blue (1/4), 4 amber (1/3) --------
cells=[]
for idx in range(12):
    r,c = divmod(idx,4)
    x=8+c*44; y=8+r*44
    if idx in (0,1,2): fill='fill="#60a5fa" fill-opacity="0.35"'      # quarter = 3 squares
    elif idx in (3,4,5,6): fill='fill="#f59e0b" fill-opacity="0.35"'  # third = 4 squares
    else: fill='fill="none"'
    cells.append(f'<rect x="{x}" y="{y}" width="44" height="44" rx="4" {fill} stroke="currentColor" stroke-width="1.5"/>')
svg=('<svg viewBox="0 0 192 148" role="img" aria-label="A chocolate bar of 12 equal squares: 3 squares shaded blue and 4 squares shaded orange">'
     + "".join(cells)
     + '<text x="96" y="142" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">12 squares in the bar</text></svg>')

opener={
 "label":"Before any fraction rules",
 "display": svg + "<br>A chocolate bar has <strong>12 equal squares</strong>. You eat \\(\\frac{1}{4}\\) of it (the blue squares), then \\(\\frac{1}{3}\\) of it (the orange squares).",
 "steps":[
   BOX(r"\(\frac{1}{4}\) of the 12 squares is ", 3, "12 shared into 4 equal groups.", post=" squares",
       say="No fraction rules yet, just count squares."),
   BOX(r"\(\frac{1}{3}\) of the 12 squares is ", 4, "12 shared into 3 equal groups.", post=" squares"),
   BOX("So altogether you ate 3 + 4 = ", 7, "Add the two amounts of squares.", post=" squares",
       done="7 out of 12 squares."),
   SAY(r"You just found \(\frac{1}{4} + \frac{1}{3} = \frac{7}{12}\) by counting. Why did 12 work so neatly? Because 12 splits evenly into quarters AND thirds. That shared bottom number is the <strong>common denominator</strong>, and it is the whole trick to adding fractions."),
 ],
}

# -------- teach walks (not in bank) --------
teach={
 "bronze":{
   "label":"Together: your first one",
   "display": r"Work out \(\frac{1}{2} + \frac{1}{3}\)",
   "steps": b.addsub_walk(1,2,1,3,"+",5,6),
 },
 "silver":{
   "label":"Together: a mixed-number one",
   "display": r"Work out \(1\frac{1}{2} \times 2\frac{1}{3}\)",
   "steps": b.two_mixed_mult(1,1,2,2,1,3,7,2),
 },
 "gold":{
   "label":"Together: two operations",
   "display": r"Work out \(\frac{3}{4} \div \frac{1}{2} - \frac{1}{2}\)",
   "steps": [
     SAY(r"Two operations. Division comes before subtraction, so do \(\frac{3}{4} \div \frac{1}{2}\) first."),
     BOX(r"Keep, Flip, Change to \(\frac{3}{4} \times \frac{2}{1}\). Multiply the tops: 3 × 2 = ", 6, "3 times 2."),
     BOX("Multiply the bottoms: 4 × 1 = ", 4, "4 times 1."),
     BOX(r"Simplify \(\frac{6}{4}\) by dividing by 2: top = ", 3, "6 ÷ 2, giving three halves."),
     BOX(r"Now subtract \(\frac{1}{2}\). Same bottom 2, so subtract the tops: 3 − 1 = ", 2, "The division gave 3/2."),
     BOX(r"Simplify \(\frac{2}{2}\): top = ", 1, "2 ÷ 2."),
     BOX("bottom = ", 1, "2 ÷ 2.", done=r"\(\frac{2}{2} = 1\). Order of operations settled it."),
     SAY(r"Check: \(\frac{3}{2} - \frac{1}{2} = 1\). Correct."),
   ],
 },
}

# -------- tier_guides --------
tier_guides={
 "bronze":{
   "title":"Bronze: two simple fractions",
   "steps":[
     "To <strong>add or subtract</strong>, the bottoms must match. Find the lowest common denominator, convert both fractions, then work only on the tops.",
     "To <strong>multiply</strong>, go straight across: tops together, bottoms together.",
     "To <strong>divide</strong>, use KFC: Keep the first, Flip the second, Change ÷ to ×. Always simplify at the end.",
   ],
   "example":{
     "question":"Work out 2/3 + 1/6",
     "steps":[
       {"label":"Common bottom","content":r"<p>LCD of 3 and 6 is 6.</p>"},
       {"label":"Convert","content":r"<p>\(\frac{2}{3} = \frac{4}{6}\)</p>"},
       {"label":"Add","content":r"<p>\(\frac{4}{6} + \frac{1}{6} = \frac{5}{6}\)</p>"},
       {"label":"Check","content":r"<p>5 and 6 share no common factor, so it is simplest.</p>"},
       {"label":"Answer","content":r"<p>\(\frac{5}{6}\)</p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "silver":{
   "title":"Silver: mixed numbers",
   "steps":[
     "Turn every <strong>mixed number</strong> into an improper fraction first: whole × bottom + top, over the same bottom.",
     "Then use the bronze moves: common denominator to add or subtract, straight across to multiply, KFC to divide.",
     "Simplify the final fraction, and turn it back into a mixed number if the question used one.",
   ],
   "example":{
     "question":"Work out 2¼ × 1⅓",
     "steps":[
       {"label":"To improper","content":r"<p>\(2\frac{1}{4} = \frac{9}{4}\), \(1\frac{1}{3} = \frac{4}{3}\)</p>"},
       {"label":"Multiply","content":r"<p>\(\frac{9}{4} \times \frac{4}{3} = \frac{36}{12}\)</p>"},
       {"label":"Simplify","content":r"<p>\(\frac{36}{12} = 3\)</p>"},
       {"label":"Check","content":r"<p>About 2 × 1.3 ≈ 3, so 3 is sensible.</p>"},
       {"label":"Answer","content":r"<p>3</p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "gold":{
   "title":"Gold: multi-step order of operations",
   "steps":[
     "With more than one operation, follow <strong>order of operations</strong>: do × and ÷ before + and −, left to right.",
     "Handle each operation with its own rule (common denominator, straight across, or KFC), one step at a time.",
     "Simplify only at the very end, and turn improper fractions into mixed numbers if needed.",
   ],
   "example":{
     "question":"Work out 2/3 ÷ 4/9 + 1/2",
     "steps":[
       {"label":"Divide first","content":r"<p>\(\frac{2}{3} \div \frac{4}{9} = \frac{2}{3} \times \frac{9}{4} = \frac{18}{12} = \frac{3}{2}\)</p>"},
       {"label":"Then add","content":r"<p>\(\frac{3}{2} + \frac{1}{2} = \frac{4}{2}\)</p>"},
       {"label":"Simplify","content":r"<p>\(\frac{4}{2} = 2\)</p>"},
       {"label":"Check","content":r"<p>Division was done before addition, as required.</p>"},
       {"label":"Answer","content":r"<p>2</p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
}

# -------- method_card (slim, <=140 words, <=4 steps) --------
method_card={
 "title":"Working with Fractions",
 "steps":[
   "Add or subtract: use a common denominator, combine the numerators, keep the denominator.",
   "Multiply: tops together, bottoms together, then cancel.",
   "Divide: Keep the first, Flip the second, Change ÷ to × (KFC).",
   "Mixed numbers: change to improper fractions first, and always simplify at the end.",
 ],
 "content":("<p>A <strong>fraction</strong> is a part of a whole: the top (numerator) counts the parts, the bottom "
   "(denominator) says how many equal parts make one whole.</p><p><strong>Add or subtract</strong> only when the "
   "denominators match: find the lowest common denominator, convert both, then work on the numerators. "
   "<strong>Multiply</strong> straight across, cancelling common factors first to keep the numbers small. "
   "<strong>Divide</strong> with KFC: Keep the first fraction, Flip the second, Change ÷ to ×. Turn any "
   "<strong>mixed number</strong> into an improper fraction before you start, and simplify your answer by dividing "
   "top and bottom by their highest common factor.</p>"),
 "example": live["method_card"].get("example"),
}

# -------- assemble: preserve everything else --------
pd={
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites":[]}),
 "problem_bank":{
   "bronze": bank["bronze"], "silver": bank["silver"], "gold": bank["gold"],
   "bronze_description":"Add, subtract, multiply or divide two simple fractions, then simplify to lowest terms.",
   "silver_description":"The same four operations, now with mixed numbers: convert to improper fractions first.",
   "gold_description":"Multi-step calculations: follow order of operations, then simplify the final fraction.",
 },
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", []),
 "tier_guides": tier_guides,
 "guided": {"opener": opener, "teach": teach},
}

json.dump(pd, io.open("lesson_number-L02.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# sanity: teach walks land, tier examples arithmetic, word budgets
def wc(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot=sum(wc(s) for s in tier_guides[t]["steps"])
    print(f"tier_guides.{t} steps words={tot} (<=115)")
mc_words=wc(method_card["content"])
print("method_card.content words=",mc_words,"(<=140), steps=",len(method_card["steps"]))
for t in ("bronze","silver","gold"):
    nb=len([s for s in teach[t]["steps"] if s.get("answer") is not None])
    print(f"teach.{t} boxes={nb} (>=4)")
print("preserved worked_examples:", len(pd["worked_examples"]), " topic_links:", pd["topic_links"])
print("WROTE lesson_number-L02.json")
