# -*- coding: utf-8 -*-
"""Cut real listening excerpts from the eight cleared public-domain recordings.

Task #46. Generated clips are too clean and Tom cannot verify them by ear. Real
recordings of NAMED works make the answer a documented fact instead: Mozart 40
IS in G minor, checkable in any score.

Windows are chosen so the feature is unambiguous and nothing competes — in
particular the Beethoven window deliberately skips the Adagio introduction,
whose whole joke is that the key is NOT yet established.

Source files are already provenanced in AUDIO_PROVENANCE.md; these are trims of
audio we already host, so no new licence question arises.

    python make_real_excerpts.py --dry-run
    python make_real_excerpts.py
"""
import hashlib, json, os, subprocess, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.r2 import get_r2_client, upload_bytes_to_r2, AUDIO_BUCKET, AUDIO_PUBLIC_URL

SRC = AUDIO_PUBLIC_URL + "/music-aqa/western-classical-1650-1910/%s"
DEST = "music-aqa/listening-skills/real/%s"
MANIFEST = os.path.join(HERE, "_real_excerpts.json")

# name, source file, start, length, what it demonstrates, the work (for explanations)
CUTS = [
    ("real_major_beethoven", "lesson-01.mp3", 118, 16, "major",
     "Beethoven, Symphony No.1 in C major, Op.21 — Allegro con brio",
     "Window starts after the Adagio introduction, whose opening chord deliberately withholds "
     "the home key. From here C major is unambiguous."),
    ("real_minor_mozart40", "lesson-02.mp3", 2, 16, "minor",
     "Mozart, Symphony No.40 in G minor, K.550 — opening theme",
     "The famous first-subject theme, unmistakably minor from the first bar."),
    ("real_major_k622", "lesson-03.mp3", 3, 16, "major",
     "Mozart, Clarinet Concerto in A major, K.622 — rondo theme",
     "The solo clarinet states the rondo theme in A major."),
    ("real_major_haydn94", "lesson-04.mp3", 2, 16, "major",
     "Haydn, Symphony No.94 in G major — Andante theme",
     "Quiet strings, but the G major tonality is clear. Window ends well before the "
     "fortissimo chord at 0:42 so that surprise is not spoiled."),
    ("real_minor_verdi", "lesson-08.mp3", 2, 14, "minor",
     "Verdi, Requiem — Dies Irae",
     "Full chorus and orchestra in G minor; the minor tonality drives the whole movement."),
    ("real_major_chopin", "lesson-06.mp3", 4, 16, "major",
     "Chopin, Nocturne in E flat major, Op.9 No.2",
     "E flat major, and a textbook melody-and-accompaniment texture."),
    # textures
    ("real_tex_melacc_chopin", "lesson-06.mp3", 20, 16, "melody and accompaniment",
     "Chopin, Nocturne in E flat major, Op.9 No.2",
     "Right-hand melody over left-hand broken chords — the clearest melody-and-accompaniment "
     "on the cleared set."),
    ("real_tex_homophonic_zadok", "lesson-05.mp3", 100, 16, "homophonic",
     "Handel, Zadok the Priest",
     "The full choir enters around 1:36 in a block of chords moving together — homophony."),
    ("real_tex_homophonic_verdi", "lesson-08.mp3", 20, 15, "homophonic",
     "Verdi, Requiem — Dies Irae",
     "Chorus and orchestra hammering the same rhythm together — homophony at full force, a "
     "deliberate contrast with Handel's."),
    ("real_tex_melacc_traumerei", "lesson-07.mp3", 3, 16, "melody and accompaniment",
     "Schumann, Kinderszenen No.7 'Träumerei'",
     "A singing melody supported by quiet chords beneath it."),
]


def main():
    dry = "--dry-run" in sys.argv
    r2 = None if dry else get_r2_client()
    out, seen = [], {}
    for name, src, start, dur, feature, work, why in CUTS:
        tmp = os.path.join(tempfile.gettempdir(), "src_" + src)
        if not os.path.exists(tmp):
            req = urllib.request.Request(SRC % src, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=180) as r, open(tmp, "wb") as f:
                f.write(r.read())
        cut = os.path.join(tempfile.gettempdir(), name + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-ss", str(start), "-t", str(dur),
                        "-i", tmp, "-ac", "1", "-ar", "44100", "-b:a", "96k",
                        "-af", "afade=t=in:st=0:d=0.4,afade=t=out:st=%s:d=0.5" % (dur - 0.5),
                        cut], check=True)
        data = open(cut, "rb").read()
        h = hashlib.md5(data).hexdigest()
        assert h not in seen, "%s is identical to %s" % (name, seen.get(h))
        seen[h] = name
        assert len(data) > 20000, "%s came out suspiciously small" % name
        url = AUDIO_PUBLIC_URL + "/" + DEST % (name + ".mp3")
        if not dry:
            upload_bytes_to_r2(r2, AUDIO_BUCKET, DEST % (name + ".mp3"), data, "audio/mpeg")
        out.append({"id": name, "url": url, "feature": feature, "work": work,
                    "why": why, "source": src, "start": start, "dur": dur,
                    "md5": h, "bytes": len(data)})
        print("  %-28s %-26s %5.1f KB  %s" % (name, feature, len(data) / 1024.0, work[:38]))

    if not dry:
        json.dump(out, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\nmanifest ->", MANIFEST)
    print(("DRY RUN — nothing uploaded. " if dry else "") + "%d excerpts" % len(out))


if __name__ == "__main__":
    main()
