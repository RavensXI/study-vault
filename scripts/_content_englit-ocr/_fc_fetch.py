# -*- coding: utf-8 -*-
import sys, os, json
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING","utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,".."))
from lib.supabase_client import get_client
sb = get_client()
OUT = os.path.join(HERE,"_fc"); os.makedirs(OUT, exist_ok=True)

subs = sb.table("subjects").select("id,name,slug,exam_board,school_id,settings").eq("slug","english-literature-ocr").execute().data
for s in subs:
    print("SUBJECT", s["id"], s["slug"], s["exam_board"], "school_id=", s["school_id"])
sub = [s for s in subs if s["school_id"] is None][0]
units = sb.table("units").select("id,slug,name,sort_order").eq("subject_id",sub["id"]).order("sort_order").execute().data
for u in units:
    print("UNIT", u["id"], u["slug"], "|", u["name"])
unit = [u for u in units if u["slug"]=="unseen-poetry"]
if not unit:
    print("NO unseen-poetry unit; slugs above")
    sys.exit(1)
unit = unit[0]
rows = sb.table("lessons").select("*").eq("unit_id",unit["id"]).execute().data
rows.sort(key=lambda r:r["lesson_number"])
for r in rows:
    p=os.path.join(OUT,"L%02d.json"%r["lesson_number"])
    json.dump(r,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("L%d %-58s %s status=%s"%(r["lesson_number"],r["title"],r["id"],r.get("status")))
json.dump({"subject":sub,"unit":unit},open(os.path.join(OUT,"_meta.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
