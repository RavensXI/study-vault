# -*- coding: utf-8 -*-
import json, re, io

pd = json.load(io.open("_MY_canonical.json", encoding="utf-8"))["practice_data"]
pb = pd["problem_bank"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def fix_svg(s):
    """Strip xmlns (contains http://, validator rejects) and add role/aria-label."""
    if "<svg" not in s:
        return s
    s = s.replace(' xmlns="http://www.w3.org/2000/svg"', "")
    # add role + aria-label to each <svg ...> that lacks them
    def repl(m):
        tag = m.group(0)
        if 'role="img"' in tag:
            return tag
        return tag[:4] + ' role="img" aria-label="Diagram of the spring showing the labelled force and extension"' + tag[4:]
    s = re.sub(r"<svg\b", lambda m: '<svg role="img" aria-label="Diagram of the spring showing the labelled force and extension"', s)
    return s

def set_display(p, new_display):
    """Update plain display and the <p>...</p> inside question, then fix svg."""
    old = p["display"]
    p["display"] = new_display
    if "question" in p and old in p["question"]:
        p["question"] = p["question"].replace(old, new_display)
    if "question" in p:
        p["question"] = fix_svg(p["question"])

# fix all existing svgs first (question fields)
for tier in ("bronze", "silver", "gold"):
    for p in pb[tier]:
        if "question" in p:
            p["question"] = fix_svg(p["question"])

# ---------------------------------------------------------------------------
# BANK REPAIRS
# ---------------------------------------------------------------------------
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# --- B4: em dash in equation_hint -> comma
B[3]["equation_hint"] = "\\(k = \\frac{F}{e}\\), remember extension = stretched − natural"

# --- S2 (silver[1]): stored sol 1.0 was WRONG. Change mass 0.50 -> 0.20 kg => v = 5.0 m/s (clean).
p = S[1]
p["display"] = ("A spring (k = 500 N/m) is stretched 0.10 m and releases a ball of mass 0.20 kg. "
                "Assuming all elastic PE converts to kinetic energy, calculate the ball's speed.")
p["question"] = p["question"].replace("0.50 kg", "0.20 kg").replace(">0.5kg<", ">0.2kg<")
p["question"] = re.sub(r"A spring \(k = 500 N/m\).*?calculate the ball's speed\.",
                       p["display"], p["question"], flags=re.S)
p["solutions"] = [5.0]
p["accept"] = 0.1

# --- G1 (gold[0]): stored sol 6.0 needs m=0.16 kg (display said 0.080 => 8.49). Change mass to 0.16.
p = G[0]
p["display"] = ("A spring (k = 400 N/m) is compressed by 12 cm and releases a 0.16 kg ball. "
                "Assuming all elastic PE converts to kinetic energy, calculate the ball's speed in m/s.")
p["question"] = p["question"].replace("0.080 kg", "0.16 kg").replace(">0.08kg<", ">0.16kg<")
p["question"] = re.sub(r"A spring \(k = 400 N/m\).*?calculate the ball's speed in m/s\.",
                       p["display"], p["question"], flags=re.S)
p["solutions"] = [6.0]
p["accept"] = 0.05

# --- G3 (gold[2]): confusing wording + wrong '0.063 m' figure label. Ask only for Epe.
p = G[2]
new = ("A 0.20 kg ball is dropped from a height of 3.0 m onto a spring (k = 1500 N/m). "
       "Assuming all gravitational potential energy converts to elastic PE (g = 9.8 N/kg), "
       "calculate the elastic PE stored in the spring at maximum compression (in J).")
old = p["display"]
p["display"] = new
p["question"] = p["question"].replace(old, new).replace("compressed 0.063 m", "compression")
p["solutions"] = [5.88]
p["accept"] = 0.01

# --- G4 (gold[3]): unit was "N" but answer is an extension in metres; em dash in text.
p = G[3]
new = ("Two springs A and B are connected end-to-end (in series). Spring A has k = 100 N/m and "
       "spring B has k = 200 N/m. A force of 10 N is applied. In series the same force acts on "
       "each spring. Calculate the total extension of the pair, in metres.")
old = p["display"]
p["display"] = new
p["question"] = p["question"].replace(old, new)
p["unit"] = "m"
p["solutions"] = [0.15]

# --- S3 (silver[2]): text claims a "force-extension graph" but the figure is a spring. Reword.
p = S[2]
new = "A spring is stretched 6.0 cm when a 15 N force is applied. Calculate the spring constant."
old = p["display"]
p["display"] = new
p["question"] = p["question"].replace(old, new)

# re-fix svgs after text edits
for tier in ("bronze", "silver", "gold"):
    for pp in pb[tier]:
        if "question" in pp:
            pp["question"] = fix_svg(pp["question"])

# ---------------------------------------------------------------------------
# HINTS (plain text) + MISCONCEPTION EXPECTS
# ---------------------------------------------------------------------------
def set_misc(p, items):
    """items: list of (pattern, message, expect)."""
    p["misconceptions"] = [{"check": "common", "pattern": pat, "message": msg, "expect": exp}
                           for pat, msg, exp in items]

# Bronze
B[0]["hint"] = "Multiply the spring constant by the extension."
set_misc(B[0], [("inverse_error",
    "F = ke means multiply: 40 × 0.05 = 2 N. Dividing (40 ÷ 0.05 = 800) is upside down.", 800)])

B[1]["hint"] = "Divide the force by the extension."
set_misc(B[1], [("inverse_error",
    "k = F/e = 5.0 ÷ 0.10 = 50 N/m. Dividing extension by force (0.02) is upside down.", 0.02)])

B[2]["hint"] = "Divide the force by the spring constant."
set_misc(B[2], [("inverse_error",
    "e = F/k = 10 ÷ 200 = 0.05 m. Dividing k by F (20) is upside down.", 20)])

B[3]["hint"] = "Extension = stretched minus natural, converted to metres, then k = F/e."
set_misc(B[3], [
    ("wrong_length",
     "Extension = 23 − 20 = 3 cm = 0.03 m. k = 3 ÷ 0.03 = 100 N/m. Using the total length "
     "0.23 m gives about 13 N/m, which is wrong.", 13.04),
    ("unit_error",
     "Convert the extension to metres: 3 cm = 0.03 m. Leaving it as 3 gives k = 3 ÷ 3 = 1 N/m.", 1)])

B[4]["hint"] = "Square the extension, multiply by k, then halve."
set_misc(B[4], [
    ("forgot_half",
     "Epe = ½ × 50 × 0.04² = 0.04 J. Forgetting the ½ doubles it to 0.08 J.", 0.08),
    ("forgot_square",
     "Square the extension first: 0.04² = 0.0016. Using 0.04 without squaring gives 1.0 J.", 1.0)])

# Silver
S[0]["hint"] = "Convert 8.0 cm to metres, square it, then use Epe = half k e squared."
set_misc(S[0], [
    ("unit_error",
     "Convert 8.0 cm to 0.08 m first. Epe = ½ × 120 × 0.08² = 0.384 J. Using 8 cm "
     "(as 8) gives 3840 J.", 3840),
    ("forgot_square",
     "Square the extension: 0.08² = 0.0064. Skipping the square gives ½ × 120 × 0.08 = 4.8 J.", 4.8)])

S[1]["hint"] = "Find the elastic PE, set it equal to half m v squared, then solve for v."
set_misc(S[1], [
    ("forgot_step",
     "Epe = ½ × 500 × 0.10² = 2.5 J. Then 2.5 = ½ × 0.20 × v², so v² = 25 "
     "and v = 5.0 m/s. 2.5 is the energy, not the speed.", 2.5),
    ("forgot_sqrt",
     "After v² = 25 you must take the square root: v = 5.0 m/s, not 25.", 25)])

S[2]["hint"] = "Convert 6.0 cm to metres, then k = F/e."
set_misc(S[2], [
    ("unit_error",
     "Convert 6.0 cm to 0.06 m. k = 15 ÷ 0.06 = 250 N/m. Using 6 cm (as 6) gives 2.5 N/m.", 2.5)])

S[3]["hint"] = "Rearrange Epe = half k e squared for e: e = square root of (2 Epe over k)."
set_misc(S[3], [
    ("forgot_sqrt",
     "e² = 2 × 5.4 ÷ 300 = 0.036. Take the square root: e = 0.190 m. Stopping at 0.036 forgets the root.", 0.036),
    ("forgot_half",
     "Use the ½: e² = 2 × 5.4 ÷ 300 = 0.036. Dropping the doubling gives e² = 0.018 and e = 0.134 m.", 0.1342)])

S[4]["hint"] = "Find the energy in one spring, then double it for both."
set_misc(S[4], [
    ("forgot_step",
     "Each spring stores ½ × 60 × 0.15² = 0.675 J. Two springs store 0.675 × 2 = 1.35 J. "
     "0.675 J is only one spring.", 0.675),
    ("forgot_square",
     "Square the extension: 0.15² = 0.0225. Skipping the square gives ½ × 60 × 0.15 × 2 = 9.0 J.", 9.0)])

# Gold
G[0]["hint"] = "Find the elastic PE, set it equal to half m v squared, then solve for v."
set_misc(G[0], [
    ("forgot_step",
     "Epe = ½ × 400 × 0.12² = 2.88 J. Then 2.88 = ½ × 0.16 × v², so v² = 36 "
     "and v = 6.0 m/s. 2.88 is the energy, not the speed.", 2.88),
    ("forgot_sqrt",
     "After v² = 36 take the square root: v = 6.0 m/s, not 36.", 36)])

G[1]["hint"] = "Find the extension in metres, then k = 2 Epe over e squared."
set_misc(G[1], [
    ("wrong_length",
     "Extension = 30 − 24 = 6 cm = 0.06 m. k = 2 × 0.450 ÷ 0.06² = 250 N/m. Using the total "
     "30 cm (0.30 m) gives 10 N/m.", 10),
    ("forgot_square",
     "Square the extension in the formula: k = 2 × 0.450 ÷ 0.06². Forgetting to square gives "
     "0.9 ÷ 0.06 = 15 N/m.", 15)])

G[2]["hint"] = "At maximum compression all the GPE has become elastic PE, so find mgh."
set_misc(G[2], [
    ("rounding",
     "Use g = 9.8 N/kg: Epe = 0.20 × 9.8 × 3.0 = 5.88 J. Using g = 10 gives 6.0 J.", 6.0)])

G[3]["hint"] = "The same force acts on each spring; find each extension with e = F/k, then add."
set_misc(G[3], [
    ("forgot_step",
     "The same 10 N acts on each spring. eA = 10 ÷ 100 = 0.10 m, eB = 10 ÷ 200 = 0.05 m, total "
     "= 0.15 m. 0.10 m is only spring A.", 0.1),
    ("wrong_rearrange",
     "In series you add the extensions, not the spring constants. 10 ÷ (100 + 200) = 0.033 m is the wrong route.", 0.0333)])

# ---------------------------------------------------------------------------
# GUIDED_STEPS per problem
# ---------------------------------------------------------------------------
B[0]["guided_steps"] = [
    sayonly("Hooke's law is \\(F = ke\\): force equals spring constant times extension, with e in metres."),
    box("The extension is already in metres, so e = 0.05 m. Enter e: ", 0.05, "It is given as 0.05 m, no conversion needed."),
    box("Substitute into F = ke: 40 × 0.05 = ", 2, "Multiply the spring constant by the extension.", phase="substitute"),
    box("Check by reversing: 2 ÷ 0.05 = ", 40, "Force ÷ extension returns the spring constant.",
        done="Back to k = 40 N/m, so F = 2 N is right."),
]
B[1]["guided_steps"] = [
    sayonly("Rearrange Hooke's law for the spring constant: \\(k = F/e\\), with e in metres."),
    box("The extension is in metres: e = 0.10 m. Enter e: ", 0.10, "Given as 0.10 m already."),
    box("k = F/e = 5.0 ÷ 0.10 = ", 50, "Divide the force by the extension.", phase="substitute"),
    box("Reverse it: 50 × 0.10 = ", 5, "k × e should return the 5.0 N force.",
        done="Back to 5.0 N, so k = 50 N/m is right."),
]
B[2]["guided_steps"] = [
    sayonly("Rearrange for extension: \\(e = F/k\\). The answer will be in metres."),
    box("Both values are ready. Enter the force in N: ", 10, "The applied force is 10 N."),
    box("e = F/k = 10 ÷ 200 = ", 0.05, "Divide the force by the spring constant.", phase="substitute"),
    box("Reverse: 200 × 0.05 = ", 10, "k × e should return 10 N.",
        done="Back to 10 N, so e = 0.05 m is right."),
]
B[3]["guided_steps"] = [
    sayonly("First find the extension: \\(e =\\) stretched length − natural length. Then \\(k = F/e\\)."),
    box("Extension in cm: 23 − 20 = ", 3, "Stretched minus natural."),
    box("Convert to metres: 3 ÷ 100 = ", 0.03, "Divide cm by 100."),
    box("k = F/e = 3 ÷ 0.03 = ", 100, "Divide the force by the extension in metres.", phase="substitute"),
    box("Reverse: 100 × 0.03 = ", 3, "k × e should return the 3 N force.",
        done="Back to 3 N, so k = 100 N/m is right."),
]
B[4]["guided_steps"] = [
    sayonly("Elastic PE: \\(E_{pe} = \\frac{1}{2}ke^2\\). Square the extension, multiply by k, then halve."),
    box("The extension is in metres: e = 0.04 m. Square it: 0.04² = ", 0.0016, "0.04 × 0.04."),
    box("Epe = ½ × 50 × 0.0016 = ", 0.04, "Multiply 50 by 0.0016, then halve.", phase="substitute"),
    box("Undo the half: 0.04 × 2 = ", 0.08, "0.04 J doubled.",
        done="0.08 = 50 × 0.0016, which matches ke², so Epe = 0.04 J is right."),
]

S[0]["guided_steps"] = [
    sayonly("Elastic PE: \\(E_{pe} = \\frac{1}{2}ke^2\\). Convert the length to metres first."),
    box("Convert 8.0 cm to metres: 8.0 ÷ 100 = ", 0.08, "Divide cm by 100."),
    box("Square it: 0.08² = ", 0.0064, "0.08 × 0.08."),
    box("Epe = ½ × 120 × 0.0064 = ", 0.384, "Multiply 120 by 0.0064, then halve.", phase="substitute"),
    box("Undo the half: 0.384 × 2 = ", 0.768, "0.384 doubled.",
        done="0.768 = 120 × 0.0064, matching ke², so Epe = 0.384 J is right."),
]
S[1]["guided_steps"] = [
    sayonly("Two energy stores. First the elastic PE: \\(E_{pe} = \\frac{1}{2}ke^2\\). Then all of it becomes "
            "kinetic energy: \\(E_{pe} = \\frac{1}{2}mv^2\\)."),
    box("Elastic PE: ½ × 500 × 0.10² = ½ × 500 × 0.01 = ", 2.5,
        "Square 0.10, then × 500, then halve."),
    box("All 2.5 J becomes KE. First work out ½ × 0.20 = ", 0.1, "Half of the 0.20 kg mass."),
    box("So v² = 2.5 ÷ 0.1 = ", 25, "Divide the energy by 0.1.", phase="substitute"),
    box("v = √25 = ", 5, "Square root of 25.", phase="substitute"),
    box("Reverse: ½ × 0.20 × 5² = ", 2.5, "½ × 0.20 × 25.",
        done="Back to 2.5 J, so v = 5.0 m/s is right."),
]
S[2]["guided_steps"] = [
    sayonly("Rearrange for the spring constant: \\(k = F/e\\). Convert the extension to metres first."),
    box("Convert 6.0 cm to metres: 6.0 ÷ 100 = ", 0.06, "Divide cm by 100."),
    box("k = F/e = 15 ÷ 0.06 = ", 250, "Divide the force by the extension in metres.", phase="substitute"),
    box("Reverse: 250 × 0.06 = ", 15, "k × e should return 15 N.",
        done="Back to 15 N, so k = 250 N/m is right."),
]
S[3]["guided_steps"] = [
    sayonly("Rearrange \\(E_{pe} = \\frac{1}{2}ke^2\\) for e: \\(e = \\sqrt{2E_{pe}/k}\\)."),
    box("Work out e² = 2 × 5.4 ÷ 300 = ", 0.036, "Double the energy, then divide by k."),
    box("e = √0.036 = ", 0.1897, "Take the square root; give 4 significant figures.", phase="substitute"),
    box("Reverse: ½ × 300 × 0.036 = ", 5.4, "½ × 300 × e².",
        done="Back to 5.4 J, so e = 0.1897 m is right."),
]
S[4]["guided_steps"] = [
    sayonly("Elastic PE per spring: \\(E_{pe} = \\frac{1}{2}ke^2\\). Then add both springs."),
    box("Square the extension: 0.15² = ", 0.0225, "0.15 × 0.15."),
    box("One spring: ½ × 60 × 0.0225 = ", 0.675, "Multiply 60 by 0.0225, then halve."),
    box("Two identical springs: 0.675 × 2 = ", 1.35, "Double it for both springs.", phase="substitute"),
    box("Undo: 1.35 ÷ 2 = ", 0.675, "Total shared between two springs.",
        done="0.675 J per spring, so the total is 1.35 J."),
]

G[0]["guided_steps"] = [
    sayonly("Elastic PE launches the ball as kinetic energy: \\(E_{pe} = \\frac{1}{2}ke^2\\) then "
            "\\(E_{pe} = \\frac{1}{2}mv^2\\)."),
    box("Elastic PE: ½ × 400 × 0.12² = ½ × 400 × 0.0144 = ", 2.88,
        "Square 0.12, then × 400, then halve."),
    box("All 2.88 J becomes KE. First work out ½ × 0.16 = ", 0.08, "Half of the 0.16 kg mass."),
    box("v² = 2.88 ÷ 0.08 = ", 36, "Divide the energy by 0.08.", phase="substitute"),
    box("v = √36 = ", 6, "Square root of 36.", phase="substitute"),
    box("Reverse: ½ × 0.16 × 6² = ", 2.88, "½ × 0.16 × 36.",
        done="Back to 2.88 J, so v = 6.0 m/s is right."),
]
G[1]["guided_steps"] = [
    sayonly("Rearrange \\(E_{pe} = \\frac{1}{2}ke^2\\) for k: \\(k = 2E_{pe}/e^2\\). Find the extension first."),
    box("Extension in cm: 30 − 24 = ", 6, "Stretched minus natural."),
    box("Convert and square: (6 ÷ 100)² = 0.06² = ", 0.0036, "0.06 × 0.06."),
    box("k = 2 × 0.450 ÷ 0.0036 = 0.9 ÷ 0.0036 = ", 250, "Double the energy, then divide by e².", phase="substitute"),
    box("Reverse: ½ × 250 × 0.0036 = ", 0.45, "½ × 250 × e² gives the stored energy.",
        done="Back to 0.450 J, so k = 250 N/m is right."),
]
G[2]["guided_steps"] = [
    sayonly("At maximum compression all the gravitational PE has become elastic PE, so first find \\(E_p = mgh\\)."),
    box("Mass and height are in base units. GPE = m × g × h = 0.20 × 9.8 × 3.0. First 0.20 × 9.8 = ", 1.96,
        "Mass times g."),
    box("Now × 3.0: 1.96 × 3.0 = ", 5.88, "Multiply by the height.", phase="substitute"),
    box("This equals the elastic PE stored. Check: 5.88 ÷ 3.0 = ", 1.96, "Energy ÷ height returns the weight.",
        done="1.96 N is the ball's weight (0.20 × 9.8), so Epe = 5.88 J is right."),
]
G[3]["guided_steps"] = [
    sayonly("In series the same 10 N acts on both springs. Find each extension with \\(e = F/k\\), then add them."),
    box("Spring A: eA = 10 ÷ 100 = ", 0.1, "Force ÷ spring constant of A."),
    box("Spring B: eB = 10 ÷ 200 = ", 0.05, "Force ÷ spring constant of B."),
    box("Total extension = 0.10 + 0.05 = ", 0.15, "Add the two extensions.", phase="substitute"),
    box("Reverse using B: 200 × 0.05 = ", 10, "k × e for B returns the 10 N force.",
        done="The same 10 N acts on each, so the total extension 0.15 m is right."),
]

# ---------------------------------------------------------------------------
# TIER DESCRIPTIONS
# ---------------------------------------------------------------------------
pb["bronze_description"] = ("One equation, one step: put the given values straight into F = ke, or rearrange for "
                            "the missing quantity. Extensions are already in metres.")
pb["silver_description"] = ("One extra move: convert a length from centimetres to metres, or use the energy "
                            "equation Epe = ½ke², squaring the extension first.")
pb["gold_description"] = ("Multi-step: chain elastic PE with kinetic energy or gravitational PE, or combine two "
                          "springs, then finish the calculation.")

# ---------------------------------------------------------------------------
# TIER_GUIDES
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, one step",
        "steps": [
            "Bronze problems give two of the three quantities in \\(F = ke\\): force in N, spring constant k in N/m, extension e in m.",
            "Substitute straight in, or rearrange first: \\(k = F/e\\) for stiffness, \\(e = F/k\\) for extension.",
            "Keep the extension in metres. Here the lengths are already in metres."
        ],
        "example": {
            "question": "A spring of spring constant 80 N/m is stretched by 0.05 m. Calculate the force.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(F = ke\\)</p>"},
                {"label": "Substitute", "content": "<p>F = 80 × 0.05</p>"},
                {"label": "Check", "content": "<p>80 × 0.05 = 4</p>"},
                {"label": "Answer", "content": "<p><strong>4 N</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: convert units or rearrange",
        "steps": [
            "Silver adds one twist: either the length is in centimetres (divide by 100 for metres) or you must rearrange before substituting.",
            "For elastic PE use \\(E_{pe} = \\frac{1}{2}ke^2\\): square the extension first, then multiply by k, then halve.",
            "To find e from energy, rearrange: \\(e = \\sqrt{2E_{pe}/k}\\), taking the square root last."
        ],
        "example": {
            "question": "A spring (k = 200 N/m) is stretched 5.0 cm. Calculate the elastic PE stored.",
            "steps": [
                {"label": "Convert", "content": "<p>5.0 cm = 0.05 m</p>"},
                {"label": "Square then substitute", "content": "<p>\\(E_{pe} = \\frac{1}{2} \\times 200 \\times 0.05^2 = \\frac{1}{2} \\times 200 \\times 0.0025\\)</p>"},
                {"label": "Check", "content": "<p>½ × 200 × 0.0025 = 0.25</p>"},
                {"label": "Answer", "content": "<p><strong>0.25 J</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two equations",
        "steps": [
            "Gold problems link two ideas: a spring's energy converts into movement, or comes from a drop.",
            "Launch: all the stored \\(E_{pe} = \\frac{1}{2}ke^2\\) becomes \\(E_k = \\frac{1}{2}mv^2\\). Set them equal, solve for v.",
            "Drop onto a spring: the lost \\(E_p = mgh\\) becomes elastic PE. Work out the energy first, then the quantity asked for."
        ],
        "example": {
            "question": "A spring (k = 100 N/m) stretched 0.20 m launches a 0.50 kg trolley. Find its speed, assuming all Epe becomes KE.",
            "steps": [
                {"label": "Elastic PE", "content": "<p>\\(E_{pe} = \\frac{1}{2} \\times 100 \\times 0.20^2 = 2\\ \\text{J}\\)</p>"},
                {"label": "Set equal to KE", "content": "<p>\\(2 = \\frac{1}{2} \\times 0.50 \\times v^2\\), so \\(v^2 = 8\\)</p>"},
                {"label": "Check", "content": "<p>√8 = 2.83</p>"},
                {"label": "Answer", "content": "<p><strong>v = 2.83 m/s</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# GUIDED (opener + teach)
# ---------------------------------------------------------------------------
pd["guided"] = {
    "opener": {
        "label": "Before any equations",
        "display": "Picture a spring hanging from a hook. Hang one 1 N weight on it and it stretches 2 cm.",
        "steps": [
            box("Springs stretch in step with the pull. Hang a second 1 N weight (2 N in total). "
                "How far does it stretch, in cm? ", 4,
                "One weight gave 2 cm, so two weights give twice as much."),
            box("Now hang three weights (3 N in total). Extension in cm? ", 6,
                "Each 1 N adds another 2 cm."),
            sayonly("You just used <strong>Hooke's law</strong>: the extension is proportional to the force. "
                    "Every 1 N adds a fixed 2 cm, so force = stiffness × extension, written \\(F = ke\\). "
                    "The stiffness k (the spring constant) is the force needed per metre of stretch."),
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: the bronze move",
            "display": "A spring is stretched 0.05 m by a 4 N force. Find the spring constant, the force needed for "
                       "0.12 m, and the extension a 10 N force would give.",
            "steps": [
                sayonly("Bronze move: use \\(F = ke\\), rearranging when the unknown is not F."),
                box("Rearrange for k: k = F/e = 4 ÷ 0.05 = ", 80, "Divide force by extension."),
                box("Force at 0.12 m: F = ke = 80 × 0.12 = ", 9.6, "Multiply k by the new extension."),
                box("Extension for 10 N: e = F/k = 10 ÷ 80 = ", 0.125, "Divide the force by k."),
                box("Check the last one: 80 × 0.125 = ", 10, "k × e should return 10 N.",
                    done="Every step used \\(F = ke\\). That is the whole bronze move."),
            ],
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "A spring (k = 250 N/m) is stretched by 8.0 cm. Calculate the elastic potential energy stored.",
            "steps": [
                sayonly("Silver move: convert the length to metres first, then use \\(E_{pe} = \\frac{1}{2}ke^2\\)."),
                box("Convert 8.0 cm to metres: 8.0 ÷ 100 = ", 0.08, "Divide cm by 100."),
                box("Square the extension: 0.08² = ", 0.0064, "0.08 × 0.08."),
                box("Epe = ½ × 250 × 0.0064 = ", 0.8, "Multiply k by e², then halve."),
                box("Check by reversing: √(2 × 0.8 ÷ 250) = √0.0064 = ", 0.08,
                    "This should return the 0.08 m extension.",
                    done="Back to 0.08 m, so 0.8 J is right. Converting units first is the silver move."),
            ],
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "A spring (k = 800 N/m) is compressed 0.10 m and launches a 0.40 kg ball. Assuming all elastic "
                       "PE becomes kinetic energy, find the ball's speed.",
            "steps": [
                sayonly("Gold move: the stored elastic PE turns into kinetic energy. Work out Epe, set it equal to "
                        "\\(\\frac{1}{2}mv^2\\), then solve for v."),
                box("Epe = ½ × 800 × 0.10² = ½ × 800 × 0.01 = ", 4,
                    "Square 0.10, then × 800, then halve."),
                box("All 4 J becomes KE: 4 = ½ × 0.40 × v². First ½ × 0.40 = ", 0.2, "Half of 0.40."),
                box("So v² = 4 ÷ 0.2 = ", 20, "Divide the energy by 0.2."),
                box("v = √20 = ", 4.47, "Square root of 20.",
                    done="Energy in equals energy out: 4.47 m/s. Chaining the two equations is the gold move."),
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# SLIM METHOD_CARD
# ---------------------------------------------------------------------------
pd["method_card"] = {
    "title": "Hooke's Law and Elastic PE",
    "steps": [
        "Find the extension: e = stretched length − natural length, in metres (÷100 from cm).",
        "Force: F = ke. Rearrange for whatever is missing.",
        "Energy: Epe = ½ke². Square e first, then ×k, then halve.",
        "State the answer with its unit (N, N/m, m or J).",
    ],
    "content": ("<p>Two equations. <strong>Hooke's law</strong> \\(F = ke\\): force (N) = spring constant (N/m) "
                "× extension (m). <strong>Elastic PE</strong> \\(E_{pe} = \\frac{1}{2}ke^2\\): energy (J) stored "
                "in a stretched or compressed spring.</p><p>Keep the extension in metres, and remember it is the "
                "change in length, not the total length. Check whether your board gives you the \\(E_{pe}\\) "
                "equation or expects you to recall it.</p>"),
}

# ---------------------------------------------------------------------------
# EM-DASH SWEEP (pre-existing dashes in preserved fields: labels, exam_context)
# ---------------------------------------------------------------------------
def sweep(o):
    if isinstance(o, dict):
        return {k: (v if k in ("note", "guided_skip_reason") else sweep(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [sweep(v) for v in o]
    if isinstance(o, str):
        return o.replace(" — ", ": ").replace("—", ":")
    return o
pd = sweep(pd)

# ---------------------------------------------------------------------------
# WRITE SHARD
# ---------------------------------------------------------------------------
out = "lesson_higher-calculations-L01@8a0771bf50.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out)
