"""Fetch England KS4 2024/25 school-level exam entries from DfE Explore Education
Statistics and aggregate them by subject.

Dataset: "Subject school level exam data", KS4 performance 2024/25
id 1ae39901-b462-df76-b108-640a078d7944

Read-only. Writes scripts/_planning/dfe_subject_entries_2025.json
"""

import json
import os
import time
import urllib.error
import urllib.request

DATASET = "1ae39901-b462-df76-b108-640a078d7944"
API = f"https://api.education.gov.uk/statistics/v1/data-sets/{DATASET}"
HERE = os.path.dirname(os.path.abspath(__file__))

GRADE_TOTAL_ENTRIES = "mgN9K"          # grade filter: "Total exam entries"
QUALS = {
    "AHDJG": "GCSE (9-1) Full Course",
    "V4Hh5": "GCSE (9-1) Full Course (Double Award)",
    "U3TrR": "Level 1 / Level 2 vocational qualification (any AO and grade structure)",
    "oWV1m": "OCR Level 1 / 2 Cambridge National Certificate",
    "hsusy": "BTEC Technical Award L1 / 2 - Band C - P-D*",
    "rGZFN": "VRQ Level 2",
}
IND_ENTRIES = "TEpPJ"                  # "Number of entries at grade"

F_QUAL = "yM9aB"
F_SUBJECT_DG = "dmG0Z"                 # subject_discount_group (78 options, granular)
F_GRADE = "1wmi3"
F_SUBJECT_GROUP = "b7NtT"              # subject (51 options, coarse)

NICHE_THRESHOLD = 3000                 # <= this many entries -> list top schools


def get(url, timeout=600):
    req = urllib.request.Request(url, headers={"User-Agent": "StudyVault-research"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def post(body, timeout=600, tries=4):
    data = json.dumps(body).encode()
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                API + "/query", data=data, method="POST",
                headers={"Content-Type": "application/json",
                         "User-Agent": "StudyVault-research"})
            return json.load(urllib.request.urlopen(req, timeout=timeout))
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == tries - 1:
                raise
            print(f"  retry {attempt + 1} after {exc}")
            time.sleep(5 * (attempt + 1))


def load_meta():
    path_f = os.path.join(HERE, "_dfe_meta_filters.json")
    path_l = os.path.join(HERE, "_dfe_meta_locations.json")
    if not os.path.exists(path_f):
        json.dump(get(API + "/meta?types=Filters"), open(path_f, "w", encoding="utf-8"),
                  ensure_ascii=False)
    if not os.path.exists(path_l):
        json.dump(get(API + "/meta?types=Locations"), open(path_l, "w", encoding="utf-8"),
                  ensure_ascii=False)
    filters = json.load(open(path_f, encoding="utf-8"))
    locations = json.load(open(path_l, encoding="utf-8"))

    labels = {}
    for f in filters["filters"]:
        for o in f["options"]:
            labels.setdefault(f["id"], {})[o["id"]] = o["label"]

    schools = {}
    for lv in locations["locations"]:
        if lv["level"]["code"] != "SCH":
            continue
        for o in lv["options"]:
            schools[o["id"]] = {"name": o.get("label"),
                                "urn": o.get("urn"),
                                "laEstab": o.get("laEstab")}
    return labels, schools


def fetch_rows():
    """Every school-level 'Total exam entries' row for the qualification types
    we care about. The subject filter values ride along in each row, so one
    sweep covers every subject."""
    body = {
        "criteria": {"and": [
            {"filters": {"in": [GRADE_TOTAL_ENTRIES]}},
            {"filters": {"in": list(QUALS)}},
        ]},
        "indicators": [IND_ENTRIES],
        "page": 1,
        "pageSize": 10000,
    }
    first = post(body)
    total_pages = first["paging"]["totalPages"]
    print(f"rows: {first['paging']['totalResults']} over {total_pages} pages")
    rows = list(first["results"])
    for p in range(2, total_pages + 1):
        body["page"] = p
        rows += post(body)["results"]
        print(f"  page {p}/{total_pages} -> {len(rows)} rows")
    return rows


def main():
    labels, schools = load_meta()
    rows = fetch_rows()

    agg = {}
    for r in rows:
        f = r.get("filters", {})
        if r.get("geographicLevel") != "SCH":
            continue
        qual = f.get(F_QUAL)
        dg = f.get(F_SUBJECT_DG)
        grp = f.get(F_SUBJECT_GROUP)
        try:
            n = int(float(r["values"][IND_ENTRIES]))
        except (KeyError, TypeError, ValueError):
            continue
        if n <= 0:
            continue
        key = (qual, dg, grp)
        e = agg.setdefault(key, {"entries": 0, "schools": 0, "by_school": {}})
        e["entries"] += n
        sch = r.get("locations", {}).get("SCH")
        if sch:
            e["by_school"][sch] = e["by_school"].get(sch, 0) + n

    out = []
    for (qual, dg, grp), e in agg.items():
        e["schools"] = len(e["by_school"])
        rec = {
            "qualification_id": qual,
            "qualification": QUALS.get(qual, qual),
            "subject_discount_group_id": dg,
            "subject_discount_group": labels.get(F_SUBJECT_DG, {}).get(dg, dg),
            "subject_group_id": grp,
            "subject_group": labels.get(F_SUBJECT_GROUP, {}).get(grp, grp),
            "entries": e["entries"],
            "schools_entering": e["schools"],
        }
        top = sorted(e["by_school"].items(), key=lambda kv: -kv[1])[:10]
        rec["top_schools"] = [
            {"name": schools.get(sid, {}).get("name", sid),
             "urn": schools.get(sid, {}).get("urn"),
             "entries": n}
            for sid, n in top
        ]
        rec["is_niche"] = e["entries"] <= NICHE_THRESHOLD
        out.append(rec)

    out.sort(key=lambda r: -r["entries"])

    payload = {
        "source": {
            "publication": "Key stage 4 performance, Academic year 2024/25",
            "dataset": "Subject school level exam data",
            "dataset_id": DATASET,
            "api": API,
            "url": "https://explore-education-statistics.service.gov.uk/find-statistics/key-stage-4-performance",
            "coverage": "England, school level (4,865 schools in the dataset)",
            "grade_filter": "Total exam entries (mgN9K)",
            "indicator": "Number of entries at grade (TEpPJ)",
            "qualifications": QUALS,
            "time_period": "2024/25",
        },
        "niche_threshold": NICHE_THRESHOLD,
        "rows": out,
    }
    path = os.path.join(HERE, "dfe_subject_entries_2025.json")
    json.dump(payload, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {path}: {len(out)} subject/qualification rows")

    print("\nTop 25 GCSE Full Course subjects by entries:")
    for r in [r for r in out if r["qualification_id"] in ("AHDJG", "V4Hh5")][:25]:
        print(f"  {r['entries']:>8,}  {r['schools_entering']:>5} schools  "
              f"{r['subject_discount_group']}  [{r['subject_group']}]")


if __name__ == "__main__":
    main()
