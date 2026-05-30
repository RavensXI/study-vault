"""Verify every local /images/ asset referenced by index.html actually exists.

Catches the failure mode where a build wires a homepage card / picker-item /
freeSubjectMeta entry to `/images/subject-{slug}.jpg` but never commits the
file — the card then renders broken (e.g. Psychology, 30 May 2026).

Scans index.html for every `/images/....(jpg|jpeg|png|webp|svg|gif|avif)`
reference (covers src="...", image: '...', CSS url(...), etc.), de-dupes, and
confirms the file exists under the repo's images/ tree. Remote http(s) image
URLs (Unsplash, R2) are out of scope — only local /images/ paths are checked.

Usage:
    python scripts/_verify_homepage_images.py            # exit 1 if any missing
    python scripts/_verify_homepage_images.py --quiet    # only print on failure

Exit codes: 0 = all referenced local images exist; 1 = one or more missing.
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "index.html"

# Any /images/....<ext> token, regardless of quoting/attribute. Stops at the
# first quote, paren, whitespace or closing angle bracket.
IMG_RE = re.compile(r"/images/[^\"')>\s]+?\.(?:jpg|jpeg|png|webp|svg|gif|avif)", re.IGNORECASE)


def find_missing_images(repo_root=None):
    """Return (missing, total): local /images/ refs in index.html with no file.

    `missing` is a sorted list of referenced paths that don't resolve;
    `total` is the count of distinct local image references checked.
    Importable by other verifiers (e.g. _verify_subject_build.py).
    """
    root = Path(repo_root) if repo_root else REPO
    index = root / "index.html"
    if not index.exists():
        return [], 0
    html = index.read_text(encoding="utf-8")
    refs = sorted(set(IMG_RE.findall(html)))
    missing = [r for r in refs if not (root / r.lstrip("/")).exists()]
    return missing, len(refs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="only print on failure")
    args = ap.parse_args()

    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found")
        return 2

    missing, total = find_missing_images()

    if missing:
        print(f"FAIL: {len(missing)} of {total} local image reference(s) in index.html have no file:")
        for m in missing:
            print(f"  MISSING  {m}")
        return 1

    if not args.quiet:
        print(f"PASS: all {total} local /images/ references in index.html resolve to files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
