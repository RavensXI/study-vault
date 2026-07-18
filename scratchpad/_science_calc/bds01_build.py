# -*- coding: utf-8 -*-
"""Build guided practice_data for biology-data-skills-L01 (Magnification & Unit
Conversions). Verifies every box value arithmetically, writes the shard."""
import json, io

def box(pre, answer, hint, post="", done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def say(s): return {"say": s}

MAG = "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)"

pd = {}

# ---------- method_card (slim) ----------
pd["method_card"] = {
    "title": "Magnification and Unit Conversions",
    "steps": [
        "Decide what you are finding: magnification, image size, or actual size.",
        "Convert both sizes to the same unit before dividing.",
        "Substitute into magnification = image ÷ actual, rearranging if needed.",
        "State the answer; magnification has no unit."
    ],
    "content": ("<p>Magnification links three quantities: " + MAG +
        ". You are given two and find the third.</p><p>The rule that saves most "
        "marks: both sizes must be in the <strong>same unit</strong> before you "
        "divide, so convert first. Going to a smaller unit (mm → μm → nm) "
        "multiply by 1000; going larger, divide by 1000.</p><p>Rearrange when "
        "needed: actual size = image ÷ magnification, image size = magnification "
        "× actual. Magnification has <strong>no unit</strong>.</p>")
}

pd["topic_links"] = {"prerequisites": ["Cell structure (Biology Paper 1)",
                                       "Required Practical 1: Microscopy"]}
pd["exam_context"] = {
    "marks": "2–3 marks per calculation",
    "paper": "Paper 1 (Biology)",
    "frequency": "Very common. Appears regularly and links to Required Practical 1 (microscopy)"
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one conversion, then divide",
        "steps": [
            "Read off the image size and the actual size. Put both in the same unit first: mm to μm means multiply by 1000.",
            "Divide: " + MAG + ".",
            "Magnification has no unit; a length answer keeps its unit."
        ],
        "example": {
            "question": "A cell is 40 μm wide. Its image is 16 mm wide. Calculate the magnification.",
            "steps": [
                {"label": "Convert", "content": "16 mm = 16 × 1000 = 16,000 μm"},
                {"label": "Substitute", "content": "16,000 ÷ 40"},
                {"label": "Check", "content": "400 × 40 = 16,000"},
                {"label": "Answer", "content": "<strong>×400</strong> (no unit)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert, then rearrange",
        "steps": [
            "If the unknown is the actual size or the image size, rearrange first: actual = image ÷ magnification, image = magnification × actual.",
            "Convert units before or after so the answer is in the unit asked for.",
            "Standard form: 1 μm = 10⁻⁶ m and 1 nm = 10⁻⁹ m."
        ],
        "example": {
            "question": "An image is 18 mm long at ×3000 magnification. Find the actual size in μm.",
            "steps": [
                {"label": "Convert", "content": "18 mm = 18,000 μm"},
                {"label": "Rearrange", "content": "actual = 18,000 ÷ 3000"},
                {"label": "Check", "content": "6 × 3000 = 18,000"},
                {"label": "Answer", "content": "<strong>6 μm</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: two steps or a comparison",
        "steps": [
            "Multi-step questions chain a conversion with a calculation, or compare two cells.",
            "To compare sizes fairly, work out each actual size first, then subtract or divide. Never compare image sizes directly.",
            "For very small lengths, finish in standard form: one digit before the point, then the power of 10."
        ],
        "example": {
            "question": "A ribosome is 20 nm wide. Give its width in metres in standard form.",
            "steps": [
                {"label": "Convert power", "content": "1 nm = 10⁻⁹ m, so 20 nm = 20 × 10⁻⁹ m"},
                {"label": "Tidy", "content": "20 × 10⁻⁹ = 2 × 10⁻⁸"},
                {"label": "Check", "content": "2 × 10⁻⁸ = 0.00000002 m = 20 nm"},
                {"label": "Answer", "content": "<strong>2 × 10⁻⁸ m</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided.opener + teach ----------
pd["guided"] = {
    "opener": {
        "steps": [
            say("A photographer blows up a picture of a bee. In the enlarged print the bee is 12 cm long. The real bee is 2 cm long."),
            box("How many times longer is the printed bee than the real bee? ", 6, "12 ÷ 2."),
            say("That number, 6, is the <strong>magnification</strong>: how many times bigger the image is than the real thing. So " + MAG + "."),
            say("Cells are the tricky part: they are far smaller than a ruler's markings, so a real cell might be 0.05 mm while its image is 50 mm. Before you can divide, both sizes must be in the <strong>same unit</strong>."),
            box("There are how many μm (micrometres) in 1 mm? ", 1000, "Milli to micro is a factor of 1000."),
            say("Convert first, then divide. That single habit is the whole lesson.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A cell is 50 μm wide. Its image under a microscope is 30 mm wide. Calculate the magnification.",
            "steps": [
                say("Magnification = image ÷ actual, but the units must match. Convert the image to μm first."),
                box("μm in 1 mm: ", 1000, "Milli to micro is a factor of 1000."),
                box("Image in μm: 30 × 1000 = ", 30000, "Multiply the mm by 1000."),
                box("Magnification: 30000 ÷ 50 = ", 600, "Image ÷ actual."),
                box("Check: 600 × 50 = ", 30000, "Magnification × actual recovers the image.",
                    done="Recovers 30,000 μm, so ×600 is right.")
            ]
        },
        "silver": {
            "display": "An image of a cell is 24 mm long at ×3000 magnification. Calculate the actual size in μm.",
            "steps": [
                say("The unknown is the actual size, so rearrange: actual = image ÷ magnification. Convert the image to μm first."),
                box("μm in 1 mm: ", 1000, "Milli to micro is a factor of 1000."),
                box("Image in μm: 24 × 1000 = ", 24000, "Multiply the mm by 1000."),
                box("Actual size: 24000 ÷ 3000 = ", 8, "Image ÷ magnification."),
                box("Check: 8 × 3000 = ", 24000, "Actual × magnification recovers the image.",
                    done="Recovers 24,000 μm, so 8 μm is right. The new move was rearranging.")
            ]
        },
        "gold": {
            "display": "Cell A has an image 40 mm wide at ×2000. Cell B has an image 45 mm wide at ×1500. Which cell is actually bigger, and by how many μm?",
            "steps": [
                say("A bigger image does not mean a bigger cell. Work out each actual size (image ÷ magnification, images already in μm: 40 mm = 40,000 μm, 45 mm = 45,000 μm), then compare."),
                box("Cell A actual: 40000 ÷ 2000 = ", 20, "Image ÷ magnification."),
                box("Cell B actual: 45000 ÷ 1500 = ", 30, "Image ÷ magnification."),
                box("Difference: 30 − 20 = ", 10, "Larger actual size minus smaller."),
                box("Check: 20 + 10 = ", 30, "Add the difference back to Cell A.",
                    done="Cell B is bigger by 10 μm, even though its image was only a little wider.")
            ]
        }
    }
}

# ---------- problem_bank ----------
pb = {
    "bronze_description": "One step: convert the two sizes to the same unit, then divide image by actual (or read off a single unit conversion).",
    "silver_description": "Rearrange the equation to find the actual size or the image size, converting units so the answer lands in the unit asked for.",
    "gold_description": "Chain two steps: convert to metres in standard form, or work out and compare two actual sizes."
}

# ---- BRONZE ----
bronze = []

# B0
bronze.append({
    "unit": "", "display": "A plant cell has an actual size of 100 μm. Under a microscope the image is 40 mm long. Calculate the magnification. (Convert the image to μm first.)",
    "solutions": [400], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide image by actual size.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "Convert the image to μm first: 40 mm = 40,000 μm. Then 40,000 ÷ 100 = ×400.", "expect": 0.4},
        {"pattern": "inverted", "message": "Magnification = image ÷ actual, not actual ÷ image. 40,000 ÷ 100 = 400.", "expect": 0.0025}
    ],
    "guided_steps": [
        say("Magnification compares the image with the real thing: " + MAG + ". Convert the image to μm so both sizes share a unit."),
        box("Image in μm: 40 × 1000 = ", 40000, "1 mm = 1000 μm."),
        box("Magnification: 40000 ÷ 100 = ", 400, "Image ÷ actual.", done="×400. Magnification has no unit.", phase="substitute"),
        box("Check: 400 × 100 = ", 40000, "Magnification × actual recovers the image.", done="Recovers 40,000 μm, so ×400 is right.", phase="substitute")
    ]
})

# B1
bronze.append({
    "unit": "μm", "display": "Convert 0.5 mm to μm.", "solutions": [500],
    "calculator": False, "input_type": "single_value",
    "equation_hint": "\\(1 \\text{ mm} = 1000 \\text{ μm}\\)",
    "hint": "Going to a smaller unit, multiply by 1000.",
    "misconceptions": [
        {"pattern": "wrong_direction", "message": "mm to μm is going to a smaller unit, so multiply by 1000: 0.5 × 1000 = 500 μm.", "expect": 0.0005}
    ],
    "guided_steps": [
        say("mm to μm is going to a smaller unit, so you multiply by 1000."),
        box("μm in 1 mm: ", 1000, "Milli to micro is a factor of 1000."),
        box("0.5 × 1000 = ", 500, "Multiply by 1000.", done="500 μm.", phase="substitute"),
        box("Check: 500 ÷ 1000 = ", 0.5, "Dividing back returns the mm value.", done="Back to 0.5 mm, so 500 μm is right.", phase="substitute")
    ]
})

# B2
bronze.append({
    "unit": "", "display": "A cheek cell is 60 μm across. An image of it is 12 mm across. What is the magnification?",
    "solutions": [200], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide image by actual size.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "Convert the image to μm: 12 mm = 12,000 μm. Magnification = 12,000 ÷ 60 = ×200.", "expect": 0.2},
        {"pattern": "inverted", "message": "Magnification = image ÷ actual = 12,000 ÷ 60 = 200, not 60 ÷ 12,000.", "expect": 0.005}
    ],
    "guided_steps": [
        say("Magnification = image ÷ actual, with both in the same unit. Convert the image to μm."),
        box("Image in μm: 12 × 1000 = ", 12000, "1 mm = 1000 μm."),
        box("Magnification: 12000 ÷ 60 = ", 200, "Image ÷ actual.", done="×200.", phase="substitute"),
        box("Check: 200 × 60 = ", 12000, "Magnification × actual recovers the image.", done="Recovers 12,000 μm, so ×200 is right.", phase="substitute")
    ]
})

# B3
bronze.append({
    "unit": "mm", "display": "Convert 7500 μm to mm.", "solutions": [7.5],
    "calculator": False, "input_type": "single_value",
    "equation_hint": "\\(1 \\text{ mm} = 1000 \\text{ μm}\\)",
    "hint": "Going to a larger unit, divide by 1000.",
    "misconceptions": [
        {"pattern": "wrong_direction", "message": "μm to mm is going to a larger unit, so divide by 1000: 7500 ÷ 1000 = 7.5 mm.", "expect": 7500000}
    ],
    "guided_steps": [
        say("μm to mm is going to a larger unit, so you divide by 1000."),
        box("μm in 1 mm: ", 1000, "Milli to micro is a factor of 1000."),
        box("7500 ÷ 1000 = ", 7.5, "Divide by 1000.", done="7.5 mm.", phase="substitute"),
        box("Check: 7.5 × 1000 = ", 7500, "Multiplying back returns the μm value.", done="Back to 7500 μm, so 7.5 mm is right.", phase="substitute")
    ]
})

# B4
bronze.append({
    "unit": "μm", "display": "A microscope has a magnification of ×400. The image of a cell is 20 mm long. What is the actual size of the cell in μm?",
    "solutions": [50], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide by the magnification.",
    "misconceptions": [
        {"pattern": "wrong_rearrangement", "message": "Actual = image ÷ magnification, not image × magnification. 20,000 ÷ 400 = 50 μm.", "expect": 8000000},
        {"pattern": "unit_error", "message": "Convert the image to μm before dividing: 20 mm = 20,000 μm. 20,000 ÷ 400 = 50 μm.", "expect": 0.05}
    ],
    "guided_steps": [
        say("The unknown is the actual size, so rearrange: \\(\\text{actual size} = \\frac{\\text{image size}}{\\text{magnification}}\\). Convert the image to μm first."),
        box("Image in μm: 20 × 1000 = ", 20000, "1 mm = 1000 μm."),
        box("Actual size: 20000 ÷ 400 = ", 50, "Image ÷ magnification.", done="50 μm.", phase="substitute"),
        box("Check: 50 × 400 = ", 20000, "Actual × magnification recovers the image.", done="Recovers 20,000 μm, so 50 μm is right.", phase="substitute")
    ]
})

# B5
bronze.append({
    "unit": "nm", "display": "Convert 3 μm to nm.", "solutions": [3000],
    "calculator": False, "input_type": "single_value",
    "equation_hint": "\\(1 \\text{ μm} = 1000 \\text{ nm}\\)",
    "hint": "Going to a smaller unit, multiply by 1000.",
    "misconceptions": [
        {"pattern": "wrong_direction", "message": "μm to nm is going to a smaller unit, so multiply by 1000: 3 × 1000 = 3000 nm.", "expect": 0.003}
    ],
    "guided_steps": [
        say("μm to nm is going to a smaller unit, so you multiply by 1000."),
        box("nm in 1 μm: ", 1000, "Micro to nano is a factor of 1000."),
        box("3 × 1000 = ", 3000, "Multiply by 1000.", done="3000 nm.", phase="substitute"),
        box("Check: 3000 ÷ 1000 = ", 3, "Dividing back returns the μm value.", done="Back to 3 μm, so 3000 nm is right.", phase="substitute")
    ]
})

# B6
bronze.append({
    "unit": "", "display": "An onion cell has an actual width of 80 μm. A student draws it 24 mm wide. Calculate the magnification.",
    "solutions": [300], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide image by actual size.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "Convert the drawing to μm: 24 mm = 24,000 μm. Magnification = 24,000 ÷ 80 = ×300.", "expect": 0.3}
    ],
    "guided_steps": [
        say("Magnification = image ÷ actual, with both in the same unit. Convert the drawing to μm."),
        box("Image in μm: 24 × 1000 = ", 24000, "1 mm = 1000 μm."),
        box("Magnification: 24000 ÷ 80 = ", 300, "Image ÷ actual.", done="×300.", phase="substitute"),
        box("Check: 300 × 80 = ", 24000, "Magnification × actual recovers the image.", done="Recovers 24,000 μm, so ×300 is right.", phase="substitute")
    ]
})

# B7 (MC)
bronze.append({
    "display": "Which of these is the correct unit conversion?",
    "options": ["1 mm = 100 μm", "1 mm = 1000 μm", "1 mm = 10,000 μm", "1 mm = 1,000,000 μm"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "equation_hint": "\\(1 \\text{ mm} = 1000 \\text{ μm}\\)",
    "hint": "Milli is 10⁻³ and micro is 10⁻⁶, so there are 1000 μm in 1 mm.",
    "misconceptions": [
        {"pattern": "wrong_conversion", "message": "1 mm = 1000 μm. Milli is 10⁻³ and micro is 10⁻⁶, so there are 10³ = 1000 μm in every mm.", "expect": None}
    ]
})

pb["bronze"] = bronze

# ---- SILVER ----
silver = []

# S0
silver.append({
    "unit": "", "display": "A bacterium has an actual length of 2 μm. A photograph shows it as 15 mm long. Calculate the magnification of the photograph.",
    "solutions": [7500], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide image by actual size.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "Convert the photo to μm: 15 mm = 15,000 μm. Magnification = 15,000 ÷ 2 = ×7500.", "expect": 7.5},
        {"pattern": "inverted", "message": "Magnification = image ÷ actual = 15,000 ÷ 2 = 7500. Dividing the wrong way gives about 0.000133.", "expect": 0.000133}
    ],
    "guided_steps": [
        say("Magnification = image ÷ actual. Convert the photograph to μm first."),
        box("Image in μm: 15 × 1000 = ", 15000, "1 mm = 1000 μm."),
        box("Magnification: 15000 ÷ 2 = ", 7500, "Image ÷ actual.", done="×7500.", phase="substitute"),
        box("Check: 7500 × 2 = ", 15000, "Magnification × actual recovers the image.", done="Recovers 15,000 μm, so ×7500 is right.", phase="substitute")
    ]
})

# S1
silver.append({
    "unit": "μm", "display": "An image of a cell is 36 mm long. The magnification used was ×1200. Calculate the actual size of the cell in μm.",
    "solutions": [30], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide by the magnification.",
    "misconceptions": [
        {"pattern": "wrong_rearrangement", "message": "Actual = image ÷ magnification, not image × magnification. 36,000 ÷ 1200 = 30 μm.", "expect": 43200000},
        {"pattern": "unit_error", "message": "Convert the image to μm first: 36 mm = 36,000 μm. Then 36,000 ÷ 1200 = 30 μm.", "expect": 0.03}
    ],
    "guided_steps": [
        say("The unknown is the actual size, so rearrange: actual = image ÷ magnification. Convert the image to μm first."),
        box("Image in μm: 36 × 1000 = ", 36000, "1 mm = 1000 μm."),
        box("Actual size: 36000 ÷ 1200 = ", 30, "Image ÷ magnification.", done="30 μm.", phase="substitute"),
        box("Check: 30 × 1200 = ", 36000, "Actual × magnification recovers the image.", done="Recovers 36,000 μm, so 30 μm is right.", phase="substitute")
    ]
})

# S2
silver.append({
    "unit": "mm", "display": "A red blood cell has a diameter of 7 μm. A student wants to draw it with a magnification of ×2000. How long should the drawing be, in mm?",
    "solutions": [14], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Multiply magnification by actual size, then convert μm to mm.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "Image size = 2000 × 7 = 14,000 μm. The question asks for mm: 14,000 ÷ 1000 = 14 mm.", "expect": 14000},
        {"pattern": "wrong_rearrangement", "message": "The image is the unknown, so multiply: image = magnification × actual = 2000 × 7 = 14,000 μm = 14 mm.", "expect": 0.0035}
    ],
    "guided_steps": [
        say("The unknown is the image size, so rearrange: \\(\\text{image size} = \\text{magnification} \\times \\text{actual size}\\). That gives μm; convert to mm at the end."),
        box("Image in μm: 2000 × 7 = ", 14000, "Magnification × actual size."),
        box("Convert to mm: 14000 ÷ 1000 = ", 14, "1000 μm = 1 mm.", done="14 mm.", phase="substitute"),
        box("Check: 14 × 1000 ÷ 7 = ", 2000, "Back to μm, then ÷ actual recovers the magnification.", done="Recovers ×2000, so 14 mm is right.", phase="substitute")
    ]
})

# S3
silver.append({
    "unit": "μm", "display": "A micrograph shows a sperm cell head as 8 mm across at ×5000 magnification. Calculate the actual size of the sperm head in μm.",
    "solutions": [1.6], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{magnification} = \\frac{\\text{image size}}{\\text{actual size}}\\)",
    "hint": "Convert the image to μm, then divide by the magnification.",
    "misconceptions": [
        {"pattern": "wrong_rearrangement", "message": "Actual = image ÷ magnification, not image × magnification. 8000 ÷ 5000 = 1.6 μm.", "expect": 40000000}
    ],
    "guided_steps": [
        say("The unknown is the actual size, so rearrange: actual = image ÷ magnification. Convert the image to μm first."),
        box("Image in μm: 8 × 1000 = ", 8000, "1 mm = 1000 μm."),
        box("Actual size: 8000 ÷ 5000 = ", 1.6, "Image ÷ magnification.", done="1.6 μm.", phase="substitute"),
        box("Check: 1.6 × 5000 = ", 8000, "Actual × magnification recovers the image.", done="Recovers 8000 μm, so 1.6 μm is right.", phase="substitute")
    ]
})

# S4 (standard form)
silver.append({
    "display": "An E. coli bacterium is 2 μm long. Express this length in metres, giving your answer in standard form.",
    "solutions": [2, -6], "calculator": False, "input_type": "standard_form",
    "equation_hint": "\\(1 \\text{ μm} = 1 \\times 10^{-6} \\text{ m}\\)",
    "hint": "1 μm = 10⁻⁶ m, so the power of 10 is −6.",
    "misconceptions": [
        {"pattern": "wrong_power", "message": "1 μm = 10⁻⁶ m, so 2 μm = 2 × 10⁻⁶ m. The exponent is −6, not −3 (that would be mm).", "expect": [2, -3]}
    ],
    "guided_steps": [
        say("Convert micrometres to metres: 1 μm = \\(10^{-6}\\) m. Then write it in standard form."),
        box("1 μm in metres is 10 to the power ", -6, "Micro means a millionth, 10⁻⁶."),
        box("The number in front (between 1 and 10) is ", 2, "2 μm gives 2 in front.", phase="substitute"),
        box("and the power of 10 is ", -6, "The same power as the μm-to-metre step.", done="So 2 × 10⁻⁶ m.", phase="substitute")
    ]
})

# S5
silver.append({
    "unit": "μm", "display": "A palisade cell is 0.035 mm long. Convert this to μm.",
    "solutions": [35], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(1 \\text{ mm} = 1000 \\text{ μm}\\)",
    "hint": "Going to a smaller unit, multiply by 1000.",
    "misconceptions": [
        {"pattern": "wrong_direction", "message": "mm to μm means multiply by 1000: 0.035 × 1000 = 35 μm.", "expect": 0.000035},
        {"pattern": "decimal_error", "message": "Move the decimal point exactly three places right: 0.035 × 1000 = 35, not 3.5.", "expect": 3.5}
    ],
    "guided_steps": [
        say("mm to μm is going to a smaller unit, so you multiply by 1000."),
        box("μm in 1 mm: ", 1000, "Milli to micro is a factor of 1000."),
        box("0.035 × 1000 = ", 35, "Move the decimal point three places right.", done="35 μm.", phase="substitute"),
        box("Check: 35 ÷ 1000 = ", 0.035, "Dividing back returns the mm value.", done="Back to 0.035 mm, so 35 μm is right.", phase="substitute")
    ]
})

pb["silver"] = silver

# ---- GOLD ----
gold = []

# G0 (standard form)
gold.append({
    "display": "A ribosome has a diameter of 25 nm. Express this in metres, giving your answer in standard form.",
    "solutions": [2.5, -8], "calculator": False, "input_type": "standard_form",
    "hint": "1 nm = 10⁻⁹ m, then tidy to one digit before the decimal point.",
    "misconceptions": [
        {"pattern": "wrong_power", "message": "25 nm = 25 × 10⁻⁹ m = 2.5 × 10⁻⁸ m. Raising 25 to 2.5 lifts the power by one, so −9 becomes −8.", "expect": [2.5, -9]},
        {"pattern": "unit_confusion", "message": "nm is 10⁻⁹ m, not 10⁻⁶ (that is μm). 25 nm = 2.5 × 10⁻⁸ m, not 2.5 × 10⁻⁵.", "expect": [2.5, -5]}
    ],
    "guided_steps": [
        say("1 nm = \\(10^{-9}\\) m, so 25 nm = 25 × 10⁻⁹ m. Then tidy to proper standard form (one digit before the point)."),
        box("1 nm in metres is 10 to the power ", -9, "Nano means 10⁻⁹."),
        box("In proper standard form the number in front is ", 2.5, "25 = 2.5 × 10, so 25 × 10⁻⁹ = 2.5 × 10⁻⁸.", phase="substitute"),
        box("and the power of 10 is ", -8, "Turning 25 into 2.5 lifts the power by one: −9 becomes −8.", done="So 2.5 × 10⁻⁸ m.", phase="substitute")
    ]
})

# G1
gold.append({
    "unit": "μm", "display": "An electron micrograph shows a mitochondrion at ×40,000 magnification. The image is 80 mm long. Calculate the actual length in μm.",
    "solutions": [2], "calculator": True, "input_type": "single_value",
    "hint": "Convert the image to μm, then divide by the magnification.",
    "misconceptions": [
        {"pattern": "wrong_rearrangement", "message": "Actual = image ÷ magnification, not image × magnification. 80,000 ÷ 40,000 = 2 μm.", "expect": 3200000000},
        {"pattern": "unit_error", "message": "Convert the image to μm first: 80 mm = 80,000 μm. Then 80,000 ÷ 40,000 = 2 μm.", "expect": 0.002}
    ],
    "guided_steps": [
        say("The unknown is the actual size, so rearrange: actual = image ÷ magnification. Convert the image to μm first."),
        box("Image in μm: 80 × 1000 = ", 80000, "1 mm = 1000 μm."),
        box("Actual size: 80000 ÷ 40000 = ", 2, "Image ÷ magnification.", done="2 μm.", phase="substitute"),
        box("Check: 2 × 40000 = ", 80000, "Actual × magnification recovers the image.", done="Recovers 80,000 μm, so 2 μm is right.", phase="substitute")
    ]
})

# G2
gold.append({
    "unit": "", "accept": 0.05,
    "display": "A white blood cell has an actual diameter of 12 μm. A red blood cell has an actual diameter of 7 μm. How many times wider is the white blood cell than the red blood cell? Give your answer to 1 decimal place.",
    "solutions": [1.7], "calculator": True, "input_type": "single_value",
    "hint": "How many times bigger means divide the larger by the smaller.",
    "misconceptions": [
        {"pattern": "inverted", "message": "Divide the larger by the smaller: 12 ÷ 7 = 1.7. Dividing 7 ÷ 12 gives about 0.6.", "expect": 0.6},
        {"pattern": "subtracted", "message": "How many times wider means divide, not subtract: 12 ÷ 7 ≈ 1.7, not 12 − 7 = 5.", "expect": 5}
    ],
    "guided_steps": [
        say("How many times wider means divide the larger diameter by the smaller. Both are already in μm."),
        box("Which value goes on top? The larger diameter = ", 12, "Wider means the bigger one over the smaller."),
        box("12 ÷ 7 to 1 d.p. = ", 1.7, "12 ÷ 7 = 1.714..., round to 1 d.p.", done="1.7 times wider.", phase="substitute"),
        box("Check: 1.7 × 7 = ", 11.9, "About 12, confirming the ratio.", done="≈12 μm, so 1.7 times is right.", phase="substitute")
    ]
})

# G3 (MC)
gold.append({
    "display": "A student measures an image of a cell as 45 mm. The actual cell is 0.015 mm. Calculate the magnification, then determine if this cell is likely to be a bacterium (1–5 μm), an animal cell (10–30 μm), or a plant cell (10–100 μm).",
    "options": ["×3000, bacterium", "×3000, animal cell", "×3000, plant cell", "×300, bacterium"],
    "solutions": [1], "calculator": True, "input_type": "multiple_choice",
    "hint": "Magnification = image ÷ actual, then convert the actual size to μm to name the cell.",
    "misconceptions": [
        {"pattern": "wrong_calc", "message": "Magnification = 45 ÷ 0.015 = 3000. Actual size = 0.015 mm = 15 μm, which fits an animal cell (10–30 μm).", "expect": None},
        {"pattern": "unit_error", "message": "0.015 mm = 15 μm (×1000). 15 μm is too big for a bacterium (1–5 μm); it fits an animal cell.", "expect": None}
    ]
})

# G4
gold.append({
    "unit": "", "display": "A virus is 300 nm in diameter. An electron microscope produces an image 18 mm across. Calculate the magnification.",
    "solutions": [60000], "calculator": True, "input_type": "single_value",
    "hint": "Convert the image all the way to nm, then divide by the actual size.",
    "misconceptions": [
        {"pattern": "unit_error", "message": "The actual size is in nm, so convert the image to nm too: 18 mm = 18,000,000 nm. Converting only to μm (18,000) and dividing by 300 wrongly gives 60.", "expect": 60},
        {"pattern": "wrong_conversion", "message": "1 mm = 1,000,000 nm, so 18 mm = 18,000,000 nm. Magnification = 18,000,000 ÷ 300 = ×60,000.", "expect": 0.06}
    ],
    "guided_steps": [
        say("Magnification = image ÷ actual with both in the same unit. The actual size is in nm, so convert the image all the way to nm."),
        box("Image in μm: 18 × 1000 = ", 18000, "1 mm = 1000 μm."),
        box("Now in nm: 18000 × 1000 = ", 18000000, "1 μm = 1000 nm."),
        box("Magnification: 18000000 ÷ 300 = ", 60000, "Image ÷ actual.", done="×60,000.", phase="substitute"),
        box("Check: 60000 × 300 = ", 18000000, "Magnification × actual recovers the image in nm.", done="Recovers 18,000,000 nm, so ×60,000 is right.", phase="substitute")
    ]
})

# G5 (MC)
gold.append({
    "display": "A student measures the image of a bacterial cell as 14 mm under ×4000 magnification. Another student measures the image of a plant cell as 48 mm under ×800 magnification. Which cell has the larger actual size, and by how many μm?",
    "options": ["Plant cell, larger by 56.5 μm", "Bacterial cell, larger by 56.5 μm", "Plant cell, larger by 3.5 μm", "They are the same size"],
    "solutions": [0], "calculator": True, "input_type": "multiple_choice",
    "hint": "Work out each actual size, then compare those, not the image sizes.",
    "misconceptions": [
        {"pattern": "wrong_calc", "message": "Bacterium: 14 mm = 14,000 μm, actual = 14,000 ÷ 4000 = 3.5 μm. Plant: 48 mm = 48,000 μm, actual = 48,000 ÷ 800 = 60 μm. Difference = 60 − 3.5 = 56.5 μm.", "expect": None},
        {"pattern": "compared_images", "message": "Compare actual sizes, not image sizes. A larger image at a higher magnification can still be a smaller cell.", "expect": None}
    ]
})

pb["gold"] = gold

pd["problem_bank"] = pb
pd["related_videos"] = []

# ---------- worked_examples (preserved from canonical) ----------
canon = json.load(io.open("bds01_canonical_raw.json", encoding="utf-8"))
we = canon["worked_examples"]
# preserve content; only swap em dashes (validator + house style) in labels
def deemdash(obj):
    if isinstance(obj, dict):
        return {k: deemdash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deemdash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ", ")
    return obj
pd["worked_examples"] = deemdash(we)

with io.open("lesson_biology-data-skills-L01@d923f94f54.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

print("written. keys:", list(pd.keys()))
