import json, re
pd=json.load(open('_live_geometry_L04.json',encoding='utf-8'))

def find_svgs(obj, path=''):
    out=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            out+=find_svgs(v,path+'/'+str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            out+=find_svgs(v,path+f'[{i}]')
    elif isinstance(obj,str) and '<svg' in obj:
        out.append((path,obj))
    return out

def analyze(svg):
    # darker axis lines: group stroke-opacity 0.5
    m=re.search(r'stroke-opacity="0.5"[^>]*>(.*?)</g>',svg,re.S)
    seg=m.group(1)
    lines=re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"',seg)
    # horizontal axis (y1==y2) gives y0; vertical (x1==x2) gives x0
    x0=y0=None
    for x1,y1,x2,y2 in lines:
        x1,y1,x2,y2=map(float,(x1,y1,x2,y2))
        if y1==y2: y0=y1
        if x1==x2: x0=x1
    circles=re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)"',svg)
    pts=[]
    for cx,cy in circles:
        cx,cy=float(cx),float(cy)
        gx=(cx-x0)/18.0
        gy=(y0-cy)/18.0
        pts.append((round(gx,3),round(gy,3)))
    # orange X centre markers
    xm=re.findall(r'#f59e0b" stroke-width="1.6"><line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"/><line x1="([\d.]+)" y1="([\d.]+)"',svg)
    centres=[]
    mm=re.findall(r'stroke="#f59e0b" stroke-width="1.6"><line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"/>',svg)
    for a in mm:
        x1,y1,x2,y2=map(float,a)
        ccx=(x1+x2)/2; ccy=(y1+y2)/2
        centres.append((round((ccx-x0)/18,3),round((y0-ccy)/18,3)))
    aria=re.search(r'aria-label="([^"]*)"',svg).group(1)
    return x0,y0,pts,centres,aria

for path,svg in find_svgs(pd):
    x0,y0,pts,centres,aria=analyze(svg)
    print(f"{path}\n  origin=({x0},{y0}) points={pts} centres={centres}\n  aria: {aria}")
