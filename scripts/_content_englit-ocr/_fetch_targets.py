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
OUT = os.path.join(HERE,"_target"); os.makedirs(OUT, exist_ok=True)
UNIT="d15cce20-ab7f-4b4b-849f-53fd6595785d"
rows = sb.table("lessons").select("*").eq("unit_id",UNIT).execute().data
rows.sort(key=lambda r:r["lesson_number"])
for r in rows:
    p=os.path.join(OUT,"L%02d.json"%r["lesson_number"])
    json.dump(r,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("L%d %-52s %s  status=%s"%(r["lesson_number"],r["title"],r["id"],r.get("status")))
