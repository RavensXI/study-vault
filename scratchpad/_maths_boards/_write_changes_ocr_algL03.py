# -*- coding: utf-8 -*-
import json, io

changes = {
    "key": "algebra-L03",
    "problems_fixed": [
        {"tier": "all", "index": "*", "what": "Added expect:null to every existing misconception (validator requires the key present; MC problems have no single numeric expect)", "old": "no expect key", "new": "expect: null"},
        {"tier": "all", "index": "*", "what": "Added a plain-text hint to all 20 problems (none had one)", "old": "hint: None", "new": "one method-move sentence each"},
        {"tier": "all", "index": "*", "what": "Added bronze/silver/gold _description (all were None)", "old": "None", "new": "one line per tier"},
        {"tier": "worked_examples", "index": "*", "what": "Replaced em dashes in step labels with colons (style law)", "old": "Step 1 — Find HCF", "new": "Step 1: Find HCF"},
        {"tier": "method_card", "index": "0", "what": "Removed em dash and redundant clause; slimmed content to reference-only within budget", "old": "reverse of expanding — ... It's the opposite of expanding.", "new": "reverse of expanding: you put an expression back into brackets."},
    ],
    "issues_resolved": 0,
    "opener_concept": "Party bags: 12 sweets + 8 chocolates into the biggest number of identical bags (HCF = 4) gives 4 bags of (3 sweets + 2 chocolates), i.e. 12s + 8c = 4(3s + 2c). Splitting into equal groups with common sense IS taking out the HCF, which is factorising.",
    "notes": "Bank was mathematically clean: fresh-solved all 20 multiple_choice problems from display, every stored solution (option 0) correct, no degenerate/duplicate/messy answers, so no answer edits. All problems kept as multiple_choice (matches approved OCR sibling algebra-L01), so guided_steps are correctly omitted (validator-permitted for MC) and no completion boundary applies. Added tier_guides, guided.opener (with SVG) and guided.teach walks (>=4 numeric boxes per tier, each verified to expand back to the target). Preserved related_videos, topic_links, worked_examples content, all displays/options/solutions byte-for-byte."
}
json.dump(changes, io.open("changes_maths-ocr_algebra-L03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
    "key": "algebra-L03",
    "figures_added": [
        {"tier": "opener", "index": 0, "kind": "svg", "what": "12 sweets (circles) + 8 chocolates (squares) illustrating the party-bag HCF hook; theme-safe currentColor labels, soft opacity fills, viewBox/role/aria-label present"}
    ],
    "opener_touched": True,
    "notes": "Factorising is a textual algebra unit: the exam prints no figure for 'Factorise 6x + 12' style questions, so no per-problem SVG/chart is warranted (exam-realism test). The only figure is the concrete opener illustration, mirroring the approved OCR algebra-L01 opener. All 20 problems are pure-algebra multiple choice with no shape/graph/tree/grid described."
}
json.dump(diagrams, io.open("changes_maths-ocr_algebra-L03_diagrams.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes files written")
