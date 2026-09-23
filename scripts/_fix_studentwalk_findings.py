"""Fix the questions the student walk found faulty (23 Sep 2026).

The walk (scripts/_qa_student_walk.py) had a model answer every English Language 2.0
question blind, marked it through the page, and had Opus adjudicate every wrong verdict and
every written answer. 68 findings: key_wrong, ambiguous, unanswerable, marker_lenient,
marker_harsh. The page-side faults (highlight matching, the AI marker not seeing the text
beside the question) are fixed in practice.html; this fixes the question data.

For each finding Opus gets the stored question, the texts on screen, the adjudication and
how the page marks that question type, and returns the corrected question (same schema) or
"none". Every patch is checked mechanically before it is written.

  python scripts/_fix_studentwalk_findings.py submit
  python scripts/_fix_studentwalk_findings.py plan      # collect, validate, print every change
  python scripts/_fix_studentwalk_findings.py apply     # write, with a backup
"""
import io, json, os, re, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, "_studentwalk")
STATE = os.path.join(W, "fix_state.json")
KINDS = ("key_wrong", "ambiguous", "unanswerable", "marker_lenient", "marker_harsh")

SYSTEM = """You fix GCSE English Language practice questions on a revision website. A careful
review found a fault in the question below. Return the corrected question.

How the page shows and marks each question type (keep to these contracts exactly):
- highlight_evidence: the student highlights ONE continuous stretch of the passage. Correct when
  it covers 60% of an acceptable answer, or is a stretch of 3+ words wholly inside one.
  Acceptable answers: "answer_texts" (list) or "answer_text". Every acceptable answer MUST be
  copied verbatim from the passage. The stem must ask for ONE quotation/phrase/sentence.
- spot_error: "tokens" are shown in order as one text; each token is one clickable span.
  The student clicks every token with an error; exactly the tokens with "error": true must be
  clicked. Punctuation errors belong on the token that carries the punctuation (the word the
  comma is attached to). Every real error in the text must be keyed, and a token must not
  contain an error unless it is keyed. Each error token has "explain" and "correction".
- reorder: "items" shown shuffled; "correct_order" lists item indices in the right order.
- traffic_light: each statement is put in one category; "correct" names it. Categories come from
  "categories" if present, else the ones used in "correct". Each statement must fit ONE category
  only; the question may define the categories in its stem.
- misleading_summary: "summaryParts"; the student clicks every part with "wrong": true. Parts
  marked not wrong must be plainly accurate, with no absolutes or unsupported superlatives.
- evidence_match: each claim is matched to one quote; quote "correctClaim" is a claim index,
  -1 for a distractor. Each claim must fit one quote only.
- multiple_choice: "options", "solutions" (indices). Options must come from the text named.
- improve_sentence / ai_mark / ai_write: marked by an AI marker from the task, the
  model answer ("improved" / model fields) and any marking prompt. The marker also sees the
  text beside the question and gives no credit for copying it where own writing is asked for.

Rules:
- Fix what the review found, and anything else plainly wrong in this question. Change as little
  as possible; keep the wording style, the field names and every field you do not need to change.
- Where the student's answer was right, make the key accept it (add it as an acceptable answer,
  or correct the key). Where the question was unclear, make it clear.
- Plain text fields use unicode characters, not HTML entities.
- If no change to the question data would help (the fault was only in the page's marking, or
  the review is mistaken), reply "none".

Reply with JSON only:
{"action": "patch", "summary": "<one line: what changed>", "question": {<the whole corrected question>}}
or {"action": "none", "summary": "<why>"}"""


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=240).read())


def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()


def load(p, d=None):
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else d


def lesson(key, cache):
    lk = key.rsplit("/", 2)[0]
    if lk not in cache:
        sub, unit, ln = lk.split("/")
        cache[lk] = get("lessons?select=id,practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                        "&units.slug=eq.%s&lesson_number=eq.%s" % (sub, unit, ln))[0]
    return cache[lk]


def passages_for(q, pd):
    ids = list(q.get("passage_ids") or []) or ([q["passage_id"]] if q.get("passage_id") else [])
    ps = {p.get("id"): p for p in (pd.get("passages") or [])}
    out = [(ps[i].get("label") or i, ps[i].get("text") or "") for i in ids if i in ps]
    if q.get("passage"): out.append(("Source Text", q["passage"]))
    return out


def norm(s):
    return " ".join(re.sub(r"[^0-9a-z\u00c0-\u024f\s]", "", str(s).lower()).split())


def validate(old, new, texts):
    """Mechanical checks on a patched question; returns a list of problems."""
    errs = []
    if new.get("input_type") != old.get("input_type"): errs.append("input_type changed")
    t = new.get("input_type")
    whole = norm(" ".join(x for _, x in texts))
    if t == "highlight_evidence":
        ans = new.get("answer_texts") or [new.get("answer_text")]
        for a in ans:
            if not a or norm(a) not in whole: errs.append("answer not verbatim in passage: %r" % (a or "")[:80])
    if t == "spot_error":
        tk = new.get("tokens") or []
        if not tk or not any(x.get("error") for x in tk): errs.append("no error tokens")
        for x in tk:
            if x.get("error") and not (x.get("explain") and x.get("correction")): errs.append("error token lacks explain/correction")
    if t == "reorder":
        if sorted(new.get("correct_order") or []) != list(range(len(new.get("items") or []))): errs.append("correct_order not a permutation")
    if t == "multiple_choice":
        n = len(new.get("options") or [])
        if not new.get("solutions") or any(not (0 <= s < n) for s in new["solutions"]): errs.append("bad solutions")
    if t == "evidence_match":
        n = len(new.get("claims") or [])
        cc = [x.get("correctClaim") for x in new.get("quotes") or []]
        if any(c is None or c < -1 or c >= n for c in cc): errs.append("bad correctClaim")
        if sorted(c for c in cc if c >= 0) != list(range(n)): errs.append("claims not matched one-to-one")
    if t == "misleading_summary":
        if not any(x.get("wrong") for x in new.get("summaryParts") or []): errs.append("no wrong part")
    if t == "traffic_light":
        cats = new.get("categories")
        if cats:
            names = [c if isinstance(c, str) else (c.get("name") or c.get("label") or c.get("id")) for c in cats]
            for s in new.get("statements") or []:
                if s.get("correct") not in names: errs.append("statement category not in categories: %r" % s.get("correct"))
    if re.search(r"&(#\d+|[a-z]+);", json.dumps(new, ensure_ascii=False)): errs.append("HTML entity in plain text")
    return errs


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    import anthropic
    cl = anthropic.Anthropic()
    adj = load(os.path.join(W, "adjudications.json"))
    views = load(os.path.join(W, "views.json"))
    attempts = load(os.path.join(W, "attempts.json"))
    cache = {}
    if cmd == "submit":
        reqs, ids = [], {}
        for n, (k, a) in enumerate(sorted(adj.items())):
            if a.get("finding") not in KINDS: continue
            row = lesson(k, cache); pd = row["practice_data"]
            v = views[k]; q = pd["problem_bank"][v["tier"]][v["i"]]
            scheme = q.get("ai_system_prompt") or (pd.get("ai_marking_prompts") or {}).get(q.get("ai_prompt_key") or "")
            body = "\n\n".join(filter(None, [
                "\n\n".join("TEXT ON SCREEN — %s:\n%s" % (lab, txt) for lab, txt in passages_for(q, pd)),
                "STORED QUESTION:\n" + json.dumps(q, ensure_ascii=False, indent=1),
                ("AI MARKING PROMPT FOR THIS QUESTION:\n" + str(scheme)[:4000]) if scheme else "",
                "WHAT A STUDENT ANSWERED:\n" + json.dumps(attempts.get(k, {}).get("answer"), ensure_ascii=False)[:3000],
                "REVIEW: finding=%s\nWhy: %s\nSuggested fix: %s" % (a["finding"], a.get("why", ""), a.get("fix", ""))]))
            cid = "f%04d" % n; ids[cid] = k
            reqs.append({"custom_id": cid, "params": {"model": "claude-opus-5", "max_tokens": 32000,
                         "thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}, "system": SYSTEM,
                         "messages": [{"role": "user", "content": body}]}})
        b = cl.messages.batches.create(requests=reqs)
        io.open(STATE, "w", encoding="utf-8").write(json.dumps({"batch": b.id, "ids": ids}, indent=1))
        print("submitted", b.id, len(reqs), "questions")
        return

    st = load(STATE)
    b = cl.messages.batches.retrieve(st["batch"])
    if b.processing_status != "ended":
        print("batch", b.processing_status, b.request_counts); return
    out = {}
    for r in cl.messages.batches.results(b.id):
        k = st["ids"][r.custom_id]
        if r.result.type != "succeeded": out[k] = {"action": "error"}; continue
        txt = "".join(x.text for x in r.result.message.content if x.type == "text")
        m = re.search(r"\{.*\}", txt, re.S)
        try: out[k] = json.loads(m.group(0), strict=False)
        except Exception: out[k] = {"action": "unparseable", "summary": txt[:200]}
    by_lesson, counts, backup = {}, {}, {}
    for k in sorted(out): by_lesson.setdefault(k.rsplit("/", 2)[0], []).append(k)
    for lk, keys in by_lesson.items():
        row = lesson(keys[0], cache); pd = row["practice_data"]
        before = json.dumps(pd, ensure_ascii=False)
        for k in keys:
            d = out[k]; v = views[k]; act = d.get("action")
            old = pd["problem_bank"][v["tier"]][v["i"]]
            if act != "patch":
                counts[act] = counts.get(act, 0) + 1
                print("%-8s %-58s %s" % (act.upper(), k, (d.get("summary") or "")[:150])); continue
            new = d["question"]
            errs = validate(old, new, passages_for(new, pd))
            if errs:
                counts["rejected"] = counts.get("rejected", 0) + 1
                print("REJECTED %-58s %s\n         %s" % (k, d.get("summary", "")[:150], "; ".join(errs))); continue
            changed = sorted(f for f in set(old) | set(new) if old.get(f) != new.get(f))
            counts["patch"] = counts.get("patch", 0) + 1
            print("PATCH    %-58s [%s] %s" % (k, ",".join(changed), d.get("summary", "")[:200]))
            pd["problem_bank"][v["tier"]][v["i"]] = new
        if json.dumps(pd, ensure_ascii=False) != before:
            backup[row["id"]] = json.loads(before)
            if cmd == "apply":
                patch("lessons?id=eq." + row["id"], {"practice_data": pd})
    print("\n", counts, "| lessons touched:", len(backup))
    if cmd == "apply":
        path = os.path.join(HERE, "_backup_studentwalk_fixes_%s.json" % time.strftime("%Y-%m-%d"))
        io.open(path, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
        print("written, backup:", path)


if __name__ == "__main__":
    main()
