# Fact-Check Report: Engineering AQA
**Date:** 2026-05-22  
**Lessons checked:** 22 (4 units: Engineering Materials, Manufacturing Processes, Engineering Systems, Testing Drawing and the Engineering Industry)  
**Total findings:** 3 medium, 0 high, remainder low/confirmed-correct

---

## Summary

The 22 lessons are largely accurate for GCSE level. All core formulas (stress/strain/Young's modulus, gear ratio, mechanical advantage, Pascal's law, P=F/A) are correct. All logic gate truth tables (AND, OR, NOT, NAND, NOR, XOR) are correct. Material property values for aluminium density, cast iron carbon content, stainless steel chromium threshold, hot-dip galvanising temperature, brazing temperatures and filler composition are all confirmed. UK mains voltage/frequency is correct. ISO 9001 and BS 8888 references are accurate. Rolls-Royce metal AM attribution is supported.

Three issues were identified:

---

## HIGH severity — None

---

## MEDIUM severity

### 1. SLS terminology misapplied to metals
**Lesson:** Additive Manufacturing and Rapid Prototyping (manufacturing-processes, L1)  
**Lesson ID:** `837d69b8-ce3a-49a0-80c8-9b42d3675773`

**Claim:** *"Metal sintering … also called selective laser sintering or SLS when applied to metals, or DMLS — Direct Metal Laser Sintering"*

**Issue:** SLS (Selective Laser Sintering) is the polymer/nylon process. In current industry and academic usage, SLS is explicitly restricted to polymer powder-bed fusion. The metal equivalent is DMLS (Direct Metal Laser Sintering) or SLM (Selective Laser Melting). Describing DMLS as "SLS when applied to metals" is incorrect terminology. AQA mark schemes at GCSE may not penalise this, but the definition as written would be wrong in any engineering context beyond GCSE.

**Suggested fix:** Remove "also called selective laser sintering or SLS when applied to metals". Replace with: "Metal powder-bed fusion is properly called DMLS (Direct Metal Laser Sintering) or SLM (Selective Laser Melting); SLS refers specifically to polymer/nylon sintering."

**Source:** https://www.xometry.com/resources/3d-printing/sls-vs-dmls-3d-printing/

---

### 2. Aluminium elongation given as a fixed 25% (oversimplified)
**Lesson:** Mechanical Properties of Engineering Materials (engineering-materials, L1)  
**Lesson ID:** `4649fb10-0a6e-4bd9-87a7-c854beeb85b2`

**Claim:** *"aluminium at about 25% [percentage elongation at fracture]"*

**Issue:** 25% is plausible for some annealed alloys (6061-O: 25–30%) but many common aluminium alloys have 10–18% elongation. Pure aluminium (1100-O) can reach 35%+. The figure of 25% is presented as a single definitive value for "aluminium" rather than acknowledging alloy and temper dependency. This is an oversimplification that could give students an inaccurate impression. Not off by >20% from pure annealed aluminium (which is higher), but could be misleading for engineering alloys. Compare: copper at 45% (for annealed C10400) is well-supported.

**Suggested fix:** Change to "aluminium at typically 10–30% depending on alloy and temper" to reflect the real range.

**Source:** https://copper.org/applications/industrial/DesignGuide/props/ductility.html

---

### 3. Tempering colour temperature: straw at 230°C attributed to woodworking chisels
**Lesson:** Heat Treatment and Chemical Treatment (manufacturing-processes, L5)  
**Lesson ID:** `f2cd1f81-8abc-4f0b-8a4a-abc7b513d830`

**Claim:** *"straw (230°C) for woodworking chisels"*

**Issue:** Standard steel temper colour charts show:
- Faint/pale straw: 200°C  
- Light straw: 210°C  
- Dark straw: 220–226°C  
- Golden/brown: 230–240°C  

At 230°C the colour is transitioning from dark straw to golden-brown. Woodworking chisels require the hardest practical temper, conventionally taken at pale/light straw (200–220°C), not at 230°C. Some GCSE textbooks do give 230°C for chisels, so this may match the AQA mark scheme, but it sits at the upper edge of the straw range. The blue at 300°C for springs/screwdrivers is within the accepted range (light blue appears at ~280–340°C).

**Suggested fix:** Adjust to "pale straw (~220°C) for woodworking chisels" to match the majority of metalworking references. If the AQA spec/mark scheme explicitly states 230°C, retain it but note the range.

**Source:** https://www.westyorkssteel.com/technical-information/steel-heat-treatment/tempering-temperatures/

---

## LOW severity (confirmed correct or minor wording notes)

| Lesson | Claim | Status |
|--------|-------|--------|
| Metals and Alloys | Aluminium density 2.7 g/cm³, one-third of steel | Correct |
| Metals and Alloys | Stainless steel: minimum 10.5% chromium | Correct |
| Metals and Alloys | Cast iron: 2–4% carbon | Correct |
| Metals and Alloys | High carbon steel: 0.6–1.4% carbon | Acceptable range |
| Metals and Alloys | Hardening above 723°C critical temperature | Technically correct as lower bound; imprecise for hypo-eutectoid steels |
| Joining and Assembly | Soft solder < 450°C; brazing > 450°C | Correct (AWS/ISO standard) |
| Joining and Assembly | Brazing: brass filler 60% Cu/40% Zn, ~870°C melting point | Correct |
| Joining and Assembly | BAE Systems uses MIG welding for ship structural fabrication | Confirmed |
| Heat Treatment | Normalising: 830–900°C for medium-carbon steels | Correct |
| Heat Treatment | Galvanising bath: ~450°C | Correct |
| Surface Finishing | Hot-dip galvanising: ~450°C | Correct |
| Systems: Block Diagrams | BS 3939 symbol set reference | Minor note: BS 3939 superseded by BS EN 60617; terminology still used in GCSE context. UK resistor symbol is rectangular box, not zigzag. L5 correctly distinguishes this. |
| Mechanical Systems | Rolls-Royce cam precision claim | Plausible historically; modern turbines use FADEC. Low risk as context/colour item |
| Mechanical Calculations | Gear ratio formula: driven ÷ driver | Correct |
| Mechanical Calculations | Mechanical advantage: load ÷ effort | Correct |
| Electrical Systems | UK mains: 230V AC, 50Hz | Correct |
| Electronic Systems | AND, OR, NOT, NAND, NOR, XOR truth tables | All correct |
| Structural/Pneumatic | Pascal's law P=F/A; F2=F1×(A2/A1) | Correct |
| Structural/Pneumatic | Die casting pressure: 10–200 MPa | Correct |
| Calculations Lesson | Stress σ=F/A, Strain ε=ΔL/L, E=σ/ε | All correct |
| Calculations Lesson | E: steel 200 GPa, aluminium 70 GPa, rubber 0.01 GPa | All within accepted ranges |
| Testing/QC | ISO 9001 = quality assurance standard | Correct |
| Engineering Drawing | BS 8888 third-angle projection | Correct |
| Additive Manufacturing | Rolls-Royce uses metal AM for turbine components | Confirmed |
| Polymers/Composites | Boeing 787 uses CFRP fuselage | Correct (50% by weight composite) |

---

## No issues found in

- All logic gate truth tables (AND, OR, NOT, NAND, NOR, XOR)
- All mechanical formulas (stress, strain, Young's modulus, gear ratio, MA, Pascal's law)
- Material cost comparisons (copper vs gold, timber vs steel)
- Injection moulding process description
- Sand casting process stages
- Press forming description
- Annealing and case hardening descriptions
- Composite materials (GRP, CFRP) descriptions
- Recycling energy comparisons (aluminium recycling at 5% of primary smelting energy)

---

`FACT_CHECK_DONE: subject=engineering-aqa lessons=22 high=0 medium=3 low=0`
