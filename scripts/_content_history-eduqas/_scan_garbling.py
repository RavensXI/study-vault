#!/usr/bin/env python3
"""One-off scanner: find malformed HTML entities + em-dash issues in the
History Eduqas lesson JSONs. Reports file / field / snippet so we can see the
real scope of the Paré-style garbling Tom spotted."""
import json, re, glob, os, html, collections

LESSON_DIR = os.path.join(os.path.dirname(__file__), 'lessons')

# Valid HTML named entities we expect to legitimately see in *_html fields.
VALID = {'amp', 'lt', 'gt', 'quot', 'apos', 'nbsp', 'mdash', 'ndash',
         'rsquo', 'lsquo', 'rdquo', 'ldquo', 'hellip', 'eacute', 'egrave',
         'agrave', 'ccedil', 'uuml', 'ouml', 'auml', 'iexcl', 'aacute',
         'oacute', 'iacute', 'uacute', 'ntilde', 'deg', 'pound', 'copy',
         'reg', 'times', 'frac12', 'frac14', 'frac34', 'euml', 'iuml',
         'ecirc', 'ocirc', 'acirc', 'icirc', 'ucirc', 'oslash', 'aelig',
         'szlig', 'middot', 'bull', 'dagger', 'sect', 'para'}

PLAIN_FIELDS = {'description', 'practice_questions', 'knowledge_checks',
                'flashcard_questions', 'glossary_terms', 'title'}

ENTITY_RE = re.compile(r'&([a-zA-Z][a-zA-Z0-9]{0,12});')
# double-encoded: &amp;eacute; etc.
DOUBLE_RE = re.compile(r'&amp;([a-zA-Z]{2,12});')

findings = collections.defaultdict(list)   # bucket -> [ (file, field, snippet) ]


def walk(obj, path, fname):
    if isinstance(obj, str):
        check(obj, path, fname)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, k, fname)
    elif isinstance(obj, list):
        for it in obj:
            walk(it, path, fname)


def snip(s, idx, w=45):
    a = max(0, idx - w); b = min(len(s), idx + w)
    return ('…' if a else '') + s[a:b].replace('\n', ' ') + ('…' if b < len(s) else '')


def check(s, field, fname):
    is_plain = field in PLAIN_FIELDS
    # 1. double-encoded entities anywhere
    for m in DOUBLE_RE.finditer(s):
        findings['double_encoded'].append((fname, field, snip(s, m.start())))
    # 2. unknown/broken named entities (e.g. &reacute;) anywhere
    for m in ENTITY_RE.finditer(s):
        name = m.group(1).lower()
        if name not in VALID and not name.startswith('#'):
            findings['broken_entity'].append((fname, field, m.group(0), snip(s, m.start())))
    # 3. ANY entity in a plain-text field (should be unicode)
    if is_plain:
        for m in ENTITY_RE.finditer(s):
            findings['entity_in_plaintext'].append((fname, field, m.group(0), snip(s, m.start())))
        if re.search(r'\bem[ -]?dash(es)?\b', s, re.I):
            findings['written_em_dash'].append((fname, field, snip(s, re.search(r'\bem[ -]?dash(es)?\b', s, re.I).start())))


files = sorted(glob.glob(os.path.join(LESSON_DIR, '*.json')))
for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        findings['parse_error'].append((os.path.basename(f), '', str(e)))
        continue
    walk(data, '', os.path.basename(f))

for bucket in ['parse_error', 'broken_entity', 'double_encoded', 'entity_in_plaintext', 'written_em_dash']:
    rows = findings.get(bucket, [])
    print(f'\n=== {bucket}: {len(rows)} ===')
    # summarise broken_entity by entity token
    if bucket == 'broken_entity' and rows:
        by_tok = collections.Counter(r[2] for r in rows)
        for tok, n in by_tok.most_common():
            print(f'  {tok}  x{n}')
    for r in rows[:25]:
        print('   ', ' | '.join(str(x) for x in r))
    if len(rows) > 25:
        print(f'    ... +{len(rows)-25} more')
