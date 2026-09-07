# -*- coding: utf-8 -*-
"""Guided-listening deck builder for the music-aqa lessons.

Differences from deck.py, which serves the single-work Edexcel/Eduqas lessons:

  * The dock is REUSED VERBATIM from the live lesson rather than rebuilt. These
    lessons are live and QA'd; the R2 wave dock (sv-ap-canvas + the inline
    peaks JSON) and the multi-track YouTube bar must survive untouched. Only
    the run of pin buttons inside .sv-ap-wrap is replaced, plus any data-dur
    that has been proved wrong against YouTube's own metadata.
  * The wave dock's refs and pins carry no data-track (main.js line 3926 seeks
    on data-t alone); the multi-track YouTube dock's do (line 4130).
  * Pin numbering restarts per track, and each track's left% is a percentage of
    that track's own duration.
  * Card cap is pins + 2, not 9: these are multi-work study pieces, so one card
    per landmark scales with the number of works.
"""
import io, json, os, re, sys, html as _html
from deck import Deck, dfn, _Bal, check_plain, patch  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
PIN_RUN = re.compile(r'<button type="button" class="sv-ap-pin".*?</span></button>(?=(?:<button type="button" class="sv-ap-pin")|</div>)', re.S)


class RawDeck(Deck):
    def __init__(self, lesson_id, subject, unit, lesson_no, original_html, durs=None, board=None):
        Deck.__init__(self, lesson_id, subject, unit, lesson_no, yt="", dur=1,
                      track_label="", credit="", board=board)
        cut = original_html.index('<div class="sv-listening"')
        self.dock = original_html[:cut]
        self.is_wave = "sv-ap-wave" in self.dock
        # correct any proved-wrong track durations before anything is measured
        for tid, newdur in (durs or {}).items():
            self.dock = re.sub(r'(data-track="%s" data-yt="[^"]+" data-dur=")\d+(")' % tid,
                               r"\g<1>%d\g<2>" % newdur, self.dock)
        self.durs = {}
        for m in re.finditer(r'data-track="(t\d)"[^>]*data-dur="(\d+)"', self.dock):
            self.durs[m.group(1)] = int(m.group(2))
        if self.is_wave:
            m = re.search(r'class="sv-ap-peaks">\{"duration":([\d.]+)', self.dock)
            self.durs["t1"] = float(m.group(1))
        self.pins = []   # (track, cid, seconds, title, tip)

    # ---- dock -----------------------------------------------------------
    def _pin_html(self, track, cid, t, title, tip, n):
        trk = "" if self.is_wave else ' data-track="%s"' % track
        return ('<button type="button" class="sv-ap-pin"%s data-cid="%s" data-t="%s" style="left:%.2f%%">%d'
                '<span class="sv-ap-tip"><strong>%d &middot; %s</strong>%s</span></button>'
                % (trk, cid, ("%g" % t), 100.0 * t / self.durs[track], n, n, title, tip))

    def player(self):
        seen = {}
        out = []
        for track, cid, t, title, tip in self.pins:
            seen[track] = seen.get(track, 0) + 1
            out.append(self._pin_html(track, cid, t, title, tip, seen[track]))
        newpins = "".join(out)
        n_old = len(PIN_RUN.findall(self.dock))
        if not n_old:
            raise SystemExit("could not locate the existing pin run in the dock")
        dock, done = [], False
        def sub(m):
            nonlocal done
            if done:
                return ""
            done = True
            return newpins
        return PIN_RUN.sub(sub, self.dock)

    def ref(self, n):
        track, _, t = self.pins[n - 1][0], None, self.pins[n - 1][2]
        seen = 0
        for tr, _c, _t, _ti, _tp in self.pins[:n]:
            if tr == track:
                seen += 1
        trk = "" if self.is_wave else ' data-track="%s"' % track
        return '<button type="button" class="sv-ap-ref" data-t="%s"%s>%d</button>' % (("%g" % t), trk, seen)

    def add_statement(self, n, pin_title, heading, para, listen_for, extra=""):
        cid = self.pins[n - 1][1]
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        p1 = "<p %s>%s</p>" % (self.nid(), para)
        p2 = "<p %s><strong>Listen for:</strong> %s</p>" % (self.nid(), listen_for)
        trk = "" if self.is_wave else ' data-track="%s"' % self.pins[n - 1][0]
        self.cards.append(
            '<section class="sv-card sv-card--statement" data-title="%s"%s data-chapters="%s"'
            ' style="display:flex;align-items:center;justify-content:center">'
            '<div class="sv-card-body" style="max-width:640px;font-size:1.08em;column-count:1">%s%s%s%s</div></section>'
            % (pin_title, trk, cid, h, p1, p2, extra))

    def content(self):
        return self.player() + '<div class="sv-listening">' + "".join(self.cards) + '</div>'

    # ---- verification ---------------------------------------------------
    def verify(self, content, extra_text="", allow_img=False):
        errs, warns = [], []
        b = _Bal(); b.feed(content)
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

        pins = re.findall(r'class="sv-ap-pin"(?: data-track="(t\d)")? data-cid="([^"]+)" data-t="([\d.]+)" style="left:([\d.]+)%"', content)
        if len(pins) != len(self.pins):
            errs.append("%d pins rendered, %d expected" % (len(pins), len(self.pins)))
        cids = {c for _, c, _, _ in pins}
        for (trk, cid, t, pct), (etrk, ecid, et, _, _) in zip(pins, self.pins):
            d = self.durs[etrk]
            if abs(float(pct) - 100.0 * float(t) / d) > 0.02:
                errs.append("pin %s left=%s%% != %.2f%%" % (cid, pct, 100.0 * float(t) / d))
            if float(t) > d:
                errs.append("pin %s beyond track length" % cid)
            if not self.is_wave and trk != etrk:
                errs.append("pin %s wrong data-track" % cid)
        for tr in {p[0] for p in self.pins}:
            ts = [p[2] for p in self.pins if p[0] == tr]
            if ts != sorted(ts):
                errs.append("pins out of time order on %s" % tr)
        reft = re.findall(r'class="sv-ap-ref" data-t="([\d.]+)"', content)
        pint = {("%g" % p[2]) for p in self.pins}
        for t in reft:
            if t not in pint:
                errs.append("ref data-t=%s has no pin" % t)
        for cid in re.findall(r'data-chapters="([^"]+)"', content):
            for k in cid.split(","):
                if k.strip() not in cids:
                    errs.append("data-chapters=%s has no pin" % k)

        for m in re.finditer(r"%[sdr](?![a-zA-Z])", content):
            errs.append("unsubstituted format placeholder %r" % m.group(0))
        low = (content + extra_text).lower()
        if "video walkthrough" in low:
            errs.append('contains "Video walkthrough"')
        if "<iframe" in low or "youtube.com/embed" in low:
            errs.append("contains an embedded iframe")
        if not allow_img and "<img" in low:
            errs.append("contains an image")
        if self.board == "eduqas":
            for w in ("eduqas", "wjec"):
                if w in low:
                    errs.append("names the board: %s" % w)
        cards = re.findall(r'<section class="sv-card', content)
        cap = len(self.pins) + 2
        if len(cards) > cap:
            errs.append("%d cards (cap %d = pins + cover + checklist)" % (len(cards), cap))
        self.card_words = []
        for m in re.finditer(r'<section class="sv-card sv-card--statement".*?</section>', content, re.S):
            w = len(_html.unescape(re.sub(r"<[^>]+>", " ", m.group(0))).split())
            self.card_words.append(w)
            if w > 92:
                warns.append("statement card %d words" % w)
        for ch, name in (("—", "&mdash;"), ("‘", "&lsquo;"), ("’", "&rsquo;"),
                         ("“", "&ldquo;"), ("”", "&rdquo;"), ("–", "&ndash;")):
            if ch in content:
                errs.append("raw %s in content_html" % name)
        # the dock must be carried through untouched apart from pins and dur
        for marker in ("sv-ap-bar", "sv-ap-play", "sv-ap-tick", "sv-ap-wrap"):
            if marker not in content:
                errs.append("dock lost %s" % marker)
        if self.is_wave:
            for marker in ("sv-ap-canvas", "sv-ap-peaks", "data-audio", "data-peaks"):
                if marker not in content:
                    errs.append("wave dock lost %s" % marker)
        return errs, warns


def renumber_tail(deck, *htmls):
    """The live AQA lessons carry data-narration-id values inside exam_tip_html
    and conclusion_html (n19-n25). Those collide with the rebuilt deck's own
    n1..nN, which would give one page two elements with the same id and a
    narration manifest that cannot be mapped back. Renumber them to continue
    the deck's sequence instead."""
    out = []
    for h in htmls:
        if not h:
            out.append(h)
            continue
        def bump(m):
            deck._n += 1
            return 'data-narration-id="n%d"' % deck._n
        out.append(re.sub(r'data-narration-id="[^"]+"', bump, h))
    return out


def build_questions_keep(backup, practice=None, kcs=None, flashcards=None):
    """These lessons are live and Tom has QA'd them, so questions are carried
    over unchanged unless a replacement is passed in explicitly."""
    old = json.load(io.open(os.path.join(HERE, "backups", backup + ".json"), encoding="utf-8"))
    pq = practice if practice is not None else [dict(q) for q in old["practice_questions"]]
    kc = kcs if kcs is not None else [dict(q) for q in old["knowledge_checks"]]
    fc = flashcards if flashcards is not None else [dict(q) for q in old["flashcard_questions"]]
    return pq, kc, fc
