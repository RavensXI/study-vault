# -*- coding: utf-8 -*-
"""Shared builder for the guided-listening deck format approved on
music-edexcel/aos1-instrumental-music/L2 (Brandenburg 5/iii).

Structure produced:
  <figure class="sv-annotated-player sv-ap-yt"> docked player + numbered pins
  <div class="sv-listening">
     cover card, one statement card per pin, exam-checklist card
  </div>

Rules enforced by verify():
  * balanced tags
  * data-narration-id contiguous n1..nN over h2 + p
  * every sv-ap-ref data-t equals a pin data-t
  * every data-chapters equals a pin cid
  * pin left:% == t / dur * 100
  * no "Video walkthrough", no second embed, <= 9 cards, statements <= 90 words
  * no board name in Eduqas lessons
"""
import io, json, os, re, sys, html as _html
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "track", "wbr", "col", "area", "base", "embed", "param"}


class _Bal(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("stray </%s>" % tag)
        elif self.stack[-1] != tag:
            self.errors.append("</%s> closes <%s>" % (tag, self.stack[-1]))
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def dfn(term, d):
    return '<dfn class="term" data-def="%s">%s</dfn>' % (d, term)


class Deck(object):
    def __init__(self, lesson_id, subject, unit, lesson_no, yt, dur, track_label, credit, board=None):
        self.lesson_id = lesson_id
        self.subject, self.unit, self.lesson_no = subject, unit, lesson_no
        self.yt, self.dur = yt, int(dur)
        self.track_label, self.credit, self.board = track_label, credit, board
        self.pins = []          # (cid, seconds, title, tip)
        self.cards = []
        self._n = 0
        self.card_words = []

    # ---- helpers -------------------------------------------------------
    def nid(self):
        self._n += 1
        return 'data-narration-id="n%d"' % self._n

    def ref(self, n):
        t = self.pins[n - 1][1]
        return '<button type="button" class="sv-ap-ref" data-t="%d" data-track="t1">%d</button>' % (t, n)

    def _pin_html(self, cid, t, title, tip, n):
        return ('<button type="button" class="sv-ap-pin" data-track="t1" data-cid="%s" data-t="%d" '
                'style="left:%.2f%%">%d<span class="sv-ap-tip"><strong>%d &middot; %s</strong>%s</span></button>'
                % (cid, t, 100.0 * t / self.dur, n, n, title, tip))

    def player(self):
        return ('<figure class="sv-annotated-player sv-ap-yt" data-lesson-id="%s"><div class="sv-ap-bar">'
                '<button type="button" class="sv-ap-play">&#9654;</button>'
                '<span class="sv-ap-tick">0:00 / &ndash;:&ndash;&ndash;</span><div class="sv-ap-tracks">'
                '<button type="button" class="sv-ap-trackbtn sv-ap-trackbtn--on" data-track="t1" data-yt="%s" '
                'data-dur="%d">%s</button></div></div><div class="sv-ap-media"><div class="sv-ap-video">'
                '<div class="sv-ap-ytmount"></div></div><div class="sv-ap-wrap"><div class="sv-ap-track">'
                '<div class="sv-ap-trackfill"></div></div>' % (self.lesson_id, self.yt, self.dur, self.track_label)
                + "".join(self._pin_html(c, t, ti, tp, i + 1) for i, (c, t, ti, tp) in enumerate(self.pins))
                + '</div></div><figcaption class="sv-listen-credit">%s</figcaption></figure>' % self.credit)

    # ---- cards ---------------------------------------------------------
    def add_cover(self, heading, paras, title="The set work"):
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        body = "".join("<p %s>%s</p>" % (self.nid(), p) for p in paras)
        self.cards.append('<section class="sv-card sv-card--cover" data-title="%s">%s<div class="sv-card-body">%s</div></section>'
                          % (title, h, body))

    def add_statement(self, n, pin_title, heading, para, listen_for):
        cid = self.pins[n - 1][0]
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        p1 = "<p %s>%s</p>" % (self.nid(), para)
        p2 = "<p %s><strong>Listen for:</strong> %s</p>" % (self.nid(), listen_for)
        self.cards.append(
            '<section class="sv-card sv-card--statement" data-title="%d · %s" data-track="t1" data-chapters="%s"'
            ' style="display:flex;align-items:center;justify-content:center">'
            '<div class="sv-card-body" style="max-width:640px;font-size:1.08em;column-count:1">%s%s%s</div></section>'
            % (n, pin_title, cid, h, p1, p2))

    def add_checklist(self, summary, precision, heading="Say it precisely in the exam"):
        h = "<h2 %s>%s</h2>" % (self.nid(), heading)
        p1 = "<p %s>%s</p>" % (self.nid(), summary)
        p2 = "<p %s>%s</p>" % (self.nid(), precision)
        self.cards.append('<section class="sv-card" data-title="Exam checklist" data-track="t1">%s'
                          '<div class="sv-card-body">%s%s</div></section>' % (h, p1, p2))

    def content(self):
        return self.player() + '<div class="sv-listening">' + "".join(self.cards) + '</div>'

    # ---- verification --------------------------------------------------
    def verify(self, content, extra_text=""):
        errs, warns = [], []
        self.card_words = []
        b = _Bal()
        b.feed(content)
        if b.errors:
            errs += b.errors
        if b.stack:
            errs.append("unclosed: %s" % b.stack)

        ids = re.findall(r'data-narration-id="n(\d+)"', content)
        nums = [int(i) for i in ids]
        if nums != list(range(1, len(nums) + 1)):
            errs.append("narration ids not contiguous from n1: %s" % nums[:40])
        # every narration id must sit on an h2 or p
        for m in re.finditer(r"<(\w+)[^>]*data-narration-id=", content):
            if m.group(1) not in ("h2", "p"):
                errs.append("narration id on <%s>" % m.group(1))

        pin_t = {int(m) for m in re.findall(r'class="sv-ap-pin"[^>]*data-t="(\d+)"', content)}
        pin_cid = {m for m in re.findall(r'class="sv-ap-pin"[^>]*data-cid="([^"]+)"', content)}
        for t in re.findall(r'class="sv-ap-ref" data-t="(\d+)"', content):
            if int(t) not in pin_t:
                errs.append("sv-ap-ref data-t=%s has no pin" % t)
        for c in re.findall(r'data-chapters="([^"]+)"', content):
            if c not in pin_cid:
                errs.append("data-chapters=%s has no pin" % c)
        for m in re.finditer(r'class="sv-ap-pin"[^>]*data-t="(\d+)" style="left:([\d.]+)%"', content):
            t, pct = int(m.group(1)), float(m.group(2))
            if abs(pct - 100.0 * t / self.dur) > 0.02:
                errs.append("pin t=%d left=%.2f%% != %.2f%%" % (t, pct, 100.0 * t / self.dur))
        if len(pin_cid) != len(self.pins):
            errs.append("pin count mismatch")
        ts = [p[1] for p in self.pins]
        if ts != sorted(ts):
            errs.append("pins not in time order")
        if max(ts) > self.dur:
            errs.append("pin beyond video length")

        low = (content + extra_text).lower()
        if "video walkthrough" in low:
            errs.append('contains "Video walkthrough"')
        if "<iframe" in low or "youtube.com/embed" in low:
            errs.append("contains an embedded iframe")
        if self.board == "eduqas":
            for w in ("eduqas", "wjec"):
                if w in low:
                    errs.append("names the board: %s" % w)
        cards = re.findall(r'<section class="sv-card', content)
        if len(cards) > 9:
            errs.append("%d cards (max 9)" % len(cards))
        for m in re.finditer(r'<section class="sv-card sv-card--statement".*?</section>', content, re.S):
            txt = _html.unescape(re.sub(r"<[^>]+>", " ", m.group(0)))
            w = len(txt.split())
            self.card_words.append(w)
            if w > 88:
                warns.append("statement card %d words (exemplar range 68-76, cap ~90)" % w)
        # entity discipline: content_html should use entities, not raw curly punctuation
        for ch, name in (("—", "&mdash;"), ("‘", "&lsquo;"), ("’", "&rsquo;"),
                         ("“", "&ldquo;"), ("”", "&rdquo;"), ("–", "&ndash;")):
            if ch in content:
                errs.append("raw %s in content_html, use %s" % (repr(ch), name))
        return errs, warns


def check_plain(obj, label, errs):
    """question / KC / flashcard fields must be plain unicode, no entities, no tags."""
    s = json.dumps(obj, ensure_ascii=False)
    for bad in ("&mdash;", "&lsquo;", "&rsquo;", "&ldquo;", "&rdquo;", "&ndash;", "&amp;", "<p>", "<em>", "<strong>"):
        if bad in s:
            errs.append("%s contains %s" % (label, bad))


def patch(deck, payload, apply=False):
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
    print("PATCH", r.status_code, "" if r.status_code < 300 else r.text[:400])
    if r.status_code >= 300:
        raise SystemExit(1)
    return r.json()


def build_questions(backup, practice, kcs, flashcards):
    """Preserve the original shapes: practice = text/type('N marks - X')/marks(=mark scheme text),
    KC = q/type/options/correct, flashcards = q/a."""
    old = json.load(io.open(os.path.join(HERE, "backups", backup + ".json"), encoding="utf-8"))
    pq = []
    for i, q in enumerate(practice):
        base = dict(old["practice_questions"][i]) if i < len(old["practice_questions"]) else {}
        kind = q.get("kind")
        if not kind:
            t = base.get("type", "")
            kind = t.split("—")[-1].strip() if "—" in t else "Explanation"
        row = {"text": q["text"], "type": "%d mark%s — %s" % (q["marks"], "" if q["marks"] == 1 else "s", kind),
               "marks": q["mark_scheme"]}
        pq.append(row)
    kc = []
    for i, q in enumerate(kcs):
        kc.append({"q": q["q"], "type": "mcq", "correct": q["correct"], "options": q["options"]})
    fc = [{"q": f["q"], "a": f["a"]} for f in flashcards]
    return pq, kc, fc
