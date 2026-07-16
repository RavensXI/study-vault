# -*- coding: utf-8 -*-
"""geometry-L05 opener: draw the picture the text promises. Inline SVG of the
classic 3-4-5 right triangle with tiled squares on all three sides (9 + 16
tiles visible, hypotenuse square marked ?), matching the counting boxes."""
import json, io, os, sys, subprocess, urllib.request

sys.stdout.reconfigure(errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = json.load(io.open(os.path.join(HERE, "_worklist.json"), encoding="utf-8"))["geometry-L05"]["id"]

def cells(x0, y0, nx, ny, s, fill):
    out = []
    for i in range(nx):
        for j in range(ny):
            out.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="#fff" stroke-width="1.2"/>'
                       % (x0 + i * s, y0 + j * s, s, s, fill))
    return "".join(out)

U = 18
svg = (
 '<svg viewBox="14 0 232 248" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%" role="img" '
 'aria-label="Right-angled triangle, short sides 3 and 4, with a tiled square drawn on each of the three sides">'
 # square on the vertical leg: 3x3 = 9 tiles
 + cells(95 - 3 * U, 96, 3, 3, U, "#dbeafe")
 # square on the horizontal leg: 4x4 = 16 tiles
 + cells(95, 150, 4, 4, U, "#fef3c7")
 # square on the hypotenuse: 5x5 = 25 tiles, rotated onto the slope
 + '<g transform="translate(167,150) rotate(216.87)">'
 + cells(0, 0, 5, 5, U, "#dcfce7")
 + '</g>'
 # the triangle itself
 + '<polygon points="95,150 167,150 95,96" fill="#f3ece2" stroke="#2d2a26" stroke-width="1.6"/>'
 + '<rect x="95" y="142" width="8" height="8" fill="none" stroke="#2d2a26" stroke-width="1.2"/>'
 # labels
 + '<text x="68" y="127" font-family="Inter,sans-serif" font-size="11" fill="#2d2a26" text-anchor="middle">9 tiles</text>'
 + '<text x="131" y="190" font-family="Inter,sans-serif" font-size="11" fill="#2d2a26" text-anchor="middle">16 tiles</text>'
 + '<text x="158" y="90" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#2d2a26" text-anchor="middle">? tiles</text>'
 + '<text x="102" y="127" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="#2d2a26">3</text>'
 + '<text x="128" y="146" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="#2d2a26" text-anchor="middle">4</text>'
 + '</svg>'
)

req = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + LID + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]

op = pd["guided"]["opener"]
op["display"] = svg + '<span style="font-size:0.8rem;font-weight:400">Short sides 3 and 4, a tiled square on every side.</span>'

tmp = os.path.join(HERE, "_geo_l05_fixed.json")
io.open(tmp, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, os.path.join(HERE, "_validate_guided.py"), tmp], capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    sys.exit("validator failed; not patching")

req = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + LID, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json; charset=utf-8", "Prefer": "return=minimal"},
    data=json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8"))
urllib.request.urlopen(req)
print("PATCHED geometry-L05 opener with tiled-squares SVG")
