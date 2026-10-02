"""Preview: the preview lessons' narration re-voiced with Microsoft's MAI voices (Tom, 2 Oct 2026).

Odd lesson -> en-GB-Harry:MAI-Voice-2.1-Flash, even -> en-GB-Emily:MAI-Voice-2.1-Flash, synthesised on
the Foundry resource (these British MAI voices are not in Azure's voice list, but answer there).
Same chunks and ids as the live pipeline (lib/narration.extract_narration_chunks over content_html,
exam_tip_html and conclusion_html), same foreign-word SSML. Audio goes to NEW R2 keys only
(preview/mai-voice/...), never over live audio; the manifest ships in the branch as
transcripts/<s>/<u>/lNN.narration-mai.json, which js/podcast-extras.js prefers when it exists.
Read-only database reads.

  python scripts/build_mai_narration_preview.py
"""
import json, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_podcast_transcripts as B
from lib.narration import extract_narration_chunks, _build_ssml_body, get_mp3_duration
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET

VOICES = {1: "en-GB-Harry:MAI-Voice-2.1-Flash", 0: "en-GB-Emily:MAI-Voice-2.1-Flash"}
STATS = os.path.join(HERE, "_mai_narration_preview_stats.json")


def tts_url():
    res = re.sub(r"^https://([^.]+)\..*$", r"\1", B.gv("FOUNDRY_ENDPOINT").rstrip("/"))
    return "https://%s.cognitiveservices.azure.com/tts/cognitiveservices/v1" % res


def synth(text, voice, lang_code, log):
    body = _build_ssml_body(text, lang_code)
    ssml = ("<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' "
            "xml:lang='en-GB'><voice name='%s'>%s</voice></speak>" % (voice, body))
    for attempt in range(6):
        try:
            req = urllib.request.Request(tts_url(), data=ssml.encode("utf-8"), method="POST", headers={
                "Ocp-Apim-Subscription-Key": B.gv("FOUNDRY_KEY"), "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3", "User-Agent": "StudyVault-narration-preview"})
            data = urllib.request.urlopen(req, timeout=120).read()
            if data: return data
        except urllib.error.HTTPError as e:
            log["errors"].append(e.code)
            if e.code not in (429, 500, 502, 503, 504): raise
        except Exception as e:
            log["errors"].append(str(e)[:60])
        time.sleep(min(30, 2 * 2 ** attempt))
    raise RuntimeError("gave up after 6 tries")


def main():
    r2 = get_r2_client()
    stats = []
    for s, u, n in B.PREVIEW:
        L = B.rest("lessons?select=id,title,content_html,exam_tip_html,conclusion_html,narration_manifest,"
                   "units!inner(slug,subjects!inner(slug,school_id,settings))&units.slug=eq.%s&units.subjects.slug=eq.%s"
                   "&units.subjects.school_id=is.null&lesson_number=eq.%d&limit=1" % (u, s, n))[0]
        lang = ((L["units"]["subjects"].get("settings") or {}).get("narration_lang")) or None
        texts = {}
        for f in ("content_html", "exam_tip_html", "conclusion_html"):
            for nid, txt in extract_narration_chunks(L.get(f) or "", lang_code=lang):
                texts.setdefault(nid, txt)
        live = L["narration_manifest"] or []
        voice = VOICES[n % 2]
        log = {"errors": []}
        out, chars, t0 = [], 0, time.time()
        for e in live:
            txt = texts.get(e["id"])
            if not txt:
                print("   no text for", e["id"], "- keeping live clip"); out.append(dict(e)); continue
            mp3 = synth(txt, voice, lang, log)
            chars += len(txt)
            key = "preview/mai-voice/%s/%s/narration_lesson-%02d_%s.mp3" % (s, u, n, e["id"])
            url = upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            ne = dict(e); ne["src"] = url; ne["duration"] = round(get_mp3_duration(mp3), 2)
            out.append(ne)
        path = os.path.join(ROOT, "transcripts", s, u, "l%02d.narration-mai.json" % n)
        json.dump(out, open(path, "w", encoding="utf-8"), indent=1)
        retried = sum(1 for x in log["errors"])
        stats.append({"lesson": "%s/%s/%d" % (s, u, n), "title": L["title"], "voice": voice, "chunks": len(out),
                      "chars": chars, "retries": retried, "errors": log["errors"][:20], "seconds": round(time.time() - t0)})
        print("%s/%s/%d  %s  %d chunks, %d chars, %d retries, %.0fs" % (s, u, n, voice, len(out), chars, retried, time.time() - t0))
    json.dump(stats, open(STATS, "w"), indent=1)
    tot = sum(x["chars"] for x in stats)
    print("total %d chars, about $%.2f at $15 per million" % (tot, tot * 15 / 1e6))


if __name__ == "__main__":
    main()
