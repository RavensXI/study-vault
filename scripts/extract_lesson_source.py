"""
Extract relevant source material for a specific lesson from the full science source text.

Usage:
    python scripts/extract_lesson_source.py <source_file> <keyword1> [keyword2] ...

Splits the source text by document markers (=== filename ===), searches each document's
filename and first 2000 chars for any matching keyword, and outputs the matching documents
(truncated to 5000 chars each). Total output capped at 60KB.
"""
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    source_file = sys.argv[1]
    keywords = [kw.lower() for kw in sys.argv[2:]]

    with open(source_file, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    # Split by document markers: === filename.pptx ===
    file_pattern = r"={3,}\s*(.+?\.(?:pptx?|pdf|docx?))\s*={3,}"
    parts = re.split(file_pattern, text, flags=re.IGNORECASE)

    results = []
    total_size = 0
    MAX_TOTAL = 60000  # 60KB cap
    MAX_PER_DOC = 5000

    for i in range(1, len(parts), 2):
        filename = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""

        # Search filename + first 2000 chars of content
        searchable = (filename + " " + content[:2000]).lower()
        if any(kw in searchable for kw in keywords):
            truncated = content[:MAX_PER_DOC]
            if len(content) > MAX_PER_DOC:
                truncated += "\n[... truncated ...]"
            entry = f"=== {filename} ===\n{truncated}"
            total_size += len(entry)
            if total_size > MAX_TOTAL:
                results.append("\n[... additional matching sources omitted (60KB limit) ...]")
                break
            results.append(entry)

    if results:
        print("\n\n".join(results))
    else:
        print("(No matching source material found for keywords: " + ", ".join(keywords) + ")")


if __name__ == "__main__":
    main()
