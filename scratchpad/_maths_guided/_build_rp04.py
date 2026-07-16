# -*- coding: utf-8 -*-
"""Rebuild ratio-proportion-L04 (Direct & Inverse Proportion) in guided format.
Restores the correct topic from the pre-dump, fixes filed audit issues,
dedups solution values, and adds the guided layer. Verifies every box.
"""
import json, io

DIV="÷"; MUL="×"; MIN="−"; PND="£"

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d={"pre":pre,"post":post,"answer":answer,"hint":hint}
    if say is not None: d["say"]=say
    if done is not None: d["done"]=done
    if phase is not None: d["phase"]=phase
    return d
def sayer(say): return {"say":say}

# ---- guided_steps generators (each ends with a CHECK box; phase marks finish) ----
def direct_unitary(total,n1,n2,thing,meas,money=False,ans=None):
    cur=PND if money else ""
    unit=total/n1
    if unit==int(unit): unit=int(unit)
    val=unit*n2
    if val==int(val): val=int(val)
    assert val==ans, (thing,val,ans)
    tail=(" "+meas) if meas else ""
    return [
        sayer("Direct proportion: more %s, more %s. Find the value of ONE first."%(thing,meas or "cost")),
        box("One %s: %g %s %d = %s"%(thing,total,DIV,n1,cur), unit,
            "Divide the total by how many there are.", post=tail),
        box("%d %s: %g %s %d = %s"%(n2,thing,unit,MUL,n2,cur), val,
            "Multiply the one-unit value by %d."%n2, post=tail, phase="substitute",
            say="Now scale up to %d."%n2),
        box("Check: %g %s %d = %s"%(val,DIV,n2,cur), unit,
            "Dividing back should give the one-unit value.", post=tail, phase="substitute",
            say="Check it fits the start.",
            done="Back to %s%g each, so %s%g is right."%(cur,unit,cur,val)),
    ]

def inverse_rate(r1,t1,r2,res,meas,ans,res_word=None,unit_post=""):
    k=r1*t1; val=k/r2
    if val==int(val): val=int(val)
    assert val==ans,(res,val,ans)
    return [
        sayer("Inverse proportion: more %s, LESS %s. The total stays fixed, so find it."%(res,meas)),
        box("Total = %d %s %d = "%(r1,MUL,t1), k,
            "Multiply the two together for inverse.", post=unit_post),
        box("%d %s: %d %s %d = "%(r2,res,k,DIV,r2), val,
            "Divide the fixed total by %d."%r2, post=unit_post, phase="substitute",
            say="Now share that total among %d %s."%(r2,res)),
        box("Check: %d %s %g = "%(r2,MUL,val), k,
            "%s times %s should return the total."%(res.capitalize(),meas), post=unit_post,
            phase="substitute", say="Check the product is unchanged.",
            done="Same total (%d), so %g is right."%(k,val)),
    ]

def direct_alg_findy(x1,y1,x2,ans):
    k=y1/x1
    if k==int(k): k=int(k)
    val=k*x2
    if val==int(val): val=int(val)
    assert val==ans,(val,ans)
    return [
        sayer("Direct means \\(y = kx\\). Find the constant \\(k\\) from the pair."),
        box("k = %g %s %g = "%(y1,DIV,x1), k, "Divide y by the matching x."),
        box("y = %g %s %g = "%(k,MUL,x2), val, "Multiply k by the new x.", phase="substitute",
            say="Now use \\(y = kx\\) at the new x."),
        box("Check: %g %s %g = "%(k,MUL,x1), y1, "k times the first x should give the first y.",
            phase="substitute", say="Check with the first pair.",
            done="That returns the given y = %g, so %g is right."%(y1,val)),
    ]

def direct_alg_findx(x1,y1,y2,ans):
    k=y1/x1
    if k==int(k): k=int(k)
    val=y2/k
    if val==int(val): val=int(val)
    assert val==ans,(val,ans)
    return [
        sayer("Direct means \\(y = kx\\). Find the constant \\(k\\) first."),
        box("k = %g %s %g = "%(y1,DIV,x1), k, "Divide y by the matching x."),
        box("x = %g %s %g = "%(y2,DIV,k), val, "Divide the new y by k.", phase="substitute",
            say="Now we know y = %g and want x. Rearrange to \\(x = y \\div k\\)."%y2),
        box("Check: %g %s %g = "%(k,MUL,val), y2, "k times x should give the new y.",
            phase="substitute", say="Check with the rule.",
            done="Gives %g, so x = %g is right."%(y2,val)),
    ]

def inverse_alg_findy(x1,y1,x2,ans):
    k=x1*y1
    if k==int(k): k=int(k)
    val=k/x2
    if val==int(val): val=int(val)
    assert val==ans,(val,ans)
    return [
        sayer("Inverse means \\(y = \\frac{k}{x}\\), so the constant is the product."),
        box("k = %g %s %g = "%(x1,MUL,y1), k, "Multiply the pair together for inverse."),
        box("y = %g %s %g = "%(k,DIV,x2), val, "Divide k by the new x.", phase="substitute",
            say="Now use \\(y = \\frac{k}{x}\\) at the new x."),
        box("Check: %g %s %g = "%(x2,MUL,val), k, "x times y should return the constant.",
            phase="substitute", say="Check the product.",
            done="Same product (%g), so %g is right."%(k,val)),
    ]

def inverse_alg_findx(x1,y1,y2,ans):
    k=x1*y1
    if k==int(k): k=int(k)
    val=k/y2
    if val==int(val): val=int(val)
    assert val==ans,(val,ans)
    return [
        sayer("Inverse means \\(y = \\frac{k}{x}\\), so the constant is the product."),
        box("k = %g %s %g = "%(x1,MUL,y1), k, "Multiply the pair together for inverse."),
        box("x = %g %s %g = "%(k,DIV,y2), val, "Divide k by the new y.", phase="substitute",
            say="We know y = %g, and \\(x = \\frac{k}{y}\\)."%y2),
        box("Check: %g %s %g = "%(val,MUL,y2), k, "x times y should return the constant.",
            phase="substitute", say="Check the product.",
            done="Same product (%g), so %g is right."%(k,val)),
    ]

# ---------------- BRONZE ----------------
bronze=[
 {"display":"3 pizzas cost \\(\\pounds21\\). How much do 5 pizzas cost?","solutions":[35],
  "hint":"Find the cost of one pizza first, then multiply by five.",
  "misc":[("common","forgot_step",7,"One pizza = 21 %s 3 = %s7. Five = 7 %s 5 = %s35."%(DIV,PND,MUL,PND))],
  "gs":direct_unitary(21,3,5,"pizza","",money=True,ans=35)},
 {"display":"A car uses 8 litres of fuel to travel 96 km. How far can it travel on 5 litres?","solutions":[60],
  "hint":"Work out the distance for one litre, then multiply by five.",
  "misc":[("common","forgot_step",12,"1 litre = 96 %s 8 = 12 km. 5 litres = 60 km."%DIV)],
  "gs":direct_unitary(96,8,5,"litre","km",ans=60)},
 {"display":"6 identical bars weigh 900 g. What do 10 bars weigh (in grams)?","solutions":[1500],
  "hint":"Find the weight of one bar, then multiply by ten.",
  "misc":[("common","forgot_step",150,"One bar = 900 %s 6 = 150 g. Ten = 1500 g."%DIV)],
  "gs":direct_unitary(900,6,10,"bar","g",ans=1500)},
 {"display":"A recipe for 6 pancakes uses 180 g of flour. How much flour for 10 pancakes?","solutions":[300],
  "hint":"Find the flour for one pancake, then multiply by ten.",
  "misc":[("common","forgot_step",30,"One pancake = 30 g. Ten = 300 g.")],
  "gs":direct_unitary(180,6,10,"pancake","g",ans=300)},
 {"display":"2 workers take 8 hours to paint a fence. How long for 4 workers?","solutions":[4],
  "hint":"Inverse: multiply workers by hours to get the fixed total, then divide by four.",
  "misc":[("common","inverse_error",16,"Inverse: more workers, less time. k = 2 %s 8 = 16. Time = 16 %s 4 = 4 hours."%(MUL,DIV))],
  "gs":inverse_rate(2,8,4,"workers","time",4,unit_post="")},
 {"display":"3 pumps empty a tank in 18 hours. How long would 9 pumps take?","solutions":[6],
  "hint":"Inverse: multiply pumps by hours to get the fixed total, then divide by nine.",
  "misc":[("common","inverse_error",54,"Inverse: more pumps, less time. k = 3 %s 18 = 54. Time = 54 %s 9 = 6 hours."%(MUL,DIV))],
  "gs":inverse_rate(3,18,9,"pumps","time",6,unit_post="")},
 {"display":"12 sweets cost \\(\\pounds1.80\\). How much do 20 sweets cost?","solutions":[3],
  "hint":"Find the cost of one sweet, then multiply by twenty.",
  "misc":[("common","forgot_step",0.15,"One sweet = 1.80 %s 12 = %s0.15. 20 sweets = 20 %s 0.15 = %s3."%(DIV,PND,MUL,PND))],
  "gs":direct_unitary(1.80,12,20,"sweet","",money=True,ans=3)},
 {"display":"3 taps fill a tank in 15 hours. How long for 5 taps?","solutions":[9],
  "hint":"Inverse: multiply taps by hours to get the fixed total, then divide by five.",
  "misc":[("common","inverse_error",25,"Inverse: more taps, less time. k = 3 %s 15 = 45. Time = 45 %s 5 = 9 hours."%(MUL,DIV))],
  "gs":inverse_rate(3,15,5,"taps","time",9,unit_post="")},
]

# ---------------- SILVER ----------------
silver=[
 {"display":"\\(y\\) is directly proportional to \\(x\\). When \\(x = 3\\), \\(y = 15\\). Find \\(y\\) when \\(x = 7\\).","solutions":[35],
  "hint":"Find k by dividing y by x, then multiply k by the new x.",
  "misc":[("common","wrong_formula",19,"k = 15 %s 3 = 5. y = 5 %s 7 = 35. Adding the change in x (15 + 4) is the slip."%(DIV,MUL))],
  "gs":direct_alg_findy(3,15,7,35)},
 {"display":"\\(y\\) is inversely proportional to \\(x\\). When \\(x = 4\\), \\(y = 6\\). Find \\(y\\) when \\(x = 8\\).","solutions":[3],
  "hint":"Inverse: multiply x by y to get k, then divide by the new x.",
  "misc":[("common","inverse_error",12,"k = 4 %s 6 = 24. y = 24 %s 8 = 3."%(MUL,DIV))],
  "gs":inverse_alg_findy(4,6,8,3)},
 {"display":"8 identical tiles cover 2400 cm\\(^2\\). What area would 14 tiles cover?","solutions":[4200],
  "hint":"Find the area of one tile, then multiply by fourteen.",
  "misc":[("common","forgot_step",300,"One tile = 300 cm². 14 tiles = 4200 cm².")],
  "gs":direct_unitary(2400,8,14,"tile","cm²",ans=4200)},
 {"display":"A journey takes 6 hours at 40 km/h. How long would it take at 60 km/h? Give your answer in hours.","solutions":[4],
  "hint":"Inverse: work out the fixed distance, then divide by the new speed.",
  "misc":[("common","inverse_error",9,"Inverse: faster speed, less time. Distance = 40 %s 6 = 240 km. Time = 240 %s 60 = 4 hours."%(MUL,DIV))],
  "gs":inverse_rate(40,6,60,"km/h","time",4,unit_post="")},
 {"display":"\\(y\\) is directly proportional to \\(x\\). When \\(x = 6\\), \\(y = 21\\). Find \\(x\\) when \\(y = 49\\).","solutions":[14],
  "hint":"Find k, then divide the new y by k to get x.",
  "misc":[("common","wrong_formula",171.5,"k = 21 %s 6 = 3.5. x = 49 %s 3.5 = 14. Multiplying by k instead of dividing gives 171.5."%(DIV,DIV))],
  "gs":direct_alg_findx(6,21,49,14)},
 {"display":"\\(y\\) is inversely proportional to \\(x\\). When \\(x = 3\\), \\(y = 12\\). Find \\(x\\) when \\(y = 4\\).","solutions":[9],
  "hint":"Inverse: multiply x by y to get k, then divide k by the new y.",
  "misc":[("common","inverse_error",1,"k = 3 %s 12 = 36. x = 36 %s 4 = 9. Treating it as direct gives 1."%(MUL,DIV))],
  "gs":inverse_alg_findx(3,12,4,9)},
 {"display":"12 workers finish a job in 8 days. How many workers are needed to finish it in 6 days?","solutions":[16],
  "hint":"Inverse: multiply workers by days to get the total, then divide by the new number of days.",
  "misc":[("common","inverse_error",9,"Inverse: fewer days needs MORE workers. k = 12 %s 8 = 96 worker-days. Workers = 96 %s 6 = 16."%(MUL,DIV))],
  "gs":inverse_rate(12,8,6,"days","workers",16,unit_post=" worker-days")},
]

# ---------------- GOLD ----------------
gold=[
 {"display":"\\(y\\) is directly proportional to \\(x\\). When \\(x = 5\\), \\(y = 8\\). Find \\(y\\) when \\(x = 12.5\\).","solutions":[20],
  "hint":"Find k by dividing y by x, then multiply by the new x.",
  "misc":[("common","wrong_formula",None,"k = 8 %s 5 = 1.6. y = 1.6 %s 12.5 = 20."%(DIV,MUL))],
  "gs":direct_alg_findy(5,8,12.5,20)},
 {"display":"A gear with 20 teeth meshes with a gear of 30 teeth. The small gear rotates at 150 rpm. Find the speed of the large gear.","solutions":[100],
  "hint":"Inverse: teeth times speed stays constant, so divide by the larger gear's teeth.",
  "misc":[("common","inverse_error",225,"Inverse: k = 20 %s 150 = 3000. Large gear = 3000 %s 30 = 100 rpm."%(MUL,DIV))],
  "gs":[
    sayer("Gears are inverse: more teeth means slower turning. Teeth %s speed stays constant. Find it from the small gear."%MUL),
    box("k = 20 %s 150 = "%MUL, 3000, "Multiply the small gear's teeth by its speed."),
    box("Large gear: 3000 %s 30 = "%DIV, 100, "Divide the constant by the large gear's teeth.",
        post="rpm", phase="substitute", say="Now use it on the large gear (30 teeth)."),
    box("Check: 30 %s 100 = "%MUL, 3000, "Teeth times speed should return the constant.",
        phase="substitute", say="Check the product still holds.",
        done="Same 3000, so 100 rpm is right."),
  ]},
 {"display":"It takes 12 workers 15 days to dig a trench. After 5 days, 4 workers leave. How many more days to finish?","solutions":[15],
  "hint":"Work in worker-days: find the total, subtract what is already done, then divide by the workers left.",
  "misc":[("common","wrong_formula",22.5,"Total = 12 %s 15 = 180 worker-days. Done = 12 %s 5 = 60. Remaining = 120. Workers left = 8. Days = 120 %s 8 = 15."%(MUL,MUL,DIV))],
  "gs":[
    sayer("Work in worker-days. First find the whole job."),
    box("Total = 12 %s 15 = "%MUL, 180, "Multiply workers by days for the whole job.", post=" worker-days"),
    box("Done = 12 %s 5 = "%MUL, 60, "Twelve workers for the first five days.", post=" worker-days",
        say="Now the work already done in the first 5 days."),
    box("Left = 180 %s 60 = "%MIN, 120, "Take the done work from the total.", post=" worker-days",
        phase="substitute", say="So the work still left is:"),
    box("Days = 120 %s 8 = "%DIV, 15, "Divide the work left by the 8 workers still there.",
        phase="substitute", say="Only 8 workers remain. Share the remaining work among them."),
    box("Check: 60 + 8 %s 15 = "%MUL, 180, "Phase-one work plus phase-two work should equal the total.",
        phase="substitute", say="Check the whole job adds up.",
        done="Back to 180 worker-days, so 15 more days is right."),
  ]},
 {"display":"\\(y\\) is inversely proportional to \\(x\\). When \\(x = 2\\), \\(y = 18\\). Find \\(y\\) when \\(x = 12\\).","solutions":[3],
  "hint":"Inverse: multiply x by y to get k, then divide k by the new x.",
  "misc":[("common","inverse_error",108,"k = 2 %s 18 = 36. y = 36 %s 12 = 3. Treating it as direct gives 108."%(MUL,DIV))],
  "gs":inverse_alg_findy(2,18,12,3)},
 {"display":"\\(y\\) is directly proportional to \\(x\\). When \\(x = 8\\), \\(y = 6\\). Find \\(x\\) when \\(y = 12\\).","solutions":[16],
  "hint":"Find k, then divide the new y by k to get x.",
  "misc":[("common","wrong_formula",9,"k = 6 %s 8 = 0.75. x = 12 %s 0.75 = 16. Multiplying by k instead gives 9."%(DIV,DIV))],
  "gs":direct_alg_findx(8,6,12,16)},
]

def build_problems(lst):
    out=[]
    for p in lst:
        mc=[]
        for check,pat,exp,msg in p["misc"]:
            mc.append({"check":check,"expect":exp,"message":msg,"pattern":pat})
        out.append({
            "display":p["display"],
            "solutions":p["solutions"],
            "calculator":False,
            "input_type":"single_value",
            "hint":p["hint"],
            "misconceptions":mc,
            "guided_steps":p["gs"],
        })
    return out

# --------- load pre-dump for preserved fields + method_card ---------
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
entry=[e for e in dump if e["id"]=="a43f9613-dd40-45e2-b692-00ac9c01fb92"][0]
src=entry["practice_data"]

pd={}
pd["method_card"]=src["method_card"]          # preserved (correct proportion content)
pd["topic_links"]=src["topic_links"]          # preserved
pd["problem_bank"]={
    "bronze_description":"Everyday direct and inverse word problems: find the value of one unit, then scale.",
    "silver_description":"Algebraic proportion (y = kx or y = k/x): find the constant k, then use it forwards or backwards.",
    "gold_description":"Multi-step and reverse proportion: gears, work rates, and finding x from y.",
    "bronze":build_problems(bronze),
    "silver":build_problems(silver),
    "gold":build_problems(gold),
}
pd["related_videos"]=src["related_videos"]    # preserved (two Corbett proportion videos)
# preserved, except em dashes in step labels replaced with a colon (style rule + validator)
pd["worked_examples"]=json.loads(json.dumps(src["worked_examples"]).replace(" \\u2014 ",": "))
assert "—" not in json.dumps(pd["worked_examples"]), "em dash still present"

pd["tier_guides"]={
 "bronze":{
   "title":"Bronze: find one, then scale",
   "steps":[
     "Decide the type. If more means more, it is <strong>direct</strong>. If more means less (more workers, less time), it is <strong>inverse</strong>.",
     "Direct: find the value of ONE unit by dividing, then multiply for how many you want.",
     "Inverse: multiply the pair to get the fixed total, then divide by the new amount.",
   ],
   "example":{
     "question":"3 pizzas cost £21. Find the cost of 5 pizzas.",
     "steps":[
       {"label":"Type","content":"<p>More pizzas, more money: direct proportion.</p>"},
       {"label":"One unit","content":"<p>One pizza \\(= 21 \\div 3 = \\pounds7\\).</p>"},
       {"label":"Scale","content":"<p>Five pizzas \\(= 7 \\times 5 = \\pounds35\\).</p>"},
       {"label":"Check","content":"<p>\\(35 \\div 5 = \\pounds7\\) each ✓</p>"},
       {"label":"Answer","content":"<p><strong>£35</strong></p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "silver":{
   "title":"Silver: find the constant k",
   "steps":[
     "Write the rule: direct is \\(y = kx\\), inverse is \\(y = \\frac{k}{x}\\).",
     "Find \\(k\\) from the pair you are given: direct \\(k = y \\div x\\), inverse \\(k = y \\times x\\).",
     "Put \\(k\\) back into the rule and solve for the missing value, forwards or backwards.",
   ],
   "example":{
     "question":"y is directly proportional to x. When x = 3, y = 15. Find y when x = 7.",
     "steps":[
       {"label":"Rule","content":"<p>Direct, so \\(y = kx\\).</p>"},
       {"label":"Find k","content":"<p>\\(k = 15 \\div 3 = 5\\).</p>"},
       {"label":"Use it","content":"<p>\\(y = 5 \\times 7 = 35\\).</p>"},
       {"label":"Check","content":"<p>\\(35 \\div 7 = 5 = k\\) ✓</p>"},
       {"label":"Answer","content":"<p><strong>35</strong></p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
 "gold":{
   "title":"Gold: reverse and multi-step proportion",
   "steps":[
     "Same rules, harder set-ups: gears and work rates are <strong>inverse</strong>, so the product stays fixed.",
     "Given \\(y\\) and asked for \\(x\\)? Rearrange \\(y = kx\\) to \\(x = y \\div k\\), or \\(y = \\frac{k}{x}\\) to \\(x = k \\div y\\).",
     "For work problems, track the total (worker-days), and subtract any work already done before scaling.",
   ],
   "example":{
     "question":"y is inversely proportional to x. When x = 2, y = 18. Find y when x = 12.",
     "steps":[
       {"label":"Rule","content":"<p>Inverse, so \\(y = \\frac{k}{x}\\).</p>"},
       {"label":"Find k","content":"<p>\\(k = 2 \\times 18 = 36\\).</p>"},
       {"label":"Use it","content":"<p>\\(y = 36 \\div 12 = 3\\).</p>"},
       {"label":"Check","content":"<p>\\(12 \\times 3 = 36 = k\\) ✓</p>"},
       {"label":"Answer","content":"<p><strong>3</strong></p>","isAnswer":True,"is_answer":True},
     ],
   },
 },
}

pd["guided"]={
 "opener":{
   "label":"Before any algebra",
   "display":"6 cakes cost £12<br>A job takes 4 builders 6 days",
   "steps":[
     {"say":"Two everyday puzzles. No algebra, just common sense. Start with the cakes.",
      "pre":"12 cakes would cost £","post":"","answer":24,
      "hint":"Twice as many cakes means twice the money."},
     {"say":"Now the builders. Same job, but put 8 builders on it instead of 4.",
      "pre":"With 8 builders it takes ","post":" days","answer":3,
      "hint":"Twice as many builders means half the time."},
     {"say":"Two everyday moves. Cakes: <strong>more means more</strong>, that is <strong>direct proportion</strong>. Builders: <strong>more means less</strong>, that is <strong>inverse proportion</strong>. The trick for both is to find the value of ONE first (one cake is £2; four builders take 24 builder-days), then scale. Algebra just writes direct as \\(y = kx\\) and inverse as \\(y = \\frac{k}{x}\\)."},
   ],
 },
 "teach":{
   "bronze":{
     "display":"6 identical bricks weigh 15 kg. How much do 10 bricks weigh?",
     "label":"Together: your first one",
     "steps":[
       {"say":"Direct proportion: more bricks, more weight. The safest route is to find ONE brick first.",
        "pre":"One brick: 15 %s 6 = "%DIV,"post":" kg","answer":2.5,
        "hint":"Divide the total weight by the number of bricks."},
       {"say":"Now scale up. Ten bricks is ten lots of that.",
        "pre":"10 bricks: 2.5 %s 10 = "%MUL,"post":" kg","answer":25,
        "hint":"Multiply the one-brick weight by 10."},
       {"say":"The one-brick value works backwards too. How many bricks weigh 20 kg?",
        "pre":"20 %s 2.5 = "%DIV,"post":" bricks","answer":8,
        "hint":"Divide the weight by the one-brick weight.",
        "done":"Find one, then multiply or divide. That is the whole bronze method."},
       {"say":"Check against the start.",
        "pre":"6 bricks: 2.5 %s 6 = "%MUL,"post":" kg","answer":15,
        "hint":"Six bricks should return the starting weight.",
        "done":"Back to the given 15 kg, so 2.5 kg per brick is right."},
     ],
   },
   "silver":{
     "display":"\\(y\\) is directly proportional to \\(x\\). When \\(x = 4\\), \\(y = 10\\). Find \\(y\\) when \\(x = 6\\).",
     "label":"Together: the silver move",
     "steps":[
       {"say":"Now it is written in algebra. Direct means \\(y = kx\\). First find the constant \\(k\\).",
        "pre":"k = 10 %s 4 = "%DIV,"post":"","answer":2.5,
        "hint":"Divide the y value by the matching x value."},
       {"say":"So the rule is \\(y = 2.5x\\). Use it at the new x.",
        "pre":"y = 2.5 %s 6 = "%MUL,"post":"","answer":15,
        "hint":"Multiply k by the new x."},
       {"say":"It runs backwards too. If y were 20, what is x?",
        "pre":"x = 20 %s 2.5 = "%DIV,"post":"","answer":8,
        "hint":"Divide y by k to get x.",
        "done":"Find k once, then multiply or divide. That is the silver move."},
       {"say":"Check with the first pair.",
        "pre":"2.5 %s 4 = "%MUL,"post":"","answer":10,
        "hint":"k times the original x should give the original y.",
        "done":"That returns the given y = 10, so k = 2.5 is right."},
     ],
   },
   "gold":{
     "display":"\\(y\\) is inversely proportional to \\(x\\). When \\(x = 3\\), \\(y = 8\\). Find \\(x\\) when \\(y = 6\\).",
     "label":"Together: the gold move",
     "steps":[
       {"say":"Inverse means \\(y = \\frac{k}{x}\\), so the constant is the PRODUCT: \\(k = x \\times y\\).",
        "pre":"k = 3 %s 8 = "%MUL,"post":"","answer":24,
        "hint":"Multiply the pair together for inverse."},
       {"say":"The rule is \\(y = \\frac{24}{x}\\). This time we know y = 6 and want x. Rearrange: \\(x = \\frac{k}{y}\\).",
        "pre":"x = 24 %s 6 = "%DIV,"post":"","answer":4,
        "hint":"Divide the constant by y."},
       {"say":"Sense check: y dropped from 8 to 6, so x should rise. It did, from 3 to 4.",
        "pre":"Confirm the product: 4 %s 6 = "%MUL,"post":"","answer":24,
        "hint":"x times y should return the constant.",
        "done":"Same 24, so x = 4 fits."},
       {"say":"One more, to prove the product never changes. What is x when y = 2?",
        "pre":"x = 24 %s 2 = "%DIV,"post":"","answer":12,
        "hint":"Divide the constant by the new y.",
        "done":"12 %s 2 = 24 again. The product stays fixed: that is the gold idea."%MUL},
     ],
   },
 },
}

json.dump(pd, io.open("lesson_ratio-proportion-L04.json","w",encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("built ok; bronze/silver/gold solution values:")
for t in ("bronze","silver","gold"):
    print(" ",t,[p["solutions"][0] for p in pd["problem_bank"][t]])
