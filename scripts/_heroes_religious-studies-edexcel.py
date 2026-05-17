"""
Phase 4 hero images for religious-studies-edexcel (free-tier, school_id NULL).
71 lessons across 15 units.

Strategy:
  1. Search Wikimedia Commons (no hourly rate limit, 4s delay between requests).
     Excellent architectural/documentary photography for religious buildings.
  2. If Wikimedia returns nothing, fall back to Unsplash (50 requests/hour demo limit).
  3. Download, resize to max 1200px, JPEG q82, upload to R2.
  4. Update Supabase lessons.hero_image_url. Unit card auto-syncs from L01 via trigger.

Safety rules:
  - No depictions of the Prophet Muhammad (architectural / abstract for Islam).
  - No anti-religious imagery.
  - Prefer architectural, landscape, symbol, candlelight, scriptural-object imagery.
  - Do NOT reuse images from other subjects (school content vs generic).

Usage:
    python scripts/_heroes_religious-studies-edexcel.py
    python scripts/_heroes_religious-studies-edexcel.py --dry-run
    python scripts/_heroes_religious-studies-edexcel.py --force   (re-run even if hero set)
    python scripts/_heroes_religious-studies-edexcel.py --unit paper-1-islam
"""

import argparse
import os
import sys
import tempfile
import time
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.supabase_client import get_client
from lib.r2 import get_r2_client, IMAGES_BUCKET
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.wikimedia import (
    search_wikimedia, download_image, resize_and_compress,
    MIN_FILE_SIZE, API_DELAY
)
from lib.hero_index import add_to_index

SUBJECT_SLUG = "religious-studies-edexcel"

# ---------------------------------------------------------------------------
# Lesson manifest — (unit_slug, lesson_number, title, [keywords])
# Keywords are religion-safe: architectural, symbolic, abstract, no identifiable
# worship subjects. Islam lessons avoid human-figure searches entirely.
# ---------------------------------------------------------------------------
LESSONS = [
    # ── Paper 1: Catholic Christianity (6 lessons) ──────────────────────────
    ("paper-1-catholic-christianity", 1, "The Trinity, Creation and Human Nature",
     ["catholic cathedral interior", "stained glass window church", "cross architecture"]),
    ("paper-1-catholic-christianity", 2, "Incarnation, Paschal Mystery and Salvation",
     ["crucifix sculpture stone", "easter cross sunrise", "resurrection cathedral"]),
    ("paper-1-catholic-christianity", 3, "Eschatology: Life After Death, Resurrection and Purgatory",
     ["candles cathedral dark", "gothic church arch light", "sacred sanctuary candles"]),
    ("paper-1-catholic-christianity", 4, "Sacraments, the Mass and Catholic Worship",
     ["catholic mass altar", "church eucharist chalice", "pilgrimage lourdes candles"]),
    ("paper-1-catholic-christianity", 5, "Catholic Social Teaching, Mission and Funeral Rite",
     ["charity hands food poverty", "mission church community", "dove peace sky"]),
    ("paper-1-catholic-christianity", 6, "Sources of Wisdom and Forms of Expression in Catholic Christianity",
     ["illuminated manuscript bible", "religious art fresco ceiling", "sacred geometry architecture"]),

    # ── Paper 1: Christianity (6 lessons) ────────────────────────────────────
    ("paper-1-christianity", 1, "The Trinity, Creation and the Incarnation",
     ["church architecture sunlight", "stained glass trinity", "cathedral gothic exterior"]),
    ("paper-1-christianity", 2, "The Last Days of Jesus, Salvation and Atonement",
     ["cross silhouette sunset", "crown thorns abstract", "stone tomb garden"]),
    ("paper-1-christianity", 3, "Eschatology and the Problem of Evil",
     ["church candles dark", "gothic window light stone", "graveyard peaceful mist"]),
    ("paper-1-christianity", 4, "Christian Worship, Sacraments and Prayer",
     ["church prayer kneeling pew", "baptismal font stone church", "hands prayer candles"]),
    ("paper-1-christianity", 5, "Pilgrimage, Festivals and the Church in the Community",
     ["pilgrimage path landscape", "christmas church lights night", "taize community candles"]),
    ("paper-1-christianity", 6, "Sources of Wisdom and Forms of Expression in Christianity",
     ["open bible parchment", "christian icon painting gold", "church music choir organ"]),

    # ── Paper 1: Islam (6 lessons) ────────────────────────────────────────────
    ("paper-1-islam", 1, "The Nature of Allah and Core Muslim Beliefs",
     ["mosque dome blue sky", "islamic geometry tiles", "minaret architecture sky"]),
    ("paper-1-islam", 2, "Risalah, Holy Books, Angels and Predestination",
     ["quran open book calligraphy", "islamic calligraphy gold", "crescent moon night sky"]),
    ("paper-1-islam", 3, "Akhirah: Life After Death and the Day of Judgement",
     ["mosque interior arch light", "dawn sky horizon spiritual", "islamic garden fountain"]),
    ("paper-1-islam", 4, "The Five Pillars and Ten Obligatory Acts",
     ["mecca grand mosque aerial", "hajj kaaba architecture", "ramadan lantern night"]),
    ("paper-1-islam", 5, "Jihad and Islamic Festivals",
     ["eid celebration lanterns", "islamic festival lights", "crescent moon stars night"]),
    ("paper-1-islam", 6, "Sources of Authority and Muslim Identity",
     ["mosque architecture interior arches", "arabic calligraphy wall", "islamic art geometric pattern"]),

    # ── Paper 2: Catholic Christianity (4 lessons) ───────────────────────────
    ("paper-2-catholic-christianity", 1, "Catholic Beliefs: Trinity, Incarnation and Creation",
     ["sunlight cathedral nave", "church rose window", "cross stone sunlight"]),
    ("paper-2-catholic-christianity", 2, "Paschal Mystery, Salvation and Eschatology",
     ["easter sunrise cross hill", "church candles vigil", "resurrection garden stone"]),
    ("paper-2-catholic-christianity", 3, "Sacraments, the Mass and Catholic Prayer",
     ["altar candles church gold", "rosary beads close up", "mass chalice church"]),
    ("paper-2-catholic-christianity", 4, "Pilgrimage, Catholic Social Teaching and Mission",
     ["lourdes pilgrimage candles", "charity community hands", "mission church sunlight"]),

    # ── Paper 2: Christianity (4 lessons) ────────────────────────────────────
    ("paper-2-christianity", 1, "Christian Beliefs: God, Creation and Jesus",
     ["church sunlight nave", "cross landscape sunrise", "stained glass light colours"]),
    ("paper-2-christianity", 2, "Eschatology and the Problem of Evil",
     ["candles stone church dark", "peaceful cemetery garden", "storm clouds cross"]),
    ("paper-2-christianity", 3, "Christian Worship, Sacraments and Prayer",
     ["church interior worship", "baptism water font", "prayer candles peaceful"]),
    ("paper-2-christianity", 4, "Pilgrimage, Festivals, Mission and the Worldwide Church",
     ["christian pilgrimage path", "easter candle procession", "global church community"]),

    # ── Paper 2: Islam (4 lessons) ────────────────────────────────────────────
    ("paper-2-islam", 1, "Core Muslim Beliefs and the Nature of Allah",
     ["blue mosque exterior turkey", "islamic architecture dome", "minaret sunset"]),
    ("paper-2-islam", 2, "Angels, Predestination and Akhirah",
     ["night sky stars spiritual", "mosque interior dome light", "crescent stars dark sky"]),
    ("paper-2-islam", 3, "The Five Pillars and Ten Obligatory Acts",
     ["kaaba mecca architecture", "ramadan crescent moon", "mosque ablution fountain"]),
    ("paper-2-islam", 4, "Jihad and Islamic Festivals",
     ["eid lights celebration", "islamic lanterns night", "mosque lit evening"]),

    # ── Paper 2: Buddhism (4 lessons) ────────────────────────────────────────
    ("paper-2-buddhism", 1, "The Buddha, the Dhamma and the Three Marks of Existence",
     ["buddhist temple architecture", "bodhi tree roots ancient", "lotus flower water"]),
    ("paper-2-buddhism", 2, "The Four Noble Truths and the Eightfold Path",
     ["buddhist wheel dharma stone", "prayer flags himalaya", "zen garden stones"]),
    ("paper-2-buddhism", 3, "Human Life, Ethics and Worship in Buddhism",
     ["incense smoke temple", "meditation cushion hall", "buddhist shrine candles"]),
    ("paper-2-buddhism", 4, "Buddhist Worship: Temples, Puja, Death Rites and Festivals",
     ["buddhist temple lanterns", "vesak festival lights", "pagoda architecture landscape"]),

    # ── Paper 2: Hinduism (4 lessons) ────────────────────────────────────────
    ("paper-2-hinduism", 1, "Brahman, the Three Aspects of the Divine and the Deities",
     ["hindu temple architecture", "om symbol stone carving", "temple gopuram colourful"]),
    ("paper-2-hinduism", 2, "Atman, Samsara and the Purpose of Life",
     ["lotus flower sunrise reflection", "ganges river sunrise", "mandala sacred geometry"]),
    ("paper-2-hinduism", 3, "Suffering, Cosmology and Hindu Worship",
     ["puja flowers offering", "diya lamp flame", "temple incense smoke"]),
    ("paper-2-hinduism", 4, "Hindu Festivals, Pilgrimage and Charity",
     ["diwali diya lamps", "holi colours festival", "ganges ghats varanasi"]),

    # ── Paper 2: Judaism (4 lessons) ─────────────────────────────────────────
    ("paper-2-judaism", 1, "The Nature of God, Shekhinah and the Messiah",
     ["synagogue interior architecture", "star of david stained glass", "menorah gold candlestick"]),
    ("paper-2-judaism", 2, "The Covenant and Jewish Moral Principles",
     ["torah scroll parchment", "hebrew calligraphy scroll", "stone tablets commandments"]),
    ("paper-2-judaism", 3, "Jewish Worship: Synagogue, Prayer and Sacred Texts",
     ["synagogue ark curtain", "prayer shawl tallit", "menorah shabbat candles"]),
    ("paper-2-judaism", 4, "Family Life, Shabbat, Festivals and the Synagogue",
     ["shabbat candles bread challah", "passover seder table", "jewish wedding chuppah"]),

    # ── Paper 2: Sikhism (4 lessons) ─────────────────────────────────────────
    ("paper-2-sikhism", 1, "The Nature of God and Human Life in Sikhism",
     ["golden temple amritsar", "sikh khanda symbol gold", "gurdwara architecture"]),
    ("paper-2-sikhism", 2, "Gurmukh, Equality, Sewa and the Sangat",
     ["langar community kitchen sikh", "sikh turban colourful", "gurdwara interior"]),
    ("paper-2-sikhism", 3, "The Gurdwara, Langar and Daily Worship",
     ["golden temple reflection water", "gurdwara interior prayer hall", "sikh scripture guru granth"]),
    ("paper-2-sikhism", 4, "Akhand Path, Gurpurbs and Sikh Ceremonies",
     ["vaisakhi sikh festival", "gurdwara lights celebration", "sikh procession lantern"]),

    # ── Paper 3: Philosophy and Ethics (Catholic) (5 lessons) ────────────────
    ("paper-3-philosophy-ethics-catholic", 1, "Revelation, Visions and Miracles as Proof of God",
     ["light rays cathedral", "miracle healing sanctuary candles", "vision sky clouds light"]),
    ("paper-3-philosophy-ethics-catholic", 2, "Religious Experience, the Design Argument and the Cosmological Argument",
     ["universe cosmos stars nebula", "watchmaker gears intricate", "nature pattern sacred geometry"]),
    ("paper-3-philosophy-ethics-catholic", 3, "The Problem of Evil and Catholic Responses",
     ["stormy sky dramatic light", "hands prayer dark suffering", "candles memorial peace"]),
    ("paper-3-philosophy-ethics-catholic", 4, "Marriage, Sexual Relationships and Family",
     ["wedding church rings ceremony", "family hands together", "couple church steps"]),
    ("paper-3-philosophy-ethics-catholic", 5, "Contraception, Divorce, Gender Equality and Discrimination",
     ["scales justice balance", "equality symbol hands", "church community people"]),

    # ── Paper 3: Philosophy and Ethics (Christianity) (5 lessons) ────────────
    ("paper-3-philosophy-ethics-christianity", 1, "Revelation, Visions and Miracles",
     ["light beam cathedral", "burning bush fire symbolic", "transfiguration light clouds"]),
    ("paper-3-philosophy-ethics-christianity", 2, "Religious Experience, Prayer, Design and Cosmological Arguments",
     ["cosmos nebula stars blue", "nature design intricate leaf", "prayer hands close up"]),
    ("paper-3-philosophy-ethics-christianity", 3, "Religious Upbringing as an Argument",
     ["family church sunday", "child bible reading", "church community children"]),
    ("paper-3-philosophy-ethics-christianity", 4, "Marriage, Sexual Relationships and Family",
     ["church wedding aisle flowers", "family together park", "wedding rings bible"]),
    ("paper-3-philosophy-ethics-christianity", 5, "Contraception, Divorce, Gender Equality and Discrimination",
     ["justice scales law book", "equality sign protest art", "community diverse hands"]),

    # ── Paper 3: Philosophy and Ethics (Islam) (5 lessons) ───────────────────
    ("paper-3-philosophy-ethics-islam", 1, "Revelation, Visions and Miracles in Islam",
     ["quran open pages light", "mosque dome gold light", "crescent moon night revelation"]),
    ("paper-3-philosophy-ethics-islam", 2, "Religious Experience, Design and Cosmological Arguments",
     ["stars milky way cosmos", "islamic geometric pattern", "mosque dome architecture stars"]),
    ("paper-3-philosophy-ethics-islam", 3, "The Problem of Suffering in Islam",
     ["desert landscape spiritual", "prayer beads close up", "mosque archway light shadow"]),
    ("paper-3-philosophy-ethics-islam", 4, "Marriage, Sexual Relationships and Family in Islam",
     ["wedding ceremony arch flowers", "family together warm", "islamic garden courtyard"]),
    ("paper-3-philosophy-ethics-islam", 5, "Contraception, Divorce, Gender Equality and Discrimination",
     ["scales justice architecture", "community unity hands diverse", "mosque courtyard peaceful"]),

    # ── Paper 4: Mark's Gospel (5 lessons) ───────────────────────────────────
    ("paper-4-marks-gospel", 1, "Jesus as Messiah, Son of Man and the Baptism",
     ["river baptism water light", "ancient scroll parchment", "galilee sea of landscape"]),
    ("paper-4-marks-gospel", 2, "Miracles of Jesus in Mark",
     ["sea of galilee sunrise", "ancient boat fishing sea", "bread loaves wheat field"]),
    ("paper-4-marks-gospel", 3, "Peter's Confession, the Transfiguration and Conflicts of Jesus",
     ["mountain summit clouds mist", "temple ancient stone ruins", "sunrise mountains holy"]),
    ("paper-4-marks-gospel", 4, "The Last Days of Jesus and the Passion",
     ["cross hill sunrise dramatic", "garden olive tree ancient", "stone tomb door sealed"]),
    ("paper-4-marks-gospel", 5, "Discipleship: The Call, the Cost and Living It Today",
     ["fishing boat sea morning", "path road journey landscape", "cross carrying discipleship"]),

    # ── Paper 4: The Qur'an (5 lessons) ──────────────────────────────────────
    ("paper-4-quran", 1, "Allah in the Qur'an: Al-Fatiha, Tawhid and the 99 Names",
     ["quran pages calligraphy gold", "arabic script manuscript", "mosque ceiling geometric"]),
    ("paper-4-quran", 2, "Believers, Creation and Humanity as Khalifah",
     ["earth from space nature", "arabic calligraphy creation", "mosque garden green"]),
    ("paper-4-quran", 3, "Justice, Shirk and Shari'ah Law",
     ["islamic architecture archway", "arabic manuscript ancient", "mosque courtyard fountain"]),
    ("paper-4-quran", 4, "The Prophets: Nuh, Ibrahim, Ismail and Yusuf",
     ["desert landscape ancient", "kaaba architecture night stars", "ancient river nile egypt"]),
    ("paper-4-quran", 5, "Dawud, Maryam, Isa and the Mission of Muhammad",
     ["moon stars night spiritual", "ancient city jerusalem hills", "dawn sky desert horizon"]),
]


def _upload_to_r2(tmp_src, subject_slug, unit_slug, lesson_number):
    """Resize, compress, upload image file to R2. Returns public R2 URL."""
    tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
    resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
    r2_key = f"{subject_slug}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
    r2 = get_r2_client()
    with open(tmp_dest, "rb") as f:
        r2.put_object(
            Bucket=IMAGES_BUCKET,
            Key=r2_key,
            Body=f.read(),
            ContentType="image/jpeg",
        )
    os.unlink(tmp_dest)
    return f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"


def find_hero_image(keywords, subject_slug, unit_slug, lesson_number, dry_run=False):
    """Search Wikimedia then Unsplash for an appropriate hero image.
    Downloads, compresses, uploads to R2. Returns dict or None."""

    # --- Try Wikimedia first (no hourly rate limit) ---
    for query in keywords:
        try:
            results = search_wikimedia(query, limit=10)
        except Exception as e:
            print(f"      Wikimedia error for '{query}': {e}")
            continue
        for r in results:
            if r.get("size", 0) < MIN_FILE_SIZE:
                continue
            print(f"      Wikimedia hit: '{r['title'][:60]}'  ({r['width']}x{r['height']})")
            if dry_run:
                return {"dry": True, "url": "(dry-wikimedia)", "alt": r["title"], "source": "wikimedia"}
            try:
                tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                dl_url = r["url"] or r.get("original_url", "")
                raw_size = download_image(dl_url, tmp_src)
                if raw_size < MIN_FILE_SIZE:
                    dl_url = r.get("original_url", dl_url)
                    raw_size = download_image(dl_url, tmp_src)
                if raw_size < MIN_FILE_SIZE:
                    os.unlink(tmp_src)
                    continue
                r2_url = _upload_to_r2(tmp_src, subject_slug, unit_slug, lesson_number)
                os.unlink(tmp_src)
                wiki_title = r["title"].replace("File:", "").rsplit(".", 1)[0].replace("_", " ").strip()
                return {
                    "url": r2_url,
                    "alt": wiki_title or query,
                    "caption": wiki_title or "Photo via Wikimedia Commons",
                    "source": "wikimedia",
                }
            except Exception as e:
                print(f"      Wikimedia download error: {e}")
                continue
        time.sleep(API_DELAY)

    # --- Fallback: Unsplash ---
    for query in keywords:
        try:
            results = search_unsplash(query, per_page=5, orientation="landscape")
        except Exception as e:
            print(f"      Unsplash error for '{query}': {e}")
            continue
        if not results:
            continue
        top = results[0]
        print(f"      Unsplash hit: '{top['title'][:60]}' by {top['photographer']}")
        if dry_run:
            return {"dry": True, "url": "(dry-unsplash)", "alt": top["title"], "source": "unsplash"}
        try:
            trigger_unsplash_download(top.get("_download_location", ""))
        except Exception:
            pass
        img_url = top["url"]
        try:
            tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            urllib.request.urlretrieve(img_url, tmp_src)
            r2_url = _upload_to_r2(tmp_src, subject_slug, unit_slug, lesson_number)
            os.unlink(tmp_src)
            photographer = top.get("photographer") or ""
            caption = f"Photo: {photographer} / Unsplash" if photographer else "Photo via Unsplash"
            return {
                "url": r2_url,
                "alt": top.get("title") or query,
                "caption": caption,
                "source": "unsplash",
            }
        except Exception as e:
            print(f"      Unsplash download/upload error for '{query}': {e}")
            continue
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without downloading")
    parser.add_argument("--force", action="store_true", help="Re-process even if hero already set")
    parser.add_argument("--unit", help="Process only this unit slug")
    args = parser.parse_args()

    sb = get_client()

    # Fetch subject + units
    subj_rows = (
        sb.table("subjects")
        .select("id")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if not subj_rows:
        print(f"[ERR] Subject '{SUBJECT_SLUG}' not found (school_id NULL)")
        return
    subject_id = subj_rows[0]["id"]

    # Build unit slug -> unit_id map
    units = (
        sb.table("units")
        .select("id,slug")
        .eq("subject_id", subject_id)
        .execute()
        .data
    )
    unit_map = {u["slug"]: u["id"] for u in units}

    ok = skipped = miss = 0
    for unit_slug, lesson_number, title, keywords in LESSONS:
        if args.unit and unit_slug != args.unit:
            continue
        if unit_slug not in unit_map:
            print(f"[ERR] unit '{unit_slug}' not in Supabase — skipping")
            miss += 1
            continue
        unit_id = unit_map[unit_slug]
        lessons = (
            sb.table("lessons")
            .select("id,hero_image_url")
            .eq("unit_id", unit_id)
            .eq("lesson_number", lesson_number)
            .execute()
            .data
        )
        if not lessons:
            print(f"[ERR] lesson {unit_slug}/L{lesson_number:02d} not found")
            miss += 1
            continue
        lesson_id = lessons[0]["id"]
        existing_hero = lessons[0].get("hero_image_url")

        if existing_hero and not args.force:
            print(f"[SKIP] {unit_slug}/L{lesson_number:02d} — already has hero")
            skipped += 1
            continue

        print(f"\n  {unit_slug}/L{lesson_number:02d}  {title[:55]}")
        print(f"      keywords: {keywords}")

            # No index reuse for this subject — all images must be fresh from Wikimedia/Unsplash
        # to ensure religion-appropriate imagery (the index has no RS content yet
        # and score-4 hits from unrelated subjects return visually wrong images).

        result = find_hero_image(keywords, SUBJECT_SLUG, unit_slug, lesson_number, dry_run=args.dry_run)
        if result:
            if args.dry_run:
                print(f"      [DRY] would set hero from {result.get('source', 'web')} — {result.get('alt','')[:50]}")
                ok += 1
                continue
            r2_url = result["url"]
            sb.table("lessons").update({
                "hero_image_url": r2_url,
                "hero_image_alt": result.get("alt", title),
                "hero_image_caption": result.get("caption", "Photo via Unsplash"),
                "hero_image_position": "center 50%",
            }).eq("id", lesson_id).execute()
            # Add to index for future reuse
            try:
                add_to_index(
                    title=title,
                    description=" ".join(keywords),
                    subject_slug=SUBJECT_SLUG,
                    subject_name="Religious Studies (Edexcel)",
                    unit_slug=unit_slug,
                    unit_name=unit_slug,
                    lesson_slug=f"{unit_slug}-l{lesson_number:02d}",
                    hero_url=r2_url,
                )
            except Exception as e:
                print(f"      index add error: {e}")
            ok += 1
            print(f"      [OK] downloaded from Unsplash")
        else:
            print(f"      [MISS] no image found for L{lesson_number:02d}")
            miss += 1

        time.sleep(1.0)

    print(f"\n{'='*60}")
    print(f"Done — ok={ok}  skipped={skipped}  miss={miss}  total={ok+skipped+miss}/71")


if __name__ == "__main__":
    main()
