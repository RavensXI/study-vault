"""Generate all 12 Drama GCSE diagrams using the matplotlib -> Gemini pictorial pipeline.

Blood Brothers (lessons 1-8): structural diagrams for plot, characters, themes, costumes,
staging, lighting/sound, performance skills, and key scenes.

Rise Up (lessons 9-12): context timeline, stage layouts, and SEAS paragraph structure.

Usage:
    python scripts/generate_drama_diagrams.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import base64
import time
import urllib.request
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ArrowStyle
import matplotlib.patheffects as pe
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image-preview"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BB_DIR = os.path.join(PROJECT_ROOT, "drama", "blood-brothers")
RU_DIR = os.path.join(PROJECT_ROOT, "drama", "rise-up")

os.makedirs(BB_DIR, exist_ok=True)
os.makedirs(RU_DIR, exist_ok=True)

# Drama purple palette (dark -> light)
PURPLE_DARKEST = "#4c1d95"
PURPLE_DARK    = "#6d28d9"
PURPLE_MID     = "#7c3aed"
PURPLE_LIGHT   = "#8b5cf6"
PURPLE_LIGHTER = "#a78bfa"
PURPLE_LIGHTEST = "#c4b5fd"
CREAM = "#faf8f5"
WARM_DARK = "#2d2a26"

# ---------------------------------------------------------------------------
# Gemini API helper
# ---------------------------------------------------------------------------
def call_gemini(matplotlib_path, output_path, prompt):
    """Send matplotlib image to Gemini for pictorial infographic transformation."""
    with open(matplotlib_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "contents": [{"parts": [
            {"text": prompt},
            {"inlineData": {"mimeType": "image/jpeg", "data": img_data}}
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    print(f"  Calling Gemini API for {os.path.basename(output_path)}...")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR: Gemini API call failed: {e}")
        return False

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  Saved Gemini output: {os.path.basename(output_path)}")
                return True

    print(f"  WARNING: No image in Gemini response for {os.path.basename(output_path)}")
    # Check for text-only response or errors
    if result.get("candidates"):
        for part in result["candidates"][0].get("content", {}).get("parts", []):
            if "text" in part:
                print(f"  Gemini text: {part['text'][:200]}")
    return False


# ---------------------------------------------------------------------------
# Common Gemini prompt parts
# ---------------------------------------------------------------------------
COMMON_STYLE = """You are a world-class infographic designer creating a STRUCTURAL DIAGRAM for a GCSE Drama revision website (students aged 15-16). The site uses a purple theme.

I'm giving you a matplotlib structural diagram as a LAYOUT REFERENCE. Transform it into a polished, engaging PICTORIAL INFOGRAPHIC that a teenager would find clear and memorable.

STYLE DIRECTION:
- Think "editorial magazine infographic" or "BBC Bitesize visual"
- Clean, flat-design, vector-illustration style (not realistic or photographic)
- Use small thematic icons or illustrations to make it visually engaging
- All text must be clearly legible at normal zoom
- Keep the SAME data/structure as the matplotlib reference — do NOT add or remove items
"""

COMMON_RULES = """
DESIGN RULES:
- Purple colour scheme (primary: #7c3aed, dark: #4c1d95, accents: #8b5cf6, #a78bfa, #c4b5fd)
- Landscape orientation, roughly 1800x1050 pixels
- White or very light warm cream (#faf8f5) background
- Clean modern sans-serif typography
- No watermarks, no photographic elements, no AI artifacts, no hands
- Flat design, vector-illustration style
- All labels must appear ONLY ONCE (no duplicate text above AND below elements)
"""


# ===========================================================================
# MATPLOTLIB GENERATORS
# ===========================================================================

def draw_lesson_01(out_dir):
    """L01: Blood Brothers — Cyclical Structure Timeline"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    events = [
        ("Opening", "Death of the Twins\n(Narrator reveals ending)"),
        ("Act 1\nEarly", "Mrs Johnstone gives\naway baby Edward"),
        ("Act 1\nMiddle", "Boys meet at age 7,\nbecome blood brothers"),
        ("Act 1\nLate", "Mrs Lyons fires\nMrs Johnstone"),
        ("Act 2\nEarly", "Teenagers reunite,\nLinda joins the group"),
        ("Act 2\nMiddle", "Mickey unemployed,\nEdward at university"),
        ("Act 2\nLate", "Mickey imprisoned,\nLinda's affair"),
        ("Climax", "Confrontation at\nTown Hall — both die"),
    ]

    # Draw a curved path with boxes
    n = len(events)
    # Positions in an elongated oval
    angles = np.linspace(np.pi, -np.pi, n, endpoint=False)
    cx, cy = 7, 3.5
    rx, ry = 5.5, 2.5
    xs = cx + rx * np.cos(angles)
    ys = cy + ry * np.sin(angles)

    colors = [PURPLE_DARKEST, PURPLE_DARK, PURPLE_MID, PURPLE_LIGHT,
              PURPLE_LIGHTER, PURPLE_MID, PURPLE_DARK, PURPLE_DARKEST]

    # Draw connecting arrows
    for i in range(n):
        j = (i + 1) % n
        ax.annotate("", xy=(xs[j], ys[j]), xytext=(xs[i], ys[i]),
                     arrowprops=dict(arrowstyle="-|>", color=PURPLE_LIGHTER,
                                     lw=2.5, connectionstyle="arc3,rad=0.15"))

    # Draw event boxes
    for i, (label, desc) in enumerate(events):
        box = FancyBboxPatch((xs[i] - 1.3, ys[i] - 0.7), 2.6, 1.4,
                             boxstyle="round,pad=0.15", facecolor=colors[i],
                             edgecolor="white", linewidth=2)
        ax.add_patch(box)
        ax.text(xs[i], ys[i] + 0.2, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color="white")
        ax.text(xs[i], ys[i] - 0.25, desc, ha="center", va="center",
                fontsize=6.5, color="#e8e0f0", linespacing=1.2)

    # Cyclical arrow label in centre
    ax.text(cx, cy + 0.3, "CYCLICAL\nSTRUCTURE", ha="center", va="center",
            fontsize=16, fontweight="bold", color=PURPLE_DARKEST)
    ax.text(cx, cy - 0.5, '"Begins and ends in\nthe self same way"',
            ha="center", va="center", fontsize=10, color=PURPLE_MID, style="italic")

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("Blood Brothers — Cyclical Structure", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_cyclical_structure_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_02(out_dir):
    """L02: Blood Brothers — Character Relationship Map"""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # Character positions (x, y)
    chars = {
        "Mrs Johnstone":   (3, 7),
        "Mrs Lyons":       (11, 7),
        "Mickey":          (3, 4),
        "Edward":          (11, 4),
        "Linda":           (7, 3),
        "Sammy":           (1, 2.5),
        "Narrator":        (7, 8.5),
        "Mr Lyons":        (13, 6),
    }

    colors_map = {
        "Mrs Johnstone": PURPLE_DARK,
        "Mrs Lyons": PURPLE_DARKEST,
        "Mickey": "#c44536",  # Working class - red
        "Edward": "#2563eb",  # Upper class - blue
        "Linda": "#db2777",   # Pink
        "Sammy": "#6b7280",   # Grey
        "Narrator": PURPLE_MID,
        "Mr Lyons": "#2563eb",
    }

    # Draw relationship lines first
    relationships = [
        ("Mrs Johnstone", "Mickey", "Mother\n(raises)", PURPLE_DARK),
        ("Mrs Johnstone", "Edward", "Birth mother\n(gives away)", PURPLE_DARK),
        ("Mrs Lyons", "Edward", "Adoptive\nmother", PURPLE_DARKEST),
        ("Mrs Lyons", "Mrs Johnstone", "Employer →\nManipulator", PURPLE_DARKEST),
        ("Mickey", "Edward", "Blood brothers /\nTwin brothers", PURPLE_MID),
        ("Mickey", "Linda", "Marries", "#db2777"),
        ("Edward", "Linda", "Affair", "#db2777"),
        ("Sammy", "Mickey", "Older\nbrother", "#6b7280"),
        ("Mr Lyons", "Mrs Lyons", "Husband", "#2563eb"),
        ("Narrator", "Mickey", "Foreshadows\nfate", PURPLE_LIGHTER),
        ("Narrator", "Edward", "Foreshadows\nfate", PURPLE_LIGHTER),
    ]

    for c1, c2, label, col in relationships:
        x1, y1 = chars[c1]
        x2, y2 = chars[c2]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.plot([x1, x2], [y1, y2], color=col, lw=2, alpha=0.5, zorder=1)
        ax.text(mx, my, label, ha="center", va="center", fontsize=6,
                color=col, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor=col, alpha=0.9), zorder=3)

    # Draw character boxes
    for name, (x, y) in chars.items():
        col = colors_map[name]
        box = FancyBboxPatch((x - 1.2, y - 0.5), 2.4, 1.0,
                             boxstyle="round,pad=0.15", facecolor=col,
                             edgecolor="white", linewidth=2, zorder=4)
        ax.add_patch(box)
        ax.text(x, y, name, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=5)

    # Legend for class divide
    ax.text(7, 1.2, "Working Class (Johnstones)", ha="center",
            fontsize=9, color="#c44536", fontweight="bold")
    ax.text(7, 0.7, "Upper Class (Lyons)", ha="center",
            fontsize=9, color="#2563eb", fontweight="bold")

    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Blood Brothers — Character Relationship Map", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_character_relationships_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_03(out_dir):
    """L03: Blood Brothers — Themes & Context Concept Map"""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # Centre node
    cx, cy = 7, 4.5

    themes = [
        ("Social Class", "Mickey vs Edward\nPoverty vs privilege", 0),
        ("Fate & Destiny", "Superstition, Narrator\n'Shoes upon the table'", 1),
        ("Nature vs\nNurture", "Same genes, different\nupbringing → different lives", 2),
        ("Education", "Edward → university\nMickey → no qualifications", 3),
        ("Growing Up", "Childhood innocence lost\nAdulthood brings tragedy", 4),
        ("Money", "Catalogue debts,\nredundancy, inequality", 5),
        ("Men &\nWomen", "Mrs J's sacrifice,\nLinda's choices", 6),
    ]

    n = len(themes)
    radius = 3.2
    angles = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, n, endpoint=False)

    colors = [PURPLE_DARKEST, PURPLE_DARK, PURPLE_MID, PURPLE_LIGHT,
              PURPLE_LIGHTER, PURPLE_MID, PURPLE_DARK]

    # Draw centre
    centre_box = FancyBboxPatch((cx - 1.5, cy - 0.6), 3.0, 1.2,
                                boxstyle="round,pad=0.2", facecolor=PURPLE_DARKEST,
                                edgecolor="white", linewidth=3)
    ax.add_patch(centre_box)
    ax.text(cx, cy, "BLOOD\nBROTHERS\nTHEMES", ha="center", va="center",
            fontsize=13, fontweight="bold", color="white")

    for i, (theme, detail, _) in enumerate(themes):
        x = cx + radius * np.cos(angles[i])
        y = cy + radius * np.sin(angles[i])

        # Connecting line
        ax.plot([cx, x], [cy, y], color=colors[i], lw=2.5, alpha=0.6, zorder=1)

        # Theme box
        box = FancyBboxPatch((x - 1.4, y - 0.6), 2.8, 1.2,
                             boxstyle="round,pad=0.15", facecolor=colors[i],
                             edgecolor="white", linewidth=2, zorder=4)
        ax.add_patch(box)
        ax.text(x, y + 0.15, theme, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="white", zorder=5)
        ax.text(x, y - 0.28, detail, ha="center", va="center",
                fontsize=6, color="#e8e0f0", zorder=5, linespacing=1.2)

    # Context labels
    contexts = [
        ("Social Context", "Relationships, class divide,\ndiscrimination", 1, 0.8),
        ("Historical Context", "Thatcher era, Toxteth riots,\nunemployment, welfare cuts", 7, 0.8),
        ("Cultural Context", "Cinema, Beatles, street play,\nmusicals of the 1980s", 13, 0.8),
    ]
    for label, desc, x, y in contexts:
        ax.text(x, y + 0.2, label, ha="center", fontsize=7.5,
                fontweight="bold", color=PURPLE_DARK)
        ax.text(x, y - 0.15, desc, ha="center", fontsize=6,
                color=PURPLE_MID, linespacing=1.2)

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_title("Blood Brothers — Themes & Context", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_themes_context_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_04(out_dir):
    """L04: Blood Brothers — Colour Symbolism Chart"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    colour_data = [
        ("#dc2626", "Red", "Labour Party, danger, anger,\nblood, Mrs Lyons' rage",
         "Mickey's jumper, Mrs Lyons'\ncardigan (older)"),
        ("#2563eb", "Blue", "Conservative Party, wealth,\ncold, isolation",
         "Edward's jumper,\nMr Lyons' tie"),
        ("#ec4899", "Pink", "Warmth, love, femininity,\nfun, romance",
         "Mrs Johnstone's dress\n(loving nature)"),
        ("#111827", "Black", "Crime, shadows, mourning,\nsinister, death",
         "Sammy's clothes (criminal life),\nMrs Lyons (older - madness)"),
        ("#eab308", "Yellow", "Hope, positivity,\nenthusiasm, brightness",
         "Linda as a child\n(positive personality)"),
        ("#f3f4f6", "White", "Purity, innocence,\nhygiene, cleanliness",
         "Edward's shirt (privilege),\nNarrator's shirt"),
        ("#6b7280", "Grey", "Dullness, conformity,\npoverty, loss of hope",
         "Mickey's shorts (poverty),\nMrs Lyons' suit (formality)"),
    ]

    y_start = 6.0
    for i, (hex_col, name, meanings, examples) in enumerate(colour_data):
        y = y_start - i * 0.85

        # Colour swatch
        swatch = FancyBboxPatch((0.5, y - 0.3), 1.2, 0.6,
                                boxstyle="round,pad=0.05",
                                facecolor=hex_col,
                                edgecolor=PURPLE_LIGHTER, linewidth=1.5)
        ax.add_patch(swatch)

        # Colour name
        text_col = "white" if hex_col in ["#111827"] else WARM_DARK
        if hex_col == "#f3f4f6":
            text_col = "#6b7280"
        ax.text(1.1, y, name, ha="center", va="center",
                fontsize=10, fontweight="bold", color=text_col if hex_col in ["#111827"] else WARM_DARK)

        # Meanings column
        ax.text(4.5, y, meanings, ha="center", va="center",
                fontsize=7.5, color=WARM_DARK, linespacing=1.3)

        # Examples column
        ax.text(9.5, y, examples, ha="center", va="center",
                fontsize=7.5, color=PURPLE_DARK, linespacing=1.3)

    # Column headers
    ax.text(1.1, y_start + 0.6, "COLOUR", ha="center", fontsize=10,
            fontweight="bold", color=PURPLE_DARKEST)
    ax.text(4.5, y_start + 0.6, "SYMBOLISM", ha="center", fontsize=10,
            fontweight="bold", color=PURPLE_DARKEST)
    ax.text(9.5, y_start + 0.6, "EXAMPLES IN PLAY", ha="center", fontsize=10,
            fontweight="bold", color=PURPLE_DARKEST)

    # Divider lines
    for x_div in [2.5, 6.8]:
        ax.plot([x_div, x_div], [0, y_start + 0.3], color=PURPLE_LIGHTEST,
                lw=1, alpha=0.5)

    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")
    ax.set_title("Blood Brothers — Colour Symbolism in Costume & Design",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_colour_symbolism_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_05(out_dir):
    """L05: Blood Brothers — Staging Types Comparison (top-down views)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor(CREAM)
    fig.suptitle("Four Key Staging Types — Top-Down View", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, y=0.98)

    staging = [
        ("Proscenium Arch", "Audience on ONE side\nMany entrances & exits\nFly loft for set storage\nClear US/DS/SL/SR blocking",
         "front"),
        ("Thrust", "Audience on THREE sides\nSet at the back only\nGreat for large-scale\nActors respond to 3 sides",
         "thrust"),
        ("Traverse", "Audience on TWO sides\n(like a catwalk)\nLimited set & exits\nActors keep moving",
         "traverse"),
        ("In the Round", "Audience on ALL sides\nIntimate environment\nNo large set pieces\nMust move constantly",
         "round"),
    ]

    for idx, (title, notes, stype) in enumerate(staging):
        ax = axes[idx // 2][idx % 2]
        ax.set_facecolor(CREAM)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

        ax.set_title(title, fontsize=12, fontweight="bold", color=PURPLE_DARK, pad=8)

        # Draw stage area
        if stype == "front":
            # Proscenium: rectangular stage at top, audience below
            stage = FancyBboxPatch((2, 5.5), 6, 3, boxstyle="round,pad=0.1",
                                   facecolor=PURPLE_LIGHTEST, edgecolor=PURPLE_MID, lw=2)
            ax.add_patch(stage)
            ax.text(5, 7, "STAGE", ha="center", va="center", fontsize=10,
                    fontweight="bold", color=PURPLE_DARKEST)
            # Audience
            for row in range(3):
                for col in range(8):
                    ax.plot(1.5 + col * 1.0, 4 - row * 1.0, "o",
                            color=PURPLE_MID, markersize=6, alpha=0.6)
            ax.text(5, 0.8, "AUDIENCE", ha="center", fontsize=9, color=PURPLE_MID)

        elif stype == "thrust":
            # Thrust: stage sticking out, audience on 3 sides
            stage = FancyBboxPatch((3, 4), 4, 4, boxstyle="round,pad=0.1",
                                   facecolor=PURPLE_LIGHTEST, edgecolor=PURPLE_MID, lw=2)
            ax.add_patch(stage)
            ax.text(5, 6, "STAGE", ha="center", va="center", fontsize=10,
                    fontweight="bold", color=PURPLE_DARKEST)
            # Audience: left, front, right
            for row in range(3):
                for col in range(5):
                    ax.plot(1.5 + col * 1.0, 2.5 - row * 0.8, "o",
                            color=PURPLE_MID, markersize=5, alpha=0.6)
            for row in range(4):
                ax.plot(1.5, 4.5 + row * 0.8, "o", color=PURPLE_MID, markersize=5, alpha=0.6)
                ax.plot(8.5, 4.5 + row * 0.8, "o", color=PURPLE_MID, markersize=5, alpha=0.6)
            ax.text(5, 0.5, "AUDIENCE", ha="center", fontsize=8, color=PURPLE_MID)

        elif stype == "traverse":
            # Traverse: long stage in middle, audience on 2 sides
            stage = FancyBboxPatch((3, 3), 4, 4, boxstyle="round,pad=0.1",
                                   facecolor=PURPLE_LIGHTEST, edgecolor=PURPLE_MID, lw=2)
            ax.add_patch(stage)
            ax.text(5, 5, "STAGE", ha="center", va="center", fontsize=10,
                    fontweight="bold", color=PURPLE_DARKEST)
            for row in range(4):
                for col in range(2):
                    ax.plot(1.0 + col * 0.7, 3.5 + row * 1.0, "o",
                            color=PURPLE_MID, markersize=5, alpha=0.6)
                    ax.plot(8.0 + col * 0.7, 3.5 + row * 1.0, "o",
                            color=PURPLE_MID, markersize=5, alpha=0.6)
            ax.text(1.3, 8, "AUDIENCE", ha="center", fontsize=8, color=PURPLE_MID)
            ax.text(8.3, 8, "AUDIENCE", ha="center", fontsize=8, color=PURPLE_MID)

        elif stype == "round":
            # In the round: circular stage, audience all around
            circle = plt.Circle((5, 5), 2, facecolor=PURPLE_LIGHTEST,
                                edgecolor=PURPLE_MID, lw=2)
            ax.add_patch(circle)
            ax.text(5, 5, "STAGE", ha="center", va="center", fontsize=10,
                    fontweight="bold", color=PURPLE_DARKEST)
            for angle in np.linspace(0, 2 * np.pi, 16, endpoint=False):
                ax.plot(5 + 3.2 * np.cos(angle), 5 + 3.2 * np.sin(angle), "o",
                        color=PURPLE_MID, markersize=5, alpha=0.6)
            ax.text(5, 0.5, "AUDIENCE (all sides)", ha="center",
                    fontsize=8, color=PURPLE_MID)

        # Notes
        ax.text(5, -0.3, notes, ha="center", va="top", fontsize=6.5,
                color=WARM_DARK, linespacing=1.3,
                bbox=dict(facecolor="white", edgecolor=PURPLE_LIGHTEST,
                          boxstyle="round,pad=0.3", alpha=0.8))

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    path = os.path.join(out_dir, "diagram_staging_types_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_06(out_dir):
    """L06: Blood Brothers — Lighting & Sound Design (Mood vs Atmosphere)"""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 8))
    fig.patch.set_facecolor(CREAM)
    fig.suptitle("Blood Brothers — Lighting & Sound Design", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, y=0.98)

    # LEFT: Lighting techniques
    ax = ax_left
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("LIGHTING\n(Creates Atmosphere)", fontsize=12,
                 fontweight="bold", color=PURPLE_DARK, pad=10)

    lighting = [
        ("Wash / Flood", "Warm straw wash when\nMickey & Edward first meet\n= happiness", "#fbbf24"),
        ("Spotlight", "White spotlight on Mrs J\nin final scene = isolation\nand truth revealed", "#f3f4f6"),
        ("Gobo", "Prison bar gobo with\nwhite light = Mickey trapped\nin prison & mental anguish", "#6b7280"),
        ("Crossfade", "Straw → steel wash in\nbattle scene = joy → misery", PURPLE_LIGHTER),
        ("Strobe", "Pulsating blue/red for\nfinal scene = police arrival\n= foreshadow danger", "#dc2626"),
    ]

    for i, (technique, desc, col) in enumerate(lighting):
        y = 8.5 - i * 1.7
        swatch = FancyBboxPatch((0.3, y - 0.5), 1.2, 1.0,
                                boxstyle="round,pad=0.1", facecolor=col,
                                edgecolor=PURPLE_MID, lw=1.5)
        ax.add_patch(swatch)
        ax.text(2.0, y + 0.1, technique, fontsize=9, fontweight="bold",
                color=PURPLE_DARKEST, va="center")
        ax.text(2.0, y - 0.35, desc, fontsize=6.5, color=WARM_DARK,
                va="center", linespacing=1.2)

    # RIGHT: Sound techniques
    ax = ax_right
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("SOUND\n(Creates Mood & Atmosphere)", fontsize=12,
                 fontweight="bold", color=PURPLE_DARK, pad=10)

    sound = [
        ("Live Orchestra", "Expectation of the\nplaywright for a musical.\nAllows incidental music."),
        ("Sound Effects", "Singular magpie cackle\nwhen Mrs J swears on\nbible = foreshadow sorrow"),
        ("Diegetic", "Cow mooing at end of\nAct 1 = arrived in\nthe country"),
        ("Underscoring", "Beatles song while Mrs J\ncleans = fun nature,\nlocation & time period"),
        ("Non-diegetic", "Heartbeat when Mrs J\nswears on bible =\nstressful decision"),
    ]

    for i, (technique, desc) in enumerate(sound):
        y = 8.5 - i * 1.7
        box = FancyBboxPatch((0.3, y - 0.5), 1.2, 1.0,
                             boxstyle="round,pad=0.1", facecolor=PURPLE_MID,
                             edgecolor="white", lw=1.5)
        ax.add_patch(box)
        ax.text(0.9, y, technique.split()[0] if len(technique.split()) == 1
                else technique[:6], ha="center", va="center",
                fontsize=6.5, fontweight="bold", color="white", rotation=0)
        ax.text(2.0, y + 0.1, technique, fontsize=9, fontweight="bold",
                color=PURPLE_DARKEST, va="center")
        ax.text(2.0, y - 0.35, desc, fontsize=6.5, color=WARM_DARK,
                va="center", linespacing=1.2)

    # Bottom key
    fig.text(0.5, 0.02,
             "MOOD = created by what actors do  |  ATMOSPHERE = created by design elements (lighting, sound, set)",
             ha="center", fontsize=10, color=PURPLE_DARK, fontweight="bold")

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    path = os.path.join(out_dir, "diagram_lighting_sound_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_07(out_dir):
    """L07: Blood Brothers — Performance Skills (Voice + Physicality) Reference"""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 8))
    fig.patch.set_facecolor(CREAM)
    fig.suptitle("Blood Brothers — Performance Skills Reference", fontsize=16,
                 fontweight="bold", color=PURPLE_DARKEST, y=0.98)

    # LEFT: Voice skills (CTPAPVE mnemonic)
    ax = ax_left
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("VOICE SKILLS", fontsize=13, fontweight="bold",
                 color=PURPLE_DARK, pad=10)

    voice_skills = [
        ("C", "Clarity", "Clear diction so audience understands every word"),
        ("T", "Tone", "Emotional quality (angry, sad, sarcastic, warm)"),
        ("P", "Pace", "Speed of delivery (fast = panic, slow = sadness)"),
        ("A", "Accent", "RP = wealth/education, Scouse = working class"),
        ("P", "Pitch", "High = excitement/fear, Low = authority/threat"),
        ("V", "Volume", "Loud = anger/power, Quiet = intimacy/secrecy"),
        ("E", "Emphasis", "Stress key words to change meaning"),
    ]

    # Also: Pause
    voice_skills.append(("—", "Pause", "Silence before/after key lines for impact"))

    for i, (letter, skill, desc) in enumerate(voice_skills):
        y = 9.0 - i * 1.05
        # Letter circle
        circle = plt.Circle((1.0, y), 0.35, facecolor=PURPLE_DARK,
                             edgecolor="white", lw=2)
        ax.add_patch(circle)
        ax.text(1.0, y, letter, ha="center", va="center",
                fontsize=12, fontweight="bold", color="white")
        ax.text(2.0, y + 0.15, skill, fontsize=10, fontweight="bold",
                color=PURPLE_DARKEST, va="center")
        ax.text(2.0, y - 0.2, desc, fontsize=7, color=WARM_DARK, va="center")

    # RIGHT: Physicality skills
    ax = ax_right
    ax.set_facecolor(CREAM)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("PHYSICALITY SKILLS", fontsize=13, fontweight="bold",
                 color=PURPLE_DARK, pad=10)

    phys_skills = [
        ("EC", "Eye Contact", "Direct = confidence, Averted = guilt/fear"),
        ("FE", "Facial Expression", "Shows emotion (shock, joy, despair)"),
        ("Po", "Posture", "Upright = confidence, Slumped = defeat"),
        ("MT", "Muscle Tension", "Tense = anger/stress, Relaxed = calm"),
        ("Ge", "Gesture", "Pointing = accusation, Open palms = sincerity"),
        ("BL", "Body Language", "Open = welcoming, Closed = defensive"),
        ("Ga", "Gait", "Stride = confidence, Shuffle = depression"),
        ("Lv", "Levels", "High = power, Low = powerlessness"),
        ("Px", "Proximity", "Close = intimacy/threat, Far = isolation"),
    ]

    for i, (abbr, skill, desc) in enumerate(phys_skills):
        y = 9.0 - i * 0.93
        circle = plt.Circle((1.0, y), 0.35, facecolor=PURPLE_MID,
                             edgecolor="white", lw=2)
        ax.add_patch(circle)
        ax.text(1.0, y, abbr, ha="center", va="center",
                fontsize=9, fontweight="bold", color="white")
        ax.text(2.0, y + 0.15, skill, fontsize=10, fontweight="bold",
                color=PURPLE_DARKEST, va="center")
        ax.text(2.0, y - 0.2, desc, fontsize=7, color=WARM_DARK, va="center")

    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    path = os.path.join(out_dir, "diagram_performance_skills_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_08(out_dir):
    """L08: Blood Brothers — 10 Key Scenes Timeline with Dramatic Conventions"""
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    scenes = [
        ("1", "Mrs J agrees to\ngive away baby", "Marking the\nmoment", PURPLE_DARKEST),
        ("2", "Mickey & Edward\nbecome friends", "Dramatic\nirony", PURPLE_DARK),
        ("3", "Children pick\non Mickey", "Duologue", PURPLE_MID),
        ("4", "Mrs J gives Edward\nthe locket", "Foreshadowing", PURPLE_LIGHT),
        ("5", "Mrs Lyons tries to\nstab Mrs Johnstone", "Climax /\nMarking moment", PURPLE_DARKEST),
        ("6", "Mickey asks\nLinda out", "Cross-cutting", PURPLE_DARK),
        ("7", "Mr Lyons makes\nstaff redundant", "Social context", PURPLE_MID),
        ("8", "Mickey in prison", "Monologue", PURPLE_LIGHT),
        ("9", "Linda hides Mickey's\nantidepressants", "Cross-cutting", PURPLE_DARK),
        ("10", "The final scene:\nboth twins die", "Dramatic irony /\nTragedy", PURPLE_DARKEST),
    ]

    n = len(scenes)
    # Two rows: 5 on top, 5 on bottom
    for i, (num, desc, convention, col) in enumerate(scenes):
        if i < 5:
            x = 1.5 + i * 3.0
            y = 5.5
        else:
            x = 1.5 + (i - 5) * 3.0
            y = 2.0

        # Scene box
        box = FancyBboxPatch((x - 1.2, y - 0.8), 2.4, 1.6,
                             boxstyle="round,pad=0.15", facecolor=col,
                             edgecolor="white", linewidth=2)
        ax.add_patch(box)

        # Scene number
        ax.text(x, y + 0.35, f"Scene {num}", ha="center", va="center",
                fontsize=9, fontweight="bold", color="white")
        ax.text(x, y - 0.05, desc, ha="center", va="center",
                fontsize=7, color="#e8e0f0", linespacing=1.2)

        # Convention label below box
        conv_y = y - 1.1 if i < 5 else y + 1.1
        ax.text(x, conv_y, convention, ha="center", va="center",
                fontsize=6.5, fontweight="bold", color=col,
                bbox=dict(facecolor="white", edgecolor=col,
                          boxstyle="round,pad=0.2", alpha=0.8))

    # Arrows connecting scenes
    for i in range(4):
        x1 = 1.5 + i * 3.0 + 1.2
        x2 = 1.5 + (i + 1) * 3.0 - 1.2
        ax.annotate("", xy=(x2, 5.5), xytext=(x1, 5.5),
                     arrowprops=dict(arrowstyle="-|>", color=PURPLE_LIGHTER, lw=2))
    # Curve from row 1 to row 2
    ax.annotate("", xy=(13.5 + 1.2, 2.0), xytext=(13.5 + 1.2, 5.5),
                arrowprops=dict(arrowstyle="-|>", color=PURPLE_LIGHTER, lw=2,
                               connectionstyle="arc3,rad=-0.5"))
    for i in range(4):
        x1 = 1.5 + i * 3.0 + 1.2
        x2 = 1.5 + (i + 1) * 3.0 - 1.2
        ax.annotate("", xy=(x2, 2.0), xytext=(x1, 2.0),
                     arrowprops=dict(arrowstyle="-|>", color=PURPLE_LIGHTER, lw=2))

    ax.set_xlim(-0.5, 16.5)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("Blood Brothers — 10 Key Scenes with Dramatic Conventions",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_key_scenes_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_09(out_dir):
    """L09: Rise Up — Freedom Riders Timeline (1960s Events)"""
    fig, ax = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    events = [
        ("1960", "Student sit-ins begin\nat lunch counters across\nthe Southern states"),
        ("Feb\n1961", "CORE and SNCC\norganise the first\nFreedom Rides"),
        ("May\n1961", "First bus attacked\nin Anniston, Alabama\n(firebombed)"),
        ("May\n1961", "Riders beaten in\nBirmingham by\nwhite mob"),
        ("May\n1961", "Diane Nash organises\nsecond wave from\nNashville"),
        ("May\n1961", "Riders arrested in\nJackson, Mississippi\nby Bull Connor"),
        ("Sep\n1961", "ICC ruling bans\nsegregation on\ninterstate travel"),
        ("1964", "Civil Rights Act\npassed — outlaws\ndiscrimination"),
    ]

    n = len(events)
    # Horizontal timeline
    y_line = 3.5
    x_start, x_end = 1.0, 15.0
    ax.plot([x_start, x_end], [y_line, y_line], color=PURPLE_MID, lw=4)

    colors = [PURPLE_DARKEST, PURPLE_DARK, "#dc2626", "#dc2626",
              PURPLE_MID, PURPLE_DARK, PURPLE_LIGHT, PURPLE_DARKEST]

    for i, (date, desc) in enumerate(events):
        x = x_start + i * (x_end - x_start) / (n - 1)

        # Alternate above and below
        if i % 2 == 0:
            y_box = y_line + 1.2
            y_date = y_line + 0.5
        else:
            y_box = y_line - 1.2
            y_date = y_line - 0.5

        # Dot on timeline
        ax.plot(x, y_line, "o", color=colors[i], markersize=12, zorder=5)

        # Date label
        ax.text(x, y_date, date, ha="center", va="center",
                fontsize=8, fontweight="bold", color=colors[i])

        # Event box
        box = FancyBboxPatch((x - 0.85, y_box - 0.5), 1.7, 1.0,
                             boxstyle="round,pad=0.1", facecolor=colors[i],
                             edgecolor="white", linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y_box, desc, ha="center", va="center",
                fontsize=6, color="white", linespacing=1.2)

        # Connecting line
        ax.plot([x, x], [y_line, y_box + (0.5 if i % 2 == 0 else -0.5)],
                color=colors[i], lw=1.5, alpha=0.5)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("Rise Up — The Freedom Riders Timeline (1960-1964)",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_freedom_riders_timeline_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_10(out_dir):
    """L10: Rise Up — White Shoppers Scene Stage Layout"""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # Stage boundary
    stage = FancyBboxPatch((1, 1), 12, 8, boxstyle="round,pad=0.2",
                           facecolor="#f5f3ff", edgecolor=PURPLE_MID, lw=2)
    ax.add_patch(stage)

    # Stage direction labels
    ax.text(7, 9.3, "UPSTAGE (back of stage)", ha="center", fontsize=9,
            color=PURPLE_MID, fontweight="bold")
    ax.text(7, 0.7, "DOWNSTAGE (audience)", ha="center", fontsize=9,
            color=PURPLE_MID, fontweight="bold")
    ax.text(0.3, 5, "STAGE\nRIGHT", ha="center", va="center", fontsize=8,
            color=PURPLE_LIGHTER, rotation=90)
    ax.text(13.7, 5, "STAGE\nLEFT", ha="center", va="center", fontsize=8,
            color=PURPLE_LIGHTER, rotation=270)

    # Steel flats at back
    for i, x in enumerate([3, 7, 11]):
        flat = FancyBboxPatch((x - 1, 7.5), 2, 1.0, boxstyle="round,pad=0.05",
                              facecolor="#9ca3af", edgecolor="#6b7280", lw=1.5)
        ax.add_patch(flat)
        ax.text(x, 8.0, f"Steel Flat", ha="center", va="center",
                fontsize=7, color="white", fontweight="bold")

    # LWG on tall stool - Centre Stage
    lwg = plt.Circle((7, 5.5), 0.6, facecolor=PURPLE_DARKEST, edgecolor="white", lw=2)
    ax.add_patch(lwg)
    ax.text(7, 5.5, "LWG", ha="center", va="center", fontsize=10,
            fontweight="bold", color="white")
    ax.text(7, 4.6, "Little White Girl\n(tall stool, CS)", ha="center",
            fontsize=7, color=PURPLE_DARKEST)

    # White shoppers USL
    for j, dy in enumerate([0, -0.7]):
        shopper = plt.Circle((3.5, 6.5 + dy), 0.4, facecolor=PURPLE_MID,
                             edgecolor="white", lw=1.5)
        ax.add_patch(shopper)
    ax.text(3.5, 5.2, "White Shoppers\n(USL, white gloves,\nstep in on store name)",
            ha="center", fontsize=6.5, color=PURPLE_MID)

    # LWG's Mum USR
    mum = plt.Circle((10.5, 6.5), 0.5, facecolor="#db2777", edgecolor="white", lw=2)
    ax.add_patch(mum)
    ax.text(10.5, 6.5, "Mum", ha="center", va="center", fontsize=9,
            fontweight="bold", color="white")
    ax.text(10.5, 5.7, "LWG's Mum\n(USR)", ha="center", fontsize=7, color="#db2777")

    # Audience area
    for col in range(10):
        ax.plot(3 + col * 0.9, 0.3, "^", color=PURPLE_LIGHTER, markersize=8)
    ax.text(7, -0.2, "AUDIENCE", ha="center", fontsize=10,
            fontweight="bold", color=PURPLE_MID)

    # Lighting note
    ax.text(7, 3.5,
            "Lighting: White wash, intensity increases\non LWG = innocence & purity",
            ha="center", fontsize=8, color=PURPLE_DARK, style="italic",
            bbox=dict(facecolor="white", edgecolor=PURPLE_LIGHTEST,
                      boxstyle="round,pad=0.3"))

    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.8, 10)
    ax.axis("off")
    ax.set_title("Rise Up — White Shoppers Scene: Stage Layout",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_white_shoppers_layout_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_11(out_dir):
    """L11: Rise Up — CJ Reminder Scene Stage Layout (diamond formation)"""
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # Stage boundary
    stage = FancyBboxPatch((1, 1), 12, 8, boxstyle="round,pad=0.2",
                           facecolor="#f5f3ff", edgecolor=PURPLE_MID, lw=2)
    ax.add_patch(stage)

    # Stage direction labels
    ax.text(7, 9.3, "UPSTAGE", ha="center", fontsize=9,
            color=PURPLE_MID, fontweight="bold")
    ax.text(7, 0.7, "DOWNSTAGE (audience)", ha="center", fontsize=9,
            color=PURPLE_MID, fontweight="bold")

    # Steel flats at back
    for i, (x, label) in enumerate([(3, "Confederate\nflag"), (7, "Steel Flat\n(CS)"), (11, "LWG's\nbow")]):
        flat = FancyBboxPatch((x - 1, 7.5), 2, 1.0, boxstyle="round,pad=0.05",
                              facecolor="#9ca3af", edgecolor="#6b7280", lw=1.5)
        ax.add_patch(flat)
        ax.text(x, 8.0, label, ha="center", va="center",
                fontsize=7, color="white", fontweight="bold")

    # Stools
    stool_positions = [(3, 7), (6, 7), (8, 7), (11, 7)]
    stool_labels = ["Small\nstool", "Tall\nstool", "Tall\nstool", "Small\nstool"]
    for (sx, sy), sl in zip(stool_positions, stool_labels):
        ax.plot(sx, sy, "s", color=PURPLE_LIGHTER, markersize=12)
        ax.text(sx, sy - 0.5, sl, ha="center", fontsize=5.5, color=PURPLE_LIGHTER)

    # DIAMOND FORMATION - Characters
    # Ty (Jim) USL on small stool — highest level
    ty = plt.Circle((3, 6.5), 0.5, facecolor=PURPLE_DARK, edgecolor="white", lw=2)
    ax.add_patch(ty)
    ax.text(3, 6.5, "Ty\n(Jim)", ha="center", va="center", fontsize=8,
            fontweight="bold", color="white")
    ax.text(3, 5.5, "USL, on stool\n(highest level = power)",
            ha="center", fontsize=6.5, color=PURPLE_DARK)

    # Em (Thora) USC
    em = plt.Circle((7, 6), 0.5, facecolor=PURPLE_MID, edgecolor="white", lw=2)
    ax.add_patch(em)
    ax.text(7, 6, "Em\n(Thora)", ha="center", va="center", fontsize=8,
            fontweight="bold", color="white")
    ax.text(7, 5.1, "USC", ha="center", fontsize=7, color=PURPLE_MID)

    # Dayz (Merna) CS
    dayz = plt.Circle((7, 4.5), 0.5, facecolor=PURPLE_MID, edgecolor="white", lw=2)
    ax.add_patch(dayz)
    ax.text(7, 4.5, "Dayz\n(Merna)", ha="center", va="center", fontsize=8,
            fontweight="bold", color="white")
    ax.text(7, 3.6, "CS", ha="center", fontsize=7, color=PURPLE_MID)

    # CJ (Hank) DSR
    cj = plt.Circle((10.5, 3), 0.5, facecolor="#dc2626", edgecolor="white", lw=2)
    ax.add_patch(cj)
    ax.text(10.5, 3, "CJ\n(Hank)", ha="center", va="center", fontsize=8,
            fontweight="bold", color="white")
    ax.text(10.5, 2.1, "DSR\n(forced USC when circled)",
            ha="center", fontsize=6.5, color="#dc2626")

    # Diamond shape connecting lines
    diamond_pts = [(3, 6.5), (7, 6), (10.5, 3), (7, 4.5)]
    for i in range(4):
        x1, y1 = diamond_pts[i]
        x2, y2 = diamond_pts[(i + 1) % 4]
        ax.plot([x1, x2], [y1, y2], "--", color=PURPLE_LIGHTER, lw=1.5, alpha=0.5)

    ax.text(6, 4.8, "DIAMOND\nFORMATION", ha="center", va="center",
            fontsize=7, color=PURPLE_LIGHTER, fontweight="bold", style="italic")

    # Circling technique arrow
    from matplotlib.patches import Arc
    arc = Arc((10.5, 3), 3.5, 3.5, angle=0, theta1=30, theta2=330,
              color=PURPLE_DARK, lw=2, ls="--")
    ax.add_patch(arc)
    ax.text(10.5, 1.0, "Circling technique:\nactors circle CJ, reducing\nproxemics to intimidate",
            ha="center", fontsize=7, color=PURPLE_DARK, style="italic",
            bbox=dict(facecolor="white", edgecolor=PURPLE_LIGHTEST,
                      boxstyle="round,pad=0.2"))

    # Audience
    for col in range(10):
        ax.plot(3 + col * 0.9, 0.3, "^", color=PURPLE_LIGHTER, markersize=8)
    ax.text(7, -0.2, "AUDIENCE", ha="center", fontsize=10,
            fontweight="bold", color=PURPLE_MID)

    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-0.8, 10)
    ax.axis("off")
    ax.set_title("Rise Up — CJ Reminder Scene: Diamond Formation & Circling",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_cj_reminder_layout_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


def draw_lesson_12(out_dir):
    """L12: Rise Up — SEAS Paragraph Structure Diagram"""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    steps = [
        ("S", "Statement", "Make a clear point about what you observed.\n"
         "E.g. 'The actor playing CJ used closed body language\n"
         "when the other actors circled him.'"),
        ("E", "Evidence / Example", "Give a specific example from the performance.\n"
         "E.g. 'He held his hands in front of his chest as if\n"
         "to create a barrier from the other actors.'"),
        ("A", "Analysis", "Explain WHY the technique was effective and\n"
         "what it communicated to the audience.\n"
         "E.g. 'This highlighted how intimidated his character felt.'"),
        ("S", "Suggest Development", "How could this moment be improved or developed?\n"
         "E.g. 'To develop further, the actor could use a trembling\n"
         "voice to reinforce his fear to the audience.'"),
    ]

    y_start = 7.0
    for i, (letter, title, desc) in enumerate(steps):
        y = y_start - i * 1.8

        # Letter circle
        circle = plt.Circle((1.5, y), 0.6, facecolor=PURPLE_DARKEST if i in [0, 3]
                             else PURPLE_MID, edgecolor="white", lw=3)
        ax.add_patch(circle)
        ax.text(1.5, y, letter, ha="center", va="center",
                fontsize=20, fontweight="bold", color="white")

        # Title and description
        ax.text(3.0, y + 0.3, title, fontsize=13, fontweight="bold",
                color=PURPLE_DARKEST, va="center")
        ax.text(3.0, y - 0.3, desc, fontsize=8, color=WARM_DARK,
                va="center", linespacing=1.3)

        # Arrow to next step
        if i < 3:
            ax.annotate("", xy=(1.5, y - 0.7), xytext=(1.5, y - 1.1),
                        arrowprops=dict(arrowstyle="-|>", color=PURPLE_LIGHTER, lw=2.5))

    # Footer
    ax.text(7, 0.5, "Use this SEAS structure for EVERY paragraph in Section B (Rise Up essay)",
            ha="center", fontsize=10, fontweight="bold", color=PURPLE_DARK,
            bbox=dict(facecolor=PURPLE_LIGHTEST, edgecolor=PURPLE_MID,
                      boxstyle="round,pad=0.4", alpha=0.3))

    ax.set_xlim(0, 14)
    ax.set_ylim(-0.2, 8.5)
    ax.axis("off")
    ax.set_title("SEAS Paragraph Structure — Section B Essay Writing",
                 fontsize=16, fontweight="bold", color=PURPLE_DARKEST, pad=15)

    path = os.path.join(out_dir, "diagram_seas_paragraph_matplotlib.jpg")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Saved: {os.path.basename(path)}")
    return path


# ===========================================================================
# GEMINI PROMPTS
# ===========================================================================

GEMINI_PROMPTS = {
    "diagram_cyclical_structure": COMMON_STYLE + """
THIS DIAGRAM: Blood Brothers cyclical structure timeline showing the plot arc.

The play has a CYCLICAL STRUCTURE — it begins and ends with the death of the twins.

8 KEY EVENTS in order around an oval/circle:
1. OPENING — Death of the Twins (Narrator reveals ending)
2. ACT 1 EARLY — Mrs Johnstone gives away baby Edward to Mrs Lyons
3. ACT 1 MIDDLE — Boys meet at age 7, become blood brothers
4. ACT 1 LATE — Mrs Lyons fires Mrs Johnstone, families move
5. ACT 2 EARLY — Teenagers reunite, Linda joins the group
6. ACT 2 MIDDLE — Mickey unemployed, Edward at university
7. ACT 2 LATE — Mickey imprisoned, Linda has affair with Edward
8. CLIMAX — Confrontation at Town Hall — both twins die

The arrow loops back from event 8 to event 1 (cyclical).

VISUAL FORMAT:
- Arrange the 8 events in an oval or circular path with arrows connecting them
- Use theatre/drama icons: stage curtains, masks (comedy/tragedy), a gun, a locket, a bible
- The START and END points should be visually connected with a prominent loop arrow
- Centre text: "CYCLICAL STRUCTURE" with subtitle '"Begins and ends in the self same way"'
- Colour-code: darker purple for start/end (tragedy), lighter purple for middle events
- Each event box should have a small relevant icon

DATA RULES:
- Preserve ALL 8 events exactly as listed
- Labels must appear ONLY once (not above AND below)
""" + COMMON_RULES,

    "diagram_character_relationships": COMMON_STYLE + """
THIS DIAGRAM: Blood Brothers character relationship map showing 8 characters and their connections.

CHARACTERS AND POSITIONS:
- Mrs Johnstone (top left) — working-class mother
- Mrs Lyons (top right) — upper-class employer
- Mickey (middle left) — working-class twin, raised by Mrs Johnstone
- Edward (middle right) — upper-class twin, raised by Mrs Lyons
- Linda (centre bottom) — love interest, marries Mickey, affair with Edward
- Sammy (far left) — Mickey's older brother, criminal
- Narrator (top centre) — fate figure, foreshadows tragedy
- Mr Lyons (far right) — Mrs Lyons' husband, businessman

KEY RELATIONSHIPS (connecting lines):
- Mrs Johnstone → Mickey: "Mother (raises)"
- Mrs Johnstone → Edward: "Birth mother (gives away)"
- Mrs Lyons → Edward: "Adoptive mother"
- Mrs Lyons → Mrs Johnstone: "Employer → Manipulator"
- Mickey ↔ Edward: "Blood brothers / Twin brothers" (central relationship)
- Mickey → Linda: "Marries"
- Edward → Linda: "Affair"
- Sammy → Mickey: "Older brother (leads to crime)"
- Mr Lyons → Mrs Lyons: "Husband"
- Narrator → Mickey & Edward: "Foreshadows fate"

VISUAL FORMAT:
- Character boxes with small drama-themed icons (masks, locket, gun, bible)
- Use RED tones for working-class Johnstones, BLUE tones for upper-class Lyons
- PURPLE for the Narrator (neutral/fate)
- PINK for Linda (love interest connecting both families)
- Relationship lines with labels on them
- The CLASS DIVIDE should be visually clear — a vertical line or gap between the two families
- Mickey and Edward's connection should be the most prominent (thickest line, centre)

DATA RULES:
- Include ALL 8 characters and ALL relationships listed above
- Labels must appear ONLY once per connection
""" + COMMON_RULES,

    "diagram_themes_context": COMMON_STYLE + """
THIS DIAGRAM: Blood Brothers themes and context concept map — 7 themes radiating from a central node, with 3 context types at the bottom.

CENTRAL NODE: "BLOOD BROTHERS THEMES"

7 THEMES radiating outward (each with a brief connection):
1. Social Class — Mickey vs Edward, poverty vs privilege
2. Fate & Destiny — Superstition, Narrator, "Shoes upon the table"
3. Nature vs Nurture — Same genes, different upbringing, different lives
4. Education — Edward goes to university, Mickey has no qualifications
5. Growing Up — Childhood innocence lost, adulthood brings tragedy
6. Money — Catalogue debts, redundancy, inequality
7. Men & Women — Mrs Johnstone's sacrifice, Linda's choices

3 CONTEXT TYPES at the bottom:
- Social Context: Relationships, class divide, discrimination
- Historical Context: Thatcher era, Toxteth riots, unemployment, welfare cuts
- Cultural Context: Cinema, Beatles, street play, musicals of the 1980s

VISUAL FORMAT:
- Central circle with "Blood Brothers Themes" in dark purple
- 7 branches radiating outward, each with a themed icon (scales for social class, dice for fate, DNA for nature/nurture, book for education, clock for growing up, coins for money, male/female figures for men & women)
- Each theme in a rounded box with its connection text below
- 3 context types at the bottom in a separate row with their own sub-icons
- Connections between themes and contexts (e.g. Social Class connects to Social Context)

DATA RULES:
- Include ALL 7 themes and ALL 3 contexts exactly as listed
- Labels ONLY once per element
""" + COMMON_RULES,

    "diagram_colour_symbolism": COMMON_STYLE + """
THIS DIAGRAM: Blood Brothers colour symbolism chart showing 7 colours used in costume and design, their symbolic meanings, and specific examples from the play.

7 COLOURS WITH SYMBOLISM AND EXAMPLES:
1. RED — Symbolism: Labour Party, danger, anger, blood, Mrs Lyons' rage. Examples: Mickey's red jumper, Mrs Lyons' red cardigan (older).
2. BLUE — Symbolism: Conservative Party, wealth, cold, isolation. Examples: Edward's blue jumper, Mr Lyons' blue tie.
3. PINK — Symbolism: Warmth, love, femininity, fun, romance. Examples: Mrs Johnstone's pink dress (loving nature).
4. BLACK — Symbolism: Crime, shadows, mourning, sinister, death. Examples: Sammy's dark clothes (criminal), Mrs Lyons' black (older, madness).
5. YELLOW — Symbolism: Hope, positivity, enthusiasm, brightness. Examples: Linda as a child (positive personality).
6. WHITE — Symbolism: Purity, innocence, hygiene, cleanliness. Examples: Edward's white shirt (privilege), Narrator's shirt.
7. GREY — Symbolism: Dullness, conformity, poverty, loss of hope. Examples: Mickey's shorts (poverty), Mrs Lyons' suit (formality).

VISUAL FORMAT:
- Vertical list with LARGE colour swatches on the left (actual coloured rectangles)
- Each row: colour swatch → colour name → symbolism text → costume example from the play
- Use small costume icons or fabric/thread illustrations to make it theatrical
- The colour swatches should be the ACTUAL colours (red, blue, pink, black, yellow, white, grey)
- Purple accents only for the frame/headers, NOT for the colour swatches themselves
- Clean table-like layout but with visual flair (not a boring spreadsheet)

DATA RULES:
- Include ALL 7 colours exactly as listed with their symbolism AND examples
- Labels must appear ONLY once per row
""" + COMMON_RULES,

    "diagram_staging_types": COMMON_STYLE + """
THIS DIAGRAM: Top-down comparison of 4 key staging types used in Drama GCSE, with audience and stage positions clearly shown.

4 STAGING TYPES (each shown as a bird's-eye view floor plan):

1. PROSCENIUM ARCH — Stage at one end, audience facing from one side. Many entrances/exits. Fly loft for set. Clear US/DS/SL/SR blocking. Advantage: set can be 2D (only seen from one angle). Disadvantage: audience may feel distant.

2. THRUST — Stage extends into audience, audience on THREE sides. Set only at back. Great for large-scale performances. Actors respond to 3 sides. More complex lighting.

3. TRAVERSE — Long stage in centre, audience on TWO sides (like a catwalk). Limited set and exits. Actors must keep moving. Audience can see each other.

4. IN THE ROUND — Circular/square stage in centre, audience on ALL four sides. Intimate environment. No large set pieces. Must move constantly. No wings.

VISUAL FORMAT:
- 4 equal panels in a 2x2 grid
- Each panel shows a bird's-eye view with the STAGE area in light purple and AUDIENCE seats as small dots/circles around the appropriate sides
- Small theatre icons (curtains, spotlights, chairs)
- Label: stage area, audience positions, entrances/exits
- Add a small note about suitability for Blood Brothers (Proscenium = MOST suitable, In the Round = NOT suitable due to large set needs)

DATA RULES:
- Include ALL 4 staging types with their advantages/disadvantages
- Audience positions must correctly show: 1 side, 3 sides, 2 sides, all sides
""" + COMMON_RULES,

    "diagram_lighting_sound": COMMON_STYLE + """
THIS DIAGRAM: Split diagram showing Blood Brothers lighting techniques (left) and sound techniques (right), with specific examples from the play.

LEFT PANEL — LIGHTING (creates atmosphere):
1. Wash/Flood — Warm straw wash when Mickey & Edward first meet = happiness
2. Spotlight — White spotlight on Mrs Johnstone in final scene = isolation, truth revealed
3. Gobo — Prison bar gobo with white light = Mickey trapped in prison & mental anguish
4. Crossfade — Straw to steel wash in battle scene = joy turning to misery
5. Strobe — Pulsating blue/red in final scene = police arrival, foreshadow danger

RIGHT PANEL — SOUND (creates mood & atmosphere):
1. Live Orchestra — Expected for a musical, allows incidental/transitional music
2. Sound Effects — Singular magpie cackle when Mrs J swears on bible = foreshadow sorrow
3. Diegetic — Cow mooing at end of Act 1 = arrived in the country
4. Underscoring — Beatles song while Mrs J cleans = fun nature, location & time period
5. Non-diegetic — Heartbeat when Mrs J swears on bible = stressful decision

KEY CONCEPT AT BOTTOM:
"MOOD = created by what actors do | ATMOSPHERE = created by design elements (lighting, sound, set)"

VISUAL FORMAT:
- Two-panel layout: LIGHTING left, SOUND right
- Use small icons: spotlight beam, musical notes, speaker, gobo pattern, prison bars
- Each technique has a coloured box with the example from the play
- Lighting panel uses glow effects (warm yellow, cool blue, stark white)
- Sound panel uses wave/frequency icons
- Bottom bar with the Mood vs Atmosphere distinction prominently displayed

DATA RULES:
- Include ALL 5 lighting techniques and ALL 5 sound techniques exactly as listed
- Labels ONLY once per technique
""" + COMMON_RULES,

    "diagram_performance_skills": COMMON_STYLE + """
THIS DIAGRAM: Two-panel reference showing Voice Skills (left) and Physicality Skills (right) for Blood Brothers GCSE Drama.

LEFT PANEL — VOICE SKILLS (8 skills with CTPAPVE mnemonic):
1. C — Clarity: Clear diction so audience understands every word
2. T — Tone: Emotional quality (angry, sad, sarcastic, warm)
3. P — Pace: Speed of delivery (fast = panic, slow = sadness)
4. A — Accent: RP = wealth/education, Scouse = working class
5. P — Pitch: High = excitement/fear, Low = authority/threat
6. V — Volume: Loud = anger/power, Quiet = intimacy/secrecy
7. E — Emphasis: Stress key words to change meaning
8. Pause: Silence before/after key lines for impact

RIGHT PANEL — PHYSICALITY SKILLS (9 skills):
1. Eye Contact: Direct = confidence, Averted = guilt/fear
2. Facial Expression: Shows emotion (shock, joy, despair)
3. Posture: Upright = confidence, Slumped = defeat
4. Muscle Tension: Tense = anger/stress, Relaxed = calm
5. Gesture: Pointing = accusation, Open palms = sincerity
6. Body Language: Open = welcoming, Closed = defensive
7. Gait: Stride = confidence, Shuffle = depression
8. Levels: High = power, Low = powerlessness
9. Proximity: Close = intimacy/threat, Far = isolation

VISUAL FORMAT:
- Two columns: VOICE (left) with mouth/speech icons, PHYSICALITY (right) with body/movement icons
- Each skill has a letter/abbreviation in a purple circle, then the skill name and description
- Use small illustrative icons for each skill (an ear for clarity, a metronome for pace, a pointing hand for gesture, eyes for eye contact, etc.)
- Clean list format with clear spacing
- The CTPAPVE mnemonic letters should be prominent for the voice column

DATA RULES:
- Include ALL 8 voice skills and ALL 9 physicality skills exactly as listed
- Descriptions should include the contrast pairs (e.g. "Direct = confidence, Averted = guilt/fear")
""" + COMMON_RULES,

    "diagram_key_scenes": COMMON_STYLE + """
THIS DIAGRAM: Timeline of 10 key scenes from Blood Brothers with dramatic convention labels.

10 KEY SCENES IN ORDER:
1. Mrs Johnstone agrees to give away her baby — Convention: MARKING THE MOMENT
2. Mickey and Edward become friends — Convention: DRAMATIC IRONY
3. The other children pick on Mickey — Convention: DUOLOGUE
4. Mrs Johnstone gives Edward the locket — Convention: FORESHADOWING
5. Mrs Lyons tries to stab Mrs Johnstone — Convention: CLIMAX / MARKING THE MOMENT
6. Mickey asks Linda out — Convention: CROSS-CUTTING
7. Mr Lyons makes his staff redundant — Convention: SOCIAL CONTEXT
8. Mickey in prison — Convention: MONOLOGUE
9. Linda hides Mickey's antidepressants — Convention: CROSS-CUTTING
10. The final scene: both twins die — Convention: DRAMATIC IRONY / TRAGEDY

VISUAL FORMAT:
- Flowing timeline with 10 scene boxes (5 on top row, 5 on bottom row)
- Arrows connecting scenes in sequence with a curved connection from scene 5 to scene 6
- Each scene box in purple with the scene number, brief description
- Below each box: the dramatic convention in a separate label/tag
- Use small theatre icons: a bible (scene 1), handshake (scene 2), locket (scene 4), knife (scene 5), gun (scene 10)
- Darker purple for the most dramatic moments (scenes 1, 5, 10)

DATA RULES:
- Include ALL 10 scenes and ALL conventions exactly as listed
- Labels ONLY once per scene
- Maintain the correct order (1-10)
""" + COMMON_RULES,

    "diagram_freedom_riders_timeline": COMMON_STYLE + """
THIS DIAGRAM: Timeline of the Freedom Riders movement (1960-1964) for the Rise Up study text.

8 KEY EVENTS:
1. 1960 — Student sit-ins begin at lunch counters across the Southern states
2. Feb 1961 — CORE and SNCC organise the first Freedom Rides
3. May 1961 — First bus attacked in Anniston, Alabama (firebombed by white mob)
4. May 1961 — Riders beaten in Birmingham by white mob
5. May 1961 — Diane Nash organises second wave of Freedom Riders from Nashville
6. May 1961 — Riders arrested in Jackson, Mississippi by Bull Connor
7. Sep 1961 — ICC ruling bans segregation on interstate travel
8. 1964 — Civil Rights Act passed — outlaws discrimination

VISUAL FORMAT:
- Horizontal timeline with bus/road journey metaphor (the Freedom Riders travelled by bus)
- Use a road or bus route as the timeline spine
- Events alternate above and below the timeline
- VIOLENT events (3, 4) in RED to show danger
- POSITIVE events (7, 8) in brighter purple to show progress
- Small icons: a bus, flames, handcuffs, a gavel, a phone (for Diane Nash)
- The bus journey visual reinforces that these were literally bus rides across America

DATA RULES:
- Include ALL 8 events exactly as listed with correct dates
- Maintain chronological order (left to right)
- Labels ONLY once per event
""" + COMMON_RULES,

    "diagram_white_shoppers_layout": COMMON_STYLE + """
THIS DIAGRAM: Top-down stage layout diagram for the White Shoppers scene in Rise Up.

STAGE LAYOUT:
- THREE STEEL FLATS at the back of the stage (upstage), representing the Greyhound bus. Silver/grey colour. Props hanging on them.
- LWG (Little White Girl, 12 years old) sits on a TALL STOOL at CENTRE STAGE — the focal point of the scene
- WHITE FEMALE SHOPPERS (2 actors: Em and Dayz) positioned UPSTAGE LEFT, wearing white gloves, standing close together with linked arms
- LWG's MUM positioned UPSTAGE RIGHT
- AUDIENCE at the bottom (downstage)
- Stools: tall stool CS (LWG sits on it), other stools positioned around space

LIGHTING:
- White and blue wash at start (blue from steel flat reflections = isolation)
- White light increases on LWG = innocence and purity
- Bright white when LWG introduced = her purity

KEY STAGING DETAILS:
- White shoppers "step in" (reduce proxemics) on the name of the store
- Shoppers speak in unison "we do, we do" — choral work
- LWG's mum uses derogatory flicking gesture
- Abstract performance style: all performers face out (towards audience)

VISUAL FORMAT:
- Bird's-eye view stage layout with labelled positions
- Colour-coded character circles with names
- Arrows showing movement (shoppers stepping in)
- Steel flats clearly shown at the back
- Audience area at the bottom
- Small icons: white gloves, stool, bus silhouette on flats

DATA RULES:
- Include ALL character positions exactly as described
- Label positions using stage directions (USL, USR, CS, etc.)
""" + COMMON_RULES,

    "diagram_cj_reminder_layout": COMMON_STYLE + """
THIS DIAGRAM: Top-down stage layout for the CJ Reminder scene in Rise Up, showing the diamond formation and circling technique.

STAGE LAYOUT:
- THREE STEEL FLATS at the back: USR has Confederate flag, CS has Ku Klux Klan hat and cowboy hat, USL has LWG's headband
- FOUR STOOLS: small stool USR, two tall stools USC, small stool USL

DIAMOND FORMATION (initial positions):
- Ty (as Jim, a white Freedom Rider) — USL, standing on small stool (HIGHEST LEVEL = power status, reflecting white supremacy of the era)
- Em (as Thora) — USC (upper centre)
- Dayz (as Merna) — CS (centre stage)
- CJ (as Hank) — DSR (downstage right, lowest level)
The four actors form a DIAMOND SHAPE with Ty (Jim) at the top and CJ (Hank) at the bottom — the large proxemics between them highlight the power disparity/inequality.

CIRCLING TECHNIQUE:
- When CJ asks "like what?", he steps forward to the same level as Em and Dayz
- Ty steps down from his stool
- Em, Ty, and Dayz quickly CIRCLE CJ
- CJ is forced USC, almost pinned against the steel flat CS
- This circling reduces proxemics and creates intimidation
- Sound collage builds to a climax during the circling

LIGHTING: White wash at 100% intensity throughout (actors are in role as British actors, not historical characters)

VISUAL FORMAT:
- Bird's-eye view stage layout
- Phase 1: diamond formation with dotted diamond shape connecting the 4 characters
- Highlight the circling technique with curved arrows around CJ
- Steel flats clearly labelled at the back with their props
- Stools marked with height indicators (tall vs small)
- Colour: CJ in RED (under threat), others in PURPLE (circling/intimidating)

DATA RULES:
- Include ALL character positions and stage directions
- Show the diamond formation clearly
- Label the circling technique
""" + COMMON_RULES,

    "diagram_seas_paragraph": COMMON_STYLE + """
THIS DIAGRAM: SEAS paragraph structure diagram for Section B essay writing (Rise Up evaluation).

SEAS stands for:
S — STATEMENT: Make a clear point about what you observed. E.g. "The actor playing CJ used closed body language when the other actors circled him."
E — EVIDENCE / EXAMPLE: Give a specific example from the performance. E.g. "He held his hands in front of his chest as if to create a barrier from the other actors."
A — ANALYSIS: Explain WHY the technique was effective and what it communicated to the audience. E.g. "This highlighted how intimidated his character felt at this point in the play."
S — SUGGEST DEVELOPMENT: How could this moment be improved or developed? E.g. "To develop further, the actor could use a trembling voice to reinforce his fear to the audience."

KEY INFORMATION:
- Section B is about Rise Up (live theatre evaluation)
- Worth 30 marks total (20 for answering the question, 10 for drama terminology)
- 30 minutes to answer
- Must state where and when you watched the play
- Use this SEAS structure for EVERY paragraph

VISUAL FORMAT:
- Vertical flowchart with 4 large steps flowing downward
- Each step has: a large letter (S, E, A, S) in a circle, the step name, and an example quote
- Arrows connecting each step to the next
- Use drama-themed icons: a speech bubble (statement), a magnifying glass (evidence), a brain (analysis), a lightbulb (development)
- The two S steps should be visually distinct (dark purple for Statement, medium purple for Suggest Development)
- Bottom callout: "Use SEAS for EVERY paragraph in Section B — 30 marks (20 content + 10 terminology)"

DATA RULES:
- Include ALL 4 steps with their example quotes
- The structure must flow S → E → A → S (top to bottom)
""" + COMMON_RULES,
}


# ===========================================================================
# MAIN EXECUTION
# ===========================================================================

def main():
    print("=" * 70)
    print("DRAMA GCSE DIAGRAM PIPELINE — 12 Diagrams")
    print("=" * 70)

    # Define all 12 diagrams
    diagrams = [
        # Blood Brothers (lessons 1-8) — output to blood-brothers/
        ("L01", "diagram_cyclical_structure", BB_DIR, draw_lesson_01),
        ("L02", "diagram_character_relationships", BB_DIR, draw_lesson_02),
        ("L03", "diagram_themes_context", BB_DIR, draw_lesson_03),
        ("L04", "diagram_colour_symbolism", BB_DIR, draw_lesson_04),
        ("L05", "diagram_staging_types", BB_DIR, draw_lesson_05),
        ("L06", "diagram_lighting_sound", BB_DIR, draw_lesson_06),
        ("L07", "diagram_performance_skills", BB_DIR, draw_lesson_07),
        ("L08", "diagram_key_scenes", BB_DIR, draw_lesson_08),
        # Rise Up (lessons 9-12) — output to rise-up/
        ("L09", "diagram_freedom_riders_timeline", RU_DIR, draw_lesson_09),
        ("L10", "diagram_white_shoppers_layout", RU_DIR, draw_lesson_10),
        ("L11", "diagram_cj_reminder_layout", RU_DIR, draw_lesson_11),
        ("L12", "diagram_seas_paragraph", RU_DIR, draw_lesson_12),
    ]

    # Step 1: Generate all matplotlib baselines
    print("\n--- STEP 1: Generating matplotlib baselines ---\n")
    matplotlib_paths = {}
    for lesson, name, out_dir, draw_func in diagrams:
        print(f"[{lesson}] {name}")
        path = draw_func(out_dir)
        matplotlib_paths[name] = path

    # Step 2: Send to Gemini for pictorial transformation
    print("\n--- STEP 2: Sending to Gemini for pictorial infographics ---\n")
    success_count = 0
    fail_count = 0

    for i, (lesson, name, out_dir, _) in enumerate(diagrams):
        print(f"\n[{lesson}] Processing {name}...")

        matplotlib_path = matplotlib_paths[name]
        final_path = os.path.join(out_dir, f"{name}.jpg")
        prompt = GEMINI_PROMPTS[name]

        ok = call_gemini(matplotlib_path, final_path, prompt)
        if ok:
            success_count += 1
            print(f"  SUCCESS: {os.path.basename(final_path)}")
        else:
            fail_count += 1
            # Copy matplotlib as fallback
            shutil.copy2(matplotlib_path, final_path)
            print(f"  FALLBACK: Using matplotlib version for {name}")

        # Rate limit: 5-second delay between Gemini calls
        if i < len(diagrams) - 1:
            print("  Waiting 5 seconds (rate limit)...")
            time.sleep(5)

    # Summary
    print("\n" + "=" * 70)
    print(f"COMPLETE: {success_count} Gemini successes, {fail_count} failures")
    print("=" * 70)

    print("\nMatplotlib backups:")
    for name, path in matplotlib_paths.items():
        print(f"  {path}")

    print("\nFinal diagrams:")
    for lesson, name, out_dir, _ in diagrams:
        final = os.path.join(out_dir, f"{name}.jpg")
        exists = "EXISTS" if os.path.exists(final) else "MISSING"
        print(f"  [{lesson}] {final} — {exists}")


if __name__ == "__main__":
    main()
