# -*- coding: utf-8 -*-
"""Back up the four music-ocr aos3-rhythms-listening rows before any write."""
import io, json, os, sys
sys.path.insert(0, r"C:\Users\tshau\Documents\Study Vault\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJ, UNIT = "music-ocr", "aos3-rhythms-listening"
sb = get_client()
s = sb.table("subjects").select("id,slug,school_id,name").eq("slug", SUBJ).is_("school_id", "null").execute().data[0]
u = sb.table("units").select("id,slug,name").eq("subject_id", s["id"]).eq("slug", UNIT).execute().data[0]
out = []
for n in (1, 2, 3, 4):
    l = sb.table("lessons").select("*").eq("unit_id", u["id"]).eq("lesson_number", n).single().execute().data
    fn = os.path.join(HERE, "backups", "%s__%s__L%02d.json" % (SUBJ, UNIT, n))
    io.open(fn, "w", encoding="utf-8").write(json.dumps(l, indent=1, ensure_ascii=False, default=str))
    out.append({"subject": SUBJ, "unit": UNIT, "lesson": n, "id": l["id"], "title": l["title"],
                "status": l["status"], "yt": l["youtube_video_id"], "is_listening": l.get("is_listening"),
                "hero": l.get("hero_image_url"), "rm": len(l.get("related_media") or []),
                "chars": len(l["content_html"] or ""), "pd": bool(l.get("practice_data")),
                "file": os.path.basename(fn)})
    print("L%d %-16s pd=%-5s hero=%-5s rm=%-2d chars=%-6d %s" % (n, l["status"], bool(l.get("practice_data")),
          bool(l.get("hero_image_url")), len(l.get("related_media") or []), len(l["content_html"] or ""), l["title"][:60]))
io.open(os.path.join(HERE, "_rows_index_ocr.json"), "w", encoding="utf-8").write(json.dumps(out, indent=1, ensure_ascii=False))
print("unit:", u["name"], "| subject:", s["name"])
