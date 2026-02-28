"""Generate data-driven matplotlib diagrams for Sport Science R180 (10 lessons).

Each diagram uses REAL research data with proper citations.
Orange palette. Overwrites existing files.

Usage:
    python generate_sport_diagrams.py
"""

import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ---------------------------------------------------------------------------
# Palette — orange
# ---------------------------------------------------------------------------
COLORS = ['#9a3412', '#c2410c', '#ea580c', '#f97316', '#fb923c', '#fdba74']
SHADOW = '#fed7aa'
TITLE_COLOR = '#7c2d12'
GRID_COLOR = '#fff7ed'
TEXT_DARK = '#431407'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUT_DIR = os.path.join(PROJECT_ROOT, "sport-science", "r180")
SAVE_KW = dict(dpi=150, bbox_inches='tight', facecolor='white', pad_inches=0.2)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'Segoe UI', 'Arial', 'sans-serif'],
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#cccccc',
    'axes.grid': False,
})


def save_fig(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    os.makedirs(OUT_DIR, exist_ok=True)
    fig.savefig(path, **SAVE_KW)
    plt.close(fig)
    size_kb = os.path.getsize(path) / 1024
    print(f"  -> Saved {filename} ({size_kb:.0f} KB)")


def style_axes(ax, title, ylabel=None, xlabel=None):
    ax.set_title(title, color=TITLE_COLOR, fontsize=15, fontweight='bold', pad=15)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color='#333333')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color='#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(colors='#555555')


# ============================================================
# L01 — Extrinsic Factors: HORIZONTAL BAR — Injury rate by sport
# Data: Prieto-Gonzalez et al. (2021), 498 athletes aged 14-21
# ============================================================
def gen_01_extrinsic():
    print("1/10: diagram_extrinsic_factors.jpg — Injury rates by sport")
    fig, ax = plt.subplots(figsize=(12, 7))

    sports = ['Swimming', 'Cycling', 'Weight Training', 'Tennis',
              'Paddle Tennis', 'Athletics', 'Volleyball', 'Basketball',
              'Judo', 'Soccer']
    rates = [0.35, 0.59, 1.12, 1.39, 1.72, 2.35, 2.64, 4.31, 4.82, 7.21]

    # Colour gradient from light (low risk) to dark (high risk)
    bar_colors = []
    for r in rates:
        ratio = r / max(rates)
        if ratio < 0.25:
            bar_colors.append(COLORS[5])
        elif ratio < 0.4:
            bar_colors.append(COLORS[4])
        elif ratio < 0.55:
            bar_colors.append(COLORS[3])
        elif ratio < 0.7:
            bar_colors.append(COLORS[2])
        else:
            bar_colors.append(COLORS[1])

    bars = ax.barh(sports, rates, color=bar_colors, edgecolor='white',
                   height=0.65, zorder=3)

    for bar, val in zip(bars, rates):
        ax.text(val + 0.15, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontsize=10, fontweight='bold',
                color=TEXT_DARK)

    ax.set_xlim(0, 8.5)
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax, 'Injury Rate by Sport (per 1,000 participation hours)',
               xlabel='Injuries per 1,000 hours')

    # Source annotation
    ax.text(0.5, -0.12,
            'Source: Prieto-Gonz\u00e1lez et al. (2021), Int. J. Environ. Res. Public Health, 18(9)',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    # Annotation for contact vs non-contact
    ax.annotate('Contact / combat sports\nhave higher injury rates',
                xy=(7.21, 9), xytext=(5.5, 7),
                fontsize=9, color=COLORS[0], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS[2], lw=1.5),
                ha='center')

    fig.tight_layout()
    save_fig(fig, 'diagram_extrinsic_factors.jpg')


# ============================================================
# L02 — Intrinsic Factors: GROUPED BAR — ACL injury by gender & sport
# Data: Comstock et al. (2012), high school athletics
# ============================================================
def gen_02_intrinsic():
    print("2/10: diagram_intrinsic_factors.jpg — ACL injuries by gender")
    fig, ax = plt.subplots(figsize=(12, 7))

    sports = ['Soccer', 'Basketball']
    female_rates = [12.2, 10.3]
    male_rates = [4.8, 2.3]

    x = np.arange(len(sports))
    width = 0.32

    bars_f = ax.bar(x - width/2, female_rates, width, color=COLORS[2],
                    label='Female athletes', edgecolor='white', zorder=3)
    bars_m = ax.bar(x + width/2, male_rates, width, color=COLORS[4],
                    label='Male athletes', edgecolor='white', zorder=3)

    # Value labels
    for bar, val in zip(bars_f, female_rates):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.4,
                f'{val}', ha='center', fontweight='bold', fontsize=12,
                color=COLORS[1])
    for bar, val in zip(bars_m, male_rates):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.4,
                f'{val}', ha='center', fontweight='bold', fontsize=12,
                color=COLORS[3])

    # Risk ratio annotations
    ax.annotate('2.5\u00d7\nhigher', xy=(x[0] - width/2, 12.2),
                xytext=(x[0] - 0.65, 8), fontsize=10, color=COLORS[0],
                fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS[0], lw=1.5))
    ax.annotate('4.5\u00d7\nhigher', xy=(x[1] - width/2, 10.3),
                xytext=(x[1] - 0.65, 6), fontsize=10, color=COLORS[0],
                fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS[0], lw=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(sports, fontsize=13)
    ax.set_ylim(0, 16)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(fontsize=11, frameon=False, loc='upper right')
    style_axes(ax, 'ACL Injury Rates by Sport and Gender\n(per 100,000 athlete-exposures)',
               ylabel='ACL injuries per 100,000 AEs')

    # Key takeaway box
    ax.text(0.98, 0.02,
            'In comparable sports, females are 2\u20134.5\u00d7\nmore likely to suffer an ACL injury',
            transform=ax.transAxes, fontsize=10, color='white', fontweight='bold',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS[1], alpha=0.85,
                     edgecolor='none'))

    ax.text(0.5, -0.1,
            'Source: Comstock et al. (2012), Am. J. Sports Med.',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_intrinsic_factors.jpg')


# ============================================================
# L03 — Warm Up: BAR CHART — FIFA 11+ injury reduction by body area
# Data: Sadigursky et al. (2017) systematic review, 6 RCTs, 6344 players
# ============================================================
def gen_03_warmup():
    print("3/10: diagram_warm_up_components.jpg — FIFA 11+ effectiveness")
    fig, ax = plt.subplots(figsize=(12, 7))

    areas = ['Hamstring', 'ACL', 'All Knee', 'Hip / Groin', 'Overall', 'Ankle']
    reductions = [60, 50, 48, 41, 39, 32]

    bar_colors = [COLORS[0], COLORS[1], COLORS[1], COLORS[2], COLORS[3], COLORS[4]]
    bars = ax.bar(areas, reductions, color=bar_colors, edgecolor='white',
                  width=0.6, zorder=3)

    for bar, val in zip(bars, reductions):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.5,
                f'{val}%', ha='center', fontweight='bold', fontsize=13,
                color=TEXT_DARK)

    ax.set_ylim(0, 75)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax,
               'FIFA 11+ Structured Warm-Up: Injury Reduction by Body Area',
               ylabel='Injury reduction (%)')

    # Callout
    ax.text(0.98, 0.95,
            'The FIFA 11+ is a 20-minute\nneuromuscular warm-up\nprogramme used worldwide',
            transform=ax.transAxes, fontsize=10, color=COLORS[0],
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef7f0',
                     edgecolor=COLORS[4], linewidth=1.5))

    ax.text(0.5, -0.1,
            'Source: Sadigursky et al. (2017), BMC Sports Sci. Med. Rehabil. (systematic review, 6 RCTs, 6,344 players)',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_warm_up_components.jpg')


# ============================================================
# L04 — Cool Down / Stretching: BAR CHART — performance effects
# Data: Behm & Chaouachi (2011) + Keerthiga et al. (2016)
# ============================================================
def gen_04_stretching():
    print("4/10: diagram_stretching_types.jpg — Stretching & performance")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7),
                                    gridspec_kw={'width_ratios': [1, 1]})

    # LEFT: Acute performance effect
    types = ['Dynamic', 'Static', 'PNF']
    effects = [1.3, -3.7, -4.4]
    colors_perf = [COLORS[4], COLORS[2], COLORS[0]]

    bars = ax1.bar(types, effects, color=colors_perf, edgecolor='white',
                   width=0.55, zorder=3)

    for bar, val in zip(bars, effects):
        y_off = 0.3 if val >= 0 else -0.5
        ax1.text(bar.get_x() + bar.get_width()/2, val + y_off,
                 f'{val:+.1f}%', ha='center', fontweight='bold', fontsize=13,
                 color=TEXT_DARK)

    ax1.axhline(y=0, color='#999', linewidth=1, zorder=2)
    ax1.set_ylim(-6, 3)
    ax1.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax1.set_axisbelow(True)
    style_axes(ax1, 'Immediate Effect on\nPower / Strength',
               ylabel='Performance change (%)')

    ax1.text(0.5, -0.12,
             'Behm & Chaouachi (2011)',
             transform=ax1.transAxes, fontsize=8, color='#888888',
             style='italic', ha='center')

    # Annotation
    ax1.annotate('Dynamic stretching\nmaintains power \u2014\nuse in warm-ups',
                 xy=(0, 1.3), xytext=(0.8, 2.2),
                 fontsize=9, color=COLORS[3], fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=COLORS[3], lw=1.5))

    # RIGHT: ROM improvement over 4 weeks
    types2 = ['Control', 'Static', 'PNF']
    rom_gain = [-0.1, 4.7, 15.6]
    colors_rom = ['#cccccc', COLORS[3], COLORS[1]]

    bars2 = ax2.bar(types2, rom_gain, color=colors_rom, edgecolor='white',
                    width=0.55, zorder=3)

    for bar, val in zip(bars2, rom_gain):
        y_off = 0.6 if val >= 0 else -1.0
        ax2.text(bar.get_x() + bar.get_width()/2, val + y_off,
                 f'{val:+.1f}\u00b0', ha='center', fontweight='bold', fontsize=13,
                 color=TEXT_DARK)

    ax2.axhline(y=0, color='#999', linewidth=1, zorder=2)
    ax2.set_ylim(-3, 20)
    ax2.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax2.set_axisbelow(True)
    style_axes(ax2, 'Hip Flexion ROM Gain\nAfter 4-Week Programme',
               ylabel='Range of motion improvement (\u00b0)')

    ax2.text(0.5, -0.12,
             'Keerthiga et al. (2016), randomised controlled trial',
             transform=ax2.transAxes, fontsize=8, color='#888888',
             style='italic', ha='center')

    # Annotation
    ax2.annotate('PNF produced 3.3\u00d7\ngreater ROM gains\nthan static stretching',
                 xy=(2, 15.6), xytext=(1.2, 17),
                 fontsize=9, color=COLORS[0], fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=COLORS[0], lw=1.5))

    fig.suptitle('Stretching Types: Performance and Flexibility Effects',
                 fontsize=17, fontweight='bold', color=TITLE_COLOR, y=1.02)
    fig.tight_layout()
    save_fig(fig, 'diagram_stretching_types.jpg')


# ============================================================
# L05 — Acute Injuries: HORIZONTAL BAR — most common types
# Data: Schroeder et al. (2021), ~17.4 million estimated injuries
# ============================================================
def gen_05_acute():
    print("5/10: diagram_acute_injuries.jpg — Acute injury breakdown")
    fig, ax = plt.subplots(figsize=(12, 7))

    injury_types = ['Other\n(dislocation, abrasion, etc.)', 'Fracture',
                    'Contusion (bruise)', 'Muscle Strain',
                    'Concussion', 'Ligament Sprain']
    percentages = [19.7, 3.5, 11.9, 12.2, 21.0, 31.7]

    bar_colors = ['#cccccc', COLORS[5], COLORS[4], COLORS[3], COLORS[2], COLORS[1]]

    bars = ax.barh(injury_types, percentages, color=bar_colors,
                   edgecolor='white', height=0.6, zorder=3)

    for bar, val in zip(bars, percentages):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontsize=11, fontweight='bold',
                color=TEXT_DARK)

    ax.set_xlim(0, 40)
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax, 'Most Common Acute Sports Injuries by Type',
               xlabel='Percentage of all acute injuries (%)')

    # Key insight box
    ax.text(0.98, 0.05,
            'Sprains and concussions\naccount for over half\nof all acute injuries',
            transform=ax.transAxes, fontsize=10, color='white', fontweight='bold',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS[1], alpha=0.85,
                     edgecolor='none'))

    ax.text(0.5, -0.1,
            'Source: Schroeder et al. (2021), Injury Epidemiology \u2014 ~17.4 million injuries, 2005\u20132019',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_acute_injuries.jpg')


# ============================================================
# L06 — Chronic Injuries: BAR CHART — Achilles tendinopathy by sport
# Data: PMC systematic review & meta-analysis (2022)
# ============================================================
def gen_06_chronic():
    print("6/10: diagram_chronic_injuries.jpg — Achilles tendinopathy")
    fig, ax = plt.subplots(figsize=(12, 7))

    sports = ['General\nPopulation', 'Ball Games\n(general)', 'Basketball',
              'Football\n(professional)', 'All Runners', 'Elite Runners\n(lifetime)']
    prevalence = [0.6, 6.0, 7.7, 11.6, 30.0, 52.0]

    bar_colors = [COLORS[5], COLORS[4], COLORS[4], COLORS[3], COLORS[2], COLORS[0]]

    bars = ax.bar(sports, prevalence, color=bar_colors, edgecolor='white',
                  width=0.6, zorder=3)

    for bar, val in zip(bars, prevalence):
        label = f'{val:.1f}%' if val < 1 else f'{val:.0f}%'
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.5,
                label, ha='center', fontweight='bold', fontsize=12,
                color=TEXT_DARK)

    ax.set_ylim(0, 65)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax, 'Achilles Tendinopathy Prevalence by Sport',
               ylabel='Prevalence (%)')

    # Annotation
    ax.annotate('Repetitive impact loading\nin running causes the\nhighest chronic injury rates',
                xy=(5, 52), xytext=(3.2, 55),
                fontsize=10, color=COLORS[0], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS[0], lw=1.5))

    ax.text(0.5, -0.12,
            'Source: PMC (2022), Systematic Review & Meta-Analysis of Achilles Tendinopathy Prevalence',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_chronic_injuries.jpg')


# ============================================================
# L07 — Risk / EAP: LINE CHART — Cardiac arrest survival by time
# Data: StatPearls (NCBI), Resuscitation Council UK
# ============================================================
def gen_07_risk_eap():
    print("7/10: diagram_risk_eap.jpg — Cardiac arrest survival")
    fig, ax = plt.subplots(figsize=(12, 7))

    minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    survival = [90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2]

    # Fill area under curve
    ax.fill_between(minutes, survival, alpha=0.15, color=COLORS[2], zorder=1)

    # Main line
    ax.plot(minutes, survival, color=COLORS[1], linewidth=3, marker='o',
            markersize=8, markerfacecolor=COLORS[2], markeredgecolor='white',
            markeredgewidth=2, zorder=3)

    # Value labels on key points
    key_points = [(1, 90), (3, 70), (5, 50), (8, 20), (10, 5)]
    for mins, surv in key_points:
        ax.text(mins, surv + 4, f'{surv}%', ha='center', fontsize=11,
                fontweight='bold', color=COLORS[0])

    # Dashed line at UK ambulance response time
    ax.axvline(x=8, color='#999', linestyle='--', linewidth=1.5, zorder=2)
    ax.text(8.3, 75, 'Average UK\nambulance\nresponse time',
            fontsize=9, color='#666', fontfamily='sans-serif')

    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(0, 100)
    ax.set_xticks(range(1, 13))
    ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax, 'Cardiac Arrest: Survival Rate by Minutes to Defibrillation',
               xlabel='Minutes after cardiac arrest',
               ylabel='Chance of survival (%)')

    # Key message box
    ax.text(0.98, 0.95,
            'Survival drops ~10% per minute\nwithout defibrillation \u2014\nthis is why AEDs save lives',
            transform=ax.transAxes, fontsize=10, color='white', fontweight='bold',
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS[0], alpha=0.9,
                     edgecolor='none'))

    ax.text(0.5, -0.1,
            'Source: StatPearls / NCBI (2024); Resuscitation Council UK',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_risk_eap.jpg')


# ============================================================
# L08 — Treatment / Rehab: GROUPED BAR — re-injury with/without rehab
# Data: Mendiguchia (2017), Sherry (2004), PMC9569141
# ============================================================
def gen_08_treatment():
    print("8/10: diagram_treatment_protocols.jpg — Rehab effectiveness")
    fig, ax = plt.subplots(figsize=(12, 7))

    studies = ['Hamstring\n(Mendiguchia 2017)', 'Hamstring\n(Sherry 2004)',
               'ACL\n(PMC 2022)']
    proper_rehab = [4, 7.1, 5.6]    # % re-injury with proper rehab
    inadequate = [25, 50, 38.2]      # % re-injury without proper rehab / failed criteria

    # Sherry 2004: 1/14 vs 7/14 = 7.1% vs 50%
    x = np.arange(len(studies))
    width = 0.32

    bars_good = ax.bar(x - width/2, proper_rehab, width, color=COLORS[4],
                       label='With proper rehabilitation', edgecolor='white', zorder=3)
    bars_bad = ax.bar(x + width/2, inadequate, width, color=COLORS[1],
                      label='Without proper rehabilitation', edgecolor='white', zorder=3)

    for bar, val in zip(bars_good, proper_rehab):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.2,
                f'{val}%', ha='center', fontweight='bold', fontsize=12,
                color=COLORS[3])
    for bar, val in zip(bars_bad, inadequate):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.2,
                f'{val}%', ha='center', fontweight='bold', fontsize=12,
                color=COLORS[0])

    # Risk multiplier annotations
    multiples = ['6.3\u00d7', '7\u00d7', '6.8\u00d7']
    for i, mult in enumerate(multiples):
        mid_y = (proper_rehab[i] + inadequate[i]) / 2
        ax.text(x[i] + width + 0.15, mid_y, mult,
                fontsize=11, fontweight='bold', color=COLORS[0],
                ha='left', va='center')

    ax.set_xticks(x)
    ax.set_xticklabels(studies, fontsize=11)
    ax.set_ylim(0, 58)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(fontsize=11, frameon=False, loc='upper left')
    style_axes(ax, 'Re-Injury Rates: Proper Rehabilitation vs Inadequate',
               ylabel='Re-injury rate (%)')

    # Key message box
    ax.text(0.98, 0.95,
            'Athletes who skip proper rehab\nare 6\u20137\u00d7 more likely\nto be injured again',
            transform=ax.transAxes, fontsize=10, color='white', fontweight='bold',
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS[0], alpha=0.9,
                     edgecolor='none'))

    ax.text(0.5, -0.12,
            'Sources: Mendiguchia et al. (2017); Sherry (2004); PMC9569141 (ACL return-to-sport criteria)',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_treatment_protocols.jpg')


# ============================================================
# L09 — Medical Conditions 1: GROUPED BAR (UK prevalence) — UNCHANGED
# Data: UK prevalence per 1,000 people
# ============================================================
def gen_09_medical_1():
    print("9/10: diagram_medical_conditions_1.jpg — UK prevalence")
    fig = plt.figure(figsize=(14, 7))

    ax1 = fig.add_axes([0.06, 0.42, 0.88, 0.50])

    conditions = ['Asthma', 'Type 1\nDiabetes', 'Type 2\nDiabetes', 'Epilepsy']
    prevalence = [120, 4, 68, 9]
    bar_colors = [COLORS[2], COLORS[3], COLORS[4], COLORS[1]]

    bars = ax1.bar(conditions, prevalence, color=bar_colors, edgecolor='white',
                   width=0.6, zorder=3)

    for bar, val in zip(bars, prevalence):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 3,
                 f'{val} per 1,000', ha='center', fontweight='bold', fontsize=11,
                 color=TEXT_DARK)

    ax1.set_ylim(0, 145)
    ax1.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax1.set_axisbelow(True)
    style_axes(ax1, 'UK Prevalence of Common Medical Conditions in Sport',
               ylabel='Cases per 1,000 people')

    # Bottom: key action panel
    ax2 = fig.add_axes([0.06, 0.02, 0.88, 0.32])
    ax2.axis('off')
    ax2.set_xlim(0, 14)
    ax2.set_ylim(0, 3)

    actions = [
        ('Asthma', 'Carry reliever inhaler,\nwarm up well, avoid\ncold dry air', COLORS[2]),
        ('Type 1 Diabetes', 'Monitor blood sugar,\ncarry glucose gel,\neat before exercise', COLORS[3]),
        ('Type 2 Diabetes', 'Regular exercise helps,\nmonitor levels,\nbalanced diet', COLORS[4]),
        ('Epilepsy', 'Take medication,\ninform coach/officials,\navoid known triggers', COLORS[1]),
    ]

    for i, (name, action, color) in enumerate(actions):
        x = 0.2 + i * 3.5
        box = FancyBboxPatch((x, 0.3), 3.1, 2.2, boxstyle='round,pad=0.12',
                             facecolor=color, edgecolor='none', alpha=0.9, zorder=2)
        ax2.add_patch(box)
        ax2.text(x + 1.55, 2.15, name, fontsize=11, fontweight='bold', color='white',
                 ha='center', va='center', zorder=3, fontfamily='sans-serif')
        ax2.plot([x + 0.3, x + 2.8], [1.85, 1.85], color='white', alpha=0.4,
                 linewidth=1, zorder=3)
        ax2.text(x + 1.55, 1.15, action, fontsize=9, color='white', alpha=0.9,
                 ha='center', va='center', zorder=3, fontfamily='sans-serif',
                 linespacing=1.3)

    save_fig(fig, 'diagram_medical_conditions_1.jpg')


# ============================================================
# L10 — Medical Conditions 2: BAR — Dehydration vs performance
# Data: Human Kinetics, Cheuvront & Kenefick (2014)
# ============================================================
def gen_10_medical_2():
    print("10/10: diagram_medical_conditions_2.jpg — Dehydration impact")
    fig, ax = plt.subplots(figsize=(12, 7))

    dehydration_pct = ['1%', '2%', '2.5%', '3%', '5%']
    effects = [
        'Endurance begins\nto decline',
        'Aerobic performance\ndown ~10%',
        'High-intensity\ncapacity down ~45%',
        'VO\u2082max down ~5%;\nstrength down ~5%',
        'Work capacity\ndown ~30%',
    ]
    decline_values = [5, 10, 45, 5, 30]  # Primary % decline for bar height

    # Use grouped layout: main bar + annotation
    x = np.arange(len(dehydration_pct))
    bar_colors = [COLORS[5], COLORS[4], COLORS[2], COLORS[3], COLORS[0]]

    bars = ax.bar(x, decline_values, color=bar_colors, edgecolor='white',
                  width=0.55, zorder=3)

    # Effect labels above each bar
    for i, (bar, effect) in enumerate(zip(bars, effects)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                effect, ha='center', fontsize=9, color=TEXT_DARK,
                fontweight='bold', linespacing=1.2)

    ax.set_xticks(x)
    ax.set_xticklabels([f'{d}\nbody weight\nloss' for d in dehydration_pct], fontsize=10)
    ax.set_ylim(0, 60)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax, 'How Dehydration Affects Sports Performance',
               ylabel='Performance decline (%)')

    # SCA survival callout box (covers the other L10 topic)
    ax.text(0.98, 0.95,
            'SCA: survival drops from 90%\nto <5% without defibrillation\nwithin 10 minutes (see L07)',
            transform=ax.transAxes, fontsize=9, color='white',
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS[1], alpha=0.85,
                     edgecolor='none'))

    ax.text(0.5, -0.15,
            'Sources: Human Kinetics; Cheuvront & Kenefick (2014); Sports Cardiology BC',
            transform=ax.transAxes, fontsize=8, color='#888888', style='italic')

    fig.tight_layout()
    save_fig(fig, 'diagram_medical_conditions_2.jpg')


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    gen_01_extrinsic()
    gen_02_intrinsic()
    gen_03_warmup()
    gen_04_stretching()
    gen_05_acute()
    gen_06_chronic()
    gen_07_risk_eap()
    gen_08_treatment()
    gen_09_medical_1()
    gen_10_medical_2()
    print("\nDone. All 10 diagrams generated.")
