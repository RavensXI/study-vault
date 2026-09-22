"""Walk practice lessons in a headless browser and judge each problem AS A STUDENT SEES IT.

The other gates read JSON. This one looks at pixels. Tom, 21 Sep 2026: "we've done various
gates and walks and we're still running into errors every time we look at it... I think we
could do with just having a headless version of you go through and check some of these
lessons, look at them as a student would look at them."

Every structural check we own passed clean on questions that rendered nothing, on a colour key
that contradicted itself, and on items that printed as [object Object]. None of those are
visible to a JSON validator; all three are obvious in a screenshot.

  python scripts/_qa_visual_walk.py shoot --subject english-language-2-edexcel [--limit 8]
  python scripts/_qa_visual_walk.py shoot --live-sample 40        # across every practice subject
  python scripts/_qa_visual_walk.py judge                         # submits the batch
  python scripts/_qa_visual_walk.py collect                       # writes the report

Shots land in _visualqa/shots/, findings in _visualqa/report.md. Judging runs on the Batch API.
"""
import base64, io, json, os, random, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_visualqa")
SHOTS = os.path.join(OUT, "shots")
STATE = os.path.join(OUT, "_state.json")
os.makedirs(SHOTS, exist_ok=True)
# Sonnet for the LOOKING, not the writing. This judges whether a question renders and makes
# sense on screen - a visual anomaly check, not content a student reads - and the run is
# thousands of images, so the cheaper vision model is the right call here.
MODEL = "claude-sonnet-5"
SHOT_WIDTH = 1100          # downscaled before sending: fewer tokens, still legible
BASE = os.environ.get("SV_QA_BASE", "https://www.studyvault.co.uk")

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def state():
    return json.load(io.open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
def save(s):
    io.open(STATE, "w", encoding="utf-8").write(json.dumps(s, indent=1))

RUBRIC = """You are looking at ONE practice question on a GCSE revision site, exactly as a 15-year-old
student sees it. Judge only what is visible in the image.

Answer honestly. A working question is the normal case; do not invent faults.

Report a problem ONLY if one of these is true:
- BLANK: the question is asked but there is nothing to answer with — no options, no boxes, no
  clickable text, no input.
- RAW: machine text has leaked into view — [object Object], undefined, null, NaN, JSON braces,
  a template placeholder, an unrendered HTML tag.
- MISMATCH: the answer controls plainly do not fit the question (a rewrite box under a
  multiple-choice stem, a colour key whose labels contradict the colours shown, two questions
  stacked in one card).
- UNANSWERABLE: it refers to something a student cannot see — a chart, an image, a line number,
  a source that is not on screen.
- BROKEN LAYOUT: text overlaps, is cut off mid-word, or spills outside its box so it cannot be read.
- NONSENSE: the question or its options are incoherent, contradictory, or obviously not GCSE English.

How this site works, so that working questions are not reported (the first walk, 22 Sep 2026,
flagged each of these and every one was a working question):
- Words in a passage or sentence under a "Click..." or "Click or drag to highlight" hint ARE the
  controls. They are clickable even when they are not styled as buttons. That is not BLANK.
- A matching task may list more quotes than claims on purpose: the spare quotes are distractors.
- The extract in the left-hand panel belongs to the question on the right. A question about "the
  extract" or "the passage" refers to it.
- A dropdown reading "Choose…" is an answer control.

Reply with JSON only:
{"ok": true}
or
{"ok": false, "fault": "BLANK|RAW|MISMATCH|UNANSWERABLE|BROKEN_LAYOUT|NONSENSE",
 "what_a_student_sees": "one sentence, concrete", "confidence": 0.0-1.0}"""

def lessons_for(args):
    sub = args[args.index("--subject") + 1] if "--subject" in args else None
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 0
    sample = int(args[args.index("--live-sample") + 1]) if "--live-sample" in args else 0
    q = ("lessons?select=title,lesson_number,status,units!inner(slug,subjects!inner(slug,settings))"
         "&practice_data=not.is.null&order=id&limit=3000")
    if sub: q += "&units.subjects.slug=eq." + sub
    else: q += "&status=eq.live"
    rows = get(q)
    rows = [{"subject": r["units"]["subjects"]["slug"], "unit": r["units"]["slug"],
             "n": r["lesson_number"], "title": r["title"]} for r in rows]
    if sample:
        by = {}
        for r in rows: by.setdefault(r["subject"], []).append(r)
        random.seed(); picked = []
        subs = list(by)
        while len(picked) < sample and subs:
            for s in list(subs):
                if not by[s]: subs.remove(s); continue
                picked.append(by[s].pop(random.randrange(len(by[s]))))
                if len(picked) >= sample: break
        rows = picked
    if limit: rows = rows[:limit]
    return rows

def cmd_shoot(args):
    from playwright.sync_api import sync_playwright
    rows = lessons_for(args)
    print("walking %d lessons against %s" % (len(rows), BASE), flush=True)
    shots = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        ctx.add_init_script("try{localStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
                            "sessionStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
                            "['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done']"
                            ".forEach(function(k){localStorage.setItem(k,'1')});}catch(e){}")
        pg = ctx.new_page()
        for L in rows:
            url = "%s/practice/%s/%s/%d" % (BASE, L["subject"], L["unit"], L["n"])
            try: pg.goto(url, wait_until="commit", timeout=30000)
            except Exception: pass
            time.sleep(6)
            try:
                pg.evaluate("() => document.querySelectorAll('[class*=tour],[class*=coach]').forEach(e=>e.remove())")
                # "Start Practice" opens the worked examples first; take the jump-ahead when
                # it is offered so the walk sees the problem bank, which is what a student answers
                pg.evaluate("() => { const b=[...document.querySelectorAll('button')].find(x=>/Start Practice/i.test(x.textContent)); if(b)b.click(); }")
                time.sleep(2.0)
                for _ in range(3):
                    jumped = pg.evaluate("() => { const b=[...document.querySelectorAll('button,a')].find(x=>/Jump ahead to Practice|Skip to practice|Go to practice/i.test(x.textContent||'')); if(!b) return false; b.click(); return true; }")
                    if not jumped: break
                    time.sleep(1.5)
                time.sleep(1.0)
                pg.evaluate("""() => document.querySelectorAll('[class*=modal],[class*=overlay],[class*=tour]').forEach(e=>{
                    const cs=getComputedStyle(e); if(cs.position==='fixed'&&e.offsetHeight>200) e.remove(); })""")
            except Exception: pass
            seen_text = set()
            for i in range(24):
                card = pg.query_selector(".problem-card")
                if not card: break
                # the deck stops advancing at its last problem; the Next button stays put,
                # so recognise a repeat rather than shooting the same card four more times
                try: sig = (card.inner_text() or "")[:160]
                except Exception: sig = str(i)
                if sig in seen_text: break
                seen_text.add(sig)
                if re.match(r"\s*Example \d+ of", sig):      # still in the worked examples
                    try:
                        if not pg.evaluate("() => { const b=[...document.querySelectorAll('button,a')].find(x=>/Jump ahead to Practice/i.test(x.textContent||'')); if(!b) return false; b.click(); return true; }"): break
                    except Exception: break
                    time.sleep(1.5); seen_text.discard(sig); continue
                key = "%s__%s__%d__q%02d" % (L["subject"], L["unit"], L["n"], i + 1)
                path = os.path.join(SHOTS, key + ".png")
                try:
                    # the VIEWPORT, not the card: the question often depends on the extract in
                    # the left panel, and a student judges the two together
                    pg.screenshot(path=path)
                    shots.append({"key": key, "url": url, "q": i + 1, "title": L["title"],
                                  "subject": L["subject"], "unit": L["unit"], "n": L["n"]})
                except Exception: pass
                try:
                    nxt = pg.evaluate("() => { const n=[...document.querySelectorAll('button')].find(x=>/Next Problem/i.test(x.textContent)); if(!n) return false; n.click(); return true; }")
                except Exception: nxt = False
                if not nxt: break
                time.sleep(1.0)
            print("  %-56s %d shots" % (url.replace(BASE, ""), sum(1 for s in shots if s["key"].startswith(L["subject"] + "__" + L["unit"] + "__" + str(L["n"]) + "__"))), flush=True)
        br.close()
    st = state(); st["shots"] = shots; save(st)
    print("captured %d problem screenshots" % len(shots))

SIG_JS = """() => Object.fromEntries(['bronze','silver','gold'].map(t => [t,
  (window._problemBank[t] || []).map(q => (q.input_type || '') + '|' + (q.question || '') + '|' +
     JSON.stringify(q.statements || q.chips || q.tokens || q.options || q.summaryParts || q.claims || q.original || '').slice(0, 120))]))"""
DISMISS_JS = """() => {
  document.querySelectorAll('[class*=tour],[class*=coach]').forEach(e => e.remove());
  [...document.querySelectorAll('button,a')].filter(b => /Got it|Jump ahead to Practice|let.s practi/i.test(b.textContent || ''))
    .forEach(b => { try { b.click(); } catch (e) {} });
  document.querySelectorAll('[class*=modal],[class*=overlay]').forEach(e => { const cs = getComputedStyle(e);
    if (cs.position === 'fixed' && e.offsetHeight > 200 && !e.contains(document.getElementById('current-problem-card'))) e.remove(); });
}"""


def signature(q):
    """The same fingerprint SIG_JS takes in the page, from the stored problem."""
    body = q.get("statements") or q.get("chips") or q.get("tokens") or q.get("options") or q.get("summaryParts") or q.get("claims") or q.get("original") or ""
    return (q.get("input_type") or "") + "|" + (q.get("question") or "") + "|" + json.dumps(body, ensure_ascii=False, separators=(",", ":"))[:120]


def cmd_shoot_direct(args):
    """Render every STORED problem directly, one screen each, keyed by its stored position.

    The first walk clicked Next Problem like a student, which meant tier resets repeated
    some screens, skipped others, and numbered the rest by display order, so a flag could
    not be traced to its problem without guessing. This sets the page's own state and calls
    its own renderCurrentProblem(), so each shot is exactly one stored problem."""
    from playwright.sync_api import sync_playwright
    rows = lessons_for(args)
    tall = 1500 if "--short" not in args else 1000
    print("rendering every problem of %d lessons against %s" % (len(rows), BASE), flush=True)
    shots = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": tall}, device_scale_factor=1)
        ctx.add_init_script("try{localStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
                            "sessionStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
                            "['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done']"
                            ".forEach(function(k){localStorage.setItem(k,'1')});}catch(e){}")
        pg = ctx.new_page()
        for L in rows:
            lesson = get("lessons?select=practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                         "&units.slug=eq.%s&lesson_number=eq.%d" % (L["subject"], L["unit"], L["n"]))
            if not lesson:
                continue
            bank = (lesson[0]["practice_data"] or {}).get("problem_bank") or {}
            url = "%s/practice/%s/%s/%d?prob=bronze:0" % (BASE, L["subject"], L["unit"], L["n"])
            try: pg.goto(url, wait_until="commit", timeout=30000)
            except Exception: pass
            time.sleep(6)
            try: pg.evaluate(DISMISS_JS)
            except Exception: pass
            try: shown = pg.evaluate(SIG_JS)
            except Exception: print("  no problem bank on", url); continue
            n = 0
            for tier in ("bronze", "silver", "gold"):
                used = set()
                for i, q in enumerate(bank.get(tier) or []):
                    sig = signature(q)
                    d = next((k for k, s in enumerate(shown.get(tier, [])) if k not in used and s == sig), None)
                    if d is None:
                        # a Foundation filter or a shape the fingerprint misses — say so, never guess
                        print("    %s[%d] not found in the rendered bank" % (tier, i)); continue
                    used.add(d)
                    try:
                        pg.evaluate("([t, d]) => { practiceState.currentTier = t; practiceState.currentIndex = d; practiceState.answered = false; renderCurrentProblem(); }", [tier, d])
                        time.sleep(0.9)
                        pg.evaluate(DISMISS_JS)
                        time.sleep(0.2)
                    except Exception as e:
                        print("    %s[%d] did not render: %s" % (tier, i, str(e)[:80])); continue
                    key = "%s__%s__%d__%s%02d" % (L["subject"], L["unit"], L["n"], tier, i)
                    path = os.path.join(SHOTS, key + ".png")
                    try:
                        pg.screenshot(path=path)
                        shots.append({"key": key, "url": url.split("?")[0], "q": "%s[%d]" % (tier, i), "tier": tier, "i": i,
                                      "title": L["title"], "subject": L["subject"], "unit": L["unit"], "n": L["n"],
                                      "type": q.get("input_type"), "stem": (q.get("question") or "")[:200]})
                        n += 1
                    except Exception:
                        pass
            print("  %-60s %d problems" % (url.replace(BASE, "").split("?")[0], n), flush=True)
        br.close()
    st = {"shots": shots, "mode": "direct"}
    save(st)
    print("captured %d problem screenshots" % len(shots))


def shrink(path):
    """Downscale to SHOT_WIDTH so a 1,400-image run stays affordable."""
    try:
        from PIL import Image
        im = Image.open(path)
        if im.width > SHOT_WIDTH:
            im = im.resize((SHOT_WIDTH, int(im.height * SHOT_WIDTH / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.convert("RGB").save(buf, "PNG", optimize=True)
        return buf.getvalue()
    except Exception:
        return io.open(path, "rb").read()

def cmd_judge():
    import anthropic
    cl = anthropic.Anthropic()
    st = state(); shots = st["shots"]
    reqs = []
    for s in shots:
        path = os.path.join(SHOTS, s["key"] + ".png")
        if not os.path.exists(path): continue
        b64 = base64.standard_b64encode(shrink(path)).decode()
        reqs.append({"custom_id": s["key"][:60] + "__" + str(abs(hash(s["key"])) % 9999),
                     "params": {"model": MODEL, "max_tokens": 300, "thinking": {"type": "disabled"},
                                "system": RUBRIC,
                                "messages": [{"role": "user", "content": [
                                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
                                    {"type": "text", "text": "Judge this question as the student sees it."}]}]}})
    st["ids"] = {r["custom_id"]: s["key"] for r, s in zip(reqs, shots)}
    batches = []
    for k in range(0, len(reqs), 200):
        b = cl.messages.batches.create(requests=reqs[k:k + 200])
        batches.append(b.id); print("submitted", b.id, len(reqs[k:k + 200]), flush=True)
    st["batches"] = batches; save(st)

def cmd_collect():
    import anthropic
    cl = anthropic.Anthropic()
    st = state(); by = {s["key"]: s for s in st["shots"]}; ids = st["ids"]
    pend = 0; findings = []; judged = 0; usage = {"in": 0, "out": 0}
    for bid in st["batches"]:
        b = cl.messages.batches.retrieve(bid)
        if b.processing_status != "ended": pend += 1; print(bid, b.processing_status); continue
        for r in cl.messages.batches.results(bid):
            if r.result.type != "succeeded": continue
            m = r.result.message; usage["in"] += m.usage.input_tokens; usage["out"] += m.usage.output_tokens
            txt = "".join(x.text for x in m.content if x.type == "text")
            mm = re.search(r"\{.*\}", txt, re.S)
            if not mm: continue
            try: d = json.loads(mm.group(0))
            except Exception: continue
            judged += 1
            if d.get("ok") is False and (d.get("confidence") or 1) >= 0.6:
                s = by.get(ids.get(r.custom_id), {})
                findings.append(dict(d, **{k: s.get(k) for k in ("url", "q", "title", "subject")}))
    if pend: print("still running:", pend, "batch(es)"); return
    findings.sort(key=lambda f: (f.get("subject") or "", f.get("url") or "", f.get("q") or 0))
    lines = ["# Visual walk — what a student actually sees", "",
             "%d problems looked at, %d flagged." % (judged, len(findings)), ""]
    for f in findings:
        lines += ["- **%s** — %s  " % (f.get("fault"), f.get("what_a_student_sees")),
                  "  %s (question %s, %s)" % (f.get("url"), f.get("q"), f.get("title"))]
    io.open(os.path.join(OUT, "report.md"), "w", encoding="utf-8").write("\n".join(lines))
    cost = usage["in"] / 1e6 * 1.5 + usage["out"] / 1e6 * 7.5
    print("judged %d problems, %d flagged | indicative batch cost $%.2f" % (judged, len(findings), cost))
    print("report:", os.path.join(OUT, "report.md"))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == "shoot" and "--direct" in a: cmd_shoot_direct(a)
    elif a[0] == "shoot": cmd_shoot(a)
    elif a[0] == "judge": cmd_judge()
    elif a[0] == "collect": cmd_collect()
    else: print(__doc__)
