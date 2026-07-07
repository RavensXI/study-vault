"""Build design-lab/_shorts_review.json for the shorts review page:
every banked short with its poster path, playable R2 url, lesson/unit/topic,
and the recall question it maps to (if any). Rerun after each batch/post-pass.
"""
import json, os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "scripts", "_shorts_manifest.json")
QS = os.path.join(ROOT, "scripts", "_shorts_questions.json")
OUT = os.path.join(ROOT, "design-lab", "_shorts_review.json")


def poster_rel(url):
    key = url.split(".r2.dev/", 1)[1]
    return "_posters/" + os.path.splitext(key)[0] + ".jpg"


def main():
    man = json.load(io.open(MAN, encoding="utf-8"))
    qs = json.load(io.open(QS, encoding="utf-8"))
    out = []
    for e in man:
        lid = e["lesson_id"]
        ti = e.get("topic_index")
        q = (qs.get(lid) or {}).get(str(ti)) if ti is not None else None
        out.append({
            "subject": e["subject"],
            "unit": e["unit"],
            "lesson_number": e["lesson_number"],
            "lesson_id": lid,
            "title": e["title"],
            "topic": e.get("topic"),
            "topic_index": ti,
            "url": e["url"],
            "poster": poster_rel(e["url"]),
            "created_at": e.get("created_at"),
            "q": q,   # {q, opts, correct, type} or None
        })
    # newest first within the file (so recent generations surface at the top of a subject)
    out.sort(key=lambda r: (r["subject"], r["unit"], r["lesson_number"], r["topic_index"] or 0))
    json.dump(out, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    subj = {}
    for r in out:
        subj[r["subject"]] = subj.get(r["subject"], 0) + 1
    print(f"{len(out)} shorts across {len(subj)} subjects -> {OUT}")
    print("history:", {k: v for k, v in subj.items() if k.startswith("history")})


if __name__ == "__main__":
    main()
