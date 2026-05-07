"""Audit every quote in every English Literature poetry lesson against the
canonical-text store at data/canonical_poems/.

For each lesson:
1. Parse content_html.
2. Find every quoted fragment — blockquote contents, inline "..." quotes,
   and lines inside the prose flagged as quotes.
3. For each quote, identify which poem it's from (the closest preceding
   <strong>{Title}</strong> or attribution like 'Shelley writes' / poet name).
4. Fuzzy-match the quote against the poem's canonical text. Flag mismatches.

Outputs:
- scripts/_poem_audit_findings_v2.json — full findings list
- scripts/_poem_audit_summary.md       — human-readable summary
"""
import html as html_lib
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

sys.path.insert(0, "scripts")
from lib.supabase_client import get_client

CANONICAL_BASE = Path("data/canonical_poems")
FINDINGS_PATH = Path("scripts/_poem_audit_findings_v2.json")
SUMMARY_PATH = Path("scripts/_poem_audit_summary.md")

UNIT_TO_DIR = {
    ("english-literature-aqa", "love-and-relationships"): "aqa-love-and-relationships",
    ("english-literature-aqa", "power-and-conflict"): "aqa-power-and-conflict",
    ("english-literature-aqa", "worlds-and-lives"): "aqa-worlds-and-lives",
    ("english-literature-edexcel", "poetry-belonging"): "edexcel-belonging",
    ("english-literature-edexcel", "poetry-conflict"): "edexcel-conflict",
    ("english-literature-edexcel", "poetry-relationships"): "edexcel-relationships",
    ("english-literature-edexcel", "poetry-time-and-place"): "edexcel-time-and-place",
    ("english-literature-ocr", "poetry-conflict"): "ocr-conflict",
    ("english-literature-ocr", "poetry-love-and-relationships"): "ocr-love-and-relationships",
    ("english-literature-ocr", "poetry-youth-and-age"): "ocr-youth-and-age",
    ("english-literature-eduqas", "poetry-anthology"): "eduqas",
}


def normalise(s: str) -> str:
    s = html_lib.unescape(s)
    s = (s.replace("'", "'").replace("‘", "'").replace("’", "'")
          .replace('"', '"').replace("“", '"').replace("”", '"')
          .replace("—", "-").replace("–", "-").replace("‐", "-").replace("−", "-")
          .replace("…", "...").replace("\xa0", " "))
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(".,;:!?\"'()-…/ ")
    return s


def normalise_for_match(s: str) -> str:
    s = normalise(s)
    s = re.sub(r"[^\w\s'-]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_canonical_store() -> dict:
    store = {}
    for dir_path in CANONICAL_BASE.iterdir():
        if not dir_path.is_dir():
            continue
        store[dir_path.name] = {}
        for txt in dir_path.glob("*.txt"):
            content = txt.read_text(encoding="utf-8")
            lines = content.split("\n")
            title = lines[0].lstrip("# ").strip() if lines else ""
            poet = lines[1].lstrip("# ").strip() if len(lines) > 1 else ""
            body = "\n".join(lines[3:]) if len(lines) > 3 else ""
            store[dir_path.name][txt.stem] = {
                "title": title,
                "poet": poet,
                "body": body,
                "body_normalised": normalise_for_match(body),
            }
    return store


def extract_quotes_from_html(html: str) -> list:
    quotes = []

    # 1. Blockquotes
    for m in re.finditer(r"<blockquote[^>]*>(.*?)</blockquote>", html, re.DOTALL | re.IGNORECASE):
        inner = m.group(1)
        parts = re.split(r"<br\s*/?>|</p>", inner, flags=re.IGNORECASE)
        for p in parts:
            text = re.sub(r"<[^>]+>", "", p)
            text = html_lib.unescape(text).strip()
            if len(text.split()) >= 3:
                ctx_start = max(0, m.start() - 400)
                quotes.append({
                    "text": text,
                    "kind": "blockquote",
                    "context": html[ctx_start:m.start() + 100],
                    "html_pos": m.start(),
                })

    # 2. Inline quotes
    plain = re.sub(r"<[^>]+>", " ", html)
    plain = html_lib.unescape(plain)
    plain = plain.replace("\xa0", " ")

    quote_patterns = [
        r"“([^”]{8,400})”",
        r'"([^"]{8,400})"',
        r"‘([^’]{8,400})’",
    ]
    seen_inline = set()
    for pat in quote_patterns:
        for m in re.finditer(pat, plain):
            text = m.group(1).strip()
            if len(text.split()) < 3:
                continue
            if len(text.split()) < 5 and not any(w in text.lower() for w in ["the", "and", "of", "a", "to", "in", "is", "with", "my"]):
                continue
            if text in seen_inline:
                continue
            seen_inline.add(text)
            ctx_start = max(0, m.start() - 400)
            quotes.append({
                "text": text,
                "kind": "inline",
                "context": plain[ctx_start:m.start() + len(text) + 100],
                "html_pos": m.start(),
            })

    return quotes


def find_poem_for_quote(quote: dict, canonical_dir: dict):
    ctx = quote["context"]
    ctx_norm = normalise(ctx)

    best_slug = None
    best_score = 0
    best_priority = -1

    for slug, poem in canonical_dir.items():
        title_norm = normalise(poem["title"])
        poet_norm = normalise(poem["poet"])

        # Title match (highest priority) — be careful with single-word titles
        # like "London", "Now", "Ode" — only match if word boundary
        if title_norm:
            # Word-boundary match
            pattern = r"\b" + re.escape(title_norm) + r"\b"
            for m in re.finditer(pattern, ctx_norm):
                score = m.start()
                if best_priority < 2 or score > best_score:
                    best_priority = 2
                    best_score = score
                    best_slug = slug

        # Poet surname (lower priority)
        if best_priority < 2 and poet_norm:
            surname = poet_norm.split()[-1]
            if len(surname) >= 4:
                pattern = r"\b" + re.escape(surname) + r"\b"
                for m in re.finditer(pattern, ctx_norm):
                    score = m.start()
                    if best_priority < 1 or score > best_score:
                        best_priority = 1
                        best_score = score
                        best_slug = slug

    if best_slug:
        return best_slug, canonical_dir[best_slug]
    return None


def quote_in_canonical(quote_text: str, canonical_norm: str):
    q_norm = normalise_for_match(quote_text)
    if not q_norm or not canonical_norm:
        return False, 0.0

    if q_norm in canonical_norm:
        return True, 1.0

    words = q_norm.split()
    # Try strip leading/trailing words (often quotes have ellipsis or partial endings)
    for n_strip_end in range(0, min(3, len(words) - 2)):
        for n_strip_start in range(0, min(3, len(words) - 2 - n_strip_end)):
            partial = " ".join(words[n_strip_start:len(words) - n_strip_end])
            if len(partial.split()) >= 3 and partial in canonical_norm:
                return True, (len(words) - n_strip_start - n_strip_end) / len(words)

    # Sliding window approx similarity
    sm = SequenceMatcher(None, q_norm, canonical_norm, autojunk=False)
    match = sm.find_longest_match(0, len(q_norm), 0, len(canonical_norm))
    ratio = match.size / len(q_norm) if q_norm else 0
    return ratio >= 0.85, ratio


def main():
    sb = get_client()
    canonical_store = load_canonical_store()

    print(f"Canonical store: {sum(len(v) for v in canonical_store.values())} poems")
    for d, poems in sorted(canonical_store.items()):
        print(f"  {d}: {len(poems)} poems")

    findings = []
    total_lessons = 0
    total_quotes = 0

    for (subject_slug, unit_slug), canonical_dir_slug in UNIT_TO_DIR.items():
        canonical_dir = canonical_store.get(canonical_dir_slug, {})
        if not canonical_dir:
            print(f"  WARN: no canonical dir for {canonical_dir_slug}")
            continue

        sub = sb.table("subjects").select("id").eq("slug", subject_slug).execute().data
        if not sub:
            continue
        sid = sub[0]["id"]
        units = sb.table("units").select("id, slug").eq("subject_id", sid).eq("slug", unit_slug).execute().data
        if not units:
            continue
        uid = units[0]["id"]
        rows = sb.table("lessons").select("id, slug, title, lesson_number, content_html").eq("unit_id", uid).order("lesson_number").execute().data

        for r in rows:
            content = r.get("content_html") or ""
            if not content:
                continue
            total_lessons += 1
            quotes = extract_quotes_from_html(content)
            total_quotes += len(quotes)

            # Pre-compute set of poem-title norms in this cluster (for filtering)
            cluster_titles = {normalise(p["title"]) for p in canonical_dir.values()}

            ANALYTICAL_WORDS = {
                # third-person present analytical verbs
                "uses", "presents", "describes", "explores", "represents",
                "evokes", "shows", "suggests", "creates", "emphasises",
                "emphasizes", "conveys", "depicts", "portrays", "reveals",
                "captures", "illustrates", "highlights", "establishes",
                "introduces", "develops", "demonstrates", "indicates",
                "reflects", "personifies", "compares", "contrasts",
                "begins", "ends", "structures", "frames", "shifts",
                "echoes", "mirrors", "alludes", "addresses", "acknowledges",
                "characterises", "characterizes", "challenges", "celebrates",
                "exposes", "subverts", "transforms", "questions", "asks",
                "drives", "builds", "explains", "argues", "links", "deepens",
                "transcends", "enacts", "renders", "deploys", "captures",
                # plural/auxiliary
                "use ", "both poets", "both poems", "the speaker", "the poet",
                "the simile", "the metaphor", "the imagery", "the diction",
                "the structure", "the form", "the tone",
                # biographical/observational
                "was born", "was published", "wrote", "writes", "written",
                "writing", "while ", "during", "in contrast", "by contrast",
                "as well as", "similarly", "differently", "as a result",
                # comparison markers
                "like [poet", "[poet a]", "[poet b]", "[poem]",
            }

            for q in quotes:
                qn = normalise(q["text"])

                # FILTER 1: Skip if the quote IS just a poem title verbatim
                if qn in cluster_titles:
                    continue

                # FILTER 2: Skip if quote is short (<5 words) — too noisy
                # UNLESS it came from a blockquote (which is structurally a quote)
                word_count = len(q["text"].split())
                if word_count < 5 and q["kind"] != "blockquote":
                    continue

                # FILTER 3: Skip if quote is analytical prose
                qn_lower = q["text"].lower()
                if any(w in qn_lower for w in ANALYTICAL_WORDS):
                    continue

                # FILTER 3b: Comparison prose mentioning multiple poet surnames
                surnames_in_text = sum(
                    1 for p in canonical_dir.values()
                    if re.search(r"\b" + re.escape(p["poet"].split()[-1].lower()) + r"\b", qn_lower)
                )
                if surnames_in_text >= 2:
                    continue

                # FILTER 3c: Comparison prose mentioning multiple poem titles in quoted format
                titles_in_text = sum(
                    1 for t in cluster_titles
                    if t and len(t) > 4 and re.search(r"['‘\"“]\s*" + re.escape(t) + r"\s*['’\"”]", qn_lower)
                )
                if titles_in_text >= 1 and ("both" in qn_lower or "contrast" in qn_lower or "compare" in qn_lower):
                    continue

                # Search the quote against EVERY poem in the cluster.
                best_slug = None
                best_poem = None
                best_ratio = 0.0
                matched = False
                for slug, poem in canonical_dir.items():
                    is_match, ratio = quote_in_canonical(q["text"], poem["body_normalised"])
                    if is_match:
                        matched = True
                        best_slug = slug
                        best_poem = poem
                        best_ratio = ratio
                        break
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_slug = slug
                        best_poem = poem

                if matched:
                    continue

                # FILTER 4: Skip if best partial match in cluster ≥ 0.4 — quote has
                # substantial overlap with some canonical poem (often embedded
                # quote within prose). True fabrications score <0.3 in our data.
                if best_ratio >= 0.4:
                    continue

                # FILTER 5: Skip if quote contains an obvious template placeholder
                if "[poet" in q["text"].lower() or "[poem" in q["text"].lower() or "[theme" in q["text"].lower() or "[named poem]" in q["text"].lower():
                    continue

                # No exact match in cluster. Try to attribute the quote to a poem
                # by context (so we report the poem the lesson INTENDED to quote).
                resolved = find_poem_for_quote(q, canonical_dir)
                if resolved is None:
                    # Best guess: the partial-match poem
                    poem_slug = best_slug
                    poem = best_poem
                else:
                    poem_slug, poem = resolved

                if poem_slug is None:
                    findings.append({
                        "subject_slug": subject_slug,
                        "unit_slug": unit_slug,
                        "lesson_id": r["id"],
                        "lesson_number": r["lesson_number"],
                        "lesson_title": r["title"],
                        "lesson_slug": r["slug"],
                        "quote": q["text"][:300],
                        "kind": q["kind"],
                        "issue": "no-match-no-attribution",
                        "poem_slug": None,
                        "poem_title": None,
                        "poet": None,
                        "match_ratio": 0.0,
                    })
                    continue

                # Re-check ratio against the resolved poem (may differ from best_ratio)
                _, attributed_ratio = quote_in_canonical(q["text"], poem["body_normalised"])

                findings.append({
                    "subject_slug": subject_slug,
                    "unit_slug": unit_slug,
                    "lesson_id": r["id"],
                    "lesson_number": r["lesson_number"],
                    "lesson_title": r["title"],
                    "lesson_slug": r["slug"],
                    "quote": q["text"][:300],
                    "kind": q["kind"],
                    "issue": "quote-not-in-canonical",
                    "poem_slug": poem_slug,
                    "poem_title": poem["title"],
                    "poet": poem["poet"],
                    "match_ratio": round(attributed_ratio, 2),
                    "best_match_in_cluster": round(best_ratio, 2),
                })

    FINDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINDINGS_PATH.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")

    by_severity = {"high (no match)": [], "medium (partial)": [], "unidentified-poem": []}
    for f in findings:
        if f["issue"] == "unidentified-poem":
            by_severity["unidentified-poem"].append(f)
        elif f["match_ratio"] < 0.5:
            by_severity["high (no match)"].append(f)
        else:
            by_severity["medium (partial)"].append(f)

    summary_lines = []
    summary_lines.append("# Poem Quote Audit v2 — Findings")
    summary_lines.append("")
    summary_lines.append(f"- Lessons audited: {total_lessons}")
    summary_lines.append(f"- Quotes extracted: {total_quotes}")
    summary_lines.append(f"- Total findings: {len(findings)}")
    summary_lines.append(f"  - HIGH (no canonical match): {len(by_severity['high (no match)'])}")
    summary_lines.append(f"  - MEDIUM (partial match): {len(by_severity['medium (partial)'])}")
    summary_lines.append(f"  - Unidentified poem: {len(by_severity['unidentified-poem'])}")
    SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"\nLessons: {total_lessons}, Quotes: {total_quotes}, Findings: {len(findings)}")
    print(f"  HIGH: {len(by_severity['high (no match)'])}")
    print(f"  MEDIUM: {len(by_severity['medium (partial)'])}")
    print(f"  Unidentified: {len(by_severity['unidentified-poem'])}")
    print(f"\nDetails: {FINDINGS_PATH}")


if __name__ == "__main__":
    main()
