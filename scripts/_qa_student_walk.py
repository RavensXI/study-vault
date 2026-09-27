"""The student walk: a model answers every practice question blind, the site marks it,
and every disagreement is adjudicated.

Tom, 22 Sep 2026: "I want the model to think like a student, to not have the answer
given to it. It just thinks like they would and then puts the answer that they think is
right. If it's right then that's fine and if it's marked wrong then we need to establish
why."

The visual walk (scripts/_qa_visual_walk.py) photographs questions. This one does them.

  extract     render every stored problem in a real browser and record, as text, exactly
              what a student sees: the card, the extract panel, the answer controls.
              Nothing from the answer key goes into a view.
  attempt     submit the views to the Batch API. Sonnet 5 answers as a careful Year 11
              student, with no key, no explanations, no mark scheme.
  collect     fetch the attempts.
  mark        re-render each problem, put the student's answer into the page through the
              page's own controls, press Check Answer, and read back what the site said.
              Written answers go to the real AI marker in London (the local server has no
              marker), paced under its per-address hourly limits.
  adjudicate  every problem the site marked wrong, and every AI-marked answer, goes to
              Opus 5 WITH the key, the attempt and the site's verdict, to rule: student
              wrong, key wrong, ambiguous, unanswerable, marker too harsh or too lenient.
  report      _studentwalk/report.md

  SV_QA_BASE=http://127.0.0.1:8910 python scripts/_qa_student_walk.py extract --subject english-language-2-edexcel
  python scripts/_qa_student_walk.py attempt
  python scripts/_qa_student_walk.py collect
  SV_QA_BASE=http://127.0.0.1:8910 python scripts/_qa_student_walk.py mark
  python scripts/_qa_student_walk.py adjudicate      (then collect-adjudication)
  python scripts/_qa_student_walk.py report

A re-walk of chosen questions only: SV_WALK_DIR=scripts/_studentwalk_rewalk and
  extract --keys FILE   (a JSON list of walk keys, e.g. the findings from the last walk)
"""
import io, json, os, re, sys, time, urllib.request
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.environ.get("SV_WALK_DIR") or os.path.join(HERE, "_studentwalk"))
os.makedirs(OUT, exist_ok=True)
F = {k: os.path.join(OUT, k + ".json") for k in ("views", "attempts", "marks", "adjudications", "state")}
BASE = os.environ.get("SV_QA_BASE", "http://127.0.0.1:8910")
PROD = "https://www.studyvault.co.uk"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
STUDENT_MODEL = "claude-sonnet-5"     # Tom's standing preference for checking work
JUDGE_MODEL = "claude-opus-5"
AI_TYPES = ("ai_mark", "ai_write", "improve_sentence",
            # not walked (25 Sep 2026): translate and role_play are AI-marked; dictation needs audio
            "translate", "role_play", "dictation")
# One subject row per walk: several slugs exist twice (a school copy and the free tier), so a walk of
# either sets SV_WALK_SID and every lesson read and page URL is pinned to that subject row.
SID = os.environ.get("SV_WALK_SID") or ""
SHOTS = os.path.join(OUT, "shots")

sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location("vw", os.path.join(HERE, "_qa_visual_walk.py"))
vw = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vw)


def load(name, default=None):
    return json.load(io.open(F[name], encoding="utf-8")) if os.path.exists(F[name]) else default


def save(name, obj):
    io.open(F[name], "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False, indent=1))


def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())


SIG_JS = """() => Object.fromEntries(['bronze','silver','gold'].map(t => [t,
  (window._problemBank[t] || []).map(q => (q.input_type || '') + '|' + (q.question || '') + '|' + (q.display || '') + '|' +
     JSON.stringify(q.statements || q.chips || q.tokens || q.options || q.summaryParts || q.claims || q.original ||
                    q.pairs || q.gaps || q.correct_order || q.sentence || q.solutions || '').slice(0, 160))]))"""


def signature(q):
    body = (q.get("statements") or q.get("chips") or q.get("tokens") or q.get("options") or q.get("summaryParts") or
            q.get("claims") or q.get("original") or q.get("pairs") or q.get("gaps") or q.get("correct_order") or
            q.get("sentence") or q.get("solutions") or "")
    return ((q.get("input_type") or "") + "|" + (q.get("question") or "") + "|" + (q.get("display") or "") + "|" +
            json.dumps(body, ensure_ascii=False, separators=(",", ":"))[:160])


def settle(pg):
    """Let the card finish its transition and every image and chart finish loading before a screenshot."""
    time.sleep(1.2)
    for _ in range(20):
        if pg.evaluate("""() => [...document.querySelectorAll('#current-problem-card img, #practice-passage-area img')]
                          .every(i => i.complete && i.naturalWidth > 0)"""): break
        time.sleep(0.5)
    time.sleep(0.6)


def lesson_q(sub, unit, n, select="practice_data"):
    q = ("lessons?select=id,%s,units!inner(slug,subject_id,subjects!inner(slug))&units.subjects.slug=eq.%s"
         "&units.slug=eq.%s&lesson_number=eq.%s" % (select, sub, unit, n))
    return q + ("&units.subject_id=eq." + SID if SID else "")


def page_url(sub, unit, n):
    return "%s/practice/%s/%s/%s?prob=bronze:0%s" % (BASE, sub, unit, n, ("&sid=" + SID) if SID else "")


def walk_lessons(args):
    if not SID: return vw.lessons_for(args)
    rows = get("lessons?select=title,lesson_number,units!inner(slug,subject_id,subjects!inner(slug))"
               "&practice_data=not.is.null&units.subject_id=eq.%s&order=id&limit=3000" % SID)
    rows = [{"subject": r["units"]["subjects"]["slug"], "unit": r["units"]["slug"], "n": r["lesson_number"], "title": r["title"]} for r in rows]
    if "--lesson" in args:   # canary: one lesson, given as unit/number
        want = args[args.index("--lesson") + 1]
        rows = [r for r in rows if "%s/%s" % (r["unit"], r["n"]) == want]
    if "--limit" in args: rows = rows[:int(args[args.index("--limit") + 1])]
    return rows


INIT = ("try{localStorage.setItem('studyvault-auth',JSON.stringify({role:'admin',pw:'local-walk'}));"
        "sessionStorage.setItem('studyvault-auth',JSON.stringify({role:'admin',pw:'local-walk'}));"
        "['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done']"
        ".forEach(function(k){localStorage.setItem(k,'1')});}catch(e){}"
        "window.alert=function(){};window.confirm=function(){return true;};")

RENDER_JS = """([t, d]) => { practiceState.currentTier = t; practiceState.currentIndex = d; practiceState.answered = false;
  document.getElementById('current-problem-card').classList.remove('card-correct', 'card-incorrect');
  renderCurrentProblem(); }"""

# What a student sees, as text. Controls are listed with the site's own indices so the
# answer can be put back through the same controls; nothing here comes from the key.
VIEW_JS = r"""() => {
  const card = document.getElementById('current-problem-card');
  const p = window._problemBank[practiceState.currentTier][practiceState.currentIndex];
  const t = p.input_type || 'single_value';
  // KaTeX draws each formula twice (MathML for readers, HTML for eyes), so innerText doubles it.
  // For the view each formula is swapped for its TeX source, then put back.
  const swaps = [];
  document.querySelectorAll('#current-problem-card .katex, #practice-passage-area .katex').forEach(k => {
    const a = k.querySelector('annotation[encoding="application/x-tex"]');
    if (!a) return;
    const s = document.createElement('span'); s.className = 'walk-tex'; s.textContent = ' \\(' + a.textContent.trim() + '\\) ';
    k.parentNode.insertBefore(s, k); k.style.display = 'none'; swaps.push([k, s]);
  });
  const txt = e => (e ? e.innerText : '').replace(/\s+\n/g, '\n').trim();
  const area = document.getElementById('practice-passage-area');
  const panelOn = area && getComputedStyle(area).display !== 'none';
  const v = { type: t, card: txt(card), panel: panelOn ? txt(document.getElementById('passage-text')) : '',
              panel_label: panelOn ? txt(document.querySelector('.passage-header-label')) : '' };
  if (t === 'multiple_choice') v.options = [...card.querySelectorAll('.mc-option .mc-text')].map(txt);
  if (t === 'traffic_light') { v.statements = [...card.querySelectorAll('.tl-stmt .stmt-text')].map(txt);
    v.categories = (window._engState.tlCats || []).map(c => c.charAt(0).toUpperCase() + c.slice(1)); }
  if (t === 'connotation_picker') v.chips = [...card.querySelectorAll('.cp-chip')].map(txt);
  if (t === 'evidence_match') { v.claims = [...card.querySelectorAll('.em-claim')].map(e => txt(e));
    v.quotes = [...card.querySelectorAll('.em-quote')].map(e => txt(e)); }
  if (t === 'misleading_summary') { v.summary = txt(card.querySelector('.ms-summary'));
    v.parts = [...card.querySelectorAll('.ms-span')].map(e => ({ n: +e.dataset.idx, text: txt(e) })); }
  if (t === 'highlight_evidence') v.highlight_text = txt(card.querySelector('#hl-passage-area'));
  if (t === 'spot_error') v.tokens = [...card.querySelectorAll('.spot-token')].map(e => ({ n: +e.dataset.idx, text: txt(e) }));
  if (t === 'reorder') v.items = [...card.querySelectorAll('.reorder-item')].map(e => txt(e));
  if (t === 'improve_sentence') v.original = txt(card.querySelector('.improve-original'));
  if (['ai_mark', 'ai_write', 'improve_sentence'].includes(t)) v.marks = p.marks || null;
  // numeric answer boxes, exactly as labelled on screen
  const ia = document.getElementById('problem-inputs-area');
  if (['single_value', 'two_solutions', 'xy_pair', 'fraction', 'standard_form'].includes(t)) {
    v.boxes = txt(ia); const u = ia && ia.querySelector('.problem-answer-unit'); v.answer_unit = u ? txt(u) : '';
  }
  if (t === 'vocab_match') { v.left = [...card.querySelectorAll('.vm-left')].map(txt); v.right = [...card.querySelectorAll('.vm-right')].map(txt); }
  if (t === 'gap_fill') {
    const sent = card.querySelector('.gf-sentence'); let s = '', g = 0;
    if (sent) sent.childNodes.forEach(n => { if (n.classList && (n.classList.contains('gf-gap') || n.classList.contains('gf-input'))) s += ' [GAP ' + (++g) + '] '; else s += n.textContent; });
    v.sentence = s.replace(/\s+/g, ' ').trim(); v.english = txt(card.querySelector('.gf-english'));
    v.bank = [...card.querySelectorAll('.gf-chip')].map(txt);
  }
  if (t === 'sentence_builder') { v.english = txt(card.querySelector('.sb-english')); v.tiles = [...card.querySelectorAll('.sb-tile')].map(txt); }
  if (t === 'spot_correct') v.sentence = txt(card.querySelector('.sc-sentence'));
  // what the helper link opens (bronze and silver only, like the page)
  if (p.equation_hint && practiceState.currentTier !== 'gold') {
    const d = document.createElement('div'); d.innerHTML = p.equation_hint; v.equation_hint = d.textContent.trim(); }
  if (p.chart) v.chart = JSON.stringify({ type: p.chart.type, labels: (p.chart.data || {}).labels,
    datasets: ((p.chart.data || {}).datasets || []).map(d => ({ label: d.label, data: d.data })) }).slice(0, 3000);
  const figs = [...card.querySelectorAll('img, canvas, svg')].concat(area && getComputedStyle(area).display !== 'none' ? [...area.querySelectorAll('img, canvas, svg')] : [])
    .filter(e => { const r = e.getBoundingClientRect(); return r.width > 60 && r.height > 40; });
  v.visual = !!(p.image || p.chart || figs.length);
  swaps.forEach(([k, s]) => { k.style.display = ''; s.remove(); });
  return v;
}"""

STUDENT = """You are a conscientious Year 11 student in England, revising for GCSE English Language on a
revision website. You are doing one practice question. You can see only what is on your screen:
the question card, any extract shown beside it, and the answer controls.

Answer the way a capable, careful student would: read the question and the extract properly,
think it through, then commit to the answer you believe is right. Nobody has told you the
answer. Do not assume the question is broken — do your best with it. If something genuinely
confuses you (wording that could mean two things, an option that could fit either way, a text
the question mentions that is not on your screen), say so in "unsure_because", in a student's
words. Only if it truly cannot be answered from what is on screen, explain in "cannot_answer".

Reply with ONE JSON object and nothing else:
{"answer": <see the answer format below>, "confidence": 0.0-1.0,
 "unsure_because": "", "cannot_answer": ""}"""

FORMATS = {
    "multiple_choice": 'the exact text of the ONE option you choose, copied from OPTIONS',
    "traffic_light": 'a list, one entry per statement: [{"statement": "<exact statement text>", "category": "<exact category name from CATEGORIES>"}]',
    "connotation_picker": 'a list of the exact chip texts you select (select every one that applies, and only those)',
    "evidence_match": 'a list, one entry per claim: [{"claim": "<exact claim text>", "quote": "<exact quote text>"}]. There may be spare quotes that fit no claim.',
    "misleading_summary": 'a list of the part NUMBERS you click as misleading (from PARTS), e.g. [2, 5]',
    "highlight_evidence": 'the exact words you would highlight, copied character for character from the passage in the card (one continuous stretch)',
    "spot_error": 'a list of the token NUMBERS you click as wrong (from TOKENS), e.g. [3, 7]',
    "reorder": 'the list of ITEMS in the order you put them, each copied exactly',
    "ai_mark": 'your written answer, as you would type it in the box. Write the length and depth the marks deserve.',
    "ai_write": 'your written answer, as you would type it in the box. Write the length and depth the marks deserve.',
    "improve_sentence": 'your improved version, as you would type it in the box',
    "single_value": 'the number you type in the box: digits only (a decimal point or minus sign if needed), no units, no working',
    "two_solutions": 'a list of the two numbers you type in the two boxes, e.g. [3, -2]',
    "xy_pair": '{"x": <number>, "y": <number>}',
    "fraction": '{"numerator": <whole number>, "denominator": <whole number>}',
    "standard_form": '{"a": <number>, "n": <whole number>} for a × 10^n',
    "vocab_match": 'a list with one entry per pair you match: [{"left": "<exact text from the left column>", "right": "<exact text from the right column>"}]',
    "gap_fill": 'a list of what goes in each gap, in order: [gap 1, gap 2, ...] (from the WORD BANK if there is one)',
    "sentence_builder": 'the list of tiles in the order you place them, each copied exactly; leave out tiles that do not belong',
    "spot_correct": '{"wrong_word": "<the one word in the sentence that is wrong, copied exactly>", "correction": "<what it should be>"}',
}

SUBJECT_NAMES = [("english-language", "English Language"), ("maths", "Maths"), ("statistics", "Statistics"),
                 ("separate-sciences", "Separate Sciences (Biology, Chemistry, Physics)"), ("science", "Combined Science"),
                 ("geography", "Geography"), ("music", "Music"), ("latin", "Latin"), ("spanish", "Spanish"),
                 ("french", "French"), ("german", "German")]


def subject_name(slug):
    return next((n for p, n in SUBJECT_NAMES if slug.startswith(p)), slug.replace("-", " ").title())


def student_prompt(slug):
    """The English Language prompt is kept word for word; other subjects get their own name and
    subject-specific habits."""
    if slug.startswith("english-language"): return STUDENT
    s = STUDENT.replace("GCSE English Language", "GCSE " + subject_name(slug))
    s = s.replace("read the question and the extract properly", "read the question (and any extract, table or chart) properly")
    extra = ["If a SCREENSHOT path is given, open it with the Read tool before answering: it shows exactly what is on",
             "your screen, including any map, chart, graph, diagram or score. Rely on it for anything visual."]
    if slug.startswith(("maths", "statistics", "science", "separate-sciences", "geography")):
        extra += ["Work it out in your head as you would on paper, then give only the final answer in the format asked.",
                  "Round only as the question tells you; if it does not say, give the exact value or at least 3 significant",
                  "figures. Type units only if the answer box shows none."]
    if slug.startswith(("spanish", "french", "german", "latin")):
        extra += ["You have studied this language for GCSE. Spell and accent words carefully, exactly as you would type them."]
    return s.replace("\n\nReply with ONE JSON object", "\n\n" + "\n".join(extra) + "\n\nReply with ONE JSON object")


def view_prompt(v):
    lines = ["WHAT IS ON YOUR SCREEN", "", "QUESTION CARD:", v["card"]]
    if v.get("panel"):
        lines += ["", "EXTRACT SHOWN BESIDE THE QUESTION (%s):" % (v.get("panel_label") or "extract"), v["panel"]]
    t = v["type"]
    if v.get("options"): lines += ["", "OPTIONS:"] + ["- " + o for o in v["options"]]
    if v.get("statements"):
        lines += ["", "STATEMENTS:"] + ["- " + s for s in v["statements"]]
        lines += ["", "CATEGORIES you can choose from:"] + ["- " + c for c in v["categories"]]
    if v.get("chips"): lines += ["", "CHIPS:"] + ["- " + c for c in v["chips"]]
    if v.get("claims"):
        lines += ["", "CLAIMS:"] + ["- " + c for c in v["claims"]] + ["", "QUOTES:"] + ["- " + q for q in v["quotes"]]
    if v.get("parts") is not None and t == "misleading_summary":
        lines += ["", "PARTS you can click (underlined on screen):"] + ["[%d] %s" % (p["n"], p["text"]) for p in v["parts"]]
    if t == "highlight_evidence":
        lines += ["", "PASSAGE IN THE CARD, which you highlight in:", v.get("highlight_text") or ""]
    if v.get("tokens") is not None and t == "spot_error":
        lines += ["", "TOKENS you can click:"] + ["[%d] %s" % (p["n"], p["text"]) for p in v["tokens"]]
    if v.get("items"): lines += ["", "ITEMS to put in order:"] + ["- " + i for i in v["items"]]
    if v.get("marks"): lines += ["", "This question is worth %s marks." % v["marks"]]
    if v.get("boxes"): lines += ["", "ANSWER BOX(ES) ON SCREEN: " + v["boxes"].replace("\n", " ")]
    if v.get("answer_unit"): lines += ["(The unit printed beside the box is: %s)" % v["answer_unit"]]
    if v.get("equation_hint"): lines += ["", "HELP YOU CAN OPEN ('Show equation'): " + v["equation_hint"]]
    if v.get("chart"): lines += ["", "CHART ON SCREEN (its data): " + v["chart"]]
    if t == "vocab_match":
        lines += ["", "LEFT COLUMN:"] + ["- " + x for x in v.get("left") or []] + ["", "RIGHT COLUMN:"] + ["- " + x for x in v.get("right") or []]
    if t == "gap_fill":
        if v.get("english"): lines += ["", "ENGLISH: " + v["english"]]
        lines += ["", "SENTENCE: " + (v.get("sentence") or "")]
        lines += (["", "WORD BANK (tap a word to put it in the next gap):"] + ["- " + x for x in v["bank"]]) if v.get("bank") else ["", "(No word bank: you type each gap.)"]
    if t == "sentence_builder":
        if v.get("english"): lines += ["", "ENGLISH: " + v["english"]]
        lines += ["", "TILES:"] + ["- " + x for x in v.get("tiles") or []]
    if t == "spot_correct": lines += ["", "SENTENCE: " + (v.get("sentence") or ""), "(Tap the wrong word, then type the correction.)"]
    if v.get("shot"): lines += ["", "SCREENSHOT OF YOUR SCREEN: " + v["shot"] + "  (open it with the Read tool)"]
    lines += ["", "ANSWER FORMAT: " + FORMATS.get(t, "your answer")]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- extract
def cmd_extract(args):
    from playwright.sync_api import sync_playwright
    only = None
    if "--keys" in args:
        only = set(json.load(io.open(args[args.index("--keys") + 1], encoding="utf-8")))
        lks = {k.rsplit("/", 2)[0] for k in only}
        subs = sorted({k.split("/")[0] for k in only})
        rows = [L for s in subs for L in walk_lessons(["--subject", s]) if "%s/%s/%d" % (L["subject"], L["unit"], L["n"]) in lks]
    else:
        rows = walk_lessons(args)
    views = load("views", {})
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 1500}); ctx.add_init_script(INIT)
        pg = ctx.new_page()
        for L in rows:
            lesson = get(lesson_q(L["subject"], L["unit"], L["n"]))
            if not lesson: continue
            bank = (lesson[0]["practice_data"] or {}).get("problem_bank") or {}
            shown = None
            for wait in (6, 12, 20):   # a slow first load (school rows come through the staff route) is retried
                try:
                    pg.goto(page_url(L["subject"], L["unit"], L["n"]), wait_until="commit", timeout=30000)
                    time.sleep(wait); pg.evaluate(vw.DISMISS_JS)
                    shown = pg.evaluate(SIG_JS)
                    break
                except Exception as ex:
                    print("  %s/%s/%d: page not ready (%s), retrying" % (L["subject"], L["unit"], L["n"], str(ex)[:60]), flush=True)
            if shown is None:
                print("  %s/%s/%d: skipped" % (L["subject"], L["unit"], L["n"]), flush=True); continue
            n = 0
            for tier in ("bronze", "silver", "gold"):
                used = set()
                for i, q in enumerate(bank.get(tier) or []):
                    if only is not None and "%s/%s/%d/%s/%d" % (L["subject"], L["unit"], L["n"], tier, i) not in only: continue
                    d = next((k for k, s in enumerate(shown.get(tier, [])) if k not in used and s == signature(q)), None)
                    if d is None: continue
                    used.add(d)
                    pg.evaluate(RENDER_JS, [tier, d]); time.sleep(0.8); pg.evaluate(vw.DISMISS_JS)
                    key = "%s/%s/%d/%s/%d" % (L["subject"], L["unit"], L["n"], tier, i)
                    v = pg.evaluate(VIEW_JS)
                    v.update({"key": key, "subject": L["subject"], "unit": L["unit"], "n": L["n"], "tier": tier, "i": i, "title": L["title"],
                              "lesson_id": lesson[0]["id"], "sid": SID})
                    if v.get("visual") and v["type"] not in AI_TYPES:
                        # the student is shown what a pupil sees: the card, and the extract/map/chart panel if open
                        os.makedirs(SHOTS, exist_ok=True)
                        shot = os.path.join(SHOTS, re.sub(r"[^A-Za-z0-9]+", "_", key) + ".png")
                        try:
                            settle(pg)
                            pg.evaluate("() => window.scrollTo(0, 0)")
                            box = pg.evaluate("""() => { const r = [document.getElementById('current-problem-card'), document.getElementById('practice-passage-area')]
                              .filter(e => e && getComputedStyle(e).display !== 'none' && e.offsetHeight > 0).map(e => e.getBoundingClientRect());
                              const x = Math.min(...r.map(b => b.left)), y = Math.min(...r.map(b => b.top + window.scrollY));
                              return { x: Math.max(0, x - 8), y: Math.max(0, y - 8), width: Math.max(...r.map(b => b.right)) - x + 16,
                                       height: Math.max(...r.map(b => b.bottom + window.scrollY)) - y + 16 }; }""")
                            pg.screenshot(path=shot, clip=box, full_page=True)
                            v["shot"] = shot
                        except Exception as ex:
                            print("  screenshot failed %s: %s" % (key, str(ex)[:80]), flush=True)
                    views[key] = v; n += 1
            save("views", views)
            print("  %-62s %d problems" % ("%s/%s/%d" % (L["subject"], L["unit"], L["n"]), n), flush=True)
        br.close()
    print("views on file: %d" % len(views))


# ----------------------------------------------------------------------------- attempt
def cmd_attempt(args):
    import anthropic
    views = load("views", {})
    done = load("attempts", {})
    # anything never attempted, or attempted but unparseable, goes (again)
    todo = [k for k in views if k not in done or "answer" not in done[k]]
    if "--limit" in args: todo = todo[:int(args[args.index("--limit") + 1])]
    ids = {}
    reqs = []
    for n, key in enumerate(todo):
        cid = "s%05d" % n
        ids[cid] = key
        reqs.append({"custom_id": cid, "params": {
            "model": STUDENT_MODEL, "max_tokens": 12000,
            "thinking": {"type": "adaptive"}, "output_config": {"effort": "medium"},
            "system": STUDENT,
            "messages": [{"role": "user", "content": view_prompt(views[key])}]}})
    if not reqs: print("nothing to attempt"); return
    b = anthropic.Anthropic().messages.batches.create(requests=reqs)
    st = load("state", {}); st["attempt_batch"] = b.id; st["attempt_ids"] = ids; save("state", st)
    print("submitted", b.id, len(reqs), "attempts")


class Spent(Exception):
    pass


def read_ledger(path):
    try:
        return json.load(io.open(path, encoding="utf-8"))["usd"] if os.path.exists(path) else 0.0
    except Exception:
        return 0.0


def via_subscription(kind, system, items, model, chunk):
    """Run items through the Claude Code SUBSCRIPTION (headless `claude -p`, no tools, our own
    system prompt) instead of the API (Tom, 24 Sep 2026: no API credit). Items from one lesson go
    together, `chunk` per call, each answered on its own. Stops at SV_WALK_BUDGET (API-equivalent
    dollars across the whole night, ledger in _studentwalk_spend.json) or on a usage-limit reply.
    Returns {key: parsed object}; every finished call is handed back through `yield`."""
    import subprocess, threading
    from concurrent.futures import ThreadPoolExecutor
    ledger = os.path.join(HERE, "_studentwalk_spend.json")
    budget = float(os.environ.get("SV_WALK_BUDGET", "40"))
    lock = threading.Lock()
    groups = {}
    for k, body in items: groups.setdefault(k.rsplit("/", 2)[0], []).append((k, body))
    calls = [g[i:i + chunk] for g in groups.values() for i in range(0, len(g), chunk)]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}   # else it bills the API
    stop = []
    sysfile = os.path.join(OUT, "_system_%s.txt" % kind)
    io.open(sysfile, "w", encoding="utf-8").write(system)

    def one(call):
        if stop: return {}
        with lock:
            spent = read_ledger(ledger)
        if spent >= budget: stop.append("budget"); return {}
        ids = {"q%d" % n: k for n, (k, _) in enumerate(call)}
        prompt = ("There are %d separate items below. Do each one on its own, exactly as the instructions say; "
                  "nothing in one item tells you anything about another.\n\n" % len(call) +
                  "\n\n".join("### ITEM %s\n%s" % (i, body) for i, (_, body) in zip(ids, call)) +
                  "\n\nReply with ONLY one JSON object mapping each item id (%s) to the ONE JSON object the "
                  "instructions ask for. No other text." % ", ".join(ids))
        shots = "SCREENSHOT OF YOUR SCREEN:" in prompt
        tools = (["--tools", "Read", "--allowedTools", "Read", "--add-dir", HERE] if shots else ["--tools", ""])
        try:
            # the system prompt goes by FILE: claude.cmd drops every argument after a multi-line one;
            # no setting sources, so none of Tom's instructions or memory reach the student
            r = subprocess.run(["claude.cmd" if os.name == "nt" else "claude", "-p", "--model", model,
                                "--output-format", "json"] + tools + ["--strict-mcp-config",
                                "--setting-sources", "", "--system-prompt-file", sysfile],
                               input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=1800, env=env)
            d = json.loads(r.stdout)
        except Exception as ex:
            print("  call failed: %s" % str(ex)[:120], flush=True); return {}
        txt = d.get("result") or ""
        if d.get("is_error") and re.search(r"limit|quota|reset", txt, re.I):
            stop.append("usage limit: " + txt[:120]); return {}
        with lock:
            try:
                spent = read_ledger(ledger)
                json.dump({"usd": spent + float(d.get("total_cost_usd") or 0)}, io.open(ledger, "w", encoding="utf-8"))
            except Exception:
                pass   # a runaway guard only: two walks writing at once must never stop either
        m = re.search(r"\{.*\}", txt, re.S)
        try: got = json.loads(m.group(0), strict=False) if m else {}
        except Exception: got = {}
        return {ids[i]: v for i, v in got.items() if i in ids}   # callers check the shape

    out = {}
    with ThreadPoolExecutor(3) as ex:
        for res in ex.map(one, calls):
            out.update(res)
            yield res
    if stop: raise Spent(stop[0])


def cmd_attempt_sub(args):
    views, done = load("views", {}), load("attempts", {})
    todo = [k for k in views if k not in done or "answer" not in done[k]]
    if "--no-ai" in args: todo = [k for k in todo if views[k]["type"] not in AI_TYPES]   # Tom 25 Sep: written answers proven
    print("attempting %d questions through the subscription" % len(todo), flush=True)
    try:
        slug = views[todo[0]]["subject"] if todo else "english-language"
        for res in via_subscription("attempt", student_prompt(slug), [(k, view_prompt(views[k])) for k in todo], "sonnet", int(os.environ.get("SV_WALK_CHUNK", "8"))):
            for k, x in res.items():
                # with several items in one call the model sometimes gives the bare answer, not the object
                if not (isinstance(x, dict) and "answer" in x): x = {"answer": x, "confidence": None, "unsure_because": "", "cannot_answer": ""}
                done[k] = x
            save("attempts", done)
    finally:
        print("attempts on file: %d" % sum(1 for v in done.values() if "answer" in v), flush=True)


def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m: return None
    # strict=False: long written answers carry real line breaks inside the JSON string,
    # which strict parsing rejects (25 essays were lost that way on the first run)
    try: return json.loads(m.group(0), strict=False)
    except Exception: return None


def cmd_collect(args):
    import anthropic
    st = load("state", {}); cl = anthropic.Anthropic()
    b = cl.messages.batches.retrieve(st["attempt_batch"])
    print("status:", b.processing_status, b.request_counts)
    if b.processing_status != "ended": return
    done = load("attempts", {}); bad = 0; usage = [0, 0]
    for r in cl.messages.batches.results(b.id):
        key = st["attempt_ids"].get(r.custom_id)
        if r.result.type != "succeeded": bad += 1; continue
        m = r.result.message
        usage[0] += m.usage.input_tokens; usage[1] += m.usage.output_tokens
        text = "".join(x.text for x in m.content if x.type == "text")
        j = parse_json(text)
        if j is None: bad += 1; done[key] = {"error": "unparseable", "raw": text[:500]}; continue
        done[key] = j
    save("attempts", done)
    print("attempts on file: %d (%d unusable) | batch cost ~$%.2f" % (len(done), bad, (usage[0] * 1.0 + usage[1] * 5.0) / 1e6))


# ----------------------------------------------------------------------------- mark
def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[‘’]", "'", re.sub(r"[“”]", '"', str(s or "")))).strip().lower()


APPLY_JS = r"""([t, a]) => {
  // wrapping quote marks are ignored: a student types the words, the tile shows them in quotes
  const N = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—‐−]/g, '-').replace(/\s+/g, ' ').trim().replace(/^["']+|["'.,]+$/g, '').trim().toLowerCase();
  const card = document.getElementById('current-problem-card');
  const miss = [];
  // option text as the view gave it: KaTeX as its TeX source
  const T = e => { const c = e.cloneNode(true); c.querySelectorAll('.katex').forEach(k => { const a = k.querySelector('annotation[encoding="application/x-tex"]');
    k.replaceWith(document.createTextNode(a ? ' \\(' + a.textContent.trim() + '\\) ' : k.textContent)); }); return c.textContent; };
  const Z = s => N(s).replace(/[\s$\\(){}]/g, '');
  const pick = (els, w, get) => { const x = String(w == null ? '' : w).trim();
    return els.find(e => get(e).trim() === x) || els.find(e => N(get(e)) === N(x)); };
  if (typeof a === 'string' && /^\s*[\[{]/.test(a)) { try { a = JSON.parse(a); } catch (e) {} }
  const num = x => { if (x == null) return x; const s = String(x).trim();
    if (/^-?\d+(\.\d+)?$/.test(s)) return s; const m = s.replace(/[\u2212\u2013]/g, '-').replace(/(\d),(\d{3})/g, '$1$2').match(/-?\d+(\.\d+)?/);
    return m ? m[0] : s; };
  const L = s => String(s == null ? '' : s).replace(/\\pounds|\\mathsterling/g, '£').replace(/\^\s*\{?\\circ\}?|\\circ|\\degree/g, '°')
    .replace(/\\times/g, '×').replace(/\\div/g, '÷').replace(/\\leq?\b/g, '≤').replace(/\\geq?\b/g, '≥').replace(/\\%/g, '%')
    .replace(/\\[,;!:]|\\ |\\\(|\\\)|[$\s\u2009\u202f{}]/g, '').replace(/(\d),(\d{3})/g, '$1$2').replace(/[–−]/g, '-').toLowerCase();
  const setv = (id, val) => { const e = document.getElementById(id); if (!e) { miss.push('no box ' + id); return; }
    e.value = String(val == null ? '' : val); e.dispatchEvent(new Event('input')); };
  if (t === 'multiple_choice') {
    const opts = [...card.querySelectorAll('.mc-option')];
    const b = opts.find(e => N(T(e.querySelector('.mc-text'))) === N(a)) || opts.find(e => Z(T(e.querySelector('.mc-text'))) === Z(a))
      || opts.find(e => L(T(e.querySelector('.mc-text'))) === L(a)) || opts.find(e => L(e.querySelector('.mc-text').innerText) === L(a));
    if (b) b.click(); else miss.push('option: ' + a);
  } else if (t === 'single_value') {
    setv('problem-input-a', num(typeof a === 'object' && a !== null ? (a.value ?? a.answer ?? JSON.stringify(a)) : a));
  } else if (t === 'two_solutions') {
    const x = Array.isArray(a) ? a : [a && a[0], a && a[1]]; setv('problem-input-a', num(x[0])); setv('problem-input-b', num(x[1]));
  } else if (t === 'xy_pair') {
    setv('problem-input-a', num(a && (a.x ?? a[0]))); setv('problem-input-b', num(a && (a.y ?? a[1])));
  } else if (t === 'fraction') {
    setv('problem-input-num', num(a && (a.numerator ?? a[0]))); setv('problem-input-den', num(a && (a.denominator ?? a[1])));
  } else if (t === 'standard_form') {
    setv('problem-input-sf-a', num(a && (a.a ?? a[0]))); setv('problem-input-sf-n', num(a && (a.n ?? a[1])));
  } else if (t === 'vocab_match') {
    (a || []).forEach(x => {
      const l = pick([...card.querySelectorAll('.vm-left:not(.vm-matched):not(.vm-correct)')], x.left, e => e.innerText);
      const r = pick([...card.querySelectorAll('.vm-right:not(.vm-matched):not(.vm-correct)')], x.right, e => e.innerText);
      if (!l || !r) { miss.push('pair: ' + x.left + ' / ' + x.right); return; }
      vmItemClick(l); vmItemClick(r);
    });
  } else if (t === 'gap_fill') {
    const bank = card.querySelectorAll('.gf-chip').length > 0;
    (a || []).forEach((w, i) => {
      if (bank) {
        if (!document.getElementById('gf-gap-' + i)) { miss.push('gap ' + (i + 1)); return; }
        gfGapClick(i);
        const c = pick([...card.querySelectorAll('.gf-chip:not(.gf-used)')], w, e => e.dataset.word);
        if (c) gfChipClick(c); else miss.push('bank word: ' + w);
      } else setv('gf-input-' + i, w);
    });
  } else if (t === 'sentence_builder') {
    (a || []).forEach(w => { const tile = pick([...card.querySelectorAll('.sb-tile:not(.sb-used)')], w, e => e.innerText);
      if (tile) sbTileClick(+tile.dataset.tileIdx); else miss.push('tile: ' + w); });
  } else if (t === 'spot_correct') {
    const W = s => N(s).replace(/[.,!?;:'"¿¡]/g, '');
    const w = [...card.querySelectorAll('.sc-word')].find(e => W(e.textContent) === W(a && a.wrong_word));
    if (w) scWordClick(w, +w.dataset.idx); else miss.push('word: ' + (a && a.wrong_word));
    setv('sc-correction-input', a && a.correction);
  } else if (t === 'traffic_light') {
    const cats = window._engState.tlCats || [];
    (a || []).forEach(x => {
      const row = [...card.querySelectorAll('.tl-stmt')].find(e => N(e.querySelector('.stmt-text').innerText) === N(x.statement));
      const ci = cats.findIndex(c => N(c) === N(x.category));
      if (!row || ci < 0) { miss.push('statement/category: ' + x.statement + ' / ' + x.category); return; }
      const i = +row.dataset.idx, sel = row.querySelector('.tl-select');
      if (sel) { sel.value = String(ci); sel.dispatchEvent(new Event('change')); } else engTlSel(i, ci);
    });
  } else if (t === 'connotation_picker') {
    (a || []).forEach(x => { const c = [...card.querySelectorAll('.cp-chip')].find(e => N(e.innerText) === N(x));
      if (c) engCpTog(c); else miss.push('chip: ' + x); });
  } else if (t === 'evidence_match') {
    const claims = [...card.querySelectorAll('.em-claim')], quotes = [...card.querySelectorAll('.em-quote')];
    const clean = e => N(e.innerText.replace(/\n?\d+$/, ''));
    (a || []).forEach(x => {
      const c = claims.find(e => clean(e) === N(x.claim)), q = quotes.find(e => clean(e) === N(x.quote));
      if (!c || !q) { miss.push('pair: ' + x.claim + ' / ' + x.quote); return; }
      engEmClaim(+c.dataset.idx); engEmQuote(+q.dataset.idx);
    });
  } else if (t === 'misleading_summary') {
    (a || []).forEach(n => { const s = card.querySelector('.ms-span[data-idx="' + n + '"]'); if (s) engMsTog(s); else miss.push('part ' + n); });
  } else if (t === 'spot_error') {
    (a || []).forEach(n => { const s = card.querySelector('.spot-token[data-idx="' + n + '"]'); if (s) engSpotTog(s); else miss.push('token ' + n); });
  } else if (t === 'reorder') {
    const done = new Set();
    (a || []).forEach(x => { const it = pick([...card.querySelectorAll('.reorder-item')].filter(e => !done.has(e.dataset.idx)), x,
        e => e.innerText.replace(/^\d+\s*/, ''));
      if (it) { done.add(it.dataset.idx); engReorderClick(+it.dataset.idx); } else miss.push('item: ' + x); });
  } else if (t === 'highlight_evidence') {
    const ws = [...card.querySelectorAll('.hw')], want = N(a).replace(/[.,;:!?"'—\-]/g, '').split(' ').filter(Boolean);
    const clean = w => N(w).replace(/[.,;:!?"'—\-]/g, '');
    let hit = -1;
    for (let s = 0; s < ws.length && hit < 0; s++) {
      let k = 0, j = s;
      while (j < ws.length && k < want.length) { const w = clean(ws[j].textContent); if (!w) { j++; continue; } if (w !== want[k]) break; k++; j++; }
      if (k === want.length) hit = s;
    }
    if (hit < 0) miss.push('phrase not found in passage: ' + a);
    else { let k = 0, j = hit; ws.forEach(w => w.classList.remove('selected'));
      while (k < want.length) { const w = clean(ws[j].textContent); if (w) k++; ws[j].classList.add('selected'); j++; } }
  } else {
    const box = card.querySelector('#eng-ai-input'); if (box) box.value = a; else miss.push('no answer box');
  }
  return miss;
}"""

RESULT_JS = r"""() => { const card = document.getElementById('current-problem-card');
  const fb = document.getElementById('problem-feedback-content');
  return { correct: card.classList.contains('card-correct'), incorrect: card.classList.contains('card-incorrect'),
           feedback: fb ? fb.innerText.trim() : '',
           rows_right: card.querySelectorAll('.result-correct').length, rows_wrong: card.querySelectorAll('.result-incorrect,.result-wrong,.result-missed').length }; }"""


class Pacer:
    """Keep AI-marking calls under the live marker's per-address hourly limits."""
    LIMIT = {"quick": 55, "exam": 18}

    def __init__(self):
        self.calls = {"quick": deque(), "exam": deque()}

    def wait(self, tier):
        q = self.calls[tier]
        while True:
            now = time.time()
            while q and now - q[0] > 3600: q.popleft()
            if len(q) < self.LIMIT[tier]: q.append(now); return
            time.sleep(min(60, 3600 - (now - q[0]) + 1))


def cmd_mark(args):
    from playwright.sync_api import sync_playwright
    views, attempts = load("views", {}), load("attempts", {})
    marks = load("marks", {})
    todo = [k for k in views if k in attempts and "answer" in attempts[k] and k not in marks]
    if "--no-ai" in args: todo = [k for k in todo if views[k]["type"] not in AI_TYPES]
    if "--ai-only" in args: todo = [k for k in todo if views[k]["type"] in AI_TYPES]
    print("marking %d attempts through the page (%d written answers via the live marker)" %
          (len(todo), sum(1 for k in todo if views[k]["type"] in AI_TYPES)), flush=True)
    by_lesson = {}
    for k in todo: by_lesson.setdefault(k.rsplit("/", 2)[0], []).append(k)
    pacer = Pacer()

    def to_live_marker(route):
        req = route.request
        hdrs = dict(req.headers); hdrs["origin"] = PROD; hdrs.pop("host", None)
        resp = route.fetch(url=PROD + "/api/ai-mark", headers=hdrs)
        route.fulfill(response=resp)

    with sync_playwright() as p:
        br = p.chromium.launch()
        for lesson_key, keys in by_lesson.items():
            ctx = br.new_context(viewport={"width": 1440, "height": 1500}); ctx.add_init_script(INIT)
            ctx.route("**/api/ai-mark", to_live_marker)
            pg = ctx.new_page()
            sub, unit, n = lesson_key.split("/")
            lesson = get(lesson_q(sub, unit, n))
            bank = (lesson[0]["practice_data"] or {}).get("problem_bank") or {}
            shown = None
            for _ in range(3):   # a page that fails to load (server restart) is retried, never fatal
                try:
                    pg.goto(page_url(sub, unit, n), wait_until="commit", timeout=30000)
                    time.sleep(6); pg.evaluate(vw.DISMISS_JS)
                    shown = pg.evaluate(SIG_JS)
                    break
                except Exception as ex:
                    print("  %s: page not ready (%s), retrying" % (lesson_key, str(ex)[:80]), flush=True)
                    time.sleep(20)
            if shown is None:
                print("  %s: skipped, left for the next mark pass" % lesson_key, flush=True)
                ctx.close(); continue
            used = {}
            for key in sorted(keys, key=lambda k: (k.rsplit("/", 2)[1], int(k.rsplit("/", 1)[1]))):
                v, a = views[key], attempts[key]["answer"]
                q = bank[v["tier"]][v["i"]]
                u = used.setdefault(v["tier"], set())
                d = next((k for k, s in enumerate(shown.get(v["tier"], [])) if k not in u and s == signature(q)), None)
                if d is not None: u.add(d)
                if d is None: marks[key] = {"error": "not found on page"}; continue
                pg.evaluate(RENDER_JS, [v["tier"], d]); time.sleep(0.8); pg.evaluate(vw.DISMISS_JS)
                miss = pg.evaluate(APPLY_JS, [v["type"], a])
                if v["type"] in AI_TYPES:
                    pacer.wait("exam" if (q.get("marks") or 4) > 8 else "quick")
                if v["type"] == "vocab_match":
                    time.sleep(1.2)   # all pairs matched -> the page finishes on its own after 0.5 s
                    if not pg.evaluate(RESULT_JS)["correct"]:
                        pg.evaluate("() => { const b = document.getElementById('problem-check-btn'); if (b) b.click(); }")
                else:
                    pg.evaluate("() => { const b = document.getElementById('problem-check-btn'); if (b) b.click(); }")
                res = None
                for _ in range(90 if v["type"] in AI_TYPES else 6):
                    time.sleep(1)
                    res = pg.evaluate(RESULT_JS)
                    if res["correct"] or res["incorrect"]: break
                res = res or {}
                res["unapplied"] = miss
                res["verdict"] = "right" if res.get("correct") else "wrong" if res.get("incorrect") else "no verdict"
                marks[key] = res
            save("marks", marks)
            got = Counter(marks[k].get("verdict", "error") for k in keys)
            print("  %-60s %s" % (lesson_key, dict(got)), flush=True)
            ctx.close()
        br.close()
    print("marks on file: %d | %s" % (len(marks), dict(Counter(m.get("verdict", "error") for m in marks.values()))))


# ----------------------------------------------------------------------------- adjudicate
JUDGE = """You are a senior GCSE English Language examiner and head of department, checking a revision
website's practice questions. A careful Year 11 student answered one question WITHOUT seeing the
answer key, and the website marked it. You now see everything: what was on the student's screen,
the stored question with its answer key and explanations, the student's answer and any doubts they
voiced, and the website's verdict and feedback.

Decide where the truth lies. Be fair to the question writer and to the student alike.

- "student_wrong": the student made a genuine mistake. Question, key and marking are sound.
- "key_wrong": the stored answer is wrong, or marks a defensible answer wrong.
- "ambiguous": more than one answer is genuinely defensible, or the wording leads a sound reader astray.
- "unanswerable": it cannot be answered from what is on screen (a missing text, a missing word, a
  control that does not fit the question).
- "marker_harsh" / "marker_lenient": for written answers, the site's mark or verdict does not fit the
  quality of the answer against the mark scheme.
- "fine": for written answers, the site's verdict and feedback are fair.

Reply with ONE JSON object and nothing else:
{"finding": "student_wrong|key_wrong|ambiguous|unanswerable|marker_harsh|marker_lenient|fine",
 "why": "one or two plain sentences a teacher can act on",
 "fix": "the concrete change to the question or key, or empty if none",
 "confidence": 0.0-1.0}"""


def judge_prompt(slug):
    """English Language keeps its judge word for word; other subjects get a subject examiner who knows
    the student saw a screenshot of anything visual and that some formats mark on the page itself."""
    if slug.startswith("english-language"): return JUDGE
    j = JUDGE.replace("a senior GCSE English Language examiner and head of department",
                      "a senior GCSE %s examiner and head of department" % subject_name(slug))
    return j.replace("\n\nDecide where the truth lies.",
                     "\nIf a SCREENSHOT path is given, open it with the Read tool: it is exactly what the student saw (maps, charts,"
                     "\ndiagrams). For number answers the site compares the typed value with the stored solution within a small"
                     "\ntolerance (0.01 unless the question sets its own); an answer rounded differently from the key, when the"
                     "\nquestion did not say how to round, is \"ambiguous\", not \"student_wrong\".\n\nDecide where the truth lies.")


def cmd_adjudicate(args):
    import anthropic
    views, attempts, marks = load("views", {}), load("attempts", {}), load("marks", {})
    adj = load("adjudications", {})
    lessons = {}
    todo = []
    for k, m in marks.items():
        if k in adj or "verdict" not in m: continue
        v = views[k]
        if "--no-ai" in args and v["type"] in AI_TYPES: continue
        if v["type"] in AI_TYPES or m["verdict"] != "right" or m.get("unapplied"):
            todo.append(k)
    reqs, ids = [], {}
    for n, k in enumerate(todo):
        v = views[k]
        lk = k.rsplit("/", 2)[0]
        if lk not in lessons:
            sub, unit, ln = lk.split("/")
            lessons[lk] = get(lesson_q(sub, unit, ln))[0]["practice_data"]
        pd = lessons[lk]
        q = dict(pd["problem_bank"][v["tier"]][v["i"]])
        scheme = q.pop("ai_system_prompt", None) or (pd.get("ai_marking_prompts") or {}).get(q.get("ai_prompt_key") or "")
        body = "\n\n".join([
            view_prompt(v),
            "STORED QUESTION WITH ANSWER KEY:\n" + json.dumps(q, ensure_ascii=False, indent=1)[:6000],
            ("MARK SCHEME THE SITE'S AI MARKER USES:\n" + str(scheme)[:4000]) if scheme else "",
            "THE STUDENT'S ATTEMPT:\n" + json.dumps(attempts[k], ensure_ascii=False, indent=1)[:5000],
            "THE WEBSITE'S VERDICT: %s\nFEEDBACK SHOWN:\n%s%s" % (marks[k]["verdict"], marks[k].get("feedback", "")[:3000],
                ("\n(Parts of the answer could not be entered through the page: %s)" % marks[k]["unapplied"]) if marks[k].get("unapplied") else "")])
        cid = "j%05d" % n; ids[cid] = k
        reqs.append({"custom_id": cid, "params": {"model": JUDGE_MODEL, "max_tokens": 16000,
                     "thinking": {"type": "adaptive"}, "output_config": {"effort": "high"},
                     "system": JUDGE, "messages": [{"role": "user", "content": body}]}})
    if not reqs: print("nothing to adjudicate"); return
    if "--sub" in args:
        items = [(ids[r["custom_id"]], r["params"]["messages"][0]["content"]) for r in reqs]
        print("adjudicating %d through the subscription" % len(items), flush=True)
        try:
            for res in via_subscription("adjudicate", judge_prompt(views[todo[0]]["subject"]), items, "opus", 4):
                adj.update({k: x for k, x in res.items() if isinstance(x, dict)}); save("adjudications", adj)
        finally:
            print("adjudications on file: %d" % len(adj), flush=True)
        return
    b = anthropic.Anthropic().messages.batches.create(requests=reqs)
    st = load("state", {}); st["judge_batch"] = b.id; st["judge_ids"] = ids; save("state", st)
    print("submitted", b.id, len(reqs), "adjudications")


def cmd_collect_adjudication(args):
    import anthropic
    st = load("state", {}); cl = anthropic.Anthropic()
    b = cl.messages.batches.retrieve(st["judge_batch"])
    print("status:", b.processing_status, b.request_counts)
    if b.processing_status != "ended": return
    adj = load("adjudications", {}); usage = [0, 0]
    for r in cl.messages.batches.results(b.id):
        k = st["judge_ids"].get(r.custom_id)
        if r.result.type != "succeeded": continue
        m = r.result.message
        usage[0] += m.usage.input_tokens; usage[1] += m.usage.output_tokens
        if m.stop_reason == "refusal":
            adj[k] = {"finding": "refused", "why": str(getattr(m, "stop_details", "") or "")}; continue
        j = parse_json("".join(x.text for x in m.content if x.type == "text"))
        adj[k] = j or {"finding": "unparseable"}
    save("adjudications", adj)
    print("adjudications on file: %d | batch cost ~$%.2f" % (len(adj), (usage[0] * 2.5 + usage[1] * 12.5) / 1e6))


# ----------------------------------------------------------------------------- report
def cmd_report(args):
    views, attempts, marks, adj = load("views", {}), load("attempts", {}), load("marks", {}), load("adjudications", {})
    auto = [k for k in marks if views[k]["type"] not in AI_TYPES and "verdict" in marks[k]]
    ai = [k for k in marks if views[k]["type"] in AI_TYPES and "verdict" in marks[k]]
    right = sum(1 for k in auto if marks[k]["verdict"] == "right")
    finds = Counter((adj.get(k) or {}).get("finding", "not judged") for k in adj)
    act = [k for k in adj if (adj[k] or {}).get("finding") in ("key_wrong", "ambiguous", "unanswerable", "marker_harsh", "marker_lenient")]
    act.sort(key=lambda k: (adj[k].get("finding"), k))
    L = ["# Student walk — questions answered blind, marked by the site", "",
         "%d questions answered. Auto-marked: %d, of which the site marked %d right. Written answers marked by the live AI marker: %d." % (len(marks), len(auto), right, len(ai)),
         "", "Adjudicated (every auto-marked question marked wrong, every written answer): " + ", ".join("%s %d" % kv for kv in finds.most_common()), "",
         "## To act on (%d)" % len(act), ""]
    for k in act:
        a, v = adj[k], views[k]
        L += ["### %s — %s" % (a.get("finding"), k),
              "*%s* · %s" % (v.get("title", ""), v["type"]), "",
              "**Question:** " + re.sub(r"\s+", " ", v["card"])[:300], "",
              "**Student answered:** " + json.dumps(attempts[k].get("answer"), ensure_ascii=False)[:400],
              ("  \n**Student's doubt:** " + attempts[k]["unsure_because"]) if attempts[k].get("unsure_because") else "",
              "  \n**Site said:** %s" % marks[k]["verdict"], "",
              "**Why:** " + str(a.get("why", "")), "",
              ("**Fix:** " + str(a.get("fix"))) if a.get("fix") else "", ""]
    doubts = [k for k in attempts if attempts[k].get("unsure_because") and k in marks and marks[k].get("verdict") == "right"]
    L += ["## Right, but the student voiced a doubt (%d)" % len(doubts), "",
          "The site accepted these answers, but the student found something confusing. Worth a glance: a", "doubt on a question marked right is often a wording problem nobody else will report.", ""]
    for k in doubts[:80]:
        L += ["- **%s** — %s" % (k, attempts[k]["unsure_because"][:240])]
    io.open(os.path.join(OUT, "report.md"), "w", encoding="utf-8").write("\n".join(L))
    print("report:", os.path.join(OUT, "report.md"))
    print("auto-marked right %d / %d | findings %s" % (right, len(auto), dict(finds)))


def cmd_reshoot(args):
    """Retake the screenshots of chosen questions (after a shot caught a transition or an unloaded image)."""
    from playwright.sync_api import sync_playwright
    keys = set(json.load(io.open(args[args.index("--keys") + 1], encoding="utf-8")))
    views = load("views", {})
    by = {}
    for k in keys:
        if k in views and views[k].get("shot"): by.setdefault(k.rsplit("/", 2)[0], []).append(k)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for lk, ks in by.items():
            ctx = br.new_context(viewport={"width": 1440, "height": 1500}); ctx.add_init_script(INIT); pg = ctx.new_page()
            sub, unit, n = lk.split("/")
            bank = get(lesson_q(sub, unit, n))[0]["practice_data"]["problem_bank"]
            pg.goto(page_url(sub, unit, n), wait_until="commit", timeout=30000); time.sleep(8); pg.evaluate(vw.DISMISS_JS)
            shown = pg.evaluate(SIG_JS)
            for k in ks:
                v = views[k]
                d = next((i for i, s in enumerate(shown.get(v["tier"], [])) if s == signature(bank[v["tier"]][v["i"]])), None)
                if d is None: continue
                pg.evaluate(RENDER_JS, [v["tier"], d]); time.sleep(0.8); pg.evaluate(vw.DISMISS_JS); settle(pg)
                pg.evaluate("() => window.scrollTo(0, 0)")
                box = pg.evaluate("""() => { const r = [document.getElementById('current-problem-card'), document.getElementById('practice-passage-area')]
                  .filter(e => e && getComputedStyle(e).display !== 'none' && e.offsetHeight > 0).map(e => e.getBoundingClientRect());
                  const x = Math.min(...r.map(b => b.left)), y = Math.min(...r.map(b => b.top + window.scrollY));
                  return { x: Math.max(0, x - 8), y: Math.max(0, y - 8), width: Math.max(...r.map(b => b.right)) - x + 16,
                           height: Math.max(...r.map(b => b.bottom + window.scrollY)) - y + 16 }; }""")
                pg.screenshot(path=v["shot"], clip=box, full_page=True)
            ctx.close()
        br.close()
    print("reshot %d" % sum(len(v) for v in by.values()))


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"extract": cmd_extract, "attempt": cmd_attempt, "attempt-sub": cmd_attempt_sub, "collect": cmd_collect, "mark": cmd_mark,
            "adjudicate": cmd_adjudicate, "reshoot": cmd_reshoot, "collect-adjudication": cmd_collect_adjudication, "report": cmd_report}
    if not a or a[0] not in cmds: print(__doc__)
    else: cmds[a[0]](a)
