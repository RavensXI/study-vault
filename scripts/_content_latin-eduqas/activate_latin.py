# -*- coding: utf-8 -*-
"""Phase 2 activation for GCSE Latin (Eduqas / WJEC), free tier.

Creates the subject row, the eight unit rows and the 33 lesson shells, writes
the quote ticker and the practice-unit list into subjects.settings, appends the
per-unit accent CSS, and wires the subject into every homepage/wizard map that
must move in lockstep (slugMap, freeSubjectMeta, boardConfig, FW_CATEGORIES,
browse-loader BASE_SLUG_BOARDS, plus the name/accent/alias maps).

Idempotent-ish: it refuses to create a subject that already exists, and every
text edit checks for its own marker before inserting.

Usage: python scripts/_content_latin-eduqas/activate_latin.py [--db-only|--files-only]
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")
SLUG = "latin-eduqas"
BASE_SLUG = "latin"
CARD_IMAGE = ("https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/"
              "homepage-cards/latin-eduqas.jpg")
CARD_ACCENT = "#9b2226"


# ------------------------------------------------------------------ helpers

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lighten(h, amount=0.62):
    r, g, b = hex_to_rgb(h)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return "#%02x%02x%02x" % (r, g, b)


def rgba(h, alpha):
    r, g, b = hex_to_rgb(h)
    return "rgba(%d,%d,%d,%s)" % (r, g, b, alpha)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def all_units(plan):
    """Units in sort_order, tagged with their format."""
    out = []
    for u in plan.get("article_units", []):
        out.append((u, "article"))
    for u in plan.get("practice_units", []):
        out.append((u, "practice"))
    out.sort(key=lambda t: t[0]["sort_order"])
    return out


def body_class(u):
    return "unit-%s-%d" % (SLUG, u["sort_order"])


# ------------------------------------------------------------------ database

def activate_db(cfg, plan):
    existing = D.supa(cfg, "GET", "/rest/v1/subjects?slug=eq.%s&select=id,slug" % SLUG)
    if existing:
        print("ABORT: subject %s already exists (%s) — never wipe existing rows"
              % (SLUG, existing[0]["id"]))
        sys.exit(1)

    units = all_units(plan)
    accents = [u["accent"] for u, _ in units]
    quotes = plan.get("quote_ticker_quotes", [])
    items = "".join(
        '<span class="quote-item" style="--q-color: %s;">%s <em>&mdash; %s</em></span>'
        % (accents[i % len(accents)], esc(q["quote"]), esc(q["author"]))
        for i, q in enumerate(quotes))
    ticker = ('<div class="quote-ticker"><div class="quote-ticker-track">%s%s</div></div>'
              % (items, items))

    practice_slugs = [u["slug"] for u, fmt in units if fmt == "practice"]
    subject_row = {
        "slug": SLUG, "name": "Latin", "exam_board": "Eduqas / WJEC",
        "spec_code": "C580QS", "school_id": None, "status": "live",
        "settings": {
            "quote_ticker_html": ticker,
            "practice_units": practice_slugs,
            "unit_image_positions": {},
            "mixed_format": True,
        },
    }
    created = D.supa(cfg, "POST", "/rest/v1/subjects", [subject_row],
                     prefer="return=representation")
    subject_id = created[0]["id"]
    print("subject created:", subject_id)
    print("practice_units:", practice_slugs)

    shells = 0
    for u, fmt in units:
        unit_row = {
            "subject_id": subject_id, "slug": u["slug"], "name": u["name"],
            "subtitle": u.get("subtitle"), "body_class": body_class(u),
            "accent": u["accent"], "accent_light": u["accent_light"],
            "accent_badge": u["accent_badge"], "lesson_count": len(u["lessons"]),
            "sort_order": u["sort_order"],
        }
        uc = D.supa(cfg, "POST", "/rest/v1/units", [unit_row],
                    prefer="return=representation")
        uid = uc[0]["id"]
        rows = []
        for l in u["lessons"]:
            row = {"unit_id": uid, "lesson_number": l["number"], "title": l["title"],
                   "slug": D.slugify(l["title"]), "status": "pending_review"}
            if fmt == "practice":
                # free-tier practice lessons carry the sentinel, never a video
                row["youtube_video_id"] = "practice-only"
            rows.append(row)
        D.supa(cfg, "POST", "/rest/v1/lessons", rows)
        shells += len(rows)
        print("  unit %-28s %-8s %2d shells" % (u["slug"], fmt, len(rows)))

    st = D.load_state(cfg)
    st["subject_id"] = subject_id
    D.save_state(cfg, st)
    print("activation complete: %d units, %d lesson shells" % (len(units), shells))


# ------------------------------------------------------------------ css

def activate_css(plan):
    path = os.path.join(REPO, "css", "style.css")
    css = io.open(path, encoding="utf-8").read()
    if "body.unit-%s-1" % SLUG in css:
        print("css: already wired, skipping")
        return
    lines = ["", "/* Latin (Eduqas / WJEC) unit accents */"]
    for u, _ in all_units(plan):
        bc = body_class(u)
        lines.append("body.%s { --accent: %s; --accent-light: %s; --accent-badge: %s; }"
                     % (bc, u["accent"], u["accent_light"], u["accent_badge"]))
        lines.append("body.dark-mode.%s { --accent: %s; --accent-light: %s; "
                     "--accent-badge: %s; }"
                     % (bc, lighten(u["accent"]), rgba(u["accent"], "0.18"),
                        rgba(u["accent"], "0.28")))
    marker = "/* Latin (Eduqas / WJEC) unit accents */"
    anchor = "body.unit-classical-civilisation-ocr-1"
    idx = css.index(anchor)
    # insert the block just before the Classical Civilisation rules so the
    # classics accents sit together
    css = css[:idx] + "\n".join(lines[1:]) + "\n" + css[idx:]
    io.open(path, "w", encoding="utf-8", newline="").write(css)
    print("css: added %d unit accent rules (%s)" % (len(all_units(plan)), marker))


# ------------------------------------------------------------------ index.html

def insert_once(text, anchor, addition, label, before=False):
    if addition.strip() in text:
        print("  %s: already present" % label)
        return text, False
    i = text.index(anchor)
    if before:
        out = text[:i] + addition + text[i:]
    else:
        j = i + len(anchor)
        out = text[:j] + addition + text[j:]
    print("  %s: wired" % label)
    return out, True


def activate_index(plan):
    path = os.path.join(REPO, "index.html")
    t = io.open(path, encoding="utf-8").read()
    n_units = len(all_units(plan))
    n_lessons = sum(len(u["lessons"]) for u, _ in all_units(plan))
    changed = False

    # 1. home card — placed after the Geology card (the last card in the grid)
    card = (
        '\n      <a href="/browse/%s" class="home-card sv-reveal" data-subject="%s" '
        'style="--card-accent: %s">\n'
        '        <img class="home-card-img" src="%s" alt="Latin" width="500" '
        'height="333" loading="lazy" decoding="async">\n'
        '        <div class="home-card-body">\n'
        '          <h3>Latin</h3>\n'
        '          <p class="home-card-board">Eduqas &middot; WJEC</p>\n'
        '          <p class="home-card-detail">%d units &middot; %d lessons</p>\n'
        '        </div>\n'
        '      </a>' % (BASE_SLUG, BASE_SLUG, CARD_ACCENT, CARD_IMAGE, n_units, n_lessons))
    anchor = ('          <p class="home-card-detail">5 units &middot; 30 lessons</p>\n'
              '        </div>\n      </a>')
    t, c = insert_once(t, anchor, card, "home-card")
    changed |= c

    # 2. picker item — after the Geology picker item
    picker = (
        '\n        <div class="picker-item" data-subject="%s" style="--picker-accent: %s">\n'
        '          <img class="picker-item-img" src="%s" alt="Latin" decoding="async">\n'
        '          <div class="picker-item-label">Latin</div>\n'
        '          <div class="picker-check"><svg width="14" height="14" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
        'stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></div>\n'
        '        </div>' % (BASE_SLUG, CARD_ACCENT, CARD_IMAGE))
    anchor = ('          <div class="picker-item-label">Geology</div>\n'
              '          <div class="picker-check"><svg width="14" height="14" '
              'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" '
              'stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/>'
              '</svg></div>\n        </div>')
    t, c = insert_once(t, anchor, picker, "picker-item")
    changed |= c

    # 3. freeSubjectMeta
    meta = ("\n        '%s': { name: 'Latin', image: '%s', accent: '%s', "
            "detail: '%d units \\u00b7 %d lessons' },"
            % (SLUG, CARD_IMAGE, CARD_ACCENT, n_units, n_lessons))
    anchor = "'geology-eduqas': { name: 'Geology',"
    line_end = t.index("\n", t.index(anchor))
    t, c = insert_once(t, t[t.index(anchor):line_end], meta, "freeSubjectMeta")
    changed |= c

    # 4. boardConfig
    t, c = insert_once(t, "      'geology': { 'Eduqas': true, 'WJEC': true },",
                       "\n      '%s': { 'Eduqas': true, 'WJEC': true }," % BASE_SLUG,
                       "boardConfig")
    changed |= c

    # 5. FW_CATEGORIES — the languages accordion, retitled to include Latin
    t = t.replace("{ id: 'languages', title: 'Modern Languages'",
                  "{ id: 'languages', title: 'Languages'")
    t, c = insert_once(t, "        { name: 'German', slug: 'german', available: true }",
                       ",\n        { name: 'Latin', slug: '%s', available: true }" % BASE_SLUG,
                       "FW_CATEGORIES")
    changed |= c

    # 6. slugMap
    t, c = insert_once(t, "      'geology': { 'eduqas': 'geology-eduqas', 'wjec': 'geology-eduqas' },",
                       "\n      '%s': { 'eduqas': '%s', 'wjec': '%s' },"
                       % (BASE_SLUG, SLUG, SLUG), "slugMap")
    changed |= c

    # 7. display-name map
    t, c = insert_once(t, "      'geology': 'Geology',",
                       " '%s': 'Latin'," % BASE_SLUG, "name map")
    changed |= c

    # 8. accent map
    t, c = insert_once(t, "      'geology': '#78350f',",
                       " '%s': '%s'," % (BASE_SLUG, CARD_ACCENT), "accent map")
    changed |= c

    # 9. wizard search aliases
    t, c = insert_once(
        t, "      'classical-civilisation': ['classics', 'classical civ', 'class civ'],",
        "\n      '%s': ['classics', 'roman', 'romans', 'ancient languages', "
        "'classical languages']," % BASE_SLUG, "search aliases")
    changed |= c

    if changed:
        io.open(path, "w", encoding="utf-8", newline="").write(t)
    print("index.html: %s" % ("updated" if changed else "unchanged"))


def activate_browse_loader():
    path = os.path.join(REPO, "js", "browse-loader.js")
    t = io.open(path, encoding="utf-8").read()
    if "'%s':" % BASE_SLUG in t:
        print("browse-loader: already wired")
        return
    anchor = ("    'geology': [\n"
              "      { board: 'Eduqas', slug: 'geology-eduqas' },\n"
              "      { board: 'WJEC', slug: 'geology-eduqas' }")
    i = t.index(anchor)
    j = t.index("]", i) + 1
    addition = (",\n    '%s': [\n"
                "      { board: 'Eduqas', slug: '%s' },\n"
                "      { board: 'WJEC', slug: '%s' }\n    ]"
                % (BASE_SLUG, SLUG, SLUG))
    t = t[:j] + addition + t[j:]
    io.open(path, "w", encoding="utf-8", newline="").write(t)
    print("browse-loader: BASE_SLUG_BOARDS wired")


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db-only", action="store_true")
    ap.add_argument("--files-only", action="store_true")
    args = ap.parse_args()

    cfg = D.load_config(CFG_PATH)
    plan = json.load(io.open(os.path.join(cfg["run_dir"], "plan.json"), encoding="utf-8"))

    if not args.files_only:
        activate_db(cfg, plan)
    if not args.db_only:
        activate_css(plan)
        activate_index(plan)
        activate_browse_loader()


if __name__ == "__main__":
    main()
