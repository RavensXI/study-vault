"""Refill related_media for lessons that fell below 6 items after the broken-URL
strip. Uses a STRICT whitelist of HEAD-validated root URLs. Adds the minimum
needed to satisfy the verifier's required-categories rule + min 6 items total.

No agent involvement — every URL is in the whitelist, which was HEAD-validated
upfront. Description text is per-subject and category-generic to minimise the
chance of producing a misleading entry.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client


# Subject-aware whitelist. Each entry: { category, title, url, description }
# All URLs HEAD-validated 2026-05-05. Generic enough that even if we add
# more than one per lesson within a subject, the hub URL still makes sense.
WHITELIST = {
    "religious-studies-aqa": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search for religion and ethics podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC Religion",
         "url": "https://www.bbc.co.uk/religion",
         "description": "BBC's hub for religion content — articles, videos and explainers."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for religion and ethics documentaries."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform with Religious Studies content."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub — search for the religion or theme you study."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "BBC Religion",
         "url": "https://www.bbc.co.uk/religion",
         "description": "BBC's articles on world religions, beliefs and ethical issues."},
    ],
    "food-preparation-and-nutrition-eduqas": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search for food and cookery podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC Food",
         "url": "https://www.bbc.co.uk/food",
         "description": "BBC Food's recipe and technique videos."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for food documentaries and cookery series."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Food Preparation and Nutrition."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Food Preparation and Nutrition."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "NHS Eatwell Guide",
         "url": "https://www.nhs.uk/live-well/eat-well/the-eatwell-guide/",
         "description": "Official NHS guidance on the Eatwell Guide and balanced diet."},
    ],
    "health-social-care-ocr": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search for health and care podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "Skills for Care",
         "url": "https://www.skillsforcare.org.uk/",
         "description": "Skills for Care — official adult social care workforce development body."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for health and care documentaries."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for Health and Social Care content."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Health and Social Care."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "NHS Live Well",
         "url": "https://www.nhs.uk/live-well/",
         "description": "Official NHS guidance on health, wellbeing and care."},
    ],
    "business-edexcel": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search for business and economics podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC News — Business",
         "url": "https://www.bbc.co.uk/news/business",
         "description": "BBC News business reporting and video content."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for business documentaries."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Tutor2u Business",
         "url": "https://www.tutor2u.net/business",
         "description": "Tutor2u's GCSE Business hub — notes, videos, and quizzes."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Business."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "BBC News Business",
         "url": "https://www.bbc.co.uk/news/business",
         "description": "Latest UK business news, case studies and analysis."},
    ],
    "cambridge-nationals-enterprise-and-marketing": [
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC News — Business",
         "url": "https://www.bbc.co.uk/news/business",
         "description": "BBC News business reporting and video content."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for business and entrepreneur documentaries."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub — search for the marketing, finance or enterprise topic you study."},
        {"category": "Study Tools", "emoji": "🧰", "title": "gov.uk — Set up a business",
         "url": "https://www.gov.uk/set-up-business",
         "description": "Official step-by-step guidance on starting a UK business — ownership types, finance, registration."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Companies House",
         "url": "https://www.gov.uk/government/organisations/companies-house",
         "description": "UK Companies House — registration, types of company, and free search of any registered business."},
        {"category": "Articles & Web", "emoji": "📰", "title": "BBC News Business",
         "url": "https://www.bbc.co.uk/news/business",
         "description": "Latest UK business news, small-business case studies and analysis."},
        {"category": "Articles & Web", "emoji": "📰", "title": "Startups.co.uk",
         "url": "https://startups.co.uk/",
         "description": "UK startup magazine — founder stories, marketing tips and small-business guides."},
    ],
    "physical-education-aqa": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds — Sport",
         "url": "https://www.bbc.co.uk/sounds/category/sport",
         "description": "BBC Sounds hub for sport podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC Sport",
         "url": "https://www.bbc.co.uk/sport",
         "description": "BBC Sport's coverage, articles and videos across all sports."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer — Sport",
         "url": "https://www.bbc.co.uk/iplayer/categories/sport",
         "description": "BBC iPlayer category for sport documentaries (verified working)."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Physical Education."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Physical Education."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "British Heart Foundation",
         "url": "https://www.bhf.org.uk/",
         "description": "BHF — research and guidance on cardiovascular health and exercise."},
    ],
    "citizenship-aqa": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search for politics and current affairs podcasts."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC News — Politics",
         "url": "https://www.bbc.co.uk/news/politics",
         "description": "BBC News politics hub — explainers, videos and current reporting."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for news and politics documentaries."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Citizenship Studies."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Citizenship Studies."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "GOV.UK",
         "url": "https://www.gov.uk/",
         "description": "Official UK government information on rights, laws and democracy."},
    ],
    "sociology-aqa": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'Thinking Allowed' for Laurie Taylor's weekly social science podcast."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "Tutor2u Sociology",
         "url": "https://www.tutor2u.net/sociology",
         "description": "Tutor2u's GCSE/A-Level Sociology hub — short videos, study notes and quizzes."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for documentaries on class, family, education, crime and inequality."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub — search for the sociology topic you're studying."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for AQA Sociology 8192."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "BBC News",
         "url": "https://www.bbc.co.uk/news/uk",
         "description": "BBC UK news — current stories on family, education, crime, class and inequality."},
    ],
    "separate-sciences-edexcel": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'CrowdScience' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers aligned to the spec."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries on cells, atoms, forces, ecology, climate."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Sciences — search the topic you're studying."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Triple Science."},
    ],
    "separate-sciences-ocr": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'The Life Scientific' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers aligned to the spec."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries on cells, atoms, forces, ecology, climate."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Sciences — search the topic you're studying."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Triple Science."},
    ],
    "science-aqa": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'CrowdScience' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers aligned to the spec."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries on cells, atoms, forces, ecology, climate."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Combined Science — search the topic you're studying."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for AQA Combined Science."},
    ],
    "science-edexcel": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'CrowdScience' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers aligned to the spec."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries spanning the spec."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Combined Science."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Edexcel Combined Science."},
    ],
    "science-ocr": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'The Life Scientific' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries on cells, atoms, forces, ecology, climate."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Combined Science."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for OCR Gateway Combined Science."},
    ],
    "separate-sciences": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'The Life Scientific' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers aligned to the spec."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Free Science Lessons",
         "url": "https://www.youtube.com/@Freesciencelessons",
         "description": "UK GCSE-aligned science videos with tier (Foundation/Higher) labelling."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries spanning the Triple curriculum."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Triple Science."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for AQA Triple Science."},
    ],
    "science-ocr-b": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'CrowdScience' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel — clean explainers."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "CrashCourse",
         "url": "https://www.youtube.com/@crashcourse",
         "description": "Bite-size topic explainers across biology, chemistry and physics."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries spanning the spec."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Combined Science."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform."},
    ],
    "separate-sciences-ocr-b": [
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds",
         "url": "https://www.bbc.co.uk/sounds",
         "description": "BBC Sounds — search 'In Our Time', 'Inside Science', 'The Life Scientific' for science podcasts."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "Cognito",
         "url": "https://www.youtube.com/@cognitoedu",
         "description": "UK GCSE Biology/Chemistry/Physics revision channel."},
        {"category": "Videos & Channels", "emoji": "📺", "title": "CrashCourse",
         "url": "https://www.youtube.com/@crashcourse",
         "description": "Bite-size topic explainers across biology, chemistry and physics."},
        {"category": "Documentaries", "emoji": "🎬", "title": "BBC iPlayer",
         "url": "https://www.bbc.co.uk/iplayer",
         "description": "BBC iPlayer — search for science documentaries spanning the Triple curriculum."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Triple Science."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform."},
    ],
    "physical-education-ocr": [
        # Same structure as AQA PE — sport content is universal
        {"category": "Podcasts", "emoji": "🎙️", "title": "BBC Sounds — Sport",
         "url": "https://www.bbc.co.uk/sounds/category/sport",
         "description": "BBC Sounds hub for sport podcasts (verified working)."},
        {"category": "Videos & Channels", "emoji": "🎬", "title": "BBC Sport",
         "url": "https://www.bbc.co.uk/sport",
         "description": "BBC Sport's coverage, articles and videos across all sports."},
        {"category": "Documentaries", "emoji": "🎞️", "title": "BBC iPlayer — Sport",
         "url": "https://www.bbc.co.uk/iplayer/categories/sport",
         "description": "BBC iPlayer category for sport documentaries (verified working)."},
        {"category": "Study Tools", "emoji": "🧰", "title": "BBC Bitesize",
         "url": "https://www.bbc.co.uk/bitesize",
         "description": "BBC's revision hub for GCSE Physical Education."},
        {"category": "Study Tools", "emoji": "🧰", "title": "Seneca Learning",
         "url": "https://senecalearning.com/en-GB/",
         "description": "Free GCSE revision platform — search for Physical Education."},
        {"category": "Articles & Reading", "emoji": "📰", "title": "British Heart Foundation",
         "url": "https://www.bhf.org.uk/",
         "description": "BHF — research and guidance on cardiovascular health and exercise."},
    ],
}


# Required categories per the verifier
REQUIRED_GROUPS = [
    ("Podcasts",),
    ("Videos & Channels",),
    ("Movies", "TV Shows", "Documentaries"),
    ("Study Tools",),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject_slug")
    ap.add_argument("needs_recurate_path")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    pool = WHITELIST.get(args.subject_slug)
    if not pool:
        print(f"No whitelist for {args.subject_slug}")
        return

    with open(args.needs_recurate_path, "r", encoding="utf-8") as f:
        targets = json.load(f)

    if not targets:
        print("No lessons need re-curating.")
        return

    print(f"Re-curating {len(targets)} lessons in {args.subject_slug}")
    DRY = not args.apply

    for t in targets:
        lesson_id = t["lesson_id"]
        row = sb.table("lessons").select("id, slug, related_media").eq("id", lesson_id).execute().data[0]
        rm = row.get("related_media") or []
        if not isinstance(rm, list):
            rm = []

        # Map of category → list of items in current state
        cat_to_items = {}
        for cat in rm:
            if isinstance(cat, dict):
                cat_to_items.setdefault(cat.get("category"), []).extend(cat.get("items") or [])

        # Determine what's needed
        # 1. Required categories that are missing or empty → must add ≥1 in each
        # 2. Total items < 6 → add more from whitelist until reach 6
        required_satisfied = []
        for group in REQUIRED_GROUPS:
            satisfied = any((c in cat_to_items and cat_to_items[c]) for c in group)
            required_satisfied.append((group, satisfied))

        existing_urls = {it.get("url") for cat in rm if isinstance(cat, dict)
                         for it in (cat.get("items") or []) if isinstance(it, dict)}

        # Add candidates from whitelist:
        added_per_cat = {}
        for group, sat in required_satisfied:
            if sat:
                continue
            # Find a whitelist entry whose category is in this group
            for cand in pool:
                if cand["category"] in group and cand["url"] not in existing_urls:
                    added_per_cat.setdefault(cand["category"], []).append(cand)
                    existing_urls.add(cand["url"])
                    break

        # Now top up to 6 total
        def total_items(cmap):
            return sum(len(v) for v in cmap.values())

        # Build the new map = existing + added
        merged = {}
        for cat in rm:
            if isinstance(cat, dict):
                merged.setdefault(cat.get("category"), {"emoji": cat.get("emoji"), "items": []})["items"] += (cat.get("items") or [])
        for cname, cands in added_per_cat.items():
            for c in cands:
                merged.setdefault(cname, {"emoji": c.get("emoji", "🔗"), "items": []})["items"].append(
                    {"title": c["title"], "url": c["url"], "description": c["description"]}
                )

        cur_total = sum(len(v["items"]) for v in merged.values())
        # Top up
        for cand in pool:
            if cur_total >= 6:
                break
            if cand["url"] in existing_urls:
                continue
            merged.setdefault(cand["category"], {"emoji": cand.get("emoji", "🔗"), "items": []})["items"].append(
                {"title": cand["title"], "url": cand["url"], "description": cand["description"]}
            )
            existing_urls.add(cand["url"])
            cur_total += 1

        # Convert merged dict → list with stable order (Podcasts, Videos & Channels, Movies/TV/Docs, Study Tools, Articles & Reading)
        order = ["Podcasts", "Videos & Channels", "Documentaries", "TV Shows", "Movies", "Study Tools", "Articles & Reading"]
        new_rm = []
        for cat_name in order:
            if cat_name in merged and merged[cat_name]["items"]:
                new_rm.append({"category": cat_name, "emoji": merged[cat_name]["emoji"] or "🔗", "items": merged[cat_name]["items"]})
        # Append any other categories not in `order`
        for cat_name, payload in merged.items():
            if cat_name not in order and payload["items"]:
                new_rm.append({"category": cat_name, "emoji": payload["emoji"] or "🔗", "items": payload["items"]})

        new_total = sum(len(c["items"]) for c in new_rm)
        added = new_total - sum(len(cat.get("items") or []) for cat in rm if isinstance(cat, dict))
        print(f"  {row['slug'][:55]:55s}  +{added} items  (total now {new_total})")

        if not DRY:
            sb.table("lessons").update({"related_media": new_rm}).eq("id", lesson_id).execute()

    if DRY:
        print(f"\n  DRY RUN — pass --apply to commit")


if __name__ == "__main__":
    main()
