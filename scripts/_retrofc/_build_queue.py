"""Append one priority band of subjects to the retro fact-check queue.

Reads `_state.json` (subjects with `priority` 1-9 and status unchecked /
partial), resolves each subject's spec file from `specs/index.json` by board
+ subject name (with slug hints for A/B variants), and appends every article
unit (practice units excluded) as a queued item carrying `family`, `spec`
and `qualification`. Prints the mapping first; nothing is saved without
`--confirm`. Idempotent per (subject, unit).

Usage:
  python scripts/_retrofc/_build_queue.py --priority 3 [--confirm]
  python scripts/_retrofc/_build_queue.py --subjects history-aqa,history-ocr --family history --confirm

Family -> checker brief mapping lives in _unit.py (history, science,
english-literature; everything else -> CHECK_PROMPT_GENERIC.md).
"""
import json
import os
import re
import sys
import urllib.request
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
QUEUE = os.path.join(HERE, "_queue.json")
STATE = os.path.join(HERE, "_state.json")
INDEX = os.path.join(ROOT, "specs", "index.json")

FAMILY_BY_PRIORITY = {1: "english-literature", 2: "science", 3: "history", 4: "geography", 5: "rs-geology-astronomy",
                      6: "business-cs-pe-sociology-dt", 7: "niche", 8: "music-technology", 9: "music"}
# Subjects already handled by a dedicated builder or exempt.
SKIP = {"science-aqa", "science-edexcel", "science-ocr", "science-ocr-b", "separate-sciences", "separate-sciences-edexcel",
        "separate-sciences-ocr", "separate-sciences-ocr-b"}
# Hand overrides where the index cannot tell: slug -> spec path relative to specs/ ("" = no spec in the repo: skip, log).
OVERRIDES = {"history-ocr": "ocr/history-a-J410.md",            # units are the Explaining the Modern World options
             "it-ocr": "ocr/cambridge-nationals-it-J836.md",
             "health-social-care-edexcel": ""}                   # BTEC Tech Award: no spec downloaded yet
BOARD_ALIASES = {"aqa": "AQA", "edexcel": "Edexcel", "pearson": "Edexcel", "ocr": "OCR", "eduqas": "Eduqas", "wjec": "Eduqas"}


def get(path):
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    req = urllib.request.Request(U + "/rest/v1/" + path, headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def resolve_spec(slug, name, board, index):
    """Best-effort spec match: same board, subject name overlap, A/B slug hints."""
    b = BOARD_ALIASES.get((board or "").split("/")[0].strip().lower(), board)
    cands = [e for e in index if e.get("board", "").lower().startswith((b or "").lower()[:3])]
    n = norm(name)
    base = re.sub(r"\b(gcse|level 1 2|l1 2|cambridge nationals?|studies)\b", "", n).strip()
    words = [w for w in base.split() if w not in ("and", "the", "of", "a", "b")]
    scored = []
    for e in cands:
        es = norm(e.get("subject", ""))
        es_words = [w for w in es.split() if w not in ("and", "the", "of", "studies")]
        score = sum(1 for w in words if w in es_words)
        if not score:
            continue
        score -= 0.6 * sum(1 for w in es_words if w not in words and w not in ("a", "b"))   # extra words: Ancient History, Citizenship Studies
        # A/B variant hints from the slug
        if slug.endswith("-a") and re.search(r"\b(a|gateway)\b", es):
            score += 2
        if slug.endswith("-b") and re.search(r"\b(b|21c|21st)\b", es):
            score += 2
        if not slug.endswith(("-a", "-b")) and re.search(r"\b(a|b)\b", es):
            score -= 0.5
        score -= 0.1 * abs(len(es.split()) - len(words))
        scored.append((score, e))
    scored.sort(key=lambda x: -x[0])
    return scored[0][1]["path"] if scored else None


def main():
    args = sys.argv[1:]
    confirm = "--confirm" in args
    prio = int(args[args.index("--priority") + 1]) if "--priority" in args else None
    subjects = args[args.index("--subjects") + 1].split(",") if "--subjects" in args else None
    family = args[args.index("--family") + 1] if "--family" in args else (FAMILY_BY_PRIORITY.get(prio) if prio else "generic")
    st = json.load(open(STATE, encoding="utf-8"))
    if subjects is None:
        subjects = [s["slug"] for s in st["subjects"] if s.get("priority") == prio and s["status"] in ("unchecked", "partial") and s["slug"] not in SKIP]
    index = json.load(open(INDEX, encoding="utf-8"))
    q = json.load(open(QUEUE, encoding="utf-8"))
    have = {(i["subject"], i["unit"]) for i in q["items"]}
    rows = {s["slug"]: s for s in get(f"subjects?select=id,slug,name,exam_board,settings&school_id=is.null&slug=in.({','.join(subjects)})")}
    added, unresolved = [], []
    for slug in subjects:
        s = rows.get(slug)
        if not s:
            print("!! subject not found:", slug)
            continue
        if OVERRIDES.get(slug) == "":
            print(f"{slug:45s} SKIPPED: no spec in the repo (download it, then queue with --subjects)")
            continue
        spec = OVERRIDES.get(slug) or resolve_spec(slug, s["name"], s.get("exam_board"), index)
        print(f"{slug:45s} {s.get('exam_board') or '':10s} {s['name'][:40]:40s} -> {spec}")
        if not spec:
            unresolved.append(slug)
            continue
        practice = set((s.get("settings") or {}).get("practice_units") or [])
        units = get(f"units?select=id,slug,name,sort_order&subject_id=eq.{s['id']}&order=sort_order")
        if not units:
            continue
        ids = ",".join(u["id"] for u in units)
        lessons = get(f"lessons?select=id,unit_id,status,practice_data&unit_id=in.({ids})")
        live = Counter(x["unit_id"] for x in lessons if x.get("status") == "live")
        pdata = Counter(x["unit_id"] for x in lessons if x.get("status") == "live" and x.get("practice_data"))
        for u in units:
            n = live.get(u["id"], 0)
            if not n or u["slug"] in practice or pdata.get(u["id"], 0) == n or (slug, u["slug"]) in have:
                continue
            item = {"subject": slug, "unit": u["slug"], "lessons": n, "status": "queued", "spec": os.path.join("specs", spec).replace("\\", "/"),
                    "family": family, "qualification": None}
            q["items"].append(item)
            added.append(item)
    print(f"\n{len(added)} units, {sum(a['lessons'] for a in added)} lessons for family '{family}'")
    if unresolved:
        print("UNRESOLVED specs (fix by hand before confirming):", unresolved)
    if confirm and not unresolved:
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("queue saved")
    elif confirm:
        print("NOT saved: unresolved specs")
    else:
        print("dry run: add --confirm to save")


if __name__ == "__main__":
    main()
