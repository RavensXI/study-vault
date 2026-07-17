import json, re
live=json.load(open('_RECHK_live.json',encoding='utf-8'))
pb=live['problem_bank']
out=[]
def labels(disp):
    return re.findall(r'>([^<]*)</text>', disp)
def has_svg(d): return '<svg' in d

# expected numeric tokens per problem (from display prose)
def nums(disp):
    prose = re.sub(r'<[^>]+>','',disp)
    return prose

for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pb[tier]):
        d=p['display']
        if not has_svg(d):
            out.append(f"{tier}[{i}] NO SVG (mc/text): {nums(d)[:50]}")
            continue
        labs=[l for l in labels(d) if l.strip()]
        # check external refs
        if 'href' in d or 'xlink' in d or '<script' in d.lower():
            out.append(f"{tier}[{i}] EXTERNAL REF/SCRIPT")
        # check hardcoded dark text fill
        for m in re.finditer(r'<text[^>]*fill="([^"]+)"', d):
            if m.group(1)!='currentColor':
                out.append(f"{tier}[{i}] non-currentColor text fill: {m.group(1)}")
        out.append(f"{tier}[{i}] labels={labs}  sol={p['solutions']}  prose='{nums(d)}'")
# teach + opener
g=live['guided']
for t in ['bronze','silver','gold']:
    d=g['teach'][t]['display']
    out.append(f"teach-{t} labels={[l for l in labels(d) if l.strip()]} prose='{re.sub(chr(60)+'[^'+chr(62)+']+'+chr(62),'',d)}'")
d=g['opener']['display']
out.append(f"opener labels={[l for l in labels(d) if l.strip()]} prose='{re.sub(chr(60)+'[^'+chr(62)+']+'+chr(62),'',d)}'")
for o in out: print(o)
