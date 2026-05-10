"""Fix generic related_media URLs in separate-sciences-ocr lessons.

Strategy:
- @cognitoedu channel root -> subject-level Cognito playlist (Bio/Chem/Physics)
- @Freesciencelessons channel root -> topic-specific FSL playlist
- b006qykl (In Our Time brand page) -> keep URL, rewrite description honestly
- b036f7w2 (Inside Science brand page) -> keep URL, rewrite description honestly
- b015sqc7 (Life Scientific brand page) -> keep URL, rewrite description honestly
- edu.rsc.org brand root -> keep URL, rewrite description honestly
- openlearn/science-maths-technology hub -> keep URL, rewrite description honestly
- rsb.org.uk/education/educational-resources hub -> keep URL, rewrite description honestly
"""

import json
import os
import glob

LESSON_DIR = os.path.join(os.path.dirname(__file__), '_content_separate-sciences-ocr', 'lessons')

# Verified Cognito playlists (oembed-confirmed)
COGNITO_PLAYLISTS = {
    'biology':   ('https://www.youtube.com/playlist?list=PLidqqIGKox7X5UFT-expKIuR-i-BN3Q1g', 'GCSE Biology (9-1)'),
    'chemistry': ('https://www.youtube.com/playlist?list=PLidqqIGKox7WeOKVGHxcd69kKqtwrKl8W', 'GCSE Chemistry (9-1)'),
    'physics':   ('https://www.youtube.com/playlist?list=PLidqqIGKox7UVC-8WC9djoeBzwxPeXph7', 'GCSE Physics (9-1)'),
}

# Verified FSL playlists (oembed-confirmed)
FSL_PLAYLIST_MAP = {
    # Biology Paper 1
    'cell-structures-and-microscopy':                       ('PL9IouNCPbCxVU74eQtCcqbaQdYmwzAnlC', 'AQA GCSE Biology Paper 1 — Cell Biology'),
    'transport-diffusion-osmosis-and-active-transport':     ('PL9IouNCPbCxXGDt3ATU1xM_X_F8JghPCB', 'AQA GCSE Biology Paper 1 — Organisation'),
    'plant-and-animal-transport-systems':                   ('PL9IouNCPbCxXGDt3ATU1xM_X_F8JghPCB', 'AQA GCSE Biology Paper 1 — Organisation'),
    'health-disease-and-the-immune-system':                 ('PL9IouNCPbCxVQPNgqka5bSs-IWe3L6OD8', 'AQA GCSE Biology Paper 1 — Infectious Diseases'),
    'photosynthesis-and-limiting-factors':                  ('PL9IouNCPbCxXVpEqkFRN5Jq8ZZTBBRWUz', 'AQA GCSE Biology Paper 1 — Bioenergetics'),
    'respiration-and-synthesis-of-biological-molecules':    ('PL9IouNCPbCxXVpEqkFRN5Jq8ZZTBBRWUz', 'AQA GCSE Biology Paper 1 — Bioenergetics'),
    'dna-enzymes-and-cell-division':                        ('PL9IouNCPbCxVU74eQtCcqbaQdYmwzAnlC', 'AQA GCSE Biology Paper 1 — Cell Biology'),
    'feeding-the-human-race-selective-breeding-and-gm':     ('PL9IouNCPbCxXqJycGYKJhk2PMKICNBBZ8', 'AQA GCSE Biology Paper 2 — Variation and Evolution'),
    # Biology Paper 2
    'homeostasis-blood-glucose-and-temperature':            ('PL9IouNCPbCxW3lptxS1yHCP2I9YDfM2co', 'AQA GCSE Biology Paper 2 — Homeostasis'),
    'hormones-the-menstrual-cycle-and-plant-hormones':      ('PL9IouNCPbCxW3lptxS1yHCP2I9YDfM2co', 'AQA GCSE Biology Paper 2 — Homeostasis'),
    'the-nervous-system-and-reflex-arc':                    ('PL9IouNCPbCxW3lptxS1yHCP2I9YDfM2co', 'AQA GCSE Biology Paper 2 — Homeostasis'),
    'the-kidneys-and-osmoregulation':                       ('PL9IouNCPbCxW3lptxS1yHCP2I9YDfM2co', 'AQA GCSE Biology Paper 2 — Homeostasis'),
    'inheritance-and-genetic-disorders':                    ('PL9IouNCPbCxXqJycGYKJhk2PMKICNBBZ8', 'AQA GCSE Biology Paper 2 — Variation and Evolution'),
    'reproduction-meiosis-and-dna':                         ('PL9IouNCPbCxXqJycGYKJhk2PMKICNBBZ8', 'AQA GCSE Biology Paper 2 — Variation and Evolution'),
    'variation-evolution-and-speciation':                   ('PL9IouNCPbCxXqJycGYKJhk2PMKICNBBZ8', 'AQA GCSE Biology Paper 2 — Variation and Evolution'),
    'ecosystems-biotic-and-abiotic-factors':                ('PL9IouNCPbCxVuf3dVIq6kHQ0b27Hu-fgW', 'AQA GCSE Biology Paper 2 — Ecology'),
    'monitoring-the-environment-and-biodiversity':          ('PL9IouNCPbCxVuf3dVIq6kHQ0b27Hu-fgW', 'AQA GCSE Biology Paper 2 — Ecology'),
    # Chemistry Paper 1
    'atomic-structure-and-the-development-of-the-atom':     ('PL9IouNCPbCxULWXCO9jt0PsuAbxYpw2_1', 'AQA GCSE Chemistry Paper 1 — Atomic Structure and the Periodic Table'),
    'periodic-table-and-group-trends':                      ('PL9IouNCPbCxULWXCO9jt0PsuAbxYpw2_1', 'AQA GCSE Chemistry Paper 1 — Atomic Structure and the Periodic Table'),
    'bonding-ionic-covalent-and-metallic':                  ('PL9IouNCPbCxXmFgiKCM60Sglh-qOG_vlE', 'AQA GCSE Chemistry Paper 1 — Structure and Bonding'),
    'properties-of-materials-and-nanoparticles':            ('PL9IouNCPbCxXmFgiKCM60Sglh-qOG_vlE', 'AQA GCSE Chemistry Paper 1 — Structure and Bonding'),
    'purity-separating-mixtures-and-chromatography':        ('PL9IouNCPbCxULWXCO9jt0PsuAbxYpw2_1', 'AQA GCSE Chemistry Paper 1 — Atomic Structure and the Periodic Table'),
    'chemical-reactions-equations-and-moles':               ('PL9IouNCPbCxXDlRtCQEG0cGehBvJ7t9Pf', 'AQA GCSE Chemistry Paper 1 — Chemical Reactions'),
    'gas-volumes-atom-economy-and-yield':                   ('PL9IouNCPbCxUhxxFUbR4SNfwmaRB8mYX3', 'AQA GCSE Chemistry Paper 1 — Quantitative Chemistry'),
    'electrolysis-of-molten-and-aqueous-compounds':         ('PL9IouNCPbCxXDlRtCQEG0cGehBvJ7t9Pf', 'AQA GCSE Chemistry Paper 1 — Chemical Reactions'),
    'energetics-reaction-profiles-and-bond-energies':       ('PL9IouNCPbCxX74bPfz0TGVVmyGYgMarWu', 'AQA GCSE Chemistry Paper 1 — Energy Changes'),
    'types-of-reaction-redox-acids-and-neutralisation':     ('PL9IouNCPbCxXDlRtCQEG0cGehBvJ7t9Pf', 'AQA GCSE Chemistry Paper 1 — Chemical Reactions'),
    # Chemistry Paper 2
    'rates-of-reaction-and-collision-theory':               ('PL9IouNCPbCxW8AN0t0py7LaKdKSwfL3fP', 'AQA GCSE Chemistry Paper 2 — Rates of Reaction'),
    'reversible-reactions-and-le-chateliers-principle':     ('PL9IouNCPbCxW8AN0t0py7LaKdKSwfL3fP', 'AQA GCSE Chemistry Paper 2 — Rates of Reaction'),
    'organic-chemistry-hydrocarbons-alcohols-and-polymers': ('PL9IouNCPbCxVDcgWiviYYWj0xKMPXTd8s', 'AQA GCSE Chemistry Paper 2 — Organic Chemistry'),
    'identifying-substances-flame-tests-and-gas-tests':     ('PL9IouNCPbCxXlBeaxebOG5yf_pGrxzOyR', 'AQA GCSE Chemistry Paper 2 — Chemical Analysis'),
    'improving-processes-metals-lcas-and-recycling':        ('PL9IouNCPbCxVQ-jFybEAnf4D8Naid7qsx', 'AQA GCSE Chemistry Paper 2 — Resources'),
    'earths-atmosphere-and-climate-change':                 ('PL9IouNCPbCxVQ-jFybEAnf4D8Naid7qsx', 'AQA GCSE Chemistry Paper 2 — Resources'),
    'earths-resources-water-pollution-and-sustainability':  ('PL9IouNCPbCxVQ-jFybEAnf4D8Naid7qsx', 'AQA GCSE Chemistry Paper 2 — Resources'),
    'titrations-and-molar-concentrations':                  ('PL9IouNCPbCxW8AN0t0py7LaKdKSwfL3fP', 'AQA GCSE Chemistry Paper 2 — Rates of Reaction'),
    # Physics Paper 1
    'energy-resources-and-efficiency':                      ('PL9IouNCPbCxWNjJvmqwZ4vKy4VfcAhsCj', 'AQA GCSE Physics Paper 1 — Energy'),
    'internal-energy-shc-and-latent-heat':                  ('PL9IouNCPbCxWdHszkb6n6503ommOpg_t7', 'AQA GCSE Physics Paper 1 — Particle Model of Matter'),
    'the-particle-model-and-states-of-matter':              ('PL9IouNCPbCxWdHszkb6n6503ommOpg_t7', 'AQA GCSE Physics Paper 1 — Particle Model of Matter'),
    'particle-model-density-and-pressure':                  ('PL9IouNCPbCxWdHszkb6n6503ommOpg_t7', 'AQA GCSE Physics Paper 1 — Particle Model of Matter'),
    'static-electricity-and-simple-circuits':               ('PL9IouNCPbCxXc2NQoIZN7-3jIKN7vW-Sq', 'AQA GCSE Physics Paper 1 — Electricity'),
    'series-parallel-and-domestic-electricity':             ('PL9IouNCPbCxXc2NQoIZN7-3jIKN7vW-Sq', 'AQA GCSE Physics Paper 1 — Electricity'),
    'radioactivity-emissions-half-life-and-equations':      ('PL9IouNCPbCxXTU7zSX4IvJDLrtCEmqEMU', 'AQA GCSE Physics Paper 1 — Atomic Structure and Radioactivity'),
    'half-life-and-nuclear-equations':                      ('PL9IouNCPbCxXTU7zSX4IvJDLrtCEmqEMU', 'AQA GCSE Physics Paper 1 — Atomic Structure and Radioactivity'),
    'uses-and-dangers-of-radiation':                        ('PL9IouNCPbCxXTU7zSX4IvJDLrtCEmqEMU', 'AQA GCSE Physics Paper 1 — Atomic Structure and Radioactivity'),
    # Physics Paper 2
    'motion-speed-velocity-and-acceleration':               ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'newtons-laws-and-resultant-forces':                    ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'forces-in-action-springs-hookes-law-and-moments':      ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'moments-levers-and-gears':                             ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'pressure-in-fluids':                                   ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'physics-on-the-move-stopping-distances-and-momentum': ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'work-energy-and-power':                                ('PL9IouNCPbCxUrQkFLoPwB67nDbhw2NfAO', 'AQA GCSE Physics Paper 2 — Forces'),
    'magnets-magnetic-fields-and-the-motor-effect':         ('PL9IouNCPbCxVean2cWoznpfC5PxYbs9TX', 'AQA GCSE Physics Paper 2 — Magnetism'),
    'transformers-and-the-national-grid':                   ('PL9IouNCPbCxVean2cWoznpfC5PxYbs9TX', 'AQA GCSE Physics Paper 2 — Magnetism'),
    'wave-behaviour-and-the-wave-equation':                 ('PL9IouNCPbCxX1-0Nr5_bMDJnN-9RqMuA6', 'AQA GCSE Physics Paper 2 — Waves'),
    'wave-interaction-reflection-refraction-and-lenses':    ('PL9IouNCPbCxX1-0Nr5_bMDJnN-9RqMuA6', 'AQA GCSE Physics Paper 2 — Waves'),
    'the-electromagnetic-spectrum':                         ('PL9IouNCPbCxX1-0Nr5_bMDJnN-9RqMuA6', 'AQA GCSE Physics Paper 2 — Waves'),
    'beyond-earth-solar-system-stars-and-the-universe':     ('PL9IouNCPbCxUGMXZ4ubg_ttcNboQa-PtI', 'AQA GCSE Physics Paper 2 — Space Physics'),
}


def get_cognito_subject(unit_slug):
    if 'biology' in unit_slug:
        return 'biology'
    elif 'chemistry' in unit_slug:
        return 'chemistry'
    elif 'physics' in unit_slug:
        return 'physics'
    return 'physics'  # fallback


def process_file(filepath):
    slug = os.path.basename(filepath).replace('.json', '')
    with open(filepath, encoding='utf-8') as fh:
        data = json.load(fh)

    unit_slug = data.get('_meta', {}).get('unit_slug', '')
    cognito_subject = get_cognito_subject(unit_slug)
    fsl_pl_id, fsl_pl_title = FSL_PLAYLIST_MAP.get(slug, (None, None))

    changes = 0

    for cat in data.get('related_media', []):
        for item in cat.get('items', []):
            url = item.get('url', '')
            title = item.get('title', '')

            # 1. Cognito channel root -> subject playlist
            if url == 'https://www.youtube.com/@cognitoedu':
                pl_url, pl_label = COGNITO_PLAYLISTS[cognito_subject]
                # Strip " — Cognito" from title and append " — Cognito Playlist"
                clean_title = title.replace(' — Cognito', '').strip()
                item['url'] = pl_url
                item['title'] = f'{clean_title} — Cognito Playlist'
                item['description'] = (
                    f'Cognito {pl_label} playlist covering all GCSE exam topics with '
                    f'animated explanations and worked examples.'
                )
                changes += 1

            # 2. Free Science Lessons channel root -> topic playlist
            elif url == 'https://www.youtube.com/@Freesciencelessons':
                if fsl_pl_id:
                    item['url'] = f'https://www.youtube.com/playlist?list={fsl_pl_id}'
                    item['description'] = (
                        f'Free Science Lessons playlist: {fsl_pl_title}. '
                        f'Step-by-step revision videos covering all required subtopics.'
                    )
                    changes += 1

            # 3. In Our Time generic programme page -> keep URL, honest description
            elif url == 'https://www.bbc.co.uk/programmes/b006qykl':
                item['description'] = (
                    'The In Our Time podcast archive on BBC Radio 4 — hundreds of science '
                    'episodes exploring the history and ideas behind major topics. '
                    'Search the back catalogue for relevant episodes on this subject.'
                )
                changes += 1

            # 4. Inside Science generic -> keep URL, honest description
            elif url == 'https://www.bbc.co.uk/programmes/b036f7w2':
                item['description'] = (
                    'BBC Radio 4 weekly science programme exploring cutting-edge research '
                    'and the science behind current news stories. Free to stream on BBC Sounds.'
                )
                changes += 1

            # 5. The Life Scientific generic -> keep URL, honest description
            elif url == 'https://www.bbc.co.uk/programmes/b015sqc7':
                item['description'] = (
                    'Jim Al-Khalili interviews leading scientists about their research and '
                    'careers on BBC Radio 4. Browse the full episode archive for biology, '
                    'chemistry and physics topics.'
                )
                changes += 1

            # 6. RSC brand root -> keep URL, honest description
            elif url == 'https://edu.rsc.org':
                item['description'] = (
                    'Free chemistry education resources from the Royal Society of Chemistry '
                    '— interactive topic guides, videos and teacher resources for GCSE and beyond.'
                )
                changes += 1

            # 7. OpenLearn hub -> keep URL, honest description
            elif url == 'https://www.open.edu/openlearn/science-maths-technology':
                item['description'] = (
                    'Free Open University short courses in science, maths and technology. '
                    'Introductory and GCSE-equivalent level — most content free without registration.'
                )
                changes += 1

            # 8. RSB educational resources hub -> keep URL, honest description
            elif 'rsb.org.uk' in url and url.endswith('/educational-resources'):
                item['description'] = (
                    'Biology education resources from the Royal Society of Biology, including '
                    'topic guides, career information and curriculum-aligned materials for GCSE students.'
                )
                changes += 1

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    return slug, changes


if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(LESSON_DIR, '*.json')))
    total_changes = 0
    files_modified = 0

    for f in files:
        slug, n = process_file(f)
        if n > 0:
            print(f'  {slug}: {n} changes')
            total_changes += n
            files_modified += 1

    print(f'\nDone. {total_changes} URL/description updates across {files_modified}/{len(files)} files.')
