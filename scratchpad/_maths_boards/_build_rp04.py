# -*- coding: utf-8 -*-
import json

live = json.load(open("_live_rp04.json", encoding="utf-8"))

# ---------- SVG helpers ----------
def tickets_svg():
    parts = ['<svg viewBox="0 0 250 70" role="img" aria-label="Five cinema tickets costing forty pounds in total" style="max-width:100%" font-family="Inter, sans-serif">']
    x = 11.0
    for i in range(5):
        parts.append('<rect x="%.1f" y="12" width="38" height="30" rx="4" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % x)
        parts.append('<text x="%.1f" y="31" text-anchor="middle" font-size="10" fill="currentColor">%d</text>' % (x + 19, i + 1))
        x += 46.0
    parts.append('<text x="125" y="58" text-anchor="middle" font-size="11" fill="currentColor">£40 total for 5 tickets</text>')
    parts.append('</svg>')
    return "".join(parts)

def graph_svg(pts, mark, xmax, ymax, aria, curve=False, color="#3b82f6"):
    # coordinate frame
    ox, oy = 34.0, 132.0          # origin pixel
    W, H = 176.0, 116.0           # axis pixel span
    def px(x): return ox + (x / xmax) * W
    def py(y): return oy - (y / ymax) * H
    s = ['<svg viewBox="0 0 224 156" role="img" aria-label="%s" style="max-width:100%%" font-family="Inter, sans-serif">' % aria]
    # axes
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (ox, oy, ox + W + 6, oy))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (ox, oy, ox, oy - H - 6))
    # data path
    d = " ".join(("%s%.1f,%.1f" % ("M" if i == 0 else "L", px(x), py(y))) for i, (x, y) in enumerate(pts))
    s.append('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (d, color))
    # marked point
    mx, my = mark
    s.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#f59e0b" stroke="currentColor" stroke-width="0.5"/>' % (px(mx), py(my)))
    s.append('<text x="%.1f" y="%.1f" font-size="10" fill="currentColor">(%s, %s)</text>' % (px(mx) + 5, py(my) - 4, mx, my))
    # axis titles
    s.append('<text x="%.1f" y="%.1f" font-size="11" fill="currentColor">x</text>' % (ox + W + 2, oy + 14))
    s.append('<text x="%.1f" y="%.1f" font-size="11" fill="currentColor">y</text>' % (ox - 10, oy - H - 2))
    s.append('<text x="%.1f" y="%.1f" font-size="10" fill="currentColor">O</text>' % (ox - 11, oy + 12))
    s.append('</svg>')
    return "".join(s)

direct_graph = graph_svg([(0, 0), (11, 33)], (4, 12), 11.0, 33.0,
    "Straight line of direct proportion through the origin and the point 4, 12", color="#3b82f6")
inv_pts = [(2, 12), (3, 8), (4, 6), (6, 4), (8, 3), (12, 2)]
inverse_graph = graph_svg(inv_pts, (3, 8), 13.0, 13.0,
    "Reciprocal curve of inverse proportion through the point 3, 8", curve=True, color="#34d399")

# ---------- method_card (slim) ----------
method_card = {
    "title": "Direct & Inverse Proportion",
    "steps": [
        "Decide direct (y = kx) or inverse (y = k ÷ x).",
        "Find k from the pair you are given.",
        "Substitute k to find the unknown.",
        "Check: direct keeps y ÷ x = k; inverse keeps x × y = k.",
    ],
    "content": "<p><strong>Direct proportion:</strong> \\(y = kx\\). As \\(x\\) doubles, \\(y\\) doubles. Find \\(k\\) by \\(y \\div x\\).</p><p><strong>Inverse proportion:</strong> \\(y = \\frac{k}{x}\\). As \\(x\\) doubles, \\(y\\) halves. Find \\(k\\) by \\(y \\times x\\).</p><p>Find \\(k\\) from the known pair, then substitute to find any unknown. The <strong>unit method</strong> (find one item, then scale) works for everyday proportion.</p>",
    "example": "<p><strong>y is directly proportional to x. When x = 4, y = 20. Find y when x = 7.</strong></p><p>\\(k = 20 \\div 4 = 5\\), so \\(y = 5 \\times 7 = 35\\).</p>",
}

# ---------- tier guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: one step of proportion",
        "steps": [
            "<strong>Direct</strong> (\\(y = kx\\)): as \\(x\\) goes up, \\(y\\) goes up. Find \\(k = y \\div x\\).",
            "<strong>Inverse</strong> (\\(y = k \\div x\\)): as \\(x\\) goes up, \\(y\\) goes down. Find \\(k = y \\times x\\).",
            "<strong>Unit method:</strong> find the value of one item first, then multiply for the amount you want.",
        ],
        "example": {
            "question": "y is directly proportional to x. When x = 4, y = 20. Find y when x = 7.",
            "steps": [
                {"label": "Find k", "content": "<p>\\(k = 20 \\div 4 = 5\\).</p>"},
                {"label": "Use k", "content": "<p>\\(y = 5 \\times 7 = 35\\).</p>"},
                {"label": "Check", "content": "<p>\\(35 \\div 7 = 5 = k\\).</p>"},
                {"label": "Answer", "content": "<p>\\(y = 35\\).</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: find k, then the unknown",
        "steps": [
            "Find \\(k\\) from the pair you know, then work back: direct \\(x = y \\div k\\); inverse \\(x = k \\div y\\).",
            "For <strong>inverse</strong> problems (machines, workers), the product \\(x \\times y\\) stays constant.",
            "On a graph, <strong>direct proportion</strong> is a straight line through the origin, \\(y = kx\\).",
        ],
        "example": {
            "question": "y is inversely proportional to x. When x = 3, y = 8. Find y when x = 4.",
            "steps": [
                {"label": "Find k", "content": "<p>\\(k = 3 \\times 8 = 24\\).</p>"},
                {"label": "Use k", "content": "<p>\\(y = 24 \\div 4 = 6\\).</p>"},
                {"label": "Check", "content": "<p>\\(4 \\times 6 = 24 = k\\).</p>"},
                {"label": "Answer", "content": "<p>\\(y = 6\\).</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: multi-step proportion",
        "steps": [
            "Break it into steps: find \\(k\\), substitute, then answer exactly what is asked.",
            "<strong>Worker-days:</strong> total work = people × time, and it stays constant as people change.",
            "If \\(y\\) is proportional to <strong>\\(x^2\\)</strong>, square \\(x\\) before finding or using \\(k\\).",
        ],
        "example": {
            "question": "y is directly proportional to x². When x = 2, y = 20. Find y when x = 4.",
            "steps": [
                {"label": "Square x", "content": "<p>\\(2^2 = 4\\).</p>"},
                {"label": "Find k", "content": "<p>\\(k = 20 \\div 4 = 5\\).</p>"},
                {"label": "New x²", "content": "<p>\\(4^2 = 16\\).</p>"},
                {"label": "Check", "content": "<p>\\(80 \\div 16 = 5 = k\\).</p>"},
                {"label": "Answer", "content": "<p>\\(y = 5 \\times 16 = 80\\).</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided: opener + teach ----------
guided = {
    "opener": {
        "label": "Before any method",
        "display": "5 cinema tickets cost £40. All tickets are the same price.<br>" + tickets_svg(),
        "steps": [
            {"say": "No formula yet, just share the money out.", "pre": "One ticket costs £", "post": "", "answer": 8, "hint": "Share £40 between 5 tickets: 40 ÷ 5."},
            {"say": "Now scale up to more tickets.", "pre": "So 8 tickets cost £", "post": "", "answer": 64, "hint": "8 tickets at £8 each."},
            {"say": "You just used <strong>direct proportion</strong>. You found the cost of one ticket (£8, the constant \\(k\\)), then multiplied: cost = 8 × tickets, or \\(y = kx\\). Sometimes more of one thing means less of the other (more workers, fewer days): that is <strong>inverse proportion</strong>, where you multiply the pair to find \\(k\\)."},
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: find k and scale",
            "display": "y is directly proportional to x. When x = 4, y = 12. Find y when x = 10.<br>" + direct_graph,
            "steps": [
                {"say": "Direct proportion means \\(y = kx\\). Find \\(k\\) by dividing y by x.", "pre": "12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide 12 by 4."},
                {"say": "Now use \\(k = 3\\) with the new x = 10.", "pre": "3 × 10 = ", "post": "", "answer": 30, "hint": "Multiply 3 by 10."},
                {"say": "Check the new pair still gives \\(k = 3\\).", "pre": "30 ÷ 10 = ", "post": "", "answer": 3, "hint": "Divide 30 by 10."},
                {"say": "k works for any x. If x = 2, then y is:", "pre": "3 × 2 = ", "post": "", "answer": 6, "hint": "Multiply k by 2.", "done": "Gone. Find k, then multiply. That is all direct proportion is."},
            ],
        },
        "silver": {
            "label": "Together: the inverse move",
            "display": "y is inversely proportional to x. When x = 3, y = 8. Find y when x = 6.<br>" + inverse_graph,
            "steps": [
                {"say": "Inverse proportion means \\(y = k \\div x\\), so \\(k = x \\times y\\). Multiply the pair.", "pre": "3 × 8 = ", "post": "", "answer": 24, "hint": "Multiply 3 by 8."},
                {"say": "Now \\(y = k \\div x\\) with the new x = 6.", "pre": "24 ÷ 6 = ", "post": "", "answer": 4, "hint": "Divide 24 by 6."},
                {"say": "Notice x doubled (3 to 6) and y halved (8 to 4). Check the product stays 24.", "pre": "6 × 4 = ", "post": "", "answer": 24, "hint": "Multiply 6 by 4."},
                {"say": "For x = 12, y is:", "pre": "24 ÷ 12 = ", "post": "", "answer": 2, "hint": "Divide 24 by 12.", "done": "The product x × y is always 24. That is inverse proportion: multiply to find k."},
            ],
        },
        "gold": {
            "label": "Together: proportional to a square",
            "display": "y is directly proportional to x². When x = 2, y = 24. Find y when x = 5.",
            "steps": [
                {"say": "y is proportional to \\(x^2\\), so \\(y = kx^2\\). Square the given x.", "pre": "2 × 2 = ", "post": "", "answer": 4, "hint": "Work out 2 squared."},
                {"say": "Find \\(k\\) by dividing y by \\(x^2\\).", "pre": "24 ÷ 4 = ", "post": "", "answer": 6, "hint": "Divide 24 by 4."},
                {"say": "Square the new x = 5.", "pre": "5 × 5 = ", "post": "", "answer": 25, "hint": "Work out 5 squared."},
                {"say": "Then \\(y = k \\times 25\\).", "pre": "6 × 25 = ", "post": "", "answer": 150, "hint": "Multiply 6 by 25."},
                {"say": "Check: divide y by \\(x^2\\) to recover k.", "pre": "150 ÷ 25 = ", "post": "", "answer": 6, "hint": "Divide 150 by 25.", "done": "y = 150. The new move: square x before using k."},
            ],
        },
    },
}

print("SVG lengths:", len(tickets_svg()), len(direct_graph), len(inverse_graph))
json.dump({"method_card": method_card, "tier_guides": tier_guides, "guided": guided},
          open("_rp04_parts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("parts written")
