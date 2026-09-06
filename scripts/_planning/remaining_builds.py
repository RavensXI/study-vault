"""Rescope the remaining StudyVault GCSE subject builds with hard numbers.

Reproduces the "To Build" logic of admin/build-status.html in Python
(EXCLUDED_FAMILIES, subjectFamily(), ENTRY_TIER, BUILD_NOTES tags), joins it to
England 2024/25 entry data from DfE Explore Education Statistics, adds exam-board
share where a published figure exists, and prices each build.

Read-only. Writes:
  scripts/_planning/remaining_builds.json
  scripts/_planning/remaining_builds_2025.html

Inputs (produced by the sibling scripts):
  _build_status_maps.json      <- _extract_maps.mjs (parses admin/build-status.html)
  _supabase_subjects.json      <- fetch_supabase_subjects.py
  dfe_subject_entries_2025.json<- fetch_dfe_entries.py
  board_share.json             <- hand-curated, sources cited inline
"""

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def load(name):
    return json.load(open(os.path.join(HERE, name), encoding="utf-8"))


MAPS = load("_build_status_maps.json")
EXCLUDED_FAMILIES = MAPS["EXCLUDED_FAMILIES"]
ENTRY_TIER = MAPS["ENTRY_TIER"]
BUILD_NOTES = MAPS["BUILD_NOTES"]
TIER_LABEL = {"S": "Top tier", "A": "High uptake", "B": "Medium",
              "C": "Lower", "N": "Niche"}


# ---------------------------------------------------------------- build-status
def subject_family(name):
    """Python port of subjectFamily() in admin/build-status.html."""
    if not name:
        return ""
    n = str(name).strip()
    n = re.sub(r":\s*(Trilogy|Synergy)\s*$", "", n, flags=re.I)
    n = re.sub(r"\s*\([^)]*\)\s*$", "", n)
    n = re.sub(r"\s+[AB]$", "", n)
    if re.match(r"^food and nutrition$", n, flags=re.I):
        n = "Food Preparation and Nutrition"
    n = n.lower()
    n = re.sub(r"[^a-z0-9]+", "-", n)
    return n.strip("-")


def tier_for(fam):
    if fam in ENTRY_TIER:
        return ENTRY_TIER[fam]
    if fam.startswith("cambridge-nationals"):
        return "C"
    if fam.startswith("level-1-2-vocational-award"):
        return "C"
    return "C"


# ------------------------------------------------------------------ cost model
# Real settled spend, not meter estimates.
#   Psychology AQA+OCR, 69 lessons, Anthropic Console $32.99 = $0.478/lesson.
#   OCR poetry rebuild 6 Sep 2026, 3 clusters x 15 lessons = 45 lessons,
#   Console $18.18 (GBP 13.38) = GBP 0.297/lesson, plus ~GBP 5 narration.
# Blend the two settled builds; both are batch + caching + fact-check shaped.
USD_GBP = 0.78
API_PER_LESSON_GBP = round(((32.99 * USD_GBP) / 69 + 13.38 / 45) / 2, 3)   # ~0.335
NARRATION_PER_LESSON_GBP = 0.11      # Azure: ~GBP 5 per 45 lessons
FACTCHECK_PER_SUBJECT_GBP = 5.00     # fact-check pass, per memory note
# A PORT reuses 60-80% of an existing build's material; an ALIAS is zero content.
COST_FACTOR = {"build": 1.0, "port": 0.55, "alias": 0.0, "skip": 0.0,
               "general": 1.0, "": 1.0}


def cost_for(lessons, tag):
    f = COST_FACTOR.get(tag, 1.0)
    if f == 0:
        return 0.0
    per = (API_PER_LESSON_GBP + NARRATION_PER_LESSON_GBP) * lessons * f
    return round(per + FACTCHECK_PER_SUBJECT_GBP * (1 if f else 0), 2)


# ------------------------------------------------- spec family -> DfE subject
# Each key is a build-status family slug. "dg" is the DfE subject_discount_group
# label, "grp" the coarse subject group label, "qual" the qualification label.
# These pairs are what dfe_subject_entries_2025.json is keyed on.
DFE_MAP = {
    "mathematics":            ("Maths (General)", "Mathematics", "GCSE (9-1) Full Course"),
    "mathematics-and-numeracy": (None, None, None),          # Wales-only WJEC
    "english-language":       ("English Language", "English Language", "GCSE (9-1) Full Course"),
    "english-literature":     ("English Literature", "English Literature", "GCSE (9-1) Full Course"),
    "combined-science":       ("Science Double Award", "Combined Science", "GCSE (9-1) Full Course (Double Award)"),
    "biology":                ("Biology", "Biology", "GCSE (9-1) Full Course"),
    "chemistry":              ("Chemistry (General)", "Chemistry", "GCSE (9-1) Full Course"),
    "physics":                ("Physics (General)", "Physics", "GCSE (9-1) Full Course"),
    "geography":              ("Geography", "Geography", "GCSE (9-1) Full Course"),
    "history":                ("History", "History", "GCSE (9-1) Full Course"),
    "religious-studies":      ("Religious Studies", "Religious Studies", "GCSE (9-1) Full Course"),
    "religious-education":    ("Religious Studies", "Religious Studies", "GCSE (9-1) Full Course"),
    "spanish":                ("Spanish", "Spanish", "GCSE (9-1) Full Course"),
    "french":                 ("French Language", "French", "GCSE (9-1) Full Course"),
    "german":                 ("German", "German", "GCSE (9-1) Full Course"),
    "italian":                ("Italian", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "physical-education":     ("Sports Studies", "Physical Education", "GCSE (9-1) Full Course"),
    "computer-science":       ("Computer Science", "Computer Science", "GCSE (9-1) Full Course"),
    "business-studies":       ("Business Studies", "Business", "GCSE (9-1) Full Course"),
    "business":               ("Business Studies", "Business", "GCSE (9-1) Full Course"),
    "sociology":              ("Sociology", "Social Studies", "GCSE (9-1) Full Course"),
    "psychology":             ("Psychology (General)", "Social Studies", "GCSE (9-1) Full Course"),
    "design-and-technology":  ("D & T", "Design & Technology", "GCSE (9-1) Full Course"),
    "food-preparation-and-nutrition": ("Food Technology", "Food Preparation & Nutrition", "GCSE (9-1) Full Course"),
    "food-and-nutrition":     ("Food Technology", "Food Preparation & Nutrition", "GCSE (9-1) Full Course"),
    "music":                  ("Music Studies (General)", "Music", "GCSE (9-1) Full Course"),
    "drama":                  ("Speech & Drama", "Drama", "GCSE (9-1) Full Course"),
    "statistics":             ("Statistics", "Statistics", "GCSE (9-1) Full Course"),
    "media-studies":          ("Media Studies", "Media / Film / TV", "GCSE (9-1) Full Course"),
    "film-studies":           ("Media Studies", "Film Studies", "GCSE (9-1) Full Course"),
    # DfE files GCSE Citizenship Studies under the "Community Development"
    # discount group (Social Studies group) - 19,680 entries / 777 schools
    # matches the JCQ Citizenship Studies total.
    "citizenship-studies":    ("Community Development", "Social Studies", "GCSE (9-1) Full Course"),
    "economics":              ("Economics", "Economics", "GCSE (9-1) Full Course"),
    "classical-civilisation": ("Classical Civilisation", "Classical Civilisation", "GCSE (9-1) Full Course"),
    "ancient-history":        ("Ancient History", "Ancient History", "GCSE (9-1) Full Course"),
    "latin":                  ("Latin", "Latin", "GCSE (9-1) Full Course"),
    "classical-greek":        ("Greek (Classic)", "Classical Greek", "GCSE (9-1) Full Course"),
    # Pearson 1GK0 "Greek" is MODERN Greek (listening + speaking papers), not
    # Classical Greek - checked against specs/edexcel/greek-1GK0.md.
    "greek":                  ("Greek", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "biblical-hebrew":        ("Other Classical Languages", "Biblical Hebrew", "GCSE (9-1) Full Course"),
    "astronomy":              ("Astronomy", "Other Sciences", "GCSE (9-1) Full Course"),
    "geology":                ("Geology", "Other Sciences", "GCSE (9-1) Full Course"),
    "electronics":            ("Electronics (Physics)", "Other Sciences", "GCSE (9-1) Full Course"),
    "engineering":            ("Engineering Studies", "Engineering", "GCSE (9-1) Full Course"),
    "arabic":                 ("Arabic", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "bengali":                ("Bengali", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "chinese":                ("Chinese", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "chinese-mandarin":       ("Chinese", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "gujarati":               ("Gujarati", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "hebrew":                 ("Hebrew Language", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "hebrew-modern":          ("Hebrew Language", "Other Modern Languages", "GCSE (9-1) Full Course"),
    # BTEC Tech Award Health & Social Care - the DfE files it under the
    # "Health Studies" discount group on the BTEC Technical Award qualification.
    "health-and-social-care": ("Health Studies", "Health", "BTEC Technical Award L1 / 2 - Band C - P-D*"),
    "music-technology":       ("Music Technology (Electronic)", "Music", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "japanese":               ("Japanese Language", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "panjabi":                ("Punjabi", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "persian":                ("Persian Language", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "polish":                 ("Polish", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "portuguese":             ("Portuguese", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "russian":                ("Russian", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "turkish":                ("Turkish", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "urdu":                   ("Urdu", "Other Modern Languages", "GCSE (9-1) Full Course"),
    "modern-greek":           ("Greek", "Other Modern Languages", "GCSE (9-1) Full Course"),
    # --- vocational families -------------------------------------------------
    "cambridge-nationals-creative-imedia": ("Multimedia", "Multimedia", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-sport-science": ("Sports / Movement Science", "Sports", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-sport-studies": ("Sports Studies", "Sports", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-enterprise-and-marketing": ("Business Studies", "Business", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-health-and-social-care": ("Health Studies", "Health", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-child-development": ("Childcare Skills", "Childcare", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-engineering-design": ("Engineering Studies", "Engineering", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-engineering-manufacture": ("Manufacturing Engineering", "Engineering", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-engineering-programmable-systems": ("Electronic / Electrical Engineering", "Engineering", "OCR Level 1 / 2 Cambridge National Certificate"),
    "cambridge-nationals-it": ("Computer Appreciation / Introduction", "Information and Communication Technology", "OCR Level 1 / 2 Cambridge National Certificate"),
    "level-1-2-vocational-award-in-hospitality-and-catering": ("Hospitality / Catering Studies", "Hospitality and Catering", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-health-and-social-care": ("Health Studies", "Health", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-engineering": ("Engineering Studies", "Engineering", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-ict": ("Computer Appreciation / Introduction", "Information and Communication Technology", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-retail-business": ("Retailing", "Business", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-sport-and-coaching-principles": ("Sports Studies", "Sports", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-constructing-the-built-environment": ("Construction and the Built Environment (Construction)", "Construction", "Level 1 / Level 2 vocational qualification (any AO and grade structure)"),
    "level-1-2-vocational-award-in-tourism": ("Tourism", "Tourism", "BTEC Technical Award L1 / 2 - Band C - P-D*"),
}

# Where a board runs two routes, its entries do NOT split evenly. Only two
# splits are actually documented (in admin/build-status.html BUILD_NOTES);
# everywhere else the report says so and splits evenly.
# Route weights (how a board's entries divide between its own routes, e.g.
# Geography A vs Geography B) are read from board_share.json, where they are
# derived from the boards' published June 2025 per-specification entry counts.
# ROUTE_WEIGHT is filled in main(); an empty entry means an even split, flagged.
ROUTE_WEIGHT = {}

# Board naming in specs/index.json -> board key used in board_share.json
BOARD_KEY = {"AQA": "AQA", "Edexcel": "Edexcel", "Pearson Edexcel": "Edexcel",
             "OCR": "OCR", "Eduqas": "Eduqas", "WJEC": "WJEC"}


def main():
    specs = load(os.path.join(ROOT, "specs", "index.json")) if False else \
        json.load(open(os.path.join(ROOT, "specs", "index.json"), encoding="utf-8"))
    sb = load("_supabase_subjects.json")
    dfe = load("dfe_subject_entries_2025.json")
    share_db = load("board_share.json")

    # Real route weights, derived from the boards' June 2025 per-spec entries.
    for key, rw in share_db.get("route_weights", {}).items():
        f, code = key.split("|", 1)
        ROUTE_WEIGHT[(f, code)] = (rw["weight_2025"], rw["source"])
        # RS is filed under two family slugs in build-status.
        if f == "religious-studies":
            ROUTE_WEIGHT[("religious-education", code)] = (rw["weight_2025"], rw["source"])

    # --- DfE lookup ---------------------------------------------------------
    dfe_idx = {}
    for r in dfe["rows"]:
        dfe_idx[(r["subject_discount_group"], r["subject_group"], r["qualification"])] = r

    # --- built specs (free tier only, spec_code may bundle several) ----------
    built_by_code = {}
    for s in sb["subjects"]:
        if s.get("school_id") or not s.get("spec_code"):
            continue
        for code in str(s["spec_code"]).split("/"):
            code = code.strip()
            if code:
                built_by_code[code] = s

    in_scope = [sp for sp in specs
                if not EXCLUDED_FAMILIES.get(subject_family(sp["subject"]))]
    excluded = [sp for sp in specs
                if EXCLUDED_FAMILIES.get(subject_family(sp["subject"]))]
    built = [sp for sp in in_scope if sp["spec_code"] in built_by_code]
    unbuilt = [sp for sp in in_scope if sp["spec_code"] not in built_by_code]

    # --- lesson-count reference: median live sibling on the same family -----
    fam_lessons = {}
    for sp in built:
        fam = subject_family(sp["subject"])
        s = built_by_code[sp["spec_code"]]
        fam_lessons.setdefault(fam, []).append(
            {"slug": s["slug"], "board": sp["board"], "lessons": s["lessons_total"]})

    LESSON_HINT = re.compile(
        r"~?\s*(\d{1,3})\s*[–—-]\s*(\d{1,3})\s*(?:article\s+|short\s+)?lesson"
        r"|~\s*(\d{1,3})\s+(?:article\s+)?lesson", re.I)

    def likely_lessons(fam, board, note_text=""):
        """Size reference. A build note that states its own lesson count wins -
        it is Tom's own decision about the shape of that build (several MFL
        specs are deliberately 8-10 lesson exam-technique guides, not full
        courses). Otherwise prefer a sibling spec already built on the SAME
        board (route B mirrors route A far better than a rival board does),
        then the median of built siblings, then a tier default."""
        def from_note(txt, where):
            m = LESSON_HINT.search(txt or "")
            if not m:
                return None
            if m.group(1):
                v = (int(m.group(1)) + int(m.group(2))) // 2
            else:
                v = int(m.group(3))
            return v, f"stated in {where} ({m.group(0).strip()})"

        hit = from_note(note_text, "the build note")
        if hit:
            return hit
        # A sibling spec in the same family may state the intended shape (the
        # MFL family is a set of 8-10 lesson exam-technique guides, and only
        # some of the notes say so). Keep the family consistent.
        for code, nt in sorted(BUILD_NOTES.get(fam, {}).items()):
            hit = from_note(nt.get("text", ""), f"a sibling note in this family ({code})")
            if hit:
                return hit
        sibs = [x for x in fam_lessons.get(fam, []) if x["lessons"] > 0]
        if sibs:
            ref = ", ".join(f"{x['board']} {x['lessons']}" for x in sibs)
            same = [x for x in sibs if x["board"] == board]
            if same:
                return same[0]["lessons"], f"same board already built ({ref})"
            vals = sorted(x["lessons"] for x in sibs)
            return vals[len(vals) // 2], f"median of sibling boards ({ref})"
        # No sibling built. Fall back on the size of a typical single-board
        # subject in the same entry tier.
        default = {"S": 60, "A": 45, "B": 35, "C": 25, "N": 18}[tier_for(fam)]
        return default, "no sibling built - tier default"

    # England-accessible boards per family. WJEC specs are Qualifications
    # Wales-regulated and "not available to centres in England" (the stated
    # reason behind every Wales-only SKIP note), so they do not dilute an
    # England share. Used only as a flagged proxy where no published share
    # exists: proxy = subject entries / number of England-accessible boards.
    # A board that offers two routes (Geography A / Geography B) sells its share
    # across both, so a single route is worth share/routes. Short-course specs
    # are excluded from the route count - the DfE full-course entry figure does
    # not contain them.
    def england_spec(sp):
        b = BOARD_KEY.get(sp["board"], sp["board"])
        if b == "WJEC":
            return False
        return "short course" not in sp["subject"].lower()

    fam_boards, fam_routes = {}, {}
    for sp in in_scope:
        if not england_spec(sp):
            continue
        fam = subject_family(sp["subject"])
        b = BOARD_KEY.get(sp["board"], sp["board"])
        fam_boards.setdefault(fam, set()).add(b)
        fam_routes[(fam, b)] = fam_routes.get((fam, b), 0) + 1

    def spec_share(fam, boardk, spec_code=None):
        """England share of the subject that one spec (board route) can reach,
        with a flag saying whether the board share behind it is published."""
        pub = share_db.get("shares", {}).get(fam, {}).get("boards")
        n_boards = len(fam_boards.get(fam, set())) or 1
        if pub and boardk in pub:
            bshare, known = pub[boardk], True
        else:
            bshare, known = 1.0 / n_boards, False
        routes = fam_routes.get((fam, boardk), 1) or 1
        rw = ROUTE_WEIGHT.get((fam, spec_code))
        if rw:
            return bshare * rw[0], known, n_boards, routes
        return bshare / routes, known, n_boards, routes

    rows, skipped = [], []
    for sp in unbuilt:
        fam = subject_family(sp["subject"])
        notes = BUILD_NOTES.get(fam, {})
        note = notes.get(sp["spec_code"])
        tag = note["tag"] if note else ""
        text = note["text"] if note else (
            notes.get("_general", {}).get("text", "") if notes else "")
        general = notes.get("_general", {}).get("text", "")

        dg = DFE_MAP.get(fam)
        drow = dfe_idx.get(dg) if dg and dg[0] else None
        entries = drow["entries"] if drow else None
        schools = drow["schools_entering"] if drow else None

        board = BOARD_KEY.get(sp["board"], sp["board"])
        sh = share_db.get("shares", {}).get(fam, {})
        share_src = sh.get("source_label")
        share_url = sh.get("source_url")

        share, share_known, n_boards, routes = spec_share(fam, board, sp["spec_code"])
        if board == "WJEC":
            # Qualifications Wales-regulated: "not available to centres in
            # England". The DfE England dataset cannot size it.
            est, share, share_known = 0, None, False
            est_basis = "Wales only - no England entries; DfE data does not apply"
        elif entries is None:
            est = None
            est_basis = "no DfE subject match"
        else:
            est = int(round(entries * share))
            if share_known:
                est_basis = "entries x published board share"
                if routes > 1:
                    rw = ROUTE_WEIGHT.get((fam, sp["spec_code"]))
                    est_basis += (f" x {rw[0]:.0%} of that board ({rw[1]})" if rw
                                  else f", split evenly across {routes} routes on this board")
            else:
                est_basis = (f"SHARE UNKNOWN - equal-split proxy, "
                             f"1/{n_boards} England boards")
                if routes > 1:
                    rw = ROUTE_WEIGHT.get((fam, sp["spec_code"]))
                    est_basis += (f" x {rw[0]:.0%} of that board ({rw[1]})" if rw
                                  else f", split evenly across {routes} routes")

        lessons, lesson_ref = likely_lessons(fam, board, text)
        cost = cost_for(lessons, tag or "build")

        rec = {
            "spec_code": sp["spec_code"], "board": sp["board"],
            "subject": sp["subject"], "family": fam, "slug": sp["slug"],
            "tier_letter": tier_for(fam), "tag": tag or "build",
            "entries": entries, "schools_entering": schools,
            "board_share": share, "board_share_known": share_known,
            "board_share_source": share_src if share_known else None,
            "board_share_url": share_url if share_known else None,
            "england_boards": n_boards,
            # Board-level share in each series, for the direction-of-travel column.
            # Not route-split: it describes the whole board, not this one route.
            "board_share_2025_boardlevel": (sh.get("boards", {}).get(board)
                                            if share_known else None),
            "board_share_2026_boardlevel": (sh.get("boards_2026", {}).get(board)
                                            if share_known else None),
            "board_delta_pp": (sh.get("delta_pp", {}).get(board)
                               if share_known else None),
            "route_weight": ROUTE_WEIGHT.get((fam, sp["spec_code"]), (None, None))[0],
            "route_weight_source": ROUTE_WEIGHT.get((fam, sp["spec_code"]),
                                                    (None, None))[1],
            "est_students": est, "est_basis": est_basis,
            "likely_lessons": lessons, "lesson_reference": lesson_ref,
            "est_cost_gbp": cost,
            "note": text, "general_note": general,
            "dfe_subject": dg[0] if dg else None,
        }
        (skipped if rec["tag"] in ("alias", "skip") else rows).append(rec)

    rows.sort(key=lambda r: (-(r["est_students"] or 0), r["subject"]))
    skipped.sort(key=lambda r: (r["tag"], -(r["entries"] or 0)))

    # --- coverage, computed per SUBJECT FAMILY so no pupil is double counted -
    # For each family with a DfE entry figure, work out what fraction of that
    # subject's England entries sit on a board we have built. Published shares
    # are used where they exist; otherwise the equal-split proxy, flagged.
    coverage, cov_built, cov_remaining, cov_parked = [], 0.0, 0.0, 0.0
    fams = sorted({subject_family(sp["subject"]) for sp in in_scope})
    skipped_codes = {r["spec_code"] for r in skipped}
    for fam in fams:
        dg = DFE_MAP.get(fam)
        drow = dfe_idx.get(dg) if dg and dg[0] else None
        if not drow:
            continue
        fam_specs = [sp for sp in in_scope
                     if subject_family(sp["subject"]) == fam and england_spec(sp)]
        f_built = f_rem = f_park = 0.0
        boards_built, boards_rem, boards_parked = set(), set(), set()
        known_basis = False
        for sp in fam_specs:
            b = BOARD_KEY.get(sp["board"], sp["board"])
            s, known, _, _ = spec_share(fam, b, sp["spec_code"])
            known_basis = known_basis or known
            if sp["spec_code"] in built_by_code:
                f_built += s
                boards_built.add(b)
            elif sp["spec_code"] in skipped_codes:
                f_park += s
                boards_parked.add(b)
            else:
                f_rem += s
                boards_rem.add(b)
        f_built = min(1.0, f_built)
        pub = share_db.get("shares", {}).get(fam, {}).get("boards") if known_basis else None
        cov_built += drow["entries"] * f_built
        cov_remaining += drow["entries"] * f_rem
        cov_parked += drow["entries"] * f_park
        coverage.append({
            "family": fam, "entries": drow["entries"],
            "schools": drow["schools_entering"],
            "qualification": drow["qualification"],
            "boards_built": sorted(boards_built),
            "boards_remaining": sorted(boards_rem),
            "boards_parked": sorted(boards_parked),
            "share_basis": "published" if pub else "equal split",
            "pct_built": round(100 * f_built, 1),
            "entries_built": int(round(drow["entries"] * f_built)),
            "entries_remaining": int(round(drow["entries"] * f_rem)),
        })
    coverage.sort(key=lambda r: -r["entries"])
    built_reach = int(round(cov_built))
    rem_reach = int(round(cov_remaining))
    parked_reach = int(round(cov_parked))
    total_entries_scope = sum(c["entries"] for c in coverage)

    # --- niche subjects (<= 3,000 entries) with their top schools -----------
    niche = [r for r in dfe["rows"] if r["entries"] <= dfe["niche_threshold"]]
    niche.sort(key=lambda r: -r["entries"])

    # --- tier letter vs the data -------------------------------------------
    TIER_BANDS = [("S", 400000, 10 ** 9), ("A", 100000, 400000),
                  ("B", 30000, 100000), ("C", 10000, 30000), ("N", 0, 10000)]

    def band(entries):
        for letter, lo, hi in TIER_BANDS:
            if lo <= entries < hi:
                return letter
        return "N"

    tier_conflicts = []
    seen_fam = set()
    for sp in in_scope:
        fam = subject_family(sp["subject"])
        if fam in seen_fam:
            continue
        seen_fam.add(fam)
        dg = DFE_MAP.get(fam)
        drow = dfe_idx.get(dg) if dg and dg[0] else None
        if not drow:
            continue
        actual = band(drow["entries"])
        stated = tier_for(fam)
        if actual != stated:
            tier_conflicts.append({
                "family": fam, "stated": stated, "actual": actual,
                "entries": drow["entries"], "schools": drow["schools_entering"],
                "dfe_subject": drow["subject_discount_group"],
                "qualification": drow["qualification"],
                "in_entry_tier_map": fam in ENTRY_TIER,
            })
    tier_conflicts.sort(key=lambda r: -r["entries"])

    # --- cross-check: DfE England subject total vs the 2025 board sum --------
    # Both now describe the summer 2025 series, so the residual measures only
    # population difference (DfE = KS4 pupils in England; boards = all their
    # entries, all ages, and for AQA/OCR/Eduqas all countries).
    crosscheck = []
    for f, s in sorted(share_db.get("shares", {}).items()):
        dg = DFE_MAP.get(f)
        drow = dfe_idx.get(dg) if dg and dg[0] else None
        tot25 = s.get("board_total_2025")
        if not drow or not tot25:
            continue
        crosscheck.append({
            "family": f,
            "dfe_entries": drow["entries"],
            "board_sum_2025": tot25,
            "board_sum_2026": s.get("board_total_2026"),
            "ratio_2025": round(tot25 / drow["entries"], 3),
            "ratio_2026": (round(s["board_total_2026"] / drow["entries"], 3)
                           if s.get("board_total_2026") else None),
            "residual": tot25 - drow["entries"],
            "residual_pct": round(100 * (tot25 - drow["entries"]) / drow["entries"], 1),
            "dfe_subject": drow["subject_discount_group"],
            "qualification": drow["qualification"],
        })
    crosscheck.sort(key=lambda r: -abs(r["residual_pct"]))
    ratios = [c["ratio_2025"] for c in crosscheck]
    ratios26 = [c["ratio_2026"] for c in crosscheck if c["ratio_2026"]]

    def median(v):
        v = sorted(v)
        return round(v[len(v) // 2], 3) if v else None

    # Entries that a board counts but the DfE KS4 population cannot: post-16
    # resits. AQA publishes the age split and it dominates three subjects.
    RESIT_HEAVY = {"mathematics", "english-language", "english-literature"}

    def quality(rows, year):
        if not rows:
            return None
        dev = [abs(r[f"ratio_{year}"] - 1) for r in rows]
        dev.sort()
        w = (sum(r["dfe_entries"] * abs(r[f"ratio_{year}"] - 1) for r in rows)
             / sum(r["dfe_entries"] for r in rows))
        return {"families": len(rows),
                "median_abs_dev": round(dev[len(dev) // 2], 4),
                "mean_abs_dev": round(sum(dev) / len(dev), 4),
                "entries_weighted_abs_dev": round(w, 4),
                "within_5pct": sum(1 for x in dev if x <= 0.05)}

    both = [c for c in crosscheck if c["ratio_2026"]]
    ex_resit = [c for c in both if c["family"] not in RESIT_HEAVY]

    # Which families still rest on a 2026 share (no 2025 board release found)?
    on_2026 = sorted(f for f, s in share_db.get("shares", {}).items()
                     if s.get("year") != 2025)

    result = {
        "generated": "2026-09-06",
        "share_year": 2025,
        "crosscheck": crosscheck,
        "crosscheck_summary": {
            "families": len(crosscheck),
            "median_ratio_2025": median(ratios),
            "median_ratio_2026": median(ratios26),
            "within_10pct_2025": sum(1 for r in ratios if 0.90 <= r <= 1.10),
            "within_10pct_2026": sum(1 for r in ratios26 if 0.90 <= r <= 1.10),
            "worst": crosscheck[0]["family"] if crosscheck else None,
            "resit_heavy": sorted(RESIT_HEAVY),
            "quality": {
                "all_2025": quality(both, 2025), "all_2026": quality(both, 2026),
                "ex_resit_2025": quality(ex_resit, 2025),
                "ex_resit_2026": quality(ex_resit, 2026),
            },
        },
        "index_gaps": share_db.get("index_gaps", []),
        "route_weights": share_db.get("route_weights", {}),
        "families_still_on_2026_share": on_2026,
        "families_without_board_release": sorted(
            f for f, s in share_db.get("shares", {}).items() if s.get("no_board_release")),
        "totals": {
            "specs_total": len(specs),
            "specs_in_scope": len(in_scope),
            "specs_excluded_portfolio": len(excluded),
            "specs_built": len(built),
            "specs_unbuilt": len(unbuilt),
            "buildable_remaining": len(rows),
            "skipped_or_aliased": len(skipped),
            "england_entries_in_scope": total_entries_scope,
            "england_entries_reached_built": built_reach,
            "england_entries_reached_remaining": rem_reach,
            "england_entries_parked": parked_reach,
            "total_cost_remaining_gbp": round(sum(r["est_cost_gbp"] for r in rows), 2),
            "total_lessons_remaining": sum(r["likely_lessons"] for r in rows),
        },
        "cost_model": {
            "api_per_lesson_gbp": API_PER_LESSON_GBP,
            "narration_per_lesson_gbp": NARRATION_PER_LESSON_GBP,
            "factcheck_per_subject_gbp": FACTCHECK_PER_SUBJECT_GBP,
            "port_factor": COST_FACTOR["port"],
        },
        "coverage_by_family": coverage,
        "table1_remaining": rows,
        "table2_skipped": skipped,
        "table3_niche": niche,
        "tier_conflicts": tier_conflicts,
        "board_share_db": share_db,
        "dfe_source": dfe["source"],
        "excluded_families": sorted(EXCLUDED_FAMILIES),
    }
    out = os.path.join(HERE, "remaining_builds.json")
    json.dump(result, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {out}")
    print(json.dumps(result["totals"], indent=1))
    return result


if __name__ == "__main__":
    main()
