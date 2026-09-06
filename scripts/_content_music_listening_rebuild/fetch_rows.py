# -*- coding: utf-8 -*-
"""Fetch every lesson in the listening queue (plus the approved exemplar L2)
and write one backup JSON per lesson under backups/."""
import io, json, os, sys
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\88006801-843c-4d74-957a-5eebdef537b9\scratchpad"
queue = json.load(io.open(os.path.join(SCRATCH, "listening_queue.json"), encoding="utf-8"))
# add the approved exemplar so L3 can complement it
queue = [{"subject": "music-edexcel", "unit": "aos1-instrumental-music", "lesson": 2}] + queue

sb = get_client()
subj_cache, unit_cache = {}, {}
out = []
for row in queue:
    s, u, n = row["subject"], row["unit"], row["lesson"]
    if s not in subj_cache:
        r = sb.table("subjects").select("id,slug,school_id,name").eq("slug", s).is_("school_id", "null").execute().data
        subj_cache[s] = r[0]
    sid = subj_cache[s]["id"]
    key = (sid, u)
    if key not in unit_cache:
        unit_cache[key] = sb.table("units").select("id,slug").eq("subject_id", sid).eq("slug", u).execute().data[0]
    uid = unit_cache[key]["id"]
    l = sb.table("lessons").select("*").eq("unit_id", uid).eq("lesson_number", n).single().execute().data
    fn = os.path.join(HERE, "backups", f"{s}__{u}__L{n:02d}.json")
    io.open(fn, "w", encoding="utf-8").write(json.dumps(l, indent=1, ensure_ascii=False, default=str))
    out.append({"subject": s, "unit": u, "lesson": n, "id": l["id"], "title": l["title"],
                "status": l["status"], "yt": l["youtube_video_id"], "is_listening": l.get("is_listening"),
                "chars": len(l["content_html"] or ""), "file": os.path.basename(fn)})
    print(f"{s}/{u}/L{n:02d}  {l['status']:16s} {len(l['content_html'] or ''):6d}  {l['title'][:60]}")
io.open(os.path.join(HERE, "_rows_index.json"), "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
print("backed up", len(out))
