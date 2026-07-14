"""Per-student pack draft — the 'teacher summary' paragraph on the printable
parents'-evening / report pack. One small-model call per student, run in a
batch when the teacher clicks "Generate packs" (never per page-view).

Demo form: reads one synthetic student's aggregates from teach.html?packagg=N
and writes design-lab/teach-pack-demo.js. The real build runs the same prompt
over real sv_progress aggregates server-side.

Usage: python scripts/_teach_pack.py --student 9 [--url URL]
"""
import argparse, html, json, os, re, shutil, subprocess, sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design-lab", "teach-pack-demo.js")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PROMPT = """You are drafting the teacher's summary paragraph for a GCSE student's
parents'-evening pack, from the revision evidence below. The teacher will edit it
before sharing. Rules:
- 4-5 sentences, warm and specific. Address the parents ("Oscar has...").
- Lead with something genuinely positive and TRUE from the data, then the one thing
  to focus on (name the actual topic), then one concrete thing that would help at home
  (10 minutes of warm-ups, redoing flashcards on X — real platform activities only).
- Recall accuracy is retention evidence, not ability — phrase as "hasn't stuck yet".
- Never invent numbers or facts not in the data. No jargon, no flattery-padding.
Output ONLY the HTML fragment (plain <b> allowed, no headings, no markdown).

DATA:
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--student", type=int, required=True)
    ap.add_argument("--url", default="http://localhost:8901/design-lab/teach.html")
    args = ap.parse_args()

    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                        "--virtual-time-budget=6000", "--dump-dom",
                        args.url + "?packagg=" + str(args.student)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    m = re.search(r'<pre id="packagg"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m:
        raise SystemExit("no pack aggregates found")
    agg = json.loads(html.unescape(m.group(1)))
    print("student:", agg["name"], "| practice answers:", len(agg.get("practiceFeedback", [])))

    exe = shutil.which("claude")
    if not exe:
        raise SystemExit("claude CLI not on PATH")
    rr = subprocess.run([exe, "-p", "--model", "sonnet"],
                        input=PROMPT + json.dumps(agg, ensure_ascii=False),
                        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    if rr.returncode != 0:
        raise SystemExit("claude -p failed: " + (rr.stderr or "")[-300:])
    frag = re.sub(r"^```(?:html)?|```$", "", rr.stdout.strip(), flags=re.M).strip()
    if len(frag) < 60:
        raise SystemExit("suspicious output: " + frag[:200])

    existing = {}
    try:
        cur = open(OUT, encoding="utf-8").read()
        mm = re.search(r"window\.SV_PACK_DEMO\s*=\s*(\{.*\});", cur, re.S)
        if mm:
            existing = json.loads(mm.group(1))
    except OSError:
        pass
    existing[str(args.student)] = frag
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* Written by scripts/_teach_pack.py — one claude -p call per student,\n"
                "   batched when the teacher generates packs. Demo entries only. */\n"
                "window.SV_PACK_DEMO = " + json.dumps(existing, ensure_ascii=False) + ";\n")
    print("pack draft written for student", args.student)
    print(frag[:300])


if __name__ == "__main__":
    main()
