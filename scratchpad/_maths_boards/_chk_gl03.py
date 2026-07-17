# -*- coding: utf-8 -*-
import json, re

d = json.load(open('_LIVE_geometry-L03.json', encoding='utf-8'))
pd = d[0]['practice_data']
s = json.dumps(pd, ensure_ascii=False)

EMDASH = '—'
MINUS = '−'
print("Real em-dash (U+2014) count:", s.count(EMDASH))

# find em dashes with context, excluding internal 'note' fields
idxs = [m.start() for m in re.finditer(EMDASH, s)]
for i in idxs[:20]:
    print("  ctx:", repr(s[i-40:i+40]))

# SVG external refs: only flag xlink:href / url() / <image href to external
svgs = re.findall(r'<svg.*?</svg>', s, re.S)
print("\nNum SVGs:", len(svgs))
ext = 0
for sv in svgs:
    if 'xlink:href' in sv or re.search(r'href=', sv) or '<image' in sv or 'url(' in sv:
        ext += 1
        print("  EXTERNAL REF in svg:", sv[:80])
print("SVG external refs:", ext)

# text fills not currentColor
badfill = set(re.findall(r'<text[^>]*fill="([^"]+)"', s))
print("text fill values:", badfill)

# Check where 'http' appears (should only be preserved related_videos, not svg)
for sv in svgs:
    if 'http' in sv:
        print("  http in SVG:", sv[:120])

# tier_guides word budget check
tg = pd['tier_guides']
for tier in ['bronze','silver','gold']:
    steps = tg[tier]['steps']
    text = ' '.join(re.sub('<[^>]+>','',x) for x in steps)
    wc = len(text.split())
    print(f"tier_guide {tier} steps words: {wc} (<=115)")
