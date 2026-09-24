"""
Browser check for the school-content privacy change (24 Sep 2026): the pages still work for each
kind of user, and admin content reads go through /api/staff/rest.

  python scripts/security/browser_content_reads.py [BASE]      default http://127.0.0.1:8911

Needs the local server scratchpad/dev_server_rls.js (admin password 'local-admin-test'), or a
BASE of the live site with RLS_ADMIN_PW set. Uses the safeguarding test pupil (fixtures.json).
Prints one line per check: PASS or FAIL with the reason.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8911"
ADMIN_PW = os.environ.get("RLS_ADMIN_PW", "local-admin-test")
HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "..", "safeguarding", "fixtures.json"), encoding="utf-8"))
SKIP_TOURS = "try{['sv-lesson-tour-v2','sv-reader-tour-v1','sv-cookie-consent','sv-dash-tour-v1'].forEach(k=>localStorage.setItem(k,'1'))}catch(e){}"
FREE_LESSON = "/lesson/history-aqa/conflict-tension-inter-war/7"
results = []


def check(name, ok, why=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  <- " + why), flush=True)


def page_text(pg):
    return pg.evaluate("document.body.innerText")


with sync_playwright() as p:
    b = p.chromium.launch()

    # 1. signed-out visitor: free lesson renders
    ctx = b.new_context(); ctx.add_init_script(SKIP_TOURS); pg = ctx.new_page()
    pg.goto(BASE + FREE_LESSON, wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    h1 = pg.evaluate("(document.querySelector('h1')||{}).innerText||''")
    check("visitor: free-tier lesson renders", "Manchuria" in h1, h1[:80])
    ctx.close()

    # 2. admin session: review page lists lessons, and content reads go through the server
    ctx = b.new_context(); ctx.add_init_script(SKIP_TOURS + "sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'admin',pw:'%s'}))" % ADMIN_PW)
    pg = ctx.new_page(); proxied = []; direct = []
    pg.on("request", lambda r: proxied.append(r.url) if "/api/staff/rest" in r.url else (direct.append(r.url) if "/rest/v1/lessons" in r.url else None))
    pg.goto(BASE + "/admin/build-status", wait_until="domcontentloaded"); pg.wait_for_timeout(8000)
    check("admin: build-status reads content through /api/staff/rest", len(proxied) > 0 and not direct, f"proxied={len(proxied)} direct={len(direct)}")
    check("admin: build-status page renders", len(page_text(pg)) > 500 and "error" not in page_text(pg).lower()[:300])
    # an unpublished free-tier lesson (staff only) and a Unity lesson (school only) both open for an admin
    pg.goto(BASE + "/practice/english-language-2-edexcel/paper-1-reading/4", wait_until="domcontentloaded"); pg.wait_for_timeout(8000)
    check("admin: previews an unpublished lesson", "Structure and Organisation" in page_text(pg), page_text(pg)[:120])
    pg.goto(BASE + "/lesson/history/conflict-tension/8", wait_until="domcontentloaded"); pg.wait_for_timeout(8000)
    h1 = pg.evaluate("(document.querySelector('h1')||{}).innerText||''")
    check("admin: previews a Unity lesson", "Manchurian" in h1, h1[:80])
    ctx.close()

    # 3. signed-in free-tier pupil: dashboard + lesson still load, dashboard reads carry the sign-in
    ctx = b.new_context(); ctx.add_init_script(SKIP_TOURS); pg = ctx.new_page()
    pg.goto(BASE + "/lesson.html", wait_until="domcontentloaded"); pg.wait_for_timeout(1500)
    ok = pg.evaluate("""async ([e,pw]) => { const sb = window.supabase.createClient('https://baipckgywpnwapobwtsy.supabase.co','sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2');
                        const r = await sb.auth.signInWithPassword({email:e,password:pw}); return !r.error; }""", [FX["pupil"]["email"], FX["pupil"]["password"]])
    check("pupil: signs in", ok)
    signed = []; statuses = []
    pg.on("request", lambda r: signed.append(bool(r.headers.get("authorization"))) if "/rest/v1/lessons" in r.url else None)
    pg.on("response", lambda r: statuses.append(r.status) if "/rest/v1/" in r.url else None)
    pg.goto(BASE + FREE_LESSON, wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    h1 = pg.evaluate("(document.querySelector('h1')||{}).innerText||''")
    check("pupil: free-tier lesson renders", "Manchuria" in h1, h1[:80])
    pg.goto(BASE + "/classic", wait_until="domcontentloaded"); pg.wait_for_timeout(9000)
    check("pupil: dashboard content reads carry the sign-in", signed and all(signed), f"{sum(signed)}/{len(signed)} signed")
    check("pupil: no failed database reads", statuses and all(s < 400 for s in statuses), str(sorted(set(statuses))))
    ctx.close()
    b.close()

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
