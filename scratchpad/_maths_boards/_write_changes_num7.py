# -*- coding: utf-8 -*-
import json

changes = {
    "key": "maths-aqa_number-L07",
    "lesson_id": "8696e75e-f9fd-40ef-b3a4-df27f5811c73",
    "title": "Indices, Surds & Bounds",
    "bank_verdict": "All 20 problems fresh-solved from display (bronze 8, silver 7, gold 5). Two genuine wrong stored answers found in gold, plus two validator-fatal within-tier duplicate solution sets in bronze. All fixed with minimal clean-answer edits and re-solved.",
    "problems_fixed": [
        {"tier": "gold", "index": 2, "what": "WRONG stored solution and a garbled self-correcting misconception message. Lower bound of perimeter of a 12.4 x 5.8 cm rectangle is 2 x (12.35 + 5.75) = 36.2, not 35.8.", "old": "solution 35.8", "new": "solution 36.2 (kept the rectangle; rewrote the misconception cleanly, added an exam-style figure)"},
        {"tier": "gold", "index": 4, "what": "WRONG stored solution. 245 / 8.35 = 29.34 rounds to 29.3 to 3 s.f., and the stored 14.9 was inconsistent with its own message and mis-rounded. Re-posed d from 120 m to 240 m (2 s.f.) to give a clean 3 s.f. answer away from a rounding boundary.", "old": "d = 120 m, solution 14.9", "new": "d = 240 m, solution 29.3"},
        {"tier": "bronze", "index": 4, "what": "Duplicate solution 3 within bronze (collided with bronze[0] 27^(1/3) = 3), validator-fatal. Re-posed the surd radicand.", "old": "Simplify sqrt(18), a*sqrt(2) (a = 3)", "new": "Simplify sqrt(8), a*sqrt(2) (a = 2)"},
        {"tier": "bronze", "index": 7, "what": "Duplicate solution 5 within bronze (collided with bronze[3] sqrt(50) -> a = 5), validator-fatal. Re-posed the surd radicand, kept the sqrt(3) family.", "old": "Simplify sqrt(75), a*sqrt(3) (a = 5)", "new": "Simplify sqrt(108), a*sqrt(3) (a = 6)"},
    ],
    "issues_resolved": 4,
    "guided_added": {
        "hints": 20,
        "guided_steps_walks": 20,
        "misconceptions_converted": 20,
        "tier_descriptions": 3,
        "tier_guides": 3,
        "teach_walks": 3,
        "opener": 1,
        "method_card": "slimmed to 4 steps + 3-paragraph content under the 140-word budget; kept the sqrt(72) = 6*sqrt(2) example."
    },
    "misconception_notes": "All misconceptions converted from the old {check,message,pattern} shape to {pattern,message,expect}. Every expect derived by committing the specific error and verified distinct from the correct answer. Errors modelled: dividing by the index (bronze[0] 27/3=9), taking the root but forgetting the power (bronze[1] 2; silver[4] 3), treating a power as a multiply (bronze[2] 5x2=10), using a square factor without rooting it (bronze[3] 25, bronze[4] 4), stopping at a non-largest factor (bronze[7] 3, silver[6] 2), whole-unit bound errors (bronze[5] 6.4, bronze[6] 350, silver[5] 4.7), adding instead of subtracting indices (silver[0] 10), base x power instead of raising (silver[1] 8), multiplying surd fronts instead of adding (silver[2] 6), forgetting to divide after rationalising (silver[3] 6), adding the squares instead of subtracting in a conjugate (gold[0] 11), dropping the constant product in a surd expansion (gold[1] 5), using rounded values not bounds (gold[2] 36.4), dividing only the first surd term (gold[3] 2), and dividing by the upper bound of time (gold[4] 29.0). No em dashes; all expects reproduce and are distinct from the correct answer.",
    "opener_concept": "Square-and-cube roots as fractional powers. An inline SVG shows a square of area 9 and a cube of volume 8. Boxes: the square's side is 3 (3x3=9) and the cube's edge is 2 (2x2x2=8), both pure common sense. The reveal names these as a square root and a cube root and writes them as 9^(1/2)=3 and 8^(1/3)=2, so a fractional power is a root, tying indices, surds and bounds together.",
    "completion_boundaries": "Every bank walk tags phase:'substitute' after the set-up move (the root/positive-power, the largest-square-factor split, the half-a-unit error, or the conjugate first-terms), leaving >= 2 live boxes so the student finishes and lands exactly on the stored solution.",
    "preservation": "related_videos ([]), topic_links ({prerequisites:[]}) and worked_examples (3 items) preserved byte-for-byte vs the pre-edit live row (JSON-equal check passed). Only the practice_data column was patched; no other column or row touched.",
    "ship": {
        "shard": "lesson_maths-aqa_number-L07.json",
        "validator": "PASS (on shard; live re-fetch == shard byte-for-byte)",
        "patch_status": 204
    }
}
json.dump(changes, open("changes_maths-aqa_number-L07.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

diagrams = {
    "key": "maths-aqa_number-L07",
    "figures_added": [
        {"tier": "opener", "index": 0, "kind": "svg", "what": "A square of area 9 and a simple isometric cube of volume 8, drawn programmatically to match the opener's numbers. Theme-safe (currentColor text, soft fill-opacity), role=img + aria-label. Makes the concrete hook (side/edge lengths) visible as the exam would."},
        {"tier": "gold", "index": 2, "kind": "svg", "what": "Rectangle labelled 12.4 cm (top) and 5.8 cm (side), with a 'Diagram not drawn accurately' caption, exactly as an AQA bounds question prints it. Labels match the problem values; the unknown (perimeter) is what the student finds."}
    ],
    "opener_touched": True,
    "notes": "Indices/surds/bounds is a mostly textual number unit; the only problems where the exam prints a figure are the rectangle-perimeter bounds question (gold[2], added) and the opener scene (added). Single rounded-measurement bounds, index laws and surd simplifications are correctly left figure-free. No question text, solution, guided step, hint or misconception was changed in the figure pass beyond the fixes already logged in the guided changes file."
}
json.dump(diagrams, open("changes_maths-aqa_number-L07_diagrams.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote changes_maths-aqa_number-L07.json and changes_maths-aqa_number-L07_diagrams.json")
