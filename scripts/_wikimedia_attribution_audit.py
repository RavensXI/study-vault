"""READ-ONLY audit of every Wikimedia-sourced hero: recover the authoritative
artist + licence from the Commons API (keyed off the filename in the URL), compare
to the stored caption, and classify the licence risk for our ink-wash DERIVATIVE
use on a commercial product. Writes a full table + a CC BY-SA hit-list. No DB writes.
"""
import os, re, json, time, urllib.request, urllib.parse, collections
from supabase import create_client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
UA = "StudyVault/1.0 (+https://www.studyvault.co.uk; studyvault.info@gmail.com)"

# --- gather unique Wikimedia heroes ---
rows = []; start = 0
while True:
    d = sb.table("lessons").select("hero_image_url,hero_image_caption").range(start, start + 999).execute().data
    if not d: break
    rows.extend(d); start += 1000
    if len(d) < 1000: break
seen = {}
for r in rows:
    u = (r.get("hero_image_url") or "")
    if "wikimedia.org" in u or "wikipedia.org" in u:
        k = u.split("?")[0]
        if k not in seen: seen[k] = r.get("hero_image_caption")

def filename(url):
    parts = url.split("?")[0].split("/")
    fn = parts[-2] if "/thumb/" in url else parts[-1]   # thumb urls end with the rendition
    return urllib.parse.unquote(fn)

def norm_title(t):
    return urllib.parse.unquote(t).replace(" ", "_")

def strip(s): return re.sub("<[^>]+>", "", s or "").strip()

def commons_batch(filenames):
    titles = "|".join("File:" + f for f in filenames)
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "extmetadata", "titles": titles})
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    d = json.loads(urllib.request.urlopen(req, timeout=40).read())
    q = d.get("query", {})
    norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
    out = {}
    for _, p in q.get("pages", {}).items():
        title = p.get("title", "")
        em = (p.get("imageinfo", [{}])[0] or {}).get("extmetadata", {}) if p.get("imageinfo") else {}
        out[title] = {
            "artist": strip((em.get("Artist", {}) or {}).get("value", "")),
            "license": strip((em.get("LicenseShortName", {}) or {}).get("value", "")),
            "license_url": (em.get("LicenseUrl", {}) or {}).get("value", ""),
            "credit": strip((em.get("Credit", {}) or {}).get("value", "")),
            "missing": "missing" in p,
        }
    return out, norm

def risk_of(lic):
    l = (lic or "").lower()
    if not l: return "UNKNOWN"
    if "sa" in l.replace("-", "") and "cc" in l: return "SHARE-ALIKE"   # CC BY-SA
    if "gfdl" in l or "gnu" in l: return "COPYLEFT"
    if "nc" in l.split() or "noncommercial" in l: return "NONCOMMERCIAL"
    if l.startswith("cc by") or "attribution" in l: return "ATTRIB-REQUIRED"  # CC BY (no SA)
    if "public domain" in l or "cc0" in l or "no restrictions" in l or "pd" == l: return "FREE"
    return "OTHER"

items = list(seen.items())
print(f"auditing {len(items)} unique Wikimedia heroes via Commons (batched)…", flush=True)
report = []
fn_to_url = {}
for url, cap in items:
    fn_to_url.setdefault(filename(url), (url, cap))
fns = list(fn_to_url.keys())
data = {}
for i in range(0, len(fns), 45):
    chunk = fns[i:i + 45]
    try:
        out, norm = commons_batch(chunk)
        for fn in chunk:
            title = "File:" + fn
            title = norm.get(title, title)
            data[fn] = out.get(title) or out.get("File:" + norm_title(fn)) or {"artist": "", "license": "", "missing": True}
    except Exception as e:
        for fn in chunk: data[fn] = {"artist": "", "license": "ERR", "err": str(e)[:50]}
    time.sleep(0.4)
    print(f"  {min(i+45,len(fns))}/{len(fns)}", flush=True)

lic_tally = collections.Counter(); risk_tally = collections.Counter()
for fn, (url, cap) in fn_to_url.items():
    info = data.get(fn, {})
    lic = info.get("license", ""); r = risk_of(lic)
    lic_tally[lic or "(none)"] += 1; risk_tally[r] += 1
    report.append({"url": url, "filename": fn, "old_caption": cap, "artist": info.get("artist", ""),
                   "license": lic, "license_url": info.get("license_url", ""), "risk": r,
                   "suggested_credit": (info.get("artist", "") + (" / " + lic if lic else "")) or info.get("credit", "")})

json.dump(report, open(os.path.join(ROOT, "design-lab", "_wikimedia_attribution_audit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("\n=== LICENCE DISTRIBUTION (", len(report), "Wikimedia heroes) ===")
for k, n in lic_tally.most_common(): print(f"  {n:4d}  {k}")
print("\n=== RISK BUCKETS (for ink-wash derivative on a commercial product) ===")
for k in ["FREE", "ATTRIB-REQUIRED", "SHARE-ALIKE", "COPYLEFT", "NONCOMMERCIAL", "OTHER", "UNKNOWN"]:
    if risk_tally.get(k): print(f"  {risk_tally[k]:4d}  {k}")
print("\nwrote design-lab/_wikimedia_attribution_audit.json")
