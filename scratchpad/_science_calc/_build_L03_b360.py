# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L03_b360_live.json", encoding="utf-8"))

# ---------- method_card (slim, <=140 words, <=4 steps) ----------
method_card = {
    "title": "Titrations, Concentration and the Mole",
    "steps": [
        "Convert every volume from cm³ to dm³ by dividing by 1000",
        "Find the moles of the substance you know fully: n = cV",
        "Use the balanced equation's mole ratio to get moles of the unknown",
        "Divide those moles by that solution's volume: c = n ÷ V",
    ],
    "content": (
        "<p>Titration sums follow one chain. The key equation is \\(n = cV\\): "
        "moles = concentration (mol/dm³) × volume (dm³).</p>"
        "<p>Volumes are usually in cm³, so divide by 1000 first. Then find the "
        "moles of the solution you know, use the balanced equation's mole ratio to "
        "get moles of the unknown, and divide by that solution's volume in dm³.</p>"
        "<p>Watch the ratio: a 1:2 equation is not 1:1. To swap between mol/dm³ "
        "and g/dm³, multiply or divide by \\(M_r\\).</p>"
    ),
}

# ---------- tier descriptions ----------
bronze_desc = ("One equation, one step: use n = cV, c = n ÷ V, or V = n ÷ c. "
               "Convert cm³ to dm³ by dividing by 1000, then substitute.")
silver_desc = ("A full titration: find moles of the solution you know, apply the "
               "balanced equation's mole ratio, then divide by the other volume.")
gold_desc = ("Multi-step problems: work back from a mass or a dilution, chain two or "
             "three calculations, and keep every volume in dm³ until the end.")

# ---------- guided.opener (counting by weighing) ----------
opener = {
    "label": "Before any chemistry",
    "display": ("Picture a sealed money bag stuffed with identical £1 coins.<br>"
                "You cannot open it, but you have kitchen scales."),
    "steps": [
        {
            "say": "The whole bag of coins weighs 180 g. One £1 coin weighs 9 g. "
                   "How many coins are in the bag?",
            "pre": "Number of coins = 180 ÷ 9 = ",
            "post": "",
            "answer": 20,
            "hint": "Divide the total weight by the weight of one coin.",
        },
        {
            "say": "You just counted objects you could not see by weighing them. Now "
                   "share those 20 coins equally into 4 jars.",
            "pre": "Coins in each jar = 20 ÷ 4 = ",
            "post": "",
            "answer": 5,
            "hint": "Share the coins equally between the jars.",
        },
        {
            "say": "Chemists cannot count atoms one by one either, so they weigh them: "
                   "<strong>moles = mass ÷ mass of one mole</strong> (that is \\(M_r\\)). "
                   "And concentration is just those moles shared through the liquid: "
                   "\\(c = n ÷ V\\). The same two moves you just did with coins.",
        },
    ],
}

# ---------- guided.teach walks ----------
teach = {
    "bronze": {
        "label": "Together: your first one",
        "display": "A solution has a concentration of 0.2 mol/dm³. Calculate the number of moles in 50 cm³ of it.",
        "steps": [
            {
                "say": "The equation is \\(n = cV\\), with V in dm³. Check whether your "
                       "board gives you this equation; either way it is worth knowing.",
                "pre": "First, how many cm³ are in 1 dm³? ",
                "post": "",
                "answer": 1000,
                "hint": "1 dm³ = 1000 cm³.",
            },
            {
                "pre": "So the volume in dm³ = 50 ÷ 1000 = ",
                "post": "",
                "answer": 0.05,
                "hint": "Divide cm³ by 1000.",
            },
            {
                "say": "Now substitute into \\(n = cV\\).",
                "pre": "moles = 0.2 × 0.05 = ",
                "post": "",
                "answer": 0.01,
                "hint": "Multiply concentration by volume in dm³.",
            },
            {
                "pre": "Check by dividing back: 0.01 ÷ 0.05 = ",
                "post": "",
                "answer": 0.2,
                "done": "Back to the 0.2 mol/dm³ you started with, so the answer is 0.01 mol.",
                "hint": "Divide moles by volume; you should get the original concentration.",
            },
        ],
    },
    "silver": {
        "label": "Together: a full titration",
        "display": ("20.0 cm³ of KOH is exactly neutralised by 25.0 cm³ of 0.10 mol/dm³ HCl. "
                    "KOH + HCl → KCl + H₂O. Calculate the concentration of the KOH."),
        "steps": [
            {
                "say": "Start with the HCl, the solution you know fully. Convert its volume.",
                "pre": "HCl volume in dm³ = 25.0 ÷ 1000 = ",
                "post": "",
                "answer": 0.025,
                "hint": "Divide cm³ by 1000.",
            },
            {
                "pre": "moles HCl = 0.10 × 0.025 = ",
                "post": "",
                "answer": 0.0025,
                "hint": "Multiply concentration by volume in dm³.",
            },
            {
                "say": "The equation is 1:1, so moles of KOH also equal 0.0025. Convert the KOH volume.",
                "pre": "KOH volume in dm³ = 20.0 ÷ 1000 = ",
                "post": "",
                "answer": 0.02,
                "hint": "Divide cm³ by 1000.",
            },
            {
                "pre": "concentration KOH = 0.0025 ÷ 0.02 = ",
                "post": "",
                "answer": 0.125,
                "done": "So the KOH is 0.125 mol/dm³.",
                "hint": "Divide moles by the KOH volume in dm³.",
            },
        ],
    },
    "gold": {
        "label": "Together: work back to a mass",
        "display": ("A student makes 250 cm³ of NaOH solution. A 25.0 cm³ portion is neutralised "
                    "by 30.0 cm³ of 0.10 mol/dm³ HCl. NaOH + HCl → NaCl + H₂O. "
                    "Calculate the mass of NaOH used. (Ar: Na = 23, O = 16, H = 1)"),
        "steps": [
            {
                "say": "Work from the HCl, then back to a mass. Convert the HCl volume.",
                "pre": "HCl volume in dm³ = 30.0 ÷ 1000 = ",
                "post": "",
                "answer": 0.03,
                "hint": "Divide cm³ by 1000.",
            },
            {
                "pre": "moles HCl = 0.10 × 0.03 = ",
                "post": "",
                "answer": 0.003,
                "hint": "Multiply concentration by volume in dm³.",
            },
            {
                "say": "1:1 ratio, so moles NaOH in the 25.0 cm³ sample = 0.003. "
                       "The sample is 25.0 ÷ 1000 = 0.025 dm³.",
                "pre": "concentration NaOH = 0.003 ÷ 0.025 = ",
                "post": "",
                "answer": 0.12,
                "hint": "Divide moles by the sample volume in dm³.",
            },
            {
                "say": "That concentration fills the whole 250 cm³ (0.25 dm³) flask.",
                "pre": "total moles NaOH = 0.12 × 0.25 = ",
                "post": "",
                "answer": 0.03,
                "hint": "Multiply concentration by the flask volume in dm³.",
            },
            {
                "pre": "mass = moles × Mr = 0.03 × 40 = ",
                "post": "",
                "answer": 1.2,
                "done": "Mr of NaOH is 40, so the mass used is 1.2 g.",
                "hint": "Mr of NaOH = 23 + 16 + 1 = 40.",
            },
        ],
    },
}

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: one equation, one step",
        "steps": [
            "Pick the right form of the mole equation: \\(n = cV\\) for moles, "
            "\\(c = n ÷ V\\) for concentration, \\(V = n ÷ c\\) for volume.",
            "If a volume is in cm³, divide by 1000 to get dm³ before you substitute.",
            "For a mass, use \\(n = mass ÷ M_r\\). To swap mol/dm³ and g/dm³, "
            "multiply or divide by \\(M_r\\).",
        ],
        "example": {
            "question": "A solution has a concentration of 0.4 mol/dm³. Calculate the moles in 100 cm³.",
            "steps": [
                {"label": "Convert the volume", "content": "<p>100 ÷ 1000 = 0.1 dm³</p>"},
                {"label": "Substitute into n = cV", "content": "<p>n = 0.4 × 0.1</p>"},
                {"label": "Answer", "content": "<p><strong>0.04 mol</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: a full titration",
        "steps": [
            "Find the moles of the solution you know everything about: convert its "
            "volume to dm³, then \\(n = cV\\).",
            "Read the mole ratio straight from the balanced equation. A 1:2 equation "
            "means halve or double, not leave it 1:1.",
            "Convert the other solution's volume to dm³ and divide its moles by it: "
            "\\(c = n ÷ V\\).",
        ],
        "example": {
            "question": ("20.0 cm³ of HCl is neutralised by 25.0 cm³ of 0.10 mol/dm³ NaOH. "
                         "HCl + NaOH → NaCl + H₂O. Find the concentration of the HCl."),
            "steps": [
                {"label": "Moles of NaOH", "content": "<p>25.0 ÷ 1000 = 0.025 dm³; n = 0.10 × 0.025 = 0.0025 mol</p>"},
                {"label": "Mole ratio", "content": "<p>1:1, so moles HCl = 0.0025 mol</p>"},
                {"label": "Concentration of HCl", "content": "<p>20.0 ÷ 1000 = 0.02 dm³; c = 0.0025 ÷ 0.02</p>"},
                {"label": "Answer", "content": "<p><strong>0.125 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain the steps",
        "steps": [
            "These start from a mass or a dilution, so plan the chain before you begin.",
            "Typical route: mass to moles, to concentration in the flask, to moles in "
            "the sample, then mole ratio, then the unknown.",
            "Keep every volume in dm³, carry full accuracy through, and round only at the very end.",
        ],
        "example": {
            "question": ("4.0 g of NaOH (Mr 40) is made up to 200 cm³. A 25.0 cm³ sample is "
                         "titrated with HCl; the titre is 25.0 cm³. NaOH + HCl → NaCl + H₂O. "
                         "Find the concentration of the HCl."),
            "steps": [
                {"label": "Moles and flask concentration", "content": "<p>n = 4.0 ÷ 40 = 0.1 mol; 200 ÷ 1000 = 0.2 dm³; c = 0.1 ÷ 0.2 = 0.5 mol/dm³</p>"},
                {"label": "Moles in the sample", "content": "<p>25.0 ÷ 1000 = 0.025 dm³; n = 0.5 × 0.025 = 0.0125 mol</p>"},
                {"label": "Concentration of HCl", "content": "<p>1:1 ratio; titre 25.0 ÷ 1000 = 0.025 dm³; c = 0.0125 ÷ 0.025</p>"},
                {"label": "Answer", "content": "<p><strong>0.5 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided_steps per bank problem ----------
GS = {}

GS["b0"] = [  # B1: conc 0.1, moles in 25 cm3 -> 0.0025
    {"say": "You know the concentration and the volume, so use \\(n = cV\\). But V must be in dm³ first."},
    {"pre": "Volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "moles = 0.1 × 0.025 = ", "post": "", "answer": 0.0025, "hint": "Multiply concentration by volume in dm³."},
    {"pre": "Check: 0.0025 ÷ 0.025 = ", "post": "", "answer": 0.1, "done": "Back to the concentration you started with, so the answer is 0.0025 mol.", "hint": "Divide moles by volume; you should get the original concentration."},
]

GS["b1"] = [  # B2: 0.5 mol in 0.25 dm3 -> c=2
    {"say": "The volume is already in dm³, so go straight to \\(c = n ÷ V\\)."},
    {"pre": "As a check the volume 0.25 dm³ = 0.25 × 1000 = ", "post": " cm³", "answer": 250, "hint": "Multiply dm³ by 1000."},
    {"phase": "substitute", "pre": "concentration = 0.5 ÷ 0.25 = ", "post": "", "answer": 2, "hint": "Divide the moles by the volume in dm³."},
    {"pre": "Check: 2 × 0.25 = ", "post": "", "answer": 0.5, "done": "That is the moles you started with, so the answer is 2 mol/dm³.", "hint": "Multiply back; you should get 0.5 mol."},
]

GS["b2"] = [  # B3: conc 0.5, V for 0.2 mol -> 0.4
    {"say": "You want a volume, so rearrange to \\(V = n ÷ c\\)."},
    {"pre": "The moles you need go on top. moles = ", "post": "", "answer": 0.2, "hint": "The amount asked for, in mol."},
    {"phase": "substitute", "pre": "volume = 0.2 ÷ 0.5 = ", "post": "", "answer": 0.4, "hint": "Divide moles by concentration."},
    {"pre": "Check: 0.5 × 0.4 = ", "post": "", "answer": 0.2, "done": "That is the 0.2 mol asked for, so the answer is 0.4 dm³.", "hint": "Multiply concentration by your volume; you should get 0.2 mol."},
]

GS["b3"] = [  # B4: 4.0 g NaOH -> moles 0.1
    {"say": "You are given a mass, so use \\(n = mass ÷ M_r\\). The volume is not needed here."},
    {"pre": "Work out Mr of NaOH: 23 + 16 + 1 = ", "post": "", "answer": 40, "hint": "Add the Ar values: Na 23, O 16, H 1."},
    {"phase": "substitute", "pre": "moles = 4.0 ÷ 40 = ", "post": "", "answer": 0.1, "hint": "Divide the mass by Mr."},
    {"pre": "Check: 0.1 × 40 = ", "post": "", "answer": 4, "done": "That is the 4.0 g you started with, so the answer is 0.1 mol.", "hint": "Multiply moles by Mr; you should get the mass back."},
]

GS["b4"] = [  # B5: 0.15 mol in 500 cm3 -> 0.3
    {"say": "\\(c = n ÷ V\\), but the volume is in cm³, so convert it first."},
    {"pre": "Volume in dm³ = 500 ÷ 1000 = ", "post": "", "answer": 0.5, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "concentration = 0.15 ÷ 0.5 = ", "post": "", "answer": 0.3, "hint": "Divide moles by volume in dm³."},
    {"pre": "Check: 0.3 × 0.5 = ", "post": "", "answer": 0.15, "done": "That is the moles you started with, so the answer is 0.3 mol/dm³.", "hint": "Multiply back; you should get 0.15 mol."},
]

GS["b5"] = [  # B6: NaCl 0.25 mol/dm3 -> g/dm3 14.625
    {"say": "To turn mol/dm³ into g/dm³, multiply by \\(M_r\\)."},
    {"pre": "Mr of NaCl = 23 + 35.5 = ", "post": "", "answer": 58.5, "hint": "Add Ar: Na 23, Cl 35.5."},
    {"phase": "substitute", "pre": "concentration in g/dm³ = 0.25 × 58.5 = ", "post": "", "answer": 14.625, "hint": "Multiply the mol/dm³ value by Mr."},
    {"pre": "Check by dividing back: 14.625 ÷ 58.5 = ", "post": "", "answer": 0.25, "done": "Back to 0.25 mol/dm³, so the answer is 14.625 g/dm³.", "hint": "Divide by Mr; you should return to 0.25 mol/dm³."},
]

GS["s0"] = [  # S1: 25 NaOH unknown, 20 cm3 0.125 HCl 1:1 -> 0.1
    {"say": "Start with the HCl, the solution you know everything about. Convert its volume and find its moles."},
    {"pre": "HCl volume in dm³ = 20.0 ÷ 1000 = ", "post": "", "answer": 0.02, "hint": "Divide cm³ by 1000."},
    {"pre": "moles HCl = 0.125 × 0.02 = ", "post": "", "answer": 0.0025, "hint": "Multiply concentration by volume in dm³."},
    {"say": "HCl + NaOH → NaCl + H₂O is 1:1, so moles of NaOH equal moles of HCl."},
    {"phase": "substitute", "pre": "NaOH volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration NaOH = 0.0025 ÷ 0.025 = ", "post": "", "answer": 0.1, "hint": "Divide moles by the NaOH volume in dm³."},
    {"pre": "Check: 0.1 × 0.025 = ", "post": "", "answer": 0.0025, "done": "That returns the NaOH moles, matching the HCl 1:1, so the answer is 0.1 mol/dm³.", "hint": "Multiply back; you should get 0.0025 mol."},
]

GS["s1"] = [  # S2: 25 cm3 0.2 NaOH, 20 cm3 H2SO4 1:2 -> 0.125
    {"say": "Here you know the NaOH fully. Convert its volume and find its moles."},
    {"pre": "NaOH volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "moles NaOH = 0.2 × 0.025 = ", "post": "", "answer": 0.005, "hint": "Multiply concentration by volume in dm³."},
    {"say": "H₂SO₄ + 2NaOH shows 1 acid for every 2 NaOH, so divide the NaOH moles by 2."},
    {"phase": "substitute", "pre": "moles H₂SO₄ = 0.005 ÷ 2 = ", "post": "", "answer": 0.0025, "hint": "One H₂SO₄ reacts with two NaOH, so halve."},
    {"pre": "H₂SO₄ volume in dm³ = 20.0 ÷ 1000 = ", "post": "", "answer": 0.02, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration H₂SO₄ = 0.0025 ÷ 0.02 = ", "post": "", "answer": 0.125, "hint": "Divide moles by volume in dm³."},
    {"pre": "Check: 0.125 × 0.02 = ", "post": "", "answer": 0.0025, "done": "That is the acid moles, half the NaOH as the ratio needs, so the answer is 0.125 mol/dm³.", "hint": "Multiply back; you should get 0.0025 mol."},
]

GS["s2"] = [  # S3: 25 cm3 0.15 HCl, 18.75 cm3 NaOH 1:1 -> 0.2
    {"say": "You know the HCl fully. Convert its volume and find its moles."},
    {"pre": "HCl volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "moles HCl = 0.15 × 0.025 = ", "post": "", "answer": 0.00375, "hint": "Multiply concentration by volume in dm³."},
    {"say": "The ratio is 1:1, so moles of NaOH also equal 0.00375. For the last step use the NaOH volume, not the HCl volume."},
    {"phase": "substitute", "pre": "NaOH volume in dm³ = 18.75 ÷ 1000 = ", "post": "", "answer": 0.01875, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration NaOH = 0.00375 ÷ 0.01875 = ", "post": "", "answer": 0.2, "hint": "Divide the moles by the NaOH volume."},
    {"pre": "Check: 0.2 × 0.01875 = ", "post": "", "answer": 0.00375, "done": "That returns the NaOH moles, matching the HCl 1:1, so the answer is 0.2 mol/dm³.", "hint": "Multiply back; you should get 0.00375 mol."},
]

GS["s3"] = [  # S4: NaOH in 250 cm3, 25 titrated 20 cm3 0.2 HNO3 1:1 -> mass 1.6
    {"say": "Work from the HNO₃, which you know fully. Convert its volume and find its moles."},
    {"pre": "HNO₃ volume in dm³ = 20.0 ÷ 1000 = ", "post": "", "answer": 0.02, "hint": "Divide cm³ by 1000."},
    {"pre": "moles HNO₃ = 0.2 × 0.02 = ", "post": "", "answer": 0.004, "hint": "Multiply concentration by volume in dm³."},
    {"say": "1:1 ratio, so moles NaOH in the 25.0 cm³ sample = 0.004. First find the NaOH concentration."},
    {"pre": "sample volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration NaOH = 0.004 ÷ 0.025 = ", "post": "", "answer": 0.16, "hint": "Divide moles by the sample volume."},
    {"say": "That concentration is the same throughout the 250 cm³ flask. Scale up to the whole flask."},
    {"phase": "substitute", "pre": "total moles in 250 cm³ (0.25 dm³) = 0.16 × 0.25 = ", "post": "", "answer": 0.04, "hint": "Multiply concentration by the flask volume in dm³."},
    {"pre": "mass = moles × Mr = 0.04 × 40 = ", "post": "", "answer": 1.6, "hint": "Mr of NaOH is 40."},
    {"pre": "Check: 1.6 ÷ 40 = ", "post": "", "answer": 0.04, "done": "That is the total moles in the flask, so the answer is 1.6 g.", "hint": "Divide the mass by Mr; you should get 0.04 mol."},
]

GS["s4"] = [  # S5: 25 cm3 0.1 Ca(OH)2, 20 cm3 HCl 1:2 -> 0.25
    {"say": "You know the Ca(OH)₂ fully. Convert its volume and find its moles."},
    {"pre": "Ca(OH)₂ volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "moles Ca(OH)₂ = 0.1 × 0.025 = ", "post": "", "answer": 0.0025, "hint": "Multiply concentration by volume in dm³."},
    {"say": "Ca(OH)₂ + 2HCl shows 2 HCl for every 1 Ca(OH)₂, so double the moles."},
    {"phase": "substitute", "pre": "moles HCl = 0.0025 × 2 = ", "post": "", "answer": 0.005, "hint": "Two HCl per Ca(OH)₂, so multiply by 2."},
    {"pre": "HCl volume in dm³ = 20.0 ÷ 1000 = ", "post": "", "answer": 0.02, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration HCl = 0.005 ÷ 0.02 = ", "post": "", "answer": 0.25, "hint": "Divide moles by volume in dm³."},
    {"pre": "Check: 0.25 × 0.02 = ", "post": "", "answer": 0.005, "done": "That is the HCl moles, twice the Ca(OH)₂ as the ratio needs, so the answer is 0.25 mol/dm³.", "hint": "Multiply back; you should get 0.005 mol."},
]

GS["g0"] = [  # G1: 2.0 g NaOH Mr40 -> 200 cm3, 25 titrated titre 31.25 1:1 -> HCl 0.2
    {"say": "Start at the very beginning: the solid NaOH. Find its moles, then its concentration in the flask."},
    {"pre": "moles NaOH = mass ÷ Mr = 2.0 ÷ 40 = ", "post": "", "answer": 0.05, "hint": "Divide the mass by Mr."},
    {"pre": "flask volume in dm³ = 200 ÷ 1000 = ", "post": "", "answer": 0.2, "hint": "Divide cm³ by 1000."},
    {"pre": "flask concentration of NaOH = 0.05 ÷ 0.2 = ", "post": "", "answer": 0.25, "hint": "Divide moles by volume."},
    {"say": "Only 25.0 cm³ of this is titrated. Find the moles of NaOH in that sample."},
    {"pre": "sample volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "moles NaOH in sample = 0.25 × 0.025 = ", "post": "", "answer": 0.00625, "hint": "Multiply the flask concentration by the sample volume."},
    {"say": "1:1 ratio, so moles of HCl = 0.00625. The titre was 31.25 cm³."},
    {"pre": "titre volume in dm³ = 31.25 ÷ 1000 = ", "post": "", "answer": 0.03125, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration HCl = 0.00625 ÷ 0.03125 = ", "post": "", "answer": 0.2, "hint": "Divide moles by the titre volume."},
    {"pre": "Check: 0.2 × 0.03125 = ", "post": "", "answer": 0.00625, "done": "That returns the HCl moles, equal to the NaOH sample 1:1, so the answer is 0.2 mol/dm³.", "hint": "Multiply back; you should get 0.00625 mol."},
]

GS["g1"] = [  # G2: 5.3 g Na2CO3 -> 250 cm3, 25 titrated titre 25 1:2 -> HCl 0.4
    {"say": "Begin with the solid Na₂CO₃. Find its Mr, then its moles, then the flask concentration."},
    {"pre": "Mr Na₂CO₃ = (2 × 23) + 12 + (3 × 16) = ", "post": "", "answer": 106, "hint": "46 + 12 + 48."},
    {"pre": "moles Na₂CO₃ = 5.3 ÷ 106 = ", "post": "", "answer": 0.05, "hint": "Divide mass by Mr."},
    {"pre": "flask volume in dm³ = 250 ÷ 1000 = ", "post": "", "answer": 0.25, "hint": "Divide cm³ by 1000."},
    {"pre": "flask concentration = 0.05 ÷ 0.25 = ", "post": "", "answer": 0.2, "hint": "Divide moles by volume."},
    {"say": "A 25.0 cm³ sample is titrated. Find the moles of Na₂CO₃ in it."},
    {"pre": "sample volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "moles Na₂CO₃ in sample = 0.2 × 0.025 = ", "post": "", "answer": 0.005, "hint": "Multiply flask concentration by sample volume."},
    {"say": "Na₂CO₃ + 2HCl is 1:2, so double for the HCl moles."},
    {"pre": "moles HCl = 0.005 × 2 = ", "post": "", "answer": 0.01, "hint": "Two HCl per carbonate."},
    {"pre": "titre volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration HCl = 0.01 ÷ 0.025 = ", "post": "", "answer": 0.4, "hint": "Divide moles by titre volume."},
    {"pre": "Check: 0.4 × 0.025 = ", "post": "", "answer": 0.01, "done": "That returns the HCl moles, twice the carbonate as the 1:2 ratio needs, so the answer is 0.4 mol/dm³.", "hint": "Multiply back; you should get 0.01 mol."},
]

GS["g2"] = [  # G3: mass HCl for 250 cm3 of 0.5 mol/dm3, Mr 36.5 -> 4.6 (1dp)
    {"say": "Work backwards from the concentration to a mass. Find the moles first, then use Mr."},
    {"pre": "volume in dm³ = 250 ÷ 1000 = ", "post": "", "answer": 0.25, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "moles HCl = 0.5 × 0.25 = ", "post": "", "answer": 0.125, "hint": "Multiply concentration by volume in dm³."},
    {"pre": "Mr of HCl = 1 + 35.5 = ", "post": "", "answer": 36.5, "hint": "Add Ar: H 1, Cl 35.5."},
    {"pre": "mass = moles × Mr = 0.125 × 36.5 = ", "post": "", "answer": 4.5625, "hint": "Multiply moles by Mr."},
    {"pre": "Check: 4.5625 ÷ 36.5 = ", "post": "", "answer": 0.125, "done": "That returns the 0.125 mol, so the mass is right. Rounded to 1 decimal place, the answer is 4.6 g.", "hint": "Divide by Mr; you should get 0.125 mol."},
]

GS["g3"] = [  # G4: KOH in 500 cm3, 25 titrated 20 cm3 0.1 HCl 1:1 -> mass 2.24, Mr 56
    {"say": "Work from the HCl, which you know fully, back to the mass of KOH."},
    {"pre": "HCl volume in dm³ = 20.0 ÷ 1000 = ", "post": "", "answer": 0.02, "hint": "Divide cm³ by 1000."},
    {"pre": "moles HCl = 0.1 × 0.02 = ", "post": "", "answer": 0.002, "hint": "Multiply concentration by volume in dm³."},
    {"say": "1:1 ratio, so moles KOH in the 25.0 cm³ sample = 0.002. Find the KOH concentration."},
    {"pre": "sample volume in dm³ = 25.0 ÷ 1000 = ", "post": "", "answer": 0.025, "hint": "Divide cm³ by 1000."},
    {"pre": "concentration KOH = 0.002 ÷ 0.025 = ", "post": "", "answer": 0.08, "hint": "Divide moles by the sample volume."},
    {"say": "That concentration fills the whole 500 cm³ flask. Scale up to find the total moles."},
    {"pre": "flask volume in dm³ = 500 ÷ 1000 = ", "post": "", "answer": 0.5, "hint": "Divide cm³ by 1000."},
    {"phase": "substitute", "pre": "total moles KOH = 0.08 × 0.5 = ", "post": "", "answer": 0.04, "hint": "Multiply concentration by flask volume."},
    {"pre": "mass = moles × Mr = 0.04 × 56 = ", "post": "", "answer": 2.24, "hint": "Mr of KOH = 39 + 16 + 1 = 56."},
    {"pre": "Check: 2.24 ÷ 56 = ", "post": "", "answer": 0.04, "done": "That is the total moles in the flask, so the answer is 2.24 g.", "hint": "Divide the mass by Mr; you should get 0.04 mol."},
]

# ---------- per-problem hints + misconception expects ----------
BRONZE_META = [
    ("Convert the volume to dm³, then multiply by the concentration.",
     [{"pattern": "unit_error", "check": "common", "expect": 2.5,
       "message": "Convert cm³ to dm³ first: 25.0 ÷ 1000 = 0.025 dm³. Then n = 0.1 × 0.025 = 0.0025 mol. Using 25 without converting gives 2.5, which is 1000 times too big."}]),
    ("Divide the moles by the volume in dm³.",
     [{"pattern": "inverse_error", "check": "common", "expect": 0.5,
       "message": "Concentration = moles ÷ volume = 0.5 ÷ 0.25 = 2 mol/dm³. Dividing the other way (0.25 ÷ 0.5) gives 0.5, which is upside down."}]),
    ("Rearrange to volume = moles ÷ concentration.",
     [{"pattern": "inverse_error", "check": "common", "expect": 2.5,
       "message": "Volume = moles ÷ concentration = 0.2 ÷ 0.5 = 0.4 dm³. Dividing 0.5 ÷ 0.2 gives 2.5, the wrong way round."}]),
    ("Find Mr, then divide the mass by it. Ignore the volume.",
     [{"pattern": "inverse_error", "check": "common", "expect": 10,
       "message": "Moles = mass ÷ Mr, not Mr ÷ mass. Mr of NaOH = 40, so moles = 4.0 ÷ 40 = 0.1 mol. Dividing the other way gives 10."}]),
    ("Convert 500 cm³ to dm³ first, then divide moles by volume.",
     [{"pattern": "unit_error", "check": "common", "expect": 0.0003,
       "message": "Convert volume first: 500 cm³ = 0.5 dm³. Concentration = 0.15 ÷ 0.5 = 0.3 mol/dm³. Using 500 without converting gives 0.0003, far too small."}]),
    ("Work out Mr of NaCl, then multiply the mol/dm³ value by it.",
     [{"pattern": "inverse_error", "check": "common", "expect": 0.00427,
       "message": "g/dm³ = mol/dm³ × Mr. Mr NaCl = 58.5, so 0.25 × 58.5 = 14.625 g/dm³. Dividing instead of multiplying gives about 0.00427."}]),
]

SILVER_META = [
    ("Find moles of HCl, apply the 1:1 ratio, then divide by the NaOH volume.",
     [{"pattern": "wrong_volume", "check": "common", "expect": 0.125,
       "message": "The final step must use the NaOH volume (25.0 cm³), not the HCl volume. Moles NaOH = 0.0025, so c = 0.0025 ÷ 0.025 = 0.1 mol/dm³. Using 0.02 dm³ gives 0.125."}]),
    ("Find moles of NaOH, then halve for H₂SO₄ using the 1:2 ratio.",
     [{"pattern": "mole_ratio", "check": "common", "expect": 0.25,
       "message": "H₂SO₄ : NaOH is 1:2, so halve the NaOH moles: 0.005 ÷ 2 = 0.0025 mol. Then c = 0.0025 ÷ 0.02 = 0.125 mol/dm³. Skipping the halving gives 0.25."}]),
    ("Find moles of HCl, then divide by the NaOH volume, 18.75 cm³.",
     [{"pattern": "wrong_volume", "check": "common", "expect": 0.15,
       "message": "Moles HCl = 0.00375, and the ratio is 1:1. Divide by the NaOH volume, 0.01875 dm³: 0.00375 ÷ 0.01875 = 0.2 mol/dm³. Using the HCl volume (0.025) gives 0.15."}]),
    ("Find the NaOH concentration, scale up to 250 cm³, then mass = n × Mr.",
     [{"pattern": "forgot_step", "check": "common", "expect": 0.16,
       "message": "The 25.0 cm³ sample holds only part of the NaOH. Scale up to the full 250 cm³: total moles = 0.16 × 0.25 = 0.04, so mass = 0.04 × 40 = 1.6 g. Using the sample moles alone gives 0.16 g."}]),
    ("Find moles of Ca(OH)₂, then double for HCl using the 1:2 ratio.",
     [{"pattern": "mole_ratio", "check": "common", "expect": 0.125,
       "message": "Ca(OH)₂ : HCl is 1:2, so double the moles: 0.0025 × 2 = 0.005 mol HCl. Then c = 0.005 ÷ 0.02 = 0.25 mol/dm³. Forgetting to double gives 0.125."}]),
]

GOLD_META = [
    ("Find the flask concentration, the moles in the 25 cm³ sample, then divide by the titre.",
     [{"pattern": "forgot_step", "check": "common", "expect": 1.6,
       "message": "Only 25.0 cm³ of the flask is titrated, not all of it. Moles NaOH in the sample = 0.25 × 0.025 = 0.00625, so c HCl = 0.00625 ÷ 0.03125 = 0.2 mol/dm³. Using all 0.05 mol against the titre gives 1.6."}]),
    ("Find Mr, the flask concentration, the sample moles, then apply the 1:2 ratio.",
     [{"pattern": "mole_ratio", "check": "common", "expect": 0.2,
       "message": "Na₂CO₃ : HCl is 1:2. Moles Na₂CO₃ in the sample = 0.005, so moles HCl = 0.01 and c = 0.01 ÷ 0.025 = 0.4 mol/dm³. Skipping the doubling gives 0.2."}]),
    ("Find the moles from n = cV, then mass = n × Mr. Round at the end.",
     [{"pattern": "forgot_convert", "check": "common", "expect": 4562.5,
       "message": "Convert the volume: 250 ÷ 1000 = 0.25 dm³. Moles = 0.5 × 0.25 = 0.125, mass = 0.125 × 36.5 = 4.6 g. Forgetting to convert (using 250) gives 4562.5."},
      {"pattern": "wrong_Mr", "check": "common", "expect": 4.4,
       "message": "Mr of HCl = 1 + 35.5 = 36.5, so mass = 0.125 × 36.5 = 4.6 g. Forgetting the hydrogen (using 35.5) gives 4.4 g."}]),
    ("Find the KOH concentration, scale up to 500 cm³, then mass = n × Mr.",
     [{"pattern": "forgot_step", "check": "common", "expect": 0.112,
       "message": "The 25.0 cm³ sample is only part of the flask. Scale up to 500 cm³: total moles = 0.08 × 0.5 = 0.04, so mass = 0.04 × 56 = 2.24 g. Using the sample moles alone gives 0.112 g."}]),
]

# ---------- assemble problem_bank ----------
pb = json.loads(json.dumps(live["problem_bank"]))  # deep copy

def apply(tier, meta, gskeys):
    probs = pb[tier]
    assert len(probs) == len(meta) == len(gskeys), (tier, len(probs), len(meta), len(gskeys))
    for p, (hint, misc), gk in zip(probs, meta, gskeys):
        p["hint"] = hint
        p["misconceptions"] = misc
        p["guided_steps"] = GS[gk]

apply("bronze", BRONZE_META, ["b0", "b1", "b2", "b3", "b4", "b5"])
apply("silver", SILVER_META, ["s0", "s1", "s2", "s3", "s4"])
apply("gold", GOLD_META, ["g0", "g1", "g2", "g3"])

pb["bronze_description"] = bronze_desc
pb["silver_description"] = silver_desc
pb["gold_description"] = gold_desc

# ---------- scrub em dashes from preserved fields (hard style gate) ----------
def scrub(o):
    if isinstance(o, dict):
        return {k: scrub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    if isinstance(o, str):
        return o.replace("— ", ": ").replace(" —", ":").replace("—", ": ")
    return o

exam_context = scrub(live["exam_context"])
worked_examples = scrub(live["worked_examples"])

# ---------- final object ----------
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "exam_context": exam_context,
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
}

json.dump(out, io.open("lesson_higher-calculations-L03@b360dedf84.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written")
