"""Fetch the QA'd question bank for every lesson that has shorts, plus the lesson's
section headings (the <h2>s that shorts are keyed to). Output feeds the KC->section
tagging step. Deterministic, no LLM.
Writes scratchpad/_shorts_qbank.json = {lessons:[{lesson_id,subject,title,sections,kcs}]}.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from lib.supabase_client import get_client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "scripts", "_shorts_manifest.json")
OUT = os.path.join(ROOT, "scratchpad", "_shorts_qbank.json")

def sections_of(html):
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", html or "", re.S)
    return [re.sub("<[^>]+>", "", x).strip() for x in h2]

def main():
    sb = get_client()
    man = json.load(open(MAN, encoding="utf-8"))
    lesson_ids = list(dict.fromkeys(e["lesson_id"] for e in man))   # preserve order, dedupe
    topics_by_lesson = {}
    for e in man:
        topics_by_lesson.setdefault(e["lesson_id"], [])
        if e.get("topic") is not None:
            topics_by_lesson[e["lesson_id"]].append({"topic": e["topic"], "topic_index": e.get("topic_index")})

    lessons = []
    for lid in lesson_ids:
        row = sb.table("lessons").select(
            "id,title,lesson_number,knowledge_checks,content_html,units!inner(subjects!inner(slug))"
        ).eq("id", lid).execute().data
        if not row:
            print("MISSING lesson", lid); continue
        row = row[0]
        # mcq + fill both carry options[] + a correct index -> usable as tap-a-card checks
        kcs = [k for k in (row.get("knowledge_checks") or [])
               if isinstance(k.get("options"), list) and isinstance(k.get("correct"), int)]
        lessons.append({
            "lesson_id": lid,
            "subject": row["units"]["subjects"]["slug"],
            "title": row["title"],
            "lesson_number": row["lesson_number"],
            "sections": sections_of(row.get("content_html")),
            "kcs": [{"q": k["q"], "type": k.get("type"), "options": k["options"], "correct": k["correct"]} for k in kcs],
            "short_topics": topics_by_lesson.get(lid, []),
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"lessons": lessons}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot_kc = sum(len(l["kcs"]) for l in lessons)
    print(f"{len(lessons)} lessons, {tot_kc} MCQ knowledge-checks -> {OUT}")
    for l in lessons:
        print(f"  {l['subject']} L{l['lesson_number']:02d}: {len(l['sections'])} sections, {len(l['kcs'])} KCs, {len(l['short_topics'])} shorts")

if __name__ == "__main__":
    main()
