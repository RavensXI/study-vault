"""Give the Demo High School History classes a believable two-thirds-of-a-year history.

The teacher screen computes everything from `progress.blob` (api/teacher/class-progress.js
+ api/teacher/_lib/strength.js). The demo classes only ever had a few quiz rows, so every
pupil read "emerging 2" and the Markbook and Topics tabs — two of the four — undersold
themselves in front of a visitor.

This writes a real teaching year for the AQA combination the class actually takes:

    Germany, 1890-1945              period study        taught first, now going cold
    Conflict and Tension 1918-1939  wider world depth   taught second, developing
    Britain: Health and the People  thematic            being taught now, strongest
    Elizabethan England             British depth       just started by the keen ones

Evidence is real: the quiz questions, the wrong options pupils "chose" and the exam
question types all come from the live lessons of those units. Only the pupils are
invented, and they were invented already — this is the demo school.

Nothing outside history-aqa is touched: every other subject's keys in a pupil's blob
are carried over untouched, and the whole blob is backed up before any write.

    python scripts/_demo_class_history.py                 # plan + band summary, no writes
    python scripts/_demo_class_history.py --apply         # write it
    python scripts/_demo_class_history.py --restore FILE  # put the backups back
"""
import io, json, os, random, sys, time, urllib.request
from datetime import date, timedelta

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
MATERIAL = os.path.join(HERE, "_demo_class_history_material.json")
ANSWERS = os.path.join(HERE, "_demo_class_history_answers.json")   # written by _demo_class_answers.py
BACKUP = os.path.join(HERE, "_backup_demo_progress_%s.json" % time.strftime("%Y-%m-%d"))

SUBJECT_ID = "e8cc884b-9619-4303-8c2f-c7531210ab6e"          # history-aqa (free tier)
SUB = "history-aqa"
CLASSES = [("11H1", "8e698c76-f54e-4c68-add3-19f1b9ddef54", 0),
           ("11H2", "554af413-2950-476b-b952-f1789b619677", 1)]

# unit -> (lessons taught, taught-window in days before today, how hard it feels)
COURSE = [
    ("germany-democracy-dictatorship", 14, (178, 126), 0.00),
    ("conflict-tension-inter-war",     14, (118,  64), -0.04),
    ("britain-health-people",          11, ( 52,   2), 0.03),
    ("elizabethan-england",             3, ( 13,   1), -0.02),
]
# Every date below is counted back from the day the class is meant to be LOOKED
# AT, not the day this runs. Strength decays daily, so a set built for "today"
# reads flat three days later; built for the day of the meeting, it reads like a
# class that worked over the weekend. Dates that land in the future are harmless:
# both strength models clamp the age of a piece of evidence at zero.
TODAY = date.fromisoformat(os.environ.get("DEMO_ASOF", "2026-09-24"))

# How long ago each unit was last brought round again, by how diligent the pupil
# is (keen / middling / drifting). The current unit is swept most recently; the
# first unit of the year is what goes cold for everyone but the keen ones.
# One entry per lesson survives in the quiz log, so a lesson's evidence count —
# and with it the half-life — tops out at read + quiz + any marked answer. A
# topic not brought round again inside a fortnight therefore reads "emerging"
# however well it was once known. The windows below are what a pupil who uses
# the plan actually looks like: the revisit slot serves 2-4 lessons a night,
# so a 42-lesson course comes round about every fortnight for the diligent,
# every three weeks for the middle, and stops altogether for the drifters.
REVISIT_WINDOW = {
    "germany-democracy-dictatorship": [(2, 11), (4, 19), (30, 78)],
    "conflict-tension-inter-war":     [(1, 9),  (3, 16), (24, 62)],
    "britain-health-people":          [(1, 6),  (2, 11), (9, 34)],
    "elizabethan-england":            [(1, 5),  (2, 9),  (3, 13)],
}
SWEEP_COVER = [0.95, 0.80, 0.50]

# the Mondays the class screen can compare against ("since last Monday")
SNAPSHOT_WEEKS = ["2026-09-14", "2026-09-21"]

# ---- the model the teacher screen uses, ported so we can tune before writing ----
HALF = [7, 14, 28, 56, 112]
REVISIT_LINE = 55

def decay(v, d, reps):
    return v * 0.5 ** (d / HALF[min(len(HALF) - 1, max(0, reps - 1))])

def band(s):
    return "g" if s >= 70 else "a" if s >= 40 else "r"

def days_since(iso, asof=None):
    return max(0, ((asof or TODAY) - date.fromisoformat(iso)).days)

def strength_units(kc, done, when, practice, asof=None):
    """A port of api/teacher/_lib/strength.js lessons() + units(), history only.

    `asof` lets the same evidence be read as it stood on an earlier Monday, which
    is how the "since last Monday" snapshot is rebuilt honestly rather than guessed.
    """
    day = asof or TODAY
    ev = {}
    def add(unit, n, v, d):
        ev.setdefault("%s/%s" % (unit, n), []).append((v, d))
    def before(iso_d):
        return date.fromisoformat(iso_d) <= day
    for k, e in kc.items():
        p = k.split("/")
        if p[0] != SUB or not e.get("t") or not before(e["d"]):
            continue
        add(p[1], int(p[2]), 25 + 75 * (e["s"] / e["t"]), days_since(e["d"], day))
    for k, lst in done.items():
        p = k.split("/")
        if p[0] != SUB:
            continue
        for n in lst:
            w = when.get("%s/%s" % (k, n))
            if w and not before(w):
                continue
            add(p[1], int(n), 45, days_since(w, day) if w else 30)
    for e in practice:
        p = str(e.get("k", "")).split("/")
        if p[0] != SUB or not before(e["d"]):
            continue
        m = e["_mark"]
        add(p[1], int(p[2]), 25 + 75 * min(1, m[0] / m[1]), days_since(e["d"], day))
    by = {}
    for key, lst in ev.items():
        unit, _n = key.rsplit("/", 1)
        best = max(decay(v, d, len(lst)) for v, d in lst)
        peak = max(v for v, _ in lst)
        u = by.setdefault(unit, {"s": 0.0, "peak": 0.0, "n": 0})
        u["s"] += round(best); u["peak"] += round(peak); u["n"] += 1
    for u in by.values():
        u["s"] = round(u["s"] / u["n"]); u["peak"] = round(u["peak"] / u["n"])
        u["band"] = band(u["s"]); u["drop"] = u["peak"] >= 70 and u["s"] < REVISIT_LINE
    return by

# ---- pupils ----
# ability, engagement, and how much they revise old topics
# A class, not a curve: two who are away ahead, a solid middle, a tail that has
# drifted, one who signed up and stopped, one who never signed in at all. The
# third number is how faithfully they do the revisit slot, and it matters more
# to what the teacher sees than ability does.
TIERS = ([(0.90, 0.98, 0.95)] * 2 + [(0.82, 0.92, 0.80)] * 5 + [(0.72, 0.82, 0.58)] * 7
         + [(0.62, 0.70, 0.45)] * 6 + [(0.52, 0.58, 0.38)] * 4 + [(0.42, 0.40, 0.12)] * 2
         + [(0.55, 0.10, 0.00)] * 1 + [(0.00, 0.00, 0.00)] * 1)

def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())

def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()

def material():
    """Real questions from the live lessons of the four units."""
    if os.path.exists(MATERIAL):
        return json.load(io.open(MATERIAL, encoding="utf-8"))
    out = {}
    for slug, _n, _w, _d in COURSE:
        u = get("units?select=id,slug,name&subject_id=eq.%s&slug=eq.%s" % (SUBJECT_ID, slug))[0]
        ls = get("lessons?select=lesson_number,title,status,knowledge_checks,practice_questions"
                 "&unit_id=eq.%s&order=lesson_number" % u["id"])
        out[slug] = {"name": u["name"], "lessons": []}
        for l in ls:
            if l["status"] != "live":
                continue
            kc = [{"q": q["q"], "options": q["options"], "correct": q["correct"]}
                  for q in (l["knowledge_checks"] or [])
                  if q.get("type") in ("mcq", "fill") and isinstance(q.get("options"), list)
                  and isinstance(q.get("correct"), int)]
            pq = [{"type": p.get("type"), "text": p.get("text", "")} for p in (l["practice_questions"] or [])]
            out[slug]["lessons"].append({"n": l["lesson_number"], "title": l["title"], "kc": kc, "pq": pq})
    io.open(MATERIAL, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
    return out

def iso(days_ago):
    return (TODAY - timedelta(days=int(days_ago))).isoformat()

NOTES_GOOD = [
    "Two factors are explained and linked, and the judgement at the end is argued rather than asserted.",
    "Strong use of specific detail. The second paragraph would be stronger with a date attached to the example.",
    "You weigh the factors against each other, which is what the top band asks for. Keep the conclusion this direct.",
]
NOTES_MID = [
    "Both points are relevant but they sit side by side. Say which one mattered more, and why.",
    "You describe what happened. The question asks why it mattered, so link each point back to consequence.",
    "Good specific knowledge, thin analysis. One sentence of judgement per paragraph would move this up a band.",
    "The example is right but undated. Examiners reward precise support, so pin it to a year.",
]
NOTES_LOW = [
    "Mostly narrative. Pick two reasons and explain each one, rather than telling the story in order.",
    "Too general. Name a person, a date or a law in each paragraph and build the point from it.",
    "You have the right idea but no support. One accurate detail per paragraph would change the mark.",
]

def build_pupil(rng, tier, mat, shift):
    """One pupil's history-aqa evidence."""
    ability, engage, revise = tier
    kc, done, when, practice = {}, {}, {}, []
    if ability == 0:                       # the one who has never signed in
        return kc, done, when, practice
    for slug, taught, (d0, d1), diff in COURSE:
        lessons = mat[slug]["lessons"]
        # how far this pupil has got through the unit
        reach = max(1, min(taught, int(round(taught * (0.55 + 0.5 * engage) + rng.uniform(-1, 1)))))
        if slug == "elizabethan-england" and engage < 0.7:
            reach = 0                       # only the keen ones have started the new unit
        done_list = []
        for i in range(reach):
            l = lessons[i]
            # read on the day it was taught, give or take
            span = d0 - d1
            read_d = d0 - span * (i / max(1, taught - 1)) + rng.uniform(-3, 3) + shift
            read_d = max(1, read_d)
            done_list.append(l["n"])
            when["%s/%s/%s" % (SUB, slug, l["n"])] = iso(read_d)
            # the quick quiz: most pupils do it, the plan books it 3 days later
            if not l["kc"] or rng.random() > (0.55 + 0.45 * engage):
                continue
            qs = l["kc"][:]
            rng.shuffle(qs)
            qs = qs[:rng.choice([4, 4, 5])]
            p_right = min(0.97, max(0.12, ability + diff + rng.gauss(0, 0.11)))
            s, miss = 0, []
            for q in qs:
                if rng.random() < p_right:
                    s += 1
                else:
                    wrong = [o for i2, o in enumerate(q["options"]) if i2 != q["correct"]]
                    miss.append({"q": q["q"], "chose": rng.choice(wrong) if wrong else "",
                                 "right": q["options"][q["correct"]]})
            quiz_d = max(1, read_d - rng.choice([0, 1, 3, 3, 4]))
            kc["%s/%s/%s" % (SUB, slug, l["n"])] = {"d": iso(quiz_d), "s": s, "t": len(qs), "miss": miss}
        if done_list:
            done["%s/%s" % (SUB, slug)] = done_list
        # The revisit slot doing its job: the plan brings old lessons back night
        # after night, so by now most of an older unit has been round again. How
        # much, and how recently, is what separates the pupils.
        if not done_list:
            continue
        tier_i = 0 if revise >= 0.7 else 1 if revise >= 0.35 else 2
        lo, hi = REVISIT_WINDOW[slug][tier_i]
        if True:
            for n in done_list:
                if rng.random() > SWEEP_COVER[tier_i]:
                    continue
                l = next((x for x in lessons if x["n"] == n), None)
                if not l or not l["kc"]:
                    continue
                qs = l["kc"][:]
                rng.shuffle(qs)
                qs = qs[:rng.choice([3, 3, 4])]
                # a revisit is easier: they have met the material before
                p_right = min(0.97, max(0.15, ability + 0.08 + rng.gauss(0, 0.10)))
                s, miss = 0, []
                for q in qs:
                    if rng.random() < p_right:
                        s += 1
                    else:
                        wrong = [o for i2, o in enumerate(q["options"]) if i2 != q["correct"]]
                        miss.append({"q": q["q"], "chose": rng.choice(wrong) if wrong else "",
                                     "right": q["options"][q["correct"]]})
                d = max(1, rng.uniform(lo, hi) + shift)
                key = "%s/%s/%s" % (SUB, slug, n)
                if key in kc and days_since(kc[key]["d"]) <= d:
                    continue                  # already seen more recently than this
                kc[key] = {"d": iso(d), "s": s, "t": len(qs), "miss": miss}
    # marked exam answers — the thing the markbook and the weekly read are built from
    pool = []
    for slug, taught, _w, _d in COURSE[:3]:
        for l in mat[slug]["lessons"][:taught]:
            for p in l["pq"]:
                if p["type"] and p["text"]:
                    pool.append((slug, l["n"], p))
    n_ans = 0 if engage < 0.2 else rng.randint(2, 4) if engage > 0.75 else rng.randint(1, 3)
    fresh = engage > 0.45 and rng.random() < 0.62     # wrote one in the last few days
    for j, (slug, n, p) in enumerate(rng.sample(pool, min(len(pool), n_ans))):
        of = int(str(p["type"]).split()[0]) if str(p["type"])[:2].strip().isdigit() else 8
        frac = min(1.0, max(0.12, ability - 0.16 + rng.gauss(0, 0.10)))
        got = max(1, min(of, int(round(of * frac))))
        note = rng.choice(NOTES_GOOD if frac > 0.72 else NOTES_MID if frac > 0.45 else NOTES_LOW)
        d = rng.randint(1, 6) if (fresh and j == 0) else rng.randint(7, 44)
        practice.append({"d": iso(d), "k": "%s/%s/%s" % (SUB, slug, n), "q": p["text"][:240],
                         "m": of, "t": p["type"],
                         "a": "", "r": "Mark: %d/%d\n\n%s" % (got, of, note), "_mark": (got, of)})
    practice.sort(key=lambda e: e["d"], reverse=True)
    return kc, done, when, practice

def post(path, body, prefer):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer=prefer), method="POST"), timeout=120).read()

def snapshot(built, week):
    """What this class looked like on `week`, read off the same evidence.

    api/cron/weekly-reads.js takes this every Monday and the class screen prints
    the difference as "since last Monday". The old rows describe units this class
    no longer studies, so leaving them would make the screen compare a history
    course with a different one.
    """
    day = date.fromisoformat(week)
    units, right, total, evid, marked = {}, 0, 0, 0, 0
    per = [strength_units(b["_kc"], b["_done"], b["_when"], b["_practice"], day) for b in built]
    for slug, _t, _w, _d in COURSE:
        c = {"g": 0, "a": 0, "r": 0}
        notyet = under = 0
        tot = cnt = 0
        for u in per:
            x = u.get(slug)
            if not x:
                notyet += 1
                continue
            c[x["band"]] += 1
            tot += x["s"]; cnt += 1
            if x["s"] < REVISIT_LINE:
                under += 1
        units[slug] = {"score": round(tot / cnt) if cnt else None, "secure": c["g"],
                       "developing": c["a"], "emerging": c["r"], "notYet": notyet, "under": under}
    for b in built:
        seen = False
        for e in b["_kc"].values():
            if date.fromisoformat(e["d"]) <= day:
                right += e["s"]; total += e["t"]; seen = True
        evid += 1 if seen else 0
        marked += sum(1 for e in b["_practice"] if date.fromisoformat(e["d"]) <= day)
    return {"recall": round(100 * right / total) if total else None, "answered": total,
            "withEvidence": evid, "marked": marked, "units": units}

def summarise(rows, mat, label):
    print("\n%s" % label)
    print("  %-34s %7s %10s %8s %8s %6s" % ("unit", "secure", "developing", "emerging", "not yet", "cold"))
    tot_r = tot_t = 0
    for slug, _t, _w, _d in COURSE:
        c = {"g": 0, "a": 0, "r": 0}
        notyet = cold = 0
        for r in rows:
            u = r["_units"].get(slug)
            if not u:
                notyet += 1
            else:
                c[u["band"]] += 1
                cold += 1 if u["drop"] else 0
        print("  %-34s %7d %10d %8d %8d %6d" % (mat[slug]["name"][:34], c["g"], c["a"], c["r"], notyet, cold))
    for r in rows:
        for e in r["_kc"].values():
            tot_r += e["s"]; tot_t += e["t"]
    print("  class quiz accuracy: %d%% over %d answers · %d pupils with evidence"
          % (round(100 * tot_r / tot_t) if tot_t else 0, tot_t,
             sum(1 for r in rows if r["_kc"])))
    print("  marked answers: %d" % sum(len(r["_practice"]) for r in rows))

def main():
    apply = "--apply" in sys.argv
    dump = "--dump-answers" in sys.argv
    snap = "--snapshot" in sys.argv
    written = json.load(io.open(ANSWERS, encoding="utf-8")) if os.path.exists(ANSWERS) else {}
    specs = []
    mat = material()
    backup = {}
    for label, class_id, shift in CLASSES:
        members = get("class_members?select=student_id&class_id=eq." + class_id)
        ids = [m["student_id"] for m in members]
        people = get("profiles?select=id,full_name&id=in.(%s)" % ",".join(ids))
        name_of = {p["id"]: p["full_name"] for p in people}
        rows = get("progress?select=person_id,blob&person_id=in.(%s)" % ",".join(ids))
        blob_of = {r["person_id"]: (r["blob"] or {}) for r in rows}
        order = sorted(ids, key=lambda i: name_of.get(i, ""))
        rng = random.Random(20260921 + shift)
        tiers = TIERS[:len(order)]
        rng.shuffle(tiers)
        built = []
        for i, pid in enumerate(order):
            prng = random.Random(hash((pid, 4)) & 0xffffffff)
            kc, done, when, practice = build_pupil(prng, tiers[i], mat, shift * 2)
            built.append({"id": pid, "name": name_of.get(pid, "?"), "_kc": kc, "_done": done,
                          "_when": when, "_practice": practice,
                          "_units": strength_units(kc, done, when, practice)})
        summarise(built, mat, "%s — %d pupils" % (label, len(order)))
        for b in built:
            for e in b["_practice"]:
                key = "%s|%s|%s" % (b["id"], e["k"], e["d"])
                if key in written:
                    e["a"] = written[key]
                elif dump:
                    specs.append({"id": key, "q": e["q"], "type": e["t"],
                                  "got": e["_mark"][0], "of": e["_mark"][1],
                                  "unit": mat[e["k"].split("/")[1]]["name"]})
        if snap:
            for week in SNAPSHOT_WEEKS:
                post("class_snapshots?on_conflict=class_id,week",
                     {"class_id": class_id, "week": week, "data": snapshot(built, week)},
                     "resolution=merge-duplicates,return=minimal")
                print("  snapshot rewritten for %s" % week)
        if dump or not apply:
            continue
        for b in built:
            old = blob_of.get(b["id"], {})
            backup[b["id"]] = json.loads(json.dumps(old))
            if os.path.exists(BACKUP):
                backup[b["id"]] = json.load(io.open(BACKUP, encoding="utf-8")).get(b["id"], old)
            new = json.loads(json.dumps(old))
            # drop this subject's old rows, keep every other subject untouched
            new["kc"] = {k: v for k, v in (new.get("kc") or {}).items() if not k.startswith(SUB + "/")}
            new["done"] = {k: v for k, v in (new.get("done") or {}).items() if not k.startswith(SUB + "/")}
            new["when"] = {k: v for k, v in (new.get("when") or {}).items() if not k.startswith(SUB + "/")}
            new["practice"] = [e for e in (new.get("practice") or [])
                               if not str(e.get("k", e.get("key", ""))).startswith(SUB + "/")]
            new["kc"].update(b["_kc"])
            new["done"].update(b["_done"])
            new["when"].update(b["_when"])
            for e in b["_practice"]:
                e = dict(e); e.pop("_mark", None)
                new["practice"].append(e)
            new["practice"].sort(key=lambda e: e.get("d", ""), reverse=True)
            new["updated"] = TODAY.isoformat()
            patch("progress?person_id=eq." + b["id"], {"blob": new, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        print("  written")
    if apply and backup:
        if os.path.exists(BACKUP):
            print("\nbackup %s is already on disk — kept, not overwritten" % BACKUP)
        else:
            io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
            print("\nbackup of every blob written to %s" % BACKUP)
    if dump:
        io.open(os.path.join(HERE, "_demo_class_answer_specs.json"), "w", encoding="utf-8").write(
            json.dumps(specs, ensure_ascii=False, indent=1))
        print("\n%d answers to write: scripts/_demo_class_answer_specs.json" % len(specs))
    elif not apply:
        print("\n(dry run — nothing written; add --apply) · %d pupil answers on file" % len(written))

def restore(path):
    data = json.load(io.open(path, encoding="utf-8"))
    for pid, blob in data.items():
        patch("progress?person_id=eq." + pid, {"blob": blob})
    print("restored %d pupils from %s" % (len(data), path))

if __name__ == "__main__":
    if "--restore" in sys.argv:
        restore(sys.argv[sys.argv.index("--restore") + 1])
    else:
        main()
