# -*- coding: utf-8 -*-
"""Weave numbered sv-ap-ref jump chips through the 20 study lessons' card
prose (Tom's review call, 16 Aug): wherever a card discusses the moment a
player pin marks, a tappable numbered chip jumps the docked player there
— the Queen-lesson behaviour.

Per lesson, one model call matches pins (number, time, label, tip)
against the card paragraphs and returns a VERBATIM anchor phrase per
placement; chips are inserted immediately after the anchor. Placement
rules: prose paragraphs only (never inside the player figure or an
existing figcaption), each pin 1-2 placements, anchor must occur exactly
once in the lesson. Narration is untouched — the extractor skips
<button> entirely.

Run: python weave_ref_chips.py [--apply]
Backup: _backup_ref_chips_2026-08-16.json
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
BACKUP = os.path.join(HERE, "_backup_ref_chips_2026-08-16.json")
TARGETS = {
    "music-eduqas": [("aos1-forms-and-devices", 3), ("aos1-forms-and-devices", 4),
                     ("aos4-popular-music", 3), ("aos4-popular-music", 4)],
    "music-edexcel": [(u, n) for u in ("aos1-instrumental-music",
                                       "aos2-vocal-music",
                                       "aos3-stage-and-screen",
                                       "aos4-fusions")
                      for n in (2, 3, 4, 5)],
}


def chip(n, t):
    return ('<button type="button" class="sv-ap-ref" data-t="%d" '
            'data-track="t1">%d</button>' % (t, n))


def main():
    sb = get_client()
    cl = anthropic.Anthropic()
    units = sb.table("units").select("id,slug,subject_id").execute().data
    subs = {s["slug"]: s["id"] for s in
            sb.table("subjects").select("id,slug,school_id").execute().data
            if not s["school_id"] and s["slug"] in TARGETS}
    backup, writes = {}, []
    total = 0
    for slug, pairs in TARGETS.items():
        umap = {u["slug"]: u["id"] for u in units
                if u["subject_id"] == subs[slug]}
        for uslug, num in pairs:
            row = sb.table("lessons").select("id,content_html") \
                .eq("unit_id", umap[uslug]).eq("lesson_number", num) \
                .execute().data[0]
            ch = row["content_html"]
            figm = re.search(r'<figure class="sv-annotated-player.*?</figure>',
                             ch, re.S)
            fig = figm.group(0)
            pins = [(int(n), int(float(t)), label.strip(), tip.strip())
                    for t, n, label, tip in re.findall(
                        r'data-t="([\d.]+)"[^>]*>(\d+)<span class="sv-ap-tip">'
                        r"<strong>\d+ &middot; ([^<]+)</strong>([^<]*)", fig)]
            body = ch.replace(fig, "")
            paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)
            prose = "\n\n".join(re.sub(r"<[^>]+>", "", p) for p in paras)
            pinlist = "\n".join("%d (at %ds): %s — %s" % p for p in pins)
            prompt = ("PLAYER PINS:\n%s\n\nLESSON PROSE (paragraphs):\n%s\n\n"
                      "For each pin, find 1 or at most 2 places in the prose "
                      "where the text discusses that pinned moment. For each "
                      "placement return the VERBATIM final 4-8 words of the "
                      "sentence (exactly as written, including punctuation "
                      "except the final full stop) after which a numbered "
                      "jump-to-player chip should sit. Skip a pin if no "
                      "sentence genuinely discusses its moment. Return ONLY "
                      'JSON: [{"pin": N, "anchor": "..."}]'
                      % (pinlist, prose[:9000]))
            placements = None
            for attempt in range(4):
                r = cl.messages.create(model="claude-sonnet-5",
                                       max_tokens=3000,
                                       messages=[{"role": "user",
                                                  "content": prompt}])
                text = re.sub(r"```(?:json)?", "",
                              "".join(getattr(b, "text", "") or ""
                                      for b in r.content))
                m = re.search(r"\[[\s\S]*\]", text)
                if not m:
                    continue
                try:
                    placements = json.loads(m.group(0))
                    break
                except ValueError:
                    continue
            if placements is None:
                print("%s %s L%d: placement generation failed" % (slug, uslug,
                                                                  num))
                continue
            new_ch = ch
            placed = 0
            pin_t = {n: t for n, t, _, _ in pins}
            for pl in placements:
                n = pl.get("pin")
                anchor = (pl.get("anchor") or "").strip().rstrip(".")
                if n not in pin_t or len(anchor) < 8:
                    continue
                # anchor must appear exactly once, in body prose (not the fig)
                if new_ch.count(anchor) != 1 or anchor in fig:
                    continue
                idx = new_ch.find(anchor) + len(anchor)
                # step over a run of closing punctuation / entities only
                m2 = re.match(r"(?:[.,!?)]|&[a-z]+;)*", new_ch[idx:])
                idx += m2.end()
                new_ch = new_ch[:idx] + " " + chip(n, pin_t[n]) + new_ch[idx:]
                placed += 1
            # validation: chip-stripping BOTH sides must give equality (the
            # lessons already carry chips from the listen-box conversion)
            strip_all = lambda s: re.sub(
                r' ?<button type="button" class="sv-ap-ref" '
                r'data-t="\d+" data-track="t1">\d+</button>', "", s)
            assert strip_all(new_ch) == strip_all(ch), \
                "%s %s L%d: content damaged" % (slug, uslug, num)
            assert new_ch.count("sv-ap-ref") == ch.count("sv-ap-ref") + placed
            total += placed
            print("%s %s L%d: %d chip(s) woven" % (slug, uslug, num, placed))
            if placed:
                backup[row["id"]] = ch
                writes.append((row["id"], new_ch))
    print("\ntotal chips: %d | lessons: %d" % (total, len(writes)))
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    if not os.path.exists(BACKUP):
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup))
    for lid, ch2 in writes:
        sb.table("lessons").update({"content_html": ch2}).eq("id", lid) \
            .execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
