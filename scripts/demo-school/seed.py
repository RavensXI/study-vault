"""Demo High School seeder — a full Y10+Y11 cohort on the real pipe.

Phase A (this file, --seed): tenant, roster, auth accounts, profiles,
classes, memberships. Phase B (--activity): activity histories into BOTH
sinks (user_metadata.sv_progress + the events table).

Usage:
  python scripts/demo-school/seed.py --plan                 # dry-run: print the cohort
  python scripts/demo-school/seed.py --seed --password X    # create everything
  python scripts/demo-school/seed.py --wipe                 # remove the tenant entirely

Deterministic: same seed -> same school. Names are fictional.
"""
import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]
SCHOOL_SLUG = "demo-high"
SCHOOL_NAME = "Demo High School"
EMAIL_DOMAIN = "demo.studyvault.co.uk"

# ---- departments: board picked ONCE, like a real school -------------------
# code = the letter used in class names (10H1, 11G2...)
DEPTS = {
    "maths-edexcel":          {"label": "Maths",             "code": "M",  "take": "all"},
    "english-language-aqa":   {"label": "English Language",  "code": "E",  "take": "all"},
    "english-literature-aqa": {"label": "English Literature","code": "L",  "take": "all"},
    "science-aqa":            {"label": "Combined Science",  "code": "S",  "take": "combined"},
    "separate-sciences":      {"label": "Separate Sciences", "code": "T",  "take": "triple"},
    "history-aqa":            {"label": "History",           "code": "H",  "take": "option"},
    "geography-aqa":          {"label": "Geography",         "code": "G",  "take": "option"},
    "french-aqa":             {"label": "French",            "code": "F",  "take": "option"},
    "spanish-aqa":            {"label": "Spanish",           "code": "N",  "take": "option"},
    "business-edexcel":       {"label": "Business",          "code": "B",  "take": "option"},
    "computer-science":       {"label": "Computer Science",  "code": "C",  "take": "option"},
    "physical-education-aqa": {"label": "PE",                "code": "P",  "take": "option"},
    "psychology-aqa":         {"label": "Psychology",        "code": "Y",  "take": "option"},
    "drama-aqa":              {"label": "Drama",             "code": "D",  "take": "option"},
    "religious-studies-aqa":  {"label": "Religious Studies", "code": "R",  "take": "option"},
}
HUMANITIES = ["history-aqa", "geography-aqa"]
LANGUAGES = ["french-aqa", "spanish-aqa"]
OTHER_OPTIONS = ["business-edexcel", "computer-science", "physical-education-aqa",
                 "psychology-aqa", "drama-aqa", "religious-studies-aqa"]
ARCHETYPES = [("steady", .74, .62, 30), ("crammer", .66, .28, 18), ("quiet", .62, .10, 12),
              ("struggling", .44, .50, 14), ("grafter", .47, .78, 10), ("flying", .88, .70, 16)]

FIRST = ("Amelia Oliver Ava Noah Isla Leo Freya Arthur Mia Oscar Grace Archie Sofia Theo Evie "
         "Finley Poppy Jude Alice Felix Ruby Louie Esme Albie Willow Ronnie Ivy Hugo Ella George "
         "Aisha Ibrahim Zara Yusuf Maryam Musa Khadija Adam Fatima Hassan Ayesha Bilal Noor Zain "
         "Daisy Alfie Rosie Charlie Millie Jacob Erin Harry Lola Henry Maya Lucas Layla Ethan "
         "Nancy Freddie Bella Jack Emily Thomas Sienna James Elsie William Phoebe Joshua Harper "
         "Reuben Matilda Elijah Florence Roman Ada Jesse Iris Ellis Orla Caleb Robyn Sonny Eliza "
         "Kai Thea Rory Lyla Ezra Ines Milo Nell Otis Romy Rex Wren Blake Juno Ashton Pearl").split()
LAST = ("Khan Booth Ahmed Riley Clarke Osei Nowak Doyle Patel Grant Bibi Walsh Singh Moore Iqbal "
        "Fox Kaur Webb Ali Dunn Shah Cole Hart Reid Amin Page Rose Todd Hughes Ward Begum Malik "
        "Hussain Akhtar Mahmood Aziz Rashid Farooq Chowdhury Uddin Miah Rahman Bird Frost Snow "
        "Lane Wells Nash Sharp Bloom Cross Dale Fenn Gale Hale Kemp Lock Marsh Nutt Peck Quill "
        "Rudd Sale Tate Vane Wick York Ash Barr Carr Dew Epps Finch Gould Holt Ives Judd Kite "
        "Lowe Mott Nye Ogden Pryce Quinn Rigg Stone Tripp Voss Wynn Yates Zaman Ncube Adeyemi "
        "Okafor Mensah Boateng Diallo Kamara Toure").split()

TEACHER_FIRST = ("Sarah David Rachel James Helen Mark Claire Paul Emma Andrew Lisa Peter Anna "
                 "Simon Kate Daniel Laura Michael Jane Robert Amara Tariq Priya Kwame").split()
TEACHER_LAST = ("Archer Bennett Crawford Dawson Ellison Foster Graham Howell Ingram Jarvis "
                "Kendall Lawton Mercer Norton Osborne Prescott Quincey Radford Sutton Thorne "
                "Underhill Vickers Whitfield Yardley").split()


def api(method, path, body=None):
    req = urllib.request.Request(URL + path, method=method,
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=representation"},
        data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path}: {e.code} {e.read().decode()[:200]}") from e


# ---- the roster -----------------------------------------------------------
def build_roster(year_size, rng):
    students, used = [], set()
    for year in (10, 11):
        for _ in range(year_size):
            while True:
                fn, ln = rng.choice(FIRST), rng.choice(LAST)
                if (fn, ln) not in used:
                    used.add((fn, ln)); break
            r = rng.random()
            acc, k = 0, ARCHETYPES[0]
            for a in ARCHETYPES:
                acc += a[3]
                if r * 100 < acc:
                    k = a; break
            ability = max(.18, min(.95, k[1] + rng.gauss(0, .09)))
            triple = ability > .72 and rng.random() < .55        # top ~25% take triple
            subjects = [s for s, d in DEPTS.items() if d["take"] == "all"]
            subjects.append("separate-sciences" if triple else "science-aqa")
            opts = []
            if rng.random() < .55: opts.append(rng.choice(HUMANITIES))
            if rng.random() < .40: opts.append(rng.choice(LANGUAGES))
            # languages are opt-IN only (the 40% above) — never filler, or the
            # cohort ends up 90% linguists. Humanities can double up as filler.
            pool = [o for o in OTHER_OPTIONS + HUMANITIES if o not in opts]
            while len(opts) < 4:
                pick = rng.choice(pool); pool.remove(pick); opts.append(pick)
            subjects += opts
            email = (fn + ln).lower() + "@" + EMAIL_DOMAIN
            students.append({"first": fn, "last": ln, "email": email, "year": year,
                             "archetype": k[0], "ability": round(ability, 3),
                             "days": k[2], "subjects": subjects})
    return students


def build_classes(students, rng):
    """Split each subject-year cohort into classes of <=28; assign teachers
    (one teacher per <=2 classes per department)."""
    classes, teachers = [], {}
    tnames = [(f, l) for f in TEACHER_FIRST for l in TEACHER_LAST]
    rng.shuffle(tnames)
    ti = 0
    for slug, d in DEPTS.items():
        dept_classes = []
        for year in (10, 11):
            cohort = [s for s in students if slug in s["subjects"] and s["year"] == year]
            rng.shuffle(cohort)
            n = max(1, -(-len(cohort) // 28)) if cohort else 0
            for i in range(n):
                group = cohort[i::n]
                dept_classes.append({"name": f"{year}{d['code']}{i+1}", "year": year,
                                     "subject": slug, "students": [s["email"] for s in group]})
        for i, c in enumerate(dept_classes):
            if i % 2 == 0:
                fn, ln = tnames[ti]; ti += 1
                key = (fn + "." + ln).lower() + "@" + EMAIL_DOMAIN
                teachers[key] = {"first": fn, "last": ln, "email": key, "dept": slug,
                                 "label": d["label"]}
                cur = key
            c["teacher"] = cur
        classes += dept_classes
    return classes, teachers


# ---- seeding --------------------------------------------------------------
def get_school():
    rows = api("GET", f"/rest/v1/schools?slug=eq.{SCHOOL_SLUG}&select=id")
    return rows[0]["id"] if rows else None


def create_user(email, password, name, extra_meta=None):
    meta = {"full_name": name, "is_demo": True}
    meta.update(extra_meta or {})
    u = api("POST", "/auth/v1/admin/users",
            {"email": email, "password": password, "email_confirm": True,
             "user_metadata": meta})
    return u["id"]


def wipe():
    sid = get_school()
    if not sid:
        print("nothing to wipe"); return
    profs = api("GET", f"/rest/v1/profiles?school_id=eq.{sid}&select=id,email")
    print(f"wiping {len(profs)} accounts + tenant rows...")
    api("DELETE", f"/rest/v1/events?school_id=eq.{sid}")
    api("DELETE", f"/rest/v1/class_members?class_id=in.(select id from classes)") if False else None
    cls = api("GET", f"/rest/v1/classes?school_id=eq.{sid}&select=id")
    for c in cls:
        api("DELETE", f"/rest/v1/class_members?class_id=eq.{c['id']}")
    api("DELETE", f"/rest/v1/classes?school_id=eq.{sid}")
    for i, pr in enumerate(profs):
        try:
            api("DELETE", f"/auth/v1/admin/users/{pr['id']}")
        except RuntimeError as e:
            print("  auth delete failed:", pr["email"], str(e)[:80])
        if i % 25 == 0:
            print(f"  {i}/{len(profs)}")
    api("DELETE", f"/rest/v1/profiles?school_id=eq.{sid}")
    api("DELETE", f"/rest/v1/schools?id=eq.{sid}")
    print("wiped.")


def seed(args):
    rng = random.Random(20261010)
    students = build_roster(args.year_size, rng)
    classes, teachers = build_classes(students, rng)
    if args.plan:
        by = {}
        for s in students: by[s["archetype"]] = by.get(s["archetype"], 0) + 1
        print(f"{len(students)} students ({args.year_size}/year) · {len(teachers)} teachers · {len(classes)} classes")
        print("archetypes:", by)
        for slug, d in DEPTS.items():
            n = sum(1 for s in students if slug in s["subjects"])
            cn = sum(1 for c in classes if c["subject"] == slug)
            print(f"  {d['label']:<20} {n:>3} students · {cn} classes")
        print("sample:", students[0]["email"], students[0]["subjects"])
        return
    if not args.password:
        raise SystemExit("--password required to create accounts")
    sid = get_school()
    if not sid:
        row = api("POST", "/rest/v1/schools",
                  {"name": SCHOOL_NAME, "slug": SCHOOL_SLUG,
                   "settings": {"demo": True}})
        sid = row[0]["id"]
        print("school created", sid)
    else:
        print("school exists", sid)

    ids = {}   # email -> auth id
    everyone = ([("teacher", t["email"], t["first"] + " " + t["last"], t) for t in teachers.values()]
                + [("student", s["email"], s["first"] + " " + s["last"], s) for s in students])
    existing = {p["email"]: p["id"] for p in api("GET", f"/rest/v1/profiles?school_id=eq.{sid}&select=id,email")}
    for i, (role, email, name, obj) in enumerate(everyone):
        if email in existing:
            ids[email] = existing[email]; continue
        try:
            uid = create_user(email, args.password, name)
        except RuntimeError as e:
            print("  user create failed:", email, str(e)[:100]); continue
        ids[email] = uid
        api("POST", "/rest/v1/profiles",
            {"id": uid, "school_id": sid, "role": role, "full_name": name,
             "email": email, "is_demo": True,
             "settings": ({"year": obj["year"], "archetype": obj["archetype"],
                           "ability": obj["ability"], "days": obj["days"],
                           "subjects": obj["subjects"]} if role == "student"
                          else {"dept": obj["dept"]})})
        if i % 20 == 0:
            print(f"  accounts {i}/{len(everyone)}"); time.sleep(.2)

    # subject ids for classes
    subs = {s["slug"]: s["id"] for s in api("GET", "/rest/v1/subjects?school_id=is.null&select=id,slug&limit=300")}
    made = 0
    for c in classes:
        if c["teacher"] not in ids: continue
        row = api("POST", "/rest/v1/classes",
                  {"school_id": sid, "teacher_id": ids[c["teacher"]],
                   "name": c["name"], "subject_id": subs.get(c["subject"]),
                   "year_group": c["year"]})
        cid = row[0]["id"]
        members = [{"class_id": cid, "student_id": ids[e]} for e in c["students"] if e in ids]
        if members:
            api("POST", "/rest/v1/class_members", members)
        made += 1
    print(f"done: {len(ids)} accounts · {made} classes · roster saved")
    json.dump({"students": students, "teachers": list(teachers.values()),
               "classes": classes, "school_id": sid},
              open(os.path.join(os.path.dirname(__file__), "_roster.json"), "w", encoding="utf-8"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--seed", action="store_true")
    ap.add_argument("--wipe", action="store_true")
    ap.add_argument("--year-size", type=int, default=150)
    ap.add_argument("--password", default=os.environ.get("DEMO_SCHOOL_PASSWORD"))
    args = ap.parse_args()
    if args.wipe: wipe()
    elif args.seed or args.plan: seed(args)
    else: ap.print_help()


if __name__ == "__main__":
    main()
