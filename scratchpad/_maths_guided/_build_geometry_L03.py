# -*- coding: utf-8 -*-
import json, io, math

PI = math.pi
def r1(x): return round(x, 1)

pd = json.load(io.open("_fresh_geometry_L03_pd.json", encoding="utf-8"))

# ---------- helpers ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def sy(say): return {"say": say}
def mis(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message, "note": note}

# ---------- BRONZE ----------
bronze = []

bronze.append({
 "display": "Find the volume of a cube with side length 6 cm.",
 "solutions": [216], "calculator": False, "input_type": "single_value",
 "hint": "Multiply the side by itself three times: 6 × 6 × 6.",
 "misconceptions": [mis("squared_not_cubed", 36,
   "Stopping at 6 × 6 = 36 gives the area of one square face. A cube's volume needs the third length too: 6 × 6 × 6 = 216 cm³.",
   "Determinate slip: computes 6² not 6³.")],
 "guided_steps": [
   sy("Volume of a cube is side × side × side. The side is 6 cm."),
   box("6 × 6 = ", 36, "Six sixes."),
   box("36 × 6 = ", 216, "Six thirty-sixes.", say="Multiply by the third side of 6.", phase="substitute"),
   box("Check by dividing back: 216 ÷ 36 = ", 6, "216 shared into 36s.",
       done="That returns the side length 6 cm, so 216 cm³ is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "A cuboid is 10 cm × 4 cm × 3 cm. Find its volume.",
 "solutions": [120], "calculator": False, "input_type": "single_value",
 "hint": "Multiply all three dimensions together.",
 "misconceptions": [mis("added_not_multiplied", 17,
   "Adding the three lengths (10 + 4 + 3 = 17) measures edges, not the space inside. Volume multiplies them: 10 × 4 × 3 = 120 cm³.",
   "Determinate slip: adds dimensions.")],
 "guided_steps": [
   sy("Volume of a cuboid is length × width × height: 10 × 4 × 3."),
   box("10 × 4 = ", 40, "Ten fours."),
   box("40 × 3 = ", 120, "Forty threes.", say="Now multiply by the height of 3.", phase="substitute"),
   box("Check: 120 ÷ 3 ÷ 4 = ", 10, "120 ÷ 3 = 40, then 40 ÷ 4.",
       done="That returns the length 10 cm, so 120 cm³ is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "A triangular prism has cross-section area 15 cm² and length 9 cm. Find its volume.",
 "solutions": [135], "calculator": False, "input_type": "single_value",
 "hint": "Multiply the cross-section area by the length.",
 "misconceptions": [mis("area_only", 15,
   "Using just the cross-section area (15 cm²) forgets the prism's length. Multiply by the length: 15 × 9 = 135 cm³.",
   "Determinate slip: cross-section only.")],
 "guided_steps": [
   sy("Volume of a prism is cross-section area × length: 15 × 9."),
   box("Ten lengths would be 10 × 15 = ", 150, "Ten fifteens."),
   box("Take one 15 back off: 150 − 15 = ", 135, "One fifteen fewer than ten.",
       say="Nine lots of 15 is ten lots minus one lot.", phase="substitute"),
   box("Check: 135 ÷ 9 = ", 15, "135 shared into 9s.",
       done="That returns the cross-section area 15 cm², so 135 cm³ is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "A cylinder has radius 3 cm and height 10 cm. Find its volume to 1 d.p.",
 "solutions": [282.7], "calculator": True, "input_type": "single_value",
 "hint": "Square the radius, multiply by the height, then by π.",
 "misconceptions": [mis("used_diameter", 1131.0,
   "Using the diameter (6 cm) in place of the radius: π × 6² × 10 = 360π ≈ 1131.0 cm³. The formula needs the radius (3 cm): π × 9 × 10 = 90π ≈ 282.7 cm³.",
   "Determinate slip: diameter for radius.")],
 "guided_steps": [
   sy("Volume of a cylinder is π × r² × h. Start with r²."),
   box("3 × 3 = ", 9, "Three squared."),
   box("9 × 10 = ", 90, "Nine tens.", say="That is the number in front of π: 90π.", phase="substitute"),
   box("90 × π, to 1 d.p. = ", 282.7, "Type 90 × π and round to one decimal place.", phase="substitute"),
   sy("Check: the base circle has area π × 9 ≈ 28.3 cm², and over height 10 that is about 283 cm³, matching 282.7 cm³."),
 ]})

bronze.append({
 "display": "Find the surface area of a cube with side 5 cm.",
 "solutions": [150], "calculator": False, "input_type": "single_value",
 "hint": "A cube has six identical faces, so find one face area and multiply by 6.",
 "misconceptions": [mis("one_face_only", 25,
   "25 cm² is the area of a single face. A cube has 6 faces, so multiply by 6: 6 × 25 = 150 cm².",
   "Determinate slip: one face only.")],
 "guided_steps": [
   sy("A cube has 6 identical square faces. Each face is 5 × 5."),
   box("5 × 5 = ", 25, "Five squared."),
   box("6 faces: 6 × 25 = ", 150, "Six twenty-fives.", say="There are 6 faces, all the same.", phase="substitute"),
   box("Check: 150 ÷ 6 = ", 25, "150 shared into 6 faces.",
       done="That returns one face area, 25 cm², so 150 cm² is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "A cuboid is 8 cm × 3 cm × 2 cm. Find its surface area.",
 "solutions": [92], "calculator": False, "input_type": "single_value",
 "hint": "Find the three different face areas, add them, then double.",
 "misconceptions": [mis("forgot_double", 46,
   "24 + 16 + 6 = 46 counts each face size only once. Every face has a matching opposite, so double it: 2 × 46 = 92 cm².",
   "Determinate slip: forgets the pairs.")],
 "guided_steps": [
   sy("A cuboid has three different face sizes, each appearing twice. Find the three areas."),
   box("8 × 3 = ", 24, "One face."),
   box("8 × 2 = ", 16, "Another face."),
   box("3 × 2 = ", 6, "The last face."),
   box("Add the three: 24 + 16 + 6 = ", 46, "Sum the three faces.",
       say="These are the three different faces.", phase="substitute"),
   box("Each appears twice: 2 × 46 = ", 92, "Double the total.",
       done="Two of each face makes the whole surface, 92 cm².", phase="substitute"),
 ]})

bronze.append({
 "display": "A cylinder has radius 4 cm and height 7 cm. Find the volume to 1 d.p.",
 "solutions": [351.9], "calculator": True, "input_type": "single_value",
 "hint": "Square the radius, times the height, times π.",
 "misconceptions": [mis("used_diameter", 1407.4,
   "Using the diameter (8 cm) instead of the radius: π × 8² × 7 = 448π ≈ 1407.4 cm³. Halve it to the radius (4 cm): π × 16 × 7 = 112π ≈ 351.9 cm³.",
   "Determinate slip: diameter for radius.")],
 "guided_steps": [
   sy("Volume of a cylinder is π × r² × h. Start with r²."),
   box("4 × 4 = ", 16, "Four squared."),
   box("16 × 7 = ", 112, "Sixteen sevens.", say="That is the number in front of π: 112π.", phase="substitute"),
   box("112 × π, to 1 d.p. = ", 351.9, "Type 112 × π and round to one decimal place.", phase="substitute"),
   sy("Check: base area π × 16 ≈ 50.3 cm², times height 7 ≈ 352 cm³, matching 351.9 cm³."),
 ]})

bronze.append({
 "display": "A fish tank is 40 cm × 25 cm × 30 cm. How many litres of water does it hold?",
 "solutions": [30], "calculator": False, "input_type": "single_value",
 "hint": "Find the volume in cm³, then divide by 1000 to get litres.",
 "misconceptions": [mis("wrong_litre_size", 300,
   "The volume is 40 × 25 × 30 = 30000 cm³. Dividing by 100 gives 300, which treats a litre as 100 cm³. A litre is 1000 cm³, so divide by 1000: 30 litres.",
   "Determinate slip: 1 litre = 100 cm³.")],
 "guided_steps": [
   sy("First find the volume in cm³: length × width × height."),
   box("40 × 25 = ", 1000, "Forty twenty-fives."),
   box("1000 × 30 = ", 30000, "A thousand thirties.", say="So the tank holds 30000 cm³."),
   box("There are 1000 cm³ in 1 litre, so 30000 ÷ 1000 = ", 30, "Divide by a thousand.",
       say="Now change cm³ into litres.", phase="substitute"),
   box("Check: 30 litres × 1000 = ", 30000, "Multiply back by a thousand.",
       done="That returns the volume in cm³, so 30 litres is right.", phase="substitute"),
 ]})

# ---------- SILVER ----------
silver = []

silver.append({
 "display": "Find the volume of a sphere with radius 6 cm to 1 d.p.",
 "solutions": [904.8], "calculator": True, "input_type": "single_value",
 "hint": "Cube the radius, then multiply by four thirds and π.",
 "misconceptions": [mis("used_surface_formula", 452.4,
   "4π × 36 = 144π ≈ 452.4 is the surface area, not the volume. Volume cubes the radius and uses four thirds: (4/3)π × 216 = 288π ≈ 904.8 cm³.",
   "Determinate slip: SA formula for volume.")],
 "guided_steps": [
   sy("Volume of a sphere is (4/3) × π × r³. Start with r³."),
   box("6 × 6 = ", 36, "Six squared."),
   box("36 × 6 = ", 216, "That is r³.", say="Cube means three sixes multiplied."),
   box("(4/3) × 216 = ", 288, "216 ÷ 3 = 72, then × 4.", say="Now apply the four thirds.", phase="substitute"),
   box("288 × π, to 1 d.p. = ", 904.8, "Type 288 × π and round to one decimal place.", phase="substitute"),
   sy("Check: r³ = 216 and (4/3) × 216 = 288, so V = 288π ≈ 904.8 cm³."),
 ]})

silver.append({
 "display": "Find the volume of a cone with radius 5 cm and height 12 cm to 1 d.p.",
 "solutions": [314.2], "calculator": True, "input_type": "single_value",
 "hint": "Square the radius, times height, times a third, times π.",
 "misconceptions": [mis("forgot_third", 942.5,
   "π × 25 × 12 = 300π ≈ 942.5 is a cylinder's volume. A cone is one third of that: (1/3) × 300π = 100π ≈ 314.2 cm³.",
   "Determinate slip: forgets the third.")],
 "guided_steps": [
   sy("Volume of a cone is (1/3) × π × r² × h. Start with r²."),
   box("5 × 5 = ", 25, "Five squared."),
   box("25 × 12 = ", 300, "Twenty-five twelves.", say="That is r² × h."),
   box("Take a third: 300 ÷ 3 = ", 100, "300 shared into 3.", say="A cone is a third of the matching cylinder.", phase="substitute"),
   box("100 × π, to 1 d.p. = ", 314.2, "Type 100 × π and round to one decimal place.", phase="substitute"),
   sy("Check: without the third it would be 300π; a third of that is 100π ≈ 314.2 cm³."),
 ]})

silver.append({
 "display": "A cylinder has volume 500 cm³ and radius 5 cm. Find the height to 1 d.p.",
 "solutions": [6.4], "calculator": True, "input_type": "single_value",
 "hint": "Rearrange V = πr²h to h = V ÷ (πr²).",
 "misconceptions": [mis("divided_by_r", 31.8,
   "Dividing by the radius instead of its square: 500 ÷ (5π) ≈ 31.8. The formula has r², so divide by π × 25: 500 ÷ (25π) ≈ 6.4 cm.",
   "Determinate slip: divides by r not r².")],
 "guided_steps": [
   sy("V = π × r² × h, so rearrange to h = V ÷ (π × r²). First find π × r²."),
   box("5 × 5 = ", 25, "Five squared."),
   box("π × 25, to 2 d.p. = ", 78.54, "Type π × 25 and round to two decimal places.",
       say="That is the whole base-times-π amount.", phase="substitute"),
   box("h = 500 ÷ 78.54, to 1 d.p. = ", 6.4, "Volume divided by the base amount.", phase="substitute"),
   sy("Check: π × 25 × 6.366 = 500 exactly; rounding the height to 6.4 explains the tiny gap, so h ≈ 6.4 cm is right."),
 ]})

silver.append({
 "display": "Find the curved surface area of a cone with radius 4 cm and slant height 9 cm. Give your answer to 1 d.p.",
 "solutions": [113.1], "calculator": True, "input_type": "single_value",
 "hint": "Curved surface of a cone is π × radius × slant height.",
 "misconceptions": [mis("used_cylinder_curved", 226.2,
   "2π × 4 × 9 = 72π ≈ 226.2 is a cylinder's curved surface. A cone's is π × r × l with no 2: π × 4 × 9 = 36π ≈ 113.1 cm².",
   "Determinate slip: cylinder curved SA.")],
 "guided_steps": [
   sy("Curved surface area of a cone is π × r × l. Multiply r and l first."),
   box("4 × 9 = ", 36, "Four nines.", say="That is the number in front of π: 36π."),
   box("36 × π, to 1 d.p. = ", 113.1, "Type 36 × π and round to one decimal place.", phase="substitute"),
   box("Check: 113.1 ÷ π, to the nearest whole number = ", 36, "Divide the answer back by π.",
       done="That returns 36, which is r × l = 4 × 9, so 113.1 cm² is right.", phase="substitute"),
 ]})

silver.append({
 "display": "Find the surface area of a sphere with radius 4 cm to 1 d.p.",
 "solutions": [201.1], "calculator": True, "input_type": "single_value",
 "hint": "Square the radius, then multiply by 4 and π.",
 "misconceptions": [mis("used_circle_area", 50.3,
   "π × 4² = 16π ≈ 50.3 is the area of a flat circle. A sphere's surface is 4 times that: 4π × 16 = 64π ≈ 201.1 cm².",
   "Determinate slip: circle area, not sphere.")],
 "guided_steps": [
   sy("Surface area of a sphere is 4 × π × r². Start with r²."),
   box("4 × 4 = ", 16, "Four squared."),
   box("4 × 16 = ", 64, "Four sixteens.", say="That is the number in front of π: 64π.", phase="substitute"),
   box("64 × π, to 1 d.p. = ", 201.1, "Type 64 × π and round to one decimal place.", phase="substitute"),
   sy("Check: 201.1 ÷ π ≈ 64, which is 4 × 16, so 201.1 cm² is right."),
 ]})

silver.append({
 "display": "A pyramid has square base 6 cm × 6 cm and height 10 cm. Find its volume.",
 "solutions": [120], "calculator": False, "input_type": "single_value",
 "hint": "A third of base area times height.",
 "misconceptions": [mis("forgot_third", 360,
   "36 × 10 = 360 would be a prism with that base. A pyramid is one third of it: (1/3) × 360 = 120 cm³.",
   "Determinate slip: forgets the third.")],
 "guided_steps": [
   sy("Volume of a pyramid is (1/3) × base area × height. Find the base area first."),
   box("6 × 6 = ", 36, "Six squared for the square base."),
   box("36 × 10 = ", 360, "Base area times height.", say="That is base area × height."),
   box("Take a third: 360 ÷ 3 = ", 120, "360 shared into 3.", say="A pyramid is a third of that box.", phase="substitute"),
   box("Check: 120 × 3 = ", 360, "Multiply back by 3.",
       done="That returns base area × height = 36 × 10, so 120 cm³ is right.", phase="substitute"),
 ]})

silver.append({
 "display": "A hemisphere has radius 8 cm. Find its volume to the nearest whole number.",
 "solutions": [1072], "calculator": True, "input_type": "single_value",
 "hint": "A hemisphere is two thirds of πr³.",
 "misconceptions": [mis("used_full_sphere", 2145,
   "(4/3)π × 512 ≈ 2145 is a whole sphere. A hemisphere is half of that, or two thirds of πr³: (2/3)π × 512 ≈ 1072 cm³.",
   "Determinate slip: full sphere.")],
 "guided_steps": [
   sy("A hemisphere is half a sphere, so its volume is (2/3) × π × r³. Start with r³."),
   box("8 × 8 = ", 64, "Eight squared."),
   box("64 × 8 = ", 512, "That is r³.", say="Cube means three eights multiplied."),
   box("(2/3) × 512, to 2 d.p. = ", 341.33, "512 ÷ 3 = 170.67, then × 2.",
       say="Apply the two thirds.", phase="substitute"),
   box("341.33 × π, to the nearest whole number = ", 1072, "Type 341.33 × π and round.", phase="substitute"),
   sy("Check: a full sphere would be (4/3)π × 512 ≈ 2145 cm³; a hemisphere is half of that, ≈ 1072 cm³."),
 ]})

# ---------- GOLD ----------
gold = []

gold.append({
 "display": "A sphere has volume \\(288\\pi\\) cm³. Find the radius.",
 "solutions": [6], "calculator": False, "input_type": "single_value",
 "hint": "Cancel the π, then rearrange (4/3)r³ = 288 and cube root.",
 "misconceptions": [mis("skipped_four_thirds", 6.6,
   "Taking r³ = 288 straight from 288π ignores the four thirds. Cancel π then multiply by 3/4: r³ = 288 × 3/4 = 216, so r = 6 cm. r = ∛288 ≈ 6.6 is the slip.",
   "Determinate slip: r = cube root of 288.")],
 "guided_steps": [
   sy("Volume of a sphere is (4/3)πr³, and here it equals 288π. The π cancels, so (4/3)r³ = 288, giving r³ = 288 × (3/4)."),
   box("288 × 3 = ", 864, "Three lots of 288."),
   box("864 ÷ 4 = ", 216, "864 shared into 4.", say="So r³ = 216.", phase="substitute"),
   box("The cube root: r = ∛216 = ", 6, "What cubed gives 216? Try 6 × 6 × 6.", phase="substitute"),
   sy("Check: 6³ = 216 and (4/3) × 216 = 288, so the volume is 288π. The radius is 6 cm."),
 ]})

gold.append({
 "display": "A cone and a cylinder have the same base radius (5 cm) and the same height (12 cm). Find the difference in their volumes to 1 d.p.",
 "solutions": [628.3], "calculator": True, "input_type": "single_value",
 "hint": "The difference is two thirds of the cylinder's volume.",
 "misconceptions": [mis("cone_as_cylinder", 0,
   "Treating the cone as a cylinder makes both 300π, so the difference looks like 0. The cone is only one third, 100π, so the difference is 300π − 100π = 200π ≈ 628.3 cm³.",
   "Determinate slip: cone = cylinder.")],
 "guided_steps": [
   sy("Cylinder volume is πr²h; the cone is one third of it, so the difference is two thirds of the cylinder. First find r²h."),
   box("5 × 5 = ", 25, "Five squared."),
   box("25 × 12 = ", 300, "Twenty-five twelves.", say="Cylinder = 300π, cone = 100π."),
   box("Two thirds of that: (2/3) × 300 = ", 200, "300 ÷ 3 = 100, then × 2.",
       say="The gap is the cylinder minus the cone.", phase="substitute"),
   box("200 × π, to 1 d.p. = ", 628.3, "Type 200 × π and round to one decimal place.", phase="substitute"),
   sy("Check: cylinder = 300π, cone = 100π, difference = 200π ≈ 628.3 cm³."),
 ]})

gold.append({
 "display": "A solid hemisphere of radius 4 cm sits on top of a cylinder of radius 4 cm and height 10 cm. Find the total volume to 1 d.p.",
 "solutions": [636.7], "calculator": True, "input_type": "single_value",
 "hint": "Add the cylinder volume and the hemisphere volume.",
 "misconceptions": [mis("used_full_sphere", 770.7,
   "Adding a whole sphere instead of a hemisphere: 160π + (4/3)π × 64 = 160π + (256/3)π ≈ 770.7. A hemisphere is two thirds of πr³, giving 160π + (128/3)π ≈ 636.7 cm³.",
   "Determinate slip: full sphere on top.")],
 "guided_steps": [
   sy("Add two volumes. Cylinder = πr²h; hemisphere = (2/3)πr³. Find each number in front of π."),
   box("Cylinder: 4 × 4 × 10 = ", 160, "Square the radius, times the height.", say="Cylinder = 160π."),
   box("Hemisphere: r³ = 4 × 4 × 4 = ", 64, "Cube the radius."),
   box("(2/3) × 64, to 2 d.p. = ", 42.67, "64 ÷ 3 = 21.33, then × 2.", say="Hemisphere ≈ 42.67π."),
   box("Add the two: 160 + 42.67 = ", 202.67, "Sum the numbers in front of π.",
       say="Now combine the coefficients of π.", phase="substitute"),
   box("202.67 × π, to 1 d.p. = ", 636.7, "Type 202.67 × π and round to one decimal place.", phase="substitute"),
   sy("Check: 160π ≈ 502.7 and 42.67π ≈ 134.0; 502.7 + 134.0 ≈ 636.7 cm³."),
 ]})

gold.append({
 "display": "A sphere has surface area \\(100\\pi\\) cm². Find the radius.",
 "solutions": [5], "calculator": False, "input_type": "single_value",
 "hint": "Cancel the π, solve 4r² = 100, then square root.",
 "misconceptions": [mis("forgot_square_root", 25,
   "Stopping at r² = 25 gives 25, but the question wants r. Take the square root: r = √25 = 5 cm.",
   "Determinate slip: forgets the square root.")],
 "guided_steps": [
   sy("Surface area of a sphere is 4πr², and here it equals 100π. The π cancels, so 4r² = 100, giving r² = 100 ÷ 4."),
   box("100 ÷ 4 = ", 25, "A hundred shared into 4.", say="So r² = 25."),
   box("The square root: r = √25 = ", 5, "What squared gives 25?", phase="substitute"),
   box("Check: 4 × 5² = 4 × ", 25, "Square the 5 again.",
       done="4 × 25 = 100, so the surface is 100π, and r = 5 cm is right.", phase="substitute"),
 ]})

gold.append({
 "display": "A frustum is formed by removing a cone of height 4 cm and radius 2 cm from a cone of height 12 cm and radius 6 cm. Find the volume of the frustum to 1 d.p.",
 "solutions": [435.6], "calculator": True, "input_type": "single_value",
 "hint": "Big cone volume minus small cone volume.",
 "misconceptions": [mis("forgot_small_cone", 452.4,
   "144π ≈ 452.4 is just the large cone. The frustum removes the small cone (16π/3): 144π − 16π/3 = 416π/3 ≈ 435.6 cm³.",
   "Determinate slip: large cone only.")],
 "guided_steps": [
   sy("The frustum is the big cone minus the small cone. Volume of a cone is (1/3)πr²h. Find each number in front of π."),
   box("Big cone r²h: 36 × 12 = ", 432, "Square 6, times 12."),
   box("A third: 432 ÷ 3 = ", 144, "432 shared into 3.", say="Big cone = 144π."),
   box("Small cone r²h: 4 × 4 = ", 16, "Square 2, times 4."),
   box("A third: 16 ÷ 3, to 2 d.p. = ", 5.33, "16 shared into 3.", say="Small cone ≈ 5.33π."),
   box("Subtract: 144 − 5.33 = ", 138.67, "Big minus small.",
       say="The frustum is what is left after removing the tip.", phase="substitute"),
   box("138.67 × π, to 1 d.p. = ", 435.6, "Type 138.67 × π and round to one decimal place.", phase="substitute"),
   sy("Check: big cone 144π ≈ 452.4, small cone 5.33π ≈ 16.8; 452.4 − 16.8 ≈ 435.6 cm³."),
 ]})

# ---------- assemble problem_bank ----------
pd["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Put numbers straight into a volume or surface-area formula for a cube, cuboid, prism or cylinder.",
  "silver_description": "Curved shapes and reverse problems: handle the π, the one-third or four-thirds factor, or rearrange to find a missing length.",
  "gold_description": "Work backwards from a volume given in terms of π, or combine and subtract solids like frustums and compound shapes.",
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: put numbers into the formula",
  "steps": [
   "Name the solid, then pick its formula. A cuboid is length × width × height, a prism is cross-section area × length, a cylinder is \\(\\pi r^2 h\\).",
   "Substitute the numbers and multiply carefully, squaring or cubing where the formula says so.",
   "For surface area add up every face: a cube has 6 equal faces, a cuboid has three pairs. Give volume in cm³ and area in cm²."
  ],
  "example": {"question": "Find the volume of a cuboid 5 cm × 4 cm × 2 cm.", "steps": [
    {"label": "Formula", "content": "<p>\\(V = l \\times w \\times h\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(5 \\times 4 \\times 2 = 40\\)</p>"},
    {"label": "Check", "content": "<p>\\(40 \\div 2 \\div 4 = 5\\), the original length.</p>"},
    {"label": "Answer", "content": "<p>\\(40\\) cm³</p>", "isAnswer": True, "is_answer": True},
  ]}},
 "silver": {
  "title": "Silver: curved shapes and reverse problems",
  "steps": [
   "Now the formula carries a \\(\\pi\\) and often a fraction: cone \\(\\tfrac{1}{3}\\pi r^2 h\\), sphere \\(\\tfrac{4}{3}\\pi r^3\\), hemisphere two thirds of \\(\\pi r^3\\).",
   "Work out the number in front of \\(\\pi\\) first, then multiply by \\(\\pi\\) at the end and round as asked.",
   "For a reverse problem (a volume is given, find a length) rearrange the formula first, for example \\(h = V \\div (\\pi r^2)\\)."
  ],
  "example": {"question": "Find the volume of a cone with radius 3 cm and height 8 cm to 1 d.p.", "steps": [
    {"label": "Formula", "content": "<p>\\(V = \\tfrac{1}{3}\\pi r^2 h\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(\\tfrac{1}{3} \\times 9 \\times 8 = 24\\), so \\(V = 24\\pi\\)</p>"},
    {"label": "Check", "content": "<p>\\(24 \\times \\pi = 75.398\\ldots\\)</p>"},
    {"label": "Answer", "content": "<p>\\(75.4\\) cm³</p>", "isAnswer": True, "is_answer": True},
  ]}},
 "gold": {
  "title": "Gold: work backwards and combine solids",
  "steps": [
   "When a volume is given as a multiple of \\(\\pi\\) (like \\(288\\pi\\)), cancel the \\(\\pi\\) on both sides, rearrange, then take a square or cube root to find the length.",
   "For compound solids work out each part separately and add them; for a frustum, subtract the small cone from the large one.",
   "Keep \\(\\pi\\) as a symbol while you can, and only turn it into a decimal at the final step."
  ],
  "example": {"question": "A sphere has volume 36π cm³. Find the radius.", "steps": [
    {"label": "Cancel π", "content": "<p>\\(\\tfrac{4}{3}r^3 = 36\\), so \\(r^3 = 36 \\times \\tfrac{3}{4} = 27\\)</p>"},
    {"label": "Cube root", "content": "<p>\\(r = \\sqrt[3]{27} = 3\\)</p>"},
    {"label": "Check", "content": "<p>\\(\\tfrac{4}{3} \\times 27 = 36\\), so the volume is \\(36\\pi\\).</p>"},
    {"label": "Answer", "content": "<p>\\(r = 3\\) cm</p>", "isAnswer": True, "is_answer": True},
  ]}},
}

# ---------- guided (opener + teach) ----------
pd["guided"] = {
 "opener": {
  "label": "Before any formula",
  "display": "A box is 3 cm long, 2 cm wide and 2 cm tall.<br>You fill it with 1 cm sugar cubes.",
  "steps": [
   box("The bottom layer is 3 long and 2 wide. How many cubes cover it? ", 6,
       "Three rows of two, or two rows of three.",
       say="No formula needed. Picture the bottom layer of cubes first."),
   box("The box is 2 cubes tall, so how many cubes in total? ", 12,
       "Two layers of six.",
       say="Now stack the layers up to the top."),
   sy("You just found the <strong>volume</strong>: 12 cm³. Counting one layer then stacking it is exactly length × width × height, \\(3 \\times 2 \\times 2 = 12\\). Every volume formula is this same idea of filling space, whether the shape is a box, a cylinder or a sphere."),
  ]},
 "teach": {
  "bronze": {
   "display": "Find the volume of a cuboid 5 cm × 4 cm × 2 cm.",
   "label": "Together: your first one",
   "steps": [
    box("5 × 4 = ", 20, "Five fours.", say="Volume of a cuboid is length × width × height. Just multiply the three numbers."),
    box("20 × 2 = ", 40, "Twenty twos.", say="Now multiply by the height of 2.", done="So the volume is 40 cm³."),
    box("Check: 40 ÷ 2 = ", 20, "Undo the last multiply."),
    box("and 20 ÷ 4 = ", 5, "Undo the width.", done="That returns the length 5 cm, so 40 cm³ is right."),
   ]},
  "silver": {
   "display": "Find the volume of a cone with radius 3 cm and height 8 cm to 1 d.p.",
   "label": "Together: the silver move",
   "steps": [
    box("3 × 3 = ", 9, "Three squared.", say="A cone brings in two new things: a \\(\\pi\\) and a factor of one third. Volume = \\(\\tfrac{1}{3}\\pi r^2 h\\). Start with r²."),
    box("9 × 8 = ", 72, "Nine eights.", say="That is r² × h."),
    box("A third: 72 ÷ 3 = ", 24, "72 shared into 3.", say="A cone is a third of the matching cylinder.", done="So V = 24π."),
    box("24 × π, to 1 d.p. = ", 75.4, "Type 24 × π and round to one decimal place.", done="Gone. The third and the π were the whole point."),
   ]},
  "gold": {
   "display": "A sphere has volume \\(36\\pi\\) cm³. Find the radius.",
   "label": "Together: the gold move",
   "steps": [
    box("36 × 3 = ", 108, "Three lots of 36.", say="This time the volume is given and we work backwards. \\(\\tfrac{4}{3}\\pi r^3 = 36\\pi\\). Cancel \\(\\pi\\): \\(\\tfrac{4}{3}r^3 = 36\\), so \\(r^3 = 36 \\times \\tfrac{3}{4}\\)."),
    box("108 ÷ 4 = ", 27, "108 shared into 4.", say="So r³ = 27."),
    box("Cube root: r = ∛27 = ", 3, "What cubed gives 27?"),
    box("Check: (4/3) × 27 = ", 36, "27 ÷ 3 = 9, then × 4.", done="That gives 36π, the volume we started with, so r = 3 cm."),
   ]},
 }
}

# ---------- method_card (slim) ----------
pd["method_card"] = {
 "title": "Volume & Surface Area",
 "steps": [
  "Name the solid and pick its formula.",
  "Substitute the numbers and multiply.",
  "Work the \\(\\pi\\) part last, then round as asked.",
  "Add or subtract parts for compound solids."
 ],
 "content": "<p>Pick the solid, use its formula, substitute, and keep the units (cm³ for volume, cm² for area).</p><p>Cuboid \\(V = lwh\\). Prism \\(V = \\text{area} \\times \\text{length}\\). Cylinder \\(V = \\pi r^2 h\\). Cone \\(V = \\tfrac{1}{3}\\pi r^2 h\\), curved SA \\(= \\pi r l\\). Sphere \\(V = \\tfrac{4}{3}\\pi r^3\\), SA \\(= 4\\pi r^2\\). Pyramid \\(V = \\tfrac{1}{3} \\times \\text{base} \\times h\\). A hemisphere is half a sphere.</p><p>For compound solids add or subtract simpler shapes. To find a missing length from a given volume, rearrange first.</p>",
 "example": "<p><strong>Find the volume of a cylinder with radius 4 cm and height 10 cm.</strong></p><p>\\(V = \\pi \\times 4^2 \\times 10 = 160\\pi \\approx 502.7\\) cm³</p>"
}

# ---------- VERIFY final boxes land on solutions ----------
def last_answer(gs):
    vals = [s["answer"] for s in gs if s.get("answer") is not None]
    return vals

# independent recompute of every 1-d.p./round answer used in boxes
checks = {
 "B3": r1(90*PI)==282.7, "B6": r1(112*PI)==351.9,
 "S0": r1(288*PI)==904.8, "S1": r1(100*PI)==314.2,
 "S2a": round(PI*25,2)==78.54, "S2b": r1(500/78.54)==6.4,
 "S3": r1(36*PI)==113.1, "S4": r1(64*PI)==201.1,
 "S6a": round((2/3)*512,2)==341.33, "S6b": round(341.33*PI)==1072,
 "G1": r1(200*PI)==628.3, "G2b": round(202.67*PI,1)==636.7,
 "G4b": r1(138.67*PI)==435.6,
 "teachS": r1(24*PI)==75.4,
}
for k,v in checks.items():
    assert v, f"recompute FAILED {k}"

# check misconception expects are recomputable
assert r1(360*PI)==1131.0
assert r1(448*PI)==1407.4
assert r1(144*PI)==452.4
assert r1(300*PI)==942.5
assert r1(500/(5*PI))==31.8
assert r1(72*PI)==226.2
assert r1(16*PI)==50.3
assert round((4/3)*PI*512)==2145
assert round(math.pow(288,1/3),1)==6.6
assert r1((160+256/3)*PI)==770.7

json.dump(pd, io.open("lesson_geometry-L03.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE lesson_geometry-L03.json")
print("all recompute assertions passed")
