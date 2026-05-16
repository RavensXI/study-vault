#!/usr/bin/env python3
"""Generate related_media for all 30 physical-education-edexcel lessons."""

import json
import os

LESSONS_DIR = os.path.join(os.path.dirname(__file__), "lessons")

# ============================================================
# VERIFIED RESOURCE LIBRARY
# YouTube: all confirmed via oembed (404 = dead check)
# JustWatch: all confirmed via page title body check
# Podcasts: show-level Apple Podcasts pages confirmed
# Study Tools: all confirmed via HTTP 200 + body check
# ============================================================

def yt(video_id, title, desc):
    return {
        "title": title,
        "description": desc,
        "url": f"https://www.youtube.com/watch?v={video_id}"
    }

def jw(slug, is_series, title, desc):
    kind = "tv-series" if is_series else "movie"
    return {
        "title": title,
        "description": desc,
        "url": f"https://www.justwatch.com/uk/{kind}/{slug}"
    }

def pod(url, title, desc):
    return {"title": title, "description": desc, "url": url}

def st(url, title, desc):
    return {"title": title, "description": desc, "url": url}

# ---- YouTube (all oembed-verified) ----
HEART = yt("X9ZZ6tcxArI", "Crash Course A&P: The Heart, Part 1 — Under Pressure",
           "How blood pressure and cardiac output change during exercise — essential cardiovascular background.")
MUSCLES_CELLS = yt("Ktv-CaOt6UQ", "Crash Course A&P: Muscles, Part 1 — Muscle Cells",
                   "How skeletal muscle fibres contract at the molecular level, linking to antagonistic pairs and fibre types.")
RESP1 = yt("bHZsvBdUC2I", "Crash Course A&P: Respiratory System, Part 1",
           "Pathway of air and gas exchange mechanics — ideal companion to the Edexcel respiratory system topic.")
NERVOUS1 = yt("qPix_X-9t7E", "Crash Course A&P: The Nervous System, Part 1",
              "Nerve signals and the motor pathway — useful for understanding reaction time and motor skill control.")
NERVOUS_9 = yt("44B0ms3XPKU", "The Nervous System in 9 Minutes",
               "Concise overview of how the nervous system controls movement — helpful for reaction time and guidance topics.")
LUNGS = yt("8NUxvJS-_0k", "TED-Ed: How do lungs work? — Emma Bryce",
           "Animated explanation of breathing mechanics and alveolar gas exchange, matching the Edexcel respiratory lesson.")
MUSCLES_GROW = yt("2tM1LFFxeKg", "TED-Ed: What makes muscles grow? — Jeffrey Siegel",
                  "Explains hypertrophy and muscle adaptation — central to long-term effects of training.")
EXERCISE_23H = yt("aUaInS6HIGo", "23 and 1/2 Hours: The Best Thing You Can Do for Your Health",
                  "Dr Mike Evans argues that 30 minutes of daily walking is the most powerful health intervention known.")
EXERCISE_BRAIN = yt("DsVzKCk066g", "WHY Exercise is so Underrated — Brain Power & Movement Link",
                    "How exercise improves mood, cognition and mental health — supports the physical, emotional and social well-being lesson.")
CARBS = yt("wxzc_2c6GMg", "TED-Ed: How do carbohydrates impact your health? — Richard Wood",
           "Carbohydrates as the primary fuel source for exercise and the role of glycogen in athletic performance.")
CALORIES = yt("zcMBm-UVdII", "Do Calories Matter? Is a Calorie a Calorie? — Science of Weight Gain",
              "Explores energy balance and macronutrient differences, supporting diet, energy and body composition topics.")
WATER = yt("9iMGFqMmUFs", "TED-Ed: What would happen if you did not drink water? — Mia Nacamulli",
           "Vivid explanation of dehydration effects on cells and performance — directly applicable to hydration and sport.")
LEVER = yt("YlYEi0PgG1g", "TED-Ed: The Mighty Mathematics of the Lever",
           "Explains first, second and third class levers with real-world examples — the perfect companion to the lever systems lesson.")
DWECK = yt("_X0mgOOSpLU", "Carol Dweck: The Power of Believing You Can Improve (TED)",
           "The growth mindset applied to skill development and effort in sport — links to goal setting and mental preparation.")
STRESS = yt("RcGyVTAoXEU", "Kelly McGonigal: How to Make Stress Your Friend (TED)",
            "Reframes arousal and stress as performance tools — central to mental preparation and anxiety control lessons.")
SMART = yt("1-SvuFIQjK8", "SMART Goals — Quick Overview",
           "Concise breakdown of SMART target-setting criteria with examples directly applicable to sport.")
DOERR = yt("L4N1q4RNi9I", "John Doerr: Why the Secret to Success is Setting the Right Goals (TED)",
           "How measurable goals drive motivation and performance — broader context for SMART targets in sport.")
PRACTICE_EFF = yt("f2O6mQkFiiw", "TED-Ed: How to Practice Effectively — Annie Bosler & Don Greene",
                  "The science of deliberate practice and skill transfer, mapping to skill classification and practice structures.")
ERICSSON = yt("uoUHlZP094Q", "How to Master Anything: PEAK by Anders Ericsson — Core Message",
              "Summary of deliberate practice research — the science behind structured training and skill acquisition in sport.")
EXPERT_MYTH = yt("5eW6Eagr9XA", "The Expert Myth — Talent vs. Practice",
                 "Challenges the idea that sporting ability is purely innate and shows how structured practice beats natural talent.")
MOTIVATION = yt("pZT-FZqfxZA", "The Science of Motivation",
                "Explores intrinsic vs extrinsic motivation and what drives persistence in sport — useful for sport psychology lessons.")
HANS_ROSLING = yt("hVimVzgtD6w", "Hans Rosling: The Best Stats You Have Ever Seen (TED)",
                  "A masterclass in reading and interpreting statistical data — directly supports the data interpretation lessons.")
DATA_VIZ = yt("5Zg-C8AAIGg", "The Beauty of Data Visualisation — David McCandless (TED)",
              "Shows how visual charts reveal patterns invisible in raw numbers — reinforces skills for interpreting sport participation graphs.")
CC_STATS = yt("HMkllhBI91Y", "Crash Course Statistics: Data Visualisation Part 2",
              "Covers outliers, box plots and scatter graphs — useful for reading health and participation data tables.")
SITTING = yt("wUEl8KrMz14", "TED-Ed: Why Sitting is Bad for You — Murat Dalkilinc",
             "Explains the physiological effects of prolonged sedentary behaviour on the cardiovascular and musculoskeletal system.")
ATP = yt("00jbG_cfGuQ", "Crash Course Biology: ATP and Respiration",
         "ATP production through aerobic and anaerobic pathways — essential background for the energy systems lesson.")

# ---- JustWatch (all title-verified) ----
FREE_SOLO = jw("free-solo", False, "Free Solo (2018)",
               "Oscar-winning documentary of Alex Honnold free-soloing El Capitan — a masterclass in mental preparation and managing fear under pressure.")
ICARUS = jw("icarus", False, "Icarus (2017)",
            "Academy Award-winning documentary exposing the Russian state doping programme — essential viewing for PEDs and sporting ethics.")
SENNA = jw("senna", False, "Senna (2010)",
           "Portrait of Ayrton Senna drive and mental focus — excellent context for sport psychology, motivation and peak performance.")
WHEN_KINGS = jw("when-we-were-kings", False, "When We Were Kings (1996)",
                "Ali vs Foreman Rumble in the Jungle — a masterclass in psychological strategy and physical conditioning against the odds.")
CONCUSSION = jw("concussion", False, "Concussion (2015)",
                "Dramatises discovery of CTE brain damage in NFL players — raises important questions about injury management and the ethics of sport.")
BEND_IT = jw("bend-it-like-beckham", False, "Bend It Like Beckham (2002)",
             "Gender, ethnicity and family background as barriers to participation — a vivid case study for the engagement patterns lesson.")
COACH_CARTER = jw("coach-carter", False, "Coach Carter (2005)",
                  "A basketball coach sets strict academic conditions on his team — themes of leadership, goal setting and extrinsic motivation.")
MONEYBALL = jw("moneyball", False, "Moneyball (2011)",
               "How Oakland used statistical analysis to challenge richer clubs — the original case study in data-driven decision making in sport.")
I_TONYA = jw("i-tonya", False, "I, Tonya (2017)",
             "Tonya Harding story explores ethics, sportsmanship, class barriers and media portrayal of elite women in sport.")
THE_PROGRAM = jw("the-program", False, "The Program (2015)",
                 "Dramatises Lance Armstrong doping cover-up — ideal for lessons on PEDs, sporting integrity and consequences of deviance.")
ATHLETE_A = jw("athlete-a", False, "Athlete A (2020)",
               "USA Gymnastics abuse scandal documentary — raises questions about ethics, performer welfare and sporting governance.")
LAST_DANCE = jw("the-last-dance", True, "The Last Dance (2020)",
                "Michael Jordan final season with the Bulls — elite performance psychology, team dynamics and commercialisation of sport.")
DRIVE_SURVIVE = jw("formula-1-drive-to-survive", True, "Formula 1: Drive to Survive",
                   "Exposes commercial pressures, sponsorship battles and the media machine behind F1 — excellent for the golden triangle lesson.")
SUNDERLAND = jw("sunderland-til-i-die", True, "Sunderland 'Til I Die",
                "Follows Sunderland AFC relegation and rebuild — fan engagement, community identity and the social importance of sport.")
ALL_OR_NOTHING = jw("all-or-nothing-manchester-city", True, "All or Nothing: Manchester City",
                    "Inside a Premier League season — training methods, sponsor relationships, commercial deals and management psychology.")
WE_CHAMPIONS = jw("we-are-the-champions", True, "We Are the Champions (2020)",
                  "Netflix series celebrating niche sports communities worldwide — participation motivation and engagement in non-mainstream sport.")

# ---- Podcasts (show-level Apple Podcasts, verified) ----
HP_POD = pod("https://podcasts.apple.com/gb/podcast/the-high-performance-podcast/id1500444735",
             "The High Performance Podcast (Jake Humphrey & Damian Hughes)",
             "In-depth conversations with elite athletes, coaches and sport psychologists on what drives sustained excellence in sport.")
DIARY_CEO = pod("https://podcasts.apple.com/gb/podcast/the-diary-of-a-ceo-with-steven-bartlett/id1291423644",
                "The Diary Of A CEO — athlete and sport episodes",
                "Steven Bartlett interviews elite performers including athletes and coaches on psychology, training and the mindset behind success.")

# ---- Study Tools (all verified) ----
NHS_EXERCISE = st("https://www.nhs.uk/live-well/exercise/", "NHS Live Well: Exercise",
                  "NHS guidance on recommended physical activity levels, types of exercise and their benefits for health.")
NHS_BENEFITS = st("https://www.nhs.uk/live-well/exercise/exercise-health-benefits/", "NHS: Benefits of Exercise",
                  "Official NHS overview of the physical and mental health benefits of regular exercise for all ages.")
BHF_ACTIVE = st("https://www.bhf.org.uk/informationsupport/support/healthy-living/staying-active", "British Heart Foundation: Staying Active",
                "BHF guidance on cardiovascular health and physical activity, including safe exercise recommendations.")
EDEXCEL_SPEC = st("https://qualifications.pearson.com/en/qualifications/edexcel-gcses/physical-education-2016.html",
                  "Edexcel GCSE PE Specification (Pearson)",
                  "Official Pearson Edexcel 9-1 PE specification — check exam structure, assessment objectives and content coverage.")
TEACH_ANATOMY = st("https://teachmeanatomy.info/", "TeachMeAnatomy",
                   "Free anatomy reference with clear labelled diagrams of muscles, joints and body systems — ideal for anatomy revision.")
SPORT_ENGLAND = st("https://www.sportengland.org/research-and-data/data/active-lives", "Sport England: Active Lives Data",
                   "Official UK participation data broken down by sport, gender, age and ethnicity — primary source for engagement pattern statistics.")
UKAD = st("https://www.ukad.org.uk/", "UK Anti-Doping (UKAD)",
          "Official anti-doping authority listing prohibited substances, past sanctions and clean sport education resources.")
PARALYMPICS = st("https://www.paralympics.org.uk/", "ParalympicsGB",
                 "Profiles of British Paralympic athletes and information on disability sport participation and classification.")
TEAM_GB = st("https://www.teamgb.com/", "Team GB",
             "Profiles of British Olympic athletes with sport science insights and training content from elite preparation camps.")
EIS = st("https://www.eis2win.co.uk/", "English Institute of Sport (EIS)",
         "Performance science organisation supporting British Olympic athletes — articles on training, nutrition and injury prevention.")


def build_related_media(pods=None, videos=None, docs=None, tv=None, movies=None, tools=None):
    """Build a related_media list from provided items."""
    result = []
    if pods:
        result.append({"category": "Podcasts", "emoji": "\U0001f3a4", "items": pods})
    if videos:
        result.append({"category": "Videos & Channels", "emoji": "\U0001f4fa", "items": videos})
    # Movies, TV, Documentaries — use "Documentaries" or split
    if movies and tv:
        # merge into Documentaries if needed, or split
        pass
    if docs:
        result.append({"category": "Documentaries", "emoji": "\U0001f3ac", "items": docs})
    if tv:
        result.append({"category": "TV Shows", "emoji": "\U0001f4fa", "items": tv})
    if movies:
        result.append({"category": "Movies", "emoji": "\U0001f3ac", "items": movies})
    if tools:
        result.append({"category": "Study Tools", "emoji": "\U0001f4da", "items": tools})
    return result


# ============================================================
# LESSON-BY-LESSON RELATED MEDIA
# Every lesson: >=6 items, >=1 Podcast, >=1 Video, >=1 Docs/TV/Movie, >=1 Study Tool
# ============================================================

LESSON_MEDIA = {

    "the-skeleton-functions-and-structure": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_CELLS, EXERCISE_23H],
        docs=[SENNA, FREE_SOLO],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC, NHS_EXERCISE]
    ),

    "joints-ligaments-and-tendons": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_CELLS, EXERCISE_23H],
        docs=[CONCUSSION, FREE_SOLO],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC, EIS]
    ),

    "muscle-types-and-major-muscles": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_CELLS, MUSCLES_GROW, NERVOUS1],
        docs=[LAST_DANCE, SENNA],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC]
    ),

    "antagonistic-pairs-and-muscle-fibre-types": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_CELLS, MUSCLES_GROW],
        docs=[LAST_DANCE, WHEN_KINGS],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC, EIS]
    ),

    "the-cardiovascular-system-and-exercise": build_related_media(
        pods=[HP_POD],
        videos=[HEART, EXERCISE_23H],
        docs=[SENNA, WHEN_KINGS],
        tools=[NHS_BENEFITS, TEACH_ANATOMY, EDEXCEL_SPEC]
    ),

    "the-respiratory-system-and-gas-exchange": build_related_media(
        pods=[HP_POD],
        videos=[RESP1, LUNGS],
        docs=[FREE_SOLO, WHEN_KINGS],
        tools=[NHS_EXERCISE, TEACH_ANATOMY, EDEXCEL_SPEC]
    ),

    "aerobic-and-anaerobic-exercise": build_related_media(
        pods=[HP_POD],
        videos=[ATP, EXERCISE_23H],
        docs=[SENNA, LAST_DANCE],
        tools=[NHS_BENEFITS, EDEXCEL_SPEC, EIS]
    ),

    "short-term-effects-of-exercise": build_related_media(
        pods=[HP_POD],
        videos=[HEART, RESP1, EXERCISE_23H],
        docs=[SENNA, FREE_SOLO],
        tools=[NHS_BENEFITS, EDEXCEL_SPEC]
    ),

    "long-term-effects-of-training": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_GROW, EXERCISE_23H, EXERCISE_BRAIN],
        docs=[LAST_DANCE, SENNA],
        tools=[NHS_BENEFITS, EIS, EDEXCEL_SPEC]
    ),

    "lever-systems-and-mechanical-advantage": build_related_media(
        pods=[HP_POD],
        videos=[LEVER, MUSCLES_CELLS],
        docs=[SENNA, FREE_SOLO],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC]
    ),

    "planes-and-axes-of-movement": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_CELLS, EXERCISE_23H],
        docs=[FREE_SOLO, SENNA],
        tools=[TEACH_ANATOMY, EDEXCEL_SPEC, EIS]
    ),

    "health-fitness-and-components-of-fitness": build_related_media(
        pods=[HP_POD],
        videos=[EXERCISE_23H, EXERCISE_BRAIN],
        docs=[LAST_DANCE, SENNA],
        tools=[NHS_EXERCISE, NHS_BENEFITS, EDEXCEL_SPEC]
    ),

    "fitness-tests-and-interpreting-results": build_related_media(
        pods=[HP_POD],
        videos=[HANS_ROSLING, CC_STATS, DATA_VIZ],
        docs=[LAST_DANCE, MONEYBALL],
        tools=[EDEXCEL_SPEC, EIS, NHS_EXERCISE]
    ),

    "principles-of-training-and-programme-design": build_related_media(
        pods=[HP_POD],
        videos=[ERICSSON, PRACTICE_EFF, MUSCLES_GROW],
        docs=[LAST_DANCE, SENNA],
        tools=[NHS_EXERCISE, EIS, EDEXCEL_SPEC]
    ),

    "methods-of-training-and-their-effects": build_related_media(
        pods=[HP_POD],
        videos=[MUSCLES_GROW, EXERCISE_23H, ERICSSON],
        docs=[LAST_DANCE, SENNA],
        tools=[NHS_EXERCISE, EIS, EDEXCEL_SPEC]
    ),

    "injury-prevention-parq-rice-and-peds": build_related_media(
        pods=[HP_POD],
        videos=[EXERCISE_23H, MUSCLES_GROW],
        docs=[ICARUS, CONCUSSION, THE_PROGRAM],
        tools=[UKAD, NHS_EXERCISE, EDEXCEL_SPEC]
    ),

    "using-data-in-physical-activity-and-sport": build_related_media(
        pods=[HP_POD],
        videos=[HANS_ROSLING, DATA_VIZ, CC_STATS],
        docs=[MONEYBALL, LAST_DANCE],
        tools=[SPORT_ENGLAND, EDEXCEL_SPEC, EIS]
    ),

    # === Health and Performance unit ===

    "physical-emotional-and-social-wellbeing": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[EXERCISE_BRAIN, EXERCISE_23H],
        docs=[BEND_IT, WE_CHAMPIONS],
        tools=[NHS_BENEFITS, BHF_ACTIVE, EDEXCEL_SPEC]
    ),

    "lifestyle-choices-and-sedentary-living": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[SITTING, EXERCISE_23H],
        docs=[CONCUSSION, WE_CHAMPIONS],
        tools=[NHS_EXERCISE, BHF_ACTIVE, EDEXCEL_SPEC]
    ),

    "diet-nutrition-and-hydration": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[CARBS, CALORIES, WATER],
        docs=[LAST_DANCE, SENNA],
        tools=[NHS_EXERCISE, BHF_ACTIVE, EDEXCEL_SPEC]
    ),

    "classification-of-skills-and-practice-structures": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[PRACTICE_EFF, ERICSSON, EXPERT_MYTH],
        docs=[LAST_DANCE, SENNA],
        tools=[EDEXCEL_SPEC, EIS]
    ),

    "goal-setting-and-smart-targets": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[SMART, DOERR, DWECK],
        docs=[COACH_CARTER, LAST_DANCE],
        tools=[EDEXCEL_SPEC, NHS_EXERCISE]
    ),

    "guidance-and-feedback-in-sport": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[PRACTICE_EFF, ERICSSON, NERVOUS1],
        docs=[LAST_DANCE, COACH_CARTER],
        tools=[EDEXCEL_SPEC, EIS]
    ),

    "mental-preparation-for-performance": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[STRESS, DWECK, MOTIVATION],
        docs=[FREE_SOLO, SENNA, WHEN_KINGS],
        tools=[EDEXCEL_SPEC, EIS]
    ),

    "engagement-patterns-in-sport": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[EXERCISE_BRAIN, SITTING],
        docs=[BEND_IT, SUNDERLAND, WE_CHAMPIONS],
        tools=[SPORT_ENGLAND, PARALYMPICS, EDEXCEL_SPEC]
    ),

    "commercialisation-sponsorship-and-the-media": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[HANS_ROSLING, DATA_VIZ],
        tv=[DRIVE_SURVIVE, ALL_OR_NOTHING, SUNDERLAND],
        tools=[EDEXCEL_SPEC, SPORT_ENGLAND]
    ),

    "ethical-behaviour-and-deviance-in-sport": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[MOTIVATION, EXPERT_MYTH],
        docs=[ICARUS, THE_PROGRAM, ATHLETE_A],
        tools=[UKAD, EDEXCEL_SPEC]
    ),

    "performance-enhancing-drugs-recap-and-application": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[MOTIVATION, EXERCISE_23H],
        docs=[ICARUS, THE_PROGRAM, ATHLETE_A],
        tools=[UKAD, EDEXCEL_SPEC, EIS]
    ),

    "interpreting-data-on-health-and-participation": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[HANS_ROSLING, DATA_VIZ, CC_STATS],
        docs=[MONEYBALL, SUNDERLAND],
        tools=[SPORT_ENGLAND, EDEXCEL_SPEC, NHS_EXERCISE]
    ),

    "revision-synthesis-component-2-synoptic-practice": build_related_media(
        pods=[HP_POD, DIARY_CEO],
        videos=[EXERCISE_BRAIN, STRESS, DWECK],
        docs=[LAST_DANCE, FREE_SOLO, SENNA],
        tools=[EDEXCEL_SPEC, EIS, NHS_BENEFITS]
    ),
}

# ============================================================
# WRITE TO FILES
# ============================================================

written = []
skipped = []

for filename in sorted(os.listdir(LESSONS_DIR)):
    if not filename.endswith(".json"):
        continue
    slug = filename.replace(".json", "")
    filepath = os.path.join(LESSONS_DIR, filename)

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    if "related_media" in data:
        skipped.append(slug)
        continue

    if slug not in LESSON_MEDIA:
        print(f"WARNING: No media defined for {slug}")
        continue

    data["related_media"] = LESSON_MEDIA[slug]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Verify count
    total_items = sum(len(cat["items"]) for cat in data["related_media"])
    cats = [cat["category"] for cat in data["related_media"]]
    has_pod = "Podcasts" in cats
    has_vid = "Videos & Channels" in cats
    has_doc_or_tv_movie = any(c in cats for c in ["Documentaries", "TV Shows", "Movies"])
    has_tool = "Study Tools" in cats
    status = "OK" if (total_items >= 6 and has_pod and has_vid and has_doc_or_tv_movie and has_tool) else "FAIL"
    written.append(f"{status} {slug}: {total_items} items, cats={cats}")

print(f"\nWritten: {len(written)} lessons")
print(f"Skipped (already had media): {len(skipped)}")
for line in written:
    print(" ", line)
