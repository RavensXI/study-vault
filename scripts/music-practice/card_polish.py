# -*- coding: utf-8 -*-
"""Rebuild the 20 study-lesson card decks to match the AQA card grammar
(Tom's review, 16 Aug): cards were whole sections (too long — internal
scrolling), lacked the two-column sv-card-body wrapper, covers could be
imageless-text or textless-image, and the old sv-listen blocks are
redundant next to pins and chips.

Changes per lesson:
- sv-listen figures REMOVED (their narration ids pruned from the
  manifest — no ghost audio).
- Sections re-split into cards of <=620 chars of text (AQA's range),
  packed at block boundaries; context sv-embed figures become their own
  card (the only-child CSS rule gives them full width).
- Every card's blocks wrapped in <div class="sv-card-body">.
- The cover card always carries real text (first content chunk if the
  lesson has no intro).
- data-chapters re-assigned to the smaller cards by pin-label keyword
  match; short titles per card from one model call per lesson.

Run: python card_polish.py [--apply]
Backup: _backup_card_polish_2026-08-16.json
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
BACKUP = os.path.join(HERE, "_backup_card_polish_2026-08-16.json")
BUDGET = 620
TARGETS = {
    "music-eduqas": [("aos1-forms-and-devices", 3), ("aos1-forms-and-devices", 4),
                     ("aos4-popular-music", 3), ("aos4-popular-music", 4)],
    "music-edexcel": [(u, n) for u in ("aos1-instrumental-music",
                                       "aos2-vocal-music",
                                       "aos3-stage-and-screen",
                                       "aos4-fusions")
                      for n in (2, 3, 4, 5)],
}
STOP = {"the", "and", "for", "with", "your", "this", "that", "how", "what",
        "music", "movement", "work", "study", "close", "exam"}


def toks(s):
    return {t for t in re.findall(r"[a-z]{4,}", s.lower()) if t not in STOP}


def txtlen(html):
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)))


def blocks_of(html):
    """Top-level blocks: p / div.key-fact / figure / h2."""
    out = re.findall(r"(<h2[^>]*>.*?</h2>|<p[^>]*>.*?</p>"
                     r"|<div class=\"key-fact\">.*?</div>"
                     r"|<figure[^>]*>.*?</figure>)", html, re.S)
    return out


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    units = sb.table("units").select("id,slug,subject_id").execute().data
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in TARGETS}
    backup, writes, man_updates = {}, [], {}
    for slug, pairs in TARGETS.items():
        umap = {u["slug"]: u["id"] for u in units
                if u["subject_id"] == subs[slug]}
        for uslug, num in pairs:
            row = sb.table("lessons").select(
                "id,title,content_html,narration_manifest") \
                .eq("unit_id", umap[uslug]).eq("lesson_number", num) \
                .execute().data[0]
            ch = row["content_html"]
            fig = re.search(r'<figure class="sv-annotated-player.*?</figure>',
                            ch, re.S).group(0)
            # flatten existing deck back to a block stream
            inner = ch.replace(fig, "")
            inner = re.sub(r'</?div class="sv-listening">|</div>\s*$', "",
                           inner)
            inner = re.sub(r'<section class="sv-card[^"]*"[^>]*>|</section>',
                           "", inner)
            # drop listen boxes, remember EVERY narration id inside them
            # (some carry inner narrated paragraphs, not just the figure id)
            dead_ids = []
            for boxm in re.finditer(r'<figure class="sv-listen".*?</figure>',
                                    inner, re.S):
                dead_ids.extend(re.findall(r'data-narration-id="([^"]+)"',
                                           boxm.group(0)))
            inner = re.sub(r'<figure class="sv-listen".*?</figure>', "",
                           inner, flags=re.S)
            blocks = blocks_of(inner)
            leftover = inner
            for b in blocks:
                leftover = leftover.replace(b, "", 1)
            assert txtlen(leftover) < 20, \
                "%s %s L%d: unparsed content %r" % (slug, uslug, num,
                                                    leftover[:80])
            # pack into chunks
            chunks, cur, cur_len = [], [], 0
            for b in blocks:
                is_embed = b.startswith("<figure")
                is_h2 = b.startswith("<h2")
                bl = txtlen(b)
                if is_embed:
                    if cur:
                        chunks.append(cur)
                    chunks.append([b])
                    cur, cur_len = [], 0
                    continue
                if cur and (cur_len + bl > BUDGET or is_h2):
                    chunks.append(cur)
                    cur, cur_len = [], 0
                cur.append(b)
                cur_len += bl
            if cur:
                chunks.append(cur)
            # orphan pass: a thin prose chunk (<260 chars) merges into a
            # prose neighbour — backwards first, forwards otherwise —
            # rather than sitting alone in the stage. A chunk that starts
            # with an h2 must not merge backwards (it opens a section).
            def is_embed_chunk(c):
                return len(c) == 1 and c[0].startswith("<figure")

            def thin(c):
                return not is_embed_chunk(c) and txtlen("".join(c)) < 260
            merged = []
            for c in chunks:
                if (thin(c) and not c[0].startswith("<h2") and merged
                        and not is_embed_chunk(merged[-1])
                        and txtlen("".join(merged[-1] + c)) < BUDGET * 1.35):
                    merged[-1] = merged[-1] + c
                else:
                    merged.append(c)
            chunks = []
            i = 0
            while i < len(merged):
                c = merged[i]
                if (thin(c) and i + 1 < len(merged)
                        and not is_embed_chunk(merged[i + 1])
                        and not merged[i + 1][0].startswith("<h2")
                        and txtlen("".join(c + merged[i + 1])) <
                        BUDGET * 1.35):
                    chunks.append(c + merged[i + 1])
                    i += 2
                else:
                    chunks.append(c)
                    i += 1
            # cover budget: the cover grid halves the text column, so a
            # heavy first chunk overflows — spill its tail to card 2
            if chunks and txtlen("".join(chunks[0])) > 420:
                head, tail, run = [], [], 0
                for b in chunks[0]:
                    if not tail and (run + txtlen(b) <= 420
                                     or b.startswith("<h2") or not head):
                        head.append(b)
                        run += txtlen(b)
                    else:
                        tail.append(b)
                if tail:
                    chunks = [head, tail] + chunks[1:]
            # titles via one model call
            briefs = []
            for i, c in enumerate(chunks):
                h2 = next((re.sub(r"<[^>]+>", "", b) for b in c
                           if b.startswith("<h2")), None)
                first = re.sub(r"\s+", " ",
                               re.sub(r"<[^>]+>", "", "".join(c)))[:110]
                briefs.append({"i": i, "heading": h2, "starts": first})
            prompt = ("Lesson: %s\nCards:\n%s\n\nGive each card a punchy "
                      "title of AT MOST 3 words (no punctuation, no "
                      "quotes). Use the heading when present, shortened. "
                      'Return ONLY JSON: ["title1", ...] in order.'
                      % (row["title"], json.dumps(briefs)))
            titles = None
            for attempt in range(3):
                r = cl.messages.create(model="claude-sonnet-5",
                                       max_tokens=2500,
                                       messages=[{"role": "user",
                                                  "content": prompt}])
                text = re.sub(r"```(?:json)?", "",
                              "".join(getattr(b, "text", "") or ""
                                      for b in r.content))
                m = re.search(r"\[[\s\S]*\]", text)
                if not m:
                    continue
                try:
                    cand = json.loads(m.group(0))
                except ValueError:
                    continue
                if len(cand) == len(chunks) and all(
                        isinstance(t, str) and t and '"' not in t
                        for t in cand):
                    titles = cand
                    break
            assert titles, "titles failed %s L%d" % (uslug, num)
            # chapters by keyword match on chunk text
            pins = re.findall(r'data-cid="(t1c\d+)"[^>]*>\d+<span class='
                              r'"sv-ap-tip"><strong>\d+ &middot; ([^<]+)'
                              r"</strong>", fig)
            chap = {i: [] for i in range(len(chunks))}
            for cid, label in pins:
                lt = toks(label)
                best, score = 0, -1
                for i, c in enumerate(chunks):
                    sc = len(lt & toks(re.sub(r"<[^>]+>", "", "".join(c))))
                    if sc > score:
                        best, score = i, sc
                chap[best].append(cid)
            cards = []
            for i, c in enumerate(chunks):
                h2s = [b for b in c if b.startswith("<h2")]
                rest = [b for b in c if not b.startswith("<h2")]
                cls = "sv-card sv-card--cover" if i == 0 else "sv-card"
                attrs = ' data-title="%s"' % titles[i]
                if i > 0:
                    attrs += ' data-track="t1"'
                    if chap[i]:
                        attrs += ' data-chapters="%s"' % ",".join(chap[i])
                # a card that stays light renders as a centred statement
                # rather than text lost top-left in an empty stage
                # (inline so it works pre-deploy; sv-card--statement CSS
                # committed for future builds)
                if (i > 0 and not h2s and not is_embed_chunk(c)
                        and txtlen("".join(rest)) < 340):
                    cls += " sv-card--statement"
                    attrs += (' style="display:flex;align-items:center;'
                              'justify-content:center"')
                    body = ('<div class="sv-card-body" style="max-width:'
                            '620px;font-size:1.12em;column-count:1">'
                            "%s</div>" % "".join(rest))
                else:
                    body = '<div class="sv-card-body">%s</div>' % \
                        "".join(rest)
                cards.append('<section class="%s"%s>%s%s</section>'
                             % (cls, attrs, "".join(h2s), body))
            new_ch = fig + '<div class="sv-listening">' + "".join(cards) + \
                "</div>"
            # validation
            old_ids = [i for i in re.findall(r'data-narration-id="([^"]+)"',
                                             ch) if i not in dead_ids]
            new_ids = re.findall(r'data-narration-id="([^"]+)"', new_ch)
            assert old_ids == new_ids, "%s %s L%d ids" % (slug, uslug, num)
            man = row["narration_manifest"] or []
            new_man = [c for c in man if c["id"] not in dead_ids]
            over = [txtlen(re.search(r'<div class="sv-card-body"[^>]*>(.*?)'
                                     r"</div></section>", c, re.S).group(1))
                    for c in cards]
            print("%s %s L%d: %d cards (max %d chars), %d listen boxes "
                  "dropped, manifest %d->%d"
                  % (slug, uslug, num, len(cards), max(over), len(dead_ids),
                     len(man), len(new_man)))
            backup[row["id"]] = {"content_html": ch,
                                 "narration_manifest": man}
            writes.append((row["id"], new_ch,
                           new_man if dead_ids else None))
    print("\nlessons to write:", len(writes))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch2, man2 in writes:
        upd = {"content_html": ch2}
        if man2 is not None:
            upd["narration_manifest"] = man2
        sb.table("lessons").update(upd).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
