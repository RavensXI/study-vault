"""End-to-end gate for practice lessons: the REAL page marks the STORED answer.

The structural validator (_qa_practice_data.py) checks the JSON. This checks
the contract between the JSON and practice.html, which is where the fraction
bug lived: the validator blessed {numerator, denominator}, the page's checker
only read [num, den], and every fraction answer in Statistics was marked wrong
for weeks. Reading JSON cannot find that; submitting the answer can.

For every problem in every tier it renders the problem on the real page,
fills the boxes from the stored solution, presses Check Answer and requires
"Correct". It also fails on any "[object Object]", "undefined" or "NaN" in the
question or feedback, and on a question that shows two pictures (an inline
SVG and a chart panel).

Usage:
  python scripts/_qa_practice_e2e.py --subject statistics-aqa [--subject ...]
  python scripts/_qa_practice_e2e.py --url /practice/statistics-aqa/representing-data/2
Needs a local server (default http://127.0.0.1:8907) and installed Chrome.
Exit 1 if any problem fails. Report: scripts/_qa_practice_e2e_report.md
"""
import io, json, os, sys, time
import requests
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("SV_E2E_BASE", "http://127.0.0.1:8907")
H = {"apikey": os.environ["SUPABASE_SERVICE_KEY"], "Authorization": "Bearer " + os.environ["SUPABASE_SERVICE_KEY"]}
U = os.environ["SUPABASE_URL"]
SKIP_TYPES = {"traffic_light", "highlight_evidence", "connotation_picker", "evidence_match", "ai_mark", "misleading_summary",
              "ai_write", "improve_sentence", "spot_error", "reorder", "vocab_match", "gap_fill", "translate", "dictation",
              "sentence_builder", "spot_correct", "role_play"}


def sb(path):
    r = requests.get(U + "/rest/v1/" + path, headers=H); r.raise_for_status(); return r.json()


def lesson_urls(slug):
    sid = sb("subjects?select=id&slug=eq.%s" % slug)[0]["id"]
    units = {u["id"]: u["slug"] for u in sb("units?select=id,slug&subject_id=eq.%s" % sid)}
    rows = sb("lessons?select=unit_id,lesson_number,practice_data&practice_data=not.is.null&status=in.(live,pending_review)&unit_id=in.(%s)" % ",".join(units))
    # article lessons also carry practice_data (their six questions); only a problem_bank is a practice page
    rows = [r for r in rows if isinstance(r["practice_data"], dict) and r["practice_data"].get("problem_bank")]
    return sorted("/practice/%s/%s/%d" % (slug, units[r["unit_id"]], r["lesson_number"]) for r in rows), sid


# Runs inside the page: render problem (tier, idx), fill from its own stored
# solution, press Check, return what the student would see.
JS_ONE = r"""
([tier, idx]) => {
  const p = window._problemBank[tier][idx];
  const t = p.input_type || 'single_value';
  practiceState.completionShown = practiceState.completionShown || {};
  practiceState.completionShown[tier] = true;      // no guided card in the way
  practiceState.currentTier = tier; practiceState.currentIndex = idx;
  try { hideGuided(); } catch (e) {}
  renderCurrentProblem();
  const out = { type: t, sol: JSON.stringify(p.solutions).slice(0, 60), result: '', text: '', problems: [] };
  const q = document.getElementById('problem-display') || document.querySelector('.problem-display') || document.body;
  const qtext = (document.getElementById('problem-inputs-area') || q).parentElement.textContent;
  if (/\[object Object\]|undefined|NaN/.test(qtext)) out.problems.push('bad text in question');
  // two pictures = the question draws its own SVG AND the page draws a chart
  // panel for it (the body carries icon SVGs, so test the problem, not the DOM)
  const canvas = document.getElementById('panel-chart-canvas');
  if (/<svg/.test(p.display || '') && p.chart && canvas && canvas.offsetParent !== null) out.problems.push('two pictures');
  const sol = p.solutions || [];
  const set = (id, v) => { const el = document.getElementById(id); if (!el) { out.problems.push('missing box ' + id); return; } el.value = String(v); };
  if (t === 'multiple_choice') {
    const b = document.querySelector('.mc-option[data-idx="' + sol[0] + '"]'); if (!b) { out.problems.push('missing option'); return out; } b.click();
  } else if (t === 'fraction') {
    const s = sol[0]; const n = (s && typeof s === 'object') ? s.numerator : sol[0]; const d = (s && typeof s === 'object') ? s.denominator : sol[1];
    set('problem-input-num', n); set('problem-input-den', d);
  } else if (t === 'xy_pair' || t === 'two_solutions') {
    set('problem-input-a', sol[0]); set('problem-input-b', sol[1]);
  } else if (t === 'standard_form') {
    const s = sol[0]; const a = (s && typeof s === 'object') ? s.a : sol[0]; const n = (s && typeof s === 'object') ? s.n : sol[1];
    set('problem-input-sf-a', a); set('problem-input-sf-n', n);
  } else {
    set('problem-input-a', sol[0]);
  }
  if (out.problems.some(x => x.startsWith('missing'))) return out;
  const btn = document.getElementById('problem-check-btn'); if (!btn) { out.problems.push('no check button'); return out; }
  btn.click();
  const fb = document.querySelector('.feedback-box');
  out.result = fb ? (fb.classList.contains('feedback-correct') ? 'correct' : 'wrong') : 'no feedback';
  out.text = fb ? fb.textContent.replace(/\s+/g, ' ').trim().slice(0, 160) : '';
  if (/\[object Object\]|undefined|NaN/.test(out.text)) out.problems.push('bad text in feedback');
  if (out.result !== 'correct') out.problems.push('stored answer marked ' + out.result);
  return out;
}
"""


def run(urls, sid=None):
    fails, total, skipped = [], 0, 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.add_init_script("localStorage.setItem('sv-lesson-tour-v2','1'); sessionStorage.setItem('studyvault-auth', JSON.stringify({role:'admin',email:'qa'}))")
        for url in urls:
            full = BASE + url + ("?sid=" + sid if sid else "")
            pg.goto(full)
            try:
                pg.wait_for_function("() => window._problemBank && window.practiceState", timeout=20000)
            except Exception:
                fails.append((url, "-", "-", "bank never loaded")); continue
            bank = pg.evaluate("() => Object.fromEntries(Object.entries(window._problemBank).map(([k,v]) => [k, v.map(p => p.input_type || 'single_value')]))")
            for tier, types in bank.items():
                for idx, t in enumerate(types):
                    if t in SKIP_TYPES: skipped += 1; continue
                    total += 1
                    try:
                        r = pg.evaluate(JS_ONE, [tier, idx])
                    except Exception as e:
                        fails.append((url, tier, idx, "page error: " + str(e)[:100])); continue
                    if r["problems"]:
                        fails.append((url, tier, idx, "%s | %s | %s | %s" % (r["type"], r["sol"], "; ".join(r["problems"]), r["text"][:110])))
            if errs:
                fails.append((url, "-", "-", "console errors: " + " / ".join(errs[:3]))); errs.clear()
            print("%-60s %s" % (url, "ok" if not any(f[0] == url for f in fails) else "FAIL"))
        b.close()
    lines = ["# Practice end-to-end report", "", "checked %d problems (%d skipped English/MFL types); %d failures" % (total, skipped, len(fails)), ""]
    for f in fails: lines.append("- `%s` %s[%s]: %s" % f)
    io.open(os.path.join(HERE, "_qa_practice_e2e_report.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[2:]))
    return 1 if fails else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    urls, sid = [], None
    i = 0
    while i < len(args):
        if args[i] == "--subject":
            u, s = lesson_urls(args[i + 1]); urls += u; sid = sid or s; i += 2
        elif args[i] == "--url":
            urls.append(args[i + 1]); i += 2
        else:
            i += 1
    if not urls: print(__doc__); sys.exit(2)
    sys.exit(run(urls, sid))
