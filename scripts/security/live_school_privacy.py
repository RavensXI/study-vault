"""
Live check after switching on the school-content rules (24 Sep 2026).

Creates a TEMPORARY Unity class (under the Unity History teacher) and a TEMPORARY pupil with NO
school on their profile, who joins that class through the real /join page. Checks in a real browser:
  visitor:      free-tier lesson renders; the old ?sid= Unity link shows "not found"
  free pupil:   (safeguarding test pupil) free-tier lesson + dashboard, no failed reads
  Unity pupil:  Unity's Manchuria lesson renders; the same pupil cannot see Severn Vale content
then DELETES the temporary class, membership and pupil, whatever happened.

  python scripts/security/live_school_privacy.py
"""
import json
import os
import secrets
import sys
import urllib.request

from playwright.sync_api import sync_playwright

BASE = "https://www.studyvault.co.uk"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "..", "safeguarding", "fixtures.json"), encoding="utf-8"))
UNITY = "a5414d1c-8841-4bc5-8573-a9756752361b"
SID = "2601f7b2-3cbd-422c-a1f2-dd7210c731e8"
SKIP = "try{['sv-lesson-tour-v2','sv-reader-tour-v1','sv-cookie-consent','sv-dash-tour-v1'].forEach(k=>localStorage.setItem(k,'1'))}catch(e){}"
FREE = "/lesson/history-aqa/conflict-tension-inter-war/7"
UNITY_LESSON = "/lesson/history/conflict-tension/8"


def api(method, path, body=None):
    req = urllib.request.Request(U + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req) as r:
        t = r.read()
        return json.loads(t) if t else None


results = []


def check(name, ok, why=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  <- " + str(why)[:160]), flush=True)


def h1(pg):
    return pg.evaluate("(document.querySelector('h1')||{}).innerText||''")


def sign_in(pg, email, pw):
    pg.goto(BASE + "/lesson.html", wait_until="domcontentloaded"); pg.wait_for_timeout(1500)
    return pg.evaluate("""async ([e,pw]) => { const sb = window.supabase.createClient('https://baipckgywpnwapobwtsy.supabase.co','sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2');
                          const r = await sb.auth.signInWithPassword({email:e,password:pw}); return r.error ? r.error.message : 'ok'; }""", [email, pw])


email = f"rls-test-{secrets.token_hex(4)}@demo.studyvault.co.uk"
pw = "Rls-" + secrets.token_hex(8) + "!"
uid = None
class_id = None
CODE = "".join(secrets.choice("ABCDEFGHJKMNPQRSTVWXYZ23456789") for _ in range(6))
try:
    user = api("POST", "/auth/v1/admin/users", {"email": email, "password": pw, "email_confirm": True})
    uid = user["id"]
    prof = api("GET", f"/rest/v1/profiles?id=eq.{uid}&select=id")
    if prof:
        api("PATCH", f"/rest/v1/profiles?id=eq.{uid}", {"role": "student", "school_id": None, "full_name": "RLS test pupil"})
    else:
        api("POST", "/rest/v1/profiles", {"id": uid, "email": email, "role": "student", "school_id": None, "full_name": "RLS test pupil"})
    cls = api("POST", "/rest/v1/classes", {"name": "RLS test (deleted automatically)", "school_id": UNITY, "teacher_id": "6d763855-069b-448e-acf6-02de2342670b",
                                          "subject_id": SID, "join_code": CODE, "join_open": True})
    class_id = cls[0]["id"]
    print("temporary Unity class", CODE, "and pupil created:", email)

    with sync_playwright() as p:
        b = p.chromium.launch()
        # visitor
        ctx = b.new_context(); ctx.add_init_script(SKIP); pg = ctx.new_page()
        pg.goto(BASE + FREE, wait_until="domcontentloaded"); pg.wait_for_timeout(7000)
        check("visitor: free-tier Manchuria lesson renders", "Manchuria" in h1(pg), h1(pg))
        pg.goto(BASE + UNITY_LESSON.replace("/8", "/7") + "?sid=" + SID, wait_until="domcontentloaded"); pg.wait_for_timeout(7000)
        t = pg.evaluate("document.body.innerText")
        check("visitor: the old ?sid= Unity link no longer shows Unity content", "Locarno" not in h1(pg) and "not found" in t.lower(), h1(pg) or t[:100])
        ctx.close()
        # free-tier pupil
        ctx = b.new_context(); ctx.add_init_script(SKIP); pg = ctx.new_page(); bad = []
        pg.on("response", lambda r: bad.append((r.status, r.url[-60:])) if "/rest/v1/" in r.url and r.status >= 400 else None)
        check("free pupil: signs in", sign_in(pg, FX["pupil"]["email"], FX["pupil"]["password"]) == "ok")
        pg.goto(BASE + FREE, wait_until="domcontentloaded"); pg.wait_for_timeout(7000)
        check("free pupil: free-tier lesson renders", "Manchuria" in h1(pg), h1(pg))
        pg.goto(BASE + "/classic", wait_until="domcontentloaded"); pg.wait_for_timeout(9000)
        check("free pupil: dashboard has no failed database reads", not bad, bad[:3])
        ctx.close()
        # Unity pupil
        ctx = b.new_context(); ctx.add_init_script(SKIP); pg = ctx.new_page()
        check("Unity pupil: signs in", sign_in(pg, email, pw) == "ok")
        pg.goto(BASE + "/join?code=" + CODE, wait_until="domcontentloaded"); pg.wait_for_timeout(2500)
        pg.evaluate("() => { const f = document.getElementById('joinForm'); f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', {cancelable: true})); }")
        pg.wait_for_timeout(6000)
        joined = api("GET", f"/rest/v1/class_members?class_id=eq.{class_id}&student_id=eq.{uid}&select=student_id")
        check("Unity pupil: joins the class through /join", bool(joined), pg.evaluate("document.body.innerText")[:120])
        pg.goto(BASE + UNITY_LESSON, wait_until="domcontentloaded"); pg.wait_for_timeout(8000)
        check("Unity pupil: Unity's Manchuria lesson renders", "Manchurian" in h1(pg), h1(pg) or pg.evaluate("document.body.innerText")[:120])
        n = pg.evaluate("""async () => { const r = await fetch('https://baipckgywpnwapobwtsy.supabase.co/rest/v1/subjects?select=slug&school_id=eq.2c9bf70b-6123-4e95-b285-4603acc2961f',
                             {headers:{apikey:'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'}}); return (await r.json()).length; }""")
        check("Unity pupil: cannot read Severn Vale's subjects", n == 0, n)
        ctx.close()
        b.close()
finally:
    if class_id:
        api("DELETE", f"/rest/v1/class_members?class_id=eq.{class_id}")
        api("DELETE", f"/rest/v1/classes?id=eq.{class_id}")
        print("temporary class deleted")
    if uid:
        try:
            api("DELETE", f"/rest/v1/profiles?id=eq.{uid}")
        except Exception as e:
            print("profile delete:", e)
        api("DELETE", f"/auth/v1/admin/users/{uid}")
        print("temporary Unity test pupil deleted")

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
