# -*- coding: utf-8 -*-
"""Batch 1b: validate the A/B regenerated clips, pick the winner per prompt,
trim it, and re-verify on the trimmed audio. Question specs come from
validate_flow_batch.CLIPS (same questions the originals failed against).

Winner rule: most verified-with-clean-distractors questions; ties go to A.

Usage: python scripts/music-practice/run_flow_batch1b.py
"""
import base64
import glob
import io
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import works_verify as wv
from validate_flow_batch import CLIPS

DOWNLOADS = os.path.join(os.environ["USERPROFILE"], "Downloads")
OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\flow_batch1b"
BASES = ["aos3_african_fusion", "aos4_minimalism", "aos4_pastoral_orchestral", "aos4_dissonant_modern"]
WINDOW = 40


def validate(name, path, spec, rng):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    print("\n=== %s ===" % name)
    desc = wv.gem({"contents": [{"parts": [
        {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
        {"text": "Describe this music: genre/era it evokes, instruments and voices you hear, "
                 "and three notable musical features. Three sentences maximum."}]}]})
    desc = " ".join(desc.split())
    print("  DESC:", desc[:200])
    time.sleep(3)
    qres = []
    for question, options, truth_i in spec["questions"]:
        truth = options[truth_i]
        votes = []
        for _ in range(3):
            topts = list(options)
            rng.shuffle(topts)
            letter, why = wv.ask(b64, question, topts)
            gi = (ord(letter) - 65) if len(letter) == 1 else -1
            votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
            time.sleep(3)
        n_truth = votes.count(truth)
        top, top_n = Counter(votes).most_common(1)[0]
        status = ("verified" if n_truth >= 2
                  else "flagged-consistent" if top_n >= 2 and top != truth
                  else "flagged-ambiguous")
        flags = []
        if status == "verified":
            for opt in options:
                if opt == truth:
                    continue
                verdict = wv.gem({"contents": [{"parts": [
                    {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
                    {"text": "Consider this statement about the audio: \"%s\" (in answer to: %s)\n"
                             "Is the statement TRUE or FALSE of this audio? A statement that is even "
                             "partially or arguably true counts as TRUE. Reply EXACTLY: VERDICT: TRUE "
                             "or VERDICT: FALSE - one sentence why" % (opt, question)}]}]})
                if "VERDICT: TRUE" in verdict.upper().replace("**", ""):
                    flags.append(opt)
                time.sleep(3)
        qres.append({"q": question, "truth": truth, "votes": votes, "status": status,
                     "distractor_flags": flags})
        print("  %-9s %s%s" % (status.upper().replace("FLAGGED-", "FLAG:"), question[:58],
                               "  [%d flag]" % len(flags) if flags else ""))
    return {"description": desc, "questions": qres}


def main():
    os.makedirs(os.path.join(OUT, "trimmed"), exist_ok=True)
    rng = random.Random(31)
    results = {}

    # convert
    files = {}
    for base in BASES:
        for suffix in ("A", "B"):
            matches = glob.glob(os.path.join(DOWNLOADS, "%s_v2%s.*" % (base, suffix)))
            if not matches:
                print("MISSING:", base, suffix)
                continue
            mp3 = os.path.join(OUT, "%s_v2%s.mp3" % (base, suffix))
            if not os.path.exists(mp3):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", matches[0],
                                "-codec:a", "libmp3lame", "-b:a", "112k", mp3], check=True)
            files[(base, suffix)] = mp3

    for (base, suffix), path in sorted(files.items()):
        results["%s_v2%s" % (base, suffix)] = validate(
            "%s_v2%s" % (base, suffix), path, CLIPS[base], rng)

    # pick winners, trim, re-verify
    winners = {}
    for base in BASES:
        scores = {}
        for suffix in ("A", "B"):
            r = results.get("%s_v2%s" % (base, suffix))
            if not r:
                continue
            scores[suffix] = sum(1 for q in r["questions"]
                                 if q["status"] == "verified" and not q["distractor_flags"])
        if not scores:
            continue
        best = max(sorted(scores), key=lambda s: scores[s])
        winners[base] = best
        print("\nWINNER %s: v2%s (clean-verified counts: %s)" % (base, best, scores))

        src = files[(base, best)]
        dst = os.path.join(OUT, "trimmed", base + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "8", "-t", str(WINDOW),
                        "-i", src, "-codec:a", "libmp3lame", "-b:a", "112k",
                        "-af", "afade=t=in:d=0.5,afade=t=out:st=%d:d=1" % (WINDOW - 1), dst], check=True)
        b64 = base64.b64encode(open(dst, "rb").read()).decode()
        for q in results["%s_v2%s" % (base, best)]["questions"]:
            if q["status"] != "verified":
                continue
            truth, options = q["truth"], None
            for question, opts, ti in CLIPS[base]["questions"]:
                if question == q["q"]:
                    options = opts
                    break
            votes = []
            for _ in range(2):
                topts = list(options)
                rng.shuffle(topts)
                letter, why = wv.ask(b64, q["q"], topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                time.sleep(3)
            q["trim_verified"] = votes.count(truth) == 2
            print("  TRIM %s %s" % ("PASS" if q["trim_verified"] else "RECHECK", q["q"][:56]))

    io.open(os.path.join(OUT, "_batch1b_results.json"), "w", encoding="utf-8").write(
        json.dumps({"results": results, "winners": winners}, ensure_ascii=False, indent=1))
    print("\n==== DONE. winners:", winners, "====")


if __name__ == "__main__":
    main()
