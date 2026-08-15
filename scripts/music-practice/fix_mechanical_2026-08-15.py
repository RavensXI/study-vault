"""Overnight mechanical fixes from Tom's review (catalogue: AOS1-1, SR-1,
AOS2-2, WC-4).

Inspect-before-cut: every change prints its before/after evidence, and the
one genuinely judgement-shaped item (WC-4's odd listen box) is inspected and
only wrapped if it unambiguously matches the listen-instruction pattern —
otherwise it is logged for Tom rather than guessed at.

Backups per lesson to _backup_mechanical_2026-08-15.json before any write.

Guard-safety note that changed the plan: ALL 37 English Language reorder
problems carry and legitimately use passage_id (reordering events from the
extract), so the renderer guard is vocab_match ONLY; music's stray reorder
refs are stripped in data instead.
"""
import io
import json
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
APPLY = "--apply" in sys.argv


def get(path):
    r = urllib.request.Request(URL + "/rest/v1/" + path, headers=H)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


def patch(path, body):
    h = dict(H)
    h["Prefer"] = "return=representation"
    r = urllib.request.Request(URL + "/rest/v1/" + path,
                               data=json.dumps(body).encode("utf-8"),
                               headers=h, method="PATCH")
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


subj = get("subjects?select=id&slug=eq.music-aqa")[0]
units = {u["slug"]: u["id"] for u in get("units?select=id,slug&subject_id=eq.%s" % subj["id"])}
backups = {}
writes = []          # (lesson_id, {fields})


def queue(lesson_id, fields, current_full_row):
    backups[lesson_id] = current_full_row
    writes.append((lesson_id, fields))


# ---------- AOS1-1: strip stray passage refs from vocab_match + reorder ----------
print("== AOS1-1: stripping stray excerpt refs (music only) ==")
stripped = 0
for l in get("lessons?select=id,lesson_number,practice_data&unit_id=eq.%s&order=lesson_number"
             % units["western-classical-1650-1910"]):
    pd = l["practice_data"]
    touched = False
    for tier in ("bronze", "silver", "gold"):
        for i, p in enumerate(pd.get("problem_bank", {}).get(tier) or []):
            if p.get("input_type") in ("vocab_match", "reorder") and p.get("passage_id"):
                print("  L%s %s[%d] %s: removing passage %s"
                      % (l["lesson_number"], tier, i, p["input_type"], p["passage_id"]))
                del p["passage_id"]
                stripped += 1
                touched = True
    if touched:
        queue(l["id"], {"practice_data": pd}, {"practice_data": l["practice_data"]})
print("  total stripped: %d (expect 16)" % stripped)

# ---------- SR-1: the 6/8 theory question loses its wrong anchor ----------
print("\n== SR-1: score-reading L2 6/8 question ==")
sr = get("lessons?select=id,lesson_number,practice_data&unit_id=eq.%s&lesson_number=eq.2"
         % units["score-reading"])[0]
pd = sr["practice_data"]
for i, p in enumerate(pd["problem_bank"]["bronze"]):
    q = re.sub(r"<[^>]+>", " ", (p.get("question") or "") + (p.get("display") or ""))
    if "6/8" in q and "simple or compound" in q.lower() and p.get("passage_id"):
        print("  bronze[%d]: removing anchor %s (theory question, self-contained)"
              % (i, p["passage_id"]))
        del p["passage_id"]
        queue(sr["id"], {"practice_data": pd}, {"practice_data": sr["practice_data"]})

# ---------- AOS2-2: exam tips restating the narrated body paragraph ----------
# The duplication is body-vs-tip, not body-vs-body. The tip is not narrated,
# the body paragraph IS (n18 / n3) — so the tip takes the cut. Drop only the
# restating sentence; keep the actionable technique/feature guidance.
print("\n== AOS2-2: dedupe exam tips in aos2-popular-music ==")
TIP_CUTS = {
    2: "Section A extracts are short and unfamiliar, so do not guess which "
       "show, film or game it is from &mdash; you are never marked on that. ",
    4: "Do not guess a year. ",
}
for lesson_no, cut in TIP_CUTS.items():
    l = get("lessons?select=id,exam_tip_html&unit_id=eq.%s&lesson_number=eq.%d"
            % (units["aos2-popular-music"], lesson_no))[0]
    tip = l["exam_tip_html"]
    if cut in tip:
        new_tip = tip.replace(cut, "", 1)
        print("  L%d tip: cut %r" % (lesson_no, cut[:60]))
        print("       now: %r" % re.sub(r"<[^>]+>", "", new_tip)[:100])
        queue(l["id"], {"exam_tip_html": new_tip}, {"exam_tip_html": tip})
    else:
        print("  !! L%d: cut text not found verbatim — left for Tom" % lesson_no)

# ---------- WC-4: report only (corrected diagnosis) ----------
# L2's first TWO sv-listen figures lack data-narration-id, so narration skips
# them and they render without the play affordance. Adding ids without audio
# segments would fake a dead control; the real fix is L2 re-narration after
# Tom approves content. No write here.
print("\n== WC-4: report only ==")
wc = get("lessons?select=content_html&unit_id=eq.%s&lesson_number=eq.2"
         % units["aos1-western-classical"])[0]
bare = len(re.findall(r'<figure class="sv-listen">', wc["content_html"]))
print("  aos1-western-classical L2: %d sv-listen figures WITHOUT narration id"
      " -> queue L2 re-narration post-approval" % bare)

# ---------- apply ----------
print("\nqueued writes: %d lesson(s)" % len(writes))
if not APPLY:
    print("DRY RUN — re-run with --apply")
    sys.exit(0)

io.open(os.path.join(HERE, "_backup_mechanical_2026-08-15.json"), "w",
        encoding="utf-8").write(json.dumps(backups))
for lesson_id, fields in writes:
    patch("lessons?id=eq.%s" % lesson_id, fields)
print("applied. backup: _backup_mechanical_2026-08-15.json")
