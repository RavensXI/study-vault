"""Add About + FAQ links to legal footers across all student-facing HTML pages."""
import os, glob

OLD = '<a href="/copyright.html">Copyright &amp; IP</a> &middot; <a href="/privacy.html">Privacy</a>'
NEW = '<a href="/about">About</a> &middot; <a href="/faq">FAQ</a> &middot; <a href="/copyright.html">Copyright &amp; IP</a> &middot; <a href="/privacy.html">Privacy</a>'

EXCLUDE_DIRS = {'admin', 'node_modules', 'claude-design-bundle', '.git', 'Spec and Materials', '.claude'}
EXCLUDE_FILES = {'about.html', 'faq.html', 'copyright.html', 'privacy.html'}

count_updated = 0
count_skipped = 0
for path in glob.glob('**/*.html', recursive=True):
    norm = path.replace(os.sep, '/')
    parts = norm.split('/')
    if any(p in EXCLUDE_DIRS for p in parts):
        continue
    if os.path.basename(path) in EXCLUDE_FILES:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
    except Exception:
        continue
    # Only update if the OLD pattern is present and we haven't already added /about
    if OLD in s and '/about' not in s:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s.replace(OLD, NEW))
        count_updated += 1
    else:
        count_skipped += 1

print(f'Updated: {count_updated}')
print(f'Skipped (no match or already done): {count_skipped}')
