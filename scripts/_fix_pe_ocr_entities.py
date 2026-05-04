"""One-off: decode HTML entities in plain-text 'marks' fields across PE OCR lessons."""
import json
import html
from pathlib import Path

LESSON_DIR = Path(__file__).parent / "_content_physical-education-ocr" / "lessons"

def decode_marks(obj):
    """Recursively decode HTML entities in any 'marks' string field."""
    changed = False
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "marks" and isinstance(v, str):
                decoded = html.unescape(v)
                if decoded != v:
                    obj[k] = decoded
                    changed = True
            elif isinstance(v, (dict, list)):
                if decode_marks(v):
                    changed = True
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                if decode_marks(item):
                    changed = True
    return changed

total_fixed = 0
for f in sorted(LESSON_DIR.glob("*.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    if decode_marks(data):
        f.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  fixed: {f.name}")
        total_fixed += 1

print(f"\nDecoded entities in {total_fixed} files.")
