"""Structural remediation pass — fixes flashcard splits, single-word answers,
insufficient dfn glossary, insufficient key-facts.

Run after _remediate_validation.py.
"""
import json
import re
from pathlib import Path

here = Path(__file__).resolve().parent
lessons_dir = here / "lessons"


def load(name):
    return json.loads((lessons_dir / name).read_text(encoding="utf-8"))


def save(name, data):
    (lessons_dir / name).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ----- L2 rewards FC[1] + FC[3] -----
d = load("rewards-and-drawbacks-of-risk-taking.json")
d["flashcard_questions"][1] = {
    "q": "What freedom does the reward of independence give an entrepreneur?",
    "a": "The freedom to make their own decisions about their business.",
}
d["flashcard_questions"][3] = {
    "q": "Which drawback of enterprise affects an entrepreneur's time with family and personal interests?",
    "a": "Work-life balance.",
}
save("rewards-and-drawbacks-of-risk-taking.json", d)
print("  L2 rewards: FC[1], FC[3] split")

# ----- L9 channels FC[5] -----
d = load("selling-channels-and-the-product-lifecycle.json")
d["flashcard_questions"][5] = {
    "q": "Name the product lifecycle stage when sales typically peak.",
    "a": "Maturity.",
}
save("selling-channels-and-the-product-lifecycle.json", d)
print("  L9 channels: FC[5] reworded to start with 'Name'")

# ----- L11 ownership FC[11] -----
d = load("business-ownership-and-sources-of-capital.json")
d["flashcard_questions"][11] = {
    "q": "What does a business angel typically receive in exchange for their investment?",
    "a": "A share of the business.",
}
save("business-ownership-and-sources-of-capital.json", d)
print("  L11 ownership: FC[11] tightened")

# ----- L12 support FC[5] (enumeration) -----
d = load("support-for-an-enterprise.json")
d["flashcard_questions"][5] = {
    "q": "What is the Chamber of Commerce?",
    "a": "A membership organisation that supports local businesses in an area.",
}
save("support-for-an-enterprise.json", d)
print("  L12 support: FC[5] tightened")

# ----- L6 break-even: add 3rd dfn term + glossary entry -----
# Add "fixed costs" or "variable costs" — both are central to break-even.
# Pick "total revenue" since it's NOT already a glossary entry and appears
# in the lesson.
d = load("break-even-and-the-importance-of-cash.json")
html = d["content_html"]
# Find first uncovered occurrence of a sensible term and wrap it in <dfn>.
# Pick "total revenue" — central to the break-even calc.
target = "total revenue"
if target in html.lower():
    # Replace the FIRST plain occurrence of the term (case-insensitive) with a dfn
    pattern = re.compile(re.escape("total revenue"), re.IGNORECASE)
    def_text = "The total money a business takes from selling its products before any costs are subtracted."
    replacement = (
        f'<dfn class="term" data-def="{def_text}">total revenue</dfn>'
    )
    html_new, n = pattern.subn(replacement, html, count=1)
    assert n == 1, "expected one replacement of 'total revenue'"
    d["content_html"] = html_new
    d["glossary_terms"].append({
        "term": "total revenue",
        "definition": def_text,
    })
    save("break-even-and-the-importance-of-cash.json", d)
    print("  L6 break-even: added 'total revenue' dfn + glossary")
else:
    print("  L6 break-even: WARN — 'total revenue' not in content_html; skipping")

# ----- L7 marketing-mix: add 3rd dfn term + glossary entry -----
d = load("the-marketing-mix-and-the-four-ps.json")
html = d["content_html"]
# Pick a term not already wrapped — try "promotion" first.
existing_dfns = re.findall(r'<dfn[^>]*>([^<]+)</dfn>', html, re.IGNORECASE)
existing_lower = {x.lower().strip() for x in existing_dfns}
# Candidates in priority order — first one already in content_html and not
# already a dfn wins.
candidates = [
    ("competitive pricing",
     "A pricing strategy that sets prices similar to or slightly below competitors to attract price-sensitive customers."),
    ("psychological pricing",
     "A pricing strategy that uses prices ending in .99 or .95 to make a product feel cheaper than it really is."),
    ("target market",
     "The specific group of customers a business is trying to reach with its marketing mix."),
]
chosen = None
for term, def_text in candidates:
    if term.lower() in existing_lower:
        continue
    if re.search(re.escape(term), html, re.IGNORECASE):
        chosen = (term, def_text)
        break
if chosen:
    term, def_text = chosen
    pattern = re.compile(re.escape(term), re.IGNORECASE)
    replacement = f'<dfn class="term" data-def="{def_text}">{term}</dfn>'
    html_new, n = pattern.subn(replacement, html, count=1)
    assert n == 1
    d["content_html"] = html_new
    d["glossary_terms"].append({
        "term": term,
        "definition": def_text,
    })
    save("the-marketing-mix-and-the-four-ps.json", d)
    print(f"  L7 marketing-mix: added '{term}' dfn + glossary")
else:
    print("  L7 marketing-mix: WARN — no candidate term found; skipping")

# ----- L12 support: add 2nd key-fact div -----
d = load("support-for-an-enterprise.json")
html = d["content_html"]
existing_kfs = html.count('class="key-fact"')
if existing_kfs >= 2:
    print(f"  L12 support: already has {existing_kfs} key-facts")
else:
    # Insert a second key-fact after the first paragraph that mentions
    # "appropriate" or "matching support". The exam-relevant pivot per the
    # plan is "appropriateness of support for a specific start-up".
    extra_kf = (
        '\n<div class="key-fact" data-revision-tip="In a marked question, '
        'don\'t just describe what each support source does — say WHY that '
        'source fits the entrepreneur in the scenario.">'
        '<p>The R067 spec assesses your ability to <strong>match support '
        'to a specific situation</strong>. Identify the entrepreneur\'s '
        'biggest current problem first (cash, legal, premises, expertise), '
        'then pick the support source that solves that exact problem.</p>'
        '</div>\n'
    )
    # Insert before the closing of content_html — i.e. just before the final
    # </section> or end of string.
    if "</section>" in html:
        # insert before the LAST </section>
        idx = html.rfind("</section>")
        html_new = html[:idx] + extra_kf + html[idx:]
    else:
        html_new = html + extra_kf
    d["content_html"] = html_new
    save("support-for-an-enterprise.json", d)
    print("  L12 support: added 2nd key-fact div")

print("\n=== Structural remediation pass complete ===")
