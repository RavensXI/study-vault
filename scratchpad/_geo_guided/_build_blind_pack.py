# -*- coding: utf-8 -*-
"""Build blind question packs for an independent adversarial check.

    python scratchpad/_geo_guided/_build_blind_pack.py

Writes one markdown pack per lesson to _blind/, containing the questions with
EVERY answer removed -- no solutions, no guided-step answers, no misconception
expect values. A checker given the stored answer tends to justify it; a checker
given nothing has to do the work.

Each pack mixes questions authored in this session with control questions from
the same lesson that were authored and reviewed earlier, unlabelled and in a
fixed shuffled order. If a checker misses the controls, its disagreements on the
new work mean much less. Without controls a wrong checker and a wrong author are
indistinguishable.

The answer key is written separately to _blind/_key.json, which the checkers are
never given.
"""
import hashlib, io, json, os, re, sys, urllib.request

B = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_blind")

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not KEY:
    sys.exit("SUPABASE_SERVICE_KEY not set")
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

# Everything authored or altered in this session.
AUTHORED = {
    4:  [("bronze", 0), ("bronze", 1), ("bronze", 3), ("silver", 0), ("silver", 3), ("silver", 5)],
    11: [("bronze", 2), ("bronze", 4), ("bronze", 5), ("silver", 2), ("silver", 5), ("gold", 2),
         ("bronze", 7), ("silver", 6), ("gold", 3)],
    12: [("silver", 4), ("bronze", 1), ("bronze", 2), ("bronze", 5), ("silver", 1),
         ("silver", 5), ("gold", 1)],
    13: [("bronze", 4)],
    14: [("bronze", 3), ("bronze", 7), ("silver", 2), ("silver", 6), ("gold", 2)],
}
# Untouched questions from the same lessons, used as controls.
CONTROLS = {
    4:  [("bronze", 2), ("gold", 0)],
    11: [("bronze", 0), ("silver", 0), ("gold", 0)],
    12: [("bronze", 0), ("silver", 0), ("gold", 0)],
    13: [("bronze", 0), ("silver", 0), ("gold", 0)],
    14: [("bronze", 0), ("silver", 0), ("gold", 0)],
}


def req(url):
    r = urllib.request.Request(url, headers=H)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def clean(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def chart_table(ch):
    d = ch.get("data") or {}
    labs = d.get("labels") or []
    out = []
    for ds in d.get("datasets") or []:
        vals = ds.get("data") or []
        pairs = ", ".join("%s=%s" % (l, abs(v) if isinstance(v, (int, float)) else v)
                          for l, v in zip(labs, vals))
        out.append("  - %s: %s" % (ds.get("label") or "series", pairs))
    ax = []
    for a in ((ch.get("options") or {}).get("scales") or {}).values():
        if isinstance(a, dict):
            t = (a.get("title") or {}).get("text")
            if t:
                ax.append(str(t))
    return ("  axis labels: %s\n" % "; ".join(ax) if ax else "") + "\n".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    subj = req(B + "subjects?slug=eq.geography-aqa&select=id")[0]["id"]
    unit = [u for u in req(B + "units?subject_id=eq.%s&select=id,slug" % subj)
            if u["slug"] == "geographical-skills"][0]["id"]
    lessons = req(B + "lessons?unit_id=eq.%s&select=lesson_number,title,practice_data" % unit)
    key = {}
    for l in sorted(lessons, key=lambda x: x["lesson_number"]):
        n = l["lesson_number"]
        if n not in AUTHORED:
            continue
        pb = (l.get("practice_data") or {}).get("problem_bank") or {}
        picks = [(t, i, "new") for t, i in AUTHORED[n]] + [(t, i, "control") for t, i in CONTROLS.get(n, [])]
        # stable shuffle so the pack is reproducible but order carries no signal
        picks.sort(key=lambda p: hashlib.md5(("%d%s%d" % (n, p[0], p[1])).encode()).hexdigest())

        lines = ["# Geography Skills L%02d - %s" % (n, l["title"]),
                 "",
                 "Answer each question from the stimulus. Show how you got there.",
                 "You are NOT told the expected answers and must not guess at them.",
                 ""]
        for qi, (tier, i, kind) in enumerate(picks, 1):
            items = pb.get(tier)
            if not isinstance(items, list) or i >= len(items):
                continue
            p = items[i]
            if not isinstance(p, dict):
                continue
            qid = "L%02d-Q%02d" % (n, qi)
            key[qid] = {"lesson": n, "tier": tier, "index": i, "kind": kind,
                        "solutions": p.get("solutions"),
                        "options": p.get("options"),
                        "display": clean(p.get("display"))}
            lines.append("## %s" % qid)
            lines.append("")
            lines.append(clean(p.get("display")))
            lines.append("")
            if p.get("image"):
                lines.append("Stimulus map: %s" % p["image"])
                lines.append("")
            if isinstance(p.get("chart"), dict):
                lines.append("Stimulus chart data (values as plotted):")
                lines.append(chart_table(p["chart"]))
                lines.append("")
            if p.get("options"):
                lines.append("Options:")
                for oi, o in enumerate(p["options"]):
                    lines.append("  %d. %s" % (oi, clean(o)))
                lines.append("")
            if p.get("unit"):
                lines.append("Answer unit: %s" % p["unit"])
                lines.append("")
            if p.get("ruler"):
                lines.append("A ruler tool is offered with this question.")
                lines.append("")
        path = os.path.join(OUT, "L%02d.md" % n)
        io.open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("wrote %s  (%d questions)" % (path, len(picks)))

    io.open(os.path.join(OUT, "_key.json"), "w", encoding="utf-8").write(
        json.dumps(key, indent=1, ensure_ascii=False))
    print("\nanswer key: %s (%d questions, %d new / %d control)"
          % (os.path.join(OUT, "_key.json"), len(key),
             sum(1 for v in key.values() if v["kind"] == "new"),
             sum(1 for v in key.values() if v["kind"] == "control")))


if __name__ == "__main__":
    main()
