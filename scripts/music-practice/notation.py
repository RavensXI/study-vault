# -*- coding: utf-8 -*-
"""Engraved, ANNOTATED notation figures for the Score Reading lessons.

Why this exists: the unit used raw 19th-century scans, rendered at 40% of their
natural size, with nothing marked. A student who cannot read music was asked to
find a time signature in a wall of dots. See SCORE_READING_AUDIT.md.

Verovio engraves real notation to SVG and tags every element with a class
(meterSig, note, rest, clef...). We read each glyph's own coordinates out of the
SVG and draw the annotation in the same coordinate space, so a ring lands
exactly on the symbol instead of being placed by eye. Output is SVG, so it stays
sharp at any size — which also fixes the "87 pixels tall" problem.

Geometry notes (verovio 6.x), learned the hard way:
  <svg viewBox="0 0 W h">                     <- outer, page units
    <svg class="definition-scale" viewBox="0 0 CW CH">   <- content units
      <g class="page-margin" transform="translate(500, 500)">
Element coords (meterSig at 735,600) are relative to page-margin. Annotations go
in a sibling group carrying the SAME translate, so coordinates match directly.
Staff lines sit 180 content-units apart; that spacing is the unit for sizing.
"""
import json
import re

import verovio

ACCENT = "#7c3aed"     # house purple — annotation ink
INK = "#2d2a26"


def render(abc, scale=55, width=1800, height=400):
    tk = verovio.toolkit()
    tk.setOptions({
        "pageWidth": width, "pageHeight": height, "scale": scale,
        "adjustPageHeight": True, "header": "none", "footer": "none",
        "breaks": "none", "svgViewBox": True, "svgRemoveXlink": True,
    })
    if not tk.loadData(abc):
        raise RuntimeError("verovio could not parse the input")
    return tk.renderToSVG(1)


def _uses(svg, cls):
    """Every <use> inside <g class="cls">, as (x, y) in page-margin coords."""
    out = []
    for m in re.finditer(r'<g[^>]*class="%s"[^>]*>(.*?)</g>' % cls, svg, re.S):
        for u in re.finditer(r'transform="translate\((-?[\d.]+),\s*(-?[\d.]+)\)', m.group(1)):
            out.append((float(u.group(1)), float(u.group(2))))
    return out


def _group_extent(svg, cls):
    """The first <g class="cls"> group's glyphs as (x_min, x_max, y_mid), or
    None. A two-letter dynamic (mf) is two <use> glyphs; ringing only the
    first clipped the f and collided with a note stem (Tom's review, 15 Aug)."""
    m = re.search(r'<g[^>]*class="%s"[^>]*>(.*?)</g>' % cls, svg, re.S)
    if not m:
        return None
    pts = [(float(u.group(1)), float(u.group(2))) for u in
           re.finditer(r'transform="translate\((-?[\d.]+),\s*(-?[\d.]+)\)', m.group(1))]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    return min(xs), max(xs), sum(p[1] for p in pts) / len(pts)


def _staff_unit(svg):
    ys = sorted(set(float(y) for y in re.findall(r'<path d="M0 ([\d.]+) L\d', svg)))
    return (ys[1] - ys[0]) if len(ys) > 1 else 180.0


def _staff_bottom(svg):
    ys = sorted(set(float(y) for y in re.findall(r'<path d="M0 ([\d.]+) L\d', svg)))
    return ys[-1] if ys else 960.0


REF_WIDTH = 5600.0   # content units that fill the column; keeps glyph size constant


def card(svg, title=None, caption=None):
    """Wrap a figure for display. Title and caption are HTML, not SVG text — SVG
    text cannot wrap, so long titles ran off the edge of the drawing."""
    h = ['<figure class="sv-notefig">']
    if title:
        h.append('<figcaption class="sv-notefig-title">%s</figcaption>' % title)
    h.append(svg)
    if caption:
        h.append('<p class="sv-notefig-cap">%s</p>' % caption)
    h.append("</figure>")
    return "".join(h)


def figure(abc, ring=None, note_labels=None, brackets=None, stagger=False,
           bare=False, scale=55, width=1800):
    """Engrave `abc` and annotate it. Returns the SVG only — use card() for
    title and caption.

    ring         [(class, label)]      ring the first element of that class
    note_labels  [(index, text)]       label notes by their order in the bar
    brackets     [(i0, i1, text)]      bracket spanning notes i0..i1
    stagger      alternate note labels between two rows when they would collide
    bare         drop the clef and time signature — for anatomy figures where a
                 repeated clef in every cell is just noise
    """
    svg = render(abc, scale=scale, width=width)
    dm = re.search(r'(<svg class="definition-scale"[^>]*viewBox=")([\d.\- ]+)(")', svg)
    cvb = [float(v) for v in dm.group(2).split()]
    cvb_w = cvb[2]
    u = _staff_unit(svg)
    fs = u * 1.5
    pad_top = fs * 0.8 + (fs * 2.0 if ring else 0)
    ring_below = any(_uses(svg, c) and _uses(svg, c)[0][1] > _staff_bottom(svg)
                     for c, _ in (ring or []))
    pad_bot = fs * 0.6 + (fs * 2.6 if ring_below else 0)
    if brackets:
        pad_bot += fs * (2.4 + (0.95 if len(brackets) > 1 else 0))
    if note_labels:
        pad_bot += fs * (1.6 + (0.9 if stagger else 0))

    a = []

    def text(x, y, s, anchor="middle", colour=ACCENT, size=None, weight="600", style=""):
        a.append('<text x="%.0f" y="%.0f" text-anchor="%s" fill="%s" '
                 'font-family="Inter, system-ui, sans-serif" font-size="%.0f" '
                 'font-weight="%s" %s>%s</text>' % (x, y, anchor, colour, size or fs, weight, style, s))

    # keep a label inside the frame: near an edge, anchor to it instead of centring
    def edge_safe(cx, s, size):
        half = len(s) * size * 0.27
        lo, hi = -400, cvb_w - 900
        if cx - half < lo:
            return lo + half * 0.0, "start"
        if cx + half > hi:
            return hi, "end"
        return cx, "middle"

    for cls, lbl in (ring or []):
        ext = _group_extent(svg, cls)
        if not ext:
            continue
        x0, x1, y = ext
        # a meter/clef glyph is centred on the middle staff line, ~2 spaces each
        # way. Dynamics anchor at their left edge and "mf" is one wide <use>
        # glyph (so extent cannot see its width) — shift and widen empirically,
        # screenshot-verified against the m and the f both sitting inside.
        wide = cls == "dynam"
        cx, cy = (x0 + x1) / 2 + u * (1.0 if wide else 0.35), y
        rx = max(u * (1.5 if wide else 0.95), (x1 - x0) / 2 + u * 0.9)
        ry = u * 1.7
        a.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="none" stroke="%s" '
                 'stroke-width="%.0f"/>' % (cx, cy, rx, ry, ACCENT, u * 0.13))
        # Elements below the stave (dynamics) need the label BELOW them, or it is
        # drawn straight over the notes — which is what happened in the narrow
        # method-card column where there is no spare width to escape sideways.
        below = y > _staff_bottom(svg)
        lx, anchor = edge_safe(cx, lbl, fs)
        if below:
            ty = cy + ry + fs * 1.15
            a.append('<path d="M %.0f %.0f L %.0f %.0f" stroke="%s" stroke-width="%.0f"/>'
                     % (cx, cy + ry + u * 0.12, cx, ty - fs * 0.85, ACCENT, u * 0.11))
        else:
            ty = cy - ry - fs * 0.8
            a.append('<path d="M %.0f %.0f L %.0f %.0f" stroke="%s" stroke-width="%.0f"/>'
                     % (cx, ty + fs * 0.3, cx, cy - ry - u * 0.12, ACCENT, u * 0.11))
        text(lx, ty, lbl, anchor=anchor)

    notes = _uses(svg, "note")
    base = _staff_bottom(svg)
    for li, (i, s) in enumerate(note_labels or []):
        if i >= len(notes):
            continue
        dy = u * (2.2 + (1.5 if (stagger and li % 2) else 0))
        lx, anchor = edge_safe(notes[i][0] + u * 0.3, s, fs * 0.88)
        text(lx, base + dy, s, anchor=anchor, size=fs * 0.88, colour=INK, weight="500")

    for bi, (i0, i1, s) in enumerate(brackets or []):
        if i1 >= len(notes):
            continue
        x0, x1 = notes[i0][0] - u * 0.6, notes[i1][0] + u * 1.0
        yb = base + u * 3.4
        a.append('<path d="M %.0f %.0f L %.0f %.0f L %.0f %.0f L %.0f %.0f" fill="none" '
                 'stroke="%s" stroke-width="%.0f"/>'
                 % (x0, yb - u * 0.6, x0, yb, x1, yb, x1, yb - u * 0.6, ACCENT, u * 0.12))
        lx, anchor = edge_safe((x0 + x1) / 2, s, fs * 0.86)
        text(lx, yb + fs * (1.0 + (0.95 if bi % 2 else 0)), s, anchor=anchor, size=fs * 0.86)

    # widen the canvas so nothing is clipped
    new_h = cvb[3] + pad_top + pad_bot
    svg = svg[:dm.start(2)] + "0 0 %.0f %.0f" % (cvb[2], new_h) + svg[dm.end(2):]
    svg = re.sub(r'(<g class="page-margin" transform="translate\(500, )500(\))',
                 lambda m: m.group(1) + "%.0f" % (500 + pad_top) + m.group(2), svg, count=1)

    om = re.search(r'(<svg viewBox=")([\d.\- ]+)(")', svg)
    ovb = [float(v) for v in om.group(2).split()]
    ratio = cvb[2] / ovb[2] if ovb[2] else 18.1
    svg = svg[:om.start(2)] + "0 0 %.0f %.0f" % (ovb[2], new_h / ratio) + svg[om.end(2):]

    annot = '<g class="sv-annot" transform="translate(500, %.0f)">%s</g>' % (500 + pad_top, "".join(a))
    k = svg.rfind("</svg>", 0, svg.rfind("</svg>"))
    svg = svg[:k] + annot + svg[k:]

    # Render every figure at the SAME notational size: a narrow example occupies
    # less of the column rather than being stretched to fill it. Without this a
    # 2-bar figure and a 6-bar figure show glyphs at wildly different sizes.
    pct = min(100.0, round(cvb_w / REF_WIDTH * 100.0, 1))
    svg = svg.replace("<svg ", '<svg style="width:%s%%;height:auto;display:block;margin:0 auto" ' % pct, 1)
    if bare:
        # Hide, do not delete. Deleting these groups by regex removed the
        # noteheads twice: <g class="keySig" /> is self-closing, so a
        # <g ...>...</g> match runs past it and swallows the notes. Injected
        # LAST because adding an attribute earlier breaks the viewBox regexes.
        svg = svg.replace('<svg ', '<svg data-bare="1" ', 1)
        svg = svg.replace('</defs>', '</defs><style>svg[data-bare="1"] g.clef,'
                          'svg[data-bare="1"] g.meterSig,'
                          'svg[data-bare="1"] g.keySig{display:none}</style>', 1)
    return svg


def row(items, title=None, caption=None):
    """Lay several small figures side by side, each with its own HTML caption.

    Long labels under closely-spaced notes always collide inside one drawing.
    Giving each note its own cell removes the problem entirely, and the captions
    wrap and re-flow because they are HTML rather than SVG text.
    items: [(abc, caption_html)]
    """
    cells = []
    for abc, cap in items:
        cells.append('<div class="sv-noterow-cell">%s<span class="sv-noterow-cap">%s</span></div>'
                     % (figure(abc, width=520, bare=True), cap))
    h = ['<figure class="sv-notefig">']
    if title:
        h.append('<figcaption class="sv-notefig-title">%s</figcaption>' % title)
    h.append('<div class="sv-noterow">%s</div>' % "".join(cells))
    if caption:
        h.append('<p class="sv-notefig-cap">%s</p>' % caption)
    h.append("</figure>")
    return "".join(h)


def playable(abc, notes, tempo=100, width=1500, title=None, caption=None,
             hint="Press play and watch the notes light up as they sound."):
    """Engraved notation that plays, with a highlight moving note by note.

    notes: [(midi, beats)] or [(midi, beats, opts)] in the same order the notes
    appear. Passed explicitly rather than parsed out of the ABC — the pairing
    with the engraved element ids is asserted below, so a mismatch fails loudly
    instead of drifting silently. Use midi=None for a rest.

    opts (dict, optional): {"vel": 0..1, "art": "stac"|"leg"} — performed
    loudness and articulation. The player's clock always advances by the full
    printed beats; staccato must NOT be faked by shortening beats (that made
    staccato bars rush — Tom's Extract F report, 15 Aug).
    """
    svg = figure(abc, width=width)
    ids = re.findall(r'<g id="([^"]+)" class="note"', svg)
    # midi=None  -> a rest: advances the clock, claims no engraved note
    # midi=False -> printed but NOT played: claims an engraved note, makes no
    #               sound and no highlight. This is what makes "spot where the
    #               performance departs from the score" possible.
    claims = [n for n in notes if n[0] is not None]
    if len(ids) != len(claims):
        raise ValueError("%d engraved notes but %d claimed (%s)" % (len(ids), len(claims), abc))
    # Rests advance the clock but claim no engraved note: they render as
    # class="rest", so pairing them against note ids silently mis-aligns
    # everything after the first rest.
    seq, k = [], 0
    for n in notes:
        midi, beats = n[0], n[1]
        opts = n[2] if len(n) > 2 else {}
        if midi is None:                       # rest
            seq.append({"id": None, "midi": None, "beats": beats})
        elif midi is False:                    # printed, never played
            k += 1
            seq.append({"id": None, "midi": None, "beats": beats})
        else:
            d = {"id": ids[k], "midi": midi, "beats": beats}
            if "vel" in opts:
                d["vel"] = opts["vel"]
            if "art" in opts:
                d["art"] = opts["art"]
            seq.append(d)
            k += 1
    payload = json.dumps({"tempo": tempo, "notes": seq}, separators=(",", ":"))
    h = ['<figure class="sv-scoreplay">']
    if title:
        h.append('<figcaption class="sv-notefig-title">%s</figcaption>' % title)
    h.append('<script type="application/json" class="sv-sp-map">%s</script>' % payload)
    h.append(svg)
    h.append('<div class="sv-sp-bar"><button type="button" class="sv-sp-play">Play</button>'
             '<span class="sv-sp-hint">%s</span></div>' % hint)
    if caption:
        h.append('<p class="sv-notefig-cap">%s</p>' % caption)
    h.append("</figure>")
    return "".join(h)
