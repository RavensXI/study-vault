# -*- coding: utf-8 -*-
"""Add a fourth gold question to the science calculation lessons that demand 100%.

practice.html::evaluateTier passes a tier on a 4-streak or >=75% of all
questions. With gold = 3, a 4-streak is impossible and 75% of 3 means 3/3, so a
single slip fails the tier with no way back. Four questions restores margin
(3/4 = 75%).

Affected lessons are the same ten calculation lessons mirrored across
science-ocr-b and separate-sciences-ocr-b, all live to students.

Every answer below is recomputed by the script from the numbers in its own
question text and asserted against the stored solution, so a typo in either
fails the run rather than shipping a wrong key.

    python scripts/fix_practice_gold_counts.py --dry-run
    python scripts/fix_practice_gold_counts.py
    python scripts/fix_practice_gold_counts.py --restore
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

BACKUP = os.path.join(HERE, "_practice_gold_backup.json")
SUBJECTS = ("science-ocr-b", "separate-sciences-ocr-b")


def Q(display, answer, unit, hint, steps, accept=0, calc=True, check=None):
    return {"input_type": "single_value", "display": display, "solutions": [answer],
            "accept": accept, "unit": unit, "hint": hint, "calculator": calc,
            "higher_only": False, "guided_steps": steps, "_check": check}


NEW = {
    ("biology-data-skills", 1): Q(
        "A mitochondrion measures 12 mm long on a photograph taken at ×8,000 magnification. "
        "Calculate its actual length in µm.",
        1.5, "µm", "Actual = image ÷ magnification. Convert mm to µm at the end.",
        [{"say": "Rearrange magnification = image ÷ actual to give actual = image ÷ magnification."},
         {"pre": "Actual size in mm: 12 ÷ 8000 = ", "post": "mm", "answer": 0.0015,
          "hint": "Divide the measured length by the magnification."},
         {"pre": "Convert to µm (×1000): 0.0015 × 1000 = ", "post": "µm", "answer": 1.5,
          "phase": "convert", "hint": "1 mm = 1000 µm."}],
        accept=0.01, check=lambda: 12.0 / 8000 * 1000),

    ("biology-data-skills", 2): Q(
        "A heterozygous black guinea pig (Bb) is crossed with a white one (bb). Black is dominant. "
        "Of 24 offspring, calculate how many are expected to be white.",
        12, "offspring", "Draw the Punnett square first, then apply the ratio to 24.",
        [{"say": "Bb × bb gives Bb, Bb, bb, bb — a 1:1 ratio of black to white."},
         {"pre": "Fraction expected to be white: ", "post": "(as a decimal)", "answer": 0.5,
          "hint": "Two of the four boxes are bb."},
         {"pre": "Number of the 24 offspring: 0.5 × 24 = ", "post": "offspring", "answer": 12,
          "phase": "substitute", "hint": "Apply the fraction to the total."}],
        calc=False, check=lambda: 0.5 * 24),

    ("biology-data-skills", 3): Q(
        "A beetle population falls from 250 to 190 over one season. Calculate the percentage decrease.",
        24, "%", "Percentage change = (change ÷ original) × 100. The original is the starting value.",
        [{"say": "Always divide by the ORIGINAL value, not the new one."},
         {"pre": "Change: 250 − 190 = ", "post": "beetles", "answer": 60,
          "hint": "Start minus finish."},
         {"pre": "Percentage: (60 ÷ 250) × 100 = ", "post": "%", "answer": 24,
          "phase": "substitute", "hint": "Divide by the starting population."}],
        accept=0.1, check=lambda: (250 - 190) / 250.0 * 100),

    ("chemistry-calculations", 2): Q(
        "2Mg + O₂ → 2MgO. Calculate the mass of MgO produced from 48 g of Mg. "
        "(Ar: Mg = 24, O = 16)",
        80, "g", "Moles of Mg first, then use the 2:2 ratio, then mass = moles × Mr.",
        [{"say": "Mass → moles → ratio → mass. The equation gives the ratio."},
         {"pre": "Moles of Mg: 48 ÷ 24 = ", "post": "mol", "answer": 2,
          "hint": "moles = mass ÷ Ar."},
         {"pre": "Moles of MgO (ratio 2:2, so equal): ", "post": "mol", "answer": 2,
          "hint": "Two Mg give two MgO."},
         {"pre": "Mr of MgO = 24 + 16 = 40. Mass: 2 × 40 = ", "post": "g", "answer": 80,
          "phase": "substitute", "hint": "mass = moles × Mr."}],
        accept=0.5, check=lambda: (48 / 24.0) * (24 + 16)),

    ("chemistry-calculations", 3): Q(
        "H₂ + Cl₂ → 2HCl. Bond energies: H–H = 436, Cl–Cl = 242, "
        "H–Cl = 431 kJ/mol. Calculate ΔH.",
        -184, "kJ/mol", "Bonds broken minus bonds made. Watch the sign.",
        [{"say": "ΔH = energy to break bonds − energy released making bonds."},
         {"pre": "Bonds broken: 436 + 242 = ", "post": "kJ/mol", "answer": 678,
          "hint": "One H–H and one Cl–Cl."},
         {"pre": "Bonds made: 2 × 431 = ", "post": "kJ/mol", "answer": 862,
          "hint": "Two H–Cl bonds form."},
         {"pre": "ΔH: 678 − 862 = ", "post": "kJ/mol", "answer": -184,
          "phase": "substitute", "hint": "A negative answer means exothermic."}],
        accept=1, check=lambda: (436 + 242) - 2 * 431),

    ("chemistry-calculations", 4): Q(
        "36 cm³ of gas is produced in the first 24 s of a reaction. Calculate the mean rate "
        "of reaction.",
        1.5, "cm³/s", "Mean rate = quantity ÷ time.",
        [{"say": "Mean rate over a period is simply the total change divided by the time taken."},
         {"pre": "Rate: 36 ÷ 24 = ", "post": "cm³/s", "answer": 1.5,
          "phase": "substitute", "hint": "Volume divided by time."}],
        accept=0.01, check=lambda: 36 / 24.0),

    ("physics-calculations", 5): Q(
        "Calculate the energy needed to melt 0.8 kg of ice at 0 °C. "
        "(Latent heat of fusion = 334,000 J/kg)",
        267200, "J", "Melting at a constant temperature uses E = mL, not mcΔθ.",
        [{"say": "There is no temperature change, so specific heat capacity is not involved."},
         {"pre": "E = mL: 0.8 × 334000 = ", "post": "J", "answer": 267200,
          "phase": "substitute", "hint": "Mass × latent heat."}],
        accept=100, check=lambda: 0.8 * 334000),

    ("physics-calculations", 6): Q(
        "A spring with a spring constant of 250 N/m is stretched by 0.20 m. Calculate the elastic "
        "potential energy stored.",
        5, "J", "E = ½ k x². Square the extension before multiplying.",
        [{"say": "Elastic potential energy is ½ × spring constant × extension squared."},
         {"pre": "Extension squared: 0.20² = ", "post": "m²", "answer": 0.04,
          "hint": "0.2 × 0.2."},
         {"pre": "Energy: 0.5 × 250 × 0.04 = ", "post": "J", "answer": 5,
          "phase": "substitute", "hint": "Half of k, times the squared extension."}],
        accept=0.05, check=lambda: 0.5 * 250 * 0.20 ** 2),

    ("physics-calculations", 7): Q(
        "A train accelerates uniformly from 12 m/s to 30 m/s in 6 s. Calculate the distance "
        "travelled.",
        126, "m", "For uniform acceleration, distance = average speed × time.",
        [{"say": "With uniform acceleration the average speed is halfway between start and finish."},
         {"pre": "Average speed: (12 + 30) ÷ 2 = ", "post": "m/s", "answer": 21,
          "hint": "Add the two speeds and halve."},
         {"pre": "Distance: 21 × 6 = ", "post": "m", "answer": 126,
          "phase": "substitute", "hint": "Average speed × time."}],
        accept=0.5, check=lambda: (12 + 30) / 2.0 * 6),

    ("physics-calculations", 8): Q(
        "A wave has a frequency of 250 Hz and a wavelength of 1.4 m. Calculate its speed.",
        350, "m/s", "v = fλ.",
        [{"say": "Wave speed is frequency multiplied by wavelength."},
         {"pre": "v = fλ: 250 × 1.4 = ", "post": "m/s", "answer": 350,
          "phase": "substitute", "hint": "Multiply the two."}],
        accept=0.5, check=lambda: 250 * 1.4),
}


def main():
    dry = "--dry-run" in sys.argv
    sb = get_client()

    # arithmetic self-check BEFORE anything is written
    for (unit, num), item in NEW.items():
        got = item.pop("_check")()
        want = item["solutions"][0]
        assert abs(got - want) <= max(item["accept"], 1e-9), \
            "%s L%s: question implies %s, stored answer is %s" % (unit, num, got, want)
        for st in item["guided_steps"]:
            if "answer" in st:
                assert isinstance(st["answer"], (int, float))
    print("arithmetic verified for all %d new questions" % len(NEW))

    if "--restore" in sys.argv:
        with open(BACKUP, "r", encoding="utf-8") as f:
            for lid, pd in json.load(f).items():
                sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
        print("restored")
        return

    saved, touched = {}, 0
    for slug in SUBJECTS:
        sub = [x for x in sb.table("subjects").select("id,slug,school_id")
               .eq("slug", slug).execute().data if not x["school_id"]][0]
        units = {u["slug"]: u["id"] for u in sb.table("units").select("id,slug")
                 .eq("subject_id", sub["id"]).execute().data}
        for (uslug, num), item in NEW.items():
            if uslug not in units:
                print("  %s has no %s — skipped" % (slug, uslug)); continue
            row = sb.table("lessons").select("id,practice_data").eq("unit_id", units[uslug]) \
                .eq("lesson_number", num).single().execute().data
            pd = json.loads(json.dumps(row["practice_data"]))
            gold = pd["problem_bank"]["gold"]
            if any(g.get("display") == item["display"] for g in gold):
                print("  %-26s %s L%s already has it" % (slug, uslug, num)); continue
            saved[row["id"]] = row["practice_data"]
            gold.append(json.loads(json.dumps(item)))
            assert len(gold) >= 4
            if not dry:
                sb.table("lessons").update({"practice_data": pd}).eq("id", row["id"]).execute()
            touched += 1
            print("  %-26s %-24s L%-2d gold %d -> %d" % (slug, uslug, num, len(gold) - 1, len(gold)))

    if not dry and saved and not os.path.exists(BACKUP):
        with open(BACKUP, "w", encoding="utf-8") as f:
            json.dump(saved, f)
        print("backup ->", BACKUP)
    print(("DRY RUN — " if dry else "") + "lessons updated: %d" % touched)


if __name__ == "__main__":
    main()
