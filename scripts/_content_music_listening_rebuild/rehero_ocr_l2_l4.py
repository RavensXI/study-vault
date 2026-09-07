# -*- coding: utf-8 -*-
"""Re-hero music-ocr / aos3-rhythms-listening L2 and L4.

Why: a listening lesson's cover card SHOWS the lesson hero (main.js lays the
cover out as a two-column grid with the hero on the left), so these images are
on screen for every student rather than hidden like the rest of the article
furniture. The two heroes inherited from the drill build are wrong for their
lessons:

  L2  Eastern Mediterranean and Middle East -> a djembe, a WEST AFRICAN drum.
  L4  Samba, Calypso and the Americas       -> a Western drum-kit snare.

L1 (a tabla being played) and L3 (a row of hand drummers) are right for their
lessons and are left alone.

The images below were chosen by eye after the automatic HeroFinder search
returned three unusable "grade A" candidates for L4 in a row -- a row of
djembes (wrong continent, and a duplicate of L3), a generic Latin band at an
evening gig, and a bass drummer at a Colombian protest march. The vision gate
is a judgement, so it was overruled and the pick made by hand from the same
stock sources the finder uses. Each pick is still put through the finder's
vision check for the record, and uploaded through the finder's own uploader, so
the R2 key and the caption convention are unchanged. hero_image_url therefore
does not change; only the bytes, the caption and the alt text.

Usage: python rehero_ocr_l2_l4.py [--apply] [2] [4]
"""
import io, json, os, sys
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
REPO = r"C:\Users\tshau\Documents\Study Vault"
sys.path.insert(0, os.path.join(REPO, "scripts"))
from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECT_SLUG, SUBJECT_NAME, UNIT = "music-ocr", "Music", "aos3-rhythms-listening"

PICKS = {
    2: {
        "url": "https://images.pexels.com/photos/19585038/pexels-photo-19585038.jpeg"
               "?auto=compress&cs=tinysrgb&dpr=2&w=1600",
        "credit": "Photo: Anthony Rahayel / Pexels",
        "shows": "Oud bodies, necks and inlaid soundhole rosettes hanging in an instrument maker's "
                 "workshop in the Eastern Mediterranean",
    },
    4: {
        "url": "https://images.pexels.com/photos/15991977/pexels-photo-15991977.png"
               "?auto=compress&cs=tinysrgb&dpr=2&w=1600",
        "credit": "Photo: Sean P. Twomey / Pexels",
        "shows": "Two players at steel pans outdoors in the Caribbean, the hammered note sections of "
                 "the drum face clearly visible",
    },
}
ONLY = [int(a) for a in sys.argv[1:] if a.isdigit()]
if ONLY:
    PICKS = {n: p for n, p in PICKS.items() if n in ONLY}
APPLY = "--apply" in sys.argv

sb = get_client()
subj = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data[0]
urow = sb.table("units").select("id,name,slug").eq("subject_id", subj["id"]).eq("slug", UNIT).execute().data[0]
lessons = {l["lesson_number"]: l for l in sb.table("lessons")
           .select("id,lesson_number,title,description,hero_image_url,hero_image_alt,hero_image_caption")
           .eq("unit_id", urow["id"]).order("lesson_number").execute().data}

finder = HeroFinder()
log = {}
for n, pick in PICKS.items():
    l = lessons[n]
    print("\n--- L%02d %s" % (n, l["title"]))
    print("    was: %s" % l["hero_image_alt"])
    jpeg = finder._fetch_jpeg(pick["url"])
    if jpeg is None:
        print("    [FAIL] could not fetch")
        continue
    grade, shows = finder.vision_check(jpeg, l["title"], pick["shows"], SUBJECT_NAME)
    print("    [vision %s] %s" % (grade, shows[:110]))
    if grade == "C":
        print("    [FAIL] vision check rejected the hand pick")
        continue
    alt = pick["shows"].rstrip(".") + "."
    caption = "%s (%s)" % (pick["shows"].rstrip("."), pick["credit"])
    url = finder._upload(jpeg, SUBJECT_SLUG, urow["slug"], n) if APPLY else l["hero_image_url"]
    log[n] = {"url": url, "caption": caption, "alt": alt, "source_url": pick["url"],
              "vision_grade": grade, "vision_shows": shows, "bytes": len(jpeg)}
    print("    now: %s" % caption)
    if APPLY:
        sb.table("lessons").update({
            "hero_image_url": url,
            "hero_image_caption": caption,
            "hero_image_alt": alt,
            "hero_image_position": "center center",
        }).eq("id", l["id"]).execute()
        print("    written (%d bytes to %s)" % (len(jpeg), url))

io.open(os.path.join(HERE, "ytpick", "rehero_log.json"), "w", encoding="utf-8").write(
    json.dumps(log, indent=1, ensure_ascii=False))
print("\n%s" % ("applied" if APPLY else "dry run"))
