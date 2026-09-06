"""Build scripts/_planning/board_share.json from the boards' own published
per-specification entry counts.

Primary column is JUNE 2025 - the same exam series the DfE 2024/25 KS4 dataset
counts, so shares and totals describe one cohort. June 2026 rides along as a
"direction of travel" column with the delta.

Shares are derived: no board or regulator publishes a share. Each board
publishes its own entries; the share is that board's entries over the sum of
the England-accessible boards' entries for the same subject.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

BE = json.load(open(os.path.join(HERE, "board_entries.json"), encoding="utf-8"))
SPECS = json.load(open(os.path.join(ROOT, "specs", "index.json"), encoding="utf-8"))

import sys
sys.path.insert(0, HERE)
from remaining_builds import subject_family, EXCLUDED_FAMILIES   # noqa: E402

BOARD_KEY = {"AQA": "AQA", "Edexcel": "Edexcel", "OCR": "OCR",
             "Eduqas": "Eduqas", "WJEC": "WJEC"}

# Eduqas publishes titles, not specification codes. Map each Eduqas spec in
# specs/index.json onto the title used in the Eduqas results PDF.
EDUQAS_TITLE = {
    "C650QS": None,                     # Art & Design - portfolio, out of scope
    "C510QS": "BUSINESS",
    "C500QS": "COMPUTER SCIENCE",
    "C600QS": "DESIGN & TECHNOLOGY",
    "C690QS": "DRAMA",
    "C490QS": "ELECTRONICS",
    "C700QS": "ENGLISH LANGUAGE",
    "C720QS": "ENGLISH LITERATURE",
    "C670QS": "FILM STUDIES",
    "C560QS": "FOOD PREPARATION & NUTRITION",
    "C800QS": "FRENCH",
    "C111QS": "GEOGRAPHY A",
    "C112QS": "GEOGRAPHY B",
    "C180QS": "GEOLOGY",
    "C100QS": "HISTORY",
    "C580QS": "LATIN",
    "C300QS": "MATHEMATICS",
    "C680QS": "MEDIA STUDIES",
    "C660QS": "MUSIC",
    "C550QS": "PHYSICAL EDUCATION",
    "C120QS": "RELIGIOUS STUDIES",
    "C200QS": "SOCIOLOGY",
    "C820QS": "SPANISH",
    "C610QS": "GERMAN",
}

# Specification codes that changed between the two series (reformed MFL: first
# award June 2026). The 2025 entries sit on the outgoing code.
LEGACY_CODE = {
    ("AQA", "8652"): "8658",     # French
    ("AQA", "8662"): "8668",     # German
    ("AQA", "8692"): "8698",     # Spanish
    ("Edexcel", "1FR1"): "1FR0",
    ("Edexcel", "1GN1"): "1GN0",
    ("Edexcel", "1SP1"): "1SP0",
    ("Edexcel", "1CP1"): "1CP2",  # Pearson lists GCSE CS under 1CP2
}


# Live specifications that appear in a board's own results release but are NOT
# in specs/index.json. They must count towards the market denominator, otherwise
# every other board's share is overstated. They are also real, unbuilt content
# gaps that the To-Build page cannot see - the report flags them separately.
INDEX_GAPS = [
    {"board": "Edexcel", "spec_code": "1EN2", "family": "english-language",
     "subject": "English Language 2.0",
     "note": "Pearson's larger English Language specification - 66,425 entries in "
             "June 2025 against 41,565 on 1EN0, which is the one we hold. Absent "
             "from specs/index.json."},
    {"board": "Edexcel", "spec_code": "1RB0", "family": "religious-studies",
     "subject": "Religious Studies B",
     "note": "Pearson's larger Religious Studies specification - 23,481 entries in "
             "June 2025 against 17,143 on 1RA0, which is the one we hold. Absent "
             "from specs/index.json."},
]


def index(year):
    by_code, by_title = {}, {}
    for key, rows in BE["entries"].items():
        board, yy = key.split("|")
        if int(yy) != year:
            continue
        for r in rows:
            if r.get("spec_code"):
                by_code[(board, r["spec_code"])] = r["entries"]
            by_title[(board, r["title"])] = r["entries"]
    return by_code, by_title


def lookup(board, spec_code, by_code, by_title):
    if board == "Eduqas":
        t = EDUQAS_TITLE.get(spec_code)
        return by_title.get((board, t)) if t else None
    hit = by_code.get((board, spec_code))
    if hit is None:
        alt = LEGACY_CODE.get((board, spec_code))
        if alt:
            hit = by_code.get((board, alt))
    return hit


def main():
    idx = {y: index(y) for y in (2025, 2026)}

    # family -> board -> {year: entries}, and per-spec entries for route weights
    fam = {}
    spec_rows = {}
    for sp in SPECS:
        f = subject_family(sp["subject"])
        if EXCLUDED_FAMILIES.get(f):
            continue
        b = BOARD_KEY.get(sp["board"], sp["board"])
        if b == "WJEC" or "short course" in sp["subject"].lower():
            continue
        rec = {}
        for y in (2025, 2026):
            n = lookup(b, sp["spec_code"], *idx[y])
            if n is not None:
                rec[y] = n
        if not rec:
            continue
        spec_rows[(f, sp["spec_code"])] = {"board": b, "subject": sp["subject"], **rec}
        d = fam.setdefault(f, {}).setdefault(b, {2025: 0, 2026: 0, "specs": []})
        d["specs"].append(sp["spec_code"])
        for y in (2025, 2026):
            if y in rec:
                d[y] += rec[y]

    # Fold the index gaps into the market denominator.
    gaps = []
    for g in INDEX_GAPS:
        rec = {}
        for y in (2025, 2026):
            n = lookup(g["board"], g["spec_code"], *idx[y])
            if n is not None:
                rec[y] = n
        if not rec:
            continue
        spec_rows[(g["family"], g["spec_code"])] = {"board": g["board"],
                                                    "subject": g["subject"], **rec}
        d = fam.setdefault(g["family"], {}).setdefault(
            g["board"], {2025: 0, 2026: 0, "specs": []})
        d["specs"].append(g["spec_code"])
        for y in (2025, 2026):
            if y in rec:
                d[y] += rec[y]
        gaps.append({**g, "entries_2025": rec.get(2025), "entries_2026": rec.get(2026)})

    SRC = {b: BE["sources"].get(f"{b}|2025", {}) for b in ("AQA", "Edexcel", "OCR", "Eduqas")}
    SRC26 = {b: BE["sources"].get(f"{b}|2026", {}) for b in ("AQA", "Edexcel", "OCR", "Eduqas")}

    shares = {}
    for f, boards in fam.items():
        tot = {y: sum(v[y] for v in boards.values()) for y in (2025, 2026)}
        if tot[2025] <= 0:
            continue
        b25 = {b: round(v[2025] / tot[2025], 4) for b, v in boards.items()}
        b26 = ({b: round(v[2026] / tot[2026], 4) for b, v in boards.items()}
               if tot[2026] > 0 else {})
        parts = " / ".join(f"{b} {boards[b][2025]:,}" for b in
                           sorted(boards, key=lambda x: -boards[x][2025])
                           if boards[b][2025])
        rec = {
            "year": 2025,
            "source_label": f"derived from the boards' own June 2025 results "
                            f"statistics ({parts})",
            "source_url": SRC.get(max(boards, key=lambda b: boards[b][2025]), {})
                             .get("url", ""),
            "board_entries_2025": {b: boards[b][2025] for b in boards},
            "board_total_2025": tot[2025],
            "boards": {**{k: 0.0 for k in ("AQA", "Edexcel", "OCR", "Eduqas", "WJEC")},
                       **b25},
        }
        if b26:
            rec["boards_2026"] = {**{k: 0.0 for k in
                                     ("AQA", "Edexcel", "OCR", "Eduqas", "WJEC")}, **b26}
            rec["board_entries_2026"] = {b: boards[b][2026] for b in boards}
            rec["board_total_2026"] = tot[2026]
            rec["delta_pp"] = {b: round(100 * (b26.get(b, 0) - b25.get(b, 0)), 1)
                               for b in boards}
            rec["source_label_2026"] = "boards' own June 2026 results statistics"
        shares[f] = rec

    # Per-spec route weights, where a board runs more than one route and both
    # routes have a published entry count.
    routes = {}
    for (f, code), r in spec_rows.items():
        sibs = [(c, v) for (ff, c), v in spec_rows.items()
                if ff == f and v["board"] == r["board"]]
        if len(sibs) < 2:
            continue
        tot25 = sum(v.get(2025, 0) for _, v in sibs)
        if tot25 <= 0 or 2025 not in r:
            continue
        routes[f"{f}|{code}"] = {
            "board": r["board"], "subject": r["subject"],
            "weight_2025": round(r[2025] / tot25, 4),
            "entries_2025": r[2025], "board_total_2025": tot25,
            "source": f"{r['board']} June 2025 results statistics: "
                      + ", ".join(f"{c} {v.get(2025, 0):,}" for c, v in sorted(sibs)),
        }

    # BTEC Technical Awards never appear in a GCSE results release. The brand is
    # Pearson-exclusive, so the DfE BTEC bucket is 100% Pearson by construction.
    shares["health-and-social-care"] = {
        "year": 2025,
        "source_label": "BTEC Technical Award is a Pearson-only qualification brand, "
                        "so the DfE BTEC Technical Award bucket is 100% Pearson by "
                        "construction - not a derived share",
        "source_url": "https://qualifications.pearson.com/en/qualifications/btec-tech-awards.html",
        "boards": {"Edexcel": 1.0, "AQA": 0.0, "OCR": 0.0, "Eduqas": 0.0, "WJEC": 0.0},
        "boards_2026": {"Edexcel": 1.0, "AQA": 0.0, "OCR": 0.0, "Eduqas": 0.0, "WJEC": 0.0},
        "delta_pp": {"Edexcel": 0.0},
        "source_label_2026": "same, by construction",
        "no_board_release": True,
    }

    out = {
        "_readme": "Exam-board share of GCSE entries by build-status subject-family "
                   "slug. PRIMARY column is June 2025 - the same exam series the DfE "
                   "2024/25 KS4 dataset counts. `boards` holds the 2025 shares used "
                   "for every calculation; `boards_2026` and `delta_pp` show the "
                   "direction of travel only. Shares are DERIVED: each board "
                   "publishes its own per-specification entries and the share is that "
                   "board's entries over the England-accessible board sum. No board "
                   "or regulator publishes a share. WJEC is excluded throughout: its "
                   "specs are Qualifications Wales-regulated and not available to "
                   "centres in England.",
        "_sources_2025": SRC,
        "_sources_2026": SRC26,
        "_caveats": [
            "Cohort aligned: June 2025 shares against DfE 2024/25 (summer 2025) "
            "entries. The 2026 column is a different cohort and is never used in a "
            "calculation.",
            "Geographic scope differs slightly by board: Pearson publishes HOME "
            "candidates; AQA, OCR and Eduqas publish all their entries. The DfE "
            "cross-check quantifies the effect per subject.",
            "Board figures are provisional, before enquiries about results.",
            "Reformed MFL specifications changed code for June 2026 (AQA 8658 to "
            "8652, Pearson 1FR0 to 1FR1 and so on). The 2025 entries sit on the "
            "outgoing code; both are joined here.",
            "Eduqas short-course tables are excluded: the DfE query covers full "
            "course only.",
        ],
        "shares": dict(sorted(shares.items())),
        "route_weights": dict(sorted(routes.items())),
        "index_gaps": gaps,
    }
    path = os.path.join(HERE, "board_share.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {path}: {len(shares)} families, {len(routes)} route weights")
    for f, r in sorted(shares.items()):
        top = sorted(r["boards"].items(), key=lambda kv: -kv[1])[:4]
        print(f"  {f:<34} " + "  ".join(f"{b} {v:.1%}" for b, v in top if v))


if __name__ == "__main__":
    main()
