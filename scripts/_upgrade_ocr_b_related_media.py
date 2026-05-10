"""
URL specificity upgrade for separate-sciences-ocr-b related_media.
Replaces generic channel-root YouTube URLs with verified playlist/video URLs.
Also replaces spark.iop.org (403 errors) with physicsandmathstutor.com.

Run: python scripts/_upgrade_ocr_b_related_media.py
"""

import json
import glob
import copy

# ── Verified playlist URLs (oembed-confirmed) ──────────────────────────────────
COGNITO_BIO   = "https://www.youtube.com/playlist?list=PLidqqIGKox7X5UFT-expKIuR-i-BN3Q1g"
COGNITO_CHEM  = "https://www.youtube.com/playlist?list=PLidqqIGKox7WeOKVGHxcd69kKqtwrKl8W"
COGNITO_PHYS  = "https://www.youtube.com/playlist?list=PLidqqIGKox7UVC-8WC9djoeBzwxPeXph7"

CC_BIO   = "https://www.youtube.com/playlist?list=PLIRCOr8Z3UMXeVmc0xZLUPUuZ_vhIGsKy"
CC_CHEM  = "https://www.youtube.com/playlist?list=PL8dPuuaLjXtPHzzYuWy6fYEaX9mQQ8oGr"
CC_PHYS  = "https://www.youtube.com/playlist?list=PL58rKAc12lkJZ_AEYekzyKqFtiFXPD2g8"

# FSL – topic-appropriate playlists (content is >90% board-agnostic at GCSE level)
FSL_BIO_P1   = "https://www.youtube.com/playlist?list=PL9IouNCPbCxVU74eQtCcqbaQdYmwzAnlC"
FSL_CHEM_P1  = "https://www.youtube.com/playlist?list=PL9IouNCPbCxULWXCO9jt0PsuAbxYpw2_1"
FSL_PHYS_P1  = "https://www.youtube.com/playlist?list=PL9IouNCPbCxWNjJvmqwZ4vKy4VfcAhsCj"

# ── Verified specific video URLs ───────────────────────────────────────────────
# TED-Ed (oembed-confirmed)
TED_ATOM   = "https://www.youtube.com/watch?v=xazQRcSCRaY"   # The 2,400-year search for the atom
TED_ACIDS  = "https://www.youtube.com/watch?v=DupXDD87oHc"   # The strengths and weaknesses of acids and bases

# Veritasium (oembed-confirmed)
VER_CLIMATE     = "https://www.youtube.com/watch?v=OWXoRSIxyIU"  # 13 Misconceptions About Global Warming
VER_DBL_SLIT    = "https://www.youtube.com/watch?v=Iuv6hY6zsd0"  # The Original Double Slit Experiment
VER_RADIOACTIVE = "https://www.youtube.com/watch?v=TRL7o2kPqw0"  # The Most Radioactive Places on Earth
VER_STATIC      = "https://www.youtube.com/watch?v=rv4MjaF_wow"  # Sparks from Falling Water: Kelvin's Thunderstorm
VER_FLUIDS      = "https://www.youtube.com/watch?v=K-Fc08X56R0"  # 3 Perplexing Physics Problems (incl. pressure)

# SciShow (oembed-confirmed)
SCISHOW_CANCER   = "https://www.youtube.com/watch?v=7tzaWOdvGMw"  # What Makes Cancer So Hard to Cure
SCISHOW_VIRUSES  = "https://www.youtube.com/watch?v=FXqmzKwBB_w"  # Are Infectious Viruses Actually Alive?
SCISHOW_VACCINES = "https://www.youtube.com/watch?v=BSudTSzeNg0"  # What's the Deal with Pfizer's Vaccine (SciShow)
SCISHOW_NANO     = "https://www.youtube.com/watch?v=HAhKh7FXomY"  # The Giant of Nanoscience

# Kurzgesagt (oembed-confirmed) – replacing Veritasium CRISPR (no Veritasium CRISPR confirmed)
KURZ_CRISPR = "https://www.youtube.com/watch?v=jAhjPd4uNFY"  # Genetic Engineering Will Change Everything Forever

# Real Engineering (oembed-confirmed)
RE_SOLAR  = "https://www.youtube.com/watch?v=yVOnHWnLSeU"  # The Mystery Flaw of Solar Panels

# IOP Spark replacement (403 errors on all spark.iop.org URLs)
IOP_REPLACEMENT      = "https://www.physicsandmathstutor.com/"
IOP_REPLACEMENT_TITLE = "Physics & Maths Tutor: GCSE Physics Revision"

# RSC generic root replacement
RSC_REPLACEMENT      = "https://www.rsc.org/periodic-table"
RSC_REPLACEMENT_TITLE = "Royal Society of Chemistry: Interactive Periodic Table"

# ── Helper functions ──────────────────────────────────────────────────────────

def get_subject(unit_slug, lesson_slug):
    """Return 'bio', 'chem', or 'phys' for a lesson."""
    if unit_slug.startswith('biology'):
        return 'bio'
    if unit_slug.startswith('chemistry'):
        return 'chem'
    if unit_slug.startswith('physics'):
        return 'phys'
    # higher-calculations: determine from lesson topic
    chem_higher = {'concentration-and-titration', 'mole-calculations', 'yield-and-atom-economy'}
    if lesson_slug in chem_higher:
        return 'chem'
    return 'phys'

def cognito_playlist(subj):
    return {'bio': COGNITO_BIO, 'chem': COGNITO_CHEM, 'phys': COGNITO_PHYS}[subj]

def cc_playlist(subj):
    return {'bio': CC_BIO, 'chem': CC_CHEM, 'phys': CC_PHYS}[subj]

def fsl_playlist(subj):
    return {'bio': FSL_BIO_P1, 'chem': FSL_CHEM_P1, 'phys': FSL_PHYS_P1}[subj]

# ── URL mapping tables ────────────────────────────────────────────────────────

# Generic channel roots → always replaced by subject playlist
COGNITO_ROOTS = {
    'https://www.youtube.com/@cognitoedu',
    'https://www.youtube.com/@Cognitoedu',
    'https://www.youtube.com/@CognitoEdu',
}
FSL_ROOTS = {
    'https://www.youtube.com/@freesciencelessons',
    'https://www.youtube.com/@Freesciencelessons',
    'https://www.youtube.com/@FreeScienceLessons',
    'https://www.youtube.com/c/Freesciencelessons',
}
CC_ROOTS = {
    'https://www.youtube.com/@crashcourse',
    'https://www.youtube.com/@CrashCourse',
    'https://www.youtube.com/user/crashcourse',
}
TED_ROOTS = {
    'https://www.youtube.com/c/TEDEd',
    'https://www.youtube.com/@TED-Ed',
    'https://www.youtube.com/@TEDEd',
    'https://www.youtube.com/c/teded',
}

# Per-lesson overrides: lesson_slug → list of (title_substring, new_url, new_title)
# title_substring is matched case-insensitively against the item title
LESSON_OVERRIDES = {
    'acids-alkalis-and-useful-products': [
        ('ted-ed', TED_ACIDS, 'TED-Ed: The Strengths and Weaknesses of Acids and Bases'),
    ],
    'atomic-models-dalton-to-bohr': [
        ('ted-ed', TED_ATOM, 'TED-Ed: The 2,400-Year Search for the Atom'),
    ],
    'climate-change-evidence-and-response': [
        ('veritasium', VER_CLIMATE, 'Veritasium: 13 Misconceptions About Global Warming'),
    ],
    'climate-models-and-earths-energy-balance': [
        ('veritasium', VER_CLIMATE, 'Veritasium: 13 Misconceptions About Global Warming'),
        ('minuteearth', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'describing-motion-speed-velocity-acceleration': [
        ('minutephysics', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'ecosystems-and-interdependence': [
        ("it's ok", COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'energy-in-motion-crumple-zones-and-momentum': [
        ('real engineering', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'energy-transforming-matter-states-and-heating': [
        ('minutephysics', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'energy-use-and-sustainable-sources': [
        ('real engineering', RE_SOLAR, 'Real Engineering: The Mystery Flaw of Solar Panels'),
    ],
    'evolution-by-natural-selection': [
        ("it's ok", COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'forces-and-motion-the-basics': [
        ('minutephysics', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'gases-pressure-and-fluids': [
        ('veritasium', VER_FLUIDS, 'Veritasium: 3 Perplexing Physics Problems'),
    ],
    'gene-technology-and-ethics': [
        ('veritasium', KURZ_CRISPR, 'Kurzgesagt: Genetic Engineering Will Change Everything – CRISPR'),
    ],
    'growth-stem-cells-and-plant-hormones': [
        ("it's ok", COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'lifestyle-genes-and-non-communicable-disease': [
        ('scishow', SCISHOW_CANCER, 'SciShow: What Makes Cancer So Hard to Cure'),
    ],
    'light-sound-and-materials': [
        ('veritasium', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'magnetism-motors-and-generators': [
        ('real engineering', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'mutations-and-variation': [
        ('scishow', COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'nanoparticles-and-end-of-life': [
        ('scishow', SCISHOW_NANO, 'SciShow: The Giant of Nanoscience'),
    ],
    'pathogens-and-disease': [
        ('scishow', SCISHOW_VIRUSES, 'SciShow: Are Infectious Viruses Actually Alive?'),
    ],
    'photosynthesis-and-plant-growth': [
        ("it's ok", COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'polymers-bonding-and-materials': [
        ('real engineering', COGNITO_CHEM, 'Cognito: GCSE Chemistry (9-1) Playlist'),
    ],
    'potable-water': [
        ('scishow', COGNITO_CHEM, 'Cognito: GCSE Chemistry (9-1) Playlist'),
    ],
    'power-energy-and-mains-electricity': [
        ('real engineering', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'radioactivity-and-half-life': [
        ('veritasium', VER_RADIOACTIVE, 'Veritasium: The Most Radioactive Places on Earth'),
    ],
    'solids-springs-and-hookes-law': [
        ('minutephysics', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'stars-galaxies-and-the-big-bang': [
        ('veritasium', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'static-electricity-and-electric-charge': [
        ('veritasium', VER_STATIC, 'Veritasium: Sparks from Falling Water – Kelvin\'s Thunderstorm'),
    ],
    'stopping-infection-vaccination-and-hygiene': [
        ('scishow', SCISHOW_VACCINES, "SciShow: What's the Deal with Pfizer's COVID-19 Vaccine?"),
    ],
    'the-earths-atmosphere-through-time': [
        ('veritasium', COGNITO_CHEM, 'Cognito: GCSE Chemistry (9-1) Playlist'),
    ],
    'the-em-spectrum-and-its-risks': [
        ('minutephysics', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'treating-disease-drugs-and-trials': [
        ('scishow', COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'using-radioactive-materials-safely': [
        ('scishow', COGNITO_PHYS, 'Cognito: GCSE Physics (9-1) Playlist'),
    ],
    'wave-behaviour-reflection-refraction-diffraction': [
        ('veritasium', VER_DBL_SLIT, 'Veritasium: The Original Double Slit Experiment'),
    ],
    'biodiversity-and-classification': [
        ("it's ok", COGNITO_BIO, 'Cognito: GCSE Biology (9-1) Playlist'),
    ],
    'equations-and-calculations': [
        ('organic chemistry tutor', COGNITO_CHEM, 'Cognito: GCSE Chemistry (9-1) Playlist'),
    ],
}


def upgrade_item(item, category, lesson_slug, subject):
    """
    Mutate item in place if its URL needs upgrading.
    Returns True if changed.
    """
    url = item.get('url', '')
    title = item.get('title', '')
    title_lower = title.lower()

    # ── spark.iop.org → physicsandmathstutor.com ──────────────────────────────
    if 'spark.iop.org' in url:
        item['url'] = IOP_REPLACEMENT
        item['title'] = IOP_REPLACEMENT_TITLE
        return True

    # ── edu.rsc.org (generic root) → RSC periodic table ──────────────────────
    if url == 'https://edu.rsc.org':
        item['url'] = RSC_REPLACEMENT
        item['title'] = RSC_REPLACEMENT_TITLE
        return True

    # ── Cognito channel root → subject playlist ───────────────────────────────
    if url in COGNITO_ROOTS:
        item['url'] = cognito_playlist(subject)
        # keep title (already says "Cognito: [Topic]")
        return True

    # ── FSL channel root → FSL subject playlist ───────────────────────────────
    if url in FSL_ROOTS:
        item['url'] = fsl_playlist(subject)
        # keep title
        return True

    # ── CrashCourse channel root → CC subject playlist ────────────────────────
    if url in CC_ROOTS:
        item['url'] = cc_playlist(subject)
        # keep title
        return True

    # ── TED-Ed channel root → specific video ─────────────────────────────────
    if url in TED_ROOTS:
        # Apply lesson-specific override if available
        if lesson_slug in LESSON_OVERRIDES:
            for frag, new_url, new_title in LESSON_OVERRIDES[lesson_slug]:
                if frag in title_lower or 'ted' in title_lower:
                    item['url'] = new_url
                    item['title'] = new_title
                    return True
        # Default fallback
        item['url'] = cognito_playlist(subject)
        return True

    # ── Per-lesson overrides for specific channels (Veritasium, SciShow, etc.)
    if lesson_slug in LESSON_OVERRIDES:
        for frag, new_url, new_title in LESSON_OVERRIDES[lesson_slug]:
            # Match fragment against title (these items already have @channel root URLs)
            if frag in title_lower and (
                url.startswith('https://www.youtube.com/@') or
                url.startswith('https://www.youtube.com/c/')
            ):
                if new_url and new_url != url:
                    item['url'] = new_url
                    if new_title:
                        item['title'] = new_title
                    return True

    # ── Catch-all for remaining generic channel roots ─────────────────────────
    # Any remaining @channel or /c/ roots not handled above → Cognito playlist
    if (url.startswith('https://www.youtube.com/@') or
            url.startswith('https://www.youtube.com/c/')) and \
            'playlist?list=' not in url and '/watch?' not in url:
        item['url'] = cognito_playlist(subject)
        return True

    return False


def process_file(filepath):
    with open(filepath, encoding='utf-8') as fh:
        data = json.load(fh)

    lesson_slug = data.get('_lesson_slug', '')
    unit_slug = data.get('_unit_slug', '') or data.get('_meta', {}).get('unit_slug', '')
    subject = get_subject(unit_slug, lesson_slug)

    changed = 0
    for cat in data.get('related_media', []):
        for item in cat.get('items', []):
            if upgrade_item(item, cat['category'], lesson_slug, subject):
                changed += 1

    if changed:
        with open(filepath, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    return changed, lesson_slug


if __name__ == '__main__':
    lessons_dir = 'scripts/_content_separate-sciences-ocr-b/lessons'
    files = sorted(glob.glob(f'{lessons_dir}/*.json'))

    total_changed = 0
    files_changed = 0

    for f in files:
        n, slug = process_file(f)
        if n:
            print(f'  {slug}: {n} URL(s) updated')
            total_changed += n
            files_changed += 1

    print(f'\nDone: {files_changed} files, {total_changed} URLs updated.')
