"""Add Eduqas as an alias of the existing WJEC Hospitality & Catering row.

Eduqas 5409QA and WJEC 5409QA are the SAME WJEC CBAC document
(dual-branded — Eduqas is WJEC's England label). Existing free-tier
row is exam_board='WJEC', spec_code='5409'. Flip to dual-board labelling.
"""

import sys
sys.path.insert(0, "scripts")
from lib.supabase_client import get_client


def main():
    sb = get_client()
    before = sb.table("subjects").select(
        "id, slug, name, exam_board, spec_code"
    ).eq("slug", "hospitality-catering").execute().data
    if not before:
        print("ERROR: hospitality-catering not found")
        sys.exit(1)

    row = before[0]
    print(f"BEFORE: exam_board={row['exam_board']!r} spec_code={row['spec_code']!r}")

    sb.table("subjects").update({
        "exam_board": "Eduqas / WJEC",
        "spec_code": "5409QA / 5409QA",
    }).eq("slug", "hospitality-catering").execute()

    after = sb.table("subjects").select(
        "id, slug, name, exam_board, spec_code"
    ).eq("slug", "hospitality-catering").execute().data[0]
    print(f"AFTER:  exam_board={after['exam_board']!r} spec_code={after['spec_code']!r}")


if __name__ == "__main__":
    main()
