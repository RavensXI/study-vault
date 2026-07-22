# -*- coding: utf-8 -*-
"""Classify maths walk-step boxes for labelling, per board.

    python scratchpad/_maths_legibility/_classify_maths.py <board-slug>
    python scratchpad/_maths_legibility/_classify_maths.py maths-aqa

Same discipline as the geography pass: label by what the step COMPUTES (read from
the prose), never blanket by value, because a 0.4 that is a probability is a
decimal but a 0.4 that is "in m" is a measurement whose prose already says so.

Buckets each numeric box with no `post` label:
  DECIMAL      prose frames a proportion / "as a decimal" / a ratio with no unit
               -> label "(a decimal)"
  UNIT         prose does NOT state a unit but the answer clearly carries one
               that maths marks (cm, cm2, cm3, degrees, etc.) -> label with it
  STATED       prose already says the unit ("in cm2", "to 2 dp") -> LEAVE
  REVIEW       ambiguous -> print for a human decision

Writes the confident DECIMAL+UNIT labels to _labels_<board>.json (the apply set)
and prints REVIEW for eyeballing. Applies nothing.
"""
import io, json, os, re, sys, urllib.request

S = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
K = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(S + u, headers=H), timeout=180))


def txt(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(t or ""))).strip()


# prose that already states the unit/format -> leave alone
STATED = re.compile(
    r"\bin (cm2|cm3|cm\^?2|cm\^?3|cm|mm|m2|m3|m|km|degrees|litres|ml|kg|g|seconds|hours|square|cubic)\b"
    r"|to \d+ (decimal|dp|sig|significant)|as a decimal|nearest (whole|integer|degree|cm|m)\b"
    r"|cm²|cm³|m²|m³|°|per cent|%",
    re.I)
DECIMALISH = re.compile(r"as a decimal|that share|proportion|divided by|÷|probability|\bratio\b|fraction as a decimal|scale factor", re.I)
# unit the answer plainly carries, keyed by a word in the prose
UNIT_HINTS = [
    (re.compile(r"\barea\b", re.I), "cm²"),
    (re.compile(r"\bvolume\b", re.I), "cm³"),
    (re.compile(r"\bsurface area\b", re.I), "cm²"),
    (re.compile(r"\bangle\b|\bbearing\b", re.I), "degrees"),
    (re.compile(r"\bperimeter\b|\bcircumference\b|\blength\b|\bradius\b|\bdiameter\b", re.I), "cm"),
    (re.compile(r"\bprobability\b", re.I), "(a decimal)"),
]


def classify(pre, ans, is_final):
    """is_final: this step's answer equals the problem's stored solution.

    A decimal label only makes sense for an actual decimal answer (0<x<1,
    non-integer) -- keying off "÷" alone wrongly caught 406 whole-number
    division steps like "24 ÷ 4 = 6". A unit label belongs only on the FINAL
    answer box; intermediate arithmetic steps ("18 + 6 =") carry no unit and
    must be left alone.
    """
    p = txt(pre)
    if STATED.search(p):
        return "STATED", ""
    is_decimal = isinstance(ans, float) and not float(ans).is_integer() and 0 < ans < 1
    if is_decimal and DECIMALISH.search(p):
        return "DECIMAL", "(a decimal)"
    if is_final:
        for rx, lab in UNIT_HINTS:
            if rx.search(p):
                # a probability's "unit" is really (a decimal); keep that honest
                if lab == "(a decimal)" and not is_decimal:
                    continue
                return "UNIT", lab
    return "REVIEW", ""


def main(board):
    sid = get("subjects?slug=eq.%s&select=id" % board)[0]["id"]
    labels, review = [], []
    counts = {"DECIMAL": 0, "UNIT": 0, "STATED": 0, "REVIEW": 0}
    for u in get("units?subject_id=eq.%s&select=id,slug" % sid):
        for l in get("lessons?unit_id=eq.%s&select=lesson_number,practice_data" % u["id"]):
            pb = (l.get("practice_data") or {}).get("problem_bank") or {}
            for tier, items in pb.items():
                if not isinstance(items, list):
                    continue
                for i, p in enumerate(items):
                    if not isinstance(p, dict):
                        continue
                    sol = (p.get("solutions") or [None])[0]
                    for si, st in enumerate(p.get("guided_steps") or []):
                        if not isinstance(st, dict):
                            continue
                        a = st.get("answer")
                        if not (isinstance(a, (int, float)) and not isinstance(a, bool)):
                            continue
                        if st.get("post"):
                            continue
                        is_final = isinstance(sol, (int, float)) and abs(float(a) - float(sol)) < 1e-9
                        cls, lab = classify(st.get("pre"), a, is_final)
                        counts[cls] += 1
                        rec = {"unit": u["slug"], "lesson": l["lesson_number"], "tier": tier,
                               "index": i, "step": si, "answer": a, "label": lab,
                               "pre": txt(st.get("pre"))[:70]}
                        if cls in ("DECIMAL", "UNIT"):
                            labels.append(rec)
                        elif cls == "REVIEW":
                            review.append(rec)
    io.open(os.path.join(HERE, "_labels_%s.json" % board), "w", encoding="utf-8").write(
        json.dumps(labels, indent=1, ensure_ascii=False))
    print("board=%s" % board)
    print("counts:", counts)
    print("confident labels (DECIMAL+UNIT) -> _labels_%s.json : %d" % (board, len(labels)))
    print("REVIEW (need eyeballing): %d" % len(review))
    for r in review[:25]:
        print("   %s L%d %s[%d].s%d ans=%s | %s" % (r["unit"], r["lesson"], r["tier"], r["index"], r["step"], r["answer"], r["pre"]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "maths-aqa")
