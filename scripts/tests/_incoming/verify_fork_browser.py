# -*- coding: utf-8 -*-
"""Prove copy-on-edit where it counts: on the rendered page.

Same URL, twice. Once as a Fork Test School student, once as a free user.
The school must see its own knowledge check; the public must see the original.
"""
import sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8907/lesson/business-aqa/marketing/1"
OUT = r"C:\Users\tshau\.claude\jobs\4059242c\tmp"
SCHOOL = "99bd48fd-f9c6-4ea4-b4a0-2d0b5c808614"

SESSION = ('sessionStorage.setItem("studyvault-school", JSON.stringify({'
           'school_id:"%s", school_name:"Fork Test School",'
           'bespoke_subjects:[], subscribed_subjects:["business-aqa"]}));' % SCHOOL)


def look(pw, as_school):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    if as_school:
        ctx.add_init_script(SESSION)
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    time.sleep(2.5)
    kc = pg.evaluate("() => (window.knowledgeCheck||[]).map(q => q.q)")
    ovr = pg.evaluate("() => window.__svOverride || null")
    title = pg.evaluate("() => (document.querySelector('h1')||{}).textContent")
    # open the modal so we see what a student actually sees. The onboarding
    # tour and the "Recently added" panel float over the sidebar button, so
    # clear them first rather than fighting them.
    pg.evaluate("""() => {
        document.querySelectorAll('.sv-tour, .sv-tour-pop, [class*="tour"], [class*="recently"], .sv-newsflash')
          .forEach(e => e.remove());
    }""")
    time.sleep(0.4)
    shot = None
    try:
        pg.locator("#knowledge-check-btn").click(timeout=8000, force=True)
        time.sleep(1.2)
        shot = OUT + (r"\fork_school.png" if as_school else r"\fork_public.png")
        pg.screenshot(path=shot)
        q = pg.inner_text(".kc-question")
    except Exception as e:
        q = "(modal not opened: %s)" % str(e)[:60]
    b.close()
    return {"title": (title or "").strip()[:50], "kcs": kc, "first_rendered": q,
            "override": ovr, "shot": shot}


with sync_playwright() as pw:
    school = look(pw, True)
    public = look(pw, False)

print("AS FORK TEST SCHOOL")
print("   lesson:", school["title"])
print("   KC[0] in data:", (school["kcs"] or ["(none)"])[0][:80])
print("   KC[0] rendered:", school["first_rendered"][:80])
print()
print("AS FREE USER")
print("   lesson:", public["title"])
print("   KC[0] in data:", (public["kcs"] or ["(none)"])[0][:80])
print("   KC[0] rendered:", public["first_rendered"][:80])
print()
ok_school = "FORK TEST" in (school["kcs"] or [""])[0]
ok_public = "FORK TEST" not in (public["kcs"] or [""])[0]
print("school sees its own version :", "PASS" if ok_school else "FAIL")
print("public sees the original    :", "PASS" if ok_public else "FAIL")
print("screenshots:", school["shot"], public["shot"])
