"""Pass 2 remediation — fixes the leftover issues from pass 1."""
import json
from pathlib import Path

# Rebuild fake-MCQ-as-match KCs as real matches
rebuilds = {
    'scripts/_content_astronomy-edexcel/lessons/space-probes-and-crewed-exploration.json': {
        'q': 'Match each probe type to its main advantage.',
        'type': 'match',
        'left': ['Fly-by', 'Orbiter', 'Lander'],
        'right': ['Low fuel cost for a single fast encounter with a distant target',
                  'Long-term observation of a body from orbit',
                  'In-situ sampling and surface measurements'],
        'order': [0, 1, 2],
    },
    'scripts/_content_astronomy-edexcel/lessons/sunspots-the-solar-cycle-and-the-solar-wind.json': {
        'q': 'Match each space-weather effect to the system most affected.',
        'type': 'match',
        'left': ['Geomagnetic storm', 'Coronal mass ejection', 'Solar flare'],
        'right': ['Induced currents in power grids on the ground',
                  'Damage to spacecraft electronics in orbit',
                  'Disruption to high-frequency radio communication'],
        'order': [0, 1, 2],
    },
    'scripts/_content_astronomy-edexcel/lessons/telescopes-optics-magnification-and-resolution.json': {
        'q': 'Match each optical defect to its cause.',
        'type': 'match',
        'left': ['Chromatic aberration', 'Spherical aberration', 'Diffraction limit'],
        'right': ['Wavelength-dependent refraction in a lens — fixed with achromatic or reflector designs',
                  'Spherical mirror shape — fixed by using a parabolic mirror',
                  'Wave nature of light — set by aperture size, no full fix'],
        'order': [0, 1, 2],
    },
    'scripts/_content_astronomy-edexcel/lessons/the-solar-system-planets-dwarf-planets-and-small-bodies.json': {
        'q': 'Match each Solar System region to what it contains.',
        'type': 'match',
        'left': ['Asteroid belt', 'Kuiper belt', 'Oort cloud'],
        'right': ['Rocky small bodies between Mars and Jupiter',
                  'Icy short-period comet source beyond Neptune',
                  'Spherical long-period comet reservoir far from the Sun'],
        'order': [0, 1, 2],
    },
    'scripts/_content_astronomy-edexcel/lessons/the-sun-structure-fusion-and-atmosphere.json': {
        'q': 'Match each solar layer to its main energy-transport mechanism.',
        'type': 'match',
        'left': ['Core', 'Radiative zone', 'Convective zone'],
        'right': ['Nuclear fusion releases energy as photons',
                  'Photon diffusion transports energy outward',
                  'Bulk plasma movement carries energy to the surface'],
        'order': [0, 1, 2],
    },
}

for path, new_kc in rebuilds.items():
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    d['knowledge_checks'][4] = new_kc
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  rebuilt match KC: {p.name}')

# Fix Eng FC[5] duplicate '0 (LOW)' in electronic-systems
p = Path('scripts/_content_engineering-aqa/lessons/electronic-systems-sensors-logic-and-components.json')
d = json.loads(p.read_text(encoding='utf-8'))
# Find FC[5] and reword
fc5 = d['flashcard_questions'][5]
fc5_q = fc5.get('q', '')
# Already disambiguated by pass 1, but if dup answer persists, change answer
# Reword the entire card
d['flashcard_questions'][5] = {
    'q': "If a NAND gate sees inputs 1 and 1, what output does it produce?",
    'a': "0 — both inputs HIGH gives a NAND output of LOW (0).",
}
p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'  reworded FC[5]: {p.name}')

# Fix Astro planet-earth description too short (<60 chars from pass 1 over-trim)
p = Path('scripts/_content_astronomy-edexcel/lessons/planet-earth-shape-structure-and-atmosphere.json')
d = json.loads(p.read_text(encoding='utf-8'))
d['description'] = 'Earth as an oblate spheroid — interior structure, atmosphere and observing conditions.'
p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'  fixed short description: {p.name}')

# Fix banned 'award 2 marks for' in celestial-sphere
p = Path('scripts/_content_astronomy-edexcel/lessons/the-celestial-sphere-and-coordinate-systems.json')
d = json.loads(p.read_text(encoding='utf-8'))
import re
changed = False
def fix_marks_text(s):
    return re.sub(r'(?i)award (\d+) marks? for', r'\1 marks awarded for', s)
for pq in d.get('practice_questions', []):
    if isinstance(pq, dict) and 'marks' in pq:
        new = fix_marks_text(pq['marks']) if isinstance(pq['marks'], str) else pq['marks']
        if new != pq['marks']:
            pq['marks'] = new
            changed = True
if changed:
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  fixed banned rubric phrase: {p.name}')

# Astro the-night-sky FC[3] enumeration "Cygnus, Lyra and Aquila"
p = Path('scripts/_content_astronomy-edexcel/lessons/the-night-sky-constellations-asterisms-and-pointers.json')
d = json.loads(p.read_text(encoding='utf-8'))
d['flashcard_questions'][3] = {
    'q': "Name one of the three constellations that form the Summer Triangle.",
    'a': "Cygnus (with Lyra and Aquila completing the asterism).",
}
p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'  fixed enumeration FC[3]: {p.name}')

# Astro cosmology — insufficient collapsibles (need 2, has 1)
p = Path('scripts/_content_astronomy-edexcel/lessons/cosmology-redshift-hubbles-law-and-the-big-bang.json')
d = json.loads(p.read_text(encoding='utf-8'))
h = d['content_html']
if h.count('class="collapsible"') < 2:
    extra = '''
<div class="collapsible">
  <button class="collapsible-toggle" aria-expanded="false">
    <span>Hubble tension — why the value of H₀ is still being argued over</span>
    <svg class="collapsible-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </button>
  <div class="collapsible-inner">
    <p data-narration-id="n_extra1">Two independent methods give slightly different values for H₀. The Planck satellite&rsquo;s measurement of the cosmic microwave background gives roughly 67 km/s/Mpc, while distance ladders built from Cepheid variables and Type Ia supernovae give around 73 km/s/Mpc. The gap, called the <strong>Hubble tension</strong>, is small but stubborn. Resolving it may need new physics &mdash; possibly hinting at properties of dark energy not yet captured by the standard cosmological model. For exam purposes the syllabus value of ~70 km/s/Mpc is fine.</p>
  </div>
</div>
'''
    # Insert before the closing </section> or at end
    if '</section>' in h:
        idx = h.rfind('</section>')
        h = h[:idx] + extra + h[idx:]
    else:
        h = h + extra
    d['content_html'] = h
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  added 2nd collapsible: {p.name}')

# Astro telescopes-across-the-spectrum — insufficient key-facts
p = Path('scripts/_content_astronomy-edexcel/lessons/telescopes-across-the-spectrum-and-in-space.json')
d = json.loads(p.read_text(encoding='utf-8'))
h = d['content_html']
if h.count('class="key-fact"') < 2:
    extra = '''
<div class="key-fact" data-revision-tip="Name the wavelength, the atmospheric problem and the instrument that solves it — three points = three marks.">
  <div class="key-fact-label">Key Fact</div>
  <p>Each waveband faces a specific atmospheric problem. Visible and radio sneak through &mdash; infrared is blocked by water vapour (high-altitude observatories help), ultraviolet and X-ray are blocked by ozone and nitrogen (space telescopes only), and gamma rays need detectors above the atmosphere because they hit the air and shower into secondary particles.</p>
</div>
'''
    if '</section>' in h:
        idx = h.rfind('</section>')
        h = h[:idx] + extra + h[idx:]
    else:
        h = h + extra
    d['content_html'] = h
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  added 2nd key-fact: {p.name}')

# Astro telescopes-optics — insufficient key-facts
p = Path('scripts/_content_astronomy-edexcel/lessons/telescopes-optics-magnification-and-resolution.json')
d = json.loads(p.read_text(encoding='utf-8'))
h = d['content_html']
if h.count('class="key-fact"') < 2:
    extra = '''
<div class="key-fact" data-revision-tip="Resolution depends on aperture, not magnification — write this in any 6-mark answer where students might confuse the two.">
  <div class="key-fact-label">Key Fact</div>
  <p>A telescope&rsquo;s ability to <strong>resolve</strong> close-together objects is set by aperture diameter (the diffraction limit θ ≈ λ/D), not by magnification. Two stars 1 arcsecond apart can never be split by a 50mm scope no matter how high the eyepiece magnification — only a bigger aperture fixes it.</p>
</div>
'''
    if '</section>' in h:
        idx = h.rfind('</section>')
        h = h[:idx] + extra + h[idx:]
    else:
        h = h + extra
    d['content_html'] = h
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  added 2nd key-fact: {p.name}')

# Astro the-milky-way — insufficient key-facts
p = Path('scripts/_content_astronomy-edexcel/lessons/the-milky-way-and-other-galaxies.json')
d = json.loads(p.read_text(encoding='utf-8'))
h = d['content_html']
if h.count('class="key-fact"') < 2:
    extra = '''
<div class="key-fact" data-revision-tip="Memorise the Hubble tuning-fork letter codes — Sa/Sb/Sc are the spirals, E0–E7 are the ellipticals from round to elongated.">
  <div class="key-fact-label">Key Fact</div>
  <p>The Hubble tuning-fork classifies galaxies by visible shape: <strong>E0–E7</strong> (ellipticals, round to elongated), <strong>Sa/Sb/Sc</strong> (spirals, tight to loose arms), <strong>SBa/SBb/SBc</strong> (barred spirals), and <strong>Irr</strong> (irregulars). The Milky Way is an SBc — a loose-armed barred spiral.</p>
</div>
'''
    if '</section>' in h:
        idx = h.rfind('</section>')
        h = h[:idx] + extra + h[idx:]
    else:
        h = h + extra
    d['content_html'] = h
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  added 2nd key-fact: {p.name}')

print('\n=== Pass 2 done ===')
