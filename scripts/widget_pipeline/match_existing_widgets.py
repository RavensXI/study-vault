# -*- coding: utf-8 -*-
"""Check a freshly built subject against the interactives we already own.

    python scripts/widget_pipeline/match_existing_widgets.py --subject music-ocr
    python scripts/widget_pipeline/match_existing_widgets.py --subject geography-eduqas --unit fieldwork-enquiry
    python scripts/widget_pipeline/match_existing_widgets.py --subject statistics-edexcel --since 2026-09-01

91 widgets are built (scripts/widget_pipeline/builds/) and 279 lessons carry
one. Most of them are model-driven, not case-study-driven, so a widget written
for one board's lesson usually fits another board's lesson on the same idea
with no code change at all. This script finds those lessons.

It reads Supabase only. It NEVER writes - not to Supabase, not to
js/widget-embed.js. It proposes; Tom approves; a human edits the MAP.

Output, per subject:
    scripts/widget_pipeline/matches/<slug>.json
    scripts/widget_pipeline/matches/<slug>.md

How a candidate is scored
-------------------------
* Subject family must line up. A widget lists the families it was built for
  (`subject_families`) and the families where the same idea is taught
  (`also_fits`). A lesson in neither is not a candidate, full stop - that is
  what keeps the list short enough to read.
* Concept keywords from widget_catalogue.json are looked for in the lesson
  title and description (weight 3), in its <h2>/<h3> headings (weight 2) and
  in the body prose (weight 1). A keyword found only in the body is weak
  evidence: the idea is mentioned, not taught.
* The widget's own `teaches` sentence is word-overlapped with the lesson text
  as a third, smaller signal.
* A lesson that already carries a widget is out of the running - it is listed
  in the report, not proposed again.
* BUILD_GUIDE 0 says roughly one lesson in three or four should carry an
  interactive, because saturation is the failure mode. That quota is enforced
  per unit, not merely warned about: ceil(lessons / 3) minus the ones already
  wired. Everything cut is listed under "Held back", so nothing is hidden.
  `--no-saturation-cap` shows the whole field.

The anchor
----------
js/widget-embed.js inserts the strip BEFORE the heading whose text starts with
`after`, i.e. at the end of the section before it. So this script scores every
section of content_html against the widget, then names the heading that FOLLOWS
the best-matching section - quoted verbatim from content_html, entities
resolved, because that is what the DOM comparison sees. If the best section is
the last one, the anchor is "$end".
"""
import argparse
import collections
import html
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CATALOGUE = os.path.join(HERE, "widget_catalogue.json")
EMBED_JS = os.path.join(REPO, "js", "widget-embed.js")
OUT_DIR = os.path.join(HERE, "matches")

SB = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

# A subject slug maps to exactly one family. FIRST MATCH WINS and a rule fires
# on a prefix or on "-<rule>" anywhere in the slug, so the traps come first:
# "computer-science" and "sport-science" both contain "-science" and must be
# claimed before the science rule. Keep this in step with widget_catalogue.json.
FAMILY_RULES = [
    ("computer-science", "computing"), ("sport-science", "pe"),
    ("music-technology", "music"),
    ("separate-sciences", "science"), ("science", "science"),
    ("astronomy", "astronomy"), ("geology", "geology"),
    ("geography", "geography"), ("history", "history"),
    ("classical-civilisation", "classics"), ("latin", "classics"),
    ("ancient-history", "classics"),
    ("english-literature", "english-literature"),
    ("english-language", "english-language"),
    ("media-studies", "media"), ("film-studies", "film"),
    ("drama", "drama"), ("music", "music"),
    ("cambridge-nationals-enterprise", "business"), ("business", "business"),
    ("economics", "economics"), ("sociology", "sociology"),
    ("psychology", "psychology"), ("religious-studies", "religious-studies"),
    ("citizenship", "citizenship"),
    ("creative-imedia", "creative-media"),
    ("design-technology", "design-engineering"),
    ("engineering", "design-engineering"),
    ("construction", "construction"), ("electronics", "electronics"),
    ("food-preparation", "food"), ("hospitality", "food"),
    ("statistics", "statistics"), ("maths", "maths"),
    ("physical-education", "pe"), ("sport", "pe"),
    ("health-social-care", "health-social-care"),
]

STOP = set(
    "the a an of to in and or is are was were be been being it its this that "
    "with for on as at by from into not no does do did can could will would "
    "has have had more most than then when where which who whom whose why how "
    "they them their there here also so such may might must one two each both "
    "only same other another every all any some out up down over under about "
    "what while because between across through after before during still".split())


# ----------------------------------------------------------------- supabase
def sb_get(path):
    if not SB or not KEY:
        sys.exit("SUPABASE_URL and SUPABASE_SERVICE_KEY (or _ANON_KEY) must be set.")
    req = urllib.request.Request(
        SB + path, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def sb_paged(path):
    rows, off = [], 0
    while True:
        page = sb_get("%s&order=id&limit=500&offset=%d" % (path, off))
        rows += page
        if len(page) < 500:
            return rows
        off += 500


# -------------------------------------------------------------------- text
def family_of(slug):
    for pre, fam in FAMILY_RULES:
        if slug.startswith(pre) or ("-" + pre) in slug:
            return fam
    return None


def strip_tags(s):
    """Body text: tags become spaces, so words never run together."""
    return html.unescape(re.sub(r"<[^>]+>", " ", s or ""))


def heading_text(s):
    """What the browser's textContent would give for a heading.

    placeStrip() compares `after` against heads[i].textContent.trim(), and
    textContent concatenates text nodes with NOTHING between them - so a
    heading written as `Foo<em>bar</em>` reads "Foobar", not "Foo bar". The
    anchor we propose has to be byte-identical to that or the strip silently
    never appears.
    """
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", s or "")).split())


def norm(s):
    """Lower case, entity-free, punctuation flattened to spaces."""
    t = strip_tags(s).lower()
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("—", " ").replace("–", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9'()\-:. ]+", " ", t)).strip()


def words(t):
    return set(w for w in re.findall(r"[a-z']+", norm(t))
               if len(w) > 2 and w not in STOP)


def sections(content_html):
    """[(heading_text, section_body_text)] from h2s, falling back to h3s."""
    for tag in ("h2", "h3"):
        parts = re.split(r"<%s[^>]*>(.*?)</%s>" % (tag, tag),
                         content_html or "", flags=re.S | re.I)
        if len(parts) > 1:
            out = []
            for i in range(1, len(parts), 2):
                head = heading_text(parts[i])
                body = strip_tags(parts[i + 1] if i + 1 < len(parts) else "")
                out.append((head, body))
            return out
    return []


def anchor_problems(anchor, headings):
    """Would js/widget-embed.js really land the strip on this heading?"""
    if anchor == "$end":
        return []
    out = []
    if anchor not in headings:
        out.append("anchor is not a heading in this lesson")
        return out
    first = next(h for h in headings if h.startswith(anchor))
    if first != anchor:
        out.append("ambiguous: the earlier heading %r also starts with this "
                   "text, and placeStrip takes the first match" % first)
    return out


# ------------------------------------------------------------------ the MAP
def read_map():
    """{lesson_key: [widget_file, ...]} parsed out of js/widget-embed.js."""
    src = io.open(EMBED_JS, encoding="utf-8").read()
    start = src.index("var MAP = {")
    depth, end = 0, None
    i = src.index("{", start)
    body_start = i
    while i < len(src):
        c = src[i]
        if c == '"':
            i += 1
            while i < len(src) and src[i] != '"':
                i += 2 if src[i] == "\\" else 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    body = src[body_start:end + 1]
    out = collections.defaultdict(list)
    key = None
    for line in body.splitlines():
        m = re.match(r'\s*"([^"]+/[^"]+/\d+)"\s*:', line)
        if m:
            key = m.group(1)
            continue
        m = re.search(r'\bfile:\s*"([^"]+)"', line)
        if m and key:
            out[key].append(m.group(1))
    return dict(out)


# ---------------------------------------------------------------- scoring
def keyword_hits(kws, hay_title, hay_heads, hay_body):
    """{keyword: ('title'|'heading'|'body')} for every keyword present."""
    hits = {}
    for kw in kws:
        k = norm(kw)
        if not k:
            continue
        where = None
        if k in hay_title:
            where = "title"
        elif k in hay_heads:
            where = "heading"
        elif k in hay_body:
            where = "body"
        if where:
            hits[kw] = where
    return hits


WEIGHT = {"title": 3.0, "heading": 2.0, "body": 1.0}


def score_pair(w, lesson):
    fam = lesson["family"]
    if fam in w["subject_families"]:
        fam_w, fam_why = 1.0, "built for %s" % "/".join(w["subject_families"])
    elif fam in (w.get("also_fits") or []):
        fam_w, fam_why = 0.72, "same idea is taught in %s" % fam
    else:
        return None

    hits = keyword_hits(w["concept_keywords"], lesson["hay_title"],
                        lesson["hay_heads"], lesson["hay_body"])
    if not hits:
        return None
    raw = sum(WEIGHT[v] for v in hits.values())
    coverage = len(hits) / float(len(w["concept_keywords"]))
    probe = words(w["teaches"] or "") | words(w["targets"] or "")
    overlap = (len(probe & lesson["body_words"]) / float(len(probe))
               if probe else 0.0)
    anchored = any(v in ("title", "heading") for v in hits.values())

    score = fam_w * (0.55 * min(1.0, raw / 9.0)
                     + 0.30 * min(1.0, coverage * 3.0)
                     + 0.15 * min(1.0, overlap * 1.4))
    if not anchored:
        score *= 0.55            # mentioned in passing, not taught here
    return {"score": round(score, 3), "hits": hits, "raw": raw,
            "coverage": round(coverage, 3), "teach_overlap": round(overlap, 3),
            "anchored": anchored, "family_why": fam_why, "family_weight": fam_w}


def pick_anchor(w, secs):
    """Best section for this widget -> the heading AFTER it, verbatim."""
    if not secs:
        # no h2 or h3 to anchor on; placeStrip appends after the last section
        return "$end", None, 0.0
    probe = (words(w["teaches"] or "") | words(w["targets"] or "")
             | set(x for kw in w["concept_keywords"] for x in words(kw)))
    best, bscore = 0, -1.0
    for idx, (head, body) in enumerate(secs):
        bw = words(head + " " + body)
        sc = len(probe & bw) / float(max(1, len(probe)))
        if sc > bscore:
            best, bscore = idx, sc
    matched = secs[best][0]
    anchor = secs[best + 1][0] if best + 1 < len(secs) else "$end"
    return anchor, matched, round(bscore, 3)


BAND_RANK = {"high": 0, "medium": 1, "low": 2}


def band(score, anchored):
    if score >= 0.62 and anchored:
        return "high"
    if score >= 0.45 and anchored:
        return "medium"
    if score >= 0.30:
        return "low"
    return None


# ------------------------------------------------------------------- report
def why_line(w, res, anchor_score):
    kw = sorted(res["hits"].items(),
                key=lambda kv: (-WEIGHT[kv[1]], kv[0]))[:6]
    bits = ", ".join("%s (%s)" % (k, v) for k, v in kw)
    return ("%s; keywords matched: %s; section overlap %.2f"
            % (res["family_why"], bits, anchor_score))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subject", required=True,
                    help="subject slug, e.g. music-ocr")
    ap.add_argument("--unit", action="append", default=[],
                    help="restrict to this unit slug (repeatable)")
    ap.add_argument("--since", default=None,
                    help="only lessons created on/after this date (YYYY-MM-DD)")
    ap.add_argument("--status", default="live,pending_review",
                    help="comma list of lesson statuses (default "
                         "live,pending_review)")
    ap.add_argument("--top", type=int, default=25,
                    help="candidates written to the report (default 25)")
    ap.add_argument("--per-lesson", type=int, default=1,
                    help="most candidates kept for one lesson (default 1)")
    ap.add_argument("--per-widget", type=int, default=2,
                    help="most lessons in this subject that may take the SAME "
                         "widget (default 2). The live MAP never puts one "
                         "widget in more than 3 lessons of a subject, and only "
                         "twice at that - meeting the same interactive over "
                         "and over is how it becomes furniture.")
    ap.add_argument("--min-score", type=float, default=0.30)
    ap.add_argument("--school-id", default=None,
                    help="needed only for the three slugs that exist twice "
                         "(separate-sciences, computer-science, "
                         "design-technology). Pass '' for the free-tier copy "
                         "or the school's uuid for theirs - generic and school "
                         "content never mix.")
    ap.add_argument("--no-saturation-cap", action="store_true",
                    help="show every candidate above the threshold instead of "
                         "holding a unit to the one-in-three rhythm "
                         "(BUILD_GUIDE 0). Useful when you want to see the "
                         "whole field before choosing.")
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--write-refine-batch", metavar="PATH", default=None,
                    help="write an Anthropic Batch API .jsonl that would ask "
                         "a model to sift the shortlist. Writes the file and "
                         "stops - it never calls the API.")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    cat = json.load(io.open(CATALOGUE, encoding="utf-8"))
    widgets = cat["widgets"]
    wired = read_map()

    slug = args.subject
    fam = family_of(slug)
    if not fam:
        sys.exit("No family rule matches %r - add one to FAMILY_RULES." % slug)

    subs = sb_get("/rest/v1/subjects?select=id,slug,name,school_id&slug=eq."
                  + urllib.parse.quote(slug))
    if not subs:
        sys.exit("No subject with slug %r." % slug)
    # Three slugs exist twice - once free tier, once Unity (separate-sciences,
    # computer-science, design-technology). Generic and school content never
    # mix, so the tier is chosen explicitly and never guessed.
    if len(subs) > 1:
        want_school = args.school_id
        picked = [s for s in subs
                  if (s["school_id"] or "") == (want_school or "")]
        if len(picked) != 1:
            sys.exit("%r exists %d times (school_id: %s). Re-run with "
                     "--school-id <uuid> for a school's copy, or "
                     "--school-id '' for the free tier."
                     % (slug, len(subs),
                        ", ".join(str(s["school_id"]) for s in subs)))
        subject = picked[0]
        print("note: %r exists in more than one tier; using school_id=%s"
              % (slug, subject["school_id"]))
    else:
        subject = subs[0]
        if args.school_id and (subject["school_id"] or "") != args.school_id:
            sys.exit("%r belongs to school_id=%s, not %s."
                     % (slug, subject["school_id"], args.school_id))
    units = sb_paged("/rest/v1/units?select=id,slug,name,sort_order"
                     "&subject_id=eq." + subject["id"])
    if args.unit:
        units = [u for u in units if u["slug"] in args.unit]
        if not units:
            sys.exit("No unit in %s matches %s" % (slug, args.unit))
    by_unit = {u["id"]: u for u in units}

    statuses = [s.strip() for s in args.status.split(",") if s.strip()]
    lessons = []
    for uid in by_unit:
        q = ("/rest/v1/lessons?select=id,unit_id,title,description,content_html,"
             "status,lesson_number,is_listening,created_at&unit_id=eq." + uid)
        q += "&status=in.(%s)" % ",".join(statuses)
        if args.since:
            q += "&created_at=gte." + args.since
        lessons += sb_paged(q)

    prepared, skipped = [], collections.Counter()
    for r in lessons:
        if r.get("is_listening"):
            skipped["listening lessons"] += 1
            continue
        if len(strip_tags(r.get("content_html") or "")) < 400:
            skipped["no article content (practice format or stub)"] += 1
            continue
        prepared.append(r)

    items = []
    for r in prepared:
        u = by_unit.get(r["unit_id"])
        if not u:
            continue
        ch = r["content_html"]
        secs = sections(ch)
        heads = " || ".join(h for h, _ in secs)
        body = strip_tags(ch)
        key = "%s/%s/%s" % (slug, u["slug"], r["lesson_number"])
        items.append({
            "key": key, "lesson_id": r["id"], "title": r["title"],
            "unit": u["slug"], "unit_title": u.get("name"),
            "n": r["lesson_number"], "status": r["status"],
            "family": fam, "headings": [h for h, _ in secs],
            "sections": secs,
            "hay_title": norm((r["title"] or "") + " " + (r.get("description") or "")),
            "hay_heads": norm(heads),
            "hay_body": norm(body),
            "body_words": words(body),
            "already": wired.get(key, []),
        })

    cands = []
    for it in items:
        if it["already"]:
            continue          # this lesson already carries an interactive
        for w in widgets:
            res = score_pair(w, it)
            if not res:
                continue
            anchor, matched, asc = pick_anchor(w, it["sections"])
            b = band(res["score"], res["anchored"])
            if not b or res["score"] < args.min_score:
                continue
            cands.append({
                "widget": w["file"], "widget_name": w["name"],
                "lesson_key": it["key"], "lesson_title": it["title"],
                "unit": it["unit"], "lesson_number": it["n"],
                "status": it["status"],
                "anchor": anchor, "anchor_is_end": anchor == "$end",
                "anchor_problems": anchor_problems(anchor, it["headings"]),
                "matched_section": matched, "section_overlap": asc,
                "confidence": b, "score": res["score"],
                "keywords_matched": res["hits"],
                "teach_overlap": res["teach_overlap"],
                "reuse": w["reuse"], "reuse_note": w.get("reuse_note"),
                "needs_data_variant": w["reuse"] != "portable",
                "variant_implemented": w["variant_implemented"],
                "targets": w["targets"],
                "lesson_already_has": it["already"],
                "why": why_line(w, res, asc),
                "wired_elsewhere": [x["key"] for x in w["wired_lessons"]],
            })

    cands.sort(key=lambda c: (BAND_RANK[c["confidence"]], -c["score"]))

    # BUILD_GUIDE 0: roughly one lesson in three or four carries a widget.
    # Saturation is the failure mode, so the quota is enforced, not warned
    # about: a unit gets ceil(lessons / 3) interactives, minus the ones it
    # already carries. Everything cut is listed as "held back".
    unit_total = collections.Counter(it["unit"] for it in items)
    unit_have = collections.Counter(it["unit"] for it in items if it["already"])
    quota = {}
    for u in units:
        s = u["slug"]
        allowed = max(1, -(-unit_total[s] // 3)) if unit_total[s] else 0
        quota[s] = max(0, allowed - unit_have[s])

    # a widget already wired into this subject counts against its own cap
    per_widget = collections.Counter()
    for k, files in wired.items():
        if k.split("/")[0] == slug:
            for f in files:
                per_widget[f] += 1

    kept, held = [], []
    per_lesson, per_unit = collections.Counter(), collections.Counter()
    for c in cands:
        reason = None
        if per_lesson[c["lesson_key"]] >= args.per_lesson:
            reason = "this lesson already has a stronger candidate"
        elif per_widget[c["widget"]] >= args.per_widget:
            reason = ("%s is already proposed or wired %d times in this "
                      "subject - the same interactive twice is the limit"
                      % (c["widget"], per_widget[c["widget"]]))
        elif not args.no_saturation_cap and per_unit[c["unit"]] >= quota[c["unit"]]:
            reason = ("unit quota reached - %s has %d lessons, %d already "
                      "wired, so %d more interactive(s)"
                      % (c["unit"], unit_total[c["unit"]],
                         unit_have[c["unit"]], quota[c["unit"]]))
        elif len(kept) >= args.top:
            reason = "past --top"
        if reason:
            held.append({"widget": c["widget"], "lesson_key": c["lesson_key"],
                         "confidence": c["confidence"], "score": c["score"],
                         "anchor": c["anchor"], "held_because": reason})
            continue
        kept.append(c)
        per_lesson[c["lesson_key"]] += 1
        per_unit[c["unit"]] += 1
        per_widget[c["widget"]] += 1

    warn = []
    for u in units:
        s = u["slug"]
        allowed = max(1, -(-unit_total[s] // 3)) if unit_total[s] else 0
        if unit_total[s] and (unit_have[s] + per_unit[s]) > allowed:
            warn.append("%s: %d lessons, %d already wired, %d proposed - over "
                        "the one-in-three rhythm in BUILD_GUIDE 0."
                        % (s, unit_total[s], unit_have[s], per_unit[s]))

    os.makedirs(args.out_dir, exist_ok=True)
    payload = {
        "subject": slug, "subject_name": subject["name"], "family": fam,
        "units": [u["slug"] for u in units],
        "filters": {"status": statuses, "since": args.since,
                    "unit": args.unit or None},
        "lessons_considered": len(items),
        "lessons_skipped": dict(skipped),
        "lessons_already_wired": sorted(it["key"] for it in items if it["already"]),
        "candidates": kept,
        "candidates_before_cap": len(cands),
        "held_back": held,
        "unit_quota": {u["slug"]: quota[u["slug"]] for u in units},
        "saturation_warnings": warn,
    }
    jp = os.path.join(args.out_dir, slug + ".json")
    io.open(jp, "w", encoding="utf-8").write(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n")

    io.open(os.path.join(args.out_dir, slug + ".md"), "w",
            encoding="utf-8").write(render_md(payload, cat))

    print("%s: %d lessons considered, %d candidates (%d kept)"
          % (slug, len(items), len(cands), len(kept)))
    for c in kept[:10]:
        print("  %-8s %.2f  %-46s %-38s after: %s"
              % (c["confidence"], c["score"], c["widget"], c["lesson_key"],
                 c["anchor"]))
    for w in warn:
        print("  ! " + w)

    if args.write_refine_batch:
        write_refine_batch(args.write_refine_batch, payload)
        print("  wrote Batch API requests to %s - NOT submitted."
              % args.write_refine_batch)


def render_md(p, cat):
    L = []
    A = L.append
    A("# Widget reuse candidates - %s (%s)" % (p["subject"], p["subject_name"]))
    A("")
    A("Generated by `scripts/widget_pipeline/match_existing_widgets.py`. "
      "Nothing here is wired. Tom approves, then a human edits the MAP in "
      "`js/widget-embed.js`.")
    A("")
    A("- family: **%s**  |  units: %s" % (p["family"], ", ".join(p["units"])))
    A("- filters: status %s, since %s" % (", ".join(p["filters"]["status"]),
                                          p["filters"]["since"] or "(none)"))
    A("- lessons considered: **%d**  (skipped: %s)"
      % (p["lessons_considered"],
         ", ".join("%s %d" % (k, v) for k, v in p["lessons_skipped"].items())
         or "none"))
    if p["lessons_already_wired"]:
        A("- already carry a widget: %s"
          % ", ".join("`%s`" % k for k in p["lessons_already_wired"]))
    A("- candidates above the threshold: **%d**, proposed after the "
      "one-in-three cap: **%d**"
      % (p["candidates_before_cap"], len(p["candidates"])))
    A("- interactives a unit may still take: %s"
      % ", ".join("`%s` %d" % (k, v) for k, v in sorted(p["unit_quota"].items())))
    A("")
    if p["saturation_warnings"]:
        A("> **Saturation check** - " + "  ".join(p["saturation_warnings"]))
        A("")
    if not p["candidates"]:
        A("No candidate cleared the bar. Nothing in the fleet fits this "
          "subject well enough to propose.")
        A("")
        return "\n".join(L) + "\n"

    by_file = {w["file"]: w for w in cat["widgets"]}
    for c in p["candidates"]:
        w = by_file[c["widget"]]
        A("## %s -> `%s`" % (c["widget"], c["lesson_key"]))
        A("")
        A("**%s** - %s" % (c["widget_name"], c["targets"]))
        A("")
        A("| | |")
        A("|---|---|")
        A("| lesson | %s (unit `%s`, lesson %s, %s) |"
          % (c["lesson_title"], c["unit"], c["lesson_number"], c["status"]))
        A("| confidence | **%s** (%.2f) |" % (c["confidence"], c["score"]))
        A("| anchor (`after:`) | %s |"
          % ("`$end` - append after the final section" if c["anchor_is_end"]
             else '`"%s"` - quoted verbatim from this lesson%s'
                  % (c["anchor"],
                     "" if not c["anchor_problems"]
                     else " (**check**: " + "; ".join(c["anchor_problems"]) + ")")))
        A("| best-matching section | %s (overlap %.2f) |"
          % (c["matched_section"] or "-", c["section_overlap"]))
        A("| why | %s |" % c["why"])
        A("| data variant | %s |"
          % ("**NEEDED** - %s" % (c["reuse_note"] or c["reuse"])
             if c["needs_data_variant"] else "not needed - drops in as built"))
        A("| already wired to | %s |"
          % (", ".join("`%s`" % k for k in c["wired_elsewhere"]) or "nothing"))
        if c["lesson_already_has"]:
            A("| note | this lesson already carries %s |"
              % ", ".join("`%s`" % x for x in c["lesson_already_has"]))
        A("")
        A("```js")
        A('    "%s": {' % c["lesson_key"])
        A('      file: "%s",' % c["widget"])
        A('      label: %s,' % json.dumps(_label_of(w, "label"),
                                          ensure_ascii=False))
        A('      line: %s,' % json.dumps(_label_of(w, "line"),
                                         ensure_ascii=False))
        A('      after: %s' % json.dumps(c["anchor"], ensure_ascii=False))
        A("    },")
        A("```")
        A("")
    if p["held_back"]:
        A("## Held back")
        A("")
        A("Above the threshold but not proposed - kept here so nothing is "
          "hidden.")
        A("")
        A("| widget | lesson | conf | why it was held |")
        A("|---|---|---|---|")
        for h in p["held_back"]:
            A("| `%s` | `%s` | %s (%.2f) | %s |"
              % (h["widget"], h["lesson_key"], h["confidence"], h["score"],
                 h["held_because"]))
        A("")
    return "\n".join(L) + "\n"


_LABELS = {}


def _label_of(w, field):
    """The label/line this widget already uses in the MAP (one pair each)."""
    if not _LABELS:
        src = io.open(EMBED_JS, encoding="utf-8").read()
        for m in re.finditer(
                r'file:\s*"([^"]+)",\s*\n\s*label:\s*"((?:[^"\\]|\\.)*)",\s*\n'
                r'\s*line:\s*"((?:[^"\\]|\\.)*)"', src):
            _LABELS.setdefault(m.group(1), {"label": m.group(2),
                                            "line": m.group(3)})
    return _LABELS.get(w["file"], {}).get(field, "TODO - write this copy")


def write_refine_batch(path, payload):
    """Optional: an Anthropic Batch API file that would sift the shortlist.

    Off by default and never submitted from here. Submit it yourself only if
    the keyword pass leaves too much to read, and remember the house rule:
    the Batch API, never the sync API. The model id matches the one the build
    driver uses (scripts/api_build/driver.py MODEL_CONTENT); Sonnet 5 runs
    adaptive thinking, which bills against max_tokens, so keep the budget
    generous if you ever raise the prompt.
    """
    reqs = []
    for i, c in enumerate(payload["candidates"]):
        prompt = (
            "You judge whether an existing GCSE revision interactive fits a "
            "lesson it was not built for.\n\n"
            "Widget: %s\nIt exists to falsify this misconception: %s\n\n"
            "Lesson: %s (%s)\nProposed anchor heading: %s\n\n"
            "Answer in JSON: {\"fits\": true|false, \"confidence\": "
            "\"high\"|\"medium\"|\"low\", \"reason\": \"one sentence\"}. "
            "Say false unless the lesson genuinely teaches the same idea."
            % (c["widget"], c["targets"], c["lesson_title"], c["lesson_key"],
               c["anchor"]))
        reqs.append({
            "custom_id": "cand-%03d" % i,
            "params": {"model": "claude-sonnet-5",
                       "max_tokens": 2000,
                       "messages": [{"role": "user", "content": prompt}]},
        })
    io.open(path, "w", encoding="utf-8").write(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in reqs) + "\n")


if __name__ == "__main__":
    main()
