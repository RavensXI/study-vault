"""Give live English Language questions the texts they are about (22 Sep 2026).

Found while fixing Edexcel English Language 2.0: the same faults are live in every
English Language subject.

  PAIR      a comparison question ("Compare how the writers of Source B and Source C...")
            showed only one of the two texts. It now carries passage_ids, and
            practice.html shows both, each under its own label. A highlight question
            keeps the text it highlights in inline and gets the other text in the panel.
  PASSAGE   a question about "Model B" / "Source B" was attached to a different text.
  TWO_WAY   a three-way stem ("supported, partially supported or not supported") over
            two-way answers.

Nothing is guessed: a question naming a letter the lesson does not have, or a highlight
whose answer is not found verbatim in any named text, is reported and left alone.

  python scripts/_fix_englang_live_passages.py            # dry run
  python scripts/_fix_englang_live_passages.py --apply    # backs up every lesson it touches
"""
import io, json, os, re, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = ["english-language-edexcel", "english-language-aqa", "english-language-ocr",
            "english-language-eduqas", "english-language"]
BACKUP = os.path.join(HERE, "_backup_englang_live_passages_%s.json" % time.strftime("%Y-%m-%d"))
if "--subject" in sys.argv:
    SUBJECTS = [sys.argv[sys.argv.index("--subject") + 1]]
    BACKUP = BACKUP.replace(".json", "_%s.json" % SUBJECTS[0])
LABEL = re.compile(r"\b(Model|Source|Extract|Text)\s+([A-E])\b")
NAMES = re.compile(r"\b(?:Model|Source|Extract|Text|Draft)s?\s+([A-E](?:\s*(?:,|and|&|or)\s*[A-E])*)\b")
SOLO = re.compile(r"\bONLY this (passage|extract|text)\b|a second text you have read", re.I)
THREE_WAY = re.compile(r"\bpartly\b|\bpartially\b|\bamber\b", re.I)


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())


def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()


def letters_in(stem):
    out = []
    for m in NAMES.finditer(stem or ""):
        for L in re.findall(r"[A-E]", m.group(1)):
            if L not in out:
                out.append(L)
    return out


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[‘’']", "'", s or "")).strip().lower()


def two_way(stem, cats):
    """Rewrite the three-way promise to name the two categories the answers use."""
    neg = [c for c in cats if re.search(r"\b(not|false|incorrect|unsupported)\b", c, re.I)]
    pos = [c for c in cats if c not in neg]
    if len(cats) != 2 or len(neg) != 1:
        return None
    new = re.sub(r"(is\s+)?(fully\s+)?%s(,)?\s*(partly|partially)\s+\w+(,)?\s*(or\s+)?%s" % (re.escape(pos[0]), re.escape(neg[0])),
                 lambda m: (m.group(1) or "") + pos[0] + " or " + neg[0], stem, flags=re.I)
    return new if new != stem else None


def main():
    apply = "--apply" in sys.argv
    backup, touched, skipped, counts = {}, {}, [], {}

    def note(cls, where, tier, i, before, after):
        counts[cls] = counts.get(cls, 0) + 1
        print("%-8s %-44s %-6s %-2d %s\n%66s-> %s" % (cls, where, tier, i, before[:96], "", after[:96]))

    for sub in SUBJECTS:
        sid = get("subjects?select=id&slug=eq." + sub)[0]["id"]
        rows = get("lessons?select=id,lesson_number,status,practice_data,units!inner(slug,subject_id)"
                   "&units.subject_id=eq.%s&limit=500" % sid)
        for r in rows:
            pd = r["practice_data"] or {}
            passages = [p for p in pd.get("passages") or [] if isinstance(p, dict)]
            by_letter = {}
            for p in passages:
                m = LABEL.search(p.get("label") or "")
                if m and m.group(2) not in by_letter:
                    by_letter[m.group(2)] = p["id"]
            text_of = {p["id"]: p.get("text") or "" for p in passages}
            letter_of = {v: k for k, v in by_letter.items()}
            where = "%s/%s/%s" % (sub, r["units"]["slug"], r["lesson_number"])
            before_pd = json.dumps(pd, ensure_ascii=False)
            for tier, qs in (pd.get("problem_bank") or {}).items():
                for i, q in enumerate(qs if isinstance(qs, list) else []):
                    if not isinstance(q, dict):
                        continue
                    stem, t = q.get("question") or "", q.get("input_type")
                    # TWO_WAY
                    if t == "traffic_light" and THREE_WAY.search(stem) and not q.get("categories"):
                        cats = []
                        for s in q.get("statements") or []:
                            c = s.get("correct") if isinstance(s, dict) else None
                            if isinstance(c, str) and c not in cats:
                                cats.append(c)
                        if len(cats) < 3:
                            new = two_way(stem, cats)
                            if new:
                                note("TWO_WAY", where, tier, i, stem, new); q["question"] = new
                            else:
                                skipped.append("%s %s[%d] three-way stem, could not rewrite: %s" % (where, tier, i, stem[:80]))
                    if SOLO.search(stem) or q.get("passage_ids"):
                        continue
                    named = letters_in(stem)
                    if not named:
                        continue
                    missing = [L for L in named if L not in by_letter]
                    if missing:
                        skipped.append("%s %s[%d] names %s, lesson has %s: %s" % (where, tier, i, "".join(missing), "".join(sorted(by_letter)), stem[:70]))
                        continue
                    ids = [by_letter[L] for L in named]
                    own = q.get("passage_id")
                    if t == "highlight_evidence":
                        # the text to highlight in is the one that holds the answer
                        ans = norm(q.get("answer_text") or q.get("answerText") or "")
                        home = [pid for pid in ids if ans and ans in norm(text_of.get(pid))]
                        if len(home) != 1:
                            if len(named) > 1 or own not in ids:
                                skipped.append("%s %s[%d] highlight answer found in %d named texts: %s" % (where, tier, i, len(home), stem[:70]))
                            continue
                        if len(named) > 1:
                            q["passage_id"] = home[0]; q["passage_ids"] = ids
                            note("PAIR", where, tier, i, "highlight in %s, alone: %s" % (letter_of.get(own), stem),
                                 "highlight in %s, beside %s" % (letter_of[home[0]], "+".join(letter_of[x] for x in ids if x != home[0])))
                        elif own != home[0]:
                            q["passage_id"] = home[0]
                            note("PASSAGE", where, tier, i, "text %s: %s" % (letter_of.get(own), stem), "text %s" % letter_of[home[0]])
                        continue
                    if len(named) > 1:
                        q["passage_ids"] = ids
                        if own not in ids:
                            q["passage_id"] = ids[0]
                        note("PAIR", where, tier, i, "text %s: %s" % (letter_of.get(own), stem), "texts %s" % "+".join(named))
                    elif own != ids[0]:
                        q["passage_id"] = ids[0]
                        note("PASSAGE", where, tier, i, "text %s: %s" % (letter_of.get(own), stem), "text %s" % named[0])
            if json.dumps(pd, ensure_ascii=False) != before_pd:
                backup[r["id"]] = json.loads(before_pd)
                touched[r["id"]] = (where, pd)

    print("\n" + " | ".join("%s %d" % kv for kv in sorted(counts.items())), "| lessons touched:", len(touched))
    if skipped:
        print("\nleft alone (%d):" % len(skipped))
        for s in skipped:
            print("  - " + s)
    if not apply:
        print("\ndry run — nothing written; add --apply"); return
    io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
    for lid, (where, pd) in touched.items():
        patch("lessons?id=eq." + lid, {"practice_data": pd})
    print("backup: %s\nwritten: %d lessons" % (BACKUP, len(touched)))


if __name__ == "__main__":
    main()
