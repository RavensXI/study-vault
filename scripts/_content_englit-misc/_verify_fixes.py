"""Final verification: re-fetch every touched row and assert each fix landed."""
import json, os, re, sys
import requests
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client
from lib.narration import extract_narration_chunks

FRANK_L2 = "07d83404-fde9-43ab-8461-2064e8bb282b"
FRANK_L6 = "0581f441-6e06-475c-b1b3-36d8184b8673"
LT_L2 = "e832b6dd-6e34-4e53-b71b-78c8ece8e905"
LT_L3 = "4038c672-d9f6-4924-9195-71745f273f3c"
LT_L5 = "dfc930cd-8246-46cc-9d9b-4fc16885d08e"
BDC_L6 = "c81cefe5-ecc1-4cc0-a8c6-1e30dbb7aee5"

# (lesson, field, must_contain[], must_NOT_contain[])
ASSERTS = [
    (FRANK_L6, "content_html",
     ["Walton yields to them", "abandons the quest and turns the ship for home",
      "ambiguous is not Walton’s choice but the Creature’s ending"],
     ["Walton must decide whether to continue", "Shelley leaves this choice ambiguous"]),
    (FRANK_L2, "content_html",
     ["and Walton agrees, abandoning the expedition"],
     ["Shelley leaves this ambiguous"]),
    (LT_L2, "title", ["Scenes 1–3: Enid, Del & the Obeah Woman"], ["Act 1", "Act 2"]),
    (LT_L3, "title", ["Scenes 4–7: Generational Conflict"], ["Act 1", "Act 2"]),
    (LT_L3, "content_html", ["Enid eventually left him"],
     ["abandoned by her husband"]),
    (LT_L5, "content_html",
     ["Enid ended the marriage to protect her daughters"],
     ["She was abandoned by her husband", "abandoned by her husband"]),
    (BDC_L6, "content_html",
     ["its effect on the reader", "state what the novelist does"],
     ["effect on the audience", "what the playwright does"]),
]

ENT = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#\d{2,6}|#[xX][0-9a-fA-F]{2,6});")
PLAIN = ["title", "description", "knowledge_checks", "practice_questions",
         "flashcard_questions", "glossary_terms"]

sb = get_client()
fails = 0

print("── content assertions " + "─" * 50)
for lid, field, must, mustnt in ASSERTS:
    row = sb.table("lessons").select(f"lesson_number,{field}").eq(
        "id", lid).single().execute().data
    val = row[field]
    for s in must:
        ok = s in val
        fails += not ok
        print(f"  [{'OK ' if ok else 'FAIL'}] {lid[:8]} L{row['lesson_number']} "
              f"{field} contains {s[:58]!r}")
    for s in mustnt:
        ok = s not in val
        fails += not ok
        print(f"  [{'OK ' if ok else 'FAIL'}] {lid[:8]} L{row['lesson_number']} "
              f"{field} free of {s[:58]!r}")

print("\n── plain-text fields free of HTML entities " + "─" * 30)
for lid in {a[0] for a in ASSERTS}:
    row = sb.table("lessons").select("lesson_number," + ",".join(PLAIN)).eq(
        "id", lid).single().execute().data
    hits = set()
    for f in PLAIN:
        v = row.get(f)
        if v is None:
            continue
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        hits |= set(ENT.findall(s))
    fails += bool(hits)
    print(f"  [{'OK ' if not hits else 'FAIL'}] {lid[:8]} L{row['lesson_number']} "
          f"{'clean' if not hits else hits}")

print("\n── narration manifest integrity + live clips " + "─" * 28)
RENARRATED = {FRANK_L6: "n13", LT_L5: "n3", BDC_L6: "n28", FRANK_L2: "n13"}
for lid, nid in RENARRATED.items():
    row = sb.table("lessons").select(
        "lesson_number,content_html,exam_tip_html,conclusion_html,"
        "narration_manifest").eq("id", lid).single().execute().data
    chunks = []
    for f in ("content_html", "exam_tip_html", "conclusion_html"):
        chunks += extract_narration_chunks(row.get(f) or "")
    mani = row["narration_manifest"]
    aligned = [c[0] for c in chunks] == [e["id"] for e in mani]
    fails += not aligned
    entry = next(e for e in mani if e["id"] == nid)
    # NB: use requests, not urllib — R2/Cloudflare 403s urllib's default UA.
    try:
        r = requests.get(entry["src"], headers={"Cache-Control": "no-cache"},
                         timeout=30)
        code, nbytes = r.status_code, len(r.content)
    except Exception as e:
        code, nbytes = f"ERR {e}", 0
    ok = code == 200
    fails += not ok
    print(f"  [{'OK ' if aligned and ok else 'FAIL'}] {lid[:8]} L{row['lesson_number']} "
          f"{nid}: ids aligned={aligned} ({len(mani)} entries), "
          f"HTTP {code}, {nbytes}B, duration={entry['duration']}s")

print(f"\n{'ALL CHECKS PASSED' if not fails else str(fails) + ' FAILURES'}")
sys.exit(1 if fails else 0)
