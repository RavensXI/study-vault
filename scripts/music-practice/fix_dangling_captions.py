# -*- coding: utf-8 -*-
"""Fix the 41 dangling 'what to listen for' captions (Tom's review find,
16 Aug). The dead-listen-box conversion kept captions verbatim; the
originals ended ': what to listen for' with nothing following. Each
caption now gets a short work-specific pointer, and because captions are
narrated, the affected clips are REGENERATED surgically (same R2 key —
music-ocr's copied film manifests point at the same files, so one
regeneration heals both subjects; durations updated in both manifests).

Run: python fix_dangling_captions.py [--apply]
Backup: _backup_dangling_captions_2026-08-16.json
"""
import html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET
from lib.narration import (generate_audio_rest, get_mp3_duration,
                           get_voice_for_lesson)

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_dangling_captions_2026-08-16.json")

# caption key-fragment -> pointer. Keyed by a distinctive substring of the
# caption; per-lesson override where the same work serves different topics.
POINTERS = {
    "Billie Jean": "the bassline riff running almost throughout, and how "
                   "the verse lifts into the chorus hook",
    "Don&rsquo;t Stop Believin": "the piano riff, the long build, and how "
                                 "late the chorus hook finally arrives",
    "Someone Like You": "melody-and-accompaniment texture at its purest: "
                        "solo voice over piano alone",
    "Mundian To Bach Ke": "the dhol&rsquo;s swung chaal groove driving "
                          "under the twangy tumbi riff",
    "Gur Nalo Ishq Mitha": "the dhol strokes and the call-and-response "
                           "between voice and instruments",
    "remix productions of traditional Punjabi": "how programmed beats and "
                          "production wrap around traditional vocals",
    "Brimful of Asha": "the drone-flavoured riff and steady indie groove "
                       "around the repeated hook",
    "Imperial March": "the snarling low-brass theme and the relentless "
                      "march tread beneath it",
    "(Jaws)": "the two-note ostinato building dread through speed and "
              "dynamics",
    "Jaws (main theme)": "the two-note ostinato building dread through "
                         "speed and dynamics",
    "(Psycho)": "the stabbing, shrieking string glissandi &mdash; terror "
                "from strings alone",
    "Psycho (shower scene cue)": "the stabbing, shrieking string "
                "glissandi &mdash; terror from strings alone",
    "the Shire theme": "the folk-like melody on solo whistle over warm, "
                       "settled strings",
    "Jurassic Park (main theme)": "the broad, hymn-like horn melody and "
                       "the orchestral swell behind it",
    "Eine kleine Nachtmusik": "the opening in bold unison &mdash; every "
                       "player on the same line &mdash; before melody "
                       "and accompaniment separate",
    "Trout": "the theme passing between instruments as each variation "
             "re-dresses it",
    "Op. 20 No. 2": "four independent lines in strict counterpoint "
                    "&mdash; try following the cello",
    "Debussy, String Quartet": "the pizzicato textures and layered "
                    "cross-rhythms",
    "So What": "the bass stating the theme, answered by piano and horns, "
               "then walking behind the solos",
    "Now&rsquo;s the Time": "the riff-based head over the rhythm section, "
               "then improvised choruses over the same 12-bar changes",
    "St Louis Blue": "the 12-bar pattern underneath and the "
               "call-and-response between voice and cornet",
    "It Don&rsquo;t Mean a": "the swing feel in the rhythm section and "
               "the call-and-response between the band&rsquo;s sections",
    "One Day More": "each character&rsquo;s melody entering in turn and "
               "layering into the ensemble climax",
    "Tonight&rsquo; (Quintet)": "five vocal lines with distinct material "
               "combining over the pit orchestra",
    "Emperor": "the hymn-like theme and its decorated variations shared "
               "around the quartet",
    "Nielsen, Wind Quintet": "five distinct wind colours combining into "
               "a full ensemble texture",
    "Rondo alla Turca": "the recurring main theme returning between "
               "contrasting episodes &mdash; count its returns",
    "Nimrod": "how the theme&rsquo;s shape survives while harmony, "
              "dynamics and scoring transform it",
    "Surprise&rsquo;, third movement": "the sturdy dance metre, and the "
              "contrasting trio before the minuet returns",
    "Pachelbel": "the endlessly repeating bass and the violins entering "
              "one by one in strict imitation above it",
    "Hallelujah": "the texture switching between massive homophonic "
              "blocks and imitative entries",
    "Toccata and Fugue": "the dramatic solo flourishes, then the fugue "
              "subject entering voice by voice",
}
# per-lesson override: Let It Be serves cadences in aos1 L2, structure in aos4 L1
LET_IT_BE = {
    ("aos1-forms-and-devices", 2): "the perfect and plagal cadences that "
                                   "close its phrases &mdash; harmonic "
                                   "punctuation you can sing",
    ("aos4-popular-music", 1): "the verse-chorus frame, and where the "
                               "middle eight and outro depart from it",
}


def pointer_for(caption, uslug, num):
    if "Let It Be" in caption:
        return LET_IT_BE.get((uslug, num))
    for frag, p in POINTERS.items():
        if frag in caption:
            return p
    return None


def main():
    sb = get_client()
    r2 = None if not APPLY else get_r2_client()
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in ("music-eduqas",
                                                    "music-ocr")}
    units = sb.table("units").select("id,slug,subject_id").execute().data
    backup, writes = {}, []
    regen = {}   # (subject, uslug, num) -> [(nid, new_text)]
    fixed = missed = 0
    for slug, sid in subs.items():
        for u in [x for x in units if x["subject_id"] == sid]:
            rows = sb.table("lessons").select(
                "id,lesson_number,content_html,narration_manifest") \
                .eq("unit_id", u["id"]).order("lesson_number").execute().data
            for l in rows:
                ch = l["content_html"] or ""
                changed = False
                for m in re.finditer(
                        r'<figure class="sv-embed"'
                        r'(?: data-narration-id="([^"]+)")?>.*?'
                        r'<figcaption class="sv-embed-cap">(.*?)'
                        r"</figcaption>", ch, re.S):
                    nid, cap = m.group(1), m.group(2)
                    if not re.search(r"what to listen for\s*$",
                                     re.sub(r"<[^>]+>", "", cap).strip()):
                        continue
                    p = pointer_for(cap, u["slug"], l["lesson_number"])
                    if not p:
                        missed += 1
                        print("!! no pointer: %s %s L%d: %s"
                              % (slug, u["slug"], l["lesson_number"],
                                 re.sub(r"<[^>]+>", "", cap)[:60]))
                        continue
                    newcap = re.sub(r"what to listen for\s*$", p,
                                    cap.rstrip())
                    ch = ch.replace(m.group(0),
                                    m.group(0).replace(cap, newcap))
                    changed = True
                    fixed += 1
                    if nid:
                        regen.setdefault((slug, u["slug"], l["lesson_number"],
                                          l["id"]), []).append(
                            (nid, html.unescape(
                                re.sub(r"<[^>]+>", "", newcap))))
                if changed:
                    backup[l["id"]] = l["content_html"]
                    writes.append((l["id"], ch))
    print("\ncaptions fixed: %d | no-pointer misses: %d | lessons: %d"
          % (fixed, missed, len(writes)))
    print("clips to regenerate: %d"
          % sum(len(v) for v in regen.values()))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    # regenerate narration clips in place (same R2 key = heals every
    # subject sharing the file); update durations in the owning manifest
    for (slug, uslug, num, lid), items in regen.items():
        row = sb.table("lessons").select("narration_manifest") \
            .eq("id", lid).execute().data[0]
        man = row["narration_manifest"] or []
        voice, _ = get_voice_for_lesson(num)
        for nid, text in items:
            entry = next((c for c in man if c["id"] == nid), None)
            if not entry:
                print("  ! %s %s L%d %s: no manifest entry" % (slug, uslug,
                                                               num, nid))
                continue
            mp3 = generate_audio_rest(text, voice)
            if mp3 is None:
                print("  ! %s %s L%d %s: TTS failed" % (slug, uslug, num,
                                                        nid))
                continue
            key = entry["src"].split(".r2.dev/")[-1]
            upload_bytes_to_r2(r2, AUDIO_BUCKET, key, mp3, "audio/mpeg")
            entry["duration"] = get_mp3_duration(mp3)
        sb.table("lessons").update({"narration_manifest": man}) \
            .eq("id", lid).execute()
        print("  regenerated %d clip(s): %s %s L%d" % (len(items), slug,
                                                       uslug, num))
    print("applied.")


if __name__ == "__main__":
    main()
