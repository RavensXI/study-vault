# Science Practice Data Schema

## Overview

Practice lessons for AQA Combined Science (8464) and Separate Sciences (8461/8462/8463).
Follows the same `practice_data` JSON structure as Maths practice lessons.

## AQA Physics Equation Reference

### Recall Equations (must memorise — NOT on the equation sheet)

| # | Name | Equation | Units |
|---|------|----------|-------|
| 1 | Weight | W = mg | N = kg × N/kg |
| 2 | Work done | W = Fs | J = N × m |
| 3 | Spring force (Hooke's law) | F = ke | N = N/m × m |
| 4 | Distance | s = vt | m = m/s × s |
| 5 | Acceleration | a = Δv / Δt | m/s² = m/s ÷ s |
| 6 | Force (Newton's 2nd law) | F = ma | N = kg × m/s² |
| 7 | Kinetic energy | Eₖ = ½mv² | J = kg × (m/s)² |
| 8 | Gravitational PE | Eₚ = mgh | J = kg × N/kg × m |
| 9 | Power (energy) | P = E/t | W = J ÷ s |
| 10 | Power (work) | P = W/t | W = J ÷ s |
| 11 | Efficiency (energy) | η = useful output / total input | decimal or % |
| 12 | Efficiency (power) | η = useful power out / total power in | decimal or % |
| 13 | Wave speed | v = fλ | m/s = Hz × m |
| 14 | Charge flow | Q = It | C = A × s |
| 15 | Ohm's law | V = IR | V = A × Ω |
| 16 | Electrical power | P = VI | W = V × A |
| 17 | Electrical power (alt) | P = I²R | W = A² × Ω |
| 18 | Energy transferred | E = Pt | J = W × s |
| 19 | Energy (charge) | E = QV | J = C × V |
| 20 | Density | ρ = m/V | kg/m³ = kg ÷ m³ |
| HT | Momentum | p = mv | kg m/s = kg × m/s |

### Given Equations (on the Physics equation sheet)

| Name | Equation | Notes |
|------|----------|-------|
| Kinematic (SUVAT) | v² − u² = 2as | HT only |
| Elastic PE | Eₑ = ½ke² | |
| Thermal energy (SHC) | ΔE = mcΔθ | |
| Period | T = 1/f | |
| Latent heat | E = mL | |
| Force on conductor | F = BIl | HT only |
| Transformer power | VₚIₚ = VₛIₛ | HT only, Separate Sciences |

### Chemistry — No Formula Sheet (all recall)

| Skill | Formula |
|-------|---------|
| Relative formula mass | Mr = sum of Ar values |
| Moles | moles = mass / Mr |
| Conservation of mass | Total mass reactants = total mass products |
| Concentration (mass) | concentration = mass / volume (g/dm³) |
| Concentration (moles) | concentration = moles / volume (mol/dm³) — HT/Sep only |
| Bond energy change | ΔH = Σ(bonds broken) − Σ(bonds made) |
| Mean rate | rate = quantity / time |
| Rf value | Rf = distance moved by substance / distance moved by solvent |
| Atom economy | % atom economy = (Mr of desired product / Mr of all products) × 100 — Sep only |
| Percentage yield | % yield = (actual yield / theoretical yield) × 100 — Sep only |

### Biology — No Formula Sheet (all recall)

| Skill | Formula |
|-------|---------|
| Magnification | magnification = image size / actual size |
| Unit conversion | 1 mm = 1000 μm = 1,000,000 nm |
| Percentage change | % change = (new − original) / original × 100 |
| Mean | mean = sum of values / number of values |

## Output Structure

Each lesson produces one JSON object in the array:

```json
{
  "unit_slug": "physics-calculations",
  "lesson_number": 1,
  "slug": "energy-ke-gpe-and-power",
  "title": "Energy: KE, GPE and Power",
  "description": "Calculate kinetic energy, gravitational PE, work done and power using recall equations.",
  "practice_data": { ... }
}
```

## practice_data Object

```json
{
  "method_card": {
    "title": "Energy: KE, GPE and Power",
    "content": "<p>HTML — ~200-300 words. Equations split into Recall and Given sections.</p>",
    "steps": [
      "Identify which equation to use from the question",
      "Write the equation",
      "Substitute values (convert units first if needed)",
      "Calculate and state your answer with the correct unit"
    ]
  },
  "exam_context": {
    "paper": "Paper 1 (Physics)",
    "marks": "3-5 per calculation",
    "frequency": "Every exam — energy calculations appear on every P1 paper"
  },
  "worked_examples": [
    {
      "difficulty": "Bronze",
      "question": "Question text with \\(LaTeX\\) equations",
      "steps": [
        {"label": "Step 1 — Write the equation", "content": "<p>\\(E_k = \\frac{1}{2}mv^2\\)</p>"},
        {"label": "Step 2 — Substitute", "content": "<p>...</p>"},
        {"label": "Answer", "content": "<p><strong>135,000 J</strong> (135 kJ)</p>", "is_answer": true}
      ]
    }
  ],
  "problem_bank": {
    "bronze": [7-8 problems],
    "silver": [6 problems],
    "gold": [6 problems]
  },
  "related_videos": [],
  "topic_links": {"prerequisites": []}
}
```

## Problem Types for Science

### single_value (most common — calculation answers)
```json
{
  "display": "A car of mass 1500 kg travels at 20 m/s. Calculate its kinetic energy.",
  "input_type": "single_value",
  "solutions": [300000],
  "accept": 100,
  "unit": "J",
  "calculator": true,
  "higher_only": false,
  "misconceptions": [
    {
      "pattern": "forgot_square",
      "check": "common",
      "message": "Remember to square the speed first. KE = ½ × 1500 × 20² = ½ × 1500 × 400 = 300,000 J."
    }
  ]
}
```

### standard_form (for very large/small values)
```json
{
  "display": "A red blood cell is 7 μm in diameter. Express this in metres in standard form.",
  "input_type": "standard_form",
  "solutions": [7, -6],
  "calculator": false,
  "misconceptions": [
    {
      "pattern": "wrong_power",
      "check": "common",
      "message": "1 μm = 1 × 10⁻⁶ m. So 7 μm = 7 × 10⁻⁶ m."
    }
  ]
}
```

### multiple_choice (equation selection, conceptual)
```json
{
  "display": "Which equation would you use to calculate the kinetic energy of a moving car?",
  "input_type": "multiple_choice",
  "options": ["\\(E = mgh\\)", "\\(E_k = \\frac{1}{2}mv^2\\)", "\\(P = \\frac{E}{t}\\)", "\\(W = Fs\\)"],
  "solutions": [1],
  "calculator": false,
  "misconceptions": [
    {
      "pattern": "wrong_equation",
      "check": "common",
      "message": "Kinetic energy uses mass and speed: Eₖ = ½mv². GPE (mgh) uses height, not speed."
    }
  ]
}
```

### Chart problems (with embedded Chart.js)
```json
{
  "chart": {
    "type": "line",
    "data": {
      "labels": [0, 10, 20, 30, 40, 50, 60],
      "datasets": [{
        "label": "Volume of gas (cm³)",
        "data": [0, 24, 40, 50, 56, 58, 58],
        "borderColor": "#dc2626",
        "backgroundColor": "rgba(220,38,38,0.1)",
        "fill": true,
        "pointRadius": 4
      }]
    },
    "options": {
      "scales": {
        "x": {"title": {"display": true, "text": "Time (s)"}},
        "y": {"title": {"display": true, "text": "Volume of gas (cm³)"}, "beginAtZero": true}
      }
    }
  },
  "display": "Calculate the mean rate of reaction for the first 20 seconds.",
  "input_type": "single_value",
  "solutions": [2],
  "unit": "cm³/s",
  "calculator": true,
  "misconceptions": [
    {
      "pattern": "wrong_formula",
      "check": "common",
      "message": "Mean rate = change in volume / time = 40 / 20 = 2 cm³/s."
    }
  ]
}
```

## Misconception Patterns

| Pattern | When to use |
|---------|-------------|
| `wrong_formula` | Used the wrong equation entirely |
| `forgot_square` | Forgot to square v in ½mv² or e in ½ke² |
| `forgot_half` | Forgot the ½ in ½mv² or ½ke² |
| `unit_error` | Wrong unit conversion (e.g. g→kg, kJ→J, mins→secs) |
| `sign_error` | Got positive/negative wrong |
| `rounding` | Rounded too early or incorrectly |
| `forgot_step` | Missed a step (e.g. didn't convert units first) |
| `inverse_error` | Divided instead of multiplied (or vice versa) |
| `wrong_rearrange` | Rearranged the equation incorrectly |
| `wrong_equation` | Selected wrong equation for the context |
| `incomplete` | Partial answer (check: "partial") |

## Rules

1. **20 problems per lesson**: Bronze 7-8, Silver 6, Gold 5-6
2. **Every problem needs**: `display`, `input_type`, `solutions`, `calculator`, at least 1 misconception
3. **Calculator flag**: `true` for most science calculations; `false` for equation selection, simple mental maths
4. **Tolerance**: Use `accept` for answers that involve rounding. E.g. `"accept": 10` means ±10
5. **Units**: Set `unit` field when the answer has a unit (J, W, N, m/s, etc.)
6. **F/H filtering**: Set `"higher_only": true` for HT-only content (momentum, v²=u²+2as)
7. **Method card recall/given split**: Always label equations clearly
8. **g = 9.8 N/kg**: Use 9.8 unless the question specifies otherwise (some say "use g = 10")
9. **LaTeX**: Use `\\(` and `\\)` for inline maths in display text
10. **Worked examples**: One per tier (Bronze, Silver, Gold), 2-4 steps each
