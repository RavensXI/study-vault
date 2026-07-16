# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_geometry-L02.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": "common", "expect": expect, "message": message, "note": note}

# ---------------- BRONZE ----------------
bronze = []

bronze.append({
 "display": "Find the area of a rectangle with length 9 cm and width 5 cm.",
 "solutions": [45], "calculator": False, "input_type": "single_value",
 "hint": "Multiply length by width; do not add the sides.",
 "misconceptions": [
   mc("wrong_formula", 28,
      "It looks like you found the perimeter, 2 × (9 + 5) = 28 cm. Area is different: multiply the sides, 9 × 5 = 45 cm².",
      "Student uses perimeter 2(9+5)=28 instead of area.")
 ],
 "guided_steps": [
   sayonly("Area of a rectangle is length × width. Just multiply the two sides, nothing else."),
   box("Write the calculation, length × width = 9 × ", 5, "The width, straight from the question."),
   box("Now work it out: 9 × 5 = ", 45, "Multiply the two numbers.", phase="substitute"),
   box("Check by dividing back: 45 ÷ 9 = ", 5, "It should give the width you started with.", done="That returns the width, 5 cm, so 45 cm² is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the perimeter of a rectangle with length 12 cm and width 7 cm.",
 "solutions": [38], "calculator": False, "input_type": "single_value",
 "hint": "Add a length and a width, then double.",
 "misconceptions": [
   mc("wrong_formula", 19,
      "It looks like you added just one length and one width. A rectangle has two of each, so double it: 2 × (12 + 7) = 38 cm.",
      "Student adds one length and one width (12+7=19) without doubling.")
 ],
 "guided_steps": [
   sayonly("Perimeter is the distance all the way round. For a rectangle, add a length and a width, then double."),
   box("First add one length and one width: 12 + 7 = ", 19, "Just add the two given sides."),
   box("Now double it, because there are two lengths and two widths: 19 × 2 = ", 38, "Multiply by 2.", phase="substitute"),
   box("Check by adding all four sides: 12 + 7 + 12 + 7 = ", 38, "Add every side separately.", done="Same answer, so 38 cm is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the area of a triangle with base 10 cm and height 6 cm.",
 "solutions": [30], "calculator": False, "input_type": "single_value",
 "hint": "Base times height, then halve.",
 "misconceptions": [
   mc("forgot_step", 60,
      "That is base × height. A triangle is only half of that, so halve it: ½ × 10 × 6 = 30 cm².",
      "Student omits the half: 10x6=60.")
 ],
 "guided_steps": [
   sayonly("Area of a triangle is half of base × height."),
   box("First multiply base × height: 10 × 6 = ", 60, "Multiply the two given numbers."),
   box("Now halve it, because a triangle is half a rectangle: 60 ÷ 2 = ", 30, "Divide by 2.", phase="substitute"),
   box("Check by doubling back: 30 × 2 = ", 60, "Should give base × height again.", done="That returns base × height (60), so 30 cm² is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the area of a parallelogram with base 8 cm and height 5 cm.",
 "solutions": [40], "calculator": False, "input_type": "single_value",
 "hint": "Base times height, and do not halve (it is not a triangle).",
 "misconceptions": [
   mc("wrong_formula", 20,
      "It looks like you halved, as for a triangle. A parallelogram is not halved: area = base × height = 8 × 5 = 40 cm².",
      "Student applies triangle half: 1/2 x 8 x 5 = 20.")
 ],
 "guided_steps": [
   sayonly("Area of a parallelogram is base × perpendicular height. No halving, unlike a triangle."),
   box("Write the calculation, base × height = 8 × ", 5, "The height, straight from the question."),
   box("Now work it out: 8 × 5 = ", 40, "Multiply.", phase="substitute"),
   box("Check by dividing back: 40 ÷ 8 = ", 5, "Should give the height.", done="That returns the height, 5 cm, so 40 cm² is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the circumference of a circle with diameter 14 cm. Give your answer to 1 d.p.",
 "solutions": [44.0], "calculator": True, "input_type": "single_value",
 "hint": "Circumference is π times the diameter; the diameter is already given.",
 "misconceptions": [
   mc("wrong_formula", 22.0,
      "It looks like you used the radius (half of 14). Circumference uses the whole diameter: π × 14 ≈ 44.0 cm.",
      "Student uses radius 7 instead of diameter 14: pi x 7 = 22.0.")
 ],
 "guided_steps": [
   sayonly("Circumference is π × diameter. The diameter is given, so there is no halving here."),
   box("Multiply the diameter by π: 14 × π = ", 43.98, "Type 14 × π. It gives 43.98..."),
   box("Round to 1 decimal place: 43.98 rounds to ", 44.0, "The second decimal is 8, so the first decimal rounds up.", phase="substitute"),
   box("Sense check: the circumference is a bit over 3 diameters, and 3 × 14 = ", 42, "Multiply the diameter by 3.", done="44.0 is just above 42, exactly what π (a little over 3) gives, so it is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the area of a circle with radius 5 cm. Give your answer to 1 d.p.",
 "solutions": [78.5], "calculator": True, "input_type": "single_value",
 "hint": "Square the radius first, then multiply by π.",
 "misconceptions": [
   mc("wrong_formula", 15.7,
      "It looks like you multiplied π by the radius. Area needs the radius squared: π × 5² = π × 25 ≈ 78.5 cm².",
      "Student forgets to square: pi x 5 = 15.7.")
 ],
 "guided_steps": [
   sayonly("Area of a circle is π × radius². Square the radius first, then multiply by π."),
   box("Square the radius: 5² = 5 × 5 = ", 25, "Multiply the radius by itself."),
   box("Now multiply by π and round to 1 d.p.: 25 × π = ", 78.5, "Type 25 × π. It gives 78.53...", phase="substitute"),
   box("Sense check: without π it would be 25, and π is a bit over 3, so 3 × 25 = ", 75, "Multiply.", done="The real area uses π, so it is just over 75: 78.5 cm² fits.", phase="substitute"),
 ]})

bronze.append({
 "display": "Find the area of a trapezium with parallel sides 5 cm and 9 cm and height 6 cm.",
 "solutions": [42], "calculator": False, "input_type": "single_value",
 "hint": "Add the parallel sides, times the height, then halve.",
 "misconceptions": [
   mc("wrong_formula", 84,
      "That is (sum of parallel sides) × height. The trapezium formula halves it: ½ × (5 + 9) × 6 = 42 cm².",
      "Student omits the half: (5+9)x6 = 84.")
 ],
 "guided_steps": [
   sayonly("Area of a trapezium is half of (the two parallel sides added) × height."),
   box("Add the parallel sides: 5 + 9 = ", 14, "Add the two parallel sides."),
   box("Multiply by the height: 14 × 6 = ", 84, "Multiply by 6."),
   box("Now halve it: 84 ÷ 2 = ", 42, "Divide by 2.", phase="substitute"),
   box("Check by doubling back: 42 × 2 = ", 84, "Should give 84 again.", done="That returns (sum of sides) × height, so 42 cm² is right.", phase="substitute"),
 ]})

bronze.append({
 "display": "A square has perimeter 48 cm. Find its area.",
 "solutions": [144], "calculator": False, "input_type": "single_value",
 "hint": "Divide the perimeter by 4 for the side, then square it.",
 "misconceptions": [
   mc("wrong_formula", 48,
      "It looks like you gave the perimeter as the area. First find one side, 48 ÷ 4 = 12 cm, then square it: 12² = 144 cm².",
      "Student reports perimeter 48 as the area."),
   mc("wrong_formula", 2304,
      "It looks like you squared the whole perimeter. Find one side first, 48 ÷ 4 = 12 cm, then square that: 12² = 144 cm².",
      "Student squares the perimeter: 48^2 = 2304.")
 ],
 "guided_steps": [
   sayonly("Two steps. A square has four equal sides, so first find one side, then square it for the area."),
   box("Find one side: 48 ÷ 4 = ", 12, "Divide the perimeter by 4."),
   box("Now the area: square the side, 12² = 12 × 12 = ", 144, "Multiply the side by itself.", phase="substitute"),
   box("Check the side: √144 = ", 12, "What squares to give 144?", done="That returns the side, 12 cm, so 144 cm² is right.", phase="substitute"),
 ]})

# ---------------- SILVER ----------------
silver = []

silver.append({
 "display": "Find the area of a circle with diameter 18 cm. Give your answer to 1 d.p.",
 "solutions": [254.5], "calculator": True, "input_type": "single_value",
 "hint": "Halve the diameter to get the radius before using π r squared.",
 "misconceptions": [
   mc("wrong_formula", 1017.9,
      "It looks like you used the diameter (18) as the radius. Halve it first: r = 9, then A = π × 9² ≈ 254.5 cm².",
      "Student uses diameter as radius: pi x 18^2 = 1017.9.")
 ],
 "guided_steps": [
   sayonly("The diameter is given, but the area formula needs the radius. Halve the diameter first."),
   box("Halve the diameter: 18 ÷ 2 = ", 9, "Radius is half the diameter."),
   box("Square the radius: 9² = ", 81, "9 × 9."),
   box("Multiply by π and round to 1 d.p.: 81 × π = ", 254.5, "Type 81 × π. It gives 254.46...", phase="substitute"),
   box("Check the radius came from the diameter: 9 × 2 = ", 18, "Double the radius.", done="That returns the diameter, 18 cm, so using r = 9 was right and the area is 254.5 cm².", phase="substitute"),
 ]})

silver.append({
 "display": "A circle has circumference 31.4 cm. Find the radius to 1 d.p. (Use \\(\\pi = 3.14\\))",
 "solutions": [5.0], "calculator": True, "input_type": "single_value",
 "hint": "Divide the circumference by 2π to get the radius.",
 "misconceptions": [
   mc("wrong_formula", 10.0,
      "It looks like you divided by π only, which gives the diameter. The radius needs dividing by 2π: 31.4 ÷ 6.28 = 5.0 cm.",
      "Student divides by pi only: 31.4/3.14 = 10 (diameter).")
 ],
 "guided_steps": [
   sayonly("Circumference is 2 × π × radius. Here the circumference is known, so work backwards to the radius."),
   box("First find 2 × π: 2 × 3.14 = ", 6.28, "Double 3.14."),
   box("Divide the circumference by that: 31.4 ÷ 6.28 = ", 5, "Divide to undo the multiplication.", phase="substitute"),
   box("Check by working forwards: 2 × 3.14 × 5 = ", 31.4, "Multiply back: 6.28 × 5.", done="That returns the circumference, so the radius is 5.0 cm.", phase="substitute"),
 ]})

silver.append({
 "display": "An L-shaped room can be split into a rectangle measuring 8 m by 4 m and another rectangle measuring 3 m by 5 m. Find the total floor area.",
 "solutions": [47], "calculator": False, "input_type": "single_value",
 "hint": "Find each rectangle's area, then add them.",
 "misconceptions": [
   mc("wrong_formula", None,
      "Split the L into two rectangles: 8 × 4 = 32 and 3 × 5 = 15. Add them: 32 + 15 = 47 m².",
      "Compound addition has no single determinate wrong answer, so expect is null.")
 ],
 "guided_steps": [
   sayonly("Split the L into two rectangles, find each area, then add."),
   box("First rectangle: 8 × 4 = ", 32, "Multiply its two sides."),
   box("Second rectangle: 3 × 5 = ", 15, "Multiply its two sides."),
   box("Add the two areas: 32 + 15 = ", 47, "Add them.", phase="substitute"),
   box("Check by subtracting one back: 47 − 15 = ", 32, "Should give the first area, 32.", done="That returns the first rectangle's area, so 47 m² is right.", phase="substitute"),
 ]})

silver.append({
 "display": "Find the area of a quarter circle with radius 10 cm. Give your answer to 1 d.p.",
 "solutions": [78.5], "calculator": True, "input_type": "single_value",
 "hint": "Find the full circle area, then take a quarter.",
 "misconceptions": [
   mc("wrong_formula", 314.2,
      "It looks like you found the whole circle. This is a quarter, so divide by 4: (π × 10²) ÷ 4 ≈ 78.5 cm².",
      "Student uses full circle: pi x 100 = 314.2.")
 ],
 "guided_steps": [
   sayonly("A quarter circle is one quarter of a full circle. Take the quarter before the π so the numbers stay tidy."),
   box("Square the radius: 10² = ", 100, "10 × 10."),
   box("Take a quarter: 100 ÷ 4 = ", 25, "Divide by 4."),
   box("Multiply by π and round to 1 d.p.: 25 × π = ", 78.5, "Type 25 × π. It gives 78.53...", phase="substitute"),
   box("Check by scaling back to a full circle: 78.5 × 4 = ", 314, "Multiply by 4.", done="That is π × 100, the whole circle (≈ 314), so the quarter 78.5 cm² is right.", phase="substitute"),
 ]})

silver.append({
 "display": "A trapezium has area 60 cm², parallel sides 8 cm and 12 cm. Find the height.",
 "solutions": [6], "calculator": False, "input_type": "single_value",
 "hint": "Halve the sum of the parallel sides, then divide the area by that.",
 "misconceptions": [
   mc("wrong_formula", 3.0,
      "It looks like you left out the half. The formula is area = ½ × (8 + 12) × h, so 60 = 10h and h = 6 cm.",
      "Student omits half when rearranging: 60/(8+12) = 3.")
 ],
 "guided_steps": [
   sayonly("Use the trapezium formula backwards. Area = half × (sum of parallel sides) × height, and the height is missing."),
   box("Add the parallel sides: 8 + 12 = ", 20, "Add the two parallel sides."),
   box("Half of that: 20 ÷ 2 = ", 10, "Halve it."),
   box("So area = 10 × height. Divide to find the height: 60 ÷ 10 = ", 6, "Divide the area by 10.", phase="substitute"),
   box("Check by working forwards: 10 × 6 = ", 60, "Should give 60.", done="That returns the area, 60 cm², so the height is 6 cm.", phase="substitute"),
 ]})

silver.append({
 "display": "Find the perimeter of a semicircle with radius 7 cm. Give your answer to 1 d.p.",
 "solutions": [36.0], "calculator": True, "input_type": "single_value",
 "hint": "Add the curved half-circumference to the straight diameter.",
 "misconceptions": [
   mc("wrong_formula", 22.0,
      "It looks like you found only the curved edge (π × 7 ≈ 22.0). A semicircle's perimeter also includes the straight diameter, 14 cm: total ≈ 36.0 cm.",
      "Student forgets the diameter: only pi r = 22.0.")
 ],
 "guided_steps": [
   sayonly("A semicircle's perimeter is the curved half PLUS the straight diameter across the middle. Both parts matter."),
   box("The straight edge is the diameter: 2 × 7 = ", 14, "Diameter is twice the radius."),
   box("The curved edge is half the circumference: π × 7, to 1 d.p. = ", 22.0, "Type 7 × π. It gives 21.99..."),
   box("Add the two parts: 14 + 22 = ", 36, "Add the straight and curved parts.", phase="substitute"),
   box("Check the straight edge: half of the diameter, 14 ÷ 2 = ", 7, "Halve the diameter.", done="That returns the radius, 7 cm, so the perimeter 36.0 cm is right.", phase="substitute"),
 ]})

silver.append({
 "display": "The area of a circle is 50.3 cm². Find the radius to 1 d.p.",
 "solutions": [4.0], "calculator": True, "input_type": "single_value",
 "hint": "Divide the area by π, then square-root to get the radius.",
 "misconceptions": [
   mc("wrong_formula", 16.0,
      "It looks like you stopped at the radius squared. Take the square root: r = √(50.3 ÷ π) ≈ √16 = 4.0 cm.",
      "Student stops at r^2 = 16 and does not square-root.")
 ],
 "guided_steps": [
   sayonly("Area is π × radius². The area is known, so undo it: divide by π, then square-root."),
   box("Divide the area by π: 50.3 ÷ π = ", 16.0, "Type 50.3 ÷ π. It gives 16.0..."),
   box("That is the radius squared. Square-root it: √16 = ", 4, "What number times itself gives 16?", phase="substitute"),
   box("Check by working forwards: 4² × π = 16 × π = ", 50.3, "16 × π rounds to 50.3.", done="That returns the area, 50.3 cm², so the radius is 4.0 cm.", phase="substitute"),
 ]})

# ---------------- GOLD ----------------
gold = []

gold.append({
 "display": "A running track is two straight sides of 100 m and two semicircular ends of diameter 60 m. Find the total perimeter to the nearest metre.",
 "solutions": [388], "calculator": True, "input_type": "single_value",
 "hint": "Two straights plus one full circle; add before rounding.",
 "misconceptions": [
   mc("wrong_formula", 294,
      "It looks like you used 30 instead of the diameter 60 for the circular part. The two ends make one full circle: π × 60 ≈ 188.5, plus the two 100 m straights, giving about 388 m.",
      "Student uses radius (30) instead of diameter (60): pi x 30 = 94.2, total 200 + 94 = 294 m.")
 ],
 "guided_steps": [
   sayonly("The perimeter is the two straight sides plus the two curved ends. The two semicircular ends together make one full circle of diameter 60 m."),
   box("The two straights: 2 × 100 = ", 200, "Two sides of 100 m."),
   box("The two ends make one full circle, circumference π × diameter. On your calculator, π × 60 = ", 188.5, "Type 60 × π. It is 188.5 to 1 d.p."),
   box("Add, using the calculator's full value (not the rounded 188.5), then round the total to the nearest metre: 200 + π × 60 = ", 388, "Type 200 + 60 × π. It gives 388.49..., which rounds down to 388.", phase="substitute"),
   box("Check the straights alone come to 200: 100 + 100 = ", 200, "Add the two straight sides.", done="The straights give 200 m and the circle adds about 188.5 m, total 388 m. Rounding the 188.5 too early would have given 389, the classic slip.", phase="substitute"),
 ]})

gold.append({
 "display": "A sector has radius 8 cm and angle \\(135°\\). Find the area to 1 d.p.",
 "solutions": [75.4], "calculator": True, "input_type": "single_value",
 "hint": "Angle over 360 times π r squared.",
 "misconceptions": [
   mc("wrong_formula", 150.8,
      "It looks like you used 135 out of 180 instead of out of 360. A sector is angle over 360: (135 ÷ 360) × π × 8² ≈ 75.4 cm².",
      "Student uses 135/180 instead of 135/360: 0.75 x 64pi = 150.8.")
 ],
 "guided_steps": [
   sayonly("A sector is a fraction of a whole circle. The fraction is the angle over 360."),
   box("The fraction of the circle: 135 ÷ 360 = ", 0.375, "Divide the angle by 360."),
   box("Square the radius: 8² = ", 64, "8 × 8."),
   box("Multiply the fraction, the square and π, then round to 1 d.p.: 0.375 × 64 × π = ", 75.4, "Type 0.375 × 64 × π. It gives 75.39...", phase="substitute"),
   box("Check the fraction step: 0.375 × 360 = ", 135, "Should give the angle back.", done="That returns the angle, 135°, so the fraction was right and the area is 75.4 cm².", phase="substitute"),
 ]})

gold.append({
 "display": "A circle has area \\(200\\) cm². Find the circumference to 1 d.p.",
 "solutions": [50.1], "calculator": True, "input_type": "single_value",
 "hint": "Turn the area into a radius, then find the circumference.",
 "misconceptions": [
   mc("wrong_formula", 400.0,
      "It looks like you skipped the square root. From area = π r², first r² = 200 ÷ π, then r = √(200 ÷ π) ≈ 7.98, so C = 2πr ≈ 50.1 cm.",
      "Student skips sqrt: treats r = 200/pi = 63.66, C = 2pi x 63.66 = 400.")
 ],
 "guided_steps": [
   sayonly("Two stages: turn the area back into a radius, then use the radius to find the circumference."),
   box("Divide the area by π: 200 ÷ π = ", 63.66, "Type 200 ÷ π. It gives 63.66 (2 d.p.)."),
   box("That is the radius squared. Square-root it: √63.66 = ", 7.98, "Type √63.66. It gives 7.98 (2 d.p.)."),
   box("Now the circumference: 2 × π × 7.98, to 1 d.p. = ", 50.1, "Type 2 × π × 7.98. It gives 50.13...", phase="substitute"),
   box("Check by squaring the radius and using π: 7.98² × π ≈ ", 200, "7.98² × π comes back to about 200.", done="That returns the area, about 200 cm², so the circumference 50.1 cm is right.", phase="substitute"),
 ]})

gold.append({
 "display": "A sector has arc length 12 cm and radius 9 cm. Find the sector angle to the nearest degree.",
 "solutions": [76], "calculator": True, "input_type": "single_value",
 "hint": "Arc over full circumference gives the fraction; times 360 for the angle.",
 "misconceptions": [
   mc("wrong_formula", 153,
      "It looks like you left the 2 out of the circumference. Arc = (θ ÷ 360) × 2πr, so θ = 12 × 360 ÷ (2 × π × 9) ≈ 76°.",
      "Student omits the 2: uses arc = (theta/360) x pi r, giving 153.")
 ],
 "guided_steps": [
   sayonly("Arc length is a fraction of the full circumference. The fraction is the angle over 360, so work backwards to the angle."),
   box("Full circumference = 2 × π × radius = 2 × π × 9 = ", 56.55, "Type 2 × π × 9. It gives 56.55 (2 d.p.)."),
   box("The arc is 12 out of that whole circumference. Fraction of the circle: 12 ÷ 56.55 = ", 0.2122, "Type 12 ÷ 56.55. It gives 0.2122."),
   box("Multiply the fraction by 360 for the angle, to the nearest degree: 0.2122 × 360 = ", 76, "0.2122 × 360 = 76.4, which rounds to 76.", phase="substitute"),
   box("Check by working forwards: 0.2122 × 56.55 = ", 12, "Should give the arc length back, 12.", done="That returns the arc length, 12 cm, so the angle 76° is right.", phase="substitute"),
 ]})

gold.append({
 "display": "An annulus (ring) has outer radius 10 cm and inner radius 6 cm. Find the area to 1 d.p.",
 "solutions": [201.1], "calculator": True, "input_type": "single_value",
 "hint": "Square both radii, subtract, then times π.",
 "misconceptions": [
   mc("wrong_formula", 50.3,
      "It looks like you subtracted the radii before squaring. Square each first: π × (10² − 6²) = π × 64 ≈ 201.1 cm².",
      "Student subtracts radii first: pi(10-6)^2 = pi x 16 = 50.3.")
 ],
 "guided_steps": [
   sayonly("An annulus is a big circle with a smaller circle cut out. Find each area, then subtract. Square each radius BEFORE subtracting."),
   box("Outer radius squared: 10² = ", 100, "10 × 10."),
   box("Inner radius squared: 6² = ", 36, "6 × 6."),
   box("Subtract the squares, then multiply by π, to 1 d.p.: (100 − 36) × π = 64 × π = ", 201.1, "Type 64 × π. It gives 201.06...", phase="substitute"),
   box("Check the subtraction: 100 − 36 = ", 64, "Subtract the two squared radii.", done="64 × π ≈ 201.1, and subtracting the squares (not the radii) is the key move, so 201.1 cm² is right.", phase="substitute"),
 ]})

# ---------------- assemble ----------------
live["problem_bank"] = {
 "gold": gold, "bronze": bronze, "silver": silver,
 "bronze_description": "Put the numbers straight into one standard area or perimeter formula.",
 "silver_description": "One extra step first: halve a diameter, take a fraction of a circle, rearrange to find a missing length, or add two shapes.",
 "gold_description": "Chain several steps, often with sectors, rings, or a mix of perimeter and area.",
}

live["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one formula, straight in",
   "steps": [
     "Pick the shape and its formula. Rectangle area is \\(l \\times w\\); triangle is \\(\\tfrac{1}{2}bh\\); parallelogram is \\(b \\times h\\); trapezium is \\(\\tfrac{1}{2}(a+b)h\\).",
     "Put the numbers straight in and calculate. <strong>Do not muddle area with perimeter</strong>: area multiplies (units cm²); perimeter adds the sides (units cm).",
     "For circles, circumference is \\(\\pi d\\) and area is \\(\\pi r^2\\). Square the radius before multiplying by \\(\\pi\\).",
   ],
   "example": {
     "question": "Find the area of a triangle with base 12 cm and height 8 cm.",
     "steps": [
       {"label": "Formula", "content": "<p>Area of a triangle = \\(\\tfrac{1}{2} \\times b \\times h\\).</p>"},
       {"label": "Substitute", "content": "<p>\\(\\tfrac{1}{2} \\times 12 \\times 8\\)</p>"},
       {"label": "Check", "content": "<p>\\(12 \\times 8 = 96\\), and half of 96 is 48. ✓</p>"},
       {"label": "Answer", "content": "<p><strong>48 cm²</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: one step first, then the formula",
   "steps": [
     "The formula will not take the numbers as given, so do one preparation step first.",
     "Common preparations: halve a diameter to get the radius; take a fraction of a circle (half, quarter); rearrange a formula to find a missing length; or split a compound shape into rectangles and add.",
     "Then finish as in bronze, and check by working back to a number you were given.",
   ],
   "example": {
     "question": "Find the area of a circle with diameter 18 cm (1 d.p.).",
     "steps": [
       {"label": "Prepare", "content": "<p>Halve the diameter: \\(r = 18 \\div 2 = 9\\) cm.</p>"},
       {"label": "Formula", "content": "<p>\\(A = \\pi r^2 = \\pi \\times 9^2 = \\pi \\times 81\\)</p>"},
       {"label": "Check", "content": "<p>Double the radius: \\(9 \\times 2 = 18\\) cm, the given diameter. ✓</p>"},
       {"label": "Answer", "content": "<p><strong>254.5 cm²</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: several steps chained",
   "steps": [
     "Gold questions combine steps, often with sectors, rings, or a mix of straight and curved edges.",
     "Work in stages and keep full accuracy on your calculator until the very end. Rounding partway (say a circle's circumference) can push the final answer out by a whole unit.",
     "A sector or arc is a fraction \\(\\tfrac{\\theta}{360}\\) of the whole circle; a ring is the big area minus the small area (square each radius first).",
   ],
   "example": {
     "question": "A sector has radius 8 cm and angle 135°. Find the area (1 d.p.).",
     "steps": [
       {"label": "Fraction", "content": "<p>\\(\\tfrac{135}{360} = 0.375\\) of the circle.</p>"},
       {"label": "Whole circle", "content": "<p>\\(\\pi \\times 8^2 = 64\\pi\\)</p>"},
       {"label": "Combine", "content": "<p>\\(0.375 \\times 64\\pi \\approx 75.4\\)</p>"},
       {"label": "Check", "content": "<p>\\(0.375 \\times 360 = 135°\\), the given angle. ✓</p>"},
       {"label": "Answer", "content": "<p><strong>75.4 cm²</strong></p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

live["guided"] = {
 "opener": {
   "label": "Before any formulas",
   "display": "A kitchen floor tiled 4 squares across and 3 squares up:<br>▦▦▦▦<br>▦▦▦▦<br>▦▦▦▦",
   "steps": [
     {"say": "No formulas yet. Just count the tiles on this floor.",
      "pre": "Tiles covering the whole floor: ", "post": "", "answer": 12,
      "hint": "4 tiles in each row, 3 rows. Count them, or do 4 × 3."},
     {"say": "Counting those tiles IS finding the <strong>area</strong>: four in a row, three rows, 4 × 3 = 12. Area of a rectangle is just length × width.",
      "pre": "Now the border. Going all the way round the edge, count the tile-sides: top 4, right 3, bottom 4, left 3, added together = ", "post": "", "answer": 14,
      "hint": "Add the four sides: 4 + 3 + 4 + 3."},
     {"say": "That trip round the edge is the <strong>perimeter</strong>: add every side, 4 + 4 + 3 + 3 = 14, the same as 2 × (4 + 3). Area fills the inside (multiply); perimeter goes round the edge (add). Those two ideas run through every question here. Algebra just calls the sides \\(l\\) and \\(w\\): area \\(= l \\times w\\), perimeter \\(= 2(l + w)\\)."},
   ],
 },
 "teach": {
   "bronze": {
     "display": "Find the area of a trapezium with parallel sides 7 cm and 11 cm and height 4 cm.",
     "label": "Together: your first one",
     "steps": [
       {"say": "Bronze means the numbers go straight into a formula. Trapezium area is half of (the parallel sides added) × height.",
        "pre": "Add the parallel sides: 7 + 11 = ", "post": "", "answer": 18, "hint": "Add the two parallel sides."},
       {"pre": "Multiply by the height: 18 × 4 = ", "post": "", "answer": 72, "hint": "Multiply by 4."},
       {"pre": "Now halve it: 72 ÷ 2 = ", "post": "", "answer": 36, "done": "That is the area.", "hint": "Divide by 2."},
       {"pre": "Check by doubling back: 36 × 2 = ", "post": "", "answer": 72, "done": "That returns (sides added) × height, so 36 cm² is right.", "hint": "Should give 72."},
     ],
   },
   "silver": {
     "display": "Find the area of a circle with diameter 20 cm. Give your answer to 1 d.p.",
     "label": "Together: the silver move",
     "steps": [
       {"say": "Silver adds ONE preparation step. The area formula needs the radius, but we are given the diameter, so halve it first. That is the new move.",
        "pre": "Halve the diameter: 20 ÷ 2 = ", "post": "", "answer": 10, "done": "That halving is the whole new move.", "hint": "Radius is half the diameter."},
       {"pre": "Square the radius: 10² = ", "post": "", "answer": 100, "hint": "10 × 10."},
       {"pre": "Multiply by π and round to 1 d.p.: 100 × π = ", "post": "", "answer": 314.2, "hint": "Type 100 × π. It gives 314.15..."},
       {"pre": "Check the radius came from the diameter: 10 × 2 = ", "post": "", "answer": 20, "done": "That returns the diameter, 20 cm, so 314.2 cm² is right.", "hint": "Double the radius."},
     ],
   },
   "gold": {
     "display": "A sector has radius 8 cm and angle 45°. Find the area to 1 d.p.",
     "label": "Together: the gold move",
     "steps": [
       {"say": "Gold chains several steps. A sector is a fraction of a whole circle, and that fraction is the angle over 360. Find each piece, then combine.",
        "pre": "The fraction of the circle: 45 ÷ 360 = ", "post": "", "answer": 0.125, "done": "That fraction is the gold move: a sector is only part of a circle.", "hint": "Divide the angle by 360."},
       {"pre": "Square the radius: 8² = ", "post": "", "answer": 64, "hint": "8 × 8."},
       {"pre": "Combine, keeping π to the end: 0.125 × 64 = ", "post": "", "answer": 8, "hint": "Multiply the fraction by the square."},
       {"pre": "Multiply by π and round to 1 d.p.: 8 × π = ", "post": "", "answer": 25.1, "hint": "Type 8 × π. It gives 25.13..."},
       {"pre": "Check the fraction: 0.125 × 360 = ", "post": "", "answer": 45, "done": "That returns the angle, 45°, so 25.1 cm² is right.", "hint": "Should give the angle back."},
     ],
   },
 },
}

# method_card left unchanged (already slim: 4 steps, content < 140 words).

# Fix em dashes in preserved worked_examples labels (hard style rule; validator-gated).
for we in live.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

io.open("lesson_geometry-L02.json", "w", encoding="utf-8").write(json.dumps(live, indent=1, ensure_ascii=False))
print("written lesson_geometry-L02.json; top keys:", list(live.keys()))
