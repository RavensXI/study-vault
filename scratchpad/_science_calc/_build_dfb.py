# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post != "": d["post"] = post
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def svg(shape, img_label, mag_label, aria):
    parts = ['<svg viewBox="0 0 320 180" role="img" aria-label="%s" '
             'style="max-width:280px;margin:0.6em auto;display:block;">' % aria]
    if shape == "cell":
        parts.append('<ellipse cx="160" cy="80" rx="95" ry="45" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
    elif shape == "cell_nuc":
        parts.append('<ellipse cx="160" cy="80" rx="95" ry="45" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
        parts.append('<ellipse cx="142" cy="72" rx="26" ry="18" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
    elif shape == "mito":
        parts.append('<rect x="70" y="58" width="180" height="44" rx="22" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
        parts.append('<path d="M92 58 q14 22 0 44 M124 58 q14 22 0 44 M156 58 q14 22 0 44 M188 58 q14 22 0 44 M220 58 q14 22 0 44" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>')
    elif shape == "rbc":
        parts.append('<ellipse cx="160" cy="80" rx="80" ry="42" fill="#f87171" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
        parts.append('<ellipse cx="160" cy="80" rx="30" ry="16" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6"/>')
    elif shape == "chloro":
        parts.append('<ellipse cx="160" cy="80" rx="95" ry="42" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
        parts.append('<ellipse cx="132" cy="74" rx="22" ry="12" fill="#059669" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2"/>')
        parts.append('<ellipse cx="184" cy="88" rx="22" ry="12" fill="#059669" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2"/>')
    elif shape == "bacterium":
        parts.append('<rect x="80" y="62" width="160" height="36" rx="18" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>')
    parts.append('<line x1="65" y1="150" x2="255" y2="150" stroke="currentColor" stroke-width="1.5"/>')
    parts.append('<line x1="65" y1="145" x2="65" y2="155" stroke="currentColor" stroke-width="1.5"/>')
    parts.append('<line x1="255" y1="145" x2="255" y2="155" stroke="currentColor" stroke-width="1.5"/>')
    parts.append('<text x="160" y="169" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="currentColor">%s</text>' % img_label)
    parts.append('<text x="160" y="28" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="currentColor">%s</text>' % mag_label)
    parts.append('</svg>')
    return "".join(parts)

def question(svg_html, text):
    return svg_html + '<p style="margin-top:0.7em;">' + text + '</p>'

def misc(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}

CHECKS = []
def A(val, computed):
    CHECKS.append((val, computed))
    return val

bronze = []
d="A cell image is 24 mm wide. The actual cell is 0.06 mm wide. Calculate the magnification."
bronze.append({
 "unit":"×","display":d,
 "question":question(svg("cell","Image length: 24 mm","Magnification: ?","Diagram of a cell image 24 mm wide, magnification unknown"),d),
 "solutions":[400],"calculator":True,"input_type":"single_value",
 "equation_hint":"magnification = image size ÷ actual size",
 "hint":"Both lengths are in mm already, so divide the image size by the actual size.",
 "misconceptions":[misc("inverse_error","Magnification = image ÷ actual, not the other way round: 24 ÷ 0.06 = 400.",A(0.0025,0.06/24))],
 "guided_steps":[
   sayonly("Magnification = image size ÷ actual size. It has no unit, it is just how many times bigger the image is."),
   box("Both lengths are in mm, so no conversion is needed. To divide 24 by 0.06 without a decimal slip, scale both by 100. Image: 24 × 100 = ",A(2400,24*100),"Move the decimal two places: 24 becomes 2400."),
   box("Actual: 0.06 × 100 = ",A(6,0.06*100),"0.06 × 100 = 6."),
   box("Now divide: 2400 ÷ 6 = ",A(400,2400/6),"How many 6s in 2400?",phase="substitute"),
   box("Check: actual × magnification should give the image. 0.06 × 400 = ",A(24,0.06*400),"0.06 × 400.",post=" mm",phase="substitute",done="Back to 24 mm, so the magnification is ×400. Remember, magnification has no unit."),
 ]})
d="A plant cell is drawn at ×400. The drawn width is 20 mm. Calculate the actual width of the cell in mm."
bronze.append({
 "unit":"mm","display":d,
 "question":question(svg("cell_nuc","Image length: 20 mm","Magnification: ×400","Diagram of a plant cell drawn 20 mm wide at magnification 400"),d),
 "solutions":[0.05],"calculator":True,"input_type":"single_value",
 "equation_hint":"actual = image ÷ magnification",
 "hint":"To find the actual size, divide the drawn size by the magnification.",
 "misconceptions":[misc("inverse_error","Actual = image ÷ magnification = 20 ÷ 400 = 0.05 mm. Multiplying instead gives 8000 mm, far too big for a real cell.",A(8000,20*400))],
 "guided_steps":[
   sayonly("To find the actual size, rearrange to actual = image ÷ magnification. The image is 20 mm and magnification has no unit, so the answer stays in mm."),
   box("Write the number you will divide by (the magnification): ",A(400,400),"It is the ×400 in the question."),
   box("Now divide: 20 ÷ 400 = ",A(0.05,20/400),"20 ÷ 400 = 0.05.",post=" mm",phase="substitute"),
   box("Check: actual × magnification = 0.05 × 400 = ",A(20,0.05*400),"0.05 × 400.",post=" mm",phase="substitute",done="Back to the 20 mm image, so the actual width is 0.05 mm."),
 ]})
d="Convert 0.25 mm to µm."
bronze.append({
 "unit":"µm","display":d,"solutions":[250],"calculator":True,"input_type":"single_value",
 "equation_hint":"Multiply by 1,000 to go from mm to µm",
 "hint":"mm to µm moves to smaller units, so multiply by 1000.",
 "misconceptions":[misc("unit_error","mm to µm makes the number bigger, so multiply by 1000: 0.25 × 1000 = 250 µm.",A(0.00025,0.25/1000))],
 "guided_steps":[
   sayonly("Going from mm to µm moves to smaller units, so the number gets bigger. The rule: 1 mm = 1000 µm."),
   box("How many µm are in 1 mm? ",A(1000,1000),"1 mm = 1000 µm."),
   box("So multiply: 0.25 × 1000 = ",A(250,0.25*1000),"0.25 × 1000 moves the decimal three places.",post=" µm",phase="substitute"),
   box("Check by going back: 250 ÷ 1000 = ",A(0.25,250/1000),"250 ÷ 1000.",post=" mm",phase="substitute",done="Back to 0.25 mm, so 0.25 mm = 250 µm."),
 ]})
d="Convert 8,500 nm to µm."
bronze.append({
 "unit":"µm","display":d,"solutions":[8.5],"calculator":True,"input_type":"single_value",
 "equation_hint":"Divide by 1,000 to go from nm to µm",
 "hint":"nm to µm moves to larger units, so divide by 1000.",
 "misconceptions":[misc("unit_error","nm to µm makes the number smaller, so divide by 1000: 8500 ÷ 1000 = 8.5 µm.",A(8500000,8500*1000))],
 "guided_steps":[
   sayonly("Going from nm to µm moves to larger units, so the number gets smaller. The rule: 1000 nm = 1 µm."),
   box("How many nm are in 1 µm? ",A(1000,1000),"1 µm = 1000 nm."),
   box("So divide: 8500 ÷ 1000 = ",A(8.5,8500/1000),"8500 ÷ 1000 moves the decimal three places left.",post=" µm",phase="substitute"),
   box("Check by going back: 8.5 × 1000 = ",A(8500,8.5*1000),"8.5 × 1000.",post=" nm",phase="substitute",done="Back to 8500 nm, so 8500 nm = 8.5 µm."),
 ]})
d="Convert 2 µm to nm."
bronze.append({
 "unit":"nm","display":d,"solutions":[2000],"calculator":True,"input_type":"single_value",
 "equation_hint":"Multiply by 1,000 to go from µm to nm",
 "hint":"µm to nm moves to smaller units, so multiply by 1000.",
 "misconceptions":[misc("unit_error","µm to nm makes the number bigger, so multiply by 1000: 2 × 1000 = 2000 nm.",A(0.002,2/1000))],
 "guided_steps":[
   sayonly("µm to nm moves to smaller units, so the number gets bigger. The rule: 1 µm = 1000 nm."),
   box("How many nm are in 1 µm? ",A(1000,1000),"1 µm = 1000 nm."),
   box("So multiply: 2 × 1000 = ",A(2000,2*1000),"2 × 1000.",post=" nm",phase="substitute"),
   box("Check by going back: 2000 ÷ 1000 = ",A(2,2000/1000),"2000 ÷ 1000.",post=" µm",phase="substitute",done="Back to 2 µm, so 2 µm = 2000 nm."),
 ]})
d="A cell is 40 µm long. What is this in mm?"
bronze.append({
 "unit":"mm","display":d,"solutions":[0.04],"calculator":True,"input_type":"single_value",
 "equation_hint":"Divide by 1,000 to go from µm to mm",
 "hint":"µm to mm moves to larger units, so divide by 1000.",
 "misconceptions":[misc("unit_error","µm to mm makes the number smaller, so divide by 1000: 40 ÷ 1000 = 0.04 mm.",A(40000,40*1000))],
 "guided_steps":[
   sayonly("µm to mm moves to larger units, so the number gets smaller. The rule: 1000 µm = 1 mm."),
   box("How many µm are in 1 mm? ",A(1000,1000),"1 mm = 1000 µm."),
   box("So divide: 40 ÷ 1000 = ",A(0.04,40/1000),"40 ÷ 1000 moves the decimal three places left.",post=" mm",phase="substitute"),
   box("Check by going back: 0.04 × 1000 = ",A(40,0.04*1000),"0.04 × 1000.",post=" µm",phase="substitute",done="Back to 40 µm, so 40 µm = 0.04 mm."),
 ]})

silver = []
d="An electron microscope image shows a mitochondrion with drawn length 60 mm at ×12,000 magnification. Calculate the actual length in µm."
silver.append({
 "unit":"µm","display":d,
 "question":question(svg("mito","Image length: 60 mm","Magnification: ×12000","Diagram of a mitochondrion image 60 mm long at magnification 12000"),d),
 "solutions":[5],"calculator":True,"input_type":"single_value",
 "equation_hint":"Actual = image ÷ magnification, then convert mm to µm.",
 "hint":"Divide to get the size in mm, then convert mm to µm.",
 "misconceptions":[misc("forgot_convert","0.005 mm is right, but the question asks for µm. Convert: 0.005 × 1000 = 5 µm.",A(0.005,60/12000))],
 "guided_steps":[
   sayonly("Two steps. First rearrange: actual = image ÷ magnification, which gives the size in mm. Then convert mm to µm because the question asks for µm."),
   box("Divide: 60 ÷ 12000 = ",A(0.005,60/12000),"60 ÷ 12000 = 0.005.",post=" mm"),
   box("Now convert mm to µm (multiply by 1000): 0.005 × 1000 = ",A(5,0.005*1000),"0.005 × 1000 moves the decimal three places.",post=" µm",phase="substitute"),
   box("Check: actual × magnification back to the image. 0.005 × 12000 = ",A(60,0.005*12000),"0.005 × 12000.",post=" mm",phase="substitute",done="Back to 60 mm, so the actual length is 5 µm."),
 ]})
d="A cell under a light microscope appears 3 mm wide at ×150. Calculate the actual width in µm."
silver.append({
 "unit":"µm","display":d,
 "question":question(svg("cell","Image length: 3 mm","Magnification: ×150","Diagram of a cell image 3 mm wide at magnification 150"),d),
 "solutions":[20],"calculator":True,"input_type":"single_value",
 "equation_hint":"Actual = image ÷ magnification, then convert mm to µm.",
 "hint":"Divide to get mm, then convert mm to µm.",
 "misconceptions":[misc("forgot_convert","0.02 mm is correct so far, but the answer must be in µm: 0.02 × 1000 = 20 µm.",A(0.02,3/150))],
 "guided_steps":[
   sayonly("Rearrange first: actual = image ÷ magnification, in mm. Then convert mm to µm."),
   box("Divide: 3 ÷ 150 = ",A(0.02,3/150),"3 ÷ 150 = 0.02.",post=" mm"),
   box("Convert mm to µm (× 1000): 0.02 × 1000 = ",A(20,0.02*1000),"0.02 × 1000.",post=" µm",phase="substitute"),
   box("Check: 0.02 × 150 = ",A(3,0.02*150),"0.02 × 150.",post=" mm",phase="substitute",done="Back to 3 mm, so the actual width is 20 µm."),
 ]})
d="A bacterium has actual length 3 µm. At ×2,000, calculate the image length in mm."
silver.append({
 "unit":"mm","display":d,
 "question":question(svg("bacterium","Image length: ?","Magnification: ×2000","Diagram of a bacterium at magnification 2000, image length unknown"),d),
 "solutions":[6],"calculator":True,"input_type":"single_value",
 "equation_hint":"Convert µm to mm first, then image = actual × magnification.",
 "hint":"Convert the actual size to mm first, then multiply by the magnification.",
 "misconceptions":[misc("forgot_convert","Convert 3 µm to mm first: 0.003 mm. Image = 0.003 × 2000 = 6 mm. Using 3 without converting gives 6000 mm, which is 6 metres.",A(6000,3*2000))],
 "guided_steps":[
   sayonly("Convert the units first, then use image = actual size × magnification. The image will be in mm, so convert the actual 3 µm to mm before multiplying."),
   box("Convert 3 µm to mm (÷ 1000): 3 ÷ 1000 = ",A(0.003,3/1000),"3 ÷ 1000 = 0.003.",post=" mm"),
   box("Now image = actual × magnification: 0.003 × 2000 = ",A(6,0.003*2000),"0.003 × 2000.",post=" mm",phase="substitute"),
   box("Check: actual = image ÷ magnification = 6 ÷ 2000 = ",A(0.003,6/2000),"6 ÷ 2000.",post=" mm",phase="substitute",done="Back to 0.003 mm, which is 3 µm, so the image is 6 mm."),
 ]})
d="A cell in a photomicrograph is 15 mm wide. The actual cell is 30 µm wide. Calculate the magnification. (Convert 30 µm to mm first)"
silver.append({
 "unit":"×","display":d,
 "question":question(svg("cell","Image length: 15 mm","Magnification: ?","Diagram of a cell image 15 mm wide, magnification unknown"),d),
 "solutions":[500],"calculator":True,"input_type":"single_value",
 "equation_hint":"Convert µm to mm, then magnification = image ÷ actual.",
 "hint":"Convert the actual size to mm so both are in mm, then divide.",
 "misconceptions":[misc("forgot_convert","Convert 30 µm to mm first: 0.03 mm. Magnification = 15 ÷ 0.03 = 500. Dividing 15 by 30 forgets the units differ.",A(0.5,15/30))],
 "guided_steps":[
   sayonly("Convert to matching units first, then magnification = image ÷ actual size. The image is in mm, so convert the actual 30 µm to mm."),
   box("Convert 30 µm to mm (÷ 1000): 30 ÷ 1000 = ",A(0.03,30/1000),"30 ÷ 1000 = 0.03.",post=" mm"),
   box("Now magnification = image ÷ actual = 15 ÷ 0.03 = ",A(500,15/0.03),"15 ÷ 0.03 is the same as 1500 ÷ 3 = 500.",phase="substitute"),
   box("Check: actual × magnification = 0.03 × 500 = ",A(15,0.03*500),"0.03 × 500.",post=" mm",phase="substitute",done="Back to 15 mm, so the magnification is ×500. No unit on magnification."),
 ]})

gold = []
d="A chloroplast has an actual diameter of 5 µm. An electron microscope image of it is 40 mm wide. Calculate the magnification."
gold.append({
 "unit":"×","display":d,
 "question":question(svg("chloro","Image length: 40 mm","Magnification: ?","Diagram of a chloroplast image 40 mm wide, magnification unknown"),d),
 "solutions":[8000],"calculator":True,"input_type":"single_value",
 "equation_hint":"Convert µm to mm, then magnification = image ÷ actual.",
 "hint":"The lengths are in different units, so convert first, then divide image by actual.",
 "misconceptions":[
   misc("forgot_convert","The image is in mm and the cell in µm. Convert 5 µm to 0.005 mm, then 40 ÷ 0.005 = 8000. Dividing 40 by 5 ignores the unit mismatch.",A(8,40/5)),
   misc("inverse_error","Magnification = image ÷ actual = 40 ÷ 0.005 = 8000, not actual ÷ image.",A(0.000125,0.005/40)),
 ],
 "guided_steps":[
   sayonly("The image is in mm and the cell in µm, so convert first, then magnification = image ÷ actual size."),
   box("Convert 5 µm to mm (÷ 1000): 5 ÷ 1000 = ",A(0.005,5/1000),"5 ÷ 1000 = 0.005.",post=" mm"),
   box("Now magnification = image ÷ actual = 40 ÷ 0.005 = ",A(8000,40/0.005),"40 ÷ 0.005 is the same as 40000 ÷ 5 = 8000.",phase="substitute"),
   box("Check: actual × magnification = 0.005 × 8000 = ",A(40,0.005*8000),"0.005 × 8000.",post=" mm",phase="substitute",done="Back to 40 mm, so the magnification is ×8000."),
 ]})
d="A virus is 150 nm in diameter. Calculate this diameter in µm."
gold.append({
 "unit":"µm","display":d,"solutions":[0.15],"calculator":True,"input_type":"single_value",
 "equation_hint":"Divide by 1,000 to go from nm to µm",
 "hint":"nm to µm moves to larger units, so divide by 1000.",
 "misconceptions":[misc("unit_error","nm to µm makes the number smaller, so divide by 1000: 150 ÷ 1000 = 0.15 µm.",A(150000,150*1000))],
 "guided_steps":[
   sayonly("Going from nm to µm moves to larger units, so the number gets smaller. The rule: 1000 nm = 1 µm."),
   box("How many nm are in 1 µm? ",A(1000,1000),"1 µm = 1000 nm."),
   box("So divide: 150 ÷ 1000 = ",A(0.15,150/1000),"150 ÷ 1000 moves the decimal three places left.",post=" µm",phase="substitute"),
   box("Check by going back: 0.15 × 1000 = ",A(150,0.15*1000),"0.15 × 1000.",post=" nm",phase="substitute",done="Back to 150 nm, so 150 nm = 0.15 µm."),
 ]})
d="A red blood cell is 7 µm in diameter. At ×1,500 magnification, what would be the diameter in mm in a drawing?"
gold.append({
 "unit":"mm","display":d,
 "question":question(svg("rbc","Image length: ?","Magnification: ×1500","Diagram of a red blood cell at magnification 1500, image length unknown"),d),
 "solutions":[10.5],"calculator":True,"input_type":"single_value",
 "equation_hint":"Convert µm to mm first, then image = actual × magnification.",
 "hint":"Convert the actual size to mm first, then multiply by the magnification.",
 "misconceptions":[misc("forgot_convert","Convert 7 µm to mm first: 0.007 mm. Image = 0.007 × 1500 = 10.5 mm. Using 7 without converting gives 10,500 mm.",A(10500,7*1500))],
 "guided_steps":[
   sayonly("Convert the units first, then image = actual size × magnification. The answer is in mm, so convert the 7 µm to mm before multiplying."),
   box("Convert 7 µm to mm (÷ 1000): 7 ÷ 1000 = ",A(0.007,7/1000),"7 ÷ 1000 = 0.007.",post=" mm"),
   box("Now image = actual × magnification: 0.007 × 1500 = ",A(10.5,0.007*1500),"0.007 × 1500 is the same as 7 × 1.5 = 10.5.",post=" mm",phase="substitute"),
   box("Check: image ÷ magnification = 10.5 ÷ 1500 = ",A(0.007,10.5/1500),"10.5 ÷ 1500.",post=" mm",phase="substitute",done="Back to 0.007 mm, which is 7 µm, so the drawing is 10.5 mm wide."),
 ]})

opener = {
 "label":"Before any formula",
 "display":"A ladybird is 5 mm long in real life.<br>In a photo it measures 60 mm across.",
 "steps":[
   box("No formula yet, just common sense. How many times bigger does the photo make the ladybird look? ",A(12,60/5),"How many 5s fit into 60? 60 ÷ 5.",say="The photo makes the ladybird look bigger. Compare the two lengths."),
   box("A beetle is really 8 mm long. A photo magnifies it 10 times. How long is it in the photo, in mm? ",A(80,8*10),"10 lots of 8 mm.",post=" mm",say="That 'how many times bigger' number is the <strong>magnification</strong>. You just did image size ÷ actual size = 60 ÷ 5."),
   sayonly("So <strong>magnification = image size ÷ actual size</strong>, a pure ratio with no unit. The one rule that catches people: both lengths must be in the SAME unit before you divide. Real cells are often measured in µm while the image is in mm, so converting units first is the whole skill."),
 ]}

teach = {
 "bronze":{
   "label":"Together: your first one",
   "display":"An image of a cell is 36 mm wide. The actual cell is 0.09 mm wide. Calculate the magnification.",
   "steps":[
     sayonly("Magnification = image size ÷ actual size, a pure ratio with no unit. Both lengths are in mm, so no conversion is needed."),
     box("Clear the decimal by scaling both by 100. Image: 36 × 100 = ",A(3600,36*100),"Move the decimal two places: 36 becomes 3600."),
     box("Actual: 0.09 × 100 = ",A(9,0.09*100),"0.09 × 100 = 9."),
     box("Now divide: 3600 ÷ 9 = ",A(400,3600/9),"How many 9s in 3600?"),
     box("Check: actual × magnification = 0.09 × 400 = ",A(36,0.09*400),"0.09 × 400.",post=" mm",done="Back to 36 mm, so the magnification is ×400. Gone, that is the whole method."),
   ]},
 "silver":{
   "label":"Together: the silver move",
   "display":"A cell appears 8 mm wide under a microscope at ×400 magnification. Calculate the actual width in µm.",
   "steps":[
     sayonly("Two steps: rearrange to actual = image ÷ magnification, which gives the size in mm, then convert mm to µm."),
     box("Divide: 8 ÷ 400 = ",A(0.02,8/400),"8 ÷ 400 = 0.02.",post=" mm"),
     box("Convert mm to µm (× 1000): 0.02 × 1000 = ",A(20,0.02*1000),"0.02 × 1000.",post=" µm"),
     box("Check the mm value: actual × magnification = 0.02 × 400 = ",A(8,0.02*400),"0.02 × 400.",post=" mm"),
     box("And 20 µm back to mm (÷ 1000) = ",A(0.02,20/1000),"20 ÷ 1000.",post=" mm",done="Everything agrees, so the actual width is 20 µm."),
   ]},
 "gold":{
   "label":"Together: the gold move",
   "display":"An image of a bacterium is 45 mm long. The bacterium is actually 3 µm long. Calculate the magnification.",
   "steps":[
     sayonly("The image is in mm and the bacterium in µm, so convert first, then magnification = image ÷ actual size."),
     box("Convert 3 µm to mm (÷ 1000): 3 ÷ 1000 = ",A(0.003,3/1000),"3 ÷ 1000 = 0.003.",post=" mm"),
     box("Magnification = 45 ÷ 0.003. Clear the decimal by scaling both by 1000. Top: 45 × 1000 = ",A(45000,45*1000),"45 × 1000 = 45000."),
     box("Bottom: 0.003 × 1000 = ",A(3,0.003*1000),"0.003 × 1000 = 3."),
     box("Now divide: 45000 ÷ 3 = ",A(15000,45000/3),"45000 ÷ 3."),
     box("Check: actual × magnification = 0.003 × 15000 = ",A(45,0.003*15000),"0.003 × 15000.",post=" mm",done="Back to 45 mm, so the magnification is ×15000. No unit on magnification."),
   ]},
}

tier_guides = {
 "bronze":{
   "title":"Bronze: one step, matching units",
   "steps":[
     "Magnification = image size ÷ actual size. It is a ratio, so it has no unit.",
     "Rearrange when you need the others: actual = image ÷ magnification; image = actual × magnification.",
     "In bronze the two lengths are already in the same unit, or it is a single unit conversion. Do one operation and you are done.",
   ],
   "example":{
     "question":"An image is 24 mm wide; the actual cell is 0.06 mm wide. Find the magnification.",
     "steps":[
       {"label":"Formula","content":"<p>magnification = image ÷ actual</p>"},
       {"label":"Same units?","content":"<p>Both are in mm, so divide straight away.</p>"},
       {"label":"Divide","content":"<p>24 ÷ 0.06 = 400</p>"},
       {"label":"Answer","content":"<p><strong>×400</strong> (no unit)</p>","isAnswer":True,"is_answer":True},
     ]}},
 "silver":{
   "title":"Silver: convert first, then apply the formula",
   "steps":[
     "Now the image and the actual size are in different units, so convert one of them first: 1 mm = 1000 µm, 1 µm = 1000 nm.",
     "Then it is a bronze question: magnification = image ÷ actual, or rearrange for the actual or image size.",
     "Watch the direction: to a smaller unit multiply by 1000, to a larger unit divide by 1000.",
   ],
   "example":{
     "question":"A cell is 3 mm wide at ×150. Find the actual width in µm.",
     "steps":[
       {"label":"Rearrange","content":"<p>actual = image ÷ magnification = 3 ÷ 150 = 0.02 mm</p>"},
       {"label":"Convert","content":"<p>0.02 mm × 1000 = 20 µm</p>"},
       {"label":"Check","content":"<p>0.02 × 150 = 3 mm ✓</p>"},
       {"label":"Answer","content":"<p><strong>20 µm</strong></p>","isAnswer":True,"is_answer":True},
     ]}},
 "gold":{
   "title":"Gold: mixed units and larger scales",
   "steps":[
     "Gold mixes units and uses large magnifications, so convert carefully before you divide or multiply.",
     "Decide what you are finding: magnification = image ÷ actual; actual = image ÷ magnification; image = actual × magnification.",
     "Convert to matching units, do the one operation, then check by working backwards.",
   ],
   "example":{
     "question":"A chloroplast is 5 µm across; its image is 40 mm. Find the magnification.",
     "steps":[
       {"label":"Convert","content":"<p>5 µm = 0.005 mm</p>"},
       {"label":"Divide","content":"<p>magnification = 40 ÷ 0.005 = 8000</p>"},
       {"label":"Check","content":"<p>0.005 × 8000 = 40 mm ✓</p>"},
       {"label":"Answer","content":"<p><strong>×8000</strong></p>","isAnswer":True,"is_answer":True},
     ]}},
}

method_card = {
 "title":"Magnification and Unit Conversions",
 "steps":[
   "Magnification = image size ÷ actual size (a ratio, no unit).",
   "Rearrange: actual = image ÷ magnification; image = actual × magnification.",
   "Put both lengths in the SAME unit before dividing.",
   "1 mm = 1000 µm, 1 µm = 1000 nm. To smaller units multiply by 1000; to larger units divide.",
 ],
 "content":("<p><strong>Magnification</strong> tells you how many times bigger an image is than the "
            "real object. It is a ratio, so it has no unit.</p>"
            "<p>The three forms: magnification = image ÷ actual; actual = image ÷ magnification; "
            "image = actual × magnification.</p>"
            "<p>The biggest mark-killer is mixed units. Always convert so the image size and actual "
            "size share one unit before you divide. Check whether your board wants the answer in mm, "
            "µm or nm.</p>"
            "<p><strong>Conversions:</strong> 1 mm = 1000 µm, 1 µm = 1000 nm. Moving to a smaller "
            "unit multiplies by 1000; moving to a larger unit divides by 1000.</p>"),
}

worked_examples = [
 {"difficulty":"Bronze",
  "question":"A cell appears 24 mm wide in a photograph. The actual width is 0.06 mm. Calculate the magnification.",
  "steps":[
   {"label":"Step 1: Identify the formula","content":"<p>magnification = image size ÷ actual size</p>"},
   {"label":"Step 2: Check units are the same (both mm)","content":"<p>image = 24 mm; actual = 0.06 mm</p>"},
   {"label":"Step 3: Calculate","content":"<p>magnification = 24 ÷ 0.06</p>"},
   {"label":"Answer","content":"<p>Magnification = <strong>×400</strong> (no units)</p>","isAnswer":True,"is_answer":True},
  ]},
 {"difficulty":"Silver",
  "question":"An electron microscope image shows a mitochondrion with a drawn length of 60 mm. The magnification is ×12,000. Calculate the actual length in µm.",
  "steps":[
   {"label":"Step 1: Rearrange for actual size","content":"<p>actual = image ÷ magnification = 60 ÷ 12,000 = 0.005 mm</p>"},
   {"label":"Step 2: Convert mm to µm","content":"<p>0.005 mm × 1,000 = 5 µm</p>"},
   {"label":"Answer","content":"<p>Actual length = <strong>5 µm</strong></p>","isAnswer":True,"is_answer":True},
  ]},
 {"difficulty":"Gold",
  "question":"A bacterium has an actual length of 2 µm. At a magnification of ×1,000, calculate the image length in mm.",
  "steps":[
   {"label":"Step 1: Convert actual size to mm","content":"<p>2 µm ÷ 1,000 = 0.002 mm</p>"},
   {"label":"Step 2: Image = actual × magnification","content":"<p>image = 0.002 × 1,000</p>"},
   {"label":"Answer","content":"<p>Image length = <strong>2 mm</strong></p>","isAnswer":True,"is_answer":True},
  ]},
]

pd = {
 "method_card": method_card,
 "topic_links": {"prerequisites": []},
 "exam_context": {
   "marks":"2 to 4 per question",
   "paper":"Biology paper (combined science)",
   "frequency":"Medium to high: magnification questions appear regularly",
 },
 "problem_bank": {
   "gold": gold,
   "bronze": bronze,
   "silver": silver,
   "bronze_description":"One step: divide or multiply once, with both lengths already in the same unit.",
   "silver_description":"Convert the units first, then apply the magnification formula (or rearrange it).",
   "gold_description":"Mixed units and larger scale factors: convert, then find magnification, image or actual size.",
 },
 "related_videos": [],
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": {"opener": opener, "teach": teach},
}

bad = [(v,c) for (v,c) in CHECKS if abs(float(v)-float(c))>1e-9]
assert not bad, ("ARITHMETIC MISMATCH: %r" % bad)
def scan(o,p=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,p+"[%d]"%i)
    elif isinstance(o,str) and "—" in o:
        raise SystemExit("EM DASH at "+p)
scan(pd)
print("checks passed:", len(CHECKS), "boxes verified")
with io.open("lesson_biology-data-skills-L01@dfb8522d32.json","w",encoding="utf-8") as f:
    json.dump(pd,f,ensure_ascii=False,indent=1)
print("written shard")
