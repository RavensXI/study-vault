"""Retro fact-check: per-unit orchestrator for the autonomous loop.

    python scripts/_retrofc/_unit.py next
        -> JSON for the next queued unit (or {"done": true})
    python scripts/_retrofc/_unit.py prep <subject> <unit>
        -> fetch the unit (raw JSON + per-lesson txt), resolve the spec file,
           try to cache the primary text from Project Gutenberg, write
           <unit-dir>/_brief.json and print it. Safe to re-run.
    python scripts/_retrofc/_unit.py finish <subject> <unit> [--no-narrate]
        -> apply <unit-dir>/_edits.json (backup first), run the content
           validator before/after and refuse on NEW violations, re-narrate
           changed narrated blocks, update _queue.json + _state.json, build
           the tracker HTML, commit. Idempotent per unit.

State on disk is the only memory this loop has: every stage leaves files in
scripts/_retrofc/units/<subject>__<unit>/ and the queue/state ledgers, so a
session cut off mid-unit costs at most that unit's partial work.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
QUEUE = os.path.join(HERE, "_queue.json")
STATE = os.path.join(HERE, "_state.json")
TEXTS = os.path.join(HERE, "_texts")
SPECS = {
    "aqa": "specs/aqa/english-literature-8702-8702.md",
    "edexcel": "specs/edexcel/english-literature-1ET0.md",
    "ocr": "specs/ocr/english-literature-J352.md",
    "eduqas": "specs/eduqas/english-literature-C720QS.md",
}
# Public-domain set texts -> Gutendex search. Anything not listed is in
# copyright: the checker verifies quotations by web search instead.
PD_TEXTS = [
    ("christmas-carol", "Dickens A Christmas Carol"),
    ("great-expectations", "Dickens Great Expectations"),
    ("pride-and-prejudice", "Austen Pride and Prejudice"),
    ("jane-eyre", "Bronte Jane Eyre"),
    ("frankenstein", "Shelley Frankenstein"),
    ("jekyll", "Stevenson Jekyll Hyde"),
    ("silas-marner", "Eliot Silas Marner"),
    ("war-of-the-worlds", "Wells War of the Worlds"),
    ("sign-of-four", "Doyle Sign of the Four"),
    ("macbeth", "Shakespeare Macbeth"),
    ("romeo-and-juliet", "Shakespeare Romeo and Juliet"),
    ("much-ado", "Shakespeare Much Ado About Nothing"),
    ("tempest", "Shakespeare Tempest"),
    ("merchant-of-venice", "Shakespeare Merchant of Venice"),
    ("julius-caesar", "Shakespeare Julius Caesar"),
    ("twelfth-night", "Shakespeare Twelfth Night"),
    ("othello", "Shakespeare Othello"),
    ("henry-v", "Shakespeare Henry V"),
]
NARRATED = ("content_html", "exam_tip_html", "conclusion_html")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def unit_dir(subject, unit):
    return os.path.join(HERE, "units", f"{subject}__{unit}")


def run(cmd, check=True, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if check and r.returncode != 0:
        raise SystemExit(f"FAILED ({r.returncode}): {' '.join(cmd)}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return r


def board_of(subject):
    return subject.rsplit("-", 1)[-1]


# ----------------------------------------------------------------------- next
def cmd_next():
    q = load(QUEUE)
    for it in q["items"]:
        if it.get("status") == "queued":
            print(json.dumps({"subject": it["subject"], "unit": it["unit"], "lessons": it.get("lessons"),
                              "remaining": sum(1 for x in q["items"] if x.get("status") == "queued")}))
            return
    print(json.dumps({"done": True}))


# ----------------------------------------------------------------------- prep
# Known Gutenberg ebook ids, used when Gutendex is down. Every download is
# checked against the title words before it is trusted.
GUTENBERG_IDS = {
    "christmas-carol": [46, 19337], "great-expectations": [1400], "pride-and-prejudice": [1342],
    "jane-eyre": [1260], "frankenstein": [84, 41445], "jekyll": [43], "silas-marner": [550],
    "war-of-the-worlds": [36], "sign-of-four": [2097], "macbeth": [1533, 2264],
    "romeo-and-juliet": [1513, 1112], "much-ado": [1519, 2240], "tempest": [23042, 1540],
    "merchant-of-venice": [1515, 2243], "julius-caesar": [1522, 2263], "twelfth-night": [1526, 2247],
    "othello": [1531, 2267], "henry-v": [1521, 2253],
}


def _get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "StudyVault fact-check"}), timeout=timeout).read()


def _title_ok(txt, query):
    head = txt[:4000].lower()
    words = [w for w in re.findall(r"[a-z]+", query.lower()) if len(w) > 3 and w not in ("shakespeare", "dickens", "austen", "bronte", "shelley", "stevenson", "eliot", "wells", "doyle")]
    return all(w in head for w in words)


def fetch_gutenberg(unit, d):
    os.makedirs(TEXTS, exist_ok=True)
    for key, query in PD_TEXTS:
        if key not in unit:
            continue
        out = os.path.join(TEXTS, f"{key}.txt")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            return out, query
        notes = []
        # 0) Curated ids first: Gutendex once returned a LibriVox catalogue whose
        #    header mentioned the title (Silas Marner, #26269), so a title match
        #    alone is not proof. Novels and plays are long; require real length.
        for gid in GUTENBERG_IDS.get(key, []):
            for url in (f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt", f"https://www.gutenberg.org/files/{gid}/{gid}-0.txt"):
                try:
                    txt = _get(url).decode("utf-8", "replace")
                except Exception:  # noqa: BLE001
                    continue
                if len(txt) > 60000 and _title_ok(txt, query):
                    with open(out, "w", encoding="utf-8") as f:
                        f.write(txt)
                    return out, f"{query} (Gutenberg #{gid}, curated id)"
        # 1) Gutendex search
        try:
            data = json.loads(_get("https://gutendex.com/books?languages=en&search=" + urllib.parse.quote(query), 60))
            for b in data.get("results", []):
                turl = next((v for k, v in b.get("formats", {}).items() if k.startswith("text/plain")), None)
                if not turl:
                    continue
                txt = _get(turl).decode("utf-8", "replace")
                if len(txt) > 20000 and _title_ok(txt, query):
                    with open(out, "w", encoding="utf-8") as f:
                        f.write(txt)
                    return out, f"{query} (Gutenberg #{b.get('id')}: {b.get('title')})"
            notes.append("gutendex: no matching plain-text edition")
        except Exception as e:  # noqa: BLE001
            notes.append(f"gutendex failed ({str(e)[:60]})")
        # 2) Direct by known id, title-verified
        for gid in GUTENBERG_IDS.get(key, []):
            for url in (f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt", f"https://www.gutenberg.org/files/{gid}/{gid}-0.txt"):
                try:
                    txt = _get(url).decode("utf-8", "replace")
                except Exception:  # noqa: BLE001
                    continue
                if len(txt) > 20000 and _title_ok(txt, query):
                    with open(out, "w", encoding="utf-8") as f:
                        f.write(txt)
                    return out, f"{query} (Gutenberg #{gid}, direct)"
            notes.append(f"#{gid}: not found or title mismatch")
        return None, f"{query}: " + "; ".join(notes)
    return None, "in copyright - verify quotations by web search"


def cmd_prep(subject, unit):
    d = unit_dir(subject, unit)
    os.makedirs(d, exist_ok=True)
    r = run(["node", os.path.join(HERE, "_fetch_unit.js"), subject, unit])
    raw = load(os.path.join(d, "_raw.json"))
    spec = SPECS[board_of(subject)]
    text_path, text_note = fetch_gutenberg(unit, d)
    brief = {
        "subject": subject, "unit": unit, "unit_name": raw["unit"]["name"], "dir": os.path.relpath(d, ROOT),
        "spec": spec, "board": board_of(subject),
        "primary_text": os.path.relpath(text_path, ROOT) if text_path else None, "primary_text_note": text_note,
        "lessons": [{"n": l["lesson_number"], "title": l["title"], "chars": len(l.get("content_html") or "")} for l in raw["lessons"]],
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    save(os.path.join(d, "_brief.json"), brief)
    print(json.dumps(brief, indent=1, ensure_ascii=False))


# --------------------------------------------------------------------- finish
def validator_violations(row):
    """Run the content validator on one lesson row; return the violation list."""
    fd, p = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    keep = ["description", "content_html", "exam_tip_html", "conclusion_html", "practice_questions",
            "knowledge_checks", "flashcard_questions", "glossary_terms", "title"]
    save(p, {k: row.get(k) for k in keep})
    r = run([sys.executable, os.path.join(ROOT, "scripts", "_validate_content_json.py"), p], check=False)
    os.remove(p)
    return sorted(set(l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip() and not l.startswith(("[OK]", "Usage", "==")) and p not in l))


def fetch_rows(unit_id):
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    cols = "id,lesson_number,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms"
    req = urllib.request.Request(f"{U}/rest/v1/lessons?unit_id=eq.{unit_id}&select={cols}&order=lesson_number",
                                 headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def cmd_finish(subject, unit, narrate=True):
    d = unit_dir(subject, unit)
    raw = load(os.path.join(d, "_raw.json"))
    report = load(os.path.join(d, "_report.json"), {})
    edits = load(os.path.join(d, "_edits.json"), [])
    findings = report.get("findings", []) if isinstance(report, dict) else []
    summary = {"subject": subject, "unit": unit, "findings": len(findings), "edits": len(edits)}

    # Validator BEFORE (live rows as they are now, i.e. pre-edit)
    pre = {r["lesson_number"]: validator_violations(r) for r in fetch_rows(raw["unit"]["id"])} if edits else {}

    applied = {"applied": 0, "skipped": 0, "lessons_changed": 0}
    if edits:
        r = run(["node", os.path.join(HERE, "_apply_edits.js"), d], check=False)
        print(r.stdout[-3000:])
        if r.returncode not in (0, 3):
            raise SystemExit("apply failed:\n" + r.stderr[-2000:])
        applied = load(os.path.join(d, "_apply_result.json"), applied)
        # Validator AFTER: refuse NEW violations by restoring from backup
        post = {r["lesson_number"]: validator_violations(r) for r in fetch_rows(raw["unit"]["id"])}
        # Compare violation KINDS, not messages: the validator embeds counts
        # ("word count 546"), so a pre-existing violation whose number moved
        # by a few words must not read as new.
        kind = lambda v: re.sub(r"\d+", "#", v.split(":")[0])  # noqa: E731
        pre_kinds = {n: {kind(v) for v in vs} for n, vs in pre.items()}
        new_viol = {n: [v for v in post.get(n, []) if kind(v) not in pre_kinds.get(n, set())] for n in post}
        new_viol = {n: v for n, v in new_viol.items() if v}
        if new_viol:
            print("NEW VALIDATOR VIOLATIONS after edits:", json.dumps(new_viol, indent=1)[:2000])
            restore_from_backup(d)
            raise SystemExit("edits rolled back - fix _edits.json and re-run finish")
    summary.update(applied)

    # Re-narrate only if a narrated field changed
    backup = load(os.path.join(d, "_backup.json"))
    narrated_changed = bool(backup and any(any(f in e.get("before", {}) for f in NARRATED) for e in backup["lessons"]))
    summary["renarrated"] = False
    if narrated_changed and narrate:
        r = run([sys.executable, os.path.join(HERE, "_renarrate_from_backup.py"), "--backup", os.path.join(d, "_backup.json")], check=False)
        print(r.stdout[-1500:])
        if r.returncode != 0:
            raise SystemExit("re-narration failed:\n" + r.stderr[-1500:])
        summary["renarrated"] = True

    # Ledgers
    today = datetime.date.today().isoformat()
    q = load(QUEUE)
    for it in q["items"]:
        if it["subject"] == subject and it["unit"] == unit:
            it.update({"status": "done", "findings": len(findings), "fixed": applied["applied"], "checked_on": today})
    save(QUEUE, q)
    st = load(STATE)
    row = next((s for s in st["subjects"] if (s.get("slug") or s.get("subject")) == subject), None)
    if row is not None:
        row["findings"] = (row.get("findings") or 0) + len(findings)
        row["fixed"] = (row.get("fixed") or 0) + applied["applied"]
        row["checked_on"] = today
        left = [x for x in q["items"] if x["subject"] == subject and x.get("status") == "queued"]
        row["status"] = "checked" if not left else "partial"   # tracker vocabulary: checked | partial
        mine = [x for x in q["items"] if x["subject"] == subject]
        done_n = sum(1 for x in mine if x.get("status") == "done")
        row["note"] = (f"{done_n} of {len(mine)} queued units checked by the overnight loop (latest: {unit}); "
                       f"mechanical relabel + band-ladder passes still pending as separate workstreams")
    st["batches"].append({"date": today, "what": f"{subject}/{unit} ({len(raw['lessons'])}L) - autonomous loop",
                          "findings": len(findings), "fixed": applied["applied"]})
    st["updated"] = today
    save(STATE, st)
    run([sys.executable, os.path.join(HERE, "build_tracker.py"), os.path.join(HERE, "_tracker.html")])

    # Commit the unit's evidence + ledgers
    rel = os.path.relpath(d, ROOT)
    run(["git", "add", rel, os.path.relpath(QUEUE, ROOT), os.path.relpath(STATE, ROOT)])
    msg = (f"Retro fact-check: {subject}/{unit} - {len(findings)} findings, {applied['applied']} fixes"
           f"{', re-narrated' if summary['renarrated'] else ''}\n\n"
           f"Autonomous overnight loop, unit-level checkpoint.\n\n"
           f"Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\n"
           f"Claude-Session: https://claude.ai/code/session_018B8Mk83MzFFhMoVFwvirTs\n")
    r = run(["git", "commit", "-q", "-m", msg], check=False)
    summary["committed"] = r.returncode == 0
    print(json.dumps(summary))


def restore_from_backup(d):
    backup = load(os.path.join(d, "_backup.json"))
    if not backup:
        return
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    for e in backup["lessons"]:
        body = json.dumps(e["before"]).encode()
        req = urllib.request.Request(f"{U}/rest/v1/lessons?id=eq.{e['id']}", data=body, method="PATCH",
                                     headers={"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=60).read()
        print("restored L", e["lesson_number"], list(e["before"]))
    stamp = datetime.datetime.now().strftime("%H%M%S")
    os.rename(os.path.join(d, "_backup.json"), os.path.join(d, f"_backup.rolledback-{stamp}.json"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    if a[0] == "next":
        cmd_next()
    elif a[0] == "prep":
        cmd_prep(a[1], a[2])
    elif a[0] == "finish":
        cmd_finish(a[1], a[2], narrate="--no-narrate" not in a)
    elif a[0] == "restore":
        restore_from_backup(unit_dir(a[1], a[2]))
    else:
        raise SystemExit(__doc__)
