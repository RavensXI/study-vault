"""Phase 7 GAP-FILL — Film Studies (Eduqas C670QS), free tier.

Restructures the Component 2 coverage so each of the 15 set films gets its
own lesson, and splits the existing combined Hurt Locker / Hate U Give
indie lesson into two single-film lessons.

Changes (idempotent):

A. Rename existing `global-film` unit to "Global Film: Foundations" and
   update its subtitle. Keeps its 5 existing lessons (foundations only).

B. Insert 3 new units AFTER global-film and BEFORE
   developments-in-film-technology:
     - global-english-language-films  (sort_order 5)
     - global-non-english-language-films (sort_order 6)
     - contemporary-uk-films (sort_order 7)
   Bump developments-in-film-technology from sort_order 5 to 8.

C. Insert 5 lesson shells per new unit (15 lessons) and 1 new lesson at
   us-independent L7 ("The Hate U Give: Issue-Led Indie"), bumping that
   unit's lesson_count from 6 to 7.

   Total lesson delta: +15 (new units) +1 (Hate U Give split) = +16.
   Total lessons after: 28 + 16 = 44.

Idempotent: re-runs detect existing rows by slug + lesson_number and skip.
Stop-condition: if any of the 16 NEW lesson shells we are about to insert
already has populated content_html or practice_questions, skip that
specific row but continue with the rest. (Phase 7 content gen has not
fired yet, so this should never trigger on first run.)

Does NOT touch index.html, vercel.json, or any other subject's data.
CSS edit for `unit-film-studies-eduqas-6/-7/-8` is applied separately to
css/style.css.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

SUBJECT_SLUG = "film-studies-eduqas"

# ---------------------------------------------------------------- locate subj
res = (
    sb.table("subjects")
    .select("id, slug, name, settings")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .execute()
    .data
)
if not res:
    print(f"FATAL: subject {SUBJECT_SLUG} not found")
    sys.exit(2)
subject = res[0]
SUBJECT_ID = subject["id"]
print(f"=== Phase 7 GAP-FILL for {SUBJECT_SLUG} ({SUBJECT_ID[:8]}...) ===\n")

# ---------------------------------------------------------------- A. rename global-film unit

print("--- A. Updating `global-film` unit to foundations-only ---")
gf_res = (
    sb.table("units")
    .select("*")
    .eq("subject_id", SUBJECT_ID)
    .eq("slug", "global-film")
    .execute()
    .data
)
if not gf_res:
    print("FATAL: global-film unit missing")
    sys.exit(2)
gf = gf_res[0]
sb.table("units").update(
    {
        "name": "Global Film: Foundations",
        "subtitle": "Foundations for Component 2 — narrative, representation and aesthetic frameworks applied across the global-film slate.",
    }
).eq("id", gf["id"]).execute()
print(f"  global-film renamed and subtitle updated\n")

# ---------------------------------------------------------------- B. bump developments sort_order to 8

print("--- B. Reordering developments-in-film-technology to sort_order 8 ---")
dev_res = (
    sb.table("units")
    .select("*")
    .eq("subject_id", SUBJECT_ID)
    .eq("slug", "developments-in-film-technology")
    .execute()
    .data
)
if not dev_res:
    print("FATAL: developments-in-film-technology unit missing")
    sys.exit(2)
dev = dev_res[0]
if dev["sort_order"] != 8:
    sb.table("units").update({"sort_order": 8}).eq("id", dev["id"]).execute()
    print(f"  developments-in-film-technology sort_order: {dev['sort_order']} -> 8\n")
else:
    print("  developments-in-film-technology already at sort_order 8\n")

# ---------------------------------------------------------------- B. insert 3 new units

print("--- B. Inserting 3 new units ---")
NEW_UNITS = [
    {
        "slug": "global-english-language-films",
        "name": "Global English-language Films",
        "subtitle": "Slumdog Millionaire, District 9, The Babadook, The Breadwinner, Jojo Rabbit — narrative analysis.",
        "body_class": "unit-film-studies-eduqas-6",
        "accent": "#2563eb",
        "accent_light": "#eff6ff",
        "accent_badge": "#3b82f633",
        "lesson_count": 5,
        "sort_order": 5,
    },
    {
        "slug": "global-non-english-language-films",
        "name": "Global Non-English-Language Films",
        "subtitle": "Tsotsi, The Wave, Wadjda, Girlhood, The Farewell — representation analysis.",
        "body_class": "unit-film-studies-eduqas-7",
        "accent": "#0e7490",
        "accent_light": "#ecfeff",
        "accent_badge": "#06b6d433",
        "lesson_count": 5,
        "sort_order": 6,
    },
    {
        "slug": "contemporary-uk-films",
        "name": "Contemporary UK Films",
        "subtitle": "Submarine, Attack the Block, Skyfall, Blinded by the Light, Rocks — aesthetic analysis.",
        "body_class": "unit-film-studies-eduqas-8",
        "accent": "#be185d",
        "accent_light": "#fdf2f8",
        "accent_badge": "#ec489933",
        "lesson_count": 5,
        "sort_order": 7,
    },
]

new_unit_rows = {}
for nu in NEW_UNITS:
    existing = (
        sb.table("units")
        .select("*")
        .eq("subject_id", SUBJECT_ID)
        .eq("slug", nu["slug"])
        .execute()
        .data
    )
    payload = {**nu, "subject_id": SUBJECT_ID}
    if existing:
        sb.table("units").update(payload).eq("id", existing[0]["id"]).execute()
        new_unit_rows[nu["slug"]] = {**existing[0], **payload}
        print(f"  UPDATED: {nu['slug']:48s} (sort {nu['sort_order']})")
    else:
        ins = sb.table("units").insert({**payload, "image_url": None}).execute()
        new_unit_rows[nu["slug"]] = ins.data[0]
        print(f"  INSERTED: {nu['slug']:48s} (sort {nu['sort_order']})")
print()

# ---------------------------------------------------------------- C. insert lesson shells

NEW_LESSONS = {
    "global-english-language-films": [
        (1, "slumdog-millionaire-narrative-and-mumbai", "Slumdog Millionaire: Narrative and Mumbai",
         "Boyle's quiz-show frame, dual timelines and Mumbai mise-en-scene as narrative engine."),
        (2, "district-9-narrative-and-segregation-allegory", "District 9: Narrative and Segregation Allegory",
         "Blomkamp's mockumentary-into-narrative shift and the apartheid allegory inside a science fiction frame."),
        (3, "the-babadook-narrative-and-grief-as-monster", "The Babadook: Narrative and Grief as Monster",
         "Kent's domestic horror narrative and how the monster works as a bereavement metaphor."),
        (4, "the-breadwinner-narrative-and-animation-under-occupation", "The Breadwinner: Narrative and Animation Under Occupation",
         "Twomey's frame-tale animation and the storybook insets that carry the film's interior narrative."),
        (5, "jojo-rabbit-narrative-and-comic-distance", "Jojo Rabbit: Narrative and Comic Distance",
         "Waititi's child-narrator satire and the comic-distance strategies that make the historical setting bearable."),
    ],
    "global-non-english-language-films": [
        (1, "tsotsi-representation-and-johannesburg", "Tsotsi: Representation and Johannesburg",
         "Hood's Johannesburg slum naturalism and the representation of post-apartheid masculinity."),
        (2, "the-wave-representation-and-conformity", "The Wave: Representation and Conformity",
         "Gansel's classroom-set thriller and how representation builds a portrait of conformity."),
        (3, "wadjda-representation-and-saudi-girlhood", "Wadjda: Representation and Saudi Girlhood",
         "Al-Mansour's Riyadh-set debut and the representation of girlhood under restriction."),
        (4, "girlhood-representation-and-paris-banlieue", "Girlhood: Representation and the Paris Banlieue",
         "Sciamma's Cinemascope ensemble and the representation of Black femininity in suburban Paris."),
        (5, "the-farewell-representation-and-diaspora-grief", "The Farewell: Representation and Diaspora Grief",
         "Wang's static-take family film and the representation of diasporic Chinese-American grief."),
    ],
    "contemporary-uk-films": [
        (1, "submarine-aesthetic-and-adolescent-imagination", "Submarine: Aesthetic and Adolescent Imagination",
         "Ayoade's saturated 1980s-throwback look and the indie-aesthetic register of adolescent imagination."),
        (2, "attack-the-block-aesthetic-and-genre-mixing", "Attack the Block: Aesthetic and Genre Mixing",
         "Cornish's neon-lit South London nights and the genre-mixing aesthetic of urban science fiction."),
        (3, "skyfall-aesthetic-and-bond-cinematography", "Skyfall: Aesthetic and Bond Cinematography",
         "Mendes and Roger Deakins's silhouette-and-skyline blockbuster look applied to the Bond franchise."),
        (4, "blinded-by-the-light-aesthetic-and-musical-realism", "Blinded by the Light: Aesthetic and Musical Realism",
         "Chadha's Springsteen needle-drops and the magical-realist text-overlay sequences that build a musical-realist look."),
        (5, "rocks-aesthetic-and-multicultural-london", "Rocks: Aesthetic and Multicultural London",
         "Gavron's hand-held London naturalism and the social-realist aesthetic of a multicultural teenage cast."),
    ],
}

print("--- C. Inserting lesson shells in 3 new units ---")
total_new = 0
for unit_slug, lessons in NEW_LESSONS.items():
    unit_id = new_unit_rows[unit_slug]["id"]
    existing = (
        sb.table("lessons")
        .select("lesson_number, slug")
        .eq("unit_id", unit_id)
        .execute()
        .data
    )
    nums_present = {L["lesson_number"] for L in existing}
    new_in_unit = 0
    for n, slug, title, desc in lessons:
        if n in nums_present:
            continue
        sb.table("lessons").insert(
            {
                "unit_id": unit_id,
                "lesson_number": n,
                "slug": slug,
                "title": title,
                "description": desc,
                "status": "pending_review",
                "tier": "both",
            }
        ).execute()
        new_in_unit += 1
        total_new += 1
    print(f"  [{unit_slug}] new={new_in_unit} skipped={len(lessons) - new_in_unit}")
print()

# ---------------------------------------------------------------- C. us-independent L7

print("--- C. Adding L7 'The Hate U Give: Issue-Led Indie' to us-independent ---")
indie_res = (
    sb.table("units")
    .select("*")
    .eq("subject_id", SUBJECT_ID)
    .eq("slug", "us-independent")
    .execute()
    .data
)
if not indie_res:
    print("FATAL: us-independent unit missing")
    sys.exit(2)
indie = indie_res[0]
indie_lessons = (
    sb.table("lessons")
    .select("lesson_number, slug")
    .eq("unit_id", indie["id"])
    .execute()
    .data
)
indie_nums = {L["lesson_number"] for L in indie_lessons}

if 7 not in indie_nums:
    sb.table("lessons").insert(
        {
            "unit_id": indie["id"],
            "lesson_number": 7,
            "slug": "the-hate-u-give-and-issue-led-indie",
            "title": "The Hate U Give: Issue-Led Indie",
            "description": "Tillman Jr.'s Black-Lives-Matter-era YA adaptation as the canonical late-2010s issue-led indie.",
            "status": "pending_review",
            "tier": "both",
        }
    ).execute()
    total_new += 1
    print("  INSERTED us-independent L7 'The Hate U Give: Issue-Led Indie'")
else:
    print("  us-independent L7 already exists; skipping")

if indie["lesson_count"] != 7:
    sb.table("units").update({"lesson_count": 7}).eq("id", indie["id"]).execute()
    print(f"  us-independent lesson_count: {indie['lesson_count']} -> 7")
print()

# ---------------------------------------------------------------- verify

print("--- Verification ---")
units_after = (
    sb.table("units")
    .select("id, slug, name, lesson_count, sort_order")
    .eq("subject_id", SUBJECT_ID)
    .order("sort_order")
    .execute()
    .data
)
total_lessons = 0
for u in units_after:
    cnt = (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", u["id"])
        .execute()
        .count
    )
    total_lessons += cnt
    flag = " <-- mismatch" if cnt != u["lesson_count"] else ""
    print(f"  [{u['sort_order']}] {u['slug']:48s} lessons={cnt}/{u['lesson_count']}{flag}")
print(f"\n  Units total: {len(units_after)}  Lessons total: {total_lessons}  New shells inserted this run: {total_new}")
print(f"\n=== Gap-fill activation complete ===")
