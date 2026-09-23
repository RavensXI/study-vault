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
"""
import io, json, os, re, sys, time, urllib.request
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_studentwalk")
os.makedirs(OUT, exist_ok=True)
F = {k: os.path.join(OUT, k + ".json") for k in ("views", "attempts", "marks", "adjudications", "state")}
BASE = os.environ.get("SV_QA_BASE", "http://127.0.0.1:8910")
PROD = "https://www.studyvault.co.uk"
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
STUDENT_MODEL = "claude-sonnet-5"     # Tom's standing preference for checking work
JUDGE_MODEL = "claude-opus-5"
AI_TYPES = ("ai_mark", "ai_write", "improve_sentence")

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


INIT = ("try{localStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
        "sessionStorage.setItem('studyvault-auth',JSON.stringify({role:'admin'}));"
        "['sv-lesson-tour-v2','sv-lesson-tutorial-done','sv-reader-tour-v1','sv-highlight-tutorial-done']"
        ".forEach(function(k){localStorage.setItem(k,'1')});}catch(e){}")

RENDER_JS = """([t, d]) => { practiceState.currentTier = t; practiceState.currentIndex = d; practiceState.answered = false;
  document.getElementById('current-problem-card').classList.remove('card-correct', 'card-incorrect');
  renderCurrentProblem(); }"""

# What a student sees, as text. Controls are listed with the site's own indices so the
# answer can be put back through the same controls; nothing here comes from the key.
VIEW_JS = r"""() => {
  const card = document.getElementById('current-problem-card');
  const p = window._problemBank[practiceState.currentTier][practiceState.currentIndex];
  const t = p.input_type || 'single_value';
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
}


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
    lines += ["", "ANSWER FORMAT: " + FORMATS.get(t, "your answer")]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- extract
def cmd_extract(args):
    from playwright.sync_api import sync_playwright
    rows = vw.lessons_for(args)
    views = load("views", {})
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 1500}); ctx.add_init_script(INIT)
        pg = ctx.new_page()
        for L in rows:
            lesson = get("lessons?select=practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                         "&units.slug=eq.%s&lesson_number=eq.%d" % (L["subject"], L["unit"], L["n"]))
            if not lesson: continue
            bank = (lesson[0]["practice_data"] or {}).get("problem_bank") or {}
            try: pg.goto("%s/practice/%s/%s/%d?prob=bronze:0" % (BASE, L["subject"], L["unit"], L["n"]), wait_until="commit", timeout=30000)
            except Exception: pass
            time.sleep(6); pg.evaluate(vw.DISMISS_JS)
            shown = pg.evaluate(vw.SIG_JS)
            n = 0
            for tier in ("bronze", "silver", "gold"):
                used = set()
                for i, q in enumerate(bank.get(tier) or []):
                    d = next((k for k, s in enumerate(shown.get(tier, [])) if k not in used and s == vw.signature(q)), None)
                    if d is None: continue
                    used.add(d)
                    pg.evaluate(RENDER_JS, [tier, d]); time.sleep(0.8); pg.evaluate(vw.DISMISS_JS)
                    key = "%s/%s/%d/%s/%d" % (L["subject"], L["unit"], L["n"], tier, i)
                    v = pg.evaluate(VIEW_JS)
                    v.update({"key": key, "subject": L["subject"], "unit": L["unit"], "n": L["n"], "tier": tier, "i": i, "title": L["title"]})
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
  const N = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim().toLowerCase();
  const card = document.getElementById('current-problem-card');
  const miss = [];
  if (t === 'multiple_choice') {
    const b = [...card.querySelectorAll('.mc-option')].find(e => N(e.querySelector('.mc-text').innerText) === N(a));
    if (b) b.click(); else miss.push('option: ' + a);
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
    (a || []).forEach(x => { const it = [...card.querySelectorAll('.reorder-item')].find(e => N(e.innerText.replace(/^\d+\s*/, '')) === N(x));
      if (it) engReorderClick(+it.dataset.idx); else miss.push('item: ' + x); });
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
            lesson = get("lessons?select=practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                         "&units.slug=eq.%s&lesson_number=eq.%s" % (sub, unit, n))
            bank = (lesson[0]["practice_data"] or {}).get("problem_bank") or {}
            try: pg.goto("%s/practice/%s/%s/%s?prob=bronze:0" % (BASE, sub, unit, n), wait_until="commit", timeout=30000)
            except Exception: pass
            time.sleep(6); pg.evaluate(vw.DISMISS_JS)
            shown = pg.evaluate(vw.SIG_JS)
            for key in keys:
                v, a = views[key], attempts[key]["answer"]
                q = bank[v["tier"]][v["i"]]
                d = next((k for k, s in enumerate(shown.get(v["tier"], [])) if s == vw.signature(q)), None)
                if d is None: marks[key] = {"error": "not found on page"}; continue
                pg.evaluate(RENDER_JS, [v["tier"], d]); time.sleep(0.8); pg.evaluate(vw.DISMISS_JS)
                miss = pg.evaluate(APPLY_JS, [v["type"], a])
                if v["type"] in AI_TYPES:
                    pacer.wait("exam" if (q.get("marks") or 4) > 8 else "quick")
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


def cmd_adjudicate(args):
    import anthropic
    views, attempts, marks = load("views", {}), load("attempts", {}), load("marks", {})
    adj = load("adjudications", {})
    lessons = {}
    todo = []
    for k, m in marks.items():
        if k in adj or "verdict" not in m: continue
        v = views[k]
        if v["type"] in AI_TYPES or m["verdict"] != "right" or m.get("unapplied"):
            todo.append(k)
    reqs, ids = [], {}
    for n, k in enumerate(todo):
        v = views[k]
        lk = k.rsplit("/", 2)[0]
        if lk not in lessons:
            sub, unit, ln = lk.split("/")
            lessons[lk] = get("lessons?select=practice_data,units!inner(slug,subjects!inner(slug))&units.subjects.slug=eq.%s"
                              "&units.slug=eq.%s&lesson_number=eq.%s" % (sub, unit, ln))[0]["practice_data"]
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


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"extract": cmd_extract, "attempt": cmd_attempt, "collect": cmd_collect, "mark": cmd_mark,
            "adjudicate": cmd_adjudicate, "collect-adjudication": cmd_collect_adjudication, "report": cmd_report}
    if not a or a[0] not in cmds: print(__doc__)
    else: cmds[a[0]](a)
