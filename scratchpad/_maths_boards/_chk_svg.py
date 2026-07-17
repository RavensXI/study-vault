import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

d = json.load(open('_live_L04.json', encoding='utf-8'))[0]['practice_data']
pb = d['problem_bank']

def parse_num(s):
    # convert unicode minus to ascii
    return float(s.replace('−', '-').replace('–', '-').replace(' ', ''))

def check_svg(tier, idx):
    disp = pb[tier][idx]['display']
    m = re.search(r'<svg.*?</svg>', disp, re.S)
    if not m:
        print(f'{tier}[{idx}]: NO SVG')
        return
    svg = m.group(0)
    # bold axis lines have stroke-width="1.6"
    bold = re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="currentColor" stroke-width="1.6"/>', svg)
    # x-axis: horizontal bold (y1==y2); y-axis: vertical bold (x1==x2)
    xaxis_y = yaxis_x = None
    for x1, y1, x2, y2 in bold:
        if y1 == y2:
            xaxis_y = float(y1)
        if x1 == x2:
            yaxis_x = float(x1)
    # scale: from gridline spacing. Find all vertical gridline x positions
    vlines = sorted(set(float(x) for x in re.findall(r'<line x1="([\d.]+)" y1="[\d.]+" x2="\1" y2="[\d.]+" stroke="currentColor" stroke-opacity', svg)))
    scale = None
    if len(vlines) >= 2:
        diffs = [round(vlines[i+1]-vlines[i], 2) for i in range(len(vlines)-1)]
        scale = sum(diffs)/len(diffs)
    print(f'{tier}[{idx}]: origin_px=({yaxis_x},{xaxis_y}) scale={scale:.3f}')
    # circles: cx, cy, then following text label
    for cm in re.finditer(r'<circle cx="([\d.]+)" cy="([\d.]+)"[^>]*/>\s*<text[^>]*>([^<]+)</text>', svg):
        cx, cy, label = float(cm.group(1)), float(cm.group(2)), cm.group(3)
        gx = (cx - yaxis_x)/scale
        gy = (xaxis_y - cy)/scale
        # parse label coords
        nums = re.findall(r'-?\d+', label.replace('−','-'))
        print(f'   circle label={label!r} -> px({cx},{cy}) -> grid=({gx:.2f},{gy:.2f})')
    # crosses: two lines crossing, followed by text 'centre (a, b)'
    for cm in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="currentColor" stroke-width="1.8"/>\s*<line[^>]*stroke-width="1.8"/>\s*<text[^>]*>([^<]+)</text>', svg):
        x1, y1, x2, y2 = map(float, cm.group(1,2,3,4))
        label = cm.group(5)
        cx = (x1+x2)/2; cy = (y1+y2)/2
        gx = (cx - yaxis_x)/scale
        gy = (xaxis_y - cy)/scale
        print(f'   cross  label={label!r} -> centre_px({cx},{cy}) -> grid=({gx:.2f},{gy:.2f})')

for t, i in [('silver',2), ('silver',6), ('gold',0), ('gold',1), ('gold',2), ('gold',4)]:
    check_svg(t, i)
