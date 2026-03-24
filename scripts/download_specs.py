"""
Download all GCSE specification PDFs and convert to Markdown.

Reads spec URLs from specs/*_specs.json files, downloads each PDF,
converts to markdown via markitdown, and adds frontmatter metadata.

Usage:
    python scripts/download_specs.py              # all boards
    python scripts/download_specs.py --board aqa  # one board
    python scripts/download_specs.py --dry-run    # preview only
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPECS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "specs")


def slugify(text):
    """Convert text to a filename-safe slug."""
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s


def download_pdf(url, dest_path):
    """Download a PDF file. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (StudyVault spec downloader)'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(dest_path, 'wb') as f:
                f.write(resp.read())
        return True
    except Exception as e:
        print(f"    DOWNLOAD FAILED: {e}")
        return False


def convert_to_markdown(pdf_path):
    """Convert PDF to markdown using markitdown. Returns the text."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "markitdown", pdf_path],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=120
        )
        return result.stdout
    except Exception as e:
        print(f"    CONVERT FAILED: {e}")
        return None


def add_frontmatter(markdown, spec):
    """Add YAML frontmatter to the markdown."""
    board = spec.get('board', 'Unknown')
    subject = spec.get('subject', 'Unknown')
    code = spec.get('spec_code', '')
    slug = spec.get('slug', slugify(subject))

    frontmatter = f"""---
board: {board}
subject: {subject}
spec_code: {code}
slug: {slug}
---

"""
    return frontmatter + markdown


def get_board_dir(board_name):
    """Map board name to directory."""
    name = board_name.lower()
    if 'aqa' in name:
        return 'aqa'
    elif 'edexcel' in name or 'pearson' in name:
        return 'edexcel'
    elif 'ocr' in name or 'cambridge' in name:
        return 'ocr'
    elif 'eduqas' in name:
        return 'eduqas'
    elif 'wjec' in name:
        return 'wjec'
    return slugify(name)


def main():
    parser = argparse.ArgumentParser(description="Download and convert GCSE specs to Markdown")
    parser.add_argument("--board", help="Only process one board (aqa, edexcel, ocr, wjec)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without downloading")
    args = parser.parse_args()

    # Find all spec JSON files
    json_files = []
    for f in sorted(os.listdir(SPECS_DIR)):
        if f.endswith('_specs.json'):
            board_key = f.replace('_specs.json', '')
            if args.board and args.board.lower() != board_key.lower():
                continue
            json_files.append(os.path.join(SPECS_DIR, f))

    if not json_files:
        print("No spec JSON files found in specs/")
        return

    # Load all specs
    all_specs = []
    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            specs = json.load(f)
        all_specs.extend(specs)
        print(f"Loaded {len(specs)} specs from {os.path.basename(jf)}")

    print(f"\nTotal: {len(all_specs)} specs to process\n")

    downloaded = 0
    converted = 0
    skipped = 0
    failed = 0

    for i, spec in enumerate(all_specs):
        board = spec.get('board', 'Unknown')
        subject = spec.get('subject', 'Unknown')
        code = spec.get('spec_code', '')
        slug = spec.get('slug', slugify(subject))
        pdf_url = spec.get('pdf_url', '')

        if not pdf_url:
            print(f"  [{i+1}/{len(all_specs)}] {board} {subject} ({code}): NO URL - skipping")
            skipped += 1
            continue

        board_dir = get_board_dir(board)
        os.makedirs(os.path.join(SPECS_DIR, board_dir), exist_ok=True)

        filename = f"{slug}-{code}" if code else slug
        md_path = os.path.join(SPECS_DIR, board_dir, f"{filename}.md")
        pdf_path = os.path.join(SPECS_DIR, board_dir, f"{filename}.pdf")

        # Skip if markdown already exists
        if os.path.exists(md_path) and os.path.getsize(md_path) > 100:
            skipped += 1
            continue

        print(f"  [{i+1}/{len(all_specs)}] {board} {subject} ({code})")

        if args.dry_run:
            print(f"    Would download: {pdf_url[:80]}...")
            print(f"    Would save to: {md_path}")
            continue

        # Download
        if not os.path.exists(pdf_path):
            ok = download_pdf(pdf_url, pdf_path)
            if not ok:
                failed += 1
                continue
            downloaded += 1
            time.sleep(0.5)  # Rate limit
        else:
            print(f"    PDF exists, converting...")

        # Convert
        markdown = convert_to_markdown(pdf_path)
        if not markdown:
            failed += 1
            continue

        # Add frontmatter and save
        markdown = add_frontmatter(markdown, spec)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        converted += 1

        # Remove PDF to save disk space
        try:
            os.remove(pdf_path)
        except:
            pass

        if converted % 10 == 0:
            print(f"    Progress: {converted} converted...")

    print(f"\n{'=' * 50}")
    print(f"DONE")
    print(f"{'=' * 50}")
    print(f"Downloaded: {downloaded}")
    print(f"Converted:  {converted}")
    print(f"Skipped:    {skipped}")
    print(f"Failed:     {failed}")


if __name__ == "__main__":
    main()
