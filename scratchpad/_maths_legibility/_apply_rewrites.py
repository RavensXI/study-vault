# -*- coding: utf-8 -*-
"""Apply agent-proposed prose edits to maths walks, with hard validation.

    python scratchpad/_maths_legibility/_apply_rewrites.py --check
    python scratchpad/_maths_legibility/_apply_rewrites.py --apply

Reads _apply_edits.json (built from the apply-workflow journal): a list of
{board, unit, lesson, tier, index, step, field, new_text}. Each edit sets one
existing step's pre/say/done text. The safety is entirely in validation:

  - the number of problems and steps must be identical before/after
  - EVERY step's answer must be byte-identical before/after
  - the ONLY thing that may differ is pre/say/done text
If a lesson's edits would change anything else, the WHOLE lesson is skipped and
flagged -- no partial, no answer ever moves. Verified again on readback.

The touched problems are then play-through-checked separately.
"""
import copy, io, json, os, re, sys, urllib.request, collections

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}


def strip(t):
    return re.sub(r"<[^>]+>", "", str(t or ""))


def leaks_answer(new_text, old_text, answer):
    """True if the rewrite introduces the step's answer as a standalone number
    that the original prose did not show -- a walk step must not hand over the
    value the student is about to type."""
    if not isinstance(answer, (int, float)) or isinstance(answer, bool):
        return False
    a = ("%g" % answer)
    pat = r"(?<![\d.])" + re.escape(a) + r"(?![\d.])"
    return bool(re.search(pat, strip(new_text))) and not re.search(pat, strip(old_text))


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def skeleton(pd):
    """Everything about the walks EXCEPT pre/say/done text -- must be invariant."""
    out = []
    for tier in sorted((pd.get("problem_bank") or {}).keys()):
        items = pd["problem_bank"][tier]
        if not isinstance(items, list):
            continue
        for i, p in enumerate(items):
            if not isinstance(p, dict):
                continue
            out.append((tier, i, tuple(p.get("solutions") or [])))
            for si, st in enumerate(p.get("guided_steps") or []):
                if isinstance(st, dict):
                    out.append((tier, i, si, st.get("answer"), st.get("post"), st.get("phase"),
                                bool(st.get("pre")), bool(st.get("say")), bool(st.get("done"))))
    return out


def main(apply_it):
    edits_file = next((a for a in sys.argv[1:] if a.endswith(".json")), "_apply_edits.json")
    edits = json.load(io.open(os.path.join(HERE, edits_file), encoding="utf-8"))
    by_lesson = collections.defaultdict(list)
    for e in edits:
        by_lesson[(e["board"], e["unit"], e["lesson"])].append(e)

    subj_cache = {}
    applied, skipped_lessons, touched, leaked = 0, [], [], []
    for (board, uslug, ln), es in by_lesson.items():
        if board not in subj_cache:
            sid = req(B + "subjects?slug=eq.%s&select=id" % board)[0]["id"]
            subj_cache[board] = {u["slug"]: u["id"] for u in req(B + "units?subject_id=eq.%s&select=id,slug" % sid)}
        uid = subj_cache[board].get(uslug)
        if not uid:
            continue
        rows = req(B + "lessons?unit_id=eq.%s&lesson_number=eq.%d&select=id,practice_data" % (uid, ln))
        if not rows:
            continue
        before = rows[0]["practice_data"]
        pd = copy.deepcopy(before)
        pb = pd.get("problem_bank") or {}
        n = 0
        for e in es:
            items = pb.get(e["tier"])
            if not isinstance(items, list) or e["index"] >= len(items):
                continue
            steps = items[e["index"]].get("guided_steps") or []
            if e["step"] >= len(steps):
                continue
            st = steps[e["step"]]
            if not isinstance(st, dict):
                continue
            fld = e["field"]
            if fld not in ("pre", "say", "done"):
                continue
            # only edit a field that already exists (don't invent pre on a say-step etc.)
            if fld not in st:
                continue
            if st[fld] == e["new_text"]:
                continue
            if leaks_answer(e["new_text"], st[fld], st.get("answer")):
                leaked.append("%s %s L%d %s[%d].s%d leaks answer %s" %
                              (board, uslug, ln, e["tier"], e["index"], e["step"], st.get("answer")))
                continue
            st[fld] = e["new_text"]
            n += 1
        if n == 0:
            continue
        # HARD validation: skeleton (answers, counts, structure) must be unchanged
        if skeleton(before) != skeleton(pd):
            skipped_lessons.append("%s %s L%d: structure/answer would change" % (board, uslug, ln))
            continue
        applied += n
        touched.append((board, uslug, ln, n))
        if apply_it:
            req(B + "lessons?id=eq.%s" % rows[0]["id"], method="PATCH",
                body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
            back = req(B + "lessons?id=eq.%s&select=practice_data" % rows[0]["id"])[0]["practice_data"]
            if skeleton(before) != skeleton(back):
                skipped_lessons.append("%s %s L%d: readback structure changed" % (board, uslug, ln))

    print("edits %s: %d across %d lessons" % ("applied" if apply_it else "to apply", applied, len(touched)))
    if leaked:
        print("LEAKAGE-BLOCKED: %d" % len(leaked))
        for l in leaked[:15]:
            print("   -", l)
    by_board = collections.Counter(t[0] for t in touched)
    print("by board:", dict(by_board))
    if skipped_lessons:
        print("SKIPPED (validation):", len(skipped_lessons))
        for s in skipped_lessons[:15]:
            print("   -", s)
    io.open(os.path.join(HERE, "_touched_lessons.json"), "w", encoding="utf-8").write(
        json.dumps(touched, ensure_ascii=False))


if __name__ == "__main__":
    main("--apply" in sys.argv)
