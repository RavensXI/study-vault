# -*- coding: utf-8 -*-
"""Build MCQs from the excerpt facts and blind-verify every question with the
Gemini machine ear. Outputs questions.json (verified/flagged per question).

Usage: python scripts/music-practice/verify_bank.py <bank_dir>
"""
import base64
import io
import json
import os
import random
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KEY = os.environ["GEMINI_API_KEY"]

OPTIONS = {
    "metre": ["simple time, in 2 or 4", "simple triple time, in 3", "compound time (6/8)"],
    "tonality": ["major", "minor", "pentatonic", "chromatic"],
    "cadence": ["perfect", "imperfect", "plagal", "interrupted"],
    "texture": ["monophonic", "melody and accompaniment", "imitative polyphony", "unison"],
    "device": ["sequence", "ostinato", "drone", "imitation"],
    "instrument_family": ["strings", "woodwind", "brass", "percussion"],
    "bass_rhythm": ["syncopated bass", "straight bass", "walking bass", "dotted rhythm bass"],
}
PROMPTS = {
    "metre": "What is the metre of this excerpt?",
    "tonality": "What is the tonality of this excerpt?",
    "cadence": "What cadence ends this excerpt?",
    "texture": "Which best describes the texture?",
    "device": "Which melodic/accompaniment device features in this excerpt?",
    "instrument_family": "Which instrument family plays the main melody?",
    "bass_rhythm": "Which best describes the bass line's rhythm?",
}
SECONDARY = {  # topic -> extra facts worth asking about
    "metre": ["instrument_family"],
    "tonality": ["instrument_family"],
    "cadence": ["tonality"],
    "texture": ["instrument_family"],
    "device": ["instrument_family"],
    "pop": ["bass_rhythm", "tonality"],
}


def ask(audio_b64, question, options):
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "audio/mp3", "data": audio_b64}},
        {"text": "Listen carefully to this short music excerpt, then answer.\n" + question + "\n"
                 + "\n".join("%s. %s" % (chr(65 + i), o) for i, o in enumerate(options))
                 + "\nReply in the exact format: ANSWER: <letter> - <one short reason>"}]}]}
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + KEY,
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(3):
        try:
            out = json.load(urllib.request.urlopen(req, timeout=120))
            text = out["candidates"][0]["content"]["parts"][0]["text"]
            m = re.search(r"ANSWER:\s*([A-Z])", text)
            return (m.group(1) if m else "?"), text.strip()[:120]
        except Exception as e:
            if attempt == 2:
                return "ERR", str(e)[:100]
            time.sleep(10)


def main(bank_dir):
    facts = json.load(io.open(os.path.join(bank_dir, "facts.json"), encoding="utf-8"))
    rng = random.Random(42)
    questions = []
    agree = flagged = 0
    for f in facts:
        audio_b64 = base64.b64encode(open(os.path.join(bank_dir, f["id"] + ".mp3"), "rb").read()).decode()
        fact_keys = [f["topic"] if f["topic"] != "pop" else "bass_rhythm"]
        fact_keys += [k for k in SECONDARY.get(f["topic"], []) if k in f and k not in fact_keys]
        for fk in fact_keys:
            truth = f.get(fk)
            if fk == "metre":
                truth = {"simple duple (2/4)": "simple time, in 2 or 4",
                         "simple quadruple (4/4)": "simple time, in 2 or 4",
                         "simple triple (3/4)": "simple triple time, in 3",
                         "compound duple (6/8)": "compound time (6/8)"}.get(truth, truth)
            if fk == "instrument_family" and f.get("instrument") in ("horn", "cello", "oboe"):
                continue  # FluidR3 timbres too ambiguous for family questions
            if truth not in (OPTIONS.get(fk) or []):
                continue
            opts = list(OPTIONS[fk])
            if truth == 'pentatonic':
                opts = ['minor', 'pentatonic', 'chromatic', 'whole-tone']
            votes = []
            last_why = ""
            for trial in range(3):
                topts = list(opts)
                rng.shuffle(topts)
                letter, why = ask(audio_b64, PROMPTS[fk], topts)
                gi = (ord(letter) - 65) if len(letter) == 1 else -1
                votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
                last_why = why
            n_truth = votes.count(truth)
            from collections import Counter as _C
            top, top_n = _C(votes).most_common(1)[0]
            if n_truth >= 2:
                status = "verified"
            elif top_n >= 2 and top != truth:
                status = "flagged-consistent"   # machine consistently hears something else
            else:
                status = "flagged-ambiguous"    # machine flip-flops: perceptually unclear
            agree += 1 if status == "verified" else 0
            flagged += 0 if status == "verified" else 1
            rng.shuffle(opts)
            questions.append({"excerpt": f["id"], "fact": fk, "question": PROMPTS[fk],
                              "options": opts, "correct": opts.index(truth), "truth": truth,
                              "votes": votes, "gemini_why": last_why, "status": status})
            print("%s %-18s truth=%-26s votes=%s %s" % (
                f["id"], fk, truth, "/".join(v[:14] for v in votes),
                "OK" if status == "verified" else "<-- " + status.upper()), flush=True)
    io.open(os.path.join(bank_dir, "questions.json"), "w", encoding="utf-8").write(
        json.dumps(questions, ensure_ascii=False, indent=1))
    print("\nTOTAL: %d questions, %d verified, %d flagged" % (len(questions), agree, flagged))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\tshau\.claude\jobs\4059242c\tmp\music_bank")
