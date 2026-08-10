"""Annual Ofqual-register check for GCSE availability.

The Ofqual Register of Regulated Qualifications is the legal source of truth
for what can be awarded in England. This script:

  1. Pulls every GCSE entry from the public register API
     (https://register-api.ofqual.gov.uk/api/Qualifications).
  2. Diffs against the previous snapshot (scripts/_ofqual_gcse_register.json):
     newly available, status changes, new/changed operational end dates.
  3. Cross-checks currently-available England-board GCSEs against our spec
     catalogue (specs/index.json) and reports any qualification we don't hold.
  4. Writes the new snapshot (previous kept as _ofqual_gcse_register_prev.json).

Run once a year before the spec-currency audit (docs/SPEC_CURRENCY_AUDIT_*.md).
The register answers WITHDRAWAL authoritatively and for free; the paid Opus
audit is then only needed for spec-content amendments and edge cases.

Limits: England only (Ofqual). Wales Made-for-Wales quals live on the
Qualifications Wales register (https://www.qiw.wales) and need their own check.
CCEA rows are Northern Ireland; reported for awareness, not catalogue-checked.

Usage:  python scripts/_ofqual_register_check.py
"""
import json
import re
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
SNAPSHOT = SCRIPT_DIR / "_ofqual_gcse_register.json"
PREV = SCRIPT_DIR / "_ofqual_gcse_register_prev.json"
SPEC_INDEX = SCRIPT_DIR.parent / "specs" / "index.json"

API = "https://register-api.ofqual.gov.uk/api/Qualifications?title=GCSE&page={page}&limit=100"
KEEP_FIELDS = [
    "qualificationNumber", "title", "status", "organisationAcronym", "type",
    "operationalStartDate", "operationalEndDate", "certificationEndDate",
    "linkToSpecification", "lastUpdatedDate",
]
ORG_TO_BOARD = {"AQA": "AQA", "Pearson": "Edexcel", "Cambridge OCR": "OCR",
                "WJEC": "Eduqas", "CCEA": "CCEA"}


def fetch_register():
    rows, page = [], 1
    while True:
        url = API.format(page=page)
        req = urllib.request.Request(url, headers={"User-Agent": "StudyVault-spec-check"})
        data = json.load(urllib.request.urlopen(req))
        rows += data["results"]
        if page * 100 >= data["count"]:
            break
        page += 1
        time.sleep(0.3)
    gcse = [r for r in rows if (r.get("type") or "").startswith("GCSE")]
    return [{k: r.get(k) for k in KEEP_FIELDS} for r in gcse]


def subject_of(title):
    m = re.search(r"GCSE(?:\s*\([^)]*\))?(?:\s*\([^)]*\))?\s+in\s+(.*)$", title, re.I)
    return (m.group(1) if m else title).strip()


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    stop = {"gcse", "in", "the", "of", "and", "a", "b", "studies", "short", "course", "9", "1"}
    return frozenset(w for w in s.split() if w and w not in stop)


def catalogue_crosscheck(available):
    idx = json.load(open(SPEC_INDEX, encoding="utf-8"))
    cat = defaultdict(list)
    for e in idx:
        cat[e["board"]].append((norm(e["subject"]), e))
    missing = []
    for r in available:
        board = ORG_TO_BOARD.get(r["organisationAcronym"], r["organisationAcronym"])
        if board == "CCEA":
            continue
        ns = norm(subject_of(r["title"]))
        pool = cat.get(board, []) + (cat.get("WJEC", []) if board == "Eduqas" else [])
        if not any(cn and (cn <= ns or ns <= cn or len(cn & ns) / max(1, len(cn | ns)) >= 0.6)
                   for cn, _ in pool):
            missing.append((board, r))
    return missing


def main():
    old = {}
    if SNAPSHOT.exists():
        old = {r["qualificationNumber"]: r for r in json.load(open(SNAPSHOT, encoding="utf-8"))}
    new_rows = fetch_register()
    new = {r["qualificationNumber"]: r for r in new_rows}
    print(f"register GCSE entries: {len(new)} (previous snapshot: {len(old) or 'none'})")

    available = [r for r in new_rows if r["status"] == "Available to learners"]
    by_org = defaultdict(int)
    for r in available:
        by_org[ORG_TO_BOARD.get(r["organisationAcronym"], r["organisationAcronym"])] += 1
    print("available to learners:", len(available), dict(by_org))

    if old:
        print("\n=== CHANGES SINCE LAST SNAPSHOT ===")
        changes = 0
        for qn, r in new.items():
            o = old.get(qn)
            if o is None:
                print(f"  NEW ENTRY | {r['title']} | {r['status']} | QN {qn}")
                changes += 1
            elif o["status"] != r["status"]:
                print(f"  STATUS    | {r['title']} | {o['status']} -> {r['status']} | QN {qn}")
                changes += 1
            elif (o.get("operationalEndDate") or "") != (r.get("operationalEndDate") or ""):
                print(f"  END DATE  | {r['title']} | {(o.get('operationalEndDate') or 'none')[:10]}"
                      f" -> {(r.get('operationalEndDate') or 'none')[:10]} | QN {qn}")
                changes += 1
        for qn, o in old.items():
            if qn not in new:
                print(f"  REMOVED   | {o['title']} | QN {qn}")
                changes += 1
        if not changes:
            print("  none")

    print("\n=== AVAILABLE ON REGISTER, MISSING FROM specs/index.json ===")
    missing = catalogue_crosscheck(available)
    for board, r in sorted(missing, key=lambda x: (x[0], x[1]["title"])):
        print(f"  {board:8} | {r['title']} | QN {r['qualificationNumber']}")
    if not missing:
        print("  none — catalogue covers every live England GCSE")

    print("\n=== SUNSET / UPCOMING ===")
    flagged = [r for r in new_rows
               if r["status"] in ("No longer available to new learners", "Not yet available to learners")]
    for r in flagged:
        print(f"  {r['status']:38} | {r['title']} | op-end: {(r.get('operationalEndDate') or '')[:10]}")
    if not flagged:
        print("  none")

    if SNAPSHOT.exists():
        PREV.write_text(SNAPSHOT.read_text(encoding="utf-8"), encoding="utf-8")
    json.dump(new_rows, open(SNAPSHOT, "w", encoding="utf-8"), indent=1)
    print(f"\nsnapshot written: {SNAPSHOT.name} ({len(new_rows)} rows)")


if __name__ == "__main__":
    main()
