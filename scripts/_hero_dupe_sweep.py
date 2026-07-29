# -*- coding: utf-8 -*-
"""Final sweep: regenerate any remaining within-subject duplicate hero.

Groups by SUBJECT ID, not slug: `design-technology` exists twice (Unity
bespoke + free tier) and the two legitimately share images, so slug-grouping
invents duplicates that are not duplicates. School-bespoke rows are skipped
entirely — they are Tom's to curate.

Tier variants (same unit + same lesson_number, Foundation/Higher) legitimately
SHARE a hero and are left alone. Only distinct lessons sharing one image are
regenerated — the later lesson keeps looking, the earlier keeps the image.

    python scripts/_hero_dupe_sweep.py [--dry]
"""
import os
import sys
from collections import defaultdict

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.hero_pipeline import HeroFinder

dry = "--dry" in sys.argv
sb = get_client()

subs = {s["id"]: s for s in
        sb.table("subjects").select("id,slug,name,school_id").execute().data}
units = sb.table("units").select("id,subject_id,slug,name").execute().data

groups = defaultdict(list)
for u in units:
    s = subs.get(u["subject_id"])
    if not s or s["school_id"]:
        continue  # school-bespoke content is never auto-rewritten
    rows = (sb.table("lessons")
            .select("id,lesson_number,title,description,hero_image_url,tier")
            .eq("unit_id", u["id"]).order("lesson_number").execute()).data
    for l in rows:
        if l.get("hero_image_url"):
            groups[(s["id"], l["hero_image_url"])].append((u, s, l))

work = []
for (subject_id, url), members in groups.items():
    if len(members) < 2:
        continue
    # tier variants of one lesson: same unit + same number -> legitimate share
    keys = {(m[0]["id"], m[2]["lesson_number"]) for m in members}
    if len(keys) == 1:
        continue
    # Regenerate the member whose lesson number does NOT match the shared R2
    # key: re-uploading for the key's owner writes the same key, so the URL
    # string never changes and the pair stays joined forever.
    def owns_key(m):
        return f"lesson-{m[2]['lesson_number']:02d}-hero" in (url or "")
    members.sort(key=lambda m: (not owns_key(m), m[2]["lesson_number"]))
    for u, s, l in members[1:] if owns_key(members[0]) else members:
        work.append((u, s, l))

print(f"distinct-lesson duplicates to regenerate: {len(work)}")
for u, s, l in work:
    print(f"  {s['slug']}/{u['slug']} L{l['lesson_number']}: {l['title'][:45]}")
if dry or not work:
    print("dry run / nothing to do")
    sys.exit(0)

finder = HeroFinder()
# seed used-set with every hero currently in play so nothing collides
for (subject_id, url), members in groups.items():
    finder.used.add(url.split("?")[0])

ok = 0
for u, s, l in work:
    print(f"\n--- {s['slug']}/{u['slug']} L{l['lesson_number']} \"{l['title'][:45]}\"")
    r = finder.find(subject_slug=s["slug"], subject_name=s["name"],
                    unit_slug=u["slug"], unit_name=u["name"],
                    lesson_number=l["lesson_number"], title=l["title"],
                    description=l.get("description") or "")
    if not r:
        print("    [FAIL] no acceptable image")
        continue
    sb.table("lessons").update({
        "hero_image_url": r["url"], "hero_image_caption": r["caption"],
        "hero_image_position": "center center"}).eq("id", l["id"]).execute()
    ok += 1
    print(f"    [OK] {r['source']}: {r['caption'][:80]}")

print(f"\nregenerated {ok}/{len(work)}")
