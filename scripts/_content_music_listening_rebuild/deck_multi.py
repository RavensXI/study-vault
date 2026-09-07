# -*- coding: utf-8 -*-
"""Guided-listening deck builder for lessons that need a MULTI-TRACK YouTube
dock built from scratch.

deck.py builds a single-track dock; deck_raw.py re-uses a dock that already
exists on a live row. The four music-ocr "Rhythms of the World" lessons have
neither: they were practice rows (practice_data + synthesised clicks) with an
empty content_html, and each needs two real recordings docked side by side.

Markup contract (main.js lines 3665-3700 and 4058-4145):
  * .sv-ap-trackbtn  carries data-track / data-yt / data-dur; the first one
    also carries sv-ap-trackbtn--on.
  * .sv-ap-pin       carries data-track, data-cid, data-t and left:%  where
    left = 100 * t / that track's own data-dur. Pin numbering restarts per
    track (only the active track's pins are visible).
  * .sv-ap-ref       carries data-t AND data-track (seek takes both).
  * .sv-card         carries data-track (switches the dock when the card is
    reached) and data-chapters (the pin cid that scrolls it into view).
Card cap is pins + 2: one cover, one card per pin, one exam checklist.
"""
import io, json, os, re, html as _html

from deck import _Bal, dfn, check_plain  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))


class MultiDeck(object):
    def __init__(self, lesson_id, subject, unit, lesson_no, tracks, credit, board=None):
        """tracks: list of (track_id, youtube_id, duration_seconds, button_label)."""
        self.lesson_id = lesson_id
        self.subject, self.unit, self.lesson_no = subject, unit, lesson_no
        self.tracks = tracks
        self.durs = {t[0]: int(t[2]) for t in tracks}
        self.credit, self.board = credit, board
        self.pins = []          # (track, cid, seconds, title, tip)
        self.cards = []
        self._n = 0
        self.card_words = []

    # ---- helpers -------------------------------------------------------
    def nid(self):
        self._n += 1
        return 'data-narration-id="n%d"' % self._n

    def _num(self, n):
        """Pin numbers restart on each track."""
        track = self.pins[n - 1][0]
        return sum(1 for p in self.pins[:n] if p[0] == track)

    def ref(self, n):
        track, _cid, t = self.pins[n - 1][0], self.pins[n - 1][1], self.pins[n - 1][2]
        return ('<button type="button" class="sv-ap-ref" data-t="%d" data-track="%s">%d</button>'
                % (t, track, self._num(n)))

    def _pin_html(self, track, cid, t, title, tip, n):
        pct = 100.0 * t / self.durs[track]
        # style.css line 9513 clamps the tooltip to the right edge for
        # .sv-ap-pin:last-of-type, but "last of type" is the last pin in the
        # DOM, i.e. the last pin of the LAST track. A pin sitting at the far
        # right of an earlier track gets the centred tooltip and pushes it off
        # the viewport (measured: 62px past the edge at 1707px wide on L3's
        # 97.6% pin). Give any such pin the same clamp inline.
        clamp = ""
        if pct >= 95.0 and track != self.tracks[-1][0]:
            clamp = ' style="left:auto;right:0;transform:none"'
        return ('<button type="button" class="sv-ap-pin" data-track="%s" data-cid="%s" data-t="%d" '
                'style="left:%.2f%%">%d<span class="sv-ap-tip"%s><strong>%d &middot; %s</strong>%s</span></button>'
                % (track, cid, t, pct, n, clamp, n, title, tip))

    def player(self):
        btns = []
        for i, (tid, yt, dur, label) in enumerate(self.tracks):
            btns.append('<button type="button" class="sv-ap-trackbtn%s" data-track="%s" data-yt="%s" '
                        'data-dur="%d">%s</button>'
                        % (" sv-ap-trackbtn--on" if i == 0 else "", tid, yt, int(dur), label))
        seen, pins = {}, []
        for track, cid, t, title, tip in self.pins:
            seen[track] = seen.get(track, 0) + 1
            pins.append(self._pin_html(track, cid, t, title, tip, seen[track]))
        return ('<figure class="sv-annotated-player sv-ap-yt" data-lesson-id="%s"><div class="sv-ap-bar">'
                '<button type="button" class="sv-ap-play">&#9654;</button>'
                '<span class="sv-ap-tick">0:00 / &ndash;:&ndash;&ndash;</span><div class="sv-ap-tracks">%s</div>'
                '</div><div class="sv-ap-media"><div class="sv-ap-video"><div class="sv-ap-ytmount"></div></div>'
                '<div class="sv-ap-wrap"><div class="sv-ap-track"><div class="sv-ap-trackfill"></div></div>%s'
                '</div></div><figcaption class="sv-listen-credit">%s</figcaption></figure>'
                % (self.lesson_id, "".join(btns), "".join(pins), self.credit))

    # ---- cards ---------------------------------------------------------
    def add_cover(self, heading, paras, title="The tradition"):
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        body = "".join("<p %s>%s</p>" % (self.nid(), p) for p in paras)
        self.cards.append('<section class="sv-card sv-card--cover" data-title="%s" data-track="%s">%s'
                          '<div class="sv-card-body">%s</div></section>'
                          % (title, self.tracks[0][0], h, body))

    def add_statement(self, n, pin_title, heading, para, listen_for):
        track, cid = self.pins[n - 1][0], self.pins[n - 1][1]
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        p1 = "<p %s>%s</p>" % (self.nid(), para)
        p2 = "<p %s><strong>Listen for:</strong> %s</p>" % (self.nid(), listen_for)
        self.cards.append(
            '<section class="sv-card sv-card--statement" data-title="%s" data-track="%s" data-chapters="%s"'
            ' style="display:flex;align-items:center;justify-content:center">'
            '<div class="sv-card-body" style="max-width:640px;font-size:1.08em;column-count:1">%s%s%s</div></section>'
            % (pin_title, track, cid, h, p1, p2))

    def add_checklist(self, summary, precision, heading="Say it precisely in the exam"):
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        p1 = "<p %s>%s</p>" % (self.nid(), summary)
        p2 = "<p %s>%s</p>" % (self.nid(), precision)
        self.cards.append('<section class="sv-card" data-title="Exam checklist" data-track="%s">%s'
                          '<div class="sv-card-body">%s%s</div></section>' % (self.tracks[-1][0], h, p1, p2))

    def content(self):
        return self.player() + '<div class="sv-listening">' + "".join(self.cards) + '</div>'

    # ---- verification --------------------------------------------------
    def verify(self, content, extra_text=""):
        errs, warns = [], []
        b = _Bal()
        b.feed(content)
        if b.errors:
            errs += b.errors
        if b.stack:
            errs.append("unclosed: %s" % b.stack)

        nums = [int(x) for x in re.findall(r'data-narration-id="n(\d+)"', content)]
        if nums != list(range(1, len(nums) + 1)):
            errs.append("narration ids not contiguous from n1")
        for m in re.finditer(r"<(\w+)[^>]*data-narration-id=", content):
            if m.group(1) not in ("h2", "p"):
                errs.append("narration id on <%s>" % m.group(1))

        pins = re.findall(r'class="sv-ap-pin" data-track="(t\d)" data-cid="([^"]+)" data-t="(\d+)" style="left:([\d.]+)%"',
                          content)
        if len(pins) != len(self.pins):
            errs.append("%d pins rendered, %d expected" % (len(pins), len(self.pins)))
        cids = set()
        for (trk, cid, t, pct), (etrk, ecid, et, _ti, _tp) in zip(pins, self.pins):
            cids.add(cid)
            if trk != etrk or cid != ecid or int(t) != int(et):
                errs.append("pin %s does not match the declared pin list" % cid)
            d = self.durs[etrk]
            if abs(float(pct) - 100.0 * float(t) / d) > 0.02:
                errs.append("pin %s left=%s%% != %.2f%%" % (cid, pct, 100.0 * float(t) / d))
            if float(t) > d:
                errs.append("pin %s beyond track length" % cid)
        if len(cids) != len(self.pins):
            errs.append("duplicate pin cids")
        for tr in self.durs:
            ts = [p[2] for p in self.pins if p[0] == tr]
            if ts != sorted(ts):
                errs.append("pins out of time order on %s" % tr)
        declared = {t[0] for t in self.tracks}
        used = {p[0] for p in self.pins}
        if used - declared:
            errs.append("pins on undeclared tracks: %s" % (used - declared))
        if declared - used:
            errs.append("declared tracks with no pins: %s" % (declared - used))

        pint = {(p[0], int(p[2])) for p in self.pins}
        for m in re.finditer(r'class="sv-ap-ref" data-t="(\d+)" data-track="(t\d)"', content):
            if (m.group(2), int(m.group(1))) not in pint:
                errs.append("ref data-t=%s on %s has no pin" % (m.group(1), m.group(2)))
        for m in re.finditer(r'<button type="button" class="sv-ap-ref"(?! data-t="\d+" data-track="t\d">)', content):
            errs.append("ref missing data-t/data-track")
        for ch in re.findall(r'data-chapters="([^"]+)"', content):
            for k in ch.split(","):
                if k.strip() not in cids:
                    errs.append("data-chapters=%s has no pin" % k)
        # every statement card must sit on the same track as its pin
        for m in re.finditer(r'<section class="sv-card sv-card--statement"[^>]*data-track="(t\d)" data-chapters="([^"]+)"', content):
            trk, cid = m.group(1), m.group(2)
            owner = [p[0] for p in self.pins if p[1] == cid]
            if owner and owner[0] != trk:
                errs.append("card for %s declares %s but the pin is on %s" % (cid, trk, owner[0]))

        for m in re.finditer(r"%[sdr](?![a-zA-Z])", content):
            errs.append("unsubstituted format placeholder %r" % m.group(0))
        low = (content + extra_text).lower()
        if "video walkthrough" in low:
            errs.append('contains "Video walkthrough"')
        if "<iframe" in low or "youtube.com/embed" in low:
            errs.append("contains an embedded iframe")
        if "<img" in low:
            errs.append("contains an image")
        if self.board == "eduqas":
            for w in ("eduqas", "wjec"):
                if w in low:
                    errs.append("names the board: %s" % w)

        cards = re.findall(r'<section class="sv-card', content)
        cap = len(self.pins) + 2
        if len(cards) != cap:
            errs.append("%d cards, expected pins+2=%d" % (len(cards), cap))
        stmts = re.findall(r'<section class="sv-card sv-card--statement".*?</section>', content, re.S)
        if len(stmts) != len(self.pins):
            errs.append("%d statement cards for %d pins" % (len(stmts), len(self.pins)))
        self.card_words = []
        for m in stmts:
            w = len(_html.unescape(re.sub(r"<[^>]+>", " ", m)).split())
            self.card_words.append(w)
            if w > 92:
                warns.append("statement card %d words" % w)
        for ch, name in (("—", "&mdash;"), ("‘", "&lsquo;"), ("’", "&rsquo;"),
                         ("“", "&ldquo;"), ("”", "&rdquo;"), ("–", "&ndash;")):
            if ch in content:
                errs.append("raw %s in content_html, use %s" % (name.strip("&;"), name))
        return errs, warns


def patch(deck, payload, apply=False):
    """PATCH the row. Refuses to touch status, practice_data-adjacent routing
    fields are passed explicitly by the caller."""
    import requests
    u = os.environ["SUPABASE_URL"]
    k = os.environ["SUPABASE_SERVICE_KEY"]
    h = {"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json",
         "Prefer": "return=representation"}
    if "status" in payload:
        raise SystemExit("refusing to change status")
    if not apply:
        print("dry run: %d chars, %d narration ids, %d cards, %d pins"
              % (len(payload["content_html"]), deck._n, len(deck.cards), len(deck.pins)))
        return None
    r = requests.patch("%s/rest/v1/lessons?id=eq.%s" % (u, deck.lesson_id), headers=h, json=payload)
    print("PATCH", r.status_code, "" if r.status_code < 300 else r.text[:500])
    if r.status_code >= 300:
        raise SystemExit(1)
    return r.json()
