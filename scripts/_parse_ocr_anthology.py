"""Parse the OCR 'Towards a World Unknown' poetry anthology PDF into per-poem files.

Uses PyMuPDF (fitz) which preserves logical reading order across columnar
layouts (markitdown jumbles them). The TOC on PDF page 7 is the canonical
poem list (45 poems across 3 clusters).

Strategy:
1. Extract each PDF page's text via fitz with text-mode reading order.
2. Concatenate all pages into one big text stream, separated by page markers.
3. Use a control list of (title, poet, page) — find each title in the stream,
   slice the body up to the poet attribution.
"""
import re
from pathlib import Path
import fitz

PDF = Path("171147-poetry-anthology-towards-a-world-unknown.pdf")
OUT_BASE = Path("data/canonical_poems")

# 45 poems — title, poet, anthology page, cluster slug
POEMS = [
    # Love and Relationships
    ("A Song", "Helen Maria Williams", 7, "ocr-love-and-relationships"),
    ("Bright Star", "John Keats", 8, "ocr-love-and-relationships"),
    ("Now", "Robert Browning", 8, "ocr-love-and-relationships"),
    ("Love and Friendship", "Emily Brontë", 9, "ocr-love-and-relationships"),
    ("A Broken Appointment", "Thomas Hardy", 9, "ocr-love-and-relationships"),
    ("Fin de Fête", "Charlotte Mew", 10, "ocr-love-and-relationships"),
    ("The Sorrow of True Love", "Edward Thomas", 10, "ocr-love-and-relationships"),
    ("An Arundel Tomb", "Philip Larkin", 11, "ocr-love-and-relationships"),
    ("Love After Love", "Derek Walcott", 12, "ocr-love-and-relationships"),
    ("Morning Song", "Sylvia Plath", 12, "ocr-love-and-relationships"),
    ("Long Distance II", "Tony Harrison", 13, "ocr-love-and-relationships"),
    ("I Wouldn't Thank You for a Valentine", "Liz Lochhead", 14, "ocr-love-and-relationships"),
    ("In Paris With You", "James Fenton", 15, "ocr-love-and-relationships"),
    ("Warming Her Pearls", "Carol Ann Duffy", 16, "ocr-love-and-relationships"),
    ("Dusting the Phone", "Jackie Kay", 17, "ocr-love-and-relationships"),
    # Conflict
    ("A Poison Tree", "William Blake", 18, "ocr-conflict"),
    ("Envy", "Mary Lamb", 19, "ocr-conflict"),
    ("Boat Stealing", "William Wordsworth", 20, "ocr-conflict"),
    ("The Destruction of Sennacherib", "Lord Byron", 21, "ocr-conflict"),
    ("There's a Certain Slant of Light", "Emily Dickinson", 22, "ocr-conflict"),
    ("The Man He Killed", "Thomas Hardy", 22, "ocr-conflict"),
    ("Anthem for Doomed Youth", "Wilfred Owen", 23, "ocr-conflict"),
    ("Vergissmeinnicht", "Keith Douglas", 24, "ocr-conflict"),
    ("What Were They Like?", "Denise Levertov", 25, "ocr-conflict"),
    ("Lament", "Gillian Clarke", 26, "ocr-conflict"),
    ("Punishment", "Seamus Heaney", 27, "ocr-conflict"),
    ("Flag", "John Agard", 28, "ocr-conflict"),
    ("Phrase Book", "Jo Shapcott", 28, "ocr-conflict"),
    ("Honour Killing", "Imtiaz Dharker", 30, "ocr-conflict"),
    ("Partition", "Sujata Bhatt", 31, "ocr-conflict"),
    # Youth and Age
    ("Holy Thursday", "William Blake", 32, "ocr-youth-and-age"),
    ("When I have fears that I may cease to be", "John Keats", 33, "ocr-youth-and-age"),
    ("The Bluebell", "Anne Brontë", 34, "ocr-youth-and-age"),
    ("Midnight on the Great Western", "Thomas Hardy", 35, "ocr-youth-and-age"),
    ("Spring and Fall", "Gerard Manley Hopkins", 36, "ocr-youth-and-age"),
    ("Ode", "Arthur O'Shaughnessy", 36, "ocr-youth-and-age"),
    ("Out, Out", "Robert Frost", 37, "ocr-youth-and-age"),
    ("Red Roses", "Anne Sexton", 38, "ocr-youth-and-age"),
    ("Baby Song", "Thom Gunn", 39, "ocr-youth-and-age"),
    ("You're", "Sylvia Plath", 40, "ocr-youth-and-age"),
    ("Cold Knap Lake", "Gillian Clarke", 40, "ocr-youth-and-age"),
    ("My First Weeks", "Sharon Olds", 41, "ocr-youth-and-age"),
    ("Venus's-flytraps", "Yusef Komunyakaa", 42, "ocr-youth-and-age"),
    ("Love", "Kate Clanchy", 43, "ocr-youth-and-age"),
    ("Farther", "Owen Sheers", 44, "ocr-youth-and-age"),
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def normalize(s: str) -> str:
    """Normalize curly quotes/dashes to straight ASCII for matching."""
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"')
             .replace("—", "-").replace("–", "-").replace("‐", "-")
             .replace("…", "...").replace("\xa0", " "))


def main():
    doc = fitz.open(PDF)
    print(f"PDF has {len(doc)} pages")

    # Build a list of (anth_page, pdf_idx, page_text) for each PDF page.
    # Anthology page numbers appear as a small standalone number at the bottom.
    page_data = []
    for pdf_idx, page in enumerate(doc):
        text = page.get_text("text")
        # Find anthology page number — pattern: a 1-3 digit number, possibly followed by whitespace, near the end
        anth_pg = None
        # Look at last 5 non-blank lines
        lines = [L.strip() for L in text.split("\n") if L.strip()]
        for L in lines[-5:]:
            m = re.fullmatch(r"(\d{1,3})", L)
            if m:
                anth_pg = int(m.group(1))
        page_data.append({"pdf_idx": pdf_idx, "anth_pg": anth_pg, "text": text})

    # For each poem, find the right page(s) and slice
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    for cluster in {p[3] for p in POEMS}:
        (OUT_BASE / cluster).mkdir(parents=True, exist_ok=True)

    extracted_count = 0
    for i, (title, poet, anth_pg, cluster) in enumerate(POEMS):
        # Find the PDF page for this anthology page
        candidates = [p for p in page_data if p["anth_pg"] == anth_pg]
        if not candidates:
            print(f"  MISS: no PDF page for anthology page {anth_pg} ({title})")
            continue

        # Concat this page + next 1-2 pages (poems may spill)
        pdf_idx = candidates[0]["pdf_idx"]
        combined = ""
        for offset in range(3):
            if pdf_idx + offset < len(doc):
                combined += "\n" + doc[pdf_idx + offset].get_text("text")

        # Find the title in the combined text (normalize for matching)
        norm_combined = normalize(combined)
        norm_title = normalize(title)

        # Be permissive: allow whitespace variations
        title_pattern = re.escape(norm_title).replace(r"\ ", r"\s+")
        match = re.search(title_pattern, norm_combined, re.IGNORECASE)
        if not match:
            print(f"  MISS: title not found — {title}")
            continue

        # Body starts after title
        body_start_norm = match.end()

        # Find the poet name (uppercased) — that's where the body ends
        poet_upper = normalize(poet).upper()
        poet_pattern = re.escape(poet_upper).replace(r"\ ", r"\s+")
        poet_match = re.search(poet_pattern, norm_combined[body_start_norm:])
        if poet_match:
            body_end_norm = body_start_norm + poet_match.start()
        else:
            # Fall back: end at a clear next-poem marker (next title or footer)
            body_end_norm = body_start_norm + 5000  # cap

        # Slice the ORIGINAL (non-normalized) text using the same offsets.
        # Since normalize is char-for-char preserving except for some
        # multi-char replacements, we need to map indices. Simplest: find the
        # title in the original, walk the same number of chars, etc.
        # Easier: re-find title in original text directly.
        orig_match = re.search(re.escape(title).replace(r"\ ", r"\s+"), combined, re.IGNORECASE)
        if not orig_match:
            # Try with normalize-style relaxed matching by replacing apostrophes
            relaxed = title.replace("'", "['’]").replace("-", "[-—–]")
            orig_match = re.search(relaxed.replace(" ", r"\s+"), combined, re.IGNORECASE)
        if not orig_match:
            # Use the match from normalize-space (less precise but better than nothing)
            print(f"  WARN: original-text title match failed for {title} — using fuzzy slice")
            continue

        orig_body_start = orig_match.end()
        # Find poet attribution in original
        poet_orig_pat = re.escape(poet.upper()).replace(r"\ ", r"\s+")
        poet_orig_match = re.search(poet_orig_pat, combined[orig_body_start:])
        if poet_orig_match:
            orig_body_end = orig_body_start + poet_orig_match.start()
        else:
            orig_body_end = orig_body_start + 5000

        body = combined[orig_body_start:orig_body_end].strip()

        # Clean: strip footers, page numbers, leading verse numbers
        cleaned = []
        for L in body.split("\n"):
            s = L.strip()
            if not s:
                cleaned.append("")
                continue
            if "Towards a World Unknown" in s:
                continue
            if re.fullmatch(r"\d+", s):
                continue
            # Strip leading verse line numbers like "1   No riches" or "10     From shore"
            s = re.sub(r"^(\d+)\s{2,}", "", s)
            cleaned.append(s)

        # Trim leading/trailing blanks
        while cleaned and not cleaned[0].strip():
            cleaned.pop(0)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()

        body_text = "\n".join(cleaned)
        slug = slugify(title)
        out_path = OUT_BASE / cluster / f"{slug}.txt"
        out_path.write_text(
            f"# {title}\n# {poet}\n\n{body_text}\n",
            encoding="utf-8",
        )
        extracted_count += 1
        print(f"  {cluster}/{slug}.txt: {len([L for L in cleaned if L.strip()])} non-blank lines")

    print(f"\nExtracted {extracted_count}/{len(POEMS)} poems")


if __name__ == "__main__":
    main()
