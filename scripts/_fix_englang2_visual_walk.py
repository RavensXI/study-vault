"""Repair the data faults the visual walk found in Edexcel English Language 2.0 (22 Sep 2026).

Renderer faults (five-way sorts drawn as blank circles, false coloured amber, paragraphs
folded into one block, a highlighter that loses paragraph breaks, stray gaps in
spot-the-error sentences, one passage for a two-text comparison) are fixed in
practice.html. This script fixes what only the data can:

  STEM      69 questions whose stem is the placeholder "Answer using the extract."
            Opus returned those four types with no stem at all and build.py's
            normaliser filled the gap with that line; the connotation questions also
            lost their target word, recovered here from the raw batch output.
  TWO_WAY   17 true/false questions whose stem promised a third "partly true" choice.
            Rewritten to two-way: offering "partly true" over statements written as
            clear-cut would make the marking arguable, which is worse than no choice.
  PASSAGE   14 questions about "Model B" shown beside Model A, re-pointed at the model
            they name.
  PAIR      6 comparison questions now carry both passages (passage_ids), relettered
            where a lesson labelled every tier's passage "Source A".
  ONE_OFF   individual faults, each described where it is fixed.

  python scripts/_fix_englang2_visual_walk.py            # dry run: prints every change
  python scripts/_fix_englang2_visual_walk.py --apply
Backup of the untouched data: scripts/_backup_englang2_practice_2026-09-22.json
"""
import importlib.util, io, json, os, re, sys, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
SID = "b6ecfffe-69da-4f15-9bb4-b69e4f54edc8"
PLACEHOLDER = "Answer using the extract."
RAW = os.path.join(HERE, "_build_englang2", "_out", "s4.json")

spec = importlib.util.spec_from_file_location("faults", os.path.join(HERE, "_qa_englang_faults.py"))
faults = importlib.util.module_from_spec(spec); spec.loader.exec_module(faults)

# ---- TWO_WAY: the stem each three-way promise becomes (lesson, tier, stored index)
TWO_WAY = {
    ("paper-1-reading/6", "gold", 3): "Decide whether each statement about the writer's methods is true or false.",
    ("paper-1-reading/4", "bronze", 3): "Decide whether each statement about the letter is true (green) or false (red).",
    ("paper-1-reading/9", "bronze", 2): "Read the following statements about the letter and decide whether each one is true (green) or false (red), based on the text.",
    ("paper-1-reading/11", "gold", 4): "Decide whether each statement about the writer's techniques is true or false, based on the passage.",
    ("paper-1-reading/7", "bronze", 3): "Read the following statements about Hartley's letter. Sort each one into green (true) or red (false).",
    ("paper-1-reading/8", "bronze", 3): "Read each statement about the letter and decide whether it is true (green) or false (red).",
    ("paper-1-reading/12", "bronze", 3): "Read these statements about Ellen's letter. Decide whether each one is true (green) or false (red), based on the text.",
    ("paper-1-reading/13", "bronze", 5): "Read the following statements about the letter and decide whether each one is true or false.",
    ("paper-2-reading/6", "gold", 1): "Decide whether each statement about the writer's use of language and structure is true (green) or false (red).",
    ("paper-2-reading/6", "bronze", 4): "Read the following statements about the extract and decide whether each one is true (green) or false (red).",
    ("paper-2-reading/12", "bronze", 3): "Read each statement about the woman sitting beside the narrator. Decide whether it is true or false.",
    ("paper-2-reading/1", "bronze", 3): "Read these statements about the extract and decide whether each one is true (green) or false (red).",
    ("paper-2-reading/3", "gold", 1): "Assess whether each analytical statement about the passage is true or false.",
    ("paper-2-reading/3", "silver", 3): "Decide whether each statement about the writer's language and structure is true or false.",
    ("paper-2-reading/5", "bronze", 3): "Decide whether each statement about the woman behind the counter is true or false, based on the extract.",
    ("paper-2-reading/9", "bronze", 2): "Decide whether each statement about the passage is true or false.",
    ("paper-2-reading/9", "silver", 3): "Decide whether each statement about the passage is true or false.",
}

# ---- PAIR: comparison questions and the two passages each needs, in the order it names them
PAIR = {
    ("paper-1-writing/10", "silver", 4): (["silver", "gold"], None, None),
    ("paper-1-writing/11", "bronze", 5): (["bronze", "silver"], None, None),
    ("paper-1-writing/11", "silver", 3): (["bronze", "silver"], None, None),
    ("paper-2-reading/10", "gold", 4): (["gold", "silver"], None, None),
    # every tier's passage is labelled "Source A" in these two; the question calls the second one B
    ("paper-2-reading/9", "gold", 4): (["gold", "bronze"], ["Source A", "Source B"], None),
    ("paper-2-reading/12", "gold", 4): (["gold", "silver"], ["Source A", "Source B"],
        # and it told students about "the gold passage above", a name only the build uses
        ("Source A (the gold passage above) and Source B (the silver passage above)",
         "Source A (Priya Chakrabarti's short story) and Source B (Marcus Obi's newspaper reportage)")),
}

# ---- ONE_OFF: (lesson, tier, index) -> (what is wrong, function applying the fix)
def _stem(new):
    def f(q): q["question"] = new
    return f

def _replace(old, new):
    def f(q):
        assert old in q["question"], "expected text not found: %r" % old
        q["question"] = q["question"].replace(old, new)
    return f

def _proofread_tokens(q):
    """One chunk had swallowed "Many student's" and the error "loose" sat in the wrong
    place, so the sentence read "Many student's student's loose marks because loose of"."""
    old = {t["text"].strip(): t for t in q["tokens"] if t.get("error")}
    def err(text, key):
        t = dict(old[key]); t["text"] = text; return t
    q["tokens"] = [
        err("Its ", "Its"),
        {"text": "important to proofread ", "error": False},
        err("you're ", "you're"),
        {"text": "work before handing it in. Many ", "error": False},
        err("student's ", "student's"),
        err("loose ", "loose"),
        {"text": "marks because of basic errors that ", "error": False},
        err("could of ", "could of"),
        {"text": "been avoided.", "error": False},
    ]

ONE_OFF = {
    ("paper-1-writing/7", "bronze", 3): ("an open question over tick-box chips",
        _stem("Model A uses the formal phrase 'adequate sustenance' where an informal writer might say 'enough to eat'. Which of these explain the writer's choice?")),
    ("paper-2-writing/11", "silver", 5): ("asks for a comparison with a first draft that is never shown",
        _stem("What specific features suggest this darkroom extract has been carefully edited, rather than left as a first draft? Identify at least three signs of revision.")),
    ("paper-2-reading/9", "silver", 5): ("asks the student to 'identify which is which' when the control is click-the-misleading-ones",
        _stem("One of these summaries accurately describes how the writer structures the passage. The other two contain a misleading element. Click the two misleading summaries.")),
    ("paper-1-reading/4", "gold", 4): ("asks for TWO quotations when the highlighter checks one",
        _stem("The final paragraph of Source C is structured around a contrast between what the writer does NOT want and what he DOES want. Highlight the sentence where he states what he does NOT want.")),
    ("paper-2-writing/10", "bronze", 1): ("sentence repeats 'student's' and misplaces 'loose'", _proofread_tokens),
    ("paper-1-writing/1", "silver", 6): ("says the error is about audience; the wrong phrase is about tone",
        _replace("an error about audience", "an error about tone")),
    ("paper-1-writing/10", "bronze", 4): ("calls 'companys' an apostrophe error; it is a plural spelling",
        _replace("the apostrophe error", "the plural spelling error")),
}


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())


def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()


def raw_words():
    """Target word of every raw connotation question, keyed by its option texts."""
    out = {}
    d = json.load(io.open(RAW, encoding="utf-8"))
    for key, tiers in d.items():
        for tier, qs in tiers.items():
            for q in qs if isinstance(qs, list) else []:
                if (q.get("input_type") or q.get("type")) == "connotation_picker" and q.get("word"):
                    out[frozenset(str(o).strip() for o in (q.get("options") or []))] = q["word"]
    return out


def placeholder_stem(q, words):
    t = q.get("input_type")
    if t == "traffic_light":
        cats = sorted({str(s.get("correct")) for s in q.get("statements") or []})
        neg = [c for c in cats if re.search(r"\b(not|false|incorrect|unsupported)\b", c, re.I)]
        pos = [c for c in cats if c not in neg]
        if len(cats) == 2 and len(neg) == 1:
            # name the two labels the legend will show, in the colours it will show them
            return "Decide whether each statement about the extract is %s (green) or %s (red)." % (pos[0], neg[0])
        return None
    if t == "evidence_match":
        return "Match each claim about the extract to the quotation that supports it."
    if t == "misleading_summary":
        parts = [p for p in q.get("summaryParts") or [] if isinstance(p, dict) and "wrong" in p]
        wrong = sum(1 for p in parts if p.get("wrong"))
        if parts and wrong == len(parts) - 1:
            return "Only one of these summaries is accurate. Click each summary that misreads the extract."
        return "Some of these summaries misread the extract. Click each one that is misleading."
    if t == "connotation_picker":
        w = words.get(frozenset(str(c.get("text")).strip() for c in q.get("chips") or []))
        if not w:
            return None
        q["word"] = w
        return "What does the writer's choice of the word '%s' suggest? Select every connotation that applies." % w
    return None


def main():
    apply = "--apply" in sys.argv
    rows = get("lessons?select=id,lesson_number,status,practice_data,units!inner(slug,subject_id)"
               "&units.subject_id=eq.%s&limit=200" % SID)
    by_key = {"%s/%s" % (r["units"]["slug"], r["lesson_number"]): r for r in rows}
    found = faults.scan(rows)
    words = raw_words()
    changed, counts, problems = set(), {}, []

    def note(cls, key, tier, i, before, after):
        counts[cls] = counts.get(cls, 0) + 1
        changed.add(key)
        print("%-8s %-20s %-6s %-2d  %s\n%38s-> %s" % (cls, key, tier, i, before[:110], "", after[:110]))

    # STEM
    for key, r in by_key.items():
        for tier, qs in r["practice_data"]["problem_bank"].items():
            for i, q in enumerate(qs):
                if (q.get("question") or "").strip() == PLACEHOLDER:
                    new = placeholder_stem(q, words)
                    if not new:
                        problems.append("no stem written for %s %s[%d] %s" % (key, tier, i, q.get("input_type"))); continue
                    note("STEM", key, tier, i, q["question"], new)
                    q["question"] = new
    # TWO_WAY
    for (key, tier, i), new in TWO_WAY.items():
        q = by_key[key]["practice_data"]["problem_bank"][tier][i]
        assert faults.THREE_WAY.search(q["question"]), "not a three-way stem any more: %s %s[%d]" % (key, tier, i)
        note("TWO_WAY", key, tier, i, q["question"], new)
        q["question"] = new
    # PASSAGE
    for it in found.get("REF_OTHER", []):
        q = by_key[it["where"]]["practice_data"]["problem_bank"][it["tier"]][it["i"]]
        note("PASSAGE", it["where"], it["tier"], it["i"], "passage %s (%s): %s" % (q.get("passage_id"), it["own"], q["question"][:60]),
             "passage %s (Model/Source %s)" % (it["should"], it["named"]))
        q["passage_id"] = it["should"]
    # PAIR
    for (key, tier, i), (ids, as_, reword) in PAIR.items():
        q = by_key[key]["practice_data"]["problem_bank"][tier][i]
        before = "passage %s: %s" % (q.get("passage_id"), q["question"][:70])
        q["passage_id"] = ids[0]
        q["passage_ids"] = ids
        if as_: q["passage_as"] = as_
        if reword:
            assert reword[0] in q["question"], "expected text not found in %s %s[%d]" % (key, tier, i)
            q["question"] = q["question"].replace(*reword)
        note("PAIR", key, tier, i, before, "passages %s%s%s" % ("+".join(ids), " as " + "/".join(as_) if as_ else "",
                                                               " | " + q["question"][:60] if reword else ""))
    # ONE_OFF
    for (key, tier, i), (why, fix) in ONE_OFF.items():
        q = by_key[key]["practice_data"]["problem_bank"][tier][i]
        before = q.get("question") or ""
        if q.get("input_type") == "spot_error":
            before += "  [" + "".join(t["text"] for t in q["tokens"]) + "]"
        fix(q)
        after = q.get("question") or ""
        if q.get("input_type") == "spot_error":
            after += "  [" + "".join(t["text"] for t in q["tokens"]) + "]"
        note("ONE_OFF", key, tier, i, before, after + "   (" + why + ")")

    print("\n" + " | ".join("%s %d" % kv for kv in counts.items()), "| lessons touched:", len(changed))
    for p in problems:
        print("  !!", p)
    if not apply:
        print("dry run — nothing written; add --apply"); return
    if problems:
        print("refusing to write with unresolved problems above"); return
    for key in sorted(changed):
        r = by_key[key]
        patch("lessons?id=eq." + r["id"], {"practice_data": r["practice_data"]})
    print("written: %d lessons" % len(changed))


if __name__ == "__main__":
    main()
