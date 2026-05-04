"""Slice specs/ocr/physical-education-J587.md into per-unit text files.

Unit 1 (Component 01: Physical factors affecting performance):  lines 656..1599
Unit 2 (Component 02: Socio-cultural issues and sports psychology): lines 1601..2143

Hand-picked from the spec markdown — verified against grep of section headings.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "specs" / "ocr" / "physical-education-J587.md"
OUT_DIR = ROOT / "scripts" / "_content_physical-education-ocr"

UNIT1_HEADER = """OCR GCSE (9-1) Physical Education (J587) — SPECIFICATION EXTRACT
Component 01 (J587/01): Physical Factors Affecting Performance

Learners explore the physical factors which underpin participation and performance in physical
activities and sports — applied anatomy, physiology, movement analysis, physical training, and
preventing injury. Use of data is embedded throughout (data-handling symbol marks examinable
sections in the spec).

Sections covered in this slice:
- 1.1.a  The structure and function of the skeletal system
- 1.1.b  The structure and function of the muscular system
- 1.1.c  Movement analysis (lever systems, planes and axes)
- 1.1.d  The cardiovascular and respiratory systems (incl. aerobic/anaerobic)
- 1.1.e  Effects of exercise (short and long term)
- 1.2.a  Components of fitness (definitions + tests)
- 1.2.b  Applying the principles of training (SPOR + FITT, methods, warm up / cool down)
- 1.2.c  Preventing injury in physical activity and training

OCR-specific notes for content agents:
- 1st-class lever = neck, 2nd-class lever = ankle (calf raise), 3rd-class lever = elbow (bicep curl)
- Axes named: frontal / transverse / longitudinal (NOT sagittal — that is AQA)
- Three muscle roles: agonist / antagonist / fixator (AQA only requires two)
- Principles of training = SPOR (Specificity, Progressive overload, Reversibility, Recovery).
  Tedium is NOT in OCR — do not include it.
- Mechanical advantage = definition only, NOT calculation
- OCR drops EPOC, oxygen debt, DOMS, blood doping, isotonic/isometric, somatotypes (vs AQA)

============================================================
"""

UNIT2_HEADER = """OCR GCSE (9-1) Physical Education (J587) — SPECIFICATION EXTRACT
Component 02 (J587/02): Socio-Cultural Issues and Sports Psychology

Learners develop knowledge of socio-cultural influences on participation and performance,
sports psychology, and the role of physical activity in health, fitness and wellbeing.

Sections covered in this slice:
- 2.1.a  Engagement patterns of different social groups in physical activity and sport
- 2.1.b  Commercialisation of physical activity and sport (sponsorship + media)
- 2.1.c  Ethical and socio-cultural issues (sportsmanship, gamesmanship, deviance, drugs, violence)
- 2.2    Sports psychology (skill characteristics + classification, goal setting, mental preparation,
         types of guidance, types of feedback)
- 2.3    Health, fitness and well-being (definitions + benefits + sedentary lifestyle + diet/nutrition)

OCR-specific notes for content agents:
- SMART = Specific / Measurable / Achievable / Recorded / Timed
  (NOT AQA's Specific / Measurable / Accepted / Realistic / Time-bound)
- Skill continua: TWO only (simple-complex difficulty + open-closed environmental).
  AQA uses four — strip the gross/fine and self-paced/externally-paced continua.
- Five characteristics of skilful movement: efficiency, pre-determined, co-ordinated,
  fluent, aesthetic. (OCR-specific. AQA has no such list.)
- Mental preparation is FOUR named techniques: imagery, mental rehearsal, selective
  attention, positive thinking. NO arousal / inverted-U / stress management.
- Drugs in sport: only THREE PED categories (anabolic steroids, beta blockers, stimulants).
  No blood doping, no EPO, no narcotic analgesics, no diuretics.
- "Player violence" is the OCR term (NOT AQA's "spectator hooliganism").
- Health/fitness/well-being: physical (CHD, BP, bone density, obesity, T2 diabetes, posture),
  emotional (self-esteem, stress management, image), social (friendship, belonging, loneliness).
- Diet: seven components (carbs, proteins, fats, minerals, vitamins, fibre, water/hydration).
  No calorie calculation depth — energy use only.
- OCR has NO somatotypes, NO information-processing model, NO personality types, NO
  aggression types, NO motivation types, NO contract-to-compete framing.

============================================================
"""


def main():
    lines = SPEC.read_text(encoding="utf-8").splitlines()

    # Unit 1: lines 656..1599 (1-indexed) -> indexes 655..1598
    unit1 = "\n".join(lines[655:1599])
    out1 = OUT_DIR / "_spec_physical-factors-affecting-performance.txt"
    out1.write_text(UNIT1_HEADER + unit1 + "\n", encoding="utf-8")
    print(f"  wrote {out1.name}  ({len(unit1.splitlines())} body lines)")

    # Unit 2: lines 1601..2143 (1-indexed) -> indexes 1600..2142
    unit2 = "\n".join(lines[1600:2143])
    out2 = OUT_DIR / "_spec_socio-cultural-issues-and-sports-psychology.txt"
    out2.write_text(UNIT2_HEADER + unit2 + "\n", encoding="utf-8")
    print(f"  wrote {out2.name}  ({len(unit2.splitlines())} body lines)")


if __name__ == "__main__":
    main()
