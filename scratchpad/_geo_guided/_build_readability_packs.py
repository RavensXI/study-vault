# -*- coding: utf-8 -*-
"""Write one readability pack per geography-skills lesson.

    python scratchpad/_geo_guided/_build_readability_packs.py

Unlike the blind packs, these KEEP the answers: the job is not to re-derive the
maths, it is to read every problem and its walk as a struggling 15-year-old and
say where the WORDING, assumed knowledge, or an unlabelled answer box would trip
them. Each pack carries the full walk, step by step, with the answer each step
expects and whether that box shows a unit label (`post`).
"""
import json, os, re, sys, urllib.request

S = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_readpacks")
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


def clean(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(t or ""))).strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    sid = get("subjects?slug=eq.geography-aqa&select=id")[0]["id"]
    uid = [u for u in get("units?subject_id=eq.%s&select=id,slug" % sid)
           if u["slug"] == "geographical-skills"][0]["id"]
    lessons = get("lessons?unit_id=eq.%s&select=lesson_number,title,practice_data" % uid)
    for l in sorted(lessons, key=lambda x: x["lesson_number"]):
        n = l["lesson_number"]
        pb = (l.get("practice_data") or {}).get("problem_bank") or {}
        lines = ["# L%02d - %s" % (n, l["title"]), ""]
        for tier in ("bronze", "silver", "gold"):
            for i, p in enumerate(pb.get(tier, [])):
                if not isinstance(p, dict):
                    continue
                lines.append("## %s[%d]  (input: %s, answer unit shown on the main box: %s)"
                             % (tier, i, p.get("input_type"), p.get("unit") or "(none)"))
                lines.append("QUESTION: " + clean(p.get("display")))
                if p.get("options"):
                    for oi, o in enumerate(p["options"]):
                        lines.append("   option %d: %s" % (oi, clean(o)))
                ch = p.get("chart")
                if isinstance(ch, dict):
                    d = ch.get("data", {})
                    labs = d.get("labels")
                    if labs:
                        lines.append("   chart categories: " + ", ".join(map(str, labs)))
                steps = p.get("guided_steps") or []
                if steps:
                    lines.append("WALK (what the student is asked, step by step):")
                    for si, st in enumerate(steps):
                        if not isinstance(st, dict):
                            continue
                        if st.get("say"):
                            lines.append("   - intro: " + clean(st["say"]))
                        if st.get("answer") is not None:
                            box = "[box expects: %s%s]" % (
                                st["answer"],
                                "  (unit label on box: '%s')" % st["post"] if st.get("post") else "  (NO unit label on box)")
                            lines.append("   - ask: %s  %s" % (clean(st.get("pre")), box))
                lines.append("")
        path = os.path.join(OUT, "L%02d.md" % n)
        import io
        io.open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("wrote L%02d (%d problems)" % (n, sum(len(pb.get(t, [])) for t in ("bronze", "silver", "gold"))))


if __name__ == "__main__":
    main()
