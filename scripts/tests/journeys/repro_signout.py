import asyncio, json, sys
sys.argv=["x"]
import run_journeys as J
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        C = J.make_user(9)
        pg = await (await b.new_context()).new_page()
        await J.inject(pg, J.session(C), {"sv-welcome": J.SEED_WELCOME, "sv-lessons-done": J.SEED_DONE})
        await pg.goto(J.SITE + "/classic"); await pg.wait_for_timeout(12000)
        print("1 server after first sign-in:", (J.server_welcome(C["id"]) or {}).get("picked"), (J.server_welcome(C["id"]) or {}).get("boards"))
        await pg.evaluate("()=>svSignOut()"); await pg.wait_for_timeout(1500)
        print("2 right after wipe (url %s): sv-welcome=%s" % (pg.url, await pg.evaluate("()=>localStorage.getItem('sv-welcome')")))
        await pg.wait_for_timeout(6000)
        st = await pg.evaluate("()=>({w:localStorage.getItem('sv-welcome'), meta:JSON.parse(localStorage.getItem('sv-sync-meta')||'{}')['sv-welcome'], owner:localStorage.getItem('sv-sync-owner'), url:location.href})")
        print("3 on /welcome after load, no clicks:", json.dumps(st)[:400])
        print("  server now:", (J.server_welcome(C["id"]) or {}).get("picked"))
        r = J.rest("user_state?select=updated_at&user_id=eq.%s&key=eq.sv-welcome" % C["id"]); print("  server updated_at:", r[0]["updated_at"] if r else None)
        await J.inject(pg, J.session(C))
        await pg.goto(J.SITE + "/classic"); await pg.wait_for_timeout(12000)
        loc = await pg.evaluate("()=>JSON.parse(localStorage.getItem('sv-welcome')||'null')")
        print("4 after signing back in: local picked=%s boards=%s" % (loc and loc.get("picked"), loc and loc.get("boards")))
        sw = J.server_welcome(C["id"]) or {}; print("  server picked=%s boards=%s" % (sw.get("picked"), sw.get("boards")))
        await b.close()
try:
    asyncio.run(main())
finally:
    J.cleanup()
