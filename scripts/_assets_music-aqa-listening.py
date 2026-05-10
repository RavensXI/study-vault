# -*- coding: utf-8 -*-
"""
Phase 4 asset pipeline -- music-aqa Listening v1
================================================
Downloads audio and score images for the 8 Unit 1 (western-classical-1650-1910)
lessons and writes a manifest to scripts/_assets_music-aqa-listening.json.

Sources:
  Audio  — Wikimedia Commons (direct upload.wikimedia.org URLs)
  Scores — Wikimedia Commons static PNG/JPG files (PD)

Rules:
  - NO IMSLP scraping
  - NO FluidSynth / MIDI rendering
  - Real PD score images only — if Commons has none, flag as no_pd_image_available
  - Audio transcoded to MP3 128 kbps stereo via ffmpeg
  - Score PNGs resized to ≤ 1400px longest dimension, uploaded to studyvault-images
  - Audio uploaded to studyvault-audio
  - Script is re-runnable (skips if R2 key already exists)

Usage:
    python scripts/_assets_music-aqa-listening.py
    python scripts/_assets_music-aqa-listening.py --skip-upload   # dry-run, no R2
    python scripts/_assets_music-aqa-listening.py --lesson 3       # single lesson
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows (cp1252 default can't encode music symbols).
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Repo root and path setup
REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from lib.r2 import (
    AUDIO_BUCKET, AUDIO_PUBLIC_URL,
    IMAGES_BUCKET, IMAGES_PUBLIC_URL,
    get_r2_client, upload_bytes_to_r2,
)

# ── Constants ─────────────────────────────────────────────────────────────
UNIT_SLUG   = "western-classical-1650-1910"
R2_AUDIO_PREFIX  = f"music-aqa/{UNIT_SLUG}"
R2_IMAGES_PREFIX = f"music-aqa/{UNIT_SLUG}"
SCORE_MAX_PX = 1400   # longest dimension cap for score images

MANIFEST_PATH = SCRIPTS_DIR / "_assets_music-aqa-listening.json"


# ── Lesson definitions ────────────────────────────────────────────────────
#
# lesson_id values come from the Phase 2 Supabase shell inserts — update here
# if the IDs change.  They are used only in the output manifest; the audio/score
# upload itself uses the numeric lesson_number.
#
# audio_url     : direct upload.wikimedia.org download URL
# audio_fmt     : source format extension (opus/ogg/oga/flac)
# audio_licence : short licence string
# audio_attribution : full attribution string (required for CC tracks)
# audio_duration_s  : seconds (from Commons file page)
#
# score_url     : direct upload.wikimedia.org download URL (None = not available)
# score_source  : Commons file page URL
# score_shows   : human description of what bars/content the image shows

LESSONS = [
    {
        "lesson_number": 1,
        "lesson_id": None,  # populated from Supabase shells in Phase 2
        "title": "Beethoven Symphony No.1, Movement 1: Slow Introduction and Sonata-Form Allegro",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/f/f4/"
            "Symphony_No._1_in_C_-_I._Adagio_molto%2C_Allegro_con_brio_-_Chamber_Orchestra_-_United_States_Marine_Band.opus"
        ),
        "audio_fmt": "opus",
        "audio_licence": "Public Domain",
        "audio_attribution": (
            "United States Marine Band, Marine Chamber Orchestra, "
            "cond. Capt. Ryan J. Nowlin (2019). U.S. federal government work, not subject to copyright."
        ),
        "audio_duration_s": 581,
        "score_url": (
            "https://upload.wikimedia.org/wikipedia/commons/9/99/"
            "Beethoven_1st_Symphony_1st_mov.png"
        ),
        "score_source": "https://commons.wikimedia.org/wiki/File:Beethoven_1st_Symphony_1st_mov.png",
        "score_shows": "Opening bars of Allegro con brio (first subject theme)",
        "score_licence": "Public Domain",
    },
    {
        "lesson_number": 2,
        "lesson_id": None,
        "title": "Mozart Symphony No.40, Movement 1: Sonata Form in G Minor",
        # Existing PoC audio at music-aqa/listening/mozart-40-mvt1.mp3 is kept.
        # We still download the Musopen FLAC as the canonical source and transcode
        # to the new key for consistency; if the target R2 key already exists it
        # will be skipped.
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/a/a8/"
            "Mozart_-_Symphony_No._40_in_G_minor%2C_K550_-_I._Molto_allegro_%28Musopen_Symphony%29.flac"
        ),
        "audio_fmt": "flac",
        "audio_licence": "Public Domain",
        "audio_attribution": "Musopen Symphony Orchestra. Released into the public domain by Musopen.",
        "audio_duration_s": 359,
        # CC0 public-domain score image from Commons
        "score_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/8c/"
            "Mozart-s40-part_I-FirstTheme.JPG"
        ),
        "score_source": "https://commons.wikimedia.org/wiki/File:Mozart-s40-part_I-FirstTheme.JPG",
        "score_shows": "Piano arrangement of the opening first-subject theme (Mvt 1)",
        "score_licence": "CC0 1.0 Universal Public Domain Dedication",
    },
    {
        "lesson_number": 3,
        "lesson_id": None,
        "title": "Mozart Clarinet Concerto K.622, Movement 3: Rondo Form",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/f/f2/"
            "Wolfgang_Amadeus_Mozart_-_Clarinet_Concerto_-_3._Allegro.ogg"
        ),
        "audio_fmt": "ogg",
        "audio_licence": "CC BY-SA 2.0",
        "audio_attribution": (
            "William McColl (basset clarinet) and the University of Washington Symphony Orchestra, "
            "cond. Abraham Kaplan (rec. December 1987, Al Goldstein collection / ibiblio.org). "
            "Licensed CC BY-SA 2.0."
        ),
        "audio_duration_s": 531,
        # No static score PNG found on Commons for this piece
        "score_url": None,
        "score_source": None,
        "score_shows": None,
        "score_licence": None,
        "score_status_note": "No static PD score image found on Wikimedia Commons for Mozart K.622 Mvt 3.",
    },
    {
        "lesson_number": 4,
        "lesson_id": None,
        "title": "Haydn Symphony No.94 'Surprise', Movement 2: Theme and Variations",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/4/42/"
            "Haydn%3B_Symphony_No._94_%22Surprise%22%2C_2._Andante.ogg"
        ),
        "audio_fmt": "ogg",
        "audio_licence": "Public Domain",
        "audio_attribution": (
            "Boston Symphony Orchestra, cond. Serge Koussevitzky (rec. 1929). "
            "Sound recording PD: published >50 years ago in the EU/UK."
        ),
        "audio_duration_s": 438,
        # No static score PNG found on Commons for Haydn Sym 94
        # (only a dynamically generated LilyPond score at an unstable /score/ URL)
        "score_url": None,
        "score_source": None,
        "score_shows": None,
        "score_licence": None,
        "score_status_note": (
            "Only dynamically-generated LilyPond score image found on Wikipedia (unstable /score/ URL). "
            "No static PD score image available on Wikimedia Commons."
        ),
    },
    {
        "lesson_number": 5,
        "lesson_id": None,
        "title": "Handel: Zadok the Priest — Coronation Anthem",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/b/b8/"
            "Handel_-_Zadok_the_Priest%2C_HWV_258_%28St_Matthew%27s_Concert_Choir%29.oga"
        ),
        "audio_fmt": "oga",
        "audio_licence": "CC BY 3.0",
        "audio_attribution": (
            "St Matthew's Concert Choir and Orchestra, dir. Damien Giromella (2013). "
            "Licensed under Creative Commons Attribution 3.0 Unported (CC BY 3.0)."
        ),
        "audio_duration_s": 362,
        # No static score PNG found on Commons for Handel Zadok
        "score_url": None,
        "score_source": None,
        "score_shows": None,
        "score_licence": None,
        "score_status_note": "No static PD score image found on Wikimedia Commons for Handel Zadok the Priest.",
    },
    {
        "lesson_number": 6,
        "lesson_id": None,
        "title": "Chopin: Nocturne in E♭ major, Op.9 No.2",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/8/89/"
            "Chopin_-_Nocturne_No._2_in_E-flat_major%2C_Op._9_No._2_%28Frank_Levy%29.flac"
        ),
        "audio_fmt": "flac",
        "audio_licence": "Public Domain",
        "audio_attribution": (
            "Frank Levy (piano). Released into the public domain by Musopen "
            "('Set Chopin Free' Kickstarter, 2014)."
        ),
        "audio_duration_s": 271,
        # Good static PD score PNG on Commons (878×493)
        "score_url": (
            "https://upload.wikimedia.org/wikipedia/commons/c/c2/"
            "Chopin_nocturne_op9_2a.png"
        ),
        "score_source": "https://commons.wikimedia.org/wiki/File:Chopin_nocturne_op9_2a.png",
        "score_shows": "First bars of the main theme (opening measures of Op.9 No.2)",
        "score_licence": "Public Domain (Creative Commons Public Domain Mark 1.0)",
    },
    {
        "lesson_number": 7,
        "lesson_id": None,
        "title": "Schumann: Kinderszenen Op.15 — Selected Pieces",
        # We download Träumerei (No.7) as the primary lesson audio.
        # Foreign Lands (No.1) is a short companion (1:52) — downloaded and uploaded
        # as a secondary asset (lesson-07b.mp3) so the Phase 3 content agent can
        # reference both.
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/0/06/"
            "Robert_Schumann_-_scenes_from_childhood%2C_op._15_-_vii._dreaming.ogg"
        ),
        "audio_fmt": "ogg",
        "audio_licence": "Public Domain",
        "audio_attribution": (
            "Donald Betts (piano) via Musopen. Released into the public domain by Musopen."
        ),
        "audio_duration_s": 203,  # 3:23
        # Secondary audio (Foreign Lands No.1)
        "audio_secondary_url": (
            "https://upload.wikimedia.org/wikipedia/commons/c/ce/"
            "Robert_Schumann_-_scenes_from_childhood%2C_op._15_-_i._of_foreign_lands_and_peoples.ogg"
        ),
        "audio_secondary_fmt": "ogg",
        "audio_secondary_duration_s": 112,  # 1:52
        # No usable notation PNG found (only a title-page JPG of the first edition)
        "score_url": None,
        "score_source": None,
        "score_shows": None,
        "score_licence": None,
        "score_status_note": (
            "Wikimedia Commons has only a title-page scan of the first edition — "
            "no notation excerpt PNG available."
        ),
    },
    {
        "lesson_number": 8,
        "lesson_id": None,
        "title": "Verdi: Requiem — 'Dies Irae'",
        "audio_url": (
            "https://upload.wikimedia.org/wikipedia/commons/b/b6/"
            "ICBSA_Verdi_-_Messa_da_requiem_parte_03%2C_Dies_irae.ogg"
        ),
        "audio_fmt": "ogg",
        "audio_licence": "CC BY-SA 4.0",
        "audio_attribution": (
            "Orchestra and Choir of Teatro Reale dell'Opera di Roma "
            "(historic ICBSA recording, La voce del padrone). "
            "Licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)."
        ),
        "audio_duration_s": 122,
        # Vreq.JPG shows Introit opening (Requiem movement), not Dies Irae — not pedagogically
        # correct for this lesson.  Flag as no_pd_image_available.
        "score_url": None,
        "score_source": None,
        "score_shows": None,
        "score_licence": None,
        "score_status_note": (
            "Vreq.JPG on Commons shows the Introit (Requiem) opening, not Dies Irae. "
            "No PD score image for the Dies Irae movement found on Wikimedia Commons."
        ),
    },
]

# ── Score-reading unit: reuse Unit 1 score images ─────────────────────────
#
# Four score-reading lessons (Unit 2).  Where a Unit 1 lesson has a score image,
# we reference that same R2 URL.  Where Unit 1 is audio-only, the score-reading
# lesson that planned to use it will also be marked as needing a substitute or
# being text-only for that excerpt.
#
# Format: list of dicts per lesson, each with a list of excerpts.

SCORE_READING_LESSONS = [
    {
        "lesson_number": 1,
        "title": "Reading Rhythm: Time Signatures, Note Values and Dotted Rhythms",
        "excerpts": [
            {
                "piece": "Mozart Symphony 40 Mvt 1 first subject",
                "reuses_unit1_lesson": 2,
                "bars": "bars 1-4 (anacrusis, quaver-driven motif, 4/4)",
                "key_feature": "Simple 4/4 time, anacrusis, quaver motif",
            },
            {
                "piece": "Beethoven Symphony 1 Mvt 1 Allegro con brio",
                "reuses_unit1_lesson": 1,
                "bars": "opening bars of Allegro (bars 13-20 approx)",
                "key_feature": "2/2 alla breve, dotted rhythms, sf accents",
            },
            {
                "piece": "Chopin Nocturne Op.9 No.2",
                "reuses_unit1_lesson": 6,
                "bars": "bars 1-4 (12/8 compound time, melody + arpeggios)",
                "key_feature": "12/8 compound time, melody and accompaniment",
            },
            {
                "piece": "Mozart Clarinet Concerto K.622 Mvt 3 — no image available",
                "reuses_unit1_lesson": 3,
                "bars": "bars 1-8 (6/8, dotted rhythms) — TEXT ONLY: no score image",
                "key_feature": "6/8 compound time — score image not available on Commons",
                "audio_only": True,
            },
        ],
    },
    {
        "lesson_number": 2,
        "title": "Reading Pitch: Key Signatures, Accidentals and Modulation",
        "excerpts": [
            {
                "piece": "Mozart Symphony 40 Mvt 1 (G minor / B♭ major modulation)",
                "reuses_unit1_lesson": 2,
                "bars": "bars 1-4 and transition area (2 flats, modulation)",
                "key_feature": "G minor key signature, modulation to relative major",
            },
            {
                "piece": "Beethoven Symphony 1 Mvt 1 introduction (C major / 'wrong key' opening)",
                "reuses_unit1_lesson": 1,
                "bars": "bars 1-4 (no sharps/flats but opens on V7/IV)",
                "key_feature": "C major, but opens on dominant seventh of subdominant",
            },
            {
                "piece": "Chopin Nocturne Op.9 No.2 opening (E♭ major, 3 flats)",
                "reuses_unit1_lesson": 6,
                "bars": "bars 1-4 (3 flats, chromatic appoggiaturas)",
                "key_feature": "E♭ major (3 flats), chromatic ornamentation",
            },
            {
                "piece": "Handel Zadok the Priest — no image available",
                "reuses_unit1_lesson": 5,
                "bars": "bars 1-8 (D major, 2 sharps) — TEXT ONLY",
                "key_feature": "D major (2 sharps) — score image not available on Commons",
                "audio_only": True,
            },
        ],
    },
    {
        "lesson_number": 3,
        "title": "Reading Expression: Dynamics, Articulation and Performance Direction",
        "excerpts": [
            {
                "piece": "Chopin Nocturne Op.9 No.2 (legato, slurs, p, espressivo)",
                "reuses_unit1_lesson": 6,
                "bars": "bars 1-8 (p dynamic, long legato slurs, phrase marks)",
                "key_feature": "Legato slurs, p dynamic, espressivo",
            },
            {
                "piece": "Beethoven Symphony 1 Mvt 1 (sf accents, crescendo)",
                "reuses_unit1_lesson": 1,
                "bars": "opening Allegro bars (sf, crescendo hairpin)",
                "key_feature": "sf accents, crescendo",
            },
            {
                "piece": "Mozart Symphony 40 Mvt 1 (p/f contrast, phrasing)",
                "reuses_unit1_lesson": 2,
                "bars": "bars 1-8 (p opening, sudden f at bar 5)",
                "key_feature": "Sudden dynamic contrast, phrase structure",
            },
            {
                "piece": "Haydn Symphony 94 Mvt 2 (pp vs ff 'Surprise') — no image available",
                "reuses_unit1_lesson": 4,
                "bars": "bars 13-20 (pp then sudden ff) — TEXT ONLY",
                "key_feature": "pp / sudden ff contrast — score image not available on Commons",
                "audio_only": True,
            },
        ],
    },
    {
        "lesson_number": 4,
        "title": "Reading the Orchestra: Clefs, Transpositions and Instrument Identification",
        "excerpts": [
            {
                "piece": "Mozart Symphony 40 Mvt 1 (full score: clarinets in B♭, strings, etc.)",
                "reuses_unit1_lesson": 2,
                "bars": "bars 1-4 (score order, transposing instruments visible)",
                "key_feature": "Full score layout, clarinets in B♭",
            },
            {
                "piece": "Beethoven Symphony 1 Mvt 1 (Classical orchestra layout)",
                "reuses_unit1_lesson": 1,
                "bars": "bars 1-4 (score layout: woodwind, brass, strings)",
                "key_feature": "Classical orchestra score order, bass clef strings",
            },
            {
                "piece": "Chopin Nocturne Op.9 No.2 (treble + bass clef piano grand staff)",
                "reuses_unit1_lesson": 6,
                "bars": "bars 1-4 (treble clef melody, bass clef arpeggios)",
                "key_feature": "Grand staff, treble and bass clef reading",
            },
            {
                "piece": "Handel Zadok the Priest (Baroque: oboes, strings, continuo) — no image",
                "reuses_unit1_lesson": 5,
                "bars": "bars 1-8 — TEXT ONLY",
                "key_feature": "Baroque instrumentation — score image not available on Commons",
                "audio_only": True,
            },
        ],
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────

def download_url(url: str, dest_path: str) -> None:
    """Download URL to dest_path with a descriptive User-Agent."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "StudyVault-AssetPipeline/1.0 (educational; contact studyvault.info@gmail.com)"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def transcode_to_mp3(src_path: str, dst_path: str) -> None:
    """Transcode src_path to MP3 128 kbps stereo via ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", src_path,
        "-vn",                  # no video
        "-ar", "44100",         # sample rate
        "-ac", "2",             # stereo
        "-b:a", "128k",         # bitrate
        "-f", "mp3",
        dst_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")


def resize_image_if_needed(img_bytes: bytes, max_px: int = SCORE_MAX_PX) -> bytes:
    """Resize image so longest dimension <= max_px. Returns bytes (JPEG)."""
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size
        if max(w, h) > max_px:
            ratio = max_px / max(w, h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            print(f"    Resized: {w}x{h} -> {new_w}x{new_h}")
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=85, optimize=True)
        return buf.getvalue()
    except ImportError:
        print("    WARNING: Pillow not installed; uploading original bytes.")
        return img_bytes


def r2_key_exists(r2_client, bucket: str, key: str) -> bool:
    """Return True if the R2 object already exists."""
    try:
        r2_client.head_object(Bucket=bucket, Key=key)
        return True
    except Exception:
        return False


# ── Main ──────────────────────────────────────────────────────────────────

def process_lesson(lesson: dict, r2_client, skip_upload: bool) -> dict:
    """Download, transcode, upload one lesson's audio (and score if available).
    Returns a manifest entry dict."""

    n = lesson["lesson_number"]
    print(f"\n-- Lesson {n}: {lesson['title'][:60]} --")

    audio_r2_key = f"{R2_AUDIO_PREFIX}/lesson-{n:02d}.mp3"
    score_r2_key = f"{R2_IMAGES_PREFIX}/lesson-{n:02d}-score.jpg"

    # ── Audio ────────────────────────────────────────────────────────────
    audio_result = {}
    with tempfile.TemporaryDirectory() as tmp:
        src_ext = lesson["audio_fmt"]
        src_file = os.path.join(tmp, f"source.{src_ext}")
        mp3_file = os.path.join(tmp, "lesson.mp3")

        if not skip_upload and r2_key_exists(r2_client, AUDIO_BUCKET, audio_r2_key):
            print(f"  Audio: already in R2 at {audio_r2_key} - skipping download")
            audio_url = f"{AUDIO_PUBLIC_URL}/{audio_r2_key}"
        else:
            print(f"  Audio: downloading {lesson['audio_url'][:80]}...")
            download_url(lesson["audio_url"], src_file)
            src_size_mb = os.path.getsize(src_file) / 1_048_576
            print(f"  Audio: {src_size_mb:.1f} MB downloaded. Transcoding to MP3 128k...")
            transcode_to_mp3(src_file, mp3_file)
            mp3_size_kb = os.path.getsize(mp3_file) // 1024
            print(f"  Audio: MP3 = {mp3_size_kb} KB")

            if skip_upload:
                audio_url = f"{AUDIO_PUBLIC_URL}/{audio_r2_key}  [NOT UPLOADED - dry run]"
                print(f"  Audio: dry run — would upload to {audio_r2_key}")
            else:
                print(f"  Audio: uploading to R2 {AUDIO_BUCKET}/{audio_r2_key}")
                with open(mp3_file, "rb") as f:
                    upload_bytes_to_r2(r2_client, AUDIO_BUCKET, audio_r2_key, f.read(), "audio/mpeg")
                audio_url = f"{AUDIO_PUBLIC_URL}/{audio_r2_key}"
                print(f"  Audio: uploaded -> {audio_url}")

        audio_result = {
            "url": audio_url,
            "r2_key": audio_r2_key,
            "attribution": lesson["audio_attribution"],
            "licence": lesson["audio_licence"],
            "duration_seconds": lesson["audio_duration_s"],
            "source_page": lesson["audio_url"],
        }

        # Secondary audio for lesson 7 (Foreign Lands)
        if lesson.get("audio_secondary_url"):
            sec_r2_key = f"{R2_AUDIO_PREFIX}/lesson-{n:02d}b.mp3"
            sec_ext = lesson["audio_secondary_fmt"]
            sec_src = os.path.join(tmp, f"source_b.{sec_ext}")
            sec_mp3 = os.path.join(tmp, "lesson_b.mp3")

            if not skip_upload and r2_key_exists(r2_client, AUDIO_BUCKET, sec_r2_key):
                print(f"  Audio (secondary): already in R2 - skipping")
                sec_url = f"{AUDIO_PUBLIC_URL}/{sec_r2_key}"
            else:
                print(f"  Audio (secondary): downloading {lesson['audio_secondary_url'][:80]}...")
                download_url(lesson["audio_secondary_url"], sec_src)
                transcode_to_mp3(sec_src, sec_mp3)
                if skip_upload:
                    sec_url = f"{AUDIO_PUBLIC_URL}/{sec_r2_key}  [NOT UPLOADED - dry run]"
                else:
                    with open(sec_mp3, "rb") as f:
                        upload_bytes_to_r2(r2_client, AUDIO_BUCKET, sec_r2_key, f.read(), "audio/mpeg")
                    sec_url = f"{AUDIO_PUBLIC_URL}/{sec_r2_key}"
                    print(f"  Audio (secondary): uploaded -> {sec_url}")

            audio_result["secondary"] = {
                "url": sec_url,
                "r2_key": sec_r2_key,
                "title": "Of Foreign Lands and Peoples (No.1)",
                "attribution": lesson["audio_attribution"],
                "licence": lesson["audio_licence"],
                "duration_seconds": lesson.get("audio_secondary_duration_s"),
            }

    # ── Score image ───────────────────────────────────────────────────────
    score_result = {}
    if not lesson.get("score_url"):
        score_result = {
            "status": "no_pd_image_available",
            "note": lesson.get("score_status_note", "No PD score image found on Wikimedia Commons."),
        }
        print(f"  Score: no PD image available - audio-only lesson for score questions")
    else:
        if not skip_upload and r2_key_exists(r2_client, IMAGES_BUCKET, score_r2_key):
            print(f"  Score: already in R2 at {score_r2_key} - skipping")
            score_url = f"{IMAGES_PUBLIC_URL}/{score_r2_key}"
        else:
            print(f"  Score: downloading {lesson['score_url'][:80]}...")
            with tempfile.TemporaryDirectory() as stmp:
                raw_file = os.path.join(stmp, "score_raw")
                download_url(lesson["score_url"], raw_file)
                raw_size_kb = os.path.getsize(raw_file) // 1024
                print(f"  Score: {raw_size_kb} KB raw. Resizing to max {SCORE_MAX_PX}px...")
                with open(raw_file, "rb") as f:
                    img_bytes = resize_image_if_needed(f.read(), SCORE_MAX_PX)
                final_size_kb = len(img_bytes) // 1024
                print(f"  Score: final {final_size_kb} KB")

                if skip_upload:
                    score_url = f"{IMAGES_PUBLIC_URL}/{score_r2_key}  [NOT UPLOADED - dry run]"
                    print(f"  Score: dry run — would upload to {score_r2_key}")
                else:
                    print(f"  Score: uploading to R2 {IMAGES_BUCKET}/{score_r2_key}")
                    upload_bytes_to_r2(r2_client, IMAGES_BUCKET, score_r2_key, img_bytes, "image/jpeg")
                    score_url = f"{IMAGES_PUBLIC_URL}/{score_r2_key}"
                    print(f"  Score: uploaded -> {score_url}")

        score_result = {
            "status": "ok",
            "url": score_url,
            "r2_key": score_r2_key,
            "source_page": lesson["score_source"],
            "shows_bars": lesson["score_shows"],
            "licence": lesson["score_licence"],
        }

    return {
        "lesson_id": lesson.get("lesson_id"),
        "lesson_number": n,
        "title": lesson["title"],
        "audio": audio_result,
        "score": score_result,
    }


def build_score_reading_manifest(unit1_manifest: dict) -> dict:
    """Build the score-reading unit manifest, referencing Unit 1 R2 URLs."""
    sr_manifest = {}
    for sr_lesson in SCORE_READING_LESSONS:
        lesson_num = sr_lesson["lesson_number"]
        excerpts = []
        for exc in sr_lesson["excerpts"]:
            reuses = exc.get("reuses_unit1_lesson")
            if reuses and str(reuses) in unit1_manifest:
                u1_score = unit1_manifest[str(reuses)].get("score", {})
                if u1_score.get("status") == "ok":
                    excerpts.append({
                        "piece": exc["piece"],
                        "url": u1_score["url"],
                        "bars": exc["bars"],
                        "key_feature": exc["key_feature"],
                        "source": u1_score.get("source_page"),
                    })
                else:
                    excerpts.append({
                        "piece": exc["piece"],
                        "status": "no_pd_image_available",
                        "bars": exc["bars"],
                        "key_feature": exc["key_feature"],
                        "note": "No PD score image in Unit 1 for this piece; text-only for this excerpt.",
                    })
            else:
                excerpts.append({
                    "piece": exc["piece"],
                    "status": "no_pd_image_available",
                    "bars": exc["bars"],
                    "key_feature": exc["key_feature"],
                })

        sr_manifest[str(lesson_num)] = {
            "lesson_number": lesson_num,
            "title": sr_lesson["title"],
            "score_excerpts": excerpts,
        }
    return sr_manifest


def main():
    parser = argparse.ArgumentParser(description="music-aqa Phase 4 asset pipeline")
    parser.add_argument("--skip-upload", action="store_true",
                        help="Dry run: download + transcode but do not upload to R2")
    parser.add_argument("--lesson", type=int, default=None,
                        help="Process only this lesson number (1-8)")
    args = parser.parse_args()

    print("=" * 60)
    print("music-aqa Phase 4 - audio + score assets")
    print("=" * 60)

    r2_client = None
    if not args.skip_upload:
        r2_client = get_r2_client()
        print("R2 client initialised.")
    else:
        print("DRY RUN: R2 uploads disabled.")

    lessons_to_process = LESSONS
    if args.lesson:
        lessons_to_process = [l for l in LESSONS if l["lesson_number"] == args.lesson]
        if not lessons_to_process:
            print(f"ERROR: lesson {args.lesson} not found.")
            sys.exit(1)

    unit1_manifest = {}
    for lesson in lessons_to_process:
        try:
            entry = process_lesson(lesson, r2_client, args.skip_upload)
            unit1_manifest[str(lesson["lesson_number"])] = entry
        except Exception as e:
            print(f"  ERROR processing lesson {lesson['lesson_number']}: {e}")
            import traceback
            traceback.print_exc()

    # If we only processed a subset, load existing manifest to merge
    if args.lesson and MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        existing_u1 = existing.get("western-classical-1650-1910", {})
        existing_u1.update(unit1_manifest)
        unit1_manifest = existing_u1
        sr_manifest = existing.get("score-reading", {})
        # Rebuild score-reading manifest with updated unit1
        sr_manifest = build_score_reading_manifest(unit1_manifest)
    else:
        sr_manifest = build_score_reading_manifest(unit1_manifest)

    manifest = {
        "western-classical-1650-1910": unit1_manifest,
        "score-reading": sr_manifest,
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nManifest written to: {MANIFEST_PATH}")

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n-- Summary --")
    audio_ok = sum(1 for v in unit1_manifest.values() if v.get("audio", {}).get("url"))
    score_ok = sum(1 for v in unit1_manifest.values() if v.get("score", {}).get("status") == "ok")
    score_audio_only = sum(1 for v in unit1_manifest.values() if v.get("score", {}).get("status") == "no_pd_image_available")

    print(f"Unit 1 audio:  {audio_ok}/8 lessons")
    print(f"Unit 1 scores: {score_ok}/8 lessons have a Commons score image")
    print(f"               {score_audio_only}/8 lessons are audio-only (no Commons score)")

    if score_audio_only:
        print("\nAudio-only lessons (no PD score image on Commons):")
        for n, v in unit1_manifest.items():
            if v.get("score", {}).get("status") == "no_pd_image_available":
                print(f"  L{n} {v['title'][:55]}")
                note = v.get("score", {}).get("note", "")
                if note:
                    print(f"      {note}")

    print("\nScore-reading unit:")
    for sn, sv in sr_manifest.items():
        imgs = [e for e in sv.get("score_excerpts", []) if e.get("url")]
        noimg = [e for e in sv.get("score_excerpts", []) if not e.get("url")]
        print(f"  SR L{sn}: {len(imgs)} images, {len(noimg)} text-only excerpts")

    print("\nDone.")


if __name__ == "__main__":
    main()
