"""
Hero image generator for French free-tier practice lessons.
Derives search queries from unit name + lesson title (French practice lessons
don't have hero_keywords in their JSONs).

Usage: python scripts/_batch_heroes_french.py [--dry-run]
"""
import argparse
import io
import os
import sys
import time
import urllib.request

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
from lib.r2 import get_r2_client, upload_file_to_r2, IMAGES_BUCKET
from lib.wikimedia import resize_and_compress


# Hand-curated topical queries per French unit/lesson — target GCSE-relevant
# photography. "France" appended where country context helps.
QUERY_MAP = {
    "people-and-lifestyle": {
        "Family and Describing People": ["French family portrait", "family multi-generational", "family together"],
        "Friendships and Personal Qualities": ["friends laughing", "teenagers friends group", "young people friends"],
        "Relationships and Future Plans": ["young couple France", "couple city street", "couple walking paris"],
        "Home Life and Daily Routine": ["parisian apartment morning", "french kitchen breakfast", "waking up bedroom"],
        "Food, Drink and Meals": ["french food market", "french bistro dining", "baguette cheese wine"],
        "Body, Illness and Wellbeing": ["pharmacy France", "doctor consultation", "healthy lifestyle"],
        "Sport and Staying Active": ["running park France", "cycling countryside france", "teenagers playing sport"],
        "School Subjects and Opinions": ["french classroom students", "high school students", "school corridor"],
        "School Life, Rules and Uniform": ["school students uniform", "classroom studying", "secondary school"],
        "Jobs, Work Experience and Career Plans": ["young professional interview", "workplace office team", "working adult"],
    },
    "popular-culture": {
        "Hobbies and Free-Time Activities": ["teenagers hobbies", "painting art class", "guitar music lesson"],
        "Music, Film and Television": ["cinema audience", "music concert crowd", "french cinema paris"],
        "Reading, Gaming and Digital Entertainment": ["young reading book", "video games teens", "reading library"],
        "French Festivals and Public Holidays": ["bastille day paris", "french festival crowd", "christmas market france"],
        "Family Celebrations and Traditions": ["family celebration dinner", "birthday candles cake", "wedding family gathering"],
        "Eating Out and Ordering Food": ["parisian cafe terrace", "french restaurant table", "ordering cafe waiter"],
        "Celebrities and Role Models": ["press conference spotlight", "microphone stage performer", "autograph fans crowd"],
        "Social Media and Celebrity Culture": ["smartphone social media", "phone scrolling app", "instagram user phone"],
    },
    "communication-and-world": {
        "Holidays and Travel Plans": ["packing suitcase travel", "airport departures", "holiday planning map"],
        "Past Holidays and Experiences": ["beach holiday france", "mediterranean coast summer", "mountain holiday view"],
        "Accommodation and Travel Problems": ["hotel reception france", "hotel room booking", "hotel lobby"],
        "Weather, Countries and Transport": ["train station france", "tgv train france", "autumn countryside france"],
        "Technology in Daily Life": ["laptop student studying", "smartphone daily use", "person typing laptop"],
        "Social Media: Pros and Cons": ["phone screen notifications", "smartphone teen bedroom", "social apps phone"],
        "My Town and Local Area": ["french town square", "provincial town street", "french village market"],
        "The Environment and Global Issues": ["recycling bins france", "paris protest climate", "nature forest path"],
    },
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sb = get_client()

    subject = sb.table("subjects").select("id").eq("slug", "french-aqa").is_("school_id", "null").single().execute().data
    sid = subject["id"]
    units = sb.table("units").select("id,slug,name").eq("subject_id", sid).execute().data
    unit_map = {u["slug"]: (u["id"], u["name"]) for u in units}

    for unit_slug, lessons_spec in QUERY_MAP.items():
        uid, uname = unit_map.get(unit_slug, (None, None))
        if not uid:
            print(f"[SKIP] unit {unit_slug} not found")
            continue
        lessons = sb.table("lessons").select("id,lesson_number,title,hero_image_url").eq("unit_id", uid).order("lesson_number").execute().data
        for l in lessons:
            title = l["title"]
            ln = l["lesson_number"]
            if l.get("hero_image_url"):
                print(f"[SKIP] L{ln:02d} {title} — already has hero")
                continue
            queries = lessons_spec.get(title)
            if not queries:
                # Fallback: use lesson title itself
                queries = [title]
            print(f"\n  L{ln:02d} {title}")
            print(f"      queries: {queries[:3]}")

            found = None
            # Try reuse from index first
            for q in queries:
                matches = search_heroes(q)
                if matches and matches[0].get("score", 0) >= 6:
                    found = {"url": matches[0]["hero_url"], "alt": matches[0]["title"], "reused": True}
                    print(f"      reuse: {found['url'][:70]}... (score {matches[0]['score']})")
                    break
            # Unsplash fallback
            if not found:
                for q in queries:
                    try:
                        results = search_unsplash(q, per_page=5)
                    except Exception as e:
                        print(f"      unsplash err '{q}': {e}")
                        continue
                    if not results:
                        continue
                    top = results[0]
                    try:
                        trigger_unsplash_download(top.get("_download_location", ""))
                    except Exception:
                        pass
                    if args.dry_run:
                        print(f"      [DRY] would use {top['url'][:70]}...")
                        found = {"url": top["url"], "alt": top.get("title") or q, "reused": False, "_dry": True}
                        break
                    try:
                        import tempfile
                        tmp_src = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                        tmp_dest = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
                        urllib.request.urlretrieve(top["url"], tmp_src)
                        resize_and_compress(tmp_src, tmp_dest, max_width=1200, quality=82)
                        r2_key = f"french-aqa/{unit_slug}/lesson-{ln:02d}-hero.jpg"
                        r2 = get_r2_client()
                        with open(tmp_dest, "rb") as f:
                            r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=f.read(), ContentType="image/jpeg")
                        os.unlink(tmp_src); os.unlink(tmp_dest)
                        r2_url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
                        photographer = top.get("photographer") or ""
                        unsplash_caption = f"Photo: {photographer} / Unsplash" if photographer else "Photo via Unsplash"
                        alt = top.get("title") or q
                        try:
                            add_to_index(
                                title=alt, description=alt,
                                subject_slug="french-aqa", subject_name="French",
                                unit_slug=unit_slug, unit_name=uname,
                                lesson_slug=f"{unit_slug}-l{ln:02d}",
                                hero_url=r2_url,
                            )
                        except Exception as e:
                            print(f"      index err: {e}")
                        found = {"url": r2_url, "alt": alt, "caption": unsplash_caption, "reused": False}
                        break
                    except Exception as e:
                        print(f"      download err '{q}': {e}")
                        continue
            if not found:
                print(f"      [MISS] no image")
                continue
            if args.dry_run:
                continue
            if found.get("_dry"):
                continue
            sb.table("lessons").update({
                "hero_image_url": found["url"],
                "hero_image_alt": found["alt"],
                "hero_image_caption": found.get("caption") or "Photo via Unsplash",
                "hero_image_position": "center 50%",
            }).eq("id", l["id"]).execute()
            tag = "reused" if found["reused"] else "downloaded"
            print(f"      [OK] {tag}")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
