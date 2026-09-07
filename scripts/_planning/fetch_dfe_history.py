"""Multi-year school-level entries for the niche GCSE / vocational subjects.

Two DfE sources, both read-only:

1. Explore Education Statistics (EES). The publication "Key stage 4 performance"
   (c8756008-ed50-4632-9b96-01b5ca002a43) carries a school-level subject data set
   ONLY for the two most recent releases:
     2024/25  API data set 1ae39901-b462-df76-b108-640a078d7944 (queryable)
     2023/24  CSV data set file 914fe46b-... (no API data set, 225 Mb CSV)
   The 2022/23, 2021/22, 2020/21 and 2019/20 releases carry no school-level
   subject file at all, so the EES API cannot give a four-year series.

2. The school performance tables download service, which publishes the same
   underlying table ("KS4 underlying data - entries and grades") for
   2021/22 .. 2024/25 as an xlsx with one stable schema. That is the series
   used here. The 2024/25 year is cross-checked against the EES API output in
   dfe_subject_entries_2025.json, so the fallback source is validated.

   2019/20 and 2020/21 have no rows anywhere: exams were cancelled (CAGs then
   TAGs) and no performance tables were published. 2018/19 is no longer offered
   by the download service (404).

Writes:
  scripts/_planning/dfe_datasets.json        every dataset / file / filter id used
  scripts/_planning/dfe_niche_history.json   raw per-school-per-year entries
"""

import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get(
    "DFE_CACHE",
    os.path.join(os.environ.get("TEMP", "/tmp"), "claude",
                 "C--Users-tshau-Documents-Study-Vault",
                 "88006801-843c-4d74-957a-5eebdef537b9", "scratchpad"))

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

EES_API = "https://api.education.gov.uk/statistics/v1"
EES_CONTENT = "https://content.explore-education-statistics.service.gov.uk/api"
PUBLICATION = "c8756008-ed50-4632-9b96-01b5ca002a43"
PT = "https://www.compare-school-performance.service.gov.uk/download-data"

# academic year -> performance-tables year slug
YEARS = {
    "2021/22": "2021-2022",
    "2022/23": "2022-2023",
    "2023/24": "2023-2024",
    "2024/25": "2024-2025",
}
NO_EXAM_YEARS = ["2019/20", "2020/21"]

# ---------------------------------------------------------------- the subjects
# Table 3 of remaining_builds_2025.html lists (subject discount group x
# qualification) pairs. Two things break a naive year-on-year match:
#
#  * qualification labels are punctuated differently by the two sources
#    ("L1 / 2" vs "L1/2") - handled by norm_qual;
#  * from 2023/24 DfE folded BTEC First, WJEC L1/L2, AQA Technical Award and
#    most VRQ rows into one "Level 1/Level 2 vocational qualification (any AO
#    and grade structure)" bucket, and re-coded several vocational discount
#    groups. GCSE (9-1) Full Course is untouched.
#
# So GCSE rows are matched on the exact qualification and carry a four-year
# series; vocational rows are rolled up over every Level 1/2 awarding route in
# the discount group, and each one is tested for a taxonomy break.
TOTAL_ROW_LABELS = {"total number entered", "total exam entries"}


def norm_qual(q):
    if q is None:
        return ""
    return re.sub(r"\s*/\s*", "/", re.sub(r"\s+", " ", str(q).strip())).lower()


def norm_subject(s):
    if s is None:
        return ""
    return re.sub(r"\s*/\s*", "/", re.sub(r"\s+", " ", str(s).strip())).lower()


GCSE_FULL = norm_qual("GCSE (9-1) Full Course")

# Qualifications that are NOT part of the Level 1/2 vocational family.
NON_VOCATIONAL_QUALS = {
    norm_qual(q) for q in [
        "GCSE (9-1) Full Course", "GCSE (9-1) Full Course (Double Award)",
        "GCE AS level", "Free standing Maths Qual Level 3",
        "Grade 6 Music or Dance", "Grade 7 Music or Dance",
        "Grade 8 Music or Dance", "Grade 6 Drama Music Lit Speech",
        "Grade 7 Drama Music Lit Speech", "Grade 8 Drama Music Lit Speech",
    ]}

# label, discount group, mode, the Table 3 qualification(s) the row covers
TABLE3 = [
    ("Engineering Studies", "gcse", ["GCSE (9-1) Full Course"]),
    ("Portuguese", "gcse", ["GCSE (9-1) Full Course"]),
    ("Turkish", "gcse", ["GCSE (9-1) Full Course"]),
    ("Ancient History", "gcse", ["GCSE (9-1) Full Course"]),
    ("Astronomy", "gcse", ["GCSE (9-1) Full Course"]),
    ("Greek (Classic)", "gcse", ["GCSE (9-1) Full Course"]),
    ("Punjabi", "gcse", ["GCSE (9-1) Full Course"]),
    ("Japanese Language", "gcse", ["GCSE (9-1) Full Course"]),
    ("Electronics (Physics)", "gcse", ["GCSE (9-1) Full Course"]),
    ("Other Classical Languages", "gcse", ["GCSE (9-1) Full Course"]),
    ("Persian Language", "gcse", ["GCSE (9-1) Full Course"]),
    ("Greek", "gcse", ["GCSE (9-1) Full Course"]),
    ("Hebrew Language", "gcse", ["GCSE (9-1) Full Course"]),
    ("Geology", "gcse", ["GCSE (9-1) Full Course"]),
    ("Bengali", "gcse", ["GCSE (9-1) Full Course"]),
    ("Gujarati", "gcse", ["GCSE (9-1) Full Course"]),
    ("Health Studies", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Animal Care", "vocational", ["BTEC Technical Award L1 / 2 - Band C - P-D*"]),
    ("Business / Finance", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Beauty Care / Services", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)",
      "VRQ Level 2"]),
    ("Retailing", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Music Technology (Electronic)", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Art & Design", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Electronic / Electrical Engineering", "vocational",
     ["OCR Level 1 / 2 Cambridge National Certificate"]),
    ("Multimedia", "vocational",
     ["Level 1 / Level 2 vocational qualification (any AO and grade structure)"]),
    ("Construction and the Built Environment", "vocational", ["VRQ Level 2"]),
    ("Land based Studies", "vocational", ["VRQ Level 2"]),
]

# Named in the brief (or one whisker over the 3,000 line) and part of the same
# small-cohort families, so they get the same treatment and are flagged
# "extended" on the page.
EXTENDED = [
    ("Latin", "gcse", ["GCSE (9-1) Full Course"]),
    ("Polish", "gcse", ["GCSE (9-1) Full Course"]),
    ("Chinese", "gcse", ["GCSE (9-1) Full Course"]),
    ("Arabic", "gcse", ["GCSE (9-1) Full Course"]),
    ("Urdu", "gcse", ["GCSE (9-1) Full Course"]),
    ("Italian", "gcse", ["GCSE (9-1) Full Course"]),
    ("Russian", "gcse", ["GCSE (9-1) Full Course"]),
]

TARGETS = {}          # normalised discount group -> record
for sdg, mode, quals in TABLE3:
    TARGETS[norm_subject(sdg)] = {"subject_discount_group": sdg, "mode": mode,
                                  "qualifications": quals, "set": "table3"}
for sdg, mode, quals in EXTENDED:
    TARGETS[norm_subject(sdg)] = {"subject_discount_group": sdg, "mode": mode,
                                  "qualifications": quals, "set": "extended"}


def row_counts(qual_norm, mode):
    """Does this qualification belong to the row's series?"""
    if mode == "gcse":
        return qual_norm == GCSE_FULL
    return qual_norm not in NON_VOCATIONAL_QUALS


# ---------------------------------------------------------------- http helpers
def jget(url, timeout=180):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def download(url, path, timeout=900):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=timeout).read()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


# ---------------------------------------------------------------- ees metadata
def ees_inventory():
    """Walk every KS4 release and record which of them carry a school-level
    subject data set, plus the API filter ids for the one release that has an
    API data set."""
    releases = jget(f"{EES_CONTENT}/publications/key-stage-4-performance/releases")
    inv = []
    for rel in releases:
        files = []
        page = 1
        while True:
            d = jget(f"{EES_CONTENT}/data-set-files?releaseId={rel['id']}"
                     f"&pageSize=40&page={page}")
            files += d["results"]
            if page >= d["paging"]["totalPages"]:
                break
            page += 1
        school_subject = [
            f for f in files
            if "subject" in f["title"].lower()
            and ("school" in f["title"].lower() or "institution level" in f["title"].lower())
            and "entries and grades" in f["title"].lower()
        ]
        inv.append({
            "release": rel["title"],
            "release_slug": rel["slug"],
            "release_version_id": rel["id"],
            "release_id": rel["releaseId"],
            "published": rel["published"][:10],
            "data_set_file_count": len(files),
            "school_level_subject_files": [
                {"data_set_file_id": f["id"], "file_id": f["fileId"],
                 "title": f["title"], "filename": f["filename"],
                 "size": f["fileSize"],
                 "download_url": f"{EES_CONTENT}/releases/{rel['id']}/files/{f['fileId']}"}
                for f in school_subject],
        })

    api_sets = []
    for page in (1, 2):
        d = jget(f"{EES_API}/publications/{PUBLICATION}/data-sets?page={page}")
        api_sets += d["results"]
        if page >= d["paging"]["totalPages"]:
            break
    api_school_subject = [s for s in api_sets
                          if s["title"] == "Subject school level exam data"]

    filters = {}
    for s in api_school_subject:
        meta = jget(f"{EES_API}/data-sets/{s['id']}/meta?types=Filters")
        for f in meta["filters"]:
            keep = {}
            for o in f["options"]:
                lab = o["label"]
                if (f["label"] in ("Grade", "Qualification")
                        or lab in {r["subject_discount_group"] for r in TARGETS.values()}):
                    keep[o["id"]] = lab
            filters[f["id"]] = {"label": f["label"], "column": f.get("column"),
                                "option_count": len(f["options"]),
                                "options_used": keep}
    return inv, api_school_subject, filters


# ---------------------------------------------------------------- the xlsx pull
def year_workbook(year, slug):
    path = os.path.join(CACHE, f"ks4_entries_{slug}.xlsx")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    url = (f"{PT}?download=true&regions=0&filters=KS4Underlying"
           f"&fileformat=csv&year={slug}&meta=false")
    print(f"  downloading {year} ...", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    blob = urllib.request.urlopen(req, timeout=900).read()
    z = zipfile.ZipFile(io.BytesIO(blob))
    name = [n for n in z.namelist() if "entriesandgrades" in n][0]
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(z.read(name))
    return path


def scan_year(year, slug):
    """-> (per_pair_totals, per_school, distinct_pairs, row_count)"""
    path = year_workbook(year, slug)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Institution_results"]
    rows = ws.iter_rows(values_only=True)
    # header casing drifts between years ("GRADE" in 2021/22, "Grade" after)
    header = [str(h).strip().lower() if h else "" for h in next(rows)]
    ix = {h: i for i, h in enumerate(header)}
    c_urn = ix["unique reference number (urn)"]
    c_name = ix["school or college name"]
    c_type = ix["institution type"]
    c_qual = ix["qualification"]
    c_sdg = ix["subject discount group"]
    c_grade = ix["grade"]
    c_n = ix["number of entries at grade"]

    pair_totals = defaultdict(int)
    pair_schools = defaultdict(set)
    per_school = defaultdict(dict)      # sdg -> urn -> {name, type, entries}
    routes = defaultdict(lambda: defaultdict(int))   # sdg -> qualification -> n
    n_rows = 0
    for r in rows:
        n_rows += 1
        g = r[c_grade]
        if not isinstance(g, str) or g.strip().lower() not in TOTAL_ROW_LABELS:
            continue
        try:
            n = int(r[c_n])
        except (TypeError, ValueError):
            continue
        if n <= 0:
            continue
        q = norm_qual(r[c_qual])
        s = norm_subject(r[c_sdg])
        pair_totals[(s, q)] += n
        urn = r[c_urn]
        if urn is not None:
            pair_schools[(s, q)].add(urn)
        target = TARGETS.get(s)
        if target and urn is not None and row_counts(q, target["mode"]):
            rec = per_school[s].setdefault(
                str(urn), {"name": r[c_name], "type": r[c_type], "entries": 0})
            rec["entries"] += n
            rec["name"] = r[c_name] or rec["name"]
            rec["type"] = r[c_type] or rec["type"]
            routes[s][str(r[c_qual]).strip()] += n
    wb.close()
    pairs = {f"{s}||{q}": {"entries": v, "schools": len(pair_schools[(s, q)])}
             for (s, q), v in pair_totals.items()}
    return pairs, per_school, {k: dict(v) for k, v in routes.items()}, n_rows


# ---------------------------------------------------------------- main
def main():
    print("EES inventory ...", flush=True)
    inv, api_sets, filters = ees_inventory()

    datasets = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "note": (
            "The EES API exposes a school-level subject data set for 2024/25 "
            "only. The 2023/24 release carries the same table as a plain CSV "
            "data-set file (no API data set). 2022/23 and earlier carry no "
            "school-level subject file at all, and the publication has no "
            "2018/19 release (its earliest is 2019/20). The four-year series on this "
            "page therefore comes from the school performance tables download "
            "service, which publishes the same underlying table for 2021/22 "
            "onwards under one stable schema; 2024/25 is cross-checked against "
            "the EES API figures."),
        "ees": {
            "publication": "Key stage 4 performance",
            "publication_id": PUBLICATION,
            "api_root": EES_API,
            "content_api_root": EES_CONTENT,
            "releases": inv,
            "api_data_sets": [
                {"id": s["id"], "title": s["title"],
                 "latest_version": s["latestVersion"]["version"],
                 "time_periods": s["latestVersion"]["timePeriods"],
                 "total_results": s["latestVersion"]["totalResults"]}
                for s in api_sets],
            "api_filters_2024_25": filters,
            "indicator_2024_25": {
                "id": "TEpPJ", "label": "Number of entries at grade"},
        },
        "performance_tables": {
            "service": "Find school and college performance data in England",
            "download_endpoint": PT,
            "query": ("?download=true&regions=0&filters=KS4Underlying"
                      "&fileformat=csv&year={YYYY-YYYY}&meta=false"),
            "file_in_zip": "england_ks4underlying_entriesandgrades_2.xlsx",
            "sheet": "Institution_results",
            "row_filter": "GRADE == 'Total number entered'",
            "years": {y: {"slug": s,
                          "url": (f"{PT}?download=true&regions=0"
                                  f"&filters=KS4Underlying&fileformat=csv"
                                  f"&year={s}&meta=false")}
                      for y, s in YEARS.items()},
            "years_unavailable": {
                "2018/19": "404 from the download service - no longer offered",
                "2019/20": "exams cancelled (centre assessed grades); no performance tables",
                "2020/21": "exams cancelled (teacher assessed grades); no performance tables",
            },
        },
    }
    json.dump(datasets, open(os.path.join(HERE, "dfe_datasets.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote dfe_datasets.json", flush=True)

    all_pairs, all_schools, all_routes, rowcounts = {}, {}, {}, {}
    for year, slug in YEARS.items():
        t = time.time()
        pairs, per_school, routes, n_rows = scan_year(year, slug)
        all_pairs[year] = pairs
        all_schools[year] = per_school
        all_routes[year] = routes
        rowcounts[year] = n_rows
        print(f"  {year}: {n_rows:,} rows, {len(pairs)} subject/qual pairs, "
              f"{round(time.time() - t)}s", flush=True)

    subjects = []
    for key, meta in TARGETS.items():
        schools = {}
        for year in YEARS:
            for urn, rec in all_schools[year].get(key, {}).items():
                sch = schools.setdefault(urn, {"urn": urn, "name": rec["name"],
                                               "type": rec["type"],
                                               "entries": {}})
                sch["entries"][year] = rec["entries"]
                sch["name"] = rec["name"] or sch["name"]
                sch["type"] = rec["type"] or sch["type"]
        years = {}
        for year in YEARS:
            per = all_schools[year].get(key, {})
            years[year] = {"entries": sum(v["entries"] for v in per.values()),
                           "schools": len(per)}

        # taxonomy break: the vocational rows were re-coded in 2023/24, so a
        # discount group can vanish, appear, or jump by a large factor for
        # reasons that have nothing to do with schools changing their offer.
        a, b = years["2022/23"]["entries"], years["2023/24"]["entries"]
        broke = False
        if meta["mode"] == "vocational":
            if a == 0 and b > 0:
                broke = True
            elif a > 0 and b == 0:
                broke = True
            elif a and b and (max(a, b) / min(a, b)) >= 4:
                broke = True

        subjects.append({
            "subject_discount_group": meta["subject_discount_group"],
            "mode": meta["mode"],
            "qualification": " + ".join(meta["qualifications"]),
            "qualifications": meta["qualifications"],
            "set": meta["set"],
            "key": key,
            "taxonomy_break_2023_24": broke,
            "comparable_years": (list(YEARS) if not broke
                                 else ["2023/24", "2024/25"]),
            "routes_by_year": {y: all_routes[y].get(key, {}) for y in YEARS},
            "totals": years,
            "schools": list(schools.values()),
        })
    subjects.sort(key=lambda r: -r["totals"]["2024/25"]["entries"])

    json.dump(all_pairs, open(os.path.join(HERE, "_dfe_pairs_by_year.json"), "w",
                              encoding="utf-8"), ensure_ascii=False, indent=1)

    payload = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "years": list(YEARS),
        "years_without_exams": NO_EXAM_YEARS,
        "source": datasets,
        "row_counts": rowcounts,
        "subjects": subjects,
    }
    out = os.path.join(HERE, "dfe_niche_history.json")
    json.dump(payload, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"wrote {out}: {len(subjects)} subjects", flush=True)

    # ---- cross-check 2024/25 against the EES API aggregate we already hold
    ref_path = os.path.join(HERE, "dfe_subject_entries_2025.json")
    if os.path.exists(ref_path):
        ref = json.load(open(ref_path, encoding="utf-8"))
        print("\ncross-check 2024/25  performance tables xlsx vs EES API")
        bad = 0
        for sub in subjects:
            k = norm_subject(sub["subject_discount_group"])
            theirs = 0
            for r in ref["rows"]:
                if norm_subject(r["subject_discount_group"]) != k:
                    continue
                if row_counts(norm_qual(r["qualification"]), sub["mode"]):
                    theirs += r["entries"]
            mine = sub["totals"]["2024/25"]["entries"]
            flag = "" if theirs == mine else "  <-- DIFFERS"
            if theirs != mine:
                bad += 1
            print(f"  {sub['subject_discount_group'][:38]:38} {sub['mode']:11} "
                  f"xlsx {mine:>6}  ees {theirs:>6}{flag}")
        print(f"  {len(subjects) - bad}/{len(subjects)} match")


if __name__ == "__main__":
    sys.exit(main())
