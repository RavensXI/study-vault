# -*- coding: utf-8 -*-
import sys, os, json, collections
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING","utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,".."))
from lib.supabase_client import get_client
sb = get_client()
SUB="641eba47-cb5b-4210-8c3e-29812629bbba"
units = sb.table("units").select("id,slug,name").eq("subject_id",SUB).execute().data
c = collections.Counter()
byunit = collections.defaultdict(collections.Counter)
for u in units:
    rows = sb.table("lessons").select("id,lesson_number,practice_questions").eq("unit_id",u["id"]).execute().data
    for r in rows:
        for q in (r.get("practice_questions") or []):
            t=q.get("type")
            c[t]+=1
            byunit[u["slug"]][t]+=1
print("ALL TYPE LABELS across english-literature-ocr:")
for t,n in c.most_common():
    print("  %5d  %s" % (n,t))
print()
print("unseen-poetry:", dict(byunit.get("unseen-poetry",{})))
for k in ["poetry-love-and-relationships","poetry-conflict","poetry-youth-and-age"]:
    print(k+":", dict(byunit.get(k,{})))
