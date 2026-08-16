# -*- coding: utf-8 -*-
"""Convert the 20 set-work study lessons (music-eduqas x4, music-edexcel
x16) from article-plus-player into the AQA listening-lesson card format
(Tom's call, 16 Aug — the article layout was already rejected on AQA).

Shape produced (matches the live Queen/Spalding lessons):
  <figure class="sv-annotated-player ...">   (moved to the top)
  <div class="sv-listening">
    <section class="sv-card sv-card--cover" data-title="...">  (intro)
    <section class="sv-card" data-title="..." data-track="t1"
             [data-chapters="t1c2,t1c3"]>    (one per h2 section)
  </div>

Content is re-housed VERBATIM — same elements, same narration ids, so
manifests stay valid (verified: id set + stripped text equality).
Chapters are assigned by keyword overlap between pin labels and card
headings (unmatched pins fall to the first card), and the mapping is
printed for eyeballing in the dry run. Card titles come from one batched
model call (<=3 words each).

Run: python convert_study_carousels.py [--apply]
Backup: _backup_study_carousels_2026-08-16.json
"""
import io
import json
import os
import re
import sys

import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_backup_study_carousels_2026-08-16.json")
TARGETS = {
    "music-eduqas": [("aos1-forms-and-devices", 3), ("aos1-forms-and-devices", 4),
                     ("aos4-popular-music", 3), ("aos4-popular-music", 4)],
    "music-edexcel": [("aos1-instrumental-music", n) for n in (2, 3, 4, 5)] +
                     [("aos2-vocal-music", n) for n in (2, 3, 4, 5)] +
                     [("aos3-stage-and-screen", n) for n in (2, 3, 4, 5)] +
                     [("aos4-fusions", n) for n in (2, 3, 4, 5)],
}
STOP = {"the", "and", "for", "with", "your", "this", "that", "how", "what",
        "music", "movement", "work", "study", "close", "exam"}


def toks(s):
    return {t for t in re.findall(r"[a-z]{4,}", s.lower()) if t not in STOP}


def split_sections(body):
    """body (content minus player figure) -> (intro, [(h2_html, sect_html)])"""
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", body, flags=re.S)
    intro = parts[0]
    sections = []
    i = 1
    while i < len(parts):
        sections.append((parts[i], parts[i + 1] if i + 1 < len(parts) else ""))
        i += 2
    return intro, sections


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    units = sb.table("units").select("id,slug,subject_id").execute().data
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in TARGETS}
    lessons = []
    for slug, pairs in TARGETS.items():
        umap = {u["slug"]: u["id"] for u in units
                if u["subject_id"] == subs[slug]}
        for uslug, num in pairs:
            row = sb.table("lessons").select("id,title,content_html") \
                .eq("unit_id", umap[uslug]).eq("lesson_number", num) \
                .execute().data[0]
            lessons.append((slug, uslug, num, row))

    # one batched call for card titles
    req = []
    parsed = {}
    for slug, uslug, num, row in lessons:
        ch = row["content_html"]
        figm = re.search(r'<figure class="sv-annotated-player.*?</figure>',
                         ch, re.S)
        assert figm, "%s %s L%d: no player" % (slug, uslug, num)
        body = ch.replace(figm.group(0), "")
        intro, sections = split_sections(body)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h, _ in sections]
        parsed[row["id"]] = (figm.group(0), intro, sections, heads)
        req.append({"key": row["id"], "lesson": row["title"],
                    "headings": heads})
    titles = {}
    for item in req:
        prompt = ("Lesson: %s\nHeadings:\n%s\n\nWrite a card title of AT "
                  "MOST 3 words for the cover card (the lesson intro) and "
                  "for each heading, in order. Punchy, specific, no "
                  "punctuation, no quotation marks. Return ONLY JSON: "
                  '{"cover": "...", "cards": ["...", ...]}'
                  % (item["lesson"],
                     "\n".join("%d. %s" % (i + 1, h)
                               for i, h in enumerate(item["headings"]))))
        got = None
        for attempt in range(3):
            r = cl.messages.create(model="claude-sonnet-5", max_tokens=600,
                                   messages=[{"role": "user",
                                              "content": prompt}])
            text = re.sub(r"```(?:json)?", "",
                          "".join(getattr(b, "text", "") or ""
                                  for b in r.content))
            m = re.search(r"\{[\s\S]*\}", text)
            if not m:
                continue
            try:
                cand = json.loads(m.group(0))
            except ValueError:
                continue
            if (cand.get("cover") and
                    len(cand.get("cards", [])) == len(item["headings"]) and
                    all('"' not in c for c in cand["cards"])):
                got = cand
                break
        assert got, "title generation failed for %s" % item["lesson"][:40]
        titles[item["key"]] = got

    backup, writes = {}, []
    for slug, uslug, num, row in lessons:
        fig, intro, sections, heads = parsed[row["id"]]
        t = titles[row["id"]]
        # pins from the player: (cid, label)
        pins = re.findall(r'data-cid="(t1c\d+)"[^>]*>\d+<span class='
                          r'"sv-ap-tip"><strong>\d+ &middot; ([^<]+)</strong>',
                          fig)
        # chapters by keyword overlap, unmatched -> first section card
        chap = {i: [] for i in range(len(sections))}
        for cid, label in pins:
            lt = toks(label)
            best, score = 0, -1
            for i, h in enumerate(heads):
                sc = len(lt & toks(h))
                if sc > score:
                    best, score = i, sc
            chap[best].append(cid)
        cards = ['<section class="sv-card sv-card--cover" data-title="%s">'
                 "%s</section>" % (t["cover"], intro.strip())]
        for i, (h2, sect) in enumerate(sections):
            attrs = ' data-title="%s" data-track="t1"' % t["cards"][i]
            if chap[i]:
                attrs += ' data-chapters="%s"' % ",".join(chap[i])
            cards.append('<section class="sv-card"%s>%s%s</section>'
                         % (attrs, h2, sect.strip()))
        new_ch = fig + '<div class="sv-listening">' + "".join(cards) + "</div>"
        # verification: narration ids + stripped text preserved
        old_ids = re.findall(r'data-narration-id="([^"]+)"', row["content_html"])
        new_ids = re.findall(r'data-narration-id="([^"]+)"', new_ch)
        assert old_ids == new_ids, "%s %s L%d: narration ids changed" \
            % (slug, uslug, num)
        strip = lambda s: re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", s))
        # the player moves to the top, so compare body text only, plus
        # exactly one player in the output
        assert new_ch.count("sv-annotated-player") == \
            row["content_html"].count("sv-annotated-player")
        body_old = row["content_html"].replace(fig, "")
        body_new = new_ch.replace(fig, "").replace(
            '<div class="sv-listening">', "")
        assert strip(body_old) == strip(body_new), \
            "%s %s L%d: body text changed" % (slug, uslug, num)
        backup[row["id"]] = row["content_html"]
        writes.append((row["id"], new_ch))
        chapdesc = ", ".join("%s->%s" % (t["cards"][i][:14], v)
                             for i, v in chap.items() if v)
        print("%s %s L%d: cover + %d cards | chapters: %s"
              % (slug, uslug, num, len(sections), chapdesc or "none"))
    print("\nlessons to write:", len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch in writes:
        sb.table("lessons").update({"content_html": ch}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
