# -*- coding: utf-8 -*-
"""Repair ratio-proportion-L01: the revision agent PATCHed with double-encoded
UTF-8 (utf-8 bytes read as cp1252 and re-encoded). The checker verified all
maths is correct, so this is a pure text repair: cp1252-encode then utf-8
decode every corrupted string, recursively. Validates before PATCHing."""
import json, io, os, sys, subprocess, urllib.request

sys.stdout.reconfigure(errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = json.load(io.open(os.path.join(HERE, "_worklist.json"), encoding="utf-8"))["ratio-proportion-L01"]["id"]

MARKERS = ("Ã", "Â", "âˆ", "â€")  # Ã Â âˆ â€

def demojibake(s):
    if not any(m in s for m in MARKERS):
        return s, False
    try:
        fixed = s.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s, False
    # accept only if it actually removed mojibake and didn't create new
    if any(m in fixed for m in MARKERS):
        # may be double-double encoded; try once more
        try:
            fixed2 = fixed.encode("cp1252").decode("utf-8")
            if not any(m in fixed2 for m in MARKERS):
                return fixed2, True
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return fixed, True

count = [0]
def walk(o):
    if isinstance(o, dict):
        return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    if isinstance(o, str):
        fixed, changed = demojibake(o)
        if changed:
            count[0] += 1
        return fixed
    return o

req = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + LID + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]

fixed = walk(pd)
print("strings repaired:", count[0])

blob = json.dumps(fixed, ensure_ascii=False)
for m in MARKERS:
    assert m not in blob, "mojibake marker still present: " + repr(m)
tmp = os.path.join(HERE, "_rp_l01_fixed.json")
io.open(tmp, "w", encoding="utf-8").write(json.dumps(fixed, ensure_ascii=False, indent=1))

r = subprocess.run([sys.executable, os.path.join(HERE, "_validate_guided.py"), tmp],
                   capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    print(r.stderr)
    sys.exit("validator failed; NOT patching")

req = urllib.request.Request(SUPA + "/rest/v1/lessons?id=eq." + LID, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json; charset=utf-8", "Prefer": "return=minimal"},
    data=json.dumps({"practice_data": fixed}, ensure_ascii=False).encode("utf-8"))
urllib.request.urlopen(req)
print("PATCHED ratio-proportion-L01 with repaired encoding")
