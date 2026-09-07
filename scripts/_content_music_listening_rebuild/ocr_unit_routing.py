# -*- coding: utf-8 -*-
"""The four aos3-rhythms-listening lessons stop being practice rows, so the
unit has to stop being a practice unit.

browse-loader.js decides the lesson URL prefix from
subjects.settings.practice_units (line 806): a unit listed there links to
/practice/..., and practice-loader.js then finds practice_data null and has
nothing to render. Removing the slug is what makes the rebuilt article
lessons reachable from the unit page.

Backs the whole settings object up to backups/ before writing.
Usage: python ocr_unit_routing.py [--apply]
"""
import io, json, os, sys
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ, UNIT = "music-ocr", "aos3-rhythms-listening"
sb = get_client()
s = sb.table("subjects").select("id,slug,settings").eq("slug", SUBJ).is_("school_id", "null").execute().data[0]
settings = s["settings"] or {}
io.open(os.path.join(HERE, "backups", "%s__subject_settings.json" % SUBJ), "w", encoding="utf-8").write(
    json.dumps(settings, indent=1, ensure_ascii=False))

pu = list(settings.get("practice_units") or [])
print("before:", pu)
if UNIT not in pu:
    print("already removed; nothing to do")
    raise SystemExit(0)
new = [u for u in pu if u != UNIT]
print("after: ", new)
if "--apply" not in sys.argv:
    print("dry run")
    raise SystemExit(0)
settings["practice_units"] = new
sb.table("subjects").update({"settings": settings}).eq("id", s["id"]).execute()
chk = sb.table("subjects").select("settings").eq("id", s["id"]).single().execute().data
print("written:", chk["settings"].get("practice_units"))
