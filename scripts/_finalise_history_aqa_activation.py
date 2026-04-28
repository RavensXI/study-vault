"""Finalise Phase 2 activation for History (AQA): CSS + SUBJECT_ORDER + Unsplash hero.

Writes:
  - CSS rules (16 unit rules, light + dark mode) appended to css/style.css
  - SUBJECT_ORDER append in scripts/generate_cinematic_videos.py
  - Subject hero image to images/subject-history-aqa.jpg + Supabase subject.image_url

Idempotent: re-running won't duplicate the CSS block (checks for marker comment).
"""
import colorsys
import json
import os
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client
from lib.unsplash import search_unsplash, trigger_unsplash_download

ROOT = Path(__file__).resolve().parent.parent
scripts = ROOT / "scripts"
master = json.loads((scripts / "_plan_history-aqa.json").read_text(encoding="utf-8"))


# ─────────────────────────────────────── CSS

def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def lighten_for_dark_mode(hex_color: str, target_lightness: float = 0.65) -> str:
    """Return a brighter shade suitable for dark-mode accent."""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    # bump lightness, slightly desaturate so it doesn't burn in dark mode
    new_l = max(target_lightness, l)
    new_s = max(0.55, s * 0.92)
    nr, ng, nb = colorsys.hls_to_rgb(h, new_l, new_s)
    return "#{:02x}{:02x}{:02x}".format(int(nr * 255), int(ng * 255), int(nb * 255))


def rgba_from_hex(hex_color: str, alpha: float) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"rgba({r},{g},{b},{alpha})"


def build_css_block() -> str:
    lines = [
        "",
        "/* History (AQA) — free tier, 16 units across 4 sections (Period / Wider world / Thematic / British depth) */",
        "/* AUTOGEN-MARKER: history-aqa unit accents */",
    ]
    for unit in master["article_units"]:
        body_class = unit["body_class"]
        accent = unit["accent"]
        accent_light = unit["accent_light"]
        accent_badge = unit["accent_badge"]
        dark_accent = lighten_for_dark_mode(accent)
        dark_light = rgba_from_hex(accent, 0.15)
        dark_badge = rgba_from_hex(accent, 0.25)
        lines.append(
            f"body.{body_class} {{ --accent: {accent}; --accent-light: {accent_light}; --accent-badge: {accent_badge}; }}"
        )
        lines.append(
            f"body.dark-mode.{body_class} {{ --accent: {dark_accent}; --accent-light: {dark_light}; --accent-badge: {dark_badge}; }}"
        )
    lines.append("/* AUTOGEN-MARKER-END: history-aqa unit accents */")
    lines.append("")
    return "\n".join(lines)


def install_css():
    css_path = ROOT / "css" / "style.css"
    css_text = css_path.read_text(encoding="utf-8")
    if "AUTOGEN-MARKER: history-aqa" in css_text:
        print("  CSS already installed, skipping")
        return
    block = build_css_block()
    # Append at end of file (existing file already grouped by subject)
    css_path.write_text(css_text.rstrip() + "\n" + block, encoding="utf-8")
    print(f"  CSS appended: {len(master['article_units']) * 2} rules added to {css_path}")


# ─────────────────────────────────────── SUBJECT_ORDER append

def install_subject_order():
    p = scripts / "generate_cinematic_videos.py"
    text = p.read_text(encoding="utf-8")
    if '"history-aqa"' in text:
        print("  SUBJECT_ORDER already includes history-aqa, skipping")
        return
    # Insert "history-aqa" after the existing "history" entry
    new_text = re.sub(
        r'(\n\s*"history",\n)',
        r'\1    "history-aqa",\n',
        text,
        count=1,
    )
    if new_text == text:
        print("  WARNING: could not locate 'history' entry in SUBJECT_ORDER")
        return
    p.write_text(new_text, encoding="utf-8")
    print(f"  SUBJECT_ORDER updated: 'history-aqa' added after 'history'")


# ─────────────────────────────────────── Unsplash subject hero

def install_subject_hero():
    target = ROOT / "images" / "subject-history-aqa.jpg"
    if target.exists():
        print(f"  Hero image already at {target}, skipping download")
        return _attach_hero_url_to_subject()

    if not os.environ.get("UNSPLASH_ACCESS_KEY"):
        print("  WARNING: UNSPLASH_ACCESS_KEY not set — skipping hero pull")
        return

    queries = [
        "vintage history book parchment",
        "old library archive",
        "history museum exhibition",
        "ancient manuscript",
    ]
    chosen = None
    for q in queries:
        results = search_unsplash(q, per_page=8)
        if results:
            chosen = results[0]
            safe_title = (chosen["title"] or "").encode("ascii", errors="ignore").decode("ascii")
            safe_photog = (chosen["photographer"] or "").encode("ascii", errors="ignore").decode("ascii")
            print(f"  Hero candidate from query '{q}': '{safe_title}' by {safe_photog}")
            break
    if not chosen:
        print("  WARNING: no Unsplash hero found — leaving image_url null")
        return

    # Download regular size (1080w) and save
    resp = requests.get(chosen["url"], timeout=30)
    resp.raise_for_status()
    target.write_bytes(resp.content)
    print(f"  Hero saved to {target} ({len(resp.content):,} bytes)")
    trigger_unsplash_download(chosen.get("_download_location", ""))
    return _attach_hero_url_to_subject(local_path=str(target.relative_to(ROOT).as_posix()))


def _attach_hero_url_to_subject(local_path: str = "images/subject-history-aqa.jpg"):
    sb = get_client()
    sb.table("subjects").update({"image_url": "/" + local_path}).eq(
        "slug", "history-aqa"
    ).is_("school_id", "null").execute()
    print(f"  subjects.image_url set to /{local_path}")


# ─────────────────────────────────────── run

if __name__ == "__main__":
    print("=== CSS ===")
    install_css()
    print("\n=== SUBJECT_ORDER ===")
    install_subject_order()
    print("\n=== Unsplash subject hero ===")
    install_subject_hero()
    print("\n=== Phase 2 activation finalised ===")
