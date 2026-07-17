# -*- coding: utf-8 -*-
import io

# --- Square-numbers dot figure: 1, 4, 9, 16 as square dot arrays ---
s = 9       # dot spacing
r = 2.6     # dot radius
gap = 16    # gap between patterns
pad = 10
counts = [1, 2, 3, 4]  # side lengths -> 1,4,9,16 dots
base_y = pad + 4 * s    # bottom row baseline (tallest = 4 dots tall)
dots = []
labels = []
x = pad
for n in counts:
    span = (n - 1) * s
    # dots: n cols x n rows, bottom aligned at base_y
    for cx in range(n):
        for cy in range(n):
            dx = x + cx * s
            dy = base_y - cy * s
            dots.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#60a5fa" fill-opacity="0.85" stroke="currentColor" stroke-width="0.6"/>' % (dx, dy, r))
    labels.append('<text x="%.1f" y="%.0f" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%d</text>' % (x + span / 2.0, base_y + 16, n * n))
    x += span + gap
vw = x - gap + pad
vh = base_y + 24
svg_sq = ('<svg viewBox="0 0 %d %d" role="img" aria-label="The square numbers shown as dot squares: 1, 4, 9, 16" style="max-width:280px;width:100%%;height:auto">'
          % (vw, vh)) + "".join(dots) + "".join(labels) + '</svg>'

# --- Function machine flow figure for the opener ---
# input box -> [x2] -> [+3] -> output box, arrows between
def box(x, y, w, h, txt, fill=None):
    f = ' fill="%s" fill-opacity="0.25"' % fill if fill else ' fill="none"'
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="6" stroke="currentColor" stroke-width="1.4"%s/>'
            '<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">%s</text>'
            % (x, y, w, h, f, x + w // 2, y + h // 2 + 4, txt))

def arrow(x1, x2, y):
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>'
            '<path d="M%d %d l-6 -3 v6 z" fill="currentColor"/>' % (x1, y, x2 - 6, y, x2 - 6, y))

y = 18
h = 30
parts = []
parts.append(box(6, y, 44, h, 'in'))
parts.append(arrow(50, 76, y + h // 2))
parts.append(box(76, y, 44, h, '× 2', '#60a5fa'))
parts.append(arrow(120, 146, y + h // 2))
parts.append(box(146, y, 44, h, '+ 3', '#34d399'))
parts.append(arrow(190, 216, y + h // 2))
parts.append(box(216, y, 44, h, 'out'))
svg_machine = ('<svg viewBox="0 0 266 66" role="img" aria-label="A function machine: input, times 2, then plus 3, giving the output" style="max-width:280px;width:100%;height:auto">'
               + "".join(parts) + '</svg>')

io.open("_svg_square.txt", "w", encoding="utf-8").write(svg_sq)
io.open("_svg_machine.txt", "w", encoding="utf-8").write(svg_machine)
print("square svg len", len(svg_sq))
print("machine svg len", len(svg_machine))
print(svg_sq[:200])
