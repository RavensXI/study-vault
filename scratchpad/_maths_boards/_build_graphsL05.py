# -*- coding: utf-8 -*-
import json

live = json.load(open("_live_graphsL05.json", encoding="utf-8"))

# ---------- programmatic figures ----------
def svg_exponential():
    # bacteria doubling: (hours x, count y) = (0,1),(1,2),(2,4),(3,8),(4,16),(5,32)
    pts = [(0,1),(1,2),(2,4),(3,8),(4,16),(5,32)]
    def px(x): return 40 + x/5.0*195
    def py(y): return 165 - y/32.0*150
    parts = ['<svg viewBox="0 0 260 200" role="img" aria-label="Exponential curve of bacteria count against hours: 1 at hour 0, doubling to 2, 4, 8, 16 and 32 by hour 5" style="max-width:260px" font-family="Inter, sans-serif">']
    # axes
    parts.append('<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    # y ticks
    for yv in [0,8,16,24,32]:
        yy = py(yv)
        parts.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (yy,yy))
        parts.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%d</text>' % (yy+3, yv))
    # x ticks
    for xv in range(0,6):
        xx = px(xv)
        parts.append('<line x1="%.1f" y1="165" x2="%.1f" y2="168" stroke="currentColor" stroke-width="1"/>' % (xx,xx))
        parts.append('<text x="%.1f" y="178" font-size="9" fill="currentColor" text-anchor="middle">%d</text>' % (xx, xv))
    # axis titles
    parts.append('<text x="137" y="193" font-size="9" fill="currentColor" text-anchor="middle">hours (x)</text>')
    parts.append('<text x="12" y="90" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">count (y)</text>')
    # curve
    poly = " ".join("%.1f,%.1f" % (px(x),py(y)) for x,y in pts)
    parts.append('<polyline points="%s" fill="none" stroke="#f59e0b" stroke-width="2"/>' % poly)
    for x,y in pts:
        parts.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#f59e0b"/>' % (px(x),py(y)))
    parts.append('</svg>')
    return "".join(parts)

def chart_reciprocal_shift():
    # y = 1/x + 2 ; two branches + asymptote y=2
    pos_x = [0.2,0.25,0.3,0.4,0.5,0.7,1,1.5,2,3,4,5]
    neg_x = [-0.2,-0.25,-0.3,-0.4,-0.5,-0.7,-1,-1.5,-2,-3,-4,-5]
    pos = [{"x":round(x,3),"y":round(1.0/x+2,3)} for x in pos_x]
    neg = [{"x":round(x,3),"y":round(1.0/x+2,3)} for x in neg_x]
    asy = [{"x":-5,"y":2},{"x":5,"y":2}]
    return {"type":"scatter","data":{"datasets":[
        {"type":"line","data":pos,"tension":0.35,"fill":False,"borderColor":"#3b82f6","pointRadius":0,"label":"y = 1/x + 2"},
        {"type":"line","data":neg,"tension":0.35,"fill":False,"borderColor":"#3b82f6","pointRadius":0},
        {"type":"line","data":asy,"borderColor":"#9ca3af","borderDash":[6,4],"borderWidth":1,"pointRadius":0,"label":"asymptote y = 2"}
    ]},"options":{"scales":{
        "x":{"min":-5,"max":5,"ticks":{"stepSize":1},"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"x","display":True}},
        "y":{"min":-4,"max":7,"ticks":{"stepSize":1},"grid":{"color":"rgba(0,0,0,0.08)"},"title":{"text":"y","display":True}}}}}

def chart_cubic_roots():
    # y = x^3 - 12x from -4 to 4
    xs = [i*0.25 for i in range(-16,17)]
    data = [{"x":round(x,3),"y":round(x**3-12*x,3)} for x in xs]
    return {"type":"scatter","data":{"datasets":[
        {"type":"line","data":data,"tension":0.35,"fill":False,"borderColor":"#ef4444","pointRadius":0,"label":"y = x³ − 12x"}
    ]},"options":{"scales":{
        "x":{"min":-4,"max":4,"ticks":{"stepSize":1},"grid":{"color":"rgba(0,0,0,0.05)"},"title":{"text":"x","display":True}},
        "y":{"min":-18,"max":18,"ticks":{"stepSize":4},"grid":{"color":"rgba(0,0,0,0.08)"},"title":{"text":"y","display":True}}}}}

# ---------- problem bank ----------
bronze = [
 {"display":"For \\(y = x^3\\), find \\(y\\) when \\(x = 2\\).","solutions":[8],"calculator":False,"input_type":"single_value",
  "hint":"Cube 2 by multiplying it by itself three times.",
  "misconceptions":[{"pattern":"cube_as_times_3","check":"cube_as_times_3","expect":6,
    "message":"A cube means multiply the number by itself three times: 2³ = 2 × 2 × 2 = 8. If you got 6 you did 2 × 3.","note":"error: 2×3=6"}],
  "guided_steps":[
    {"say":"Cubing means multiplying the number by itself three times."},
    {"pre":"First two 2s: 2 × 2 = ","post":"","answer":4,"hint":"Two times two."},
    {"phase":"substitute","pre":"Now the third 2: 4 × 2 = ","post":"","answer":8,"hint":"Multiply your answer by 2 again."},
    {"phase":"substitute","pre":"Count them back, 2 × 2 × 2 = ","post":"","answer":8,"done":"Three 2s multiplied give 8, so y = 8.","hint":"All three twos multiplied."}]},

 {"display":"For \\(y = x^3\\), find \\(y\\) when \\(x = -2\\).","solutions":[-8],"calculator":False,"input_type":"single_value",
  "hint":"Cube −2: three negatives multiplied give a negative.",
  "misconceptions":[{"pattern":"neg_cube_sign","check":"neg_cube_sign","expect":8,
    "message":"A negative number cubed stays negative: (−2)³ = (−2)(−2)(−2) = −8. Getting +8 means a minus sign was lost.","note":"error: sign dropped -> +8"}],
  "guided_steps":[
    {"say":"A negative number cubed: multiply three negatives together."},
    {"pre":"First two: (−2) × (−2) = ","post":"","answer":4,"hint":"Negative times negative is positive."},
    {"phase":"substitute","pre":"Now times the third (−2): 4 × (−2) = ","post":"","answer":-8,"hint":"Positive times negative is negative."},
    {"phase":"substitute","pre":"Three minuses multiply to a minus, so type y: ","post":"","answer":-8,"done":"An odd number of negatives stays negative: y = −8.","hint":"Odd number of minuses stays negative."}]},

 {"display":"For \\(y = \\frac{6}{x}\\), find \\(y\\) when \\(x = 3\\).","solutions":[2],"calculator":False,"input_type":"single_value",
  "hint":"Divide the top number by x: 6 ÷ 3.",
  "misconceptions":[{"pattern":"reciprocal_flip","check":"reciprocal_flip","expect":0.5,
    "message":"Divide 6 by x, not x by 6: y = 6 ÷ 3 = 2. Doing 3 ÷ 6 gives 0.5.","note":"error: 3/6=0.5"}],
  "guided_steps":[
    {"say":"A reciprocal means divide the top number by x. Here that is 6 ÷ 3."},
    {"pre":"6 ÷ 3 = ","post":"","answer":2,"hint":"Six shared into three."},
    {"phase":"substitute","pre":"Check by multiplying back: 2 × 3 = ","post":"","answer":6,"hint":"Should rebuild the 6 on top."},
    {"phase":"substitute","pre":"It rebuilds 6, so type the value of y: ","post":"","answer":2,"done":"y = 2, confirmed by the check.","hint":"The division result."}]},

 {"display":"For \\(y = \\frac{6}{x}\\), find \\(y\\) when \\(x = -2\\).","solutions":[-3],"calculator":False,"input_type":"single_value",
  "hint":"Divide 6 by −2, keeping the negative sign.",
  "misconceptions":[{"pattern":"div_sign_dropped","check":"div_sign_dropped","expect":3,
    "message":"Positive divided by negative is negative: 6 ÷ (−2) = −3. Keeping it positive gives 3.","note":"error: sign dropped -> 3"}],
  "guided_steps":[
    {"say":"Divide 6 by the negative x, keeping the sign."},
    {"pre":"Ignore signs first: 6 ÷ 2 = ","post":"","answer":3,"hint":"Six shared into two."},
    {"phase":"substitute","pre":"Positive ÷ negative is negative, so y = ","post":"","answer":-3,"hint":"Give the answer a minus sign."},
    {"phase":"substitute","pre":"Check: (−3) × (−2) = ","post":"","answer":6,"done":"It rebuilds 6, so y = −3.","hint":"Negative times negative is positive."}]},

 {"display":"For \\(y = 2^x\\), find \\(y\\) when \\(x = 4\\).","solutions":[16],"calculator":False,"input_type":"single_value",
  "hint":"2⁴ means four 2s multiplied together.",
  "misconceptions":[{"pattern":"power_as_times","check":"power_as_times","expect":8,
    "message":"A power means repeated multiplication: 2⁴ = 2 × 2 × 2 × 2 = 16. Doing 2 × 4 gives 8.","note":"error: 2×4=8"}],
  "guided_steps":[
    {"say":"A power tells you how many 2s to multiply. 2⁴ is four 2s."},
    {"pre":"First two 2s: 2 × 2 = ","post":"","answer":4,"hint":"Two times two."},
    {"phase":"substitute","pre":"Times the third 2: 4 × 2 = ","post":"","answer":8,"hint":"Double it."},
    {"phase":"substitute","pre":"Times the fourth 2: 8 × 2 = ","post":"","answer":16,"done":"Four 2s multiplied give 16, so y = 16.","hint":"Double once more."}]},

 {"display":"For \\(y = 3^x\\), find \\(y\\) when \\(x = 0\\).","solutions":[1],"calculator":False,"input_type":"single_value",
  "hint":"Any number to the power 0 is 1.",
  "misconceptions":[{"pattern":"zero_power_zero","check":"zero_power_zero","expect":0,
    "message":"Any number to the power 0 equals 1, not 0. So 3⁰ = 1.","note":"error: thinks 3^0=0"}],
  "guided_steps":[
    {"say":"Let us build down the powers of 3 to see what 3⁰ must be."},
    {"pre":"3² = 3 × 3 = ","post":"","answer":9,"hint":"Three times three."},
    {"pre":"3¹ = ","post":"","answer":3,"hint":"Just 3 itself."},
    {"phase":"substitute","pre":"Each step down divides by 3, so 3⁰ = 3 ÷ 3 = ","post":"","answer":1,"hint":"Three divided by three."},
    {"phase":"substitute","pre":"So any base to the power 0 equals ","post":"","answer":1,"done":"3⁰ = 1, and the same is true for any base.","hint":"The pattern lands on 1."}]},

 {"display":"Which graph type has a curve that never touches the axes?","options":["Reciprocal","Quadratic","Linear","Cubic"],
  "solutions":[0],"calculator":False,"input_type":"multiple_choice",
  "hint":"Think which curve has asymptotes and never meets the axes.",
  "misconceptions":[{"pattern":"graph_type","check":"graph_type","expect":None,
    "message":"Reciprocal graphs y = a/x have asymptotes at x = 0 and y = 0, so they approach but never touch the axes.","note":"MC"}]},

 {"display":"For \\(y = 2^x\\), find \\(y\\) when \\(x = 5\\).","solutions":[32],"calculator":False,"input_type":"single_value",
  "hint":"2⁵ means five 2s multiplied: keep doubling.",
  "misconceptions":[{"pattern":"power_as_times","check":"power_as_times","expect":10,
    "message":"2⁵ means five 2s multiplied: 2 × 2 × 2 × 2 × 2 = 32. Doing 2 × 5 gives 10.","note":"error: 2×5=10"}],
  "guided_steps":[
    {"say":"2⁵ is five 2s multiplied. Build it up doubling each time."},
    {"pre":"2 × 2 = ","post":"","answer":4,"hint":"Two twos."},
    {"pre":"Double again (three 2s): 4 × 2 = ","post":"","answer":8,"hint":"Double it."},
    {"phase":"substitute","pre":"Double again (four 2s): 8 × 2 = ","post":"","answer":16,"hint":"Double it."},
    {"phase":"substitute","pre":"Double once more (five 2s): 16 × 2 = ","post":"","answer":32,"done":"Five 2s multiplied give 32, so y = 32.","hint":"Final double."}]},
]

silver = [
 {"display":"For \\(y = x^3 - 4x\\), find \\(y\\) when \\(x = 2\\).","solutions":[0],"calculator":False,"input_type":"single_value",
  "hint":"Cube the 2 first, then subtract 4 times 2.",
  "misconceptions":[{"pattern":"cube_as_times_3","check":"cube_as_times_3","expect":-2,
    "message":"Cube the x, do not multiply it by 3: 2³ = 8, so y = 8 − 8 = 0. Using 3 × 2 = 6 gives −2.","note":"error: 3x -> 6-8=-2"}],
  "guided_steps":[
    {"say":"Work out the cube first, then subtract 4 times x."},
    {"pre":"Cube the 2: 2 × 2 × 2 = ","post":"","answer":8,"hint":"Three 2s multiplied."},
    {"phase":"substitute","pre":"Work out 4x: 4 × 2 = ","post":"","answer":8,"hint":"Four times two."},
    {"phase":"substitute","pre":"Subtract: 8 − 8 = ","post":"","answer":0,"done":"y = 0, so the curve crosses the x-axis here.","hint":"Take the second from the first."}]},

 {"display":"For \\(y = \\frac{12}{x}\\), find \\(y\\) when \\(x = 4\\).","solutions":[3],"calculator":False,"input_type":"single_value",
  "hint":"Divide 12 by 4.",
  "misconceptions":[{"pattern":"subtract_not_divide","check":"subtract_not_divide","expect":8,
    "message":"This is a division, not a subtraction: y = 12 ÷ 4 = 3. Doing 12 − 4 gives 8.","note":"error: 12-4=8"}],
  "guided_steps":[
    {"say":"Divide the top number by x."},
    {"pre":"12 ÷ 4 = ","post":"","answer":3,"hint":"Twelve shared into four."},
    {"phase":"substitute","pre":"Check by multiplying back: 3 × 4 = ","post":"","answer":12,"hint":"Should rebuild 12."},
    {"phase":"substitute","pre":"It rebuilds 12, so y = ","post":"","answer":3,"done":"y = 3, confirmed.","hint":"The division result."}]},

 {"display":"For \\(y = \\frac{-8}{x}\\), find \\(y\\) when \\(x = 4\\).","solutions":[-2],"calculator":False,"input_type":"single_value",
  "hint":"Divide −8 by 4, keeping the minus sign.",
  "misconceptions":[{"pattern":"div_sign_dropped","check":"div_sign_dropped","expect":2,
    "message":"Keep the negative: −8 ÷ 4 = −2. Dropping the sign gives 2.","note":"error: sign dropped -> 2"}],
  "guided_steps":[
    {"say":"Divide, keeping the negative sign on top."},
    {"pre":"Ignore signs first: 8 ÷ 4 = ","post":"","answer":2,"hint":"Eight shared into four."},
    {"phase":"substitute","pre":"Negative ÷ positive is negative, so y = ","post":"","answer":-2,"hint":"Give it a minus."},
    {"phase":"substitute","pre":"Check: (−2) × 4 = ","post":"","answer":-8,"done":"It rebuilds −8, so y = −2.","hint":"Negative times positive is negative."}]},

 {"display":"A graph passes through \\((0, 1)\\) and doubles each time \\(x\\) increases by 1. What type is it?",
  "options":["Exponential","Linear","Quadratic","Cubic"],"solutions":[0],"calculator":False,"input_type":"multiple_choice",
  "hint":"Doubling at every step is exponential growth.",
  "misconceptions":[{"pattern":"graph_type","check":"graph_type","expect":None,
    "message":"Doubling at every step is exponential growth. This is y = 2ˣ, which passes through (0, 1).","note":"MC"}]},

 {"display":"For \\(y = 5^x\\), find \\(y\\) when \\(x = 2\\).","solutions":[25],"calculator":False,"input_type":"single_value",
  "hint":"5² means 5 × 5, not 5 × 2.",
  "misconceptions":[{"pattern":"power_as_times","check":"power_as_times","expect":10,
    "message":"5² means two 5s multiplied: 5 × 5 = 25. Doing 5 × 2 gives 10.","note":"error: 5×2=10"}],
  "guided_steps":[
    {"say":"A power of 2 means multiply the base by itself once."},
    {"pre":"Write it out: 5 × 5 = ","post":"","answer":25,"hint":"Five times five."},
    {"phase":"substitute","pre":"First see the trap route: 5 × 2 = ","post":"","answer":10,"hint":"This is what NOT to do."},
    {"phase":"substitute","pre":"The power route is correct, so type the real y: ","post":"","answer":25,"done":"5² = 5 × 5 = 25, not 10. So y = 25.","hint":"Use the 5 × 5 answer."}]},

 {"display":"For \\(y = x^3 + 1\\), find \\(y\\) when \\(x = -2\\).","solutions":[-7],"calculator":False,"input_type":"single_value",
  "hint":"Cube −2 first (it stays negative), then add 1.",
  "misconceptions":[{"pattern":"neg_cube_sign","check":"neg_cube_sign","expect":9,
    "message":"A negative cubed stays negative: (−2)³ = −8, so y = −8 + 1 = −7. Treating (−2)³ as +8 gives 9.","note":"error: (-2)^3 as +8 -> 9"}],
  "guided_steps":[
    {"say":"Cube the negative first, then add 1."},
    {"pre":"Cube (−2): (−2) × (−2) × (−2) = ","post":"","answer":-8,"hint":"Three negatives multiply to a negative."},
    {"phase":"substitute","pre":"Add 1: −8 + 1 = ","post":"","answer":-7,"hint":"Count up one from −8."},
    {"phase":"substitute","pre":"Confirm the sign stayed negative, so y = ","post":"","answer":-7,"done":"(−2)³ = −8, so y = −8 + 1 = −7.","hint":"Odd power keeps the minus."}]},

 {"display":"Which point does every exponential graph \\(y = a^x\\) pass through?",
  "options":["\\((0, 1)\\)","\\((1, 0)\\)","\\((0, 0)\\)","\\((1, 1)\\)"],"solutions":[0],"calculator":False,"input_type":"multiple_choice",
  "hint":"Substitute x = 0 into y = aˣ.",
  "misconceptions":[{"pattern":"exp_property","check":"exp_property","expect":None,
    "message":"When x = 0, y = a⁰ = 1 for any a > 0, so every exponential graph passes through (0, 1).","note":"MC"}]},
]

gold = [
 {"display":"For \\(y = x^3 - 6x^2 + 9x\\), find \\(y\\) when \\(x = 3\\).","solutions":[0],"calculator":False,"input_type":"single_value",
  "hint":"Square the 3 inside 6x² before multiplying by 6.",
  "misconceptions":[{"pattern":"square_term_error","check":"square_term_error","expect":36,
    "message":"The middle term is 6x², so 6 × 3² = 6 × 9 = 54, giving 27 − 54 + 27 = 0. Using 6 × 3 = 18 gives 36.","note":"error: 6x not 6x^2 -> 27-18+27=36"}],
  "guided_steps":[
    {"say":"Work out each term at x = 3, then combine."},
    {"pre":"Cube: 3³ = ","post":"","answer":27,"hint":"3 × 3 × 3."},
    {"pre":"Middle term 6x²: 6 × 3² = 6 × 9 = ","post":"","answer":54,"hint":"Square the 3 first, then times 6."},
    {"phase":"substitute","pre":"Last term 9x: 9 × 3 = ","post":"","answer":27,"hint":"Nine times three."},
    {"phase":"substitute","pre":"Combine: 27 − 54 + 27 = ","post":"","answer":0,"done":"y = 0, so the curve touches the x-axis at x = 3.","hint":"Add the two 27s, then take off 54."}]},

 {"display":"For \\(y = \\frac{1}{x} + 2\\), what is the horizontal asymptote?","solutions":[2],"calculator":False,"input_type":"single_value",
  "hint":"As x grows, 1/x heads to 0; add the 2.",
  "chart":chart_reciprocal_shift(),
  "misconceptions":[{"pattern":"shift_ignored","check":"shift_ignored","expect":0,
    "message":"The +2 shifts the whole curve up 2, so the asymptote is y = 2, not y = 0.","note":"error: ignores +2 -> 0"}],
  "guided_steps":[
    {"say":"A horizontal asymptote is the y-value the curve creeps towards as x gets very big. Watch 1/x shrink."},
    {"pre":"When x = 10: 1 ÷ 10 = ","post":"","answer":0.1,"hint":"One tenth."},
    {"pre":"Add the 2: 0.1 + 2 = ","post":"","answer":2.1,"hint":"Just add two."},
    {"phase":"substitute","pre":"When x = 1000: 1 ÷ 1000 = 0.001, then + 2 = ","post":"","answer":2.001,"hint":"Almost exactly two."},
    {"phase":"substitute","pre":"The fraction is heading to 0, so y heads to ","post":"","answer":2,"done":"The +2 shifts the curve up 2, so the asymptote is y = 2.","hint":"0 plus 2."}]},

 {"display":"A population doubles every year from an initial 500. What is the population after 4 years?","solutions":[8000],"calculator":False,"input_type":"single_value",
  "hint":"Doubling 4 times multiplies the start by 2⁴ = 16.",
  "misconceptions":[{"pattern":"linear_not_exp","check":"linear_not_exp","expect":4000,
    "message":"Doubling 4 times means × 2⁴ = × 16, so 500 × 16 = 8000. Doing 500 × 2 × 4 gives 4000.","note":"error: 500*2*4=4000"}],
  "guided_steps":[
    {"say":"Doubling 4 times multiplies by 2 four times, that is × 2⁴."},
    {"pre":"Work out 2⁴: 2 × 2 × 2 × 2 = ","post":"","answer":16,"hint":"Double four times from 1."},
    {"phase":"substitute","pre":"Multiply the start by 16: 500 × 16 = ","post":"","answer":8000,"hint":"500 × 16."},
    {"phase":"substitute","pre":"Check by doubling year by year, 1000, 2000, 4000, then = ","post":"","answer":8000,"done":"Doubling to 1000, 2000, 4000, 8000 confirms 8000.","hint":"Keep doubling: 4000 doubled."}]},

 {"display":"For \\(y = 10^x\\), find \\(y\\) when \\(x = -1\\).","solutions":[0.1],"calculator":False,"input_type":"single_value",
  "hint":"A negative power means the reciprocal: 1 over 10¹.",
  "misconceptions":[{"pattern":"neg_power_times","check":"neg_power_times","expect":-10,
    "message":"A negative power means the reciprocal: 10⁻¹ = 1/10 = 0.1. Doing 10 × (−1) gives −10.","note":"error: 10*-1=-10"}],
  "guided_steps":[
    {"say":"A negative power means take the reciprocal, that is 1 over the positive power."},
    {"pre":"Positive power first: 10¹ = ","post":"","answer":10,"hint":"Just 10."},
    {"phase":"substitute","pre":"Reciprocal: 1 ÷ 10 = ","post":"","answer":0.1,"hint":"One tenth as a decimal."},
    {"phase":"substitute","pre":"So 10⁻¹ = ","post":"","answer":0.1,"done":"10⁻¹ = 1/10 = 0.1.","hint":"Same as the reciprocal."}]},

 {"display":"For \\(y = x^3 - 12x\\), find the two values of \\(x\\) where \\(y = 0\\) (other than \\(x = 0\\)).","solutions":[-3.46,3.46],"calculator":True,"input_type":"two_solutions",
  "hint":"Factorise as x(x² − 12) = 0, then square-root 12.",
  "chart":chart_cubic_roots(),
  "misconceptions":[{"pattern":"sqrt_halved","check":"sqrt_halved","expect":[-6,6],
    "message":"From x² = 12, take the square root: x = ±√12 ≈ ±3.46. Halving 12 to get ±6 is the slip.","note":"error: 12/2=6"}],
  "guided_steps":[
    {"say":"Set y = 0 and factorise: x³ − 12x = x(x² − 12) = 0. One root is x = 0; the others come from x² − 12 = 0."},
    {"pre":"Rearrange x² − 12 = 0 to get x² = ","post":"","answer":12,"hint":"Add 12 to both sides."},
    {"phase":"substitute","pre":"Square-root 12 on a calculator, to 2 decimal places: √12 = ","post":"","answer":3.46,"hint":"√12 is between 3 and 4."},
    {"phase":"substitute","pre":"There are two roots, one + and one −. The negative one is ","post":"","answer":-3.46,"done":"So x = ±3.46, and both satisfy x³ − 12x = 0.","hint":"Same size, opposite sign."}]},
]

# ---------- tier_guides ----------
tier_guides = {
 "bronze":{
  "title":"Bronze: reading one value off a curve",
  "steps":[
    "Cube by multiplying three times: \\(2^3 = 2 × 2 × 2 = 8\\). A power like \\(2^4\\) means four 2s multiplied.",
    "Reciprocal \\(y = \\frac{a}{x}\\): divide a by x. \\(y = \\frac{6}{3} = 2\\).",
    "Any number to the power 0 is 1. Reciprocal curves never touch the axes."],
  "example":{"question":"For y = 2ˣ, find y when x = 4.","steps":[
    {"label":"Write it out","content":"2 × 2 × 2 × 2"},
    {"label":"Multiply","content":"4 × 4 = 16"},
    {"label":"Check","content":"Powers of 2: 2, 4, 8, 16"},
    {"label":"Answer","content":"y = 16","isAnswer":True,"is_answer":True}]}},
 "silver":{
  "title":"Silver: negatives, powers and curve features",
  "steps":[
    "A negative number cubed stays negative: \\((-2)^3 = -8\\). Square first inside a term like \\(6x^2\\).",
    "Keep signs in division: \\(\\frac{-8}{4} = -2\\).",
    "Every \\(y = a^x\\) passes through \\((0, 1)\\); doubling at each step means exponential growth."],
  "example":{"question":"For y = x³ − 4x, find y when x = 3.","steps":[
    {"label":"Cube","content":"3³ = 27"},
    {"label":"Subtract 4x","content":"27 − 4 × 3 = 27 − 12"},
    {"label":"Check","content":"Cube first, then take 4x away"},
    {"label":"Answer","content":"y = 15","isAnswer":True,"is_answer":True}]}},
 "gold":{
  "title":"Gold: asymptotes, models and roots",
  "steps":[
    "A horizontal asymptote is the y-value the curve approaches. For \\(y = \\frac{1}{x} + 2\\), as x grows \\(\\frac{1}{x} \\to 0\\), so \\(y \\to 2\\).",
    "Exponential models: doubling n times multiplies the start by \\(2^n\\).",
    "Cubic roots: solve \\(y = 0\\) by factorising, e.g. \\(x^3 - 12x = x(x^2 - 12)\\)."],
  "example":{"question":"y = 3ˣ models bacteria (thousands) after x hours. How many after 3 hours?","steps":[
    {"label":"Substitute","content":"3³"},
    {"label":"Work out","content":"3 × 3 × 3 = 27"},
    {"label":"Interpret","content":"27 thousand bacteria"},
    {"label":"Answer","content":"y = 27","isAnswer":True,"is_answer":True}]}},
}

# ---------- guided (opener + teach) ----------
guided = {
 "opener":{
  "display": svg_exponential() + '<span class="figure-caption">Bacteria doubling every hour</span><p>One bacterium splits into two every hour. Start with 1, then 2, then 4, then 8...</p>',
  "steps":[
    {"pre":"Carry on doubling. How many bacteria after 4 hours? ","post":"","answer":16,"hint":"Double the 8."},
    {"pre":"And after 5 hours? ","post":"","answer":32,"hint":"Double the 16."},
    {"say":"You just followed an <strong>exponential</strong> curve, \\(y = 2^x\\): it starts almost flat, always passes through \\((0, 1)\\), then shoots up. This lesson also meets <strong>cubic</strong> curves \\(y = x^3\\) and <strong>reciprocal</strong> curves \\(y = \\frac{a}{x}\\), whose two branches never touch the axes."}]},
 "teach":{
  "bronze":{
   "display":"For \\(y = \\frac{8}{x}\\), find \\(y\\) when \\(x = 2\\), and again when \\(x = -4\\).",
   "steps":[
     {"say":"For a reciprocal, divide the top number by x."},
     {"pre":"Divide 8 by 2: 8 ÷ 2 = ","post":"","answer":4,"hint":"Eight shared into two."},
     {"pre":"Now the negative x: 8 ÷ (−4) = ","post":"","answer":-2,"hint":"Positive divided by negative is negative."},
     {"pre":"How many branches does the reciprocal curve have? ","post":"","answer":2,"hint":"One in quadrant 1, one in quadrant 3."},
     {"pre":"How many axes does the curve ever touch? ","post":"","answer":0,"done":"Zero: reciprocal curves have asymptotes at x = 0 and y = 0, so they never touch either axis.","hint":"Asymptotes mean it never touches."}]},
  "silver":{
   "display":"For \\(y = 4^x\\), find \\(y\\) when \\(x = 2\\), when \\(x = 0\\), and when \\(x = -1\\).",
   "steps":[
     {"say":"A power tells you how many 4s to multiply."},
     {"pre":"Two 4s multiplied: 4 × 4 = ","post":"","answer":16,"hint":"Four times four."},
     {"pre":"Anything to the power 0: 4⁰ = ","post":"","answer":1,"hint":"Any number to the power 0 is 1."},
     {"pre":"A negative power is the reciprocal: 4⁻¹ = 1 ÷ 4 = ","post":"","answer":0.25,"hint":"One quarter as a decimal."},
     {"pre":"So every curve y = aˣ passes through (0, 1). Type that shared y-value: ","post":"","answer":1,"done":"Every exponential curve goes through (0, 1), because a⁰ = 1 for any base.","hint":"They all share the same y when x = 0."}]},
  "gold":{
   "display":"For \\(y = \\frac{1}{x} + 3\\), find the horizontal asymptote by seeing what happens as x gets very large.",
   "steps":[
     {"say":"As x grows huge, the fraction 1/x shrinks towards 0. Let us watch it."},
     {"pre":"When x = 10: 1 ÷ 10 = ","post":"","answer":0.1,"hint":"One tenth."},
     {"pre":"Add the 3: 0.1 + 3 = ","post":"","answer":3.1,"hint":"Just add three."},
     {"pre":"When x = 1000: 1 ÷ 1000 = 0.001, add 3 = ","post":"","answer":3.001,"hint":"Almost exactly three."},
     {"pre":"The fraction is heading to 0, so y heads to which value? ","post":"","answer":3,"done":"The +3 lifts the whole curve up 3, so the horizontal asymptote is y = 3.","hint":"0 plus 3."}]}},
}

# ---------- method_card (slim) ----------
method_card = {
 "title":"Recognising Cubic, Reciprocal & Exponential Graphs",
 "steps":[
   "Spot the type: \\(x^3\\) is cubic, \\(\\frac{a}{x}\\) is reciprocal, \\(a^x\\) is exponential.",
   "Make a table of values, including negative x, then plot and join with a smooth curve.",
   "Reciprocal: two branches, asymptotes at \\(x = 0\\) and \\(y = 0\\).",
   "Exponential \\(y = a^x\\): always through \\((0, 1)\\), asymptote \\(y = 0\\)."],
 "content":"<p><strong>Cubic</strong> graphs \\(y = ax^3 + \\ldots\\) rise from bottom-left to top-right when \\(a > 0\\), and can have up to two turning points.</p><p><strong>Reciprocal</strong> graphs \\(y = \\frac{a}{x}\\) have two branches and never touch the axes.</p><p><strong>Exponential</strong> graphs \\(y = a^x\\) pass through \\((0, 1)\\); they grow fast when \\(a > 1\\) and decay when \\(0 < a < 1\\).</p>",
 "example":"<p><strong>Sketch \\(y = \\frac{4}{x}\\).</strong> \\(x = 1 \\to 4\\), \\(x = 2 \\to 2\\), \\(x = 4 \\to 1\\), with the mirror branch in quadrant 3 for negative x. Two branches; the curve never meets the axes.</p>"
}

# ---------- assemble ----------
pd = dict(live)  # preserve everything
pd["method_card"] = method_card
pd["problem_bank"] = {
  "bronze":bronze, "silver":silver, "gold":gold,
  "bronze_description":"Read one value off a cubic, reciprocal or exponential curve: substitute a whole number and work out y.",
  "silver_description":"Handle negatives, larger powers and named curve features across all three graph families.",
  "gold_description":"Interpret asymptotes, exponential models and cubic roots, reading them from the curve.",
}
pd["tier_guides"] = tier_guides
pd["guided"] = guided
# topic_links, related_videos, worked_examples preserved from live

json.dump(pd, open("lesson_maths-aqa_graphs-L05.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written; problem counts b/s/g:", len(bronze), len(silver), len(gold))
print("keys:", list(pd.keys()))
