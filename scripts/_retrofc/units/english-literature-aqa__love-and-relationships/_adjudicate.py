"""
Apply the NINE ADJUDICATED rulings to english-literature-aqa / love-and-relationships.

Rulings are judgements already made - this script applies them verbatim.

Process:
  1. fetch the live rows
  2. build the new value for every touched field (exact-string surgery on HTML
     fields, structural surgery on JSON fields - never string surgery on JSON)
  3. assert every `find` occurs exactly the expected number of times
  4. write the pre-edit values to _adjudication_backup.json and FLUSH TO DISK
  5. PATCH lessons?id=eq.<id>
  6. re-fetch and assert old strings gone / new strings present / no HTML
     entities in plain-text fields

Usage:
  python _adjudicate.py --dry-run
  python _adjudicate.py
"""
import argparse
import json
import os
import re
import sys
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "_adjudication_backup.json")
UNIT_ID = "170f32cc-ff7e-4ae6-8376-3dd18d1208f4"

SB = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": KEY, "Authorization": "Bearer " + KEY,
       "Content-Type": "application/json"}

COLS = ("id,lesson_number,title,description,content_html,exam_tip_html,"
        "conclusion_html,practice_questions,knowledge_checks,"
        "flashcard_questions,glossary_terms")
STR_FIELDS = ["description", "content_html", "exam_tip_html", "conclusion_html"]
JSON_FIELDS = ["practice_questions", "knowledge_checks",
               "flashcard_questions", "glossary_terms"]


def get(path):
    req = urllib.request.Request(SB + "/rest/v1/" + path, headers=HDR)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def patch(lid, body):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    h = dict(HDR)
    h["Prefer"] = "return=minimal"
    req = urllib.request.Request(
        SB + "/rest/v1/lessons?id=eq." + lid, data=data, headers=h, method="PATCH")
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status not in (200, 204):
            raise SystemExit("PATCH %s -> %s" % (lid, r.status))


# ---------------------------------------------------------------- rulings ---
# (lesson_number, field, find, replace, expected_count, ruling)
HTML_EDITS = [
    # ---- RULING 1: Sonnet 29 - one consistent reading -----------------------
    (1, "content_html",
     "The speaker describes how thinking of her beloved changes her emotional "
     "state from despair to joy.",
     "The speaker begins in restless longing while her beloved is absent, and "
     "ends in the fulfilment of his real presence.",
     1, "R1 L1 n10"),
    (1, "content_html",
     "The <dfn class=\"term\" data-def=\"A turning point in a sonnet where the "
     "argument shifts direction, often marked by a change in rhyme scheme or a "
     "word like 'but' or 'yet'.\">volta</dfn> comes when she rejects her own "
     "fantasies in favour of reality: “I do not think of thee — I am "
     "too near thee.”",
     "The <dfn class=\"term\" data-def=\"A turning point in a sonnet where the "
     "argument shifts direction, often marked by a change in rhyme scheme or a "
     "word like 'but' or 'yet'.\">volta</dfn> comes mid-poem, at “Rather, "
     "instantly / Renew thy presence” — she puts aside her own "
     "thoughts of him and calls for the real man. The closing line is the "
     "resolution rather than the turn: longing in absence has become fulfilled "
     "presence — “I do not think of thee — I am too near "
     "thee.”",
     1, "R1 L1 n11"),
    (1, "content_html",
     "The volta rejects idealised fantasy for real presence — “I do "
     "not think of thee — I am too near thee.”",
     "The volta — “Rather, instantly / Renew thy presence” "
     "— rejects idealised fantasy and calls for the real man; the poem "
     "then closes in fulfilled presence: “I do not think of thee — I "
     "am too near thee.”",
     1, "R1 L1 n12 key fact"),
    (1, "content_html",
     "Barrett Browning transforms grief into joy (the volta)",
     "Barrett Browning moves from restless longing in absence to fulfilled "
     "presence (the volta)",
     1, "R1 L1 n15"),
    (8, "content_html",
     "<strong>Barrett Browning (Sonnet 29):</strong> “I do not think of "
     "thee — I am too near thee” — volta rejecting fantasy for "
     "reality.",
     "<strong>Barrett Browning (Sonnet 29):</strong> “Rather, instantly / "
     "Renew thy presence” — the volta, putting aside thoughts of him "
     "for the real man; “I do not think of thee — I am too near "
     "thee” — the close, longing replaced by presence.",
     1, "R1 L8 n5"),

    # ---- RULING 2: L3 drop the synaesthesia label --------------------------
    (3, "content_html",
     "and the <dfn class=\"term\" data-def=\"The transfer of meaning from one "
     "sense to another — e.g. 'hearing' colours or 'tasting' words.\">"
     "synaesthesia</dfn>-like image of souls “tapping” messages "
     "blends the physical (tapping) with the spiritual (souls), suggesting "
     "communication that transcends technology.",
     "and the image of souls “tapping” messages gives the spiritual "
     "bond a physical action, like a signal tapped out along a wire — a "
     "private message that crosses the miles without any technology at all.",
     1, "R2 L3 n11"),

    # ---- RULING 3: L4 Singh Song! moon reference ---------------------------
    (4, "content_html",
     "The mundane domestic detail (chapattis) is presented with the same "
     "delight as the moonlit description of her face: “my bride / she hav "
     "a red crew cut / and she wear a Tartan sari.”",
     "The mundane domestic detail (chapattis) is presented with the same "
     "delight as his bride herself: “my bride / she hav a red crew cut / "
     "and she wear a Tartan sari.” The moon arrives only in the closing "
     "dialogue, where the bride asks each night what the moon would cost and "
     "the speaker answers that it is “priceless” — she is worth "
     "more than anything he could price.",
     1, "R3 L4 n9"),

    # ---- RULING 4: L6 genuine caesura example ------------------------------
    (6, "content_html",
     "<strong>Caesura</strong> (mid-line pauses) creates sudden stops: "
     "Hardy’s “We stood by a pond that winter day,” pauses "
     "before revealing the bleak setting.",
     "<strong>Caesura</strong> (mid-line pauses) creates sudden stops: the "
     "full stops inside Armitage’s “years between us. Anchor. "
     "Kite.” cut the line into separate declarations, holding mother and "
     "son apart.",
     1, "R4 L6 n13"),

    # ---- RULING 6: L7 AQA is closed book throughout ------------------------
    (7, "content_html",
     "The named poem is <strong>open book</strong> (printed), but your chosen "
     "poem is <strong>closed book</strong> — you must recall it from "
     "memory.",
     "AQA English Literature is <strong>closed book</strong> throughout — "
     "you cannot take the anthology into the exam. The named poem is "
     "reproduced on the question paper; your chosen comparison poem must come "
     "from memory.",
     1, "R6 L7 n2"),

    # ---- RULING 7: L8 remove the cross-board print hedge -------------------
    (8, "content_html",
     "Some papers print one of the poems in the question booklet while your "
     "comparison poem is from memory — others may print neither. Either "
     "way, aim to memorise 2–3 quotations per poem for your “go-to"
     "” poems. Short, punchy quotations are easier to remember and more "
     "effective to analyse than long ones. Check your exam board’s "
     "specimen paper for the exact format.",
     "AQA prints the named poem on the question paper; your comparison poem "
     "must come from memory. Aim to memorise 2–3 quotations per poem for "
     "your “go-to” poems. Short, punchy quotations are easier to "
     "remember and more effective to analyse than long ones.",
     1, "R7 L8 n2"),
]

# JSON-field surgery: (lesson_number, field, mutator, ruling)
# Each mutator takes the parsed value and returns (new_value, note).


def r1_l1_pq(pqs):
    old = "thoughts of the beloved change grief to joy"
    new = ("restless longing in his absence gives way to the fulfilment of "
           "his presence")
    hits = 0
    out = []
    for q in pqs:
        q = dict(q)
        if old in (q.get("marks") or ""):
            q["marks"] = q["marks"].replace(old, new)
            hits += 1
        out.append(q)
    assert hits == 1, "R1 L1 practice_questions: %d hits" % hits
    return out, "practice_questions[marks]: grief-to-joy -> longing-to-presence"


def r1_l1_fc(fcs):
    tgt_q = ("What does the volta 'I do not think of thee — I am too near "
             "thee' reject?")
    hits = 0
    out = []
    for c in fcs:
        c = dict(c)
        if c.get("q") == tgt_q:
            c["q"] = ("What does the volta 'Rather, instantly / Renew thy "
                      "presence' reject?")
            c["a"] = "Idealised fantasy — in favour of his real presence."
            hits += 1
        out.append(c)
    assert hits == 1, "R1 L1 flashcards: %d hits" % hits
    return out, "flashcard: volta quotation corrected to the line-7/8 turn"


def r1_l8_fc(fcs):
    tgt_q = "Give a short Barrett Browning quotation marking her Sonnet 29 volta."
    hits = 0
    out = []
    for c in fcs:
        c = dict(c)
        if c.get("q") == tgt_q:
            assert c["a"] == ("'I do not think of thee — I am too near "
                              "thee.'"), c["a"]
            c["a"] = ("'Rather, instantly / Renew thy presence' — the "
                      "volta; the poem then closes 'I do not think of thee "
                      "— I am too near thee.'")
            hits += 1
        out.append(c)
    assert hits == 1, "R1 L8 flashcards: %d hits" % hits
    return out, "flashcard: volta answer now the real turn, close kept"


def r2_l3_pq(pqs):
    old = "Nature imagery, synaesthesia, rhetorical question."
    new = ("Nature imagery, the tapped-out signal of the souls, rhetorical "
           "question.")
    hits = 0
    out = []
    for q in pqs:
        q = dict(q)
        if old in (q.get("marks") or ""):
            q["marks"] = q["marks"].replace(old, new)
            hits += 1
        out.append(q)
    assert hits == 1, "R2 L3 practice_questions: %d hits" % hits
    return out, "practice_questions[5] mark scheme: synaesthesia label removed"


def r4_l6_fc(fcs):
    tgt_q = "What effect does caesura create in Hardy's 'Neutral Tones'?"
    hits = 0
    out = []
    for c in fcs:
        c = dict(c)
        if c.get("q") == tgt_q:
            c["q"] = ("What effect does caesura create in Armitage's 'Mother, "
                      "any distance'?")
            c["a"] = ("Mid-line full stops stop the line dead — 'years "
                      "between us. Anchor. Kite.' — holding the two "
                      "figures apart.")
            hits += 1
        out.append(c)
    assert hits == 1, "R4 L6 flashcards: %d hits" % hits
    return out, "flashcard: caesura example replaced with a real caesura"


def r5_l6_fc(fcs):
    tgt_q = "Which poem uses a cyclical structure to show entrapment?"
    hits = 0
    out = []
    for c in fcs:
        c = dict(c)
        if c.get("q") == tgt_q:
            assert c["a"].startswith("Mew's"), c["a"]
            c["a"] = ("Byron's 'When We Two Parted' — the ending returns "
                      "to the opening 'silence and tears'.")
            hits += 1
        out.append(c)
    assert hits == 1, "R5 L6 flashcards: %d hits" % hits
    return out, "flashcard: cyclical poem aligned with L1/L3 (Byron)"


def r6_l7_kc(kcs):
    i = 2
    old = kcs[i]
    assert old["q"] == ("The named poem is printed (_____ book), but the "
                        "comparison poem must be recalled from memory."), old
    out = [dict(k) for k in kcs]
    out[i] = {
        "q": ("AQA English Literature is a _____ book exam — the named "
              "poem is reproduced on the paper, but your comparison poem must "
              "come from memory."),
        "type": "fill",
        "correct": 1,
        "options": ["open", "closed", "partially open", "digital"],
    }
    return out, "knowledge_checks[2]: answer is now 'closed'"


def r8_l1_kc(kcs):
    i = 2
    old = kcs[i]
    assert old["q"].startswith("Barrett Browning uses an extended _____"), old
    out = [dict(k) for k in kcs]
    out[i] = {
        "q": ("Barrett Browning introduces the vine/tree comparison with the "
              "word 'as', which makes that line, strictly, a _____."),
        "type": "fill",
        "correct": 1,
        "options": ["allegory", "simile", "symbol", "personification"],
    }
    return out, "knowledge_checks[2]: 'as' makes it a simile"


JSON_EDITS = [
    (1, "practice_questions", r1_l1_pq, "R1"),
    (1, "flashcard_questions", r1_l1_fc, "R1"),
    (8, "flashcard_questions", r1_l8_fc, "R1"),
    (3, "practice_questions", r2_l3_pq, "R2"),
    (6, "flashcard_questions", r4_l6_fc, "R4"),
    (6, "flashcard_questions", r5_l6_fc, "R5"),
    (7, "knowledge_checks", r6_l7_kc, "R6"),
    (1, "knowledge_checks", r8_l1_kc, "R8"),
]

# ---- RULING 9: Cecil Day Lewis -> Cecil Day-Lewis, every field, 19x --------
NAME_OLD = "Day Lewis"
NAME_NEW = "Day-Lewis"

ENTITY = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#\d{1,7}|#[xX][0-9a-fA-F]{1,6});")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = get("lessons?unit_id=eq.%s&select=%s&order=lesson_number" % (UNIT_ID, COLS))
    by_num = {r["lesson_number"]: r for r in rows}
    print("fetched %d lessons" % len(rows))

    new_vals = {n: {} for n in by_num}          # lesson_number -> field -> value
    notes = {n: [] for n in by_num}
    name_counts = {}

    def cur(n, f):
        return new_vals[n].get(f, by_num[n][f])

    # 1) HTML exact-string edits
    for n, field, find, repl, want, ruling in HTML_EDITS:
        s = cur(n, field)
        got = s.count(find)
        if got != want:
            raise SystemExit("ABORT %s: L%d %s expected %d of %r, found %d"
                             % (ruling, n, field, want, find[:80], got))
        new_vals[n][field] = s.replace(find, repl)
        notes[n].append("%s (%s)" % (ruling, field))
        print("  ok  %-18s L%d %s" % (ruling, n, field))

    # 2) JSON structural edits
    for n, field, fn, ruling in JSON_EDITS:
        val = cur(n, field)
        out, note = fn(val)
        new_vals[n][field] = out
        notes[n].append("%s %s: %s" % (ruling, field, note))
        print("  ok  %-18s L%d %s  %s" % (ruling, n, field, note))

    # 3) RULING 9 - global name fix, every field type, after all other edits
    total_names = 0
    for n in by_num:
        for f in STR_FIELDS:
            s = cur(n, f)
            if s and NAME_OLD in s:
                c = s.count(NAME_OLD)
                new_vals[n][f] = s.replace(NAME_OLD, NAME_NEW)
                total_names += c
                name_counts["L%d.%s" % (n, f)] = c
        for f in JSON_FIELDS:
            v = cur(n, f)
            if v is None:
                continue
            blob = json.dumps(v, ensure_ascii=False)
            if NAME_OLD in blob:
                c = blob.count(NAME_OLD)
                new_vals[n][f] = json.loads(blob.replace(NAME_OLD, NAME_NEW))
                total_names += c
                name_counts["L%d.%s" % (n, f)] = c
    print("  ok  R9                 %d occurrences of %r -> %r"
          % (total_names, NAME_OLD, NAME_NEW))
    if total_names != 19:
        raise SystemExit("ABORT R9: expected 19 occurrences, found %d" % total_names)
    for k in sorted(name_counts):
        notes[int(k.split(".")[0][1:])].append("R9 %s x%d" % (k.split(".")[1], name_counts[k]))

    # 4) entity gate on plain-text fields BEFORE writing
    for n, fields in new_vals.items():
        for f, v in fields.items():
            if f in JSON_FIELDS or f == "description":
                blob = json.dumps(v, ensure_ascii=False) if f in JSON_FIELDS else v
                m = ENTITY.search(blob)
                if m:
                    raise SystemExit("ABORT: HTML entity %r in L%d %s" % (m.group(0), n, f))

    touched = {n: f for n, f in new_vals.items() if f}
    print("\n%d lessons touched, %d field-writes"
          % (len(touched), sum(len(f) for f in touched.values())))

    if args.dry_run:
        print("DRY RUN - nothing written")
        return

    # 5) BACKUP BEFORE THE FIRST WRITE
    backup = {
        "unit": "english-literature-aqa/love-and-relationships",
        "unit_id": UNIT_ID,
        "purpose": "pre-adjudication values for the nine adjudicated rulings",
        "created": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                               __import__("time").gmtime()),
        "lessons": [],
    }
    for n in sorted(touched):
        row = by_num[n]
        backup["lessons"].append({
            "lesson_number": n,
            "id": row["id"],
            "title": row["title"],
            "rulings": notes[n],
            "before": {f: row[f] for f in touched[n]},
        })
    with open(BACKUP, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, indent=1)
    print("backup written -> %s" % BACKUP)

    # 6) PATCH
    for n in sorted(touched):
        patch(by_num[n]["id"], touched[n])
        print("  PATCHED L%d  fields: %s" % (n, ", ".join(sorted(touched[n]))))

    # 7) verify
    print("\n=== VERIFY (re-fetch) ===")
    after = {r["lesson_number"]: r
             for r in get("lessons?unit_id=eq.%s&select=%s&order=lesson_number"
                          % (UNIT_ID, COLS))}
    bad = 0
    for n, field, find, repl, want, ruling in HTML_EDITS:
        s = after[n][field]
        if find in s or repl not in s:
            print("  FAIL %s L%d %s" % (ruling, n, field)); bad += 1
        else:
            print("  ok   %s L%d %s: old gone, new present" % (ruling, n, field))
    # name fix
    resid = 0
    hyph = 0
    for n, r in after.items():
        for f in STR_FIELDS + JSON_FIELDS:
            v = r.get(f)
            if v is None:
                continue
            blob = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            resid += len(re.findall(r"Day Lewis", blob))
            hyph += len(re.findall(r"Day-Lewis", blob))
    print("  R9: 'Day Lewis' residual=%d, 'Day-Lewis'=%d" % (resid, hyph))
    if resid or hyph != 19:
        bad += 1
    # suspect strings
    SUSPECT = ["despair to joy", "grief into joy", "grief to joy",
               "synaesthesia", "moonlit description",
               "We stood by a pond that winter day,” pauses",
               "Mew's 'The Farmer's Bride' (circular",
               "open book</strong> (printed)", "others may print neither",
               "The named poem is printed (_____ book)"]
    for n, r in after.items():
        blob = "".join((r.get(f) or "") for f in STR_FIELDS)
        blob += json.dumps([r.get(f) for f in JSON_FIELDS], ensure_ascii=False)
        for s in SUSPECT:
            if s in blob:
                print("  FAIL residual suspect string in L%d: %r" % (n, s)); bad += 1
    # entity gate live
    ents = 0
    for n, r in after.items():
        for f in JSON_FIELDS + ["description"]:
            v = r.get(f)
            if v is None:
                continue
            blob = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            ents += len(ENTITY.findall(blob))
    print("  entities in plain-text fields: %d" % ents)
    if ents:
        bad += 1
    print("\n%s" % ("VERIFY FAILED (%d)" % bad if bad else "VERIFY PASSED"))


if __name__ == "__main__":
    main()
