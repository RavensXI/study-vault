# -*- coding: utf-8 -*-
"""Publish (or unpublish) the two new Geography Skills lessons.

    python scratchpad/_geo_guided/_publish_l13_l14.py --status      # where things stand
    python scratchpad/_geo_guided/_publish_l13_l14.py --publish     # go live on all six variants
    python scratchpad/_geo_guided/_publish_l13_l14.py --unpublish   # back to pending_review

L13 and L14 are created at status 'pending_review': practice-loader renders
those for admin/teacher with a preview banner and blocks them for students, so
they can be reviewed without reaching anyone.

Publishing flips status AND sets units.lesson_count to the live count. Those two
have to move together: browse-loader lists only live lessons but takes its
"0 of N" label from lesson_count, so a mismatch shows 12 cards under a heading
that says 14.
"""
import json, os, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
SUBJECTS = ["geography-aqa", "geography-edexcel-a", "geography-edexcel-b",
            "geography-ocr", "geography-eduqas", "geography"]
NEW_SLUGS = ["contours-and-relief", "map-interpretation"]

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


def run(mode):
    target = {"publish": "live", "unpublish": "pending_review"}.get(mode)
    for slug in SUBJECTS:
        subj = req(B + "subjects?slug=eq.%s&select=id" % slug)
        if not subj:
            continue
        units = req(B + "units?subject_id=eq.%s&select=id,slug,lesson_count" % subj[0]["id"])
        unit = next((u for u in units if u["slug"] == "geographical-skills"), None)
        if not unit:
            continue
        lessons = req(B + "lessons?unit_id=eq.%s&select=id,lesson_number,slug,status" % unit["id"])
        mine = [l for l in lessons if l["slug"] in NEW_SLUGS]

        if target:
            for l in mine:
                req(B + "lessons?id=eq.%s" % l["id"], method="PATCH",
                    body={"status": target}, extra={"Prefer": "return=minimal"})
            lessons = req(B + "lessons?unit_id=eq.%s&select=lesson_number,status" % unit["id"])
            live = sum(1 for l in lessons if l["status"] == "live")
            req(B + "units?id=eq.%s" % unit["id"], method="PATCH",
                body={"lesson_count": live}, extra={"Prefer": "return=minimal"})
            unit["lesson_count"] = live

        live = sum(1 for l in lessons if l.get("status") == "live")
        states = ", ".join("L%d=%s" % (l["lesson_number"], l["status"]) for l in sorted(mine, key=lambda x: x["lesson_number"]))
        print("%-22s live=%-3d lesson_count=%-3s  %s" % (slug, live, unit.get("lesson_count"), states))


if __name__ == "__main__":
    if "--publish" in sys.argv:
        run("publish")
    elif "--unpublish" in sys.argv:
        run("unpublish")
    elif "--status" in sys.argv:
        run(None)
    else:
        sys.exit(__doc__)
