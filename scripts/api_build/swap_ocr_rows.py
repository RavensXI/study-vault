# -*- coding: utf-8 -*-
"""Replace the eight wrong lessons in an OCR poetry-cluster unit with fifteen
per-poem skeletons, keeping the unit row (id and slug) untouched.

Backs the old rows up to scripts/_content_englit-ocr/_rebuild_backup_<cluster>.json
BEFORE deleting anything, and refuses to run if the backup cannot be written.

Usage: python scripts/api_build/swap_ocr_rows.py conflict
"""
import io
import json
import os
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = r"C:\Users\tshau\Documents\Study Vault"
URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BACKUP_DIR = os.path.join(REPO, "scripts", "_content_englit-ocr")


def req(method, path, body=None):
    headers = {"apikey": KEY, "Authorization": "Bearer " + KEY,
               "Content-Type": "application/json", "Prefer": "return=representation"}
    r = urllib.request.Request(URL + "/rest/v1/" + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               headers=headers, method=method)
    try:
        raw = urllib.request.urlopen(r).read().decode()
        return json.loads(raw) if raw.strip() else None
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:500])
        raise


def main(cluster):
    cfg = json.load(io.open(os.path.join(REPO, "scripts", "api_build",
                                         "config_englit-ocr-%s.json" % cluster), encoding="utf-8"))
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))
    unit = plan["article_units"][0]
    subject_id = json.load(io.open(os.path.join(cfg["run_dir"], "state.json"),
                                   encoding="utf-8"))["subject_id"]

    units = req("GET", "units?subject_id=eq.%s&slug=eq.%s&select=id,slug,name,lesson_count"
                % (subject_id, unit["slug"]))
    if len(units) != 1:
        raise SystemExit("expected exactly one unit row, got %d" % len(units))
    uid = units[0]["id"]
    print("unit:", units[0]["slug"], uid, "lesson_count", units[0]["lesson_count"])

    old = req("GET", "lessons?unit_id=eq.%s&select=*&order=lesson_number" % uid)
    print("existing lessons:", len(old))
    os.makedirs(BACKUP_DIR, exist_ok=True)
    bpath = os.path.join(BACKUP_DIR, "_rebuild_backup_%s.json" % cluster)
    io.open(bpath, "w", encoding="utf-8").write(
        json.dumps({"unit": units[0], "lessons": old}, ensure_ascii=False, indent=1))
    if os.path.getsize(bpath) < 1000:
        raise SystemExit("backup looks empty — refusing to delete")
    print("backed up %d rows to %s (%d bytes)" % (len(old), bpath, os.path.getsize(bpath)))

    gone = req("DELETE", "lessons?unit_id=eq.%s" % uid)
    print("deleted:", len(gone or []))

    rows = [{"unit_id": uid, "lesson_number": l["number"],
             "slug": "lesson-%02d" % l["number"], "title": l["title"],
             "description": l["description"], "status": "pending_review", "tier": "both"}
            for l in unit["lessons"]]
    ins = req("POST", "lessons", rows)
    print("inserted skeletons:", len(ins))

    req("PATCH", "units?id=eq." + uid,
        {"lesson_count": len(rows), "subtitle": unit["subtitle"]})
    print("unit updated: lesson_count=%d, subtitle=%r" % (len(rows), unit["subtitle"]))


if __name__ == "__main__":
    main(sys.argv[1])
