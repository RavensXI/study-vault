"""Teach the AI marking prompts to NAME the error pattern they see.

Free-writing types (translate, ai_mark, ai_write, role_play) cannot carry
pre-computed wrong answers, so their misconception route is different: the
marker returns a "misconception" field in its JSON, chosen from a controlled
per-family tag list, ONLY when it can point at the error in the student's
answer. practice.html logs a valid tag to sv-misconception-log — the same
stream the deterministic matcher feeds — so the teacher table fills from
free writing too.

This is a DETERMINISTIC text transform: it appends one instruction block to
  - lesson-level practice_data.ai_marking_prompts[*]        (EngLang mostly)
  - per-problem ai_system_prompt on the AI-marked types      (MFL mostly)
No model calls, no cost. Idempotent via the marker string, so re-running never
stacks duplicates. Backups per unit alongside this script.

Tag lists are authored HERE, not by the marker at runtime — the whole point is
a vocabulary a teacher can recognise across a class, and a model inventing new
prose tags per response would tally as one-offs and aggregate to nothing.

Usage:
  python scripts/misconceptions/enrich_ai_prompts.py --subject spanish-aqa --unit people-and-lifestyle --apply
"""
import argparse
import io
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))

MARKER = 'Also include a "misconception" field'
AI_TYPES = {"translate", "ai_mark", "ai_write", "role_play"}

TAGS_MFL = ("tense-confusion, verb-conjugation-error, adjective-agreement, word-order, "
            "false-friend, gender-error, literal-translation, wrong-person, "
            "missing-accent-changes-meaning, informal-register")

TAGS_ENG = ("no-evidence-quoted, feature-spotting-no-effect, misread-question-focus, "
            "retell-not-analyse, informal-register, unfocused-answer, "
            "wrong-text-referenced, assertion-without-support")


def block(tags):
    return ("\n\n" + MARKER + " in your JSON response. If the student's answer shows one "
            "of these error patterns AND you can point to the exact place it happens, set "
            "it to that tag; otherwise set it to \"none\". Choose ONLY from: " + tags + ". "
            "Never invent a tag that is not on this list.")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--unit", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    is_mfl = args.subject.split("-")[0] in ("spanish", "french", "german")
    tags = TAGS_MFL if is_mfl else TAGS_ENG
    addition = block(tags)

    subj = get("subjects?select=id&slug=eq.%s" % args.subject)[0]
    unit = get("units?select=id&subject_id=eq.%s&slug=eq.%s" % (subj["id"], args.unit))[0]
    lessons = get("lessons?select=id,lesson_number,practice_data"
                  "&unit_id=eq.%s&order=lesson_number" % unit["id"])

    prompts_touched = problems_touched = wrote = 0
    backup = {}

    for les in lessons:
        pd = les.get("practice_data") or {}
        touched = False

        amp = pd.get("ai_marking_prompts")
        if isinstance(amp, dict):
            for k, v in amp.items():
                if isinstance(v, str) and MARKER not in v:
                    amp[k] = v + addition
                    prompts_touched += 1
                    touched = True

        pb = pd.get("problem_bank") or {}
        for tier in ("bronze", "silver", "gold"):
            for p in pb.get(tier) or []:
                if not isinstance(p, dict) or p.get("input_type") not in AI_TYPES:
                    continue
                sp = p.get("ai_system_prompt")
                if isinstance(sp, str) and sp and MARKER not in sp:
                    p["ai_system_prompt"] = sp + addition
                    problems_touched += 1
                    touched = True

        if touched and args.apply:
            backup[les["id"]] = get("lessons?select=practice_data&id=eq.%s" % les["id"])[0]["practice_data"]
            patch("lessons?id=eq.%s" % les["id"], {"practice_data": pd})
            wrote += 1
        elif touched:
            wrote += 1

    if args.apply and backup:
        io.open(os.path.join(HERE, "_backup_prompts_%s_%s.json" % (args.subject, args.unit)),
                "w", encoding="utf-8").write(json.dumps(backup))

    print("%s/%s: %d lesson prompts + %d problem prompts %s across %d lesson(s)"
          % (args.subject, args.unit, prompts_touched, problems_touched,
             "UPDATED" if args.apply else "would update", wrote))


if __name__ == "__main__":
    main()
