# -*- coding: utf-8 -*-
"""Remove dead related-media links from ONE rebuilt OCR poetry unit.

Reads a report from scripts/_audit_related_media_urls.py and drops only the
broken items whose unit_slug matches the cluster being rebuilt, so links in
units this build never touched are left alone. URLs listed in the optional
"rescued" file (403s that answer normally to a browser user agent) are kept.
Empty categories are removed; the Lesson Podcast placeholder is preserved.

Usage: python scripts/api_build/prune_media_ocr_cluster.py <unit_slug> <report.json>
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.join(r"C:\Users\tshau\Documents\Study Vault", "scripts"))

from lib.supabase_client import get_client


def main(unit_slug, report_path):
    report = json.load(io.open(report_path, encoding="utf-8"))
    rescued_path = report_path.replace(".json", "_rescued.json")
    rescued = set(json.load(io.open(rescued_path, encoding="utf-8"))) \
        if os.path.exists(rescued_path) else set()

    dead = {}
    for b in report["broken"]:
        if b["unit_slug"] != unit_slug or b["url"] in rescued:
            continue
        dead.setdefault(b["lesson_id"], set()).add(b["url"])
    print("lessons with dead links in %s: %d (%d urls)"
          % (unit_slug, len(dead), sum(len(v) for v in dead.values())))
    if rescued:
        print("kept %d rescued url(s): %s" % (len(rescued), ", ".join(sorted(rescued))[:160]))

    sb = get_client()
    removed = 0
    for lesson_id, urls in dead.items():
        row = sb.table("lessons").select("lesson_number,related_media") \
            .eq("id", lesson_id).single().execute().data
        rm = row["related_media"] or []
        out = []
        for cat in rm:
            items = [i for i in cat.get("items", []) if i.get("url") not in urls]
            removed += len(cat.get("items", [])) - len(items)
            if items:
                out.append({"category": cat["category"], "items": items})
        sb.table("lessons").update({"related_media": out}).eq("id", lesson_id).execute()
        print("  L%02d: %d categories, %d items remain"
              % (row["lesson_number"], len(out), sum(len(c["items"]) for c in out)))
    print("removed %d dead items" % removed)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
