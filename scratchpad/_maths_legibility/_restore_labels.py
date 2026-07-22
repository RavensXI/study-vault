# -*- coding: utf-8 -*-
"""Restore the non-empty maths labels stripped in error.

    python scratchpad/_maths_legibility/_restore_labels.py --check
    python scratchpad/_maths_legibility/_restore_labels.py --apply

I stripped every `post` field on maths on a wrong assumption. 9,596 were empty
(harmless); ~1,270 were real labels from the original build (algebra x/y
suffixes, degrees, cm2, km, m/s) plus my session additions. No answer was
touched -- only label hints.

The strip snapshot preserved the exact step order (verified: the current
answer-step sequence matches the snapshot 1:1 for clean lessons, tier order
stable). So restore by POSITION where the counts and answers align -- that is an
exact undo. Where a lesson had only partial post coverage (snapshot shorter than
the answer-step list), fall back to restoring a non-empty label to the unique
answer-step that carries its value, and log anything ambiguous rather than guess.

Only non-empty labels are restored; empty posts display nothing and are left off.
Asserts only `post` is added back, so no answer can move.
"""
import copy, io, json, os, sys, urllib.request, collections

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


def req(url, method="GET", body=None, extra=None):
    h = dict(H)
    if extra:
        h.update(extra)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else None


def only_posts_added(before, after):
    def strip(pd):
        pd = copy.deepcopy(pd)
        for items in (pd.get("problem_bank") or {}).values():
            if isinstance(items, list):
                for p in items:
                    if isinstance(p, dict):
                        for st in p.get("guided_steps") or []:
                            if isinstance(st, dict) and "post" in st:
                                del st["post"]
        return pd
    return strip(before) == strip(after)


def answer_steps(pd):
    """Ordered list of steps that have an answer, in the same walk order the
    strip used (pb.items() -> problems -> steps)."""
    out = []
    for tier, items in (pd.get("problem_bank") or {}).items():
        if not isinstance(items, list):
            continue
        for p in items:
            if not isinstance(p, dict):
                continue
            for st in p.get("guided_steps") or []:
                if isinstance(st, dict) and st.get("answer") is not None:
                    out.append(st)
    return out


def main(apply_it):
    snap = json.load(io.open(os.path.join(HERE, "_stripped_labels_snapshot.json"), encoding="utf-8"))
    by_lesson = collections.defaultdict(list)
    for r in snap:
        by_lesson[(r["board"], r["unit"], r["lesson"])].append((r["answer"], r["post"]))

    restored, empty_skip, deferred = 0, 0, []
    subj_cache = {}
    for (board, uslug, ln), seq in by_lesson.items():
        nonempty = [(a, p) for a, p in seq if p not in ("", None)]
        empty_skip += len(seq) - len(nonempty)
        if not nonempty:
            continue
        if board not in subj_cache:
            sid = req(B + "subjects?slug=eq.%s&select=id" % board)[0]["id"]
            subj_cache[board] = {u["slug"]: u["id"] for u in req(B + "units?subject_id=eq.%s&select=id,slug" % sid)}
        uid = subj_cache[board].get(uslug)
        if not uid:
            deferred.append("%s %s L%d: unit missing" % (board, uslug, ln))
            continue
        rows = req(B + "lessons?unit_id=eq.%s&lesson_number=eq.%d&select=id,practice_data" % (uid, ln))
        if not rows:
            deferred.append("%s %s L%d: lesson missing" % (board, uslug, ln))
            continue
        before = rows[0]["practice_data"]
        pd = copy.deepcopy(before)
        steps = answer_steps(pd)
        hit = 0
        aligned = len(steps) == len(seq) and all(
            abs(float(steps[i]["answer"]) - float(seq[i][0])) < 1e-9 for i in range(len(seq)))
        if aligned:
            # exact position restore of the non-empty entries
            for i, (a, post) in enumerate(seq):
                if post not in ("", None) and not steps[i].get("post"):
                    steps[i]["post"] = post
                    hit += 1
        else:
            # partial coverage: restore each non-empty label to the unique answer-step
            by_ans = collections.defaultdict(list)
            for st in steps:
                by_ans[round(float(st["answer"]), 6)].append(st)
            for a, post in nonempty:
                cand = [st for st in by_ans.get(round(float(a), 6), []) if not st.get("post")]
                if len(cand) == 1:
                    cand[0]["post"] = post
                    hit += 1
                else:
                    deferred.append("%s %s L%d ans=%s post=%r (%d candidates)" % (board, uslug, ln, a, post, len(cand)))
        if hit:
            if not only_posts_added(before, pd):
                deferred.append("%s %s L%d: non-post diff, skipped" % (board, uslug, ln))
                continue
            restored += hit
            if apply_it:
                req(B + "lessons?id=eq.%s" % rows[0]["id"], method="PATCH",
                    body={"practice_data": pd}, extra={"Prefer": "return=minimal"})
                back = req(B + "lessons?id=eq.%s&select=practice_data" % rows[0]["id"])[0]["practice_data"]
                if not only_posts_added(before, back):
                    deferred.append("%s %s L%d: readback non-post change" % (board, uslug, ln))

    total_nonempty = sum(1 for r in snap if r["post"] not in ("", None))
    print("non-empty labels in snapshot:  %d" % total_nonempty)
    print("labels %s:                    %d" % ("restored" if apply_it else "to restore", restored))
    print("empty posts (correctly skipped): %d" % empty_skip)
    print("deferred/ambiguous (for agent pass): %d" % len(deferred))
    for d in deferred[:25]:
        print("   -", d)


if __name__ == "__main__":
    main("--apply" in sys.argv)
