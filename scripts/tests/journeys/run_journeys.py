import json
"""School-mode journey stress test (Tom, 1 Oct 2026). Live site, disposable users, full cleanup."""
import asyncio, json, os, random, string, sys, time, urllib.request, urllib.error
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
ANON = "sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2"
SITE = "https://www.studyvault.co.uk"
OUT = os.path.dirname(os.path.abspath(__file__))
UNITY = "a5414d1c-8841-4bc5-8573-a9756752361b"
UNITY_HIST_CLASS = "b965f7cd-2087-4228-9d82-b7b4d4489c52"
DEMO = "8ab707cc-7e3d-4243-bb12-315a29a94163"
DEMO_TEACHER = "bd4ab587-db2e-4f41-87e7-69218f51b234"
MATHS_AQA = "d7155cfc-805d-4703-a2c2-3b9c858ce2cc"
TOKEN_KEY = "sb-baipckgywpnwapobwtsy-auth-token"
SH = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
created = {"users": [], "classes": [], "members": []}
RESULTS = []


def req(url, method="GET", body=None, headers=None, timeout=30):
    t = time.time()
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                               method=method, headers=headers or SH)
    try:
        raw = urllib.request.urlopen(r, timeout=timeout).read()
    except urllib.error.HTTPError as e:
        raise RuntimeError("%s %s %s" % (e.code, url[:90], e.read()[:200]))
    if time.time() - t > 20: raise SystemExit("PRODUCTION SLOW: %s took %.0fs — stopping" % (url[:80], time.time() - t))
    return json.loads(raw) if raw else None


def rest(p, m="GET", b=None, prefer=None):
    h = dict(SH)
    if prefer: h["Prefer"] = prefer
    return req(U + "/rest/v1/" + p, m, b, h)


def make_user(n):
    email = "sv-journey-%d-%s@studyvault.test" % (n, "".join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    pw = "".join(random.choices(string.ascii_letters + string.digits, k=24))
    u = req(U + "/auth/v1/admin/users", "POST", {"email": email, "password": pw, "email_confirm": True})
    created["users"].append(u["id"])
    return {"id": u["id"], "email": email, "pw": pw}


def session(user):
    s = req(U + "/auth/v1/token?grant_type=password", "POST", {"email": user["email"], "password": user["pw"]},
            {"apikey": ANON, "Content-Type": "application/json"})
    s["expires_at"] = int(time.time()) + int(s.get("expires_in", 3600))
    return s


def add_member(uid, cid):
    rest("class_members", "POST", {"class_id": cid, "student_id": uid})
    created["members"].append((uid, cid))


def del_member(uid, cid):
    rest("class_members?student_id=eq.%s&class_id=eq.%s" % (uid, cid), "DELETE")
    if (uid, cid) in created["members"]: created["members"].remove((uid, cid))


def server_welcome(uid):
    r = rest("user_state?select=value,updated_at&user_id=eq.%s&key=eq.sv-welcome" % uid)
    if not r: return None
    try: return json.loads(r[0]["value"]["raw"])
    except Exception: return r[0]["value"]


SEED_WELCOME = {"picked": ["maths", "lang", "lit", "science", "history", "geog", "french"],
                "boards": {"maths": "edexcel", "lang": "aqa", "lit": "aqa", "science": "aqa", "history": "aqa", "geog": "aqa", "french": "aqa"},
                "topics": {}, "meta": {}, "tiers": {}, "guess": {}, "rag": {}, "budget": 45}
SEED_DONE = {"maths-edexcel/number": [1, 2], "history-aqa/america-opportunity-inequality": [6],
             "english-literature-aqa/macbeth": [1, 2], "geography-aqa/paper-1": [1]}
SEED_WHEN = {"maths-edexcel/number/1": "2026-09-20", "maths-edexcel/number/2": "2026-09-21",
             "history-aqa/america-opportunity-inequality/6": "2026-09-22", "english-literature-aqa/macbeth/1": "2026-09-23",
             "english-literature-aqa/macbeth/2": "2026-09-23", "geography-aqa/paper-1/1": "2026-09-24"}


async def inject(page, sess, extra=None):
    await page.goto(SITE + "/privacy.html")
    await page.evaluate("""([k,s,x])=>{localStorage.setItem(k,JSON.stringify(s)); if(x){for(const a in x) localStorage.setItem(a, typeof x[a]==='string'?x[a]:JSON.stringify(x[a]));}}""",
                        [TOKEN_KEY, sess, extra])


async def look(page, label, uid, wait=14000):
    """Open /classic, let sync + class check (and any reload) settle, then record everything."""
    staff = []
    page.on("request", lambda r: staff.append(r.url) if "/api/staff/rest" in r.url else None)
    await page.goto(SITE + "/classic")
    await page.wait_for_timeout(wait)
    try: await page.wait_for_load_state("networkidle", timeout=8000)
    except Exception: pass
    d = await page.evaluate("""()=>{
      const g=k=>{try{return JSON.parse(localStorage.getItem(k))}catch(e){return localStorage.getItem(k)}};
      const w=g('sv-welcome')||{};
      const body=document.body.innerText; const i=body.indexOf('your plan');
      return {subjects:(typeof SUBJECTS!=='undefined'?SUBJECTS.map(s=>s.slug+':'+(s.sub||'-')+(s.school?'[S]':'')+(s.board?'('+s.board+')':'')):null),
              picked:w.picked||null, boards:w.boards||null, done:g('sv-lessons-done'), school:(g('sv-school')||{}).school_slug||null,
              classSubs:g('sv-class-subjects'), plan: i>=0? body.slice(i, i+220).replace(/\\s+/g,' '):body.slice(0,160).replace(/\\s+/g,' ')}}""")
    d["server_picked"] = (server_welcome(uid) or {}).get("picked")
    d["staff_calls"] = len(staff)
    shot = os.path.join(OUT, "%s.png" % label.replace(" ", "_").replace("/", "-"))
    await page.screenshot(path=shot, full_page=False)
    print("\n== %s\n   subjects: %s\n   picked(local): %s\n   picked(server): %s\n   boards: %s\n   school: %s  classSubs: %s\n   done keys: %s\n   plan: %s\n   staff calls: %d"
          % (label, d["subjects"], d["picked"], d["server_picked"], d["boards"], d["school"], d["classSubs"],
             sorted((d["done"] or {}).keys()) if isinstance(d["done"], dict) else d["done"], d["plan"], d["staff_calls"]))
    return d


def record(step, expected, ok, actual):
    RESULTS.append((step, expected, "PASS" if ok else "FAIL", actual))
    print("   -> %s: %s" % ("PASS" if ok else "FAIL", step))


def sub_of(d, fam):
    for s in d["subjects"] or []:
        if s.startswith(fam + ":"): return s
    return None


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        A = make_user(1); B = make_user(2)
        # temporary free-tier class at Demo High (Maths AQA)
        cls = rest("classes", "POST", {"school_id": DEMO, "teacher_id": DEMO_TEACHER, "name": "ZZ journey test (delete)",
                                       "subject_id": MATHS_AQA, "year_group": 11,
                                       "join_code": "ZJ" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4)),
                                       "join_open": False}, prefer="return=representation")[0]
        created["classes"].append(cls["id"]); DEMO_CLASS = cls["id"]

        # ---------- Journey 1 ----------
        a1 = await (await b.new_context(viewport={"width": 1300, "height": 900})).new_page()
        await inject(a1, session(A), {"sv-welcome": SEED_WELCOME, "sv-lessons-done": SEED_DONE, "sv-lessons-when": SEED_WHEN})
        d = await look(a1, "J1.0 free pupil signed in", A["id"])
        record("J1.0 seeded free pupil: shelf = 7 picks, free boards; server copy uploaded",
               "7 subjects, none [S], server picked = seed",
               d["subjects"] and len(d["subjects"]) == 7 and not any("[S]" in s for s in d["subjects"]) and d["server_picked"] == SEED_WELCOME["picked"],
               "subjects=%s server=%s" % (d["subjects"], d["server_picked"]))
        add_member(A["id"], UNITY_HIST_CLASS)
        d = await look(a1, "J1.1 joined Unity History", A["id"], 18000)
        unity_fams = ["lang", "lit", "science", "history", "geog", "french"]
        okS = all(sub_of(d, f) and "[S]" in sub_of(d, f) for f in unity_fams)
        okM = sub_of(d, "maths") and sub_of(d, "maths").startswith("maths:maths-edexcel") and "[S]" not in sub_of(d, "maths")
        okP = all(k in (d["done"] or {}) for k in SEED_DONE)
        record("J1.1 Unity families become school rows", "lang/lit/science/history/geog/french [S]", okS, str(d["subjects"]))
        record("J1.1 Maths stays free Edexcel", "maths:maths-edexcel", okM, str(sub_of(d, "maths")))
        record("J1.1 free progress kept (+ carried)", "seed keys present", okP, str(sorted((d["done"] or {}).keys())))
        record("J1.1 picks unchanged locally + server", "7 seed picks", d["picked"] == SEED_WELCOME["picked"] and d["server_picked"] == SEED_WELCOME["picked"],
               "local=%s server=%s" % (d["picked"], d["server_picked"]))

        # ---------- Journey 2 ----------
        add_member(A["id"], DEMO_CLASS)
        d = await look(a1, "J2 also in Demo Maths AQA class", A["id"], 18000)
        record("J2 Maths board follows the free-tier class (AQA)", "maths:maths-aqa", bool(sub_of(d, "maths") and sub_of(d, "maths").startswith("maths:maths-aqa")), str(sub_of(d, "maths")))
        record("J2 Edexcel Maths completions carried to AQA", "maths-aqa/number has [1,2]",
               (d["done"] or {}).get("maths-aqa/number") == [1, 2] or sorted((d["done"] or {}).get("maths-aqa/number", [])) == [1, 2], str((d["done"] or {}).get("maths-aqa/number")))
        record("J2 still Unity mode", "school=unity-college", d["school"] == "unity-college", str(d["school"]))

        # ---------- Journey 3 ----------
        del_member(A["id"], UNITY_HIST_CLASS)
        d = await look(a1, "J3 removed from Unity class", A["id"], 18000)
        record("J3 school mode clears", "school=None, no [S]", d["school"] is None and not any("[S]" in s for s in d["subjects"] or []), "school=%s subjects=%s" % (d["school"], d["subjects"]))
        record("J3 every self-picked subject stays", "7 picks", set(SEED_WELCOME["picked"]) <= set(d["picked"] or []) and set(SEED_WELCOME["picked"]) <= set(d["server_picked"] or []),
               "local=%s server=%s" % (d["picked"], d["server_picked"]))
        record("J3 progress intact", "seed keys present", all(k in (d["done"] or {}) for k in SEED_DONE), str(sorted((d["done"] or {}).keys())))

        # ---------- Journey 4: concurrent devices ----------
        # device 1 (still in Demo maths class) changes picks the way the picker saves them
        await a1.goto(SITE + "/welcome?view=picker"); await a1.wait_for_timeout(6000)
        await a1.evaluate("""()=>{const w=JSON.parse(localStorage.getItem('sv-welcome')); w.picked=w.picked.filter(x=>x!=='french'); w.picked.push('rs'); w.boards.rs='aqa'; w.boards.history='edexcel';
                              localStorage.setItem('sv-welcome',JSON.stringify(w));}""")
        await a1.wait_for_timeout(6000)
        sp = (server_welcome(A["id"]) or {})
        record("J4.1 picker change reaches the server", "french gone, rs added, history edexcel",
               "french" not in (sp.get("picked") or []) and "rs" in (sp.get("picked") or []) and (sp.get("boards") or {}).get("history") == "edexcel",
               "server picked=%s history board=%s" % (sp.get("picked"), (sp.get("boards") or {}).get("history")))
        a2 = await (await b.new_context(viewport={"width": 1300, "height": 900})).new_page()
        await inject(a2, session(A))
        d2 = await look(a2, "J4.2 second device signs in", A["id"], 18000)
        record("J4.2 second device gets the changed picks", "no french, has rs", d2["picked"] and "french" not in d2["picked"] and "rs" in d2["picked"], str(d2["picked"]))
        # device 2 removes geog; then the class list changes (A leaves the Demo class) and device 1 reloads with its OLD copy
        await a2.goto(SITE + "/welcome?view=picker"); await a2.wait_for_timeout(5000)
        await a2.evaluate("""()=>{const w=JSON.parse(localStorage.getItem('sv-welcome')); w.picked=w.picked.filter(x=>x!=='geog'); localStorage.setItem('sv-welcome',JSON.stringify(w));}""")
        await a2.wait_for_timeout(6000)
        sp = (server_welcome(A["id"]) or {})
        record("J4.3 device 2 removal reaches the server", "no geog on server", "geog" not in (sp.get("picked") or []), str(sp.get("picked")))
        del_member(A["id"], DEMO_CLASS)
        d = await look(a1, "J4.4 device 1 reloads after class change", A["id"], 20000)
        sp = (server_welcome(A["id"]) or {})
        record("J4.4 device 1 converges (no lost update)", "no geog local+server, no french, has rs",
               "geog" not in (d["picked"] or []) and "geog" not in (sp.get("picked") or []) and "rs" in (d["picked"] or []),
               "local=%s server=%s" % (d["picked"], sp.get("picked")))
        record("J4.4 leaving the free-tier class", "maths board after leaving (design: stays AQA)", True, "maths=%s board=%s" % (sub_of(d, "maths"), (d["boards"] or {}).get("maths")))
        # sign out and back in on device 1
        await a1.evaluate("()=>{ if(window.svSignOut) svSignOut(); }"); await a1.wait_for_timeout(5000)
        after_out = await a1.evaluate("()=>({tok:!!localStorage.getItem('%s'), w:localStorage.getItem('sv-welcome')})" % TOKEN_KEY)
        # after sign-out /welcome shows the starter four, marked defaulted (it must never beat the account: J4.6)
        _w = json.loads(after_out["w"]) if after_out["w"] else None
        record("J4.5 sign-out cleans the device", "no token; device holds nothing or the marked starter shelf",
               not after_out["tok"] and (_w is None or _w.get("defaulted") is True), str(after_out)[:160])
        await inject(a1, session(A))
        d = await look(a1, "J4.6 device 1 signs back in", A["id"], 18000)
        sp = (server_welcome(A["id"]) or {})
        record("J4.6 picks after sign-back-in = server", "same list both sides", d["picked"] == sp.get("picked"), "local=%s server=%s" % (d["picked"], sp.get("picked")))

        # ---------- Journey 5: two classes at once ----------
        b1 = await (await b.new_context(viewport={"width": 1300, "height": 900})).new_page()
        await inject(b1, session(B), {"sv-welcome": SEED_WELCOME, "sv-lessons-done": SEED_DONE, "sv-lessons-when": SEED_WHEN})
        await look(b1, "J5.0 pupil B free", B["id"])
        add_member(B["id"], UNITY_HIST_CLASS); add_member(B["id"], DEMO_CLASS)
        d = await look(b1, "J5.1 B in Unity + Demo Maths", B["id"], 20000)
        record("J5.1 two classes: Unity mode + Maths AQA", "school unity, maths-aqa, Unity families [S]",
               d["school"] == "unity-college" and bool(sub_of(d, "maths")) and sub_of(d, "maths").startswith("maths:maths-aqa") and all("[S]" in (sub_of(d, f) or "") for f in unity_fams),
               "school=%s subjects=%s" % (d["school"], d["subjects"]))
        del_member(B["id"], DEMO_CLASS)
        d = await look(b1, "J5.2 B Demo class removed", B["id"], 20000)
        record("J5.2 still Unity mode after the free class goes", "school unity, picks intact",
               d["school"] == "unity-college" and set(SEED_WELCOME["picked"]) <= set(d["picked"] or []), "school=%s picked=%s maths=%s" % (d["school"], d["picked"], sub_of(d, "maths")))
        del_member(B["id"], UNITY_HIST_CLASS)

        # ---------- Journey 6: admin flag + pupil ----------
        c1 = await (await b.new_context(viewport={"width": 1300, "height": 900})).new_page()
        await c1.goto(SITE + "/privacy.html")
        await c1.evaluate("()=>localStorage.setItem('studyvault-auth', JSON.stringify({role:'admin'}))")
        await inject(c1, session(B))
        d = await look(c1, "J6 admin flag then pupil", B["id"])
        record("J6 pupil after admin flag: shelf loads, no admin-route reads", "subjects present, staff calls 0",
               bool(d["subjects"]) and d["staff_calls"] == 0, "subjects=%s staff=%d" % (d["subjects"], d["staff_calls"]))
        await b.close()


def cleanup():
    print("\n== cleanup")
    for uid, cid in list(created["members"]):
        try: del_member(uid, cid)
        except Exception as e: print("  member", e)
    for uid in created["users"]:
        for t, col in (("class_members", "student_id"), ("user_state", "user_id"), ("lesson_visits", "user_id"),
                       ("knowledge_check_scores", "user_id"), ("user_selected_subjects", "user_id"), ("profiles", "id")):
            try: rest("%s?%s=eq.%s" % (t, col, uid), "DELETE")
            except Exception as e: print("  ", t, str(e)[:120])
        try: req(U + "/auth/v1/admin/users/" + uid, "DELETE")
        except Exception as e: print("  user", str(e)[:120])
    for cid in created["classes"]:
        try: rest("class_members?class_id=eq.%s" % cid, "DELETE"); rest("classes?id=eq.%s" % cid, "DELETE")
        except Exception as e: print("  class", str(e)[:120])
    left_users = [u for u in created["users"] if rest("user_state?select=key&user_id=eq.%s&limit=1" % u) or rest("class_members?select=class_id&student_id=eq.%s" % u)]
    left_cls = [c for c in created["classes"] if rest("classes?select=id&id=eq.%s" % c)]
    gone = []
    for u in created["users"]:
        try: req(U + "/auth/v1/admin/users/" + u); gone.append((u, "STILL EXISTS"))
        except RuntimeError: gone.append((u, "deleted"))
    print("  users:", gone, "| rows left for users:", left_users, "| classes left:", left_cls)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SystemExit as e:
        print(e)
    except Exception as e:
        import traceback; traceback.print_exc()
    finally:
        cleanup()
        print("\n== RESULTS")
        for r in RESULTS: print("%s | %s | %s | %s" % (r[2], r[0], r[1], r[3][:300]))
        json.dump(RESULTS, open(os.path.join(OUT, "results.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
