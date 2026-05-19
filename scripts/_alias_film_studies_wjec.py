"""Add WJEC as an alias of the existing Eduqas Film Studies row.

Per `feedback_eduqas_wjec_neutral_phrasing.md`: Film Studies content is
identical between Eduqas C670QS and WJEC 3670QS, so a single Supabase
row serves both boards via slugMap aliasing.

This script flips the exam_board and spec_code on `film-studies-eduqas`
to advertise both boards. No row duplication. No narration regen.
"""

import sys

sys.path.insert(0, "scripts")
from lib.supabase_client import get_client


def main():
    sb = get_client()

    before = sb.table("subjects").select(
        "id, slug, name, exam_board, spec_code"
    ).eq("slug", "film-studies-eduqas").execute().data

    if not before:
        print("ERROR: film-studies-eduqas not found in Supabase")
        sys.exit(1)

    row = before[0]
    print(f"BEFORE: exam_board={row['exam_board']!r} spec_code={row['spec_code']!r}")

    update = sb.table("subjects").update({
        "exam_board": "Eduqas / WJEC",
        "spec_code": "C670QS / 3670QS",
    }).eq("slug", "film-studies-eduqas").execute()

    after = sb.table("subjects").select(
        "id, slug, name, exam_board, spec_code"
    ).eq("slug", "film-studies-eduqas").execute().data[0]
    print(f"AFTER:  exam_board={after['exam_board']!r} spec_code={after['spec_code']!r}")


if __name__ == "__main__":
    main()
