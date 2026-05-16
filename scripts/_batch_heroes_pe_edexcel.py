"""
Hero image generator for physical-education-edexcel (free-tier, school_id NULL).

Derives search queries from lesson titles with PE-appropriate imagery:
anatomy, training, sport action, equipment, health/nutrition.

Usage:
  python scripts/_batch_heroes_pe_edexcel.py
  python scripts/_batch_heroes_pe_edexcel.py --dry-run
  python scripts/_batch_heroes_pe_edexcel.py --no-reuse
"""
import argparse
import os
import sys
import time
import urllib.request
import tempfile

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.hero_index import search_heroes, add_to_index
from lib.r2 import get_r2_client, IMAGES_BUCKET
from lib.wikimedia import resize_and_compress

SUBJECT_SLUG = "physical-education-edexcel"
REUSE_MIN_SCORE = 6

# Hand-curated Unsplash queries per unit/lesson — PE-appropriate, no identifiable
# individuals where possible; prefer anatomical, silhouette, equipment, abstract.
QUERY_MAP = {
    "fitness-and-body-systems": {
        "The Skeleton: Functions and Structure": [
            "human skeleton anatomy", "x-ray bones anatomy", "skeletal system medical"
        ],
        "Joints, Ligaments and Tendons": [
            "knee joint anatomy xray", "athlete stretching flexibility", "joint physiology anatomy"
        ],
        "Muscle Types and Major Muscles": [
            "muscle anatomy diagram", "athlete muscle silhouette", "fitness anatomy body"
        ],
        "Antagonistic Pairs and Muscle Fibre Types": [
            "weightlifting silhouette gym", "bicep curl barbell", "strength training gym equipment"
        ],
        "The Cardiovascular System and Exercise": [
            "heart rate monitor sport", "cardio exercise running track", "heart anatomy medical"
        ],
        "The Respiratory System and Gas Exchange": [
            "lungs anatomy breathing", "athlete breathing sprint", "respiratory physiology medical"
        ],
        "Aerobic and Anaerobic Exercise": [
            "long distance runner trail", "sprint track athlete silhouette", "endurance running athlete"
        ],
        "Short-Term Effects of Exercise": [
            "sweating athlete exercise", "heart rate wristband fitness", "athlete warmup stretching"
        ],
        "Long-Term Effects of Training": [
            "athlete training progress", "fitness transformation gym", "endurance athlete training"
        ],
        "Lever Systems and Mechanical Advantage": [
            "biomechanics sport movement", "rowing athlete lever motion", "javelin throw athlete"
        ],
        "Planes and Axes of Movement": [
            "gymnastics split silhouette", "dancer pose axis", "yoga balance pose"
        ],
        "Health, Fitness and Components of Fitness": [
            "fitness components sport", "athlete all-round training", "speed agility sport training"
        ],
        "Fitness Tests and Interpreting Results": [
            "fitness test stopwatch", "beep test sport school", "vo2max treadmill test"
        ],
        "Principles of Training and Programme Design": [
            "training plan clipboard sport", "coach athlete training session", "sport programme planning"
        ],
        "Methods of Training and Their Effects": [
            "interval training track sprint", "circuit training gym", "weight training barbell squat"
        ],
        "Injury Prevention, PARQ, RICE and PEDs": [
            "ice pack sports injury", "physio athlete treatment", "sports injury rehabilitation"
        ],
        "Using Data in Physical Activity and Sport": [
            "sports data analytics graph", "fitness tracker data wristband", "sport performance statistics"
        ],
    },
    "health-and-performance": {
        "Physical, Emotional and Social Wellbeing": [
            "wellbeing sport happiness", "team sport celebration", "athlete mental health nature"
        ],
        "Lifestyle Choices and Sedentary Living": [
            "sedentary lifestyle couch tv", "active lifestyle walking outdoors", "health lifestyle choice"
        ],
        "Diet, Nutrition and Hydration": [
            "healthy food sport nutrition", "athlete water hydration bottle", "nutritious meal sport plate"
        ],
        "Classification of Skills and Practice Structures": [
            "sport skill practice training", "basketball dribble training", "coach drill practice sport"
        ],
        "Goal Setting and SMART Targets": [
            "goal setting notebook sport", "athlete focus goal training", "success sport target archery"
        ],
        "Guidance and Feedback in Sport": [
            "coach feedback athlete", "sports coach guidance training", "teacher student sport advice"
        ],
        "Mental Preparation for Performance": [
            "athlete mental focus concentration", "meditation sport mindfulness", "pre-match preparation athlete"
        ],
        "Engagement Patterns in Sport": [
            "diverse community sport participation", "sport club group activity", "public sport leisure centre"
        ],
        "Commercialisation, Sponsorship and the Media": [
            "sport sponsorship billboard stadium", "media broadcasting sport camera", "football stadium crowd broadcast"
        ],
        "Ethical Behaviour and Deviance in Sport": [
            "fair play sport handshake", "sportsmanship football team", "referee sport ethics decision"
        ],
        "Performance Enhancing Drugs (Recap and Application)": [
            "anti doping test sport", "clean sport campaign athlete", "drug testing laboratory sport"
        ],
        "Interpreting Data on Health and Participation": [
            "health data chart analysis", "sport statistics graph", "physical activity data research"
        ],
        "Revision Synthesis: Component 2 Synoptic Practice": [
            "exam revision notes sport", "student studying revision", "sport gcse revision books"
        ],
    },
}


def find_or_download(queries, unit_slug, lesson_number, no_reuse=False, dry_run=False):
    if not no_reuse:
        for q in queries:
            matches = search_heroes(q)
            if matches and matches[0].get("score", 0) >= REUSE_MIN_SCORE:
                top = matches[0]
                print(f"      reuse: {top['hero_url'][:70]}...  (score {top['score']}, query '{q}')")
                desc = top.get("description") or ""
                caption = desc if desc.startswith("Photo: ") else "Photo via Unsplash"
                return {"url": top["hero_url"], "alt": top.get("title", q), "caption": caption, "reused": True}

    if dry_run:
        return None

    for q in queries:
        try:
            results = search_unsplash(q, per_page=5)
        except Exception as e:
            print(f"      Unsplash err '{q}': {e}")
            continue
        if not results:
            continue
        top = results[0]
        try:
            trigger_unsplash_download(top.get("_download_location", ""))
        except Exception:
            pass
        image_url = top["url"]
        photographer = top.get("photographer") or ""
        alt = top.get("title") or q
        caption = f"Photo: {photographer} / Unsplash" if photographer else "Photo via Unsplash"
        try:
            tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            urllib.request.urlretrieve(image_url, tmp_src)
            resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
            r2_key = f"{SUBJECT_SLUG}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
            r2 = get_r2_client()
            with open(tmp_dest, "rb") as f:
                r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(), ContentType="image/jpeg")
            os.unlink(tmp_src)
            os.unlink(tmp_dest)
            r2_url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
            try:
                add_to_index(
                    title=alt,
                    description=caption,
                    subject_slug=SUBJECT_SLUG,
                    subject_name="Physical Education",
                    unit_slug=unit_slug,
                    unit_name=unit_slug,
                    lesson_slug=f"{unit_slug}-l{lesson_number:02d}",
                    hero_url=r2_url,
                )
            except Exception as e:
                print(f"      index err: {e}")
            return {"url": r2_url, "alt": alt, "caption": caption, "reused": False}
        except Exception as e:
            print(f"      download err '{q}': {e}")
            continue
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-reuse", action="store_true")
    args = parser.parse_args()

    sb = get_client()
    subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").single().execute().data
    sid = subj["id"]
    units = sb.table("units").select("id,slug,name").eq("subject_id", sid).execute().data
    unit_map = {u["slug"]: (u["id"], u["name"]) for u in units}

    total_ok = 0
    total_miss = 0
    total_skip = 0

    for unit_slug, lesson_queries in QUERY_MAP.items():
        uid, uname = unit_map.get(unit_slug, (None, None))
        if not uid:
            print(f"[SKIP] unit {unit_slug} not found in Supabase")
            continue
        lessons = sb.table("lessons").select("id,lesson_number,title,hero_image_url").eq("unit_id", uid).order("lesson_number").execute().data
        print(f"\n=== Unit: {uname} ({len(lessons)} lessons) ===")
        for l in lessons:
            title = l["title"]
            ln = l["lesson_number"]
            if l.get("hero_image_url"):
                print(f"[SKIP] L{ln:02d} {title} — already has hero")
                total_skip += 1
                continue
            queries = lesson_queries.get(title)
            if not queries:
                queries = [title, f"sport {title.lower()}", "physical education sport"]
            print(f"\n  L{ln:02d} {title}")
            print(f"      queries: {queries}")

            result = find_or_download(queries, unit_slug, ln, no_reuse=args.no_reuse, dry_run=args.dry_run)
            if not result:
                print(f"      [MISS] no image found")
                total_miss += 1
                continue
            if args.dry_run:
                print(f"      [DRY] would set hero")
                continue

            sb.table("lessons").update({
                "hero_image_url": result["url"],
                "hero_image_alt": result["alt"],
                "hero_image_caption": result["caption"],
                "hero_image_position": "center 50%",
            }).eq("id", l["id"]).execute()
            tag = "reused" if result["reused"] else "downloaded"
            print(f"      [OK] {tag} — {result['caption'][:80]}")
            total_ok += 1
            time.sleep(0.8)

    print(f"\n=== Done: {total_ok} OK, {total_miss} missed, {total_skip} skipped ===")


if __name__ == "__main__":
    main()
