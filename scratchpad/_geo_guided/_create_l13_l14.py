# -*- coding: utf-8 -*-
"""Create the two missing Geography Skills lessons as skeleton rows.

    python scratchpad/_geo_guided/_create_l13_l14.py --check
    python scratchpad/_geo_guided/_create_l13_l14.py --apply

L13 Contours & Relief and L14 Map Interpretation have never existed; the
section stops at L12. Rows are created at status 'pending_review', which
practice-loader shows to admin/teacher with a preview banner and blocks for
students, so nothing reaches production until Tom flips them.

Row creation stays here rather than in the authoring agents: agents fetch and
PATCH practice_data on one known row and nothing else.
"""
import io, json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
SUBJECTS = ["geography-aqa", "geography-edexcel-a", "geography-edexcel-b",
            "geography-ocr", "geography-eduqas", "geography"]
NEW = [
    {"n": 13, "slug": "contours-and-relief", "title": "Contours & Relief",
     "description": "Read contour lines to judge height, gradient and landform shape on an OS map."},
    {"n": 14, "slug": "map-interpretation", "title": "Map Interpretation",
     "description": "Combine symbols, relief and settlement evidence to describe and explain a landscape."},
]

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def main(apply_it):
    created, existing = [], []
    for slug in SUBJECTS:
        subj = req(B + "subjects?slug=eq.%s&select=id" % slug)
        if not subj:
            print("  !! subject not found:", slug)
            continue
        units = req(B + "units?subject_id=eq.%s&select=id,slug,lesson_count" % subj[0]["id"])
        unit = next((u for u in units if u["slug"] == "geographical-skills"), None)
        if not unit:
            print("  !! no geographical-skills unit on", slug)
            continue
        have = req(B + "lessons?unit_id=eq.%s&select=lesson_number,slug" % unit["id"])
        have_nums = {l["lesson_number"] for l in have}
        for spec in NEW:
            if spec["n"] in have_nums:
                existing.append("%s L%d" % (slug, spec["n"]))
                continue
            row = {
                "unit_id": unit["id"],
                "lesson_number": spec["n"],
                "slug": spec["slug"],
                "title": spec["title"],
                "description": spec["description"],
                "status": "pending_review",
                "tier": "both",
                "youtube_video_id": "practice-only",
                "practice_data": {},
            }
            if apply_it:
                out = req(B + "lessons", method="POST", body=row,
                          extra={"Prefer": "return=representation"})
                created.append("%s L%d -> %s" % (slug, spec["n"], out[0]["id"]))
            else:
                created.append("%s L%d (would create)" % (slug, spec["n"]))

    print("to create: %d   already present: %d" % (len(created), len(existing)))
    for c in created:
        print("   ", c)
    for e in existing:
        print("    exists:", e)

    if apply_it:
        # keep the unit counts honest
        for slug in SUBJECTS:
            subj = req(B + "subjects?slug=eq.%s&select=id" % slug)
            if not subj:
                continue
            units = req(B + "units?subject_id=eq.%s&select=id,slug" % subj[0]["id"])
            unit = next((u for u in units if u["slug"] == "geographical-skills"), None)
            if not unit:
                continue
            n = len(req(B + "lessons?unit_id=eq.%s&select=lesson_number" % unit["id"]))
            req(B + "units?id=eq.%s" % unit["id"], method="PATCH",
                body={"lesson_count": n}, extra={"Prefer": "return=minimal"})
        print("unit lesson_count refreshed on all six variants")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        main(True)
    elif "--check" in sys.argv:
        main(False)
    else:
        sys.exit(__doc__)
