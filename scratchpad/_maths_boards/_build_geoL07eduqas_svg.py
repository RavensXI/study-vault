# -*- coding: utf-8 -*-
"""SVG figure library for eduqas geometry-L07 Circle Theorems.
All figures theme-safe: currentColor strokes/text, soft opacity fills.
Coordinates reuse the Tom-approved maths-aqa geometry-L07 figures where the
geometry matches, with number/label swaps."""

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def svg_cc(centre, circ, aria):
    """Angle at centre (text bottom, between O and chord AB) and at
    circumference (text top, at C). Pass '' to hide a slot."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="84.0" r="52.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="120.0" y1="84.0" x2="75.9" y2="111.6" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="84.0" x2="164.1" y2="111.6" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="32.0" x2="75.9" y2="111.6" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="32.0" x2="164.1" y2="111.6" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="75.9" cy="111.6" r="2.1" fill="currentColor"/>'
      '<circle cx="164.1" cy="111.6" r="2.1" fill="currentColor"/>'
      '<circle cx="120.0" cy="32.0" r="2.1" fill="currentColor"/>'
      '<text x="120.0" y="98.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="60.0" y="120.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="180.0" y="120.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="120.0" y="24.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="120.0" y="112.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="120.0" y="50.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, centre, circ)) + CAP

def svg_semicircle_plain(aria):
    """AB diameter, C on circle, ? at C (angle in semicircle). No marks."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="84.0" r="52.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="68.0" y1="84.0" x2="172.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="142.8" y1="37.3" x2="68.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="142.8" y1="37.3" x2="172.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="68.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="172.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="142.8" cy="37.3" r="2.1" fill="currentColor"/>'
      '<text x="56.0" y="88.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="184.0" y="88.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="150.0" y="30.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="112.0" y="96.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="132.0" y="54.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">?</text>'
      '</svg>' % aria) + CAP

def svg_semicircle_marked(a_ang, b_ang, aria):
    """AB diameter, C on circle with right-angle mark at C; angle at A and B."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="84.0" r="52.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="68.0" y1="84.0" x2="172.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="142.8" y1="37.3" x2="68.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="142.8" y1="37.3" x2="172.0" y2="84.0" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="68.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="172.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="142.8" cy="37.3" r="2.1" fill="currentColor"/>'
      '<path d="M135.2,42.0 L139.9,49.7 L147.6,44.9" fill="none" stroke="currentColor" stroke-width="1.3"/>'
      '<text x="56.0" y="88.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="184.0" y="88.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="150.0" y="30.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="112.0" y="96.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="86.0" y="80.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="156.0" y="80.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, a_ang, b_ang)) + CAP

def svg_cyclicquad(a, b, c, d, aria):
    """ABCD inscribed quad. A top-left, B top-right, C bottom-right, D bottom-left.
    Opposite pairs (A,C) and (B,D)."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="82.0" r="54.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<polygon points="86.8,39.4 153.2,39.4 153.2,124.6 86.8,124.6" fill="#60a5fa" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="86.8" cy="39.4" r="2.1" fill="currentColor"/>'
      '<circle cx="153.2" cy="39.4" r="2.1" fill="currentColor"/>'
      '<circle cx="153.2" cy="124.6" r="2.1" fill="currentColor"/>'
      '<circle cx="86.8" cy="124.6" r="2.1" fill="currentColor"/>'
      '<text x="76.0" y="32.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="164.0" y="32.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="166.0" y="136.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="74.0" y="136.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">D</text>'
      '<text x="101.0" y="55.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="139.0" y="55.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="139.0" y="113.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="101.0" y="113.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, a, b, c, d)) + CAP

def svg_samesegment(left, right, aria):
    """Two angles in the same segment standing on chord AB. left at P, right at Q."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="82.0" r="52.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="80.2" y1="48.6" x2="80.2" y2="115.4" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="80.2" y1="48.6" x2="159.8" y2="115.4" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="159.8" y1="48.6" x2="80.2" y2="115.4" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="159.8" y1="48.6" x2="159.8" y2="115.4" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="80.2" y1="115.4" x2="159.8" y2="115.4" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="80.2" cy="115.4" r="2.1" fill="currentColor"/>'
      '<circle cx="159.8" cy="115.4" r="2.1" fill="currentColor"/>'
      '<circle cx="80.2" cy="48.6" r="2.1" fill="currentColor"/>'
      '<circle cx="159.8" cy="48.6" r="2.1" fill="currentColor"/>'
      '<text x="74.2" y="128.4" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="165.8" y="128.4" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="70.2" y="46.6" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">P</text>'
      '<text x="169.8" y="46.6" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">Q</text>'
      '<text x="88.2" y="63.6" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="151.8" y="63.6" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, left, right)) + CAP

def svg_tangent_radius(aria):
    """Tangent meets radius at T. ? marks the angle."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="80.0" r="48.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="120.0" y1="80.0" x2="120.0" y2="128.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="70.0" y1="128.0" x2="170.0" y2="128.0" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="80.0" r="2.1" fill="currentColor"/>'
      '<circle cx="120.0" cy="128.0" r="2.1" fill="currentColor"/>'
      '<text x="110.0" y="78.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="120.0" y="143.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">T</text>'
      '<text x="133.0" y="120.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">?</text>'
      '</svg>' % aria) + CAP

def svg_two_tangents(length, aria):
    """Two tangents from external point T to A and B. length on TA, ? on TB."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="150.0" cy="84.0" r="42.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="40.0" y1="84.0" x2="114.4" y2="61.7" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="40.0" y1="84.0" x2="114.4" y2="106.3" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="40.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<circle cx="114.4" cy="61.7" r="2.1" fill="currentColor"/>'
      '<circle cx="114.4" cy="106.3" r="2.1" fill="currentColor"/>'
      '<circle cx="150.0" cy="84.0" r="2.1" fill="currentColor"/>'
      '<text x="32.0" y="88.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">T</text>'
      '<text x="112.4" y="55.7" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="112.4" y="120.3" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="158.0" y="88.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="77.2" y="66.9" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="77.2" y="108.1" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">?</text>'
      '</svg>' % (aria, length)) + CAP

def svg_altsegment(tc, alt, aria):
    """Tangent at A (bottom), chord AB, point C in alternate segment.
    tc = tangent-chord angle at A; alt = angle in alternate segment at C."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="80.0" r="50.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="64.0" y1="134.0" x2="176.0" y2="134.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="134.0" x2="159.4" y2="53.2" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="76.7" y1="59.0" x2="120.0" y2="134.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="76.7" y1="59.0" x2="159.4" y2="53.2" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="134.0" r="2.1" fill="currentColor"/>'
      '<circle cx="159.4" cy="53.2" r="2.1" fill="currentColor"/>'
      '<circle cx="76.7" cy="59.0" r="2.1" fill="currentColor"/>'
      '<text x="120.0" y="148.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="169.4" y="51.2" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="65.7" y="57.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="138.0" y="125.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="92.7" y="73.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, tc, alt)) + CAP

def svg_tangent_chord_centre(tc, centre, aria):
    """Tangent at A (bottom), chord AB, radii OA and OB, centre O.
    tc = tangent-chord angle at A; centre = angle AOB."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="78.0" r="48.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="66.0" y1="126.0" x2="174.0" y2="126.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="126.0" x2="156.8" y2="47.1" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="78.0" x2="120.0" y2="126.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="78.0" x2="156.8" y2="47.1" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="78.0" r="2.1" fill="currentColor"/>'
      '<circle cx="120.0" cy="126.0" r="2.1" fill="currentColor"/>'
      '<circle cx="156.8" cy="47.1" r="2.1" fill="currentColor"/>'
      '<text x="120.0" y="140.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="167.8" y="46.1" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="108.0" y="80.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="138.0" y="117.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="120.0" y="64.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, tc, centre)) + CAP

def svg_isosceles_major(base, circ, aria):
    """O centre, radii OA OB (isosceles), C on major arc (top). base at A, circ ? at C."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="80.0" r="52.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="120.0" y1="80.0" x2="71.1" y2="97.8" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="80.0" x2="168.9" y2="97.8" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="28.0" x2="71.1" y2="97.8" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="28.0" x2="168.9" y2="97.8" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="71.1" y1="97.8" x2="168.9" y2="97.8" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="80.0" r="2.1" fill="currentColor"/>'
      '<circle cx="71.1" cy="97.8" r="2.1" fill="currentColor"/>'
      '<circle cx="168.9" cy="97.8" r="2.1" fill="currentColor"/>'
      '<circle cx="120.0" cy="28.0" r="2.1" fill="currentColor"/>'
      '<text x="62.1" y="101.8" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="177.9" y="101.8" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="112.0" y="84.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="120.0" y="22.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">C</text>'
      '<text x="120.0" y="46.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="87.1" y="95.8" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, circ, base)) + CAP

def svg_tangent_chord_radius(tc, cr, aria):
    """Tangent at A (horizontal), radius OA (up), chord AB up-right.
    tc = tangent-chord angle (marked), cr = chord-radius angle (?)."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="66.0" r="56.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="60.0" y1="122.0" x2="180.0" y2="122.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="122.0" x2="120.0" y2="66.0" stroke="currentColor" stroke-width="1.6"/>'
      '<line x1="120.0" y1="122.0" x2="175.2" y2="56.3" stroke="currentColor" stroke-width="1.6"/>'
      '<path d="M111.0,122.0 L111.0,113.0 L120.0,113.0" fill="none" stroke="currentColor" stroke-width="1.2"/>'
      '<circle cx="120.0" cy="66.0" r="2.1" fill="currentColor"/>'
      '<circle cx="120.0" cy="122.0" r="2.1" fill="currentColor"/>'
      '<circle cx="175.2" cy="56.3" r="2.1" fill="currentColor"/>'
      '<text x="108.0" y="64.0" font-size="10" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '<text x="120.0" y="136.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">A</text>'
      '<text x="185.0" y="54.0" font-size="12" text-anchor="middle" font-weight="600" fill="currentColor">B</text>'
      '<text x="141.0" y="116.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '<text x="112.0" y="104.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">%s</text>'
      '</svg>' % (aria, tc, cr)) + CAP

def svg_chord_through_centre(aria):
    """A chord passing through the centre O (a diameter)."""
    return (
      '<svg viewBox="0 0 240 160" role="img" aria-label="%s" style="max-width:280px;font-family:Inter,sans-serif" stroke-linecap="round">'
      '<circle cx="120.0" cy="80.0" r="50.0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
      '<line x1="70.0" y1="80.0" x2="170.0" y2="80.0" stroke="currentColor" stroke-width="1.6"/>'
      '<circle cx="120.0" cy="80.0" r="2.1" fill="currentColor"/>'
      '<circle cx="70.0" cy="80.0" r="2.1" fill="currentColor"/>'
      '<circle cx="170.0" cy="80.0" r="2.1" fill="currentColor"/>'
      '<text x="120.0" y="72.0" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">O</text>'
      '</svg>' % aria) + CAP

if __name__ == "__main__":
    # quick self-check: sizes lean, contain required attrs
    for name, s in [
        ("cc", svg_cc("140°","?","x")),
        ("semi_plain", svg_semicircle_plain("x")),
        ("semi_marked", svg_semicircle_marked("34°","?","x")),
        ("quad", svg_cyclicquad("72°","","?","","x")),
        ("same", svg_samesegment("48°","x","x")),
        ("tanrad", svg_tangent_radius("x")),
        ("twotan", svg_two_tangents("12 cm","x")),
        ("altseg", svg_altsegment("65°","?","x")),
        ("tcc", svg_tangent_chord_centre("65°","?","x")),
        ("iso", svg_isosceles_major("26°","?","x")),
        ("tcr", svg_tangent_chord_radius("50°","?","x")),
        ("chord", svg_chord_through_centre("x")),
    ]:
        assert "viewBox" in s and 'role="img"' in s and "aria-label" in s, name
        assert "http" not in s.lower(), name
        print(name, len(s))
