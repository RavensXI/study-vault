# -*- coding: utf-8 -*-
"""Pre-narration fact-check fixes for english-literature-ocr / unseen-poetry L1-L6.

Backs up every field it touches to _unseen_factcheck_backup.json, then PATCHes
Supabase by lesson id. Every replacement is asserted to hit exactly once, so a
drifted source aborts rather than silently no-ops.
"""
import sys, os, json, datetime
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lib.supabase_client import get_client

sb = get_client()
BACKUP = os.path.join(HERE, "_unseen_factcheck_backup.json")

L1 = "23c00d1c-4563-4335-983f-737a8bf981ae"
L2 = "242f3166-ab45-4c6d-af73-6cc404d73088"
L3 = "6ac8cb2a-b621-4d9a-9658-026e311f6fcd"
L5 = "50585cf6-b6db-4202-b235-517ac8b8ff76"
L6 = "d88323aa-2611-4bd2-80be-299975c28abd"

# ---------------------------------------------------------------- HTML edits
HTML_EDITS = [
    # HIGH — 'Love After Love' is in Love and Relationships, not Youth and Age.
    # Replaced with 'Equilibrium', named by OCR's own 2024 examiners' report as a
    # Youth and Age Part B choice.
    (L1, "F1-HIGH-cluster",
     "<strong>Youth and Age</strong> includes William Blake&rsquo;s &lsquo;Holy Thursday&rsquo; and Derek Walcott&rsquo;s &lsquo;Love After Love&rsquo;.",
     "<strong>Youth and Age</strong> includes William Blake&rsquo;s &lsquo;Holy Thursday&rsquo; and Theresa Lola&rsquo;s &lsquo;Equilibrium&rsquo;."),

    # HIGH — the anthology prints the 1799 Prelude ("a huge cliff"). The famous
    # "a huge peak, black and huge" is the 1850 text and is NOT in this anthology.
    (L2, "F2-HIGH-wordsworth",
     "In Wordsworth&rsquo;s boat-stealing episode, &ldquo;a huge peak, black and huge&rdquo; seems to rise and stride after the boy. The mountain has not moved;",
     "In Wordsworth&rsquo;s &lsquo;Boat Stealing&rsquo;, &ldquo;a huge cliff&rdquo; &ldquo;Upreared its head&rdquo; and, &ldquo;with measured motion, like a living thing&rdquo;, &ldquo;Strode after&rdquo; the boy. The cliff has not moved;"),

    # MEDIUM — 'bloom most constantly' is a question the poem asks, not a claim
    # it makes about the holly. The turn is stanza three's imperative.
    (L3, "F3-MED-bronte-turn",
     "then turns from the showy rose to the plant that will &ldquo;bloom most constantly&rdquo;.",
     "then asks &ldquo;which will bloom most constantly?&rdquo; before turning, in the final stanza, to the imperative &ldquo;scorn the silly rose-wreath now&rdquo;."),

    (L5, "F4-MED-bronte-question",
     "using the seasonal cycle as a test that love fails and friendship survives: the holly will &ldquo;bloom most constantly&rdquo;.",
     "then asks &ldquo;which will bloom most constantly?&rdquo; and uses the seasonal cycle to answer for the holly."),

    # MEDIUM — L5 teaches a five-minute grid; L6's timeline allowed three.
    # OCR's 2024 report backs the five-minute planning exercise.
    (L6, "F5-MED-timing-grid",
     "<div class=\"timeline-date\">5&ndash;8 min</div>",
     "<div class=\"timeline-date\">5&ndash;10 min</div>"),
    (L6, "F5-MED-timing-write",
     "<div class=\"timeline-date\">8&ndash;30 min</div>",
     "<div class=\"timeline-date\">10&ndash;30 min</div>"),
]

# ------------------------------------------------------ plain-text JSON edits
# LOW — plain-text fields must carry unicode, not a stripped name.
JSON_EDITS = [
    (L3, "flashcard_questions", "F6-LOW-bronte-spelling",
     "Which two plants does Emily Bronte set against each other in her poem on love?",
     "Which two plants does Emily Brontë set against each other in her poem on love?"),
    (L5, "knowledge_checks", "F6-LOW-bronte-spelling",
     "Bronte trusts constancy where Hardy finds only coldness",
     "Brontë trusts constancy where Hardy finds only coldness"),
    (L6, "knowledge_checks", "F5-MED-timing-kc-grid",
     "Minutes 5 to 8",
     "Minutes 5 to 10"),
    (L6, "knowledge_checks", "F5-MED-timing-kc-write",
     "Minutes 8 to 30",
     "Minutes 10 to 30"),
]

ids = sorted({e[0] for e in HTML_EDITS} | {e[0] for e in JSON_EDITS})
rows = {}
for i in ids:
    r = sb.table("lessons").select("id,lesson_number,title,content_html,knowledge_checks,flashcard_questions") \
        .eq("id", i).execute().data[0]
    rows[i] = r

backup = {
    "created": datetime.datetime.now().isoformat(timespec="seconds"),
    "subject": "english-literature-ocr",
    "unit": "unseen-poetry",
    "reason": "pre-narration fact-check gate",
    "lessons": {i: {"lesson_number": rows[i]["lesson_number"], "title": rows[i]["title"],
                    "content_html": rows[i]["content_html"],
                    "knowledge_checks": rows[i]["knowledge_checks"],
                    "flashcard_questions": rows[i]["flashcard_questions"]} for i in ids},
}
with open(BACKUP, "w", encoding="utf-8") as f:
    json.dump(backup, f, ensure_ascii=False, indent=1)
print("backup written:", BACKUP)

patch = {i: {} for i in ids}

for lid, tag, old, new in HTML_EDITS:
    src = patch[lid].get("content_html", rows[lid]["content_html"])
    n = src.count(old)
    assert n == 1, "%s: expected 1 match for %s, found %d" % (lid, tag, n)
    patch[lid]["content_html"] = src.replace(old, new)
    print("  ok html  %s  %s" % (tag, lid[:8]))

for lid, field, tag, old, new in JSON_EDITS:
    cur = patch[lid].get(field)
    if cur is None:
        cur = rows[lid][field]
    blob = json.dumps(cur, ensure_ascii=False)
    n = blob.count(old)
    assert n == 1, "%s.%s: expected 1 match for %s, found %d" % (lid, field, tag, n)
    patch[lid][field] = json.loads(blob.replace(old, new))
    print("  ok json  %s  %s.%s" % (tag, lid[:8], field))

for lid, fields in patch.items():
    if not fields:
        continue
    sb.table("lessons").update(fields).eq("id", lid).execute()
    print("PATCHED %s  L%s  fields=%s" % (lid, rows[lid]["lesson_number"], list(fields)))
print("done")
