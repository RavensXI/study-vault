"""Extract a spec PDF to markdown with BOLD PRESERVED (Edexcel marks Higher-tier-only
content in bold, and markitdown drops it).

Usage: python scripts/_retrofc/_spec_bold_extract.py <pdf> <out.md>
Each text span whose font is bold is wrapped in **...**; consecutive bold spans are
merged. Output is plain text per page with a page marker, good enough to grep.
"""
import re
import sys

import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8")


def is_bold(span):
    f = span.get("font", "").lower()
    return bool(span.get("flags", 0) & 16) or "bold" in f or "black" in f or "heavy" in f


def page_lines(page):
    out = []
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            parts = []
            for span in line.get("spans", []):
                t = span.get("text", "")
                if not t.strip():
                    parts.append(t)
                    continue
                parts.append(("**" + t + "**") if is_bold(span) else t)
            s = "".join(parts)
            s = s.replace("****", "")            # merge adjacent bold spans
            s = re.sub(r"\*\*(\s+)\*\*", r"\1", s)
            if s.strip():
                out.append(s.rstrip())
    return out


def main():
    pdf, out = sys.argv[1], sys.argv[2]
    doc = fitz.open(pdf)
    lines = [f"<!-- bold-preserved extraction of {pdf}; **bold** = Higher tier only where the board says so -->"]
    for i, page in enumerate(doc, 1):
        lines.append(f"\n<!-- page {i} -->")
        lines.extend(page_lines(page))
    text = "\n".join(lines)
    open(out, "w", encoding="utf-8").write(text)
    nb = text.count("**") // 2
    print(f"{out}: {len(doc)} pages, {nb} bold runs")


if __name__ == "__main__":
    main()
