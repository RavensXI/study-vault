"""Verify the Boys Don't Cry name swap and the two AO/garbling fixes."""
import json
import os
import re
import sys

os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client  # noqa: E402
from lib.narration import extract_narration_chunks  # noqa: E402

sb = get_client()
BDC_UNIT = "8716371d-c1e1-4393-85c7-92cd52dc470a"
FIELDS = ["title", "description", "content_html", "conclusion_html", "exam_tip_html",
          "practice_questions", "knowledge_checks", "flashcard_questions",
          "glossary_terms", "related_media", "hero_image_alt", "hero_image_caption"]
PLAIN = ["description", "practice_questions", "knowledge_checks",
         "flashcard_questions", "glossary_terms", "title", "hero_image_alt"]
ENTITY = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5}|#x[0-9a-fA-F]{2,5});")

fails = []
rows = sb.table("lessons").select("*").eq("unit_id", BDC_UNIT).order("lesson_number").execute().data
print("=" * 78)
print("BOYS DON'T CRY — post-fix occurrence map")
for r in rows:
    n = r["lesson_number"]
    blob = {}
    for f in FIELDS:
        v = r.get(f)
        if v is None:
            continue
        blob[f] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    joined = "\n".join(blob.values())
    counts = {k: len(re.findall(r"\b%s\b" % k, joined)) for k in ("Emma", "Melanie", "Mel", "Bryce")}
    print(f"  L{n}: {counts}")
    if counts["Bryce"]:
        fails.append(f"L{n}: residual 'Bryce'")

    # Relationship assertions
    for f, s in blob.items():
        for m in re.finditer(r"\bMel(?!anie)\b", s):
            ctx = s[max(0, m.start() - 90):m.end() + 90].replace("\n", " ")
            if "known as Mel" not in ctx:
                fails.append(f"L{n} {f}: bare 'Mel' outside the gloss → …{ctx}…")
        for pat, why in [
            (r"Emma,? (?:is |was )?(?:Dante[’']s )?ex-girlfriend", "Emma cast as the ex-girlfriend"),
            (r"ex-girlfriend[^.]{0,12}\bEmma\b(?!['’]s mother)", "Emma cast as the ex-girlfriend"),
            (r"baby[^.]{0,20}Melanie", "Melanie cast as the baby"),
            (r"Melanie is (?:his|Dante[’']s) daughter", "Melanie cast as the daughter"),
            (r"Melanie[’']s mother", "Melanie given a mother — direction reversed"),
            (r"Melanie is approximately ten months", "Melanie cast as the baby"),
            (r"Melanie arrives in a pushchair", "Melanie cast as the baby"),
            (r"(?:care for|caring for|attachment to|bond with) Melanie", "Melanie cast as the baby"),
            (r"Emma (?:abandons|leaves Dante|does not announce|exits his life|chose to leave)",
             "Emma cast as the departing mother"),
            (r"Emma[’']s (?:abandonment|text message|refusal|absence|deceptive)",
             "Emma cast as the departing mother"),
        ]:
            for m in re.finditer(pat, s):
                fails.append(f"L{n} {f}: {why} → {s[max(0,m.start()-70):m.end()+70]!r}")

    # Entities in plain-text fields
    for f in PLAIN:
        if f in blob and ENTITY.search(blob[f]):
            fails.append(f"L{n} {f}: HTML entity in a plain-text field: "
                         f"{ENTITY.findall(blob[f])[:5]}")

# Explicit relationship spot-checks
print()
l6 = [r for r in rows if r["lesson_number"] == 6][0]
i = l6["content_html"].find('data-narration-id="n27"')
sent = l6["content_html"][i:i + 200]
print("L6 corrected sentence:")
print("  " + re.sub(r"<[^>]+>", "", sent).split("She appears")[0].strip())

MUST = [
    (2, "content_html", "At the door is Melanie, known as Mel — Dante's ex-girlfriend"),
    (2, "content_html", "The baby — named Emma — is approximately ten months old"),
    (2, "content_html", "Melanie tells Dante that Emma is his daughter"),
    (2, "content_html", "Emma's arrival in a pushchair signals she is an older baby"),
    (2, "description", "baby Emma's arrival"),
    (6, "content_html", "Melanie, known as Mel, is Dante's ex-girlfriend and Emma's mother."),
    (6, "content_html", '<h2 data-narration-id="n26">Melanie</h2>'),
]
for n, f, needle in MUST:
    r = [x for x in rows if x["lesson_number"] == n][0]
    s = r[f] if isinstance(r[f], str) else json.dumps(r[f], ensure_ascii=False)
    ok = needle in s
    print(f"  [{'OK ' if ok else 'FAIL'}] L{n} {f}: {needle[:64]}")
    if not ok:
        fails.append(f"L{n} {f}: missing {needle!r}")

# KC / practice answer sanity on the touched questions
print("\nKC answer checks (touched questions):")
for r in rows:
    for kc in (r.get("knowledge_checks") or []):
        q = kc.get("q", "")
        if not re.search(r"\b(Emma|Melanie)\b", q + json.dumps(kc.get("options") or [], ensure_ascii=False)
                         + json.dumps(kc.get("right") or [], ensure_ascii=False)):
            continue
        if kc.get("type") == "match":
            print(f"  L{r['lesson_number']} match: left={kc['left']} order={kc['order']}")
            for li, oi in enumerate(kc["order"]):
                print(f"      {kc['left'][li]}  ->  {kc['right'][oi]}")
        else:
            c = kc.get("correct")
            opts = kc.get("options") or []
            print(f"  L{r['lesson_number']} {kc.get('type')}: {q}")
            print(f"      answer = {opts[c] if isinstance(c, int) and c < len(opts) else c!r}")

# ── Curious Incident + A Christmas Carol ───────────────────────────────
print("\n" + "=" * 78)
for slug, unit, num in [("english-literature-eduqas", "the-curious-incident", 8),
                        ("english-literature-ocr", "a-christmas-carol", 7)]:
    sid = sb.table("subjects").select("id").eq("slug", slug).execute().data[0]["id"]
    uid = sb.table("units").select("id").eq("subject_id", sid).eq("slug", unit).execute().data[0]["id"]
    r = sb.table("lessons").select("*").eq("unit_id", uid).eq("lesson_number", num).execute().data[0]
    blob = {}
    for f in FIELDS:
        v = r.get(f)
        if v is None:
            continue
        blob[f] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    print(f"{slug}/{unit} L{num}")
    if unit == "the-curious-incident":
        for f, s in blob.items():
            for m in re.finditer(r"AO4[^.]{0,80}", s):
                print(f"  [{f}] {m.group(0)[:110]}")
            for pat in (r"AO4 \(context\)", r"AO4 context", r"For AO4, include context",
                        r"relevant for AO4", r"AO4 should reference", r"embed AO4",
                        r"AO4:", r"Example AO4 sentence", r"analysis with AO4"):
                for m in re.finditer(pat, s):
                    fails.append(f"CI L8 {f}: AO4 still tied to context → "
                                 f"{s[max(0,m.start()-60):m.end()+60]!r}")
        gl = {g["term"]: g["definition"] for g in (r.get("glossary_terms") or [])}
        print("  glossary AO4:", gl.get("AO4", "(missing)")[:200])
        if "vocabulary and sentence structures" not in gl.get("AO4", ""):
            fails.append("CI L8: glossary AO4 not corrected")
    else:
        i = r["content_html"].find("flint”-like")
        print("  " + r["content_html"][max(0, i - 160):i + 80].replace("\n", " "))
        if "Dickens’s “flint”-like" not in r["content_html"]:
            fails.append("ACC L7: flint sentence not repaired")
    for f in PLAIN:
        if f in blob and ENTITY.search(blob[f]):
            fails.append(f"{unit} L{num} {f}: HTML entity in plain-text field")
    ids = []
    for f in ("content_html", "exam_tip_html", "conclusion_html"):
        ids += [i for i, _ in extract_narration_chunks(r.get(f) or "")]
    dups = sorted({x for x in ids if ids.count(x) > 1})
    print(f"  narration ids: {len(ids)}, duplicates: {dups or 'none'}")
    if dups:
        fails.append(f"{unit} L{num}: duplicate narration ids {dups}")

# BDC duplicate-id check
for r in rows:
    ids = []
    for f in ("content_html", "exam_tip_html", "conclusion_html"):
        ids += [i for i, _ in extract_narration_chunks(r.get(f) or "")]
    dups = sorted({x for x in ids if ids.count(x) > 1})
    if dups:
        fails.append(f"BDC L{r['lesson_number']}: duplicate narration ids {dups}")

print("\n" + "=" * 78)
if fails:
    print(f"FAILURES ({len(fails)}):")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("ALL CHECKS PASSED")
