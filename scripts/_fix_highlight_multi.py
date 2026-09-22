"""Highlight questions that ask for two or three quotations (22 Sep 2026).

The highlighter takes ONE continuous stretch. 39 English Language 2.0 questions and 8 live
ones ask for "TWO quotations" or "THREE details", and the 2.0 build kept only the first of
the several answers the model wrote (build.py's normaliser), so a student who highlighted
the second good quotation was marked wrong. The student walk found it: its student joined
two quotations with a slash, because the question asked for two.

  1. answer_texts: every acceptable answer the model wrote is restored (practice.html now
     marks against any of them).
  2. the stem is reworded to ask for one — unless a single stored answer is itself a
     continuous stretch that already satisfies the plural ("the two consecutive sentences").
     A model makes that call per question; every rewrite is printed for review.

  python scripts/_fix_highlight_multi.py submit     # batch the stem decisions
  python scripts/_fix_highlight_multi.py plan       # collect, print every change
  python scripts/_fix_highlight_multi.py apply      # write, with a backup
"""
import io, json, os, re, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "_studentwalk", "hl_multi_state.json")
RAW = [os.path.join(HERE, "_build_englang2", "_out", s + ".json") for s in ("s3", "s4")]
SUBJECTS = ["english-language-2-edexcel", "english-language-edexcel", "english-language-aqa",
            "english-language-ocr", "english-language-eduqas", "english-language"]
MULTI = re.compile(r"\b(two|both|three|four|each side|one for each|pair of|two separate)\b[^.?]{0,40}\b(phrases?|quotations?|quotes?|words|details|sentences|examples|images)\b"
                   r"|\b(phrases?|quotations?|quotes?|details|examples)\b[^.?]{0,25}\b(for each|from each)\b", re.I)
SYSTEM = """You edit GCSE English practice questions. On this website a highlight question lets the student
highlight ONE continuous stretch of the passage, and the answer is checked against the stored answers.

You get a question that asks for more than one quotation, phrase or detail, and its stored answers.

- If ONE of the stored answers is itself a single continuous stretch that fully satisfies the question
  as worded (e.g. "the two consecutive sentences" and the answer is those two sentences together),
  reply {"action": "keep"}.
- Otherwise rewrite the question to ask for ONE quotation / phrase / detail that does what the original
  asks. Change as little as possible: keep its focus, its wording and its capitalisation style; fix the
  grammar that follows (e.g. "that show" -> "that shows"). Do not mention the website or highlighting
  rules. Reply {"action": "rewrite", "stem": "<the new question>"}.

Reply with the JSON object only."""


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=240).read())


def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()


def raw_answers():
    out = {}
    for path in RAW:
        d = json.load(io.open(path, encoding="utf-8"))
        for key, tiers in d.items():
            for tier, qs in tiers.items():
                for q in qs if isinstance(qs, list) else []:
                    if (q.get("input_type") or q.get("type")) == "highlight_evidence":
                        a = q.get("answers")
                        if isinstance(a, list) and len(a) > 1:
                            out[(key, q.get("question") or q.get("instruction") or "")] = [str(x) for x in a]
    return out


def targets():
    raw = raw_answers()
    out = []
    for sub in SUBJECTS:
        sid = get("subjects?select=id&slug=eq." + sub)[0]["id"]
        rows = get("lessons?select=id,lesson_number,status,practice_data,units!inner(slug,subject_id)&units.subject_id=eq.%s&limit=500" % sid)
        for r in rows:
            lk = "%s/%s" % (r["units"]["slug"], r["lesson_number"])
            for t, qs in (r["practice_data"].get("problem_bank") or {}).items():
                for i, q in enumerate(qs if isinstance(qs, list) else []):
                    if q.get("input_type") != "highlight_evidence": continue
                    stem = q.get("question") or ""
                    alts = raw.get((lk, stem)) if sub == "english-language-2-edexcel" else None
                    if MULTI.search(stem) or alts:
                        out.append({"id": "%s/%s/%s/%d" % (sub, lk, t, i), "lesson_id": r["id"], "tier": t, "i": i,
                                    "stem": stem, "answers": alts or q.get("answer_texts") or [q.get("answer_text") or ""],
                                    "multi_ask": bool(MULTI.search(stem))})
    return out


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    st = json.load(io.open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    if cmd == "submit":
        import anthropic
        tg = targets()
        reqs = [{"custom_id": "h%04d" % n, "params": {"model": "claude-sonnet-5", "max_tokens": 4000,
                 "thinking": {"type": "adaptive"}, "output_config": {"effort": "medium"}, "system": SYSTEM,
                 "messages": [{"role": "user", "content": "QUESTION:\n%s\n\nSTORED ANSWERS:\n%s" % (x["stem"], "\n".join("- " + a for a in x["answers"]))}]}}
                for n, x in enumerate(tg) if x["multi_ask"]]
        b = anthropic.Anthropic().messages.batches.create(requests=reqs)
        st = {"batch": b.id, "targets": tg, "ids": {("h%04d" % n): x["id"] for n, x in enumerate(tg) if x["multi_ask"]}}
        io.open(STATE, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))
        print("submitted", b.id, len(reqs), "stems;", sum(1 for x in tg if len(x["answers"]) > 1), "questions get their alternative answers back")
        return
    import anthropic
    cl = anthropic.Anthropic()
    b = cl.messages.batches.retrieve(st["batch"])
    if b.processing_status != "ended":
        print("batch", b.processing_status, b.request_counts); return
    decisions = {}
    for r in cl.messages.batches.results(b.id):
        if r.result.type != "succeeded": continue
        m = re.search(r"\{.*\}", "".join(x.text for x in r.result.message.content if x.type == "text"), re.S)
        if m: decisions[st["ids"][r.custom_id]] = json.loads(m.group(0))
    by_lesson = {}
    for x in st["targets"]:
        by_lesson.setdefault(x["lesson_id"], []).append(x)
    changes = 0
    backup = {}
    for lid, xs in by_lesson.items():
        pd = get("lessons?select=practice_data&id=eq." + lid)[0]["practice_data"]
        before = json.dumps(pd, ensure_ascii=False)
        for x in xs:
            q = pd["problem_bank"][x["tier"]][x["i"]]
            assert (q.get("question") or "") == x["stem"], "stem changed since submit: " + x["id"]
            if len(x["answers"]) > 1 and q.get("answer_texts") != x["answers"]:
                q["answer_texts"] = x["answers"]
                print("ANSWERS  %-62s %d acceptable answers" % (x["id"], len(x["answers"])))
                changes += 1
            d = decisions.get(x["id"])
            if d and d.get("action") == "rewrite" and d.get("stem"):
                print("STEM     %-62s\n         %s\n      -> %s" % (x["id"], x["stem"], d["stem"]))
                q["question"] = d["stem"]; changes += 1
            elif d:
                print("KEEP     %-62s %s" % (x["id"], x["stem"][:80]))
        if json.dumps(pd, ensure_ascii=False) != before:
            backup[lid] = json.loads(before)
            if cmd == "apply":
                patch("lessons?id=eq." + lid, {"practice_data": pd})
    print("\n%d changes in %d lessons" % (changes, len(backup)))
    if cmd == "apply":
        path = os.path.join(HERE, "_backup_highlight_multi_%s.json" % time.strftime("%Y-%m-%d"))
        io.open(path, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
        print("written, backup:", path)
    else:
        print("plan only — run `apply` to write")


if __name__ == "__main__":
    main()
