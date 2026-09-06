# -*- coding: utf-8 -*-
"""Dump a backed-up lesson as readable text: title, description, content prose,
exam tip, conclusion, questions, KCs, flashcards, media.
Usage: python show.py <backup-file-stem> [--full]"""
import io, json, os, re, sys, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
stem = sys.argv[1]
p = os.path.join(HERE, "backups", stem + ".json")
d = json.load(io.open(p, encoding="utf-8"))
print("TITLE:", d["title"])
print("SLUG:", d["slug"], "| status:", d["status"], "| yt:", d["youtube_video_id"], "| is_listening:", d.get("is_listening"))
print("DESC:", d["description"])
print("HERO:", d["hero_image_url"], "|", d["hero_image_alt"], "|", d["hero_image_caption"])
c = d["content_html"] or ""
if "--full" in sys.argv:
    print("\n===== RAW CONTENT =====\n", c)
else:
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", c, flags=re.S)
    t = re.sub(r"<h2[^>]*>", "\n\n## ", t)
    t = re.sub(r"<h3[^>]*>", "\n\n### ", t)
    t = re.sub(r"<li[^>]*>", "\n - ", t)
    t = re.sub(r"</p>|</div>|</section>", "\n", t)
    t = re.sub(r"<dfn[^>]*data-def=\"([^\"]*)\"[^>]*>([^<]*)</dfn>", r"\2 [def: \1]", t)
    t = re.sub(r"<iframe[^>]*src=\"([^\"]*)\"[^>]*>", r"\n[IFRAME \1]\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    print("\n===== CONTENT =====")
    print(t.strip())
print("\n===== EXAM TIP =====\n", html.unescape(re.sub(r"<[^>]+>", "", d["exam_tip_html"] or "")))
print("\n===== CONCLUSION =====\n", html.unescape(re.sub(r"<[^>]+>", "", d["conclusion_html"] or "")))
print("\n===== PRACTICE =====")
for q in d["practice_questions"] or []:
    print(json.dumps(q, ensure_ascii=False))
print("\n===== KC =====")
for q in d["knowledge_checks"] or []:
    print(json.dumps(q, ensure_ascii=False))
print("\n===== FLASHCARDS =====")
for q in d["flashcard_questions"] or []:
    print(json.dumps(q, ensure_ascii=False))
print("\n===== RELATED MEDIA =====")
print(json.dumps(d["related_media"], ensure_ascii=False, indent=1)[:2000])
print("\n===== GLOSSARY =====")
print(json.dumps(d["glossary_terms"], ensure_ascii=False)[:1500])
