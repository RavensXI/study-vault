# -*- coding: utf-8 -*-
"""Classify every 0<answer<1 walk-step box so it gets the RIGHT label, not a
blanket "(a decimal)".

    python scratchpad/_geo_guided/_classify_decimals.py

Blanket-labelling would mislabel measurements that happen to fall below 1 -- a
0.4 m/s velocity or a 0.3 m depth is not "a decimal" the student is meant to
recognise as a proportion. The rule keys off the prose:

  MEASUREMENT  prose already states a unit ("in m/s", "in metres", "%", "°C").
               The reader pass said these are fine; LEAVE them.
  DECIMAL      prose frames the answer as a proportion or a "share as a decimal"
               with no unit. These are the ones a student converting a
               percentage might fill with 20 instead of 0.2 -> label "(a decimal)".
  REVIEW       neither pattern is clear; print for a human decision.
"""
import io, json, os, re, sys, urllib.request

S = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
K = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}


def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(S + u, headers=H), timeout=120))


def txt(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(t or ""))).strip()


HAS_UNIT = re.compile(r"\bin (m/s|metres|m|km|mm|hectares|litres)\b|°c|\bper cent\b|%|\bm/s\b|\bdegrees\b", re.I)
DECIMALISH = re.compile(r"as a decimal|that share|proportion|divided by|÷|share of|fraction", re.I)


def classify(pre):
    p = txt(pre)
    if HAS_UNIT.search(p):
        return "MEASUREMENT", ""
    if DECIMALISH.search(p):
        return "DECIMAL", "(a decimal)"
    return "REVIEW", ""


def main():
    sid = get("subjects?slug=eq.geography-aqa&select=id")[0]["id"]
    uid = [u for u in get("units?subject_id=eq.%s&select=id,slug" % sid)
           if u["slug"] == "geographical-skills"][0]["id"]
    L = {l["lesson_number"]: l for l in
         get("lessons?unit_id=eq.%s&select=lesson_number,practice_data" % uid)}
    out = {"DECIMAL": [], "MEASUREMENT": [], "REVIEW": []}
    for n, l in sorted(L.items()):
        for tier, items in l["practice_data"]["problem_bank"].items():
            if not isinstance(items, list):
                continue
            for i, p in enumerate(items):
                if not isinstance(p, dict):
                    continue
                for si, st in enumerate(p.get("guided_steps") or []):
                    if not isinstance(st, dict):
                        continue
                    a = st.get("answer")
                    if isinstance(a, float) and 0 < a < 1 and not st.get("post"):
                        cls, label = classify(st.get("pre"))
                        out[cls].append({"lesson": n, "tier": tier, "index": i, "step": si,
                                         "answer": a, "label": label,
                                         "pre": txt(st.get("pre"))})
    for cls in ("DECIMAL", "REVIEW", "MEASUREMENT"):
        print("== %s: %d ==" % (cls, len(out[cls])))
        for r in out[cls]:
            print("  L%-2d %s[%d].s%d ans=%-5s %-12s | %s"
                  % (r["lesson"], r["tier"], r["index"], r["step"], r["answer"],
                     r["label"], r["pre"][:58]))
        print()
    io.open("scratchpad/_geo_guided/_decimal_labels.json", "w", encoding="utf-8").write(
        json.dumps(out["DECIMAL"], indent=1, ensure_ascii=False))
    print("DECIMAL set (the ones to label) written to _decimal_labels.json: %d steps" % len(out["DECIMAL"]))


if __name__ == "__main__":
    main()
