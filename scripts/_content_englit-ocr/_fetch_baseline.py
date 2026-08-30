# -*- coding: utf-8 -*-
import sys, os, json
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lib.supabase_client import get_client
sb = get_client()
OUT = os.path.join(HERE, "_baseline")
os.makedirs(OUT, exist_ok=True)
TARGETS = [
    ("aqa-unseen",  "00e90d53-67ee-4074-be96-2f4f7fb9ea0f", [1,3]),
    ("ocr-greatexp","a01a4436-14a8-4fbf-ae63-3794f23ef6b4", [1]),
    ("eduqas-anth", "f3f94f98-08b9-48c7-bc8b-2d41645c29a9", [1]),
]
for tag, uid, nums in TARGETS:
    rows = sb.table("lessons").select("*").eq("unit_id", uid).in_("lesson_number", nums).execute().data
    for r in rows:
        p = os.path.join(OUT, "%s_L%d.json" % (tag, r["lesson_number"]))
        json.dump(r, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", p, "title=", r["title"], "status=", r.get("status"))
