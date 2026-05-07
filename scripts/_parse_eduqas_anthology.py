"""Parse the Eduqas 2014-2026 poetry anthology PDF into per-poem files.

Strategy:
1. Split text on \x0c (form feed) — each chunk is one PDF page.
2. Strip footer lines and page numbers from each page.
3. Concatenate pages until we hit a poet attribution line; that ends a poem.
4. The poem's title is the first non-blank line of the FIRST page in that group.
"""
import re
from pathlib import Path

INPUT = Path("eduqas-extracted.txt")
OUT_DIR = Path("data/canonical_poems/eduqas")

KNOWN_POETS = {
    "simon armitage", "elizabeth barrett browning", "william blake",
    "rupert brooke", "lord byron", "imtiaz dharker", "emily dickinson",
    "rita dove", "carol ann duffy", "thomas hardy", "seamus heaney",
    "ted hughes", "john keats", "philip larkin", "wilfred owen",
    "percy bysshe shelley", "owen sheers", "william wordsworth",
}


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def is_footer(line: str) -> bool:
    return ("WJEC Eduqas GCSE Poetry Anthology" in line
            or "oxfordsecondary.co.uk" in line
            or "examined for the final time" in line
            or "examined for the first time" in line)


def is_page_number(line: str) -> bool:
    return bool(re.match(r"^\d+\s*$", line.strip()))


def clean_page(page_text: str) -> list[str]:
    """Strip footer + page-number lines; return remaining non-empty lines (preserving structure)."""
    out = []
    for L in page_text.split("\n"):
        s = L.replace("\xa0", " ").rstrip()
        if is_footer(s):
            continue
        if is_page_number(s):
            continue
        out.append(s)
    # Trim leading/trailing blank lines
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def main():
    text = INPUT.read_text(encoding="cp1252").replace("\xa0", " ")
    pages = text.split("\x0c")

    print(f"PDF has {len(pages)} pages (form-feed separated)")

    # Group pages into poems. A poem ends when we see a poet attribution line.
    poems = []
    current_lines = []
    current_title = None

    for page_idx, page in enumerate(pages):
        cleaned = clean_page(page)
        if not cleaned:
            continue

        # If we don't have a title yet, the first non-blank line of this page is it
        if current_title is None:
            current_title = cleaned[0]
            page_body = cleaned[1:]
        else:
            page_body = cleaned

        # Walk through page body looking for a poet attribution
        for line_idx, L in enumerate(page_body):
            if L.strip().lower() in KNOWN_POETS:
                # End of poem — finalise
                poet = L.strip()
                poems.append({
                    "title": current_title,
                    "poet": poet,
                    "body": "\n".join(current_lines).strip(),
                })
                # Reset for next poem
                current_lines = []
                current_title = None
                # Anything AFTER the poet line on this page belongs to the next poem
                remainder = page_body[line_idx + 1:]
                if remainder:
                    # Find where actual poem content starts (skip blank lines)
                    while remainder and not remainder[0].strip():
                        remainder.pop(0)
                    if remainder:
                        current_title = remainder[0]
                        current_lines.extend(remainder[1:])
                break
            else:
                current_lines.append(L)

    # Catch any trailing poem (shouldn't happen if PDF ends with poet line)
    if current_title and current_lines:
        print(f"  WARN: trailing content with title {current_title!r} but no poet anchor")

    print(f"Extracted {len(poems)} poems (expecting 18)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in poems:
        slug = slugify(p["title"])
        # Drop trailing/leading blank lines from body
        body_lines = p["body"].split("\n")
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        body = "\n".join(body_lines)

        path = OUT_DIR / f"{slug}.txt"
        path.write_text(
            f"# {p['title']}\n# {p['poet']}\n\n{body}\n",
            encoding="utf-8",
        )
        print(f"  {path.name:50s}  (poet: {p['poet']:30s} body: {len(body_lines):3d} lines)")


if __name__ == "__main__":
    main()
