"""Author per-distractor misconception diagnoses for multiple-choice problems.

THE CANARY (per the standing rule: one unit, read the real cost, then decide).
First target: english-language-aqa / paper-1-reading — 30 MC problems, 8 lessons.

WHY. The misconceptions field is what the wrong-answer matcher checks, a match
is the only thing that writes the misconception log, and the log is what the
teacher dashboard shows. The quantitative families have ~99% coverage; English,
MFL and Music have none — so the practice work their students do contributes
nothing to the one panel the platform sells on. This closes that loop with no
renderer changes: practice.html already passes the chosen option's ORIGINAL
index as `given`, and matchMisconception fires on {expect: <index>}.

RUNTIME CONTRACT (verified in practice.html before writing a word):
  {expect: <wrong option's original index>, id: "<short-kebab-tag>", message: "<diagnosis>"}
  - matched -> student sees "It looks like what happened: {message}"
  - id      -> the teacher-facing tag in sv-misconception-log
  - options SHUFFLE at render: a message must never say "option A" or "the
    first option" — it names the CONTENT of the tempting answer instead.

CONTENT RULES (house style, from memory):
  - plain text: no HTML entities, no tags, unicode punctuation only
  - never "again" / "this time" — the bank is shuffled, sequence words lie
  - no board names in student-facing text
  - diagnose the TEMPTATION, then teach toward the right answer; <= 45 words
  - only genuinely tempting distractors get an entry (1-3 per problem); a
    silly distractor gets none rather than a padded diagnosis

Usage:
  python scripts/misconceptions/enrich_mc.py --subject english-language-aqa --unit paper-1-reading
  ... --apply     writes to Supabase (backup saved first). Without it: dry run.
"""
import argparse
import io
import json
import os
import re
import sys
import urllib.request

import anthropic

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}

MODEL = "claude-sonnet-5"
PRICE_IN, PRICE_OUT = 2.0, 10.0          # $/M tokens, intro pricing to 31 Aug

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = re.compile(r"<[^>]+>")

SYSTEM = """You write misconception diagnoses for GCSE multiple-choice practice questions.

For each question you are given the passage context, the question, the options
with their ORIGINAL indexes, and which index is correct. For each genuinely
tempting WRONG option, write why a student would pick it and what the right
thinking is.

Rules, all hard:
- Address the student as "you". British English. Warm, specific, brief.
- NEVER refer to options by letter or position ("option A", "the first one") —
  options are shuffled at display time. Name the CONTENT of the wrong answer.
- Each message is at most 45 words: first the tempting logic ("You picked X
  because..."), then the correction toward the right answer.
- Plain text only. No HTML, no entities, no markdown, no quotation of exam
  boards, no "again" or "this time" (question order is shuffled).
- Skip silly distractors. 1-3 entries per question. Never diagnose the correct
  index.
- id: a short kebab-case tag (max 40 chars) a teacher would recognise as the
  error pattern, e.g. "implicit-taken-as-stated".

Return ONLY a JSON array, one element per question you were given:
  [{"problem": <n>, "misconceptions": [{"expect": <wrong index>, "id": "...", "message": "..."}]}]
"""


def get(path):
    r = urllib.request.Request(URL + "/rest/v1/" + path, headers=H)
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


def patch(path, body):
    h = dict(H)
    h["Prefer"] = "return=representation"
    r = urllib.request.Request(URL + "/rest/v1/" + path,
                               data=json.dumps(body).encode("utf-8"),
                               headers=h, method="PATCH")
    return json.loads(urllib.request.urlopen(r).read().decode("utf-8"))


def passage_text(pd, p):
    pid = p.get("passage_id")
    if not pid:
        return ""
    for ps in pd.get("passages") or []:
        if ps.get("id") == pid:
            return TAGS.sub(" ", ps.get("text") or "")[:1800]
    return ""


def plain(s):
    return TAGS.sub(" ", s or "").strip()


def validate_entry(e, n_options, correct):
    """Reject anything that breaks the runtime contract or the house rules."""
    problems = []
    if not isinstance(e.get("expect"), int) or not (0 <= e["expect"] < n_options):
        problems.append("expect out of range")
    elif e["expect"] == correct:
        problems.append("diagnoses the CORRECT option")
    msg = e.get("message") or ""
    if not msg or len(msg.split()) > 55:
        problems.append("message empty or too long")
    if re.search(r"[<>]|&[a-z]+;", msg):
        problems.append("markup in message")
    if re.search(r"(?i)\boption [a-d]\b|\bthe (first|second|third|fourth) (option|one)\b", msg):
        problems.append("references option position")
    if re.search(r"(?i)\b(again|this time)\b", msg):
        problems.append("sequence word (bank is shuffled)")
    if re.search(r"(?i)\b(AQA|Edexcel|OCR|Eduqas|WJEC)\b", msg):
        problems.append("board name")
    if not re.fullmatch(r"[a-z0-9-]{3,40}", e.get("id") or ""):
        problems.append("bad id tag")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--unit", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    subj = get("subjects?select=id,slug&slug=eq.%s" % args.subject)[0]
    unit = get("units?select=id,slug&subject_id=eq.%s&slug=eq.%s" % (subj["id"], args.unit))[0]
    lessons = get("lessons?select=id,lesson_number,title,practice_data"
                  "&unit_id=eq.%s&order=lesson_number" % unit["id"])

    cl = anthropic.Anthropic()
    usage_in = usage_out = 0
    all_valid = {}
    rejected = []

    for les in lessons:
        pd = les.get("practice_data") or {}
        pb = pd.get("problem_bank") or {}
        jobs = []
        for tier in ("bronze", "silver", "gold"):
            for i, p in enumerate(pb.get(tier) or []):
                if isinstance(p, dict) and p.get("input_type") == "multiple_choice":
                    jobs.append((tier, i, p))
        if not jobs:
            continue

        lines = ["LESSON: %s" % les["title"]]
        for n, (tier, i, p) in enumerate(jobs):
            lines.append("")
            lines.append("QUESTION %d:" % n)
            ptxt = passage_text(pd, p)
            if ptxt:
                lines.append("PASSAGE (context): %s" % ptxt)
            lines.append("ASK: %s" % plain(p.get("question") or p.get("display")))
            for oi, o in enumerate(p.get("options") or []):
                mark = "  <-- CORRECT" if oi == (p.get("solutions") or [None])[0] else ""
                lines.append("  index %d: %s%s" % (oi, plain(o), mark))

        msg = cl.messages.create(
            model=MODEL, max_tokens=4000, system=SYSTEM,
            messages=[{"role": "user", "content": "\n".join(lines)}])
        usage_in += msg.usage.input_tokens
        usage_out += msg.usage.output_tokens

        text = "".join(b.text for b in msg.content if getattr(b, "text", None))
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            print("L%s: model returned no JSON — skipped" % les["lesson_number"])
            continue
        try:
            arr = json.loads(m.group(0))
        except ValueError:
            print("L%s: JSON parse failed — skipped" % les["lesson_number"])
            continue

        for item in arr:
            n = item.get("problem")
            if not isinstance(n, int) or not (0 <= n < len(jobs)):
                continue
            tier, i, p = jobs[n]
            correct = (p.get("solutions") or [None])[0]
            keep = []
            for e in item.get("misconceptions") or []:
                errs = validate_entry(e, len(p.get("options") or []), correct)
                if errs:
                    rejected.append((les["lesson_number"], tier, i, errs, e))
                else:
                    keep.append({"expect": e["expect"], "id": e["id"], "message": e["message"]})
            if keep:
                all_valid[(les["id"], tier, i)] = keep
        print("L%s: %d MC problems -> %d with diagnoses so far"
              % (les["lesson_number"], len(jobs),
                 sum(1 for k in all_valid if k[0] == les["id"])))

    cost = (usage_in * PRICE_IN + usage_out * PRICE_OUT) / 1e6
    print()
    print("tokens: %d in / %d out   COST: $%.3f" % (usage_in, usage_out, cost))
    print("problems enriched: %d | entries: %d | rejected entries: %d"
          % (len(all_valid), sum(len(v) for v in all_valid.values()), len(rejected)))
    for r in rejected[:6]:
        print("  rejected L%s %s[%d]: %s" % (r[0], r[1], r[2], ", ".join(r[3])))

    if not args.apply:
        io.open(os.path.join(HERE, "_canary_preview.json"), "w", encoding="utf-8").write(
            json.dumps([{"lesson": k[0], "tier": k[1], "idx": k[2], "entries": v}
                        for k, v in all_valid.items()], indent=1))
        print("\nDRY RUN — preview in scripts/misconceptions/_canary_preview.json. --apply to write.")
        return

    # ---- write, with a backup first ----
    backup = {}
    for les in lessons:
        backup[les["id"]] = les.get("practice_data")
    io.open(os.path.join(HERE, "_backup_%s_%s.json" % (args.subject, args.unit)),
            "w", encoding="utf-8").write(json.dumps(backup))

    wrote = 0
    for les in lessons:
        pd = les.get("practice_data") or {}
        pb = pd.get("problem_bank") or {}
        touched = False
        for (lid, tier, i), entries in all_valid.items():
            if lid != les["id"]:
                continue
            pb[tier][i]["misconceptions"] = entries
            touched = True
        if touched:
            patch("lessons?id=eq.%s" % les["id"], {"practice_data": pd})
            wrote += 1
    print("wrote %d lesson(s). Backup: _backup_%s_%s.json" % (wrote, args.subject, args.unit))


if __name__ == "__main__":
    main()
