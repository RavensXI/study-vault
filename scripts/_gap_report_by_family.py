"""Generate per-family gap data for the BUILD_NOTES fan-out task.

For every subject family in the specs catalogue (except portfolio
families excluded from build-status), list:
  - all spec_codes offered
  - which we've built (free tier only)
  - which are unbuilt (the gap)
  - spec markdown file paths for each unbuilt spec (so agents can read them)
"""

import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, "scripts")
from lib.supabase_client import get_client


EXCLUDED_FAMILIES = {"art-and-design", "dance", "photography"}


def subject_family(name: str) -> str:
    if not name:
        return ""
    n = name.strip()
    n = re.sub(r":\s*(Trilogy|Synergy)\s*$", "", n, flags=re.IGNORECASE)
    n = re.sub(r"\s*\([^)]*\)\s*$", "", n)
    n = re.sub(r"\s+[AB]$", "", n)
    if re.match(r"^food and nutrition$", n, re.IGNORECASE):
        n = "Food Preparation and Nutrition"
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", n.lower()))


def spec_filename(board: str, slug: str, spec_code: str) -> str:
    """Find the markdown file for a spec."""
    folder = os.path.join("specs", board.lower())
    if not os.path.isdir(folder):
        return ""
    # Try common naming patterns
    candidates = [
        f"{slug}-{spec_code}.md",
        f"{slug}-{spec_code.lower()}.md",
        f"{slug}-{spec_code.upper()}.md",
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(folder, c)):
            return os.path.join(folder, c)
    # Fallback — any file containing the spec code
    for f in os.listdir(folder):
        if spec_code in f or spec_code.lower() in f.lower():
            return os.path.join(folder, f)
    return ""


def main():
    sb = get_client()
    subjects = sb.table("subjects").select(
        "slug, name, exam_board, spec_code, school_id, status"
    ).execute().data or []

    # Built spec_codes — free tier only, split slash-separated codes
    built_codes: set[str] = set()
    for s in subjects:
        if s.get("school_id"):
            continue
        sc = s.get("spec_code") or ""
        for code in str(sc).split("/"):
            code = code.strip()
            if code:
                built_codes.add(code)

    # Specs catalogue
    with open("specs/index.json", "r", encoding="utf-8") as f:
        specs = json.load(f)

    families: dict[str, dict] = defaultdict(lambda: {"name": "", "specs": []})
    for sp in specs:
        fam = subject_family(sp["subject"])
        if not fam or fam in EXCLUDED_FAMILIES:
            continue
        if not families[fam]["name"]:
            # Strip route suffixes from display name
            disp = re.sub(r":\s*(Trilogy|Synergy)\s*$", "", sp["subject"], flags=re.IGNORECASE)
            disp = re.sub(r"\s*\([^)]*\)\s*$", "", disp)
            disp = re.sub(r"\s+[AB]$", "", disp)
            families[fam]["name"] = disp
        families[fam]["specs"].append(sp)

    # Already covered in BUILD_NOTES (don't re-do)
    already_covered = {
        "combined-science", "biology", "chemistry", "physics",
        "french", "spanish", "german",
        "geography", "history", "physical-education",
        "religious-studies", "religious-education",
        "business-studies", "business",
        "citizenship-studies",
    }

    # Filter to families with at least one unbuilt spec, not already covered
    gaps: list[dict] = []
    for fam, entry in families.items():
        if fam in already_covered:
            continue
        unbuilt_specs = [sp for sp in entry["specs"] if sp["spec_code"] not in built_codes]
        if not unbuilt_specs:
            continue
        gaps.append({
            "family": fam,
            "name": entry["name"],
            "all_specs": entry["specs"],
            "unbuilt_specs": [
                {
                    "board": sp["board"],
                    "subject": sp["subject"],
                    "spec_code": sp["spec_code"],
                    "spec_file": spec_filename(sp["board"], sp.get("slug", ""), sp["spec_code"]),
                }
                for sp in unbuilt_specs
            ],
            "built_specs": [
                {
                    "board": sp["board"],
                    "subject": sp["subject"],
                    "spec_code": sp["spec_code"],
                }
                for sp in entry["specs"] if sp["spec_code"] in built_codes
            ],
        })

    gaps.sort(key=lambda x: x["family"])

    print(f"\n=== {len(gaps)} families with unbuilt specs (excluding already-covered) ===\n")
    for g in gaps:
        print(f"### {g['family']} ({g['name']})")
        print(f"  built ({len(g['built_specs'])}): " + ", ".join(
            f"{b['board']} {b['spec_code']}" for b in g["built_specs"]
        ) or "  (none built)")
        print(f"  unbuilt ({len(g['unbuilt_specs'])}):")
        for u in g["unbuilt_specs"]:
            print(f"    - {u['board']:12s} {u['spec_code']:14s} {u['subject']}  [{u['spec_file']}]")
        print()

    # Also dump JSON for the agents
    with open("scripts/_gap_report_by_family.json", "w", encoding="utf-8") as f:
        json.dump(gaps, f, indent=2)
    print(f"\nFull JSON saved to scripts/_gap_report_by_family.json")


if __name__ == "__main__":
    main()
