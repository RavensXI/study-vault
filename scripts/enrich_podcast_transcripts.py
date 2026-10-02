"""Podcast extras built from the transcripts (Tom, 1 Oct 2026; preview branch podcast-transcripts).

For each lesson in build_podcast_transcripts.PREVIEW that has transcripts/<s>/<u>/lNN.json:
  lNN.factcheck.json  statements the hosts make that are wrong or contradict the lesson (staff only)
  lNN.study.json      chapters (4-8), lesson-section -> podcast moment matches (no quiz: Tom, 2 Oct 2026)
  lNN.video.vtt       captions for the lesson's explainer video (R2 .mp4), from MAI-Transcribe-2 word timings
  transcripts/index.json   search-inside-audio index for the dashboard finder

Claude calls go through the Claude Code subscription (claude -p, Opus), no API credit. Read-only
single-row database reads. Lesson audio/video only, no pupil data.

  python scripts/enrich_podcast_transcripts.py [factcheck|study|captions|index|all]
"""
import html, json, os, re, subprocess, sys, tempfile, time, urllib.request, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_podcast_transcripts as B

TDIR = os.path.join(ROOT, "transcripts")
SPEND = os.path.join(HERE, "_podcast_extras_spend.json")


def mmss(s):
    s = int(s); return "%d:%02d" % (s // 60, s % 60)


def lesson_row(s, u, n):
    return B.rest("lessons?select=id,title,content_html,youtube_video_id,units!inner(slug,subjects!inner(slug,school_id))"
                  "&units.slug=eq.%s&units.subjects.slug=eq.%s&units.subjects.school_id=is.null&lesson_number=eq.%d&limit=1" % (u, s, n))[0]


def plain(h):
    h = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", h or "")
    h = re.sub(r"<h([23])[^>]*>", lambda m: "\n\n## " if m.group(1) == "2" else "\n\n### ", h)
    h = re.sub(r"</(p|li|h2|h3|div)>", "\n", h)
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def headings(h):
    out = []
    for m in re.finditer(r"<h([23])([^>]*)>([\s\S]*?)</h\1>", h or ""):
        idm = re.search(r'id="([^"]+)"', m.group(2))
        out.append({"level": int(m.group(1)), "id": idm.group(1) if idm else None,
                    "text": html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()})
    return [x for x in out if x["text"]]


def transcript_text(tr):
    return "\n".join("[%s] %s: %s" % (mmss(t["start"]), "AB"[t["speaker"] - 1] if t["speaker"] in (1, 2) else "?", t["text"]) for t in tr["turns"])


def claude(system, user, model="opus"):
    p = os.path.join(tempfile.gettempdir(), "sv_pod_sys_%08x.txt" % (hash(system) & 0xffffffff))
    open(p, "w", encoding="utf-8").write(system)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    for _ in range(5):
        try:
            r = subprocess.run(["claude.cmd", "-p", "--model", model, "--output-format", "json", "--tools", "",
                                "--strict-mcp-config", "--setting-sources", "", "--system-prompt-file", p],
                               input=user, capture_output=True, text=True, encoding="utf-8", env=env, timeout=1200)
            out = json.loads(r.stdout)
            ledger = json.load(open(SPEND)) if os.path.exists(SPEND) else {"calls": 0, "usd_equiv": 0}
            ledger["calls"] += 1; ledger["usd_equiv"] = round(ledger["usd_equiv"] + (out.get("total_cost_usd") or 0), 4)
            json.dump(ledger, open(SPEND, "w"))
            txt = out.get("result") or ""
            m = re.search(r"\{[\s\S]*\}", txt)
            return json.loads(m.group(0))
        except FileNotFoundError:
            time.sleep(20)
        except Exception as e:
            print("   claude call failed:", str(e)[:160]); time.sleep(5)
    return None


FACT_SYS = """You fact-check a GCSE revision podcast against the lesson it accompanies. Two AI hosts (A and B) discuss the lesson; the transcript has [m:ss] times.
Flag only statements a GCSE examiner would treat as WRONG or that CONTRADICT the lesson text: wrong facts, dates, names, numbers, definitions, mistaken cause and effect, or claims the lesson says the opposite of. Do not flag style, simplification, jokes, rhetorical exaggeration, or extra correct detail the lesson does not mention. If something is not in the lesson but is correct general knowledge, do not flag it; if it is wrong general knowledge, flag it with severity "minor" or "major".
Return ONLY JSON: {"flags":[{"start":"m:ss","quote":"<exact words, <=30 words>","problem":"<one sentence>","lesson_says":"<what the lesson says, or 'not in the lesson'>","severity":"major|minor"}]}. An empty list is a valid answer."""

STUDY_SYS = """You build study aids from a GCSE revision podcast transcript (two AI hosts A and B, [m:ss] times) and its lesson.
Return ONLY JSON with two keys:
"chapters": 4 to 8 topic chapters covering the whole podcast in order: [{"start":"m:ss","title":"<plain title, max 6 words>"}]; the first starts at 0:00.
"sections": for each lesson heading given, the podcast moment that best explains it: [{"heading":"<exact heading text>","start":"m:ss","confidence":0.0-1.0}]. Use confidence >= 0.75 only when the podcast clearly discusses that heading's content at that time; otherwise give a low confidence. Plain British English, GCSE level."""


def secs(t):
    if isinstance(t, (int, float)): return float(t)
    p = [int(x) for x in str(t).strip().split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def each():
    for s, u, n in B.PREVIEW:
        path = os.path.join(TDIR, s, u, "l%02d.json" % n)
        if os.path.exists(path):
            yield s, u, n, path, json.load(open(path, encoding="utf-8"))


def do_factcheck():
    for s, u, n, path, tr in each():
        L = lesson_row(s, u, n)
        user = "LESSON: %s\n\n%s\n\nPODCAST TRANSCRIPT:\n%s" % (L["title"], plain(L["content_html"]), transcript_text(tr))
        res = claude(FACT_SYS, user) or {"flags": []}
        flags = []
        for f in res.get("flags", []):
            try: f["start"] = secs(f["start"])
            except Exception: continue
            flags.append(f)
        json.dump(flags, open(path.replace(".json", ".factcheck.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("factcheck %s/%s/%d: %d flags" % (s, u, n, len(flags)))


def do_study():
    for s, u, n, path, tr in each():
        L = lesson_row(s, u, n)
        hs = headings(L["content_html"])
        user = ("LESSON: %s\n\n%s\n\nLESSON HEADINGS:\n%s\n\nPODCAST TRANSCRIPT:\n%s"
                % (L["title"], plain(L["content_html"]), "\n".join("- " + h["text"] for h in hs), transcript_text(tr)))
        res = claude(STUDY_SYS, user)
        if not res: print("study failed", s, u, n); continue
        dur = tr["turns"][-1]["end"] if tr["turns"] else 0
        chapters = [{"start": secs(c["start"]), "title": c["title"]} for c in res.get("chapters", []) if secs(c["start"]) <= dur]
        byh = {h["text"]: h for h in hs}
        sections = [{"heading": x["heading"], "id": (byh.get(x["heading"]) or {}).get("id"), "start": secs(x["start"]),
                     "confidence": x.get("confidence", 0)} for x in res.get("sections", []) if x.get("heading") in byh]
        json.dump({"chapters": chapters, "sections": sections},
                  open(path.replace(".json", ".study.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("study %s/%s/%d: %d chapters, %d/%d sections confident" %
              (s, u, n, len(chapters), sum(1 for x in sections if x["confidence"] >= .75), len(hs)))


def vtt_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return "%02d:%02d:%06.3f" % (h, m, s)


def build_vtt(words, max_chars=42, max_dur=6.0):
    cues, line, lines, cs = [], "", [], None
    def flush(end):
        nonlocal lines, line, cs
        if line: lines.append(line)
        if lines: cues.append((cs, end, "\n".join(lines)))
        lines, line, cs = [], "", None
    last_end = 0
    for w in words:
        t, s0, e0 = w["text"], w["start"], w["end"]
        if cs is None: cs = s0
        if len(line) + len(t) + 1 > max_chars:
            lines.append(line); line = ""
            if len(lines) == 2: flush(last_end); cs = s0
        line = (line + " " + t).strip()
        last_end = e0
        if re.search(r"[.?!]$", t) and (len(lines) == 1 or e0 - cs > 2.5): flush(e0)
        elif e0 - (cs or s0) > max_dur: flush(e0)
    flush(last_end)
    return "WEBVTT\n\n" + "\n\n".join("%d\n%s --> %s\n%s" % (i + 1, vtt_time(a), vtt_time(b), txt) for i, (a, b, txt) in enumerate(cues)) + "\n"


def do_captions():
    for s, u, n, path, tr in each():
        L = lesson_row(s, u, n)
        v = L.get("youtube_video_id") or ""
        if not re.search(r"\.(mp4|webm)(\?|$)|studyvault-media\.co\.uk/|r2\.dev/", v):
            print("captions %s/%s/%d: no R2 video (%s)" % (s, u, n, v[:60] or "none")); continue
        tmp = tempfile.mkdtemp()
        src, dst = os.path.join(tmp, "v.mp4"), os.path.join(tmp, "a.mp3")
        open(src, "wb").write(B.fetch(v))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", dst], check=True)
        res_name = re.sub(r"^https://([^.]+)\..*$", r"\1", B.gv("FOUNDRY_ENDPOINT").rstrip("/"))
        url = "https://%s.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15" % res_name
        # modelOptions sit INSIDE enhancedMode (the docs' examples); outside it they are ignored
        definition = {"enhancedMode": {"enabled": True, "model": "MAI-Transcribe-2",
                                       "modelOptions": {"transcribeStyle": "clean", "timestamps": "word"}}, "locales": ["en"]}
        b = uuid.uuid4().hex
        body = (("--%s\r\nContent-Disposition: form-data; name=\"definition\"\r\n\r\n%s\r\n" % (b, json.dumps(definition))).encode()
                + ("--%s\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n" % b).encode()
                + open(dst, "rb").read() + ("\r\n--%s--\r\n" % b).encode())
        res = json.loads(urllib.request.urlopen(urllib.request.Request(url, data=body, method="POST", headers={
            "Ocp-Apim-Subscription-Key": B.gv("FOUNDRY_KEY"), "Content-Type": "multipart/form-data; boundary=" + b}), timeout=900).read())
        words = []
        for p in res.get("phrases", []):
            for w in p.get("words", []) or []:
                st = (w.get("offsetMilliseconds") or 0) / 1000.0
                words.append({"text": w.get("text", ""), "start": st, "end": st + (w.get("durationMilliseconds") or 0) / 1000.0})
        if not words: print("captions: no word timings returned", list(res.keys())); continue
        open(path.replace(".json", ".video.vtt"), "w", encoding="utf-8").write(build_vtt(words))
        print("captions %s/%s/%d: %d words, video %s" % (s, u, n, len(words), v[-50:]))


ENDS_SYS = """You mark where a GCSE revision podcast (two AI hosts) finishes explaining each lesson section, so a pupil can hear a clean clip of just that part.
You get the podcast as numbered paragraphs (turns) with start times, and for each lesson section its heading, a short extract of the lesson text, and the paragraph where the clip starts.
For each section, choose the LAST paragraph that is still about that section's topic: the hosts have finished the point and the next paragraph moves to something else (a new person, event, idea, or a recap of a different topic). The clip must end at the end of a paragraph, never mid-sentence, and should not cut off a host who is answering the other's question. Prefer a clip of 1 to 6 minutes; if the hosts return to the topic much later, ignore that.
Return ONLY JSON: {"ends":[{"heading":"<exact heading>","last_turn":<paragraph number>,"confidence":0.0-1.0}]}"""


def do_ends():
    for s, u, n, path, tr in each():
        spath = path.replace(".json", ".study.json")
        if not os.path.exists(spath): continue
        study = json.load(open(spath, encoding="utf-8"))
        turns = tr["turns"]
        L = lesson_row(s, u, n)
        lesson_txt = plain(L["content_html"])
        def first_turn(t):
            k = 0
            for i, x in enumerate(turns):
                if x["start"] <= t + 0.5: k = i
            return k
        secs_desc = []
        for x in study.get("sections", []):
            i = lesson_txt.find(x["heading"])
            extract = lesson_txt[i:i + 600] if i >= 0 else ""
            secs_desc.append("- %s (starts at paragraph %d)\n  %s" % (x["heading"], first_turn(x["start"]), extract.replace("\n", " ")))
        numbered = "\n".join("[%d] %s %s: %s" % (i, mmss(t["start"]), "AB"[t["speaker"] - 1] if t["speaker"] in (1, 2) else "?", t["text"]) for i, t in enumerate(turns))
        res = claude(ENDS_SYS, "LESSON SECTIONS:\n%s\n\nPODCAST PARAGRAPHS:\n%s" % ("\n".join(secs_desc), numbered)) or {"ends": []}
        by = {e.get("heading"): e for e in res.get("ends", [])}
        chapters = sorted(c["start"] for c in study.get("chapters", []))
        for x in study.get("sections", []):
            st = first_turn(x["start"])
            e = by.get(x["heading"])
            k = e.get("last_turn") if e else None
            ok = isinstance(k, int) and st <= k < len(turns) and turns[k]["end"] - x["start"] >= 20 and (e.get("confidence") or 0) >= 0.5
            if ok:
                x["end"] = turns[k]["end"]; x["end_src"] = "claude"
            else:   # fall back: the paragraph that ends just before the next chapter starts
                nxt = next((c for c in chapters if c > x["start"] + 20), None)
                kk = max([i for i, t in enumerate(turns) if nxt is None or t["start"] < nxt] or [len(turns) - 1])
                x["end"] = turns[kk]["end"]; x["end_src"] = "next chapter"
            print("   %-45s %s -> %s (%s)" % (x["heading"][:45], mmss(x["start"]), mmss(x["end"]), x["end_src"]))
        json.dump(study, open(spath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ends %s/%s/%d done" % (s, u, n))


def do_index():
    idx = []
    for s, u, n, path, tr in each():
        for t in tr["turns"]:
            if len(t["text"]) >= 40:
                idx.append({"p": "/lesson/%s/%s/%d" % (s, u, n), "l": tr.get("lesson", ""), "t": int(t["start"]), "x": t["text"]})
    json.dump(idx, open(os.path.join(TDIR, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("index: %d passages" % len(idx))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in (("factcheck", do_factcheck), ("study", do_study), ("ends", do_ends), ("captions", do_captions), ("index", do_index)):
        if what in (name, "all"): fn()
    if os.path.exists(SPEND): print("subscription ledger:", open(SPEND).read())
