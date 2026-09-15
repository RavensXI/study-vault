# -*- coding: utf-8 -*-
"""Guide pages for Eduqas GCSE Media Studies (C680QS).

Revision-technique guides adapted from the AQA Media set (pedagogy text
passes through; examples that lean on AQA Close Study Products are replaced
with the Eduqas set products; the index passes through with the links
re-pointed). Exam-technique guides are NOT built: retired in the spring
pipeline rebuild (see docs/PIPELINE.md, "Exam technique guides are not
generated").

Usage:
  python scripts/api_build/media_eduqas_guides.py submit
  python scripts/api_build/media_eduqas_guides.py poll      # collect, check, insert
"""
import io, json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
_s = importlib.util.spec_from_file_location("drv", os.path.join(HERE, "driver.py")); D = importlib.util.module_from_spec(_s); _s.loader.exec_module(D)
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

SP = r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault\88006801-843c-4d74-957a-5eebdef537b9\scratchpad\media_eduqas"
cfg = {"run_dir": os.path.join(SP, "run_guides")}; os.makedirs(cfg["run_dir"], exist_ok=True)
SUBJECT_ID = "4c765fb9-2a67-4414-9bcc-cf2acd581b0e"
SLUG = "media-studies-eduqas"; SRC_SLUG = "media-studies-aqa"
SPEC = os.path.join(REPO, "specs", "eduqas", "media-studies-C680QS.md")

SET_PRODUCTS = """Set products for assessment from 2027 (Component 1 Section A, media language and representation): magazine front covers Vogue (July 2021) and GQ (August 2019); film posters The Man with the Golden Gun (1974) and No Time to Die (2021); newspaper front pages The Guardian (18 January 2022) and The Sun (1 January 2021) for 2027, changing to The Guardian (6 May 2025) and The Sun (22 March 2025) from 2028; print advertisements Quality Street (1956) and NHS 111 (2023).
Component 1 Section B (industries and audiences): The Sun (newspapers), Desert Island Discs (radio), No Time to Die (film, industries only), Fortnite (video games).
Component 2 Section A (television): Trigger Point (crime drama, with The Sweeney) and one sitcom option: Man Like Mobeen or Modern Family (each with Friends).
Component 2 Section B (music): contemporary music videos Lizzo, Taylor Swift, Stormzy, Justin Bieber options; music video from the past Duran Duran or TLC; and the artists' online, social and participatory media.
Never name the exam board in student-facing text: say 'the exam board'."""

RULES = ("You write for StudyVault, a GCSE revision site. Audience: students aged 15-16. Plain English, short sentences, British spelling. "
         "Output HTML fragments only (no <html>, <head> or <body>), using named entities for special characters (&mdash; &rsquo; etc.). "
         "Never name an exam board (no AQA, Eduqas, WJEC, Pearson, OCR): write 'the exam board'. Never mention Close Study Products or CSPs; "
         "this qualification calls them set products. No coloured left-border stripes. No non-exam assessment content.")


def spec_assessment():
    md = io.open(SPEC, encoding="utf-8").read()
    i = md.find("Component 1: Exploring the Media\nWritten examination"); j = md.find("Non-exam assessment", i)
    summary = md[i:j] if i >= 0 and j > i else md[:6000]
    # the question-by-question descriptions sit at the end of each component's content chapter
    lines = md.split("\n")
    def block(start_pat, span):
        for n, l in enumerate(lines):
            if start_pat in l: return "\n".join(lines[max(0, n - 6):n + span])
        return ""
    c1 = block("Question 1 (15 marks)", 45)
    c2 = block("Question 1 (20 marks)", 45)
    ao = block("3.1  Assessment objectives and weightings", 60) if md.count("3.1  Assessment objectives") else ""
    return summary + "\n\nCOMPONENT 1 QUESTIONS:\n" + c1 + "\n\nCOMPONENT 2 QUESTIONS:\n" + c2 + "\n\nASSESSMENT OBJECTIVES:\n" + ao[-6000:]


def submit():
    cl = D.client(); reqs = []
    src = D.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id" % SRC_SLUG)[0]["id"]
    guides = D.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type,title,sort_order,content_html&order=sort_order" % src)
    passthrough = {}
    for g in guides:
        html = g["content_html"].replace("/guide/%s/" % SRC_SLUG, "/guide/%s/" % SLUG)
        if g["slug"] == "index":
            passthrough[g["slug"]] = dict(g, content_html=html); continue
        user = ("Adapt this revision-technique guide from one GCSE Media Studies course to another. The pedagogy text stays as it is. "
                "Replace every example, worked illustration or reference that relies on the source course's Close Study Products (CSPs) with the "
                "set products below, keeping the same teaching point. Keep the HTML structure, classes and length. Remove the words 'Close Study Product' and 'CSP' everywhere.\n\n"
                + SET_PRODUCTS + "\n\nGUIDE HTML:\n" + html + "\n\nReturn ONLY the adapted HTML fragment.")
        reqs.append({"custom_id": "rt-" + g["slug"], "params": {"model": D.MODEL_CONTENT, "max_tokens": 16000, "thinking": {"type": "disabled"},
                                                                  "system": [{"type": "text", "text": RULES}], "messages": [{"role": "user", "content": user}]}})
    # NOTE 15 Sep 2026: an exam-technique set was built here and then DELETED the same night.
    # Exam-technique guides were retired in the spring pipeline rebuild (copyright-adjacent: they
    # encode mark-scheme structure); per-lesson exam_tip_html and practice mark schemes carry that
    # load. Do not add them back. Revision-technique adaptation only.
    b = cl.messages.batches.create(requests=reqs)
    st = D.load_state(cfg); st["guides_batch_id"] = b.id; st["passthrough"] = passthrough; D.save_state(cfg, st)
    print("submitted", b.id, len(reqs), "requests")


BAD = re.compile(r"\b(AQA|Eduqas|WJEC|Pearson|OCR|Close Study Product|CSP)s?\b")


def strip_fence(t):
    t = t.strip(); t = re.sub(r"^```(?:html|json)?\s*|\s*```$", "", t); return t.strip()


def poll():
    st = D.load_state(cfg)
    out = D.collect_batch(cfg, st["guides_batch_id"], "guides", "raw_guides")
    if out is None: return
    texts, errors = out
    rows = []; problems = []
    src = D.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id" % SRC_SLUG)[0]["id"]
    meta = {g["slug"]: g for g in D.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=slug,guide_type,title,sort_order" % src)}
    for slug, g in st["passthrough"].items():
        html = g["content_html"]
        if BAD.search(re.sub(r"<[^>]+>", " ", html)): problems.append("index passthrough names a board/CSP")
        rows.append({"subject_id": SUBJECT_ID, "guide_type": g["guide_type"], "slug": slug, "title": g["title"], "sort_order": g["sort_order"], "content_html": html})
    for cid, text in texts.items():
        if cid.startswith("rt-"):
            slug = cid[3:]; html = strip_fence(text)
            if not html.startswith("<"): problems.append(cid + ": not html"); continue
            if BAD.search(re.sub(r"<[^>]+>", " ", html)): problems.append(cid + ": names a board/CSP")
            m = meta[slug]; rows.append({"subject_id": SUBJECT_ID, "guide_type": m["guide_type"], "slug": slug, "title": m["title"], "sort_order": m["sort_order"], "content_html": html})
        else:
            try: obj = json.loads(strip_fence(text))
            except Exception as e: problems.append("exam-set: json " + str(e)[:80]); continue
            pages = obj.get("pages") or []
            if not (5 <= len(pages) <= 8): problems.append("exam-set: %d pages" % len(pages))
            allhtml = obj.get("index_html", "") + "".join(p.get("content_html", "") for p in pages)
            if BAD.search(re.sub(r"<[^>]+>", " ", allhtml)): problems.append("exam-set: names a board/CSP")
            rows.append({"subject_id": SUBJECT_ID, "guide_type": "exam-technique", "slug": "index", "title": "Exam Technique", "sort_order": 0, "content_html": obj.get("index_html", "")})
            for i, p in enumerate(pages):
                if not re.match(r"^[a-z0-9-]+$", p.get("slug", "")): problems.append("exam-set: bad slug %r" % p.get("slug"))
                rows.append({"subject_id": SUBJECT_ID, "guide_type": "exam-technique", "slug": p["slug"], "title": p["title"], "sort_order": p.get("sort_order", i + 1), "content_html": p["content_html"]})
            hrefs = set(re.findall(r'href="([a-z0-9-]+)\.html"', obj.get("index_html", "")))
            if hrefs != set(p["slug"] for p in pages): problems.append("exam-set: index links %s != pages %s" % (sorted(hrefs), sorted(p["slug"] for p in pages)))
    D.write_json(os.path.join(cfg["run_dir"], "rows.json"), rows)
    print("rows ready:", len(rows), "| errors:", errors, "| problems:", problems)
    if problems or errors: print("NOT inserted; fix and rerun poll"); return
    existing = D.supa(cfg, "GET", "/rest/v1/guide_pages?subject_id=eq.%s&select=id" % SUBJECT_ID)
    if existing: print("subject already has %d guide rows; not inserting" % len(existing)); return
    D.supa(cfg, "POST", "/rest/v1/guide_pages", rows, prefer="return=minimal")
    print("inserted", len(rows), "guide pages for", SLUG)


if __name__ == "__main__":
    {"submit": submit, "poll": poll}[sys.argv[1]]()
