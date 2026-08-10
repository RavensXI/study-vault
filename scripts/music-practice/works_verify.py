# -*- coding: utf-8 -*-
"""Machine-ear verification of the works-based western-classical lessons.

For each audio-verifiable MCQ: clip the cited time window from the real R2
recording (ffmpeg), then ask Gemini blind 3 times with shuffled options.
Statuses follow verify_bank.py: verified / flagged-consistent (machine
consistently hears otherwise) / flagged-ambiguous (votes scatter).

Works lessons are the weaker trust class (answers NOT true by construction),
so corroboration here is required before they ship.

Usage: python scripts/music-practice/works_verify.py
"""
import base64
import io
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client

TMP = r"C:\Users\tshau\.claude\jobs\4059242c\tmp\works_verify"
FFMPEG = "ffmpeg"
MODEL = "gemini-2.5-flash"
API = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"

# Audio-verifiable questions. window=(start_s, end_s) of the passage recording.
# lesson/tier/idx address the problem in the bank; prompt strips the listening
# harness so Gemini judges the music, not the wording.
CHECKS = [
    dict(l=1, t="gold", i=0, pid="beethoven-sym1-mvt1", win=(65, 105),
         prompt="Which combination of features best describes the character of this passage?"),
    dict(l=1, t="silver", i=0, pid="beethoven-sym1-mvt1", win=(0, 6),
         prompt="Which statement best describes the very first chord you hear?"),
    dict(l=2, t="bronze", i=0, pid="mozart-40-mvt1", win=(0, 30),
         prompt="What is the home key of this piece?"),
    dict(l=2, t="bronze", i=1, pid="mozart-40-mvt1", win=(0, 8),
         prompt="Which family of instruments plays the accompaniment at the very start, before the main melody enters?"),
    dict(l=2, t="silver", i=0, pid="mozart-40-mvt1", win=(0, 25),
         prompt="What feature of the main melody contributes most to its anxious, restless mood?"),
    dict(l=2, t="gold", i=0, pid="mozart-40-mvt1", win=(150, 210),
         prompt="This passage is from the development. How does the composer destabilise the home key here?"),
    dict(l=3, t="gold", i=0, pid="mozart-k622-mvt3", win=(0, 40),
         prompt="Which two features are most characteristic of the solo instrument's playing in this passage?"),
    # Suspected false premise: the keyed answer says orchestra strings introduce
    # the theme before the clarinet. Extra option lets the machine say clarinet.
    dict(l=3, t="silver", i=0, pid="mozart-k622-mvt3", win=(0, 30),
         prompt="What introduces the main theme at the very beginning of this movement?",
         options_override=["Solo flute and oboe in unison", "The full orchestra in a loud statement",
                           "The orchestra strings, playing the theme quietly", "Brass and timpani alone",
                           "The solo clarinet"]),
    dict(l=4, t="bronze", i=1, pid="haydn-sym94-mvt2", win=(18, 35),
         prompt="A famous musical event happens partway through this clip. What is it?"),
    dict(l=4, t="silver", i=0, pid="haydn-sym94-mvt2", win=(0, 35),
         prompt="How is the opening theme structured?"),
    dict(l=4, t="silver", i=1, pid="haydn-sym94-mvt2", win=(0, 15),
         prompt="Which section of the orchestra opens the theme?"),
    dict(l=5, t="bronze", i=1, pid="handel-zadok", win=(0, 90),
         prompt="How do the dynamics change during this orchestral passage?"),
    dict(l=5, t="silver", i=0, pid="handel-zadok", win=(75, 115),
         prompt="When the choir enters in this clip, what describes the texture best?"),
    dict(l=5, t="silver", i=1, pid="handel-zadok", win=(60, 110),
         prompt="Which of the following does NOT happen in this passage?"),
    dict(l=5, t="gold", i=0, pid="handel-zadok", win=(40, 130),
         prompt="This clip spans the end of the orchestral prelude and the choral entry. Which statement most accurately describes the textural shift?"),
    dict(l=6, t="silver", i=0, pid="chopin-nocturne-op9-no2", win=(0, 105),
         prompt="The main theme is heard more than once in this clip. What happens to the ornamentation when the theme returns?"),
    dict(l=7, t="silver", i=0, pid="schumann-traumerei", win=(0, 35),
         prompt="How is the opening melody organised?"),
    dict(l=7, t="silver", i=1, pid="schumann-foreign-lands", win=(0, 30),
         prompt="Which describes the texture?"),
    dict(l=8, t="bronze", i=1, pid="verdi-dies-irae", win=(0, 12),
         prompt="Which word best describes the rhythm of this orchestral opening?"),
    dict(l=8, t="silver", i=1, pid="verdi-dies-irae", win=(5, 45),
         prompt="When the chorus enters, how do the voice parts sing the opening text?"),
]


def gem(payload):
    key = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(API % (MODEL, key), data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r)
            return out["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                time.sleep(20 * (attempt + 1))
                continue
            raise


def ask(audio_b64, question, options):
    letters = "ABCDEFGH"
    optxt = "\n".join("%s) %s" % (letters[i], o) for i, o in enumerate(options))
    prompt = ("Listen to this audio clip carefully, then answer the multiple-choice question "
              "based ONLY on what you hear.\n\n%s\n\n%s\n\n"
              "Reply in EXACTLY this format:\nANSWER: <letter> — <one sentence why>" % (question, optxt))
    try:
        text = gem({"contents": [{"parts": [
            {"inline_data": {"mime_type": "audio/mp3", "data": audio_b64}},
            {"text": prompt}]}]})
        m = re.search(r"ANSWER:\s*([A-H])", text)
        return (m.group(1) if m else "ERR"), text.strip().splitlines()[0][:120]
    except Exception as e:
        return "ERR", str(e)[:120]


def main():
    os.makedirs(TMP, exist_ok=True)
    sb = get_client()
    subj = sb.from_("subjects").select("id").eq("slug", "music-aqa").is_("school_id", "null").execute().data[0]
    unit = sb.from_("units").select("id").eq("subject_id", subj["id"]).eq("slug", "western-classical-1650-1910").execute().data[0]
    lessons = {L["lesson_number"]: L for L in sb.from_("lessons").select(
        "id, lesson_number, practice_data").eq("unit_id", unit["id"]).execute().data}

    # passage audio URLs
    urls = {}
    for L in lessons.values():
        for p in L["practice_data"].get("passages", []):
            m = re.search(r'<audio[^>]+src="([^"]+)"', p.get("text", ""))
            if m:
                urls[p["id"]] = m.group(1)

    # download each needed recording once
    for pid in sorted({c["pid"] for c in CHECKS}):
        dest = os.path.join(TMP, pid + ".mp3")
        if not os.path.exists(dest):
            req = urllib.request.Request(urls[pid], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                f.write(r.read())
            print("downloaded", pid, os.path.getsize(dest) // 1024, "KB")

    rng = random.Random(42)
    results = []
    for c in CHECKS:
        pd = lessons[c["l"]]["practice_data"]
        prob = pd["problem_bank"][c["t"]][c["i"]]
        options = c.get("options_override") or prob["options"]
        truth = prob["options"][prob["solutions"][0]]
        clip = os.path.join(TMP, "%s_%d-%d.mp3" % (c["pid"], c["win"][0], c["win"][1]))
        if not os.path.exists(clip):
            subprocess.run([FFMPEG, "-y", "-loglevel", "error",
                            "-ss", str(c["win"][0]), "-to", str(c["win"][1]),
                            "-i", os.path.join(TMP, c["pid"] + ".mp3"),
                            "-c:a", "libmp3lame", "-b:a", "96k", clip], check=True)
        b64 = base64.b64encode(open(clip, "rb").read()).decode()
        votes, whys = [], []
        for trial in range(3):
            topts = list(options)
            rng.shuffle(topts)
            letter, why = ask(b64, c["prompt"], topts)
            gi = (ord(letter) - 65) if len(letter) == 1 else -1
            votes.append(topts[gi] if 0 <= gi < len(topts) else "?")
            whys.append(why)
        n_truth = votes.count(truth)
        top, top_n = Counter(votes).most_common(1)[0]
        if n_truth >= 2:
            status = "verified"
        elif top_n >= 2 and top != truth:
            status = "flagged-consistent"
        else:
            status = "flagged-ambiguous"
        results.append(dict(l=c["l"], t=c["t"], i=c["i"], pid=c["pid"], win=c["win"],
                            truth=truth, votes=votes, whys=whys, status=status))
        print("L%d %s[%d] %-22s truth=%-40s -> %s" % (
            c["l"], c["t"], c["i"], c["pid"][:22], truth[:40], status.upper()))
        if status != "verified":
            for v, w in zip(votes, whys):
                print("      vote: %-40s %s" % (str(v)[:40], w[:70]))

    io.open(os.path.join(TMP, "results.json"), "w", encoding="utf-8").write(
        json.dumps(results, indent=1))
    n = Counter(r["status"] for r in results)
    print("\nSUMMARY:", dict(n))


if __name__ == "__main__":
    main()
