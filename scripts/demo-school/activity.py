"""Demo High phase B — activity histories into BOTH sinks.

For every seeded student: ~6 weeks of realistic revision evidence built from
REAL lessons (real questions, real distractors, real flashcards), written to
  1) user_metadata.sv_progress + sv_welcome  -> their own dashboards work
  2) public.events                           -> the teacher pipeline works

Class-level phenomena baked in so the teacher dashboard has findings:
shared misconceptions (a majority picks the SAME distractor on a seeded
question), one fading unit per subject, grafter/quiet/flying archetypes.

Usage:
  python scripts/demo-school/activity.py --limit 2     # test on 2 students
  python scripts/demo-school/activity.py               # whole cohort
  python scripts/demo-school/activity.py --wipe-events # clear events only
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import random
import sys
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
DAYS = 42            # evidence window
TODAY = dt.date.today()

# family/board mapping for sv_welcome (mirrors design-lab/dash-data.js SUBSLUG)
FAM = {
    "maths-edexcel": ("maths", "edexcel", "Edexcel"),
    "english-language-aqa": ("lang", "aqa", "AQA"),
    "english-literature-aqa": ("lit", "aqa", "AQA"),
    "science-aqa": ("science", "aqa", "AQA"),
    "separate-sciences": ("triple", "aqa", "AQA"),
    "history-aqa": ("history", "aqa", "AQA"),
    "geography-aqa": ("geog", "aqa", "AQA"),
    "french-aqa": ("french", "aqa", "AQA"),
    "spanish-aqa": ("spanish", "aqa", "AQA"),
    "business-edexcel": ("business", "edexcel", "Edexcel"),
    "computer-science": ("cs", "ocr", "OCR"),
    "physical-education-aqa": ("pe", "aqa", "AQA"),
    "psychology-aqa": ("psych", "aqa", "AQA"),
    "drama-aqa": ("drama", "aqa", "AQA"),
    "religious-studies-aqa": ("rs", "aqa", "AQA"),
}
PRACTICE_FIRST = {"maths-edexcel", "english-language-aqa", "french-aqa", "spanish-aqa"}
UNIT_PICK = {"history-aqa": 4, "english-literature-aqa": 4,   # departmental choices
             "drama-aqa": 3, "religious-studies-aqa": 8}      # one text; 2 religions + themes
Y10_COVER, Y11_COVER = .42, .78                               # course progress by year


def api(method, path, body=None):
    req = urllib.request.Request(URL + path, method=method,
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=representation"},
        data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path}: {e.code} {e.read().decode()[:200]}") from e


def iso(d): return d.isoformat()


EVENT_KEYS = ("person_id", "school_id", "subject", "unit", "lesson", "kind",
              "ok", "q", "chose", "answer", "tag", "box", "meta", "at")


def norm(e):
    """PostgREST bulk insert demands identical keys on every row."""
    return {k: e.get(k) for k in EVENT_KEYS}


def load_content():
    """subject slug -> {units:[{slug,name,lessons:[{id,n,title,kcs,cards}]}]}"""
    subs = {s["slug"]: s for s in api("GET", "/rest/v1/subjects?school_id=is.null&select=id,slug&limit=300")}
    pack = {}
    for slug in FAM:
        srow = subs.get(slug)
        if not srow:
            print("  !! subject missing:", slug); continue
        units = api("GET", f"/rest/v1/units?subject_id=eq.{srow['id']}&select=id,slug,name,sort_order&order=sort_order")
        units = units[:UNIT_PICK.get(slug, len(units))]
        ulist = []
        for u in units:
            rows = api("GET", f"/rest/v1/lessons?unit_id=eq.{u['id']}"
                       "&select=id,lesson_number,title,knowledge_checks,flashcard_questions&order=lesson_number")
            lessons = []
            for r in rows:
                kcs = [k for k in (r.get("knowledge_checks") or [])
                       if isinstance(k, dict) and k.get("type") in ("mcq", "fill")
                       and isinstance(k.get("options"), list) and len(k["options"]) >= 3
                       and isinstance(k.get("correct"), int) and k.get("q")]
                lessons.append({"id": r["id"], "n": r["lesson_number"], "title": r["title"] or "",
                                "kcs": kcs, "ncards": len(r.get("flashcard_questions") or [])})
            if lessons:
                ulist.append({"slug": u["slug"], "name": u["name"], "lessons": lessons})
        if ulist:
            pack[slug] = ulist
            print(f"  {slug}: {len(ulist)} units, {sum(len(u['lessons']) for u in ulist)} lessons")
    return pack


def stable(*parts):
    return int(hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:8], 16)


def simulate(student, pack, shared_mc, shared_pick, fading, rng):
    """Return (sv_progress, sv_welcome, events[]) for one student."""
    ability, days_p = student["ability"], student["days"]
    year = student["year"]
    cover = (Y11_COVER if year == 11 else Y10_COVER) * (0.65 + ability * 0.7)
    prog = {"done": {}, "when": {}, "warmlog": {}, "kc": {}, "shortschecks": [],
            "flashlog": [], "miscon": [], "practice": [],
            "flashsr": {"cards": {}, "streak": 0}, "warmup": None, "plan": None,
            "flashday": None, "tasks": {}}
    events = []
    mysubs = [s for s in student["subjects"] if s in pack]

    # ---- course coverage: lessons done, spread over the past term ----------
    for slug in mysubs:
        units = pack[slug]
        flat = [(u, l) for u in units for l in u["lessons"]]
        ndone = int(len(flat) * min(.96, max(.05, cover + rng.uniform(-.08, .08))))
        for i, (u, l) in enumerate(flat[:ndone]):
            key = slug + "/" + u["slug"]
            prog["done"].setdefault(key, []).append(l["n"])
            # completion dates: most are old; the recent tail lands in-window
            age = int((1 - (i + 1) / max(1, ndone)) * 110) + rng.randint(0, 6)
            d = TODAY - dt.timedelta(days=age)
            # EVERY completion becomes an event (pace/coverage read all-time);
            # only recent ones get a sv-lessons-when stamp (that powers the
            # student's "this week" figures, mirroring real capture)
            events.append({"kind": "lesson_done", "subject": slug, "unit": u["slug"],
                           "lesson": l["n"], "at": iso(d) + "T17:30:00Z"})
            if age <= DAYS:
                prog["when"][key + "/" + str(l["n"])] = iso(d)

    # ---- daily revision over the evidence window ---------------------------
    for back in range(DAYS, -1, -1):
        d = TODAY - dt.timedelta(days=back)
        date = iso(d)
        # crammers wake up near the end; Y11 revise harder as exams near
        p = days_p * (2.2 if student["archetype"] == "crammer" and back <= 6 else
                      (0.35 if student["archetype"] == "crammer" else 1))
        p *= 1.25 if year == 11 else 1
        if rng.random() > min(.95, p):
            continue
        active = rng.sample(mysubs, k=min(len(mysubs), rng.randint(1, 3)))
        for slug in active:
            art = slug not in PRACTICE_FIRST
            units = pack[slug]
            started = [u for u in units
                       if (slug + "/" + u["slug"]) in prog["done"]] or units[:1]
            def ab(u):
                a = ability + rng.uniform(-.1, .1)
                if fading.get(slug) == u["slug"] and back <= 14: a *= .72
                return max(.05, min(.97, a))
            if art:
                # warm-up: 10 real KCs from studied units. The seeded anchor
                # question appears often (like the one everyone gets wrong) so
                # class-level misconception clustering has enough signal.
                bank = [(u, l, k) for u in started for l in u["lessons"] for k in l["kcs"]]
                if bank:
                    picks = [bank[rng.randrange(len(bank))] for _ in range(10)]
                    sp = shared_pick.get(slug)
                    if sp and rng.random() < .5:
                        picks[rng.randrange(len(picks))] = sp
                    ok_n, misses, ua = 0, [], {}
                    for (u, l, k) in picks:
                        uk = slug + "/" + u["slug"]
                        ua.setdefault(uk, {"a": 0, "m": 0}); ua[uk]["a"] += 1
                        if rng.random() < ab(u):
                            ok_n += 1
                            events.append({"kind": "warmup", "subject": slug, "unit": u["slug"],
                                           "lesson": l["n"], "ok": True, "at": date + "T07:45:00Z"})
                        else:
                            ua[uk]["m"] += 1
                            wrong = [i for i in range(len(k["options"])) if i != k["correct"]]
                            smc = shared_mc.get((slug, k["q"]))
                            if smc is not None and rng.random() < .75: ci = smc
                            elif stable(student["email"], k["q"]) % 100 < 35: ci = wrong[stable(student["email"], k["q"], "x") % len(wrong)]
                            else: ci = rng.choice(wrong)
                            chose = str(k["options"][ci])[:90]; right = str(k["options"][k["correct"]])[:90]
                            misses.append({"sub": slug, "unit": u["slug"], "n": l["n"],
                                           "title": l["title"][:80], "q": k["q"][:160],
                                           "chose": chose, "right": right})
                            events.append({"kind": "warmup", "subject": slug, "unit": u["slug"],
                                           "lesson": l["n"], "ok": False, "q": k["q"][:160],
                                           "chose": chose, "answer": right, "at": date + "T07:45:00Z"})
                    wl = prog["warmlog"].setdefault(date, {"correct": 0, "total": 0, "misses": [], "units": {}})
                    wl["correct"] += ok_n; wl["total"] += len(picks)
                    wl["misses"] += misses
                    for uk, v in ua.items():
                        t = wl["units"].setdefault(uk, {"a": 0, "m": 0})
                        t["a"] += v["a"]; t["m"] += v["m"]
                # a lesson quiz some days
                if rng.random() < .5:
                    u = rng.choice(started); l = rng.choice(u["lessons"])
                    if l["kcs"]:
                        t = len(l["kcs"]); s_n, miss = 0, []
                        for k in l["kcs"]:
                            if rng.random() < ab(u): s_n += 1
                            else:
                                wrong = [i for i in range(len(k["options"])) if i != k["correct"]]
                                ci = rng.choice(wrong)
                                miss.append({"q": k["q"][:160], "chose": str(k["options"][ci])[:90],
                                             "right": str(k["options"][k["correct"]])[:90]})
                                events.append({"kind": "quiz", "subject": slug, "unit": u["slug"],
                                               "lesson": l["n"], "ok": False, "q": k["q"][:160],
                                               "chose": miss[-1]["chose"], "answer": miss[-1]["right"],
                                               "at": date + "T18:10:00Z"})
                        for _ in range(s_n):
                            events.append({"kind": "quiz", "subject": slug, "unit": u["slug"],
                                           "lesson": l["n"], "ok": True, "at": date + "T18:10:00Z"})
                        prog["kc"][slug + "/" + u["slug"] + "/" + str(l["n"])] = \
                            {"s": s_n, "t": t, "d": date, "miss": miss[:5]}
                # flashcards: box moves on real card keys (lessonId:qN)
                if rng.random() < .45:
                    u = rng.choice(started)
                    with_cards = [l for l in u["lessons"] if l["ncards"]]
                    for _ in range(rng.randint(4, 10)):
                        if not with_cards: break
                        l = rng.choice(with_cards)
                        ck = l["id"] + ":q" + str(rng.randrange(l["ncards"]))
                        c = prog["flashsr"]["cards"].setdefault(ck, {"box": 1, "attempts": 0, "correct": 0})
                        c["attempts"] += 1
                        okc = rng.random() < ab(u)
                        if okc: c["box"] = min(5, c["box"] + 1); c["correct"] += 1
                        else: c["box"] = 1
                        prog["flashlog"].append({"t": stable(student["email"], date, ck), "unit": u["slug"], "ok": okc,
                                                 "q": l["title"][:60]})
                        events.append({"kind": "flash", "subject": slug, "unit": u["slug"],
                                       "lesson": l["n"], "ok": okc, "box": c["box"],
                                       "meta": {"card": ck}, "at": date + "T19:05:00Z"})
            else:
                # practice-first: a session of graded problems
                u = rng.choice(started)
                for _ in range(rng.randint(4, 9)):
                    okp = rng.random() < ab(u)
                    events.append({"kind": "practice", "subject": slug, "unit": u["slug"],
                                   "lesson": rng.choice(u["lessons"])["n"], "ok": okp,
                                   "at": date + "T17:20:00Z"})
    prog["flashlog"] = prog["flashlog"][-400:]
    last = sorted(prog["warmlog"])[-1:] if prog["warmlog"] else []
    if last:
        w = prog["warmlog"][last[0]]
        prog["warmup"] = {"date": last[0], "correct": w["correct"], "total": w["total"]}

    # ---- sv_welcome: their shelf ------------------------------------------
    picked, boards, meta, topics = [], {}, {}, {}
    for slug in student["subjects"]:
        f = FAM.get(slug)
        if not f: continue
        fam, bkey, blabel = f
        picked.append(fam); boards[fam] = bkey
        m = {"board": blabel}
        if slug in UNIT_PICK and slug in pack:
            tslugs = [u["slug"] for u in pack[slug]]
            topics[fam] = tslugs
            m["topics"] = [u["name"] for u in pack[slug]]
        meta[fam] = m
    welcome = {"picked": picked, "boards": boards, "topics": topics, "meta": meta}
    return prog, welcome, events


def slim(prog):
    """user_metadata rides inside EVERY access token — Supabase embeds it in
    the JWT — so it must stay tiny or Cloudflare 520s all PostgREST calls
    (proved by the first full-size seed). Keep just what the student's own
    dashboards read; the rich history lives in the events table."""
    sp = {"done": prog["done"], "warmup": prog["warmup"], "plan": None,
          "flashday": None, "tasks": {}, "flashlog": [], "shortschecks": [],
          "miscon": [], "practice": prog["practice"][:1],
          "kc": {k: {"s": v["s"], "t": v["t"], "d": v["d"]}
                 for k, v in list(prog["kc"].items())[-25:]},
          "when": {}, "warmlog": {}, "flashsr": {"cards": {}, "streak": prog["flashsr"].get("streak", 0)}}
    cut = iso(TODAY - dt.timedelta(days=14))
    for k, v in prog["when"].items():
        if v >= cut: sp["when"][k] = v
    for d in sorted(prog["warmlog"])[-7:]:
        w = prog["warmlog"][d]
        sp["warmlog"][d] = {"correct": w["correct"], "total": w["total"], "units": w["units"],
                            "misses": [{"sub": m["sub"], "unit": m["unit"], "n": m["n"],
                                        "title": m["title"][:48]} for m in w["misses"][:3]]}
    cards = sorted(prog["flashsr"]["cards"].items(),
                   key=lambda kv: kv[1].get("attempts", 0), reverse=True)[:40]
    sp["flashsr"]["cards"] = dict(cards)
    return sp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", help="email substring filter")
    ap.add_argument("--wipe-events", action="store_true")
    ap.add_argument("--meta-only", action="store_true",
                    help="re-PUT slimmed user_metadata; no event writes (sim is deterministic)")
    args = ap.parse_args()

    school = api("GET", "/rest/v1/schools?slug=eq.demo-high&select=id")[0]["id"]
    if args.wipe_events:
        # a whole-tenant delete can exceed the REST statement timeout — chunk it
        while True:
            rows = api("GET", f"/rest/v1/events?school_id=eq.{school}&select=id&order=id&limit=1")
            if not rows: break
            hi = rows[0]["id"] + 20000
            api("DELETE", f"/rest/v1/events?school_id=eq.{school}&id=lt.{hi}")
            print("  wiped a chunk up to id", hi)
        print("events wiped"); return

    print("loading content bank...")
    pack = load_content()
    students = api("GET", f"/rest/v1/profiles?school_id=eq.{school}&role=eq.student&select=id,email,settings&order=email&limit=1000")
    students = [dict(s["settings"], id=s["id"], email=s["email"]) for s in students if s.get("settings")]
    if args.only: students = [s for s in students if args.only in s["email"]]
    if args.limit: students = students[:args.limit]
    print(len(students), "students to simulate")

    # class-wide phenomena: one shared misconception per article subject
    # (a real early-unit question + one fixed distractor), one fading unit
    rng0 = random.Random(20261011)
    shared_mc, shared_pick, fading = {}, {}, {}
    for slug, units in pack.items():
        if slug in PRACTICE_FIRST: continue
        bank = [(u, l, k) for u in units[:1] for l in u["lessons"][:6] for k in l["kcs"]]
        if bank:
            u, l, k = bank[rng0.randrange(len(bank))]
            wrong = [i for i in range(len(k["options"])) if i != k["correct"]]
            shared_mc[(slug, k["q"])] = rng0.choice(wrong)
            shared_pick[slug] = (u, l, k)
        if len(units) > 1:
            fading[slug] = units[rng0.randrange(1, len(units))]["slug"]

    batch, total_ev = [], 0
    for i, s in enumerate(students):
        rng = random.Random(stable(s["email"], "sim"))
        prog, welcome, events = simulate(s, pack, shared_mc, shared_pick, fading, rng)
        api("PUT", f"/auth/v1/admin/users/{s['id']}",
            {"user_metadata": {"full_name": s.get("full_name"), "is_demo": True,
                               "sv_welcome": welcome, "sv_progress": dict(slim(prog), updated=TODAY.isoformat())}})
        if args.meta_only:
            if i % 20 == 0: print(f"  meta {i}/{len(students)}")
            continue
        for e in events:
            e["person_id"] = s["id"]; e["school_id"] = school
        batch += [norm(e) for e in events]; total_ev += len(events)
        while len(batch) >= 800:
            api("POST", "/rest/v1/events", batch[:800]); batch = batch[800:]
        if i % 10 == 0:
            print(f"  {i}/{len(students)}  ({total_ev} events so far)")
    if batch:
        api("POST", "/rest/v1/events", batch)
    print(f"done: {len(students)} students, {total_ev} events")


if __name__ == "__main__":
    main()
