"""FULL-PLATFORM hero captions. One master ledger over every UNIQUE hero image
(deduped — describe once, reuse across lessons that share it). Descriptions are
cheap (Gemini flash vision) so we do them ALL now; only the Pro image regen is
chipped across months.

  python _hero_captions_full.py            # backbone only: classify every hero, assemble credit (instant)
  python _hero_captions_full.py --describe # + run the vision description pass (resumable, long)

Ledger: design-lab/_hero_caption_ledger_full.csv  (UTF-8 BOM, resumable off itself)
Reads-only against Supabase. No caption is written to the DB here.
"""
import os, io, csv, json, re, sys, time, hashlib, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image
from supabase import create_client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
LEDGER = os.path.join(ROOT, "design-lab", "_hero_caption_ledger_full.csv")
AUDIT = {a["url"].split("?")[0]: a for a in json.load(open(os.path.join(ROOT, "design-lab", "_wikimedia_attribution_audit.json"), encoding="utf-8"))}
MANIFEST = json.load(open(os.path.join(ROOT, "design-lab", "_lw_manifest.json"), encoding="utf-8"))
GENERATED = set(json.load(open(os.path.join(ROOT, "design-lab", "_lw_generated.json"), encoding="utf-8")))
UA = "StudyVault/1.0 (+https://www.studyvault.co.uk; studyvault.info@gmail.com)"
DESCRIBE = "--describe" in sys.argv

def norm(u): return (u or "").split("?")[0].strip()

def clean_artist(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    if re.match(r"(?i)unknown\s*author", s): return "Unknown author"
    n = len(s)
    if n and n % 2 == 0 and s[:n // 2].strip() == s[n // 2:].strip(): return s[:n // 2].strip()
    return s

def clean_desc(d):
    d = re.sub(r"^(a|an)\s+(close-?up\s+|aerial\s+|detailed\s+)?(watercolou?r|digital|pen[- ]and[- ]ink|ink|line)?\s*"
               r"(illustration|drawing|painting|sketch|image|artwork|photo(graph)?)\s+(of|showing|depicting|featuring)\s+",
               "", d, flags=re.I).strip()
    return d[:1].upper() + d[1:] if d else d

def source_type(nu):
    if nu in GENERATED: return "generated"
    if "wikimedia.org" in nu or "wikipedia.org" in nu: return "wikimedia"
    if "unsplash.com" in nu: return "unsplash"
    if "r2.dev" in nu: return "r2"
    if not nu or nu.startswith("/") or not nu.startswith("http"): return "relative"
    return "other"

def art_status(nu):
    if nu in GENERATED: return "generated (original)"
    if nu in MANIFEST: return "line-and-wash"
    return "photo"

def make_credit(nu):
    st = source_type(nu); ast = art_status(nu)
    lead = "Illustration after a photo" if ast == "line-and-wash" else "Photo"
    if ast == "generated (original)": return "StudyVault illustration", "", "generated", ""
    if st == "wikimedia":
        a = AUDIT.get(nu, {}); artist = clean_artist(a.get("artist")) or "unknown artist"
        lic = a.get("license") or ""; risk = a.get("risk") or ""
        if risk == "FREE": return f"{lead} by {artist} · public domain · Wikimedia Commons", lic, risk, artist
        return f"{lead} by {artist} · {lic} · Wikimedia Commons", lic, risk, artist
    return f"{lead} via Unsplash", "", "", ""

# ---- gather lessons → unique heroes ----
print("querying lessons…", flush=True)
rows = []; start = 0
while True:
    d = sb.table("lessons").select("id,lesson_number,title,description,hero_image_url,units!inner(slug,subjects!inner(slug,school_id))").range(start, start + 999).execute().data
    if not d: break
    rows.extend(d); start += 1000
    if len(d) < 1000: break
heroes = {}
for r in rows:
    nu = norm(r.get("hero_image_url"))
    if not nu: continue
    h = heroes.setdefault(nu, {"full": r.get("hero_image_url"), "title": r["title"],
                               "desc": (r.get("description") or "")[:240],
                               "subject": r["units"]["subjects"]["slug"], "count": 0})
    h["count"] += 1
print(f"{len(rows)} lessons → {len(heroes)} unique heroes", flush=True)

# ---- resume: prior descriptions from the full ledger AND the History pilot ledger ----
prior = {}
for path in (LEDGER, os.path.join(ROOT, "design-lab", "_hero_caption_ledger.csv")):
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                u = norm(row.get("hero_url")); dsc = (row.get("description") or "").strip()
                if u and dsc and not dsc.startswith("(needs"):
                    prior.setdefault(u, dsc)
print(f"{len(prior)} descriptions already on record (resume)", flush=True)

DESC_PROMPT = (
    "This is the hero image for a GCSE {subject} lesson titled \"{title}\".\n{ctx}"
    "Say what the picture SHOWS in ONE short, factual sentence (max ~14 words), for a 15–16 year old student — "
    "name the concrete subject, especially if it is abstract or might be unfamiliar. Describe the SUBJECT ONLY: do "
    "NOT mention the art style, or that it is an illustration, drawing, watercolour, painting or photo. Describe "
    "only what is visible; do not infer beyond the image. No lead-in and no quotation marks. Reply with only the sentence.")

def fetch_image(nu, full):
    if nu in MANIFEST:                                   # already line-and-washed locally
        p = os.path.join(ROOT, MANIFEST[nu].lstrip("/"))
        if os.path.exists(p): return Image.open(p).convert("RGB")
    if not full or not full.startswith("http"): return None
    full = full.replace(" ", "%20")              # some R2 paths have raw spaces → urllib rejects them
    if "wikimedia.org" in full or "wikipedia.org" in full: time.sleep(1.3)
    req = urllib.request.Request(full, headers={"User-Agent": UA})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())).convert("RGB")
    if im.width > 768: im = im.resize((768, round(im.height * 768 / im.width)))
    return im

def describe(nu, full, subject, title, desc):
    im = None
    for attempt in range(3):                       # fetch with retry; 404/410 = permanently dead URL
        try:
            im = fetch_image(nu, full); break
        except urllib.error.HTTPError as e:
            if e.code in (404, 410): return "__DEAD__"
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    if im is None: return ""
    buf = io.BytesIO(); im.save(buf, format="JPEG", quality=85)
    part = {"inline_data": {"mime_type": "image/jpeg", "data": buf.getvalue()}}
    ctx = (f"The lesson is about: {desc}\n" if desc else "")
    prompt = DESC_PROMPT.format(subject=subject.replace("-", " ").title(), title=title, ctx=ctx)
    delay = 2
    for _ in range(6):                             # back off on throttle AND on empty responses
        try:
            r = client.models.generate_content(model=MODEL, contents=[prompt, part])
            t = (getattr(r, "text", "") or "").strip().strip('"').split("\n")[0].strip()
            if t: return clean_desc(re.sub(r"\s*\.\s*$", "", t))
        except Exception as e:
            if any(k in str(e) for k in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")): delay = min(delay * 2, 30)
        time.sleep(delay); delay = min(int(delay * 1.6) + 1, 30)
    return ""

COLS = ["hero_url", "source_type", "license", "license_risk", "artist", "art_status",
        "lesson_count", "sample_subject", "sample_title", "description", "credit",
        "caption_final", "written_to_db"]

def assemble(nu, h, description):
    cred, lic, risk, artist = make_credit(nu)
    cap = f"{description} ({cred})" if description else f"(needs description) ({cred})"
    return {"hero_url": nu, "source_type": source_type(nu), "license": lic, "license_risk": risk,
            "artist": artist, "art_status": art_status(nu), "lesson_count": h["count"],
            "sample_subject": h["subject"], "sample_title": h["title"], "description": description,
            "credit": cred, "caption_final": cap, "written_to_db": "N"}

def write_ledger(records):
    with open(LEDGER, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh); w.writerow(COLS)
        for r in records: w.writerow([r[c] for c in COLS])

items = sorted(heroes.items(), key=lambda kv: (kv[1]["subject"], kv[1]["title"]))
if not DESCRIBE:
    recs = [assemble(nu, h, prior.get(nu, "")) for nu, h in items]
    write_ledger(recs)
    import collections
    print("backbone written:", LEDGER, flush=True)
    print("  by source:", dict(collections.Counter(r["source_type"] for r in recs)))
    print("  with description already:", sum(1 for r in recs if r["description"]), "/", len(recs))
    sys.exit(0)

# describe pass (resumable). Skip ones already done AND ones already known dead.
DEADPATH = os.path.join(ROOT, "design-lab", "_dead_hero_urls.json")
dead = set(json.load(open(DEADPATH, encoding="utf-8"))) if os.path.exists(DEADPATH) else set()
todo = [(nu, h) for nu, h in items if not prior.get(nu) and nu not in dead]
print(f"describing {len(todo)} heroes ({len(items)-len(todo)} already done/dead)…", flush=True)
results = dict(prior)
done = 0; lock_every = 50
def work(nu, h):
    return nu, describe(nu, h["full"], h["subject"], h["title"], h["desc"])
with ThreadPoolExecutor(max_workers=2) as ex:
    futs = [ex.submit(work, nu, h) for nu, h in todo]
    for f in as_completed(futs):
        nu, dsc = f.result(); done += 1
        if dsc == "__DEAD__":
            dead.add(nu); dsc = ""
        results[nu] = dsc
        if done % lock_every == 0:
            write_ledger([assemble(nu2, h2, results.get(nu2, "")) for nu2, h2 in items])   # checkpoint
            json.dump(sorted(dead), open(DEADPATH, "w", encoding="utf-8"), indent=1)
            fld = sum(1 for nu2, h2 in items if results.get(nu2))
            print(f"  {done}/{len(todo)} done | filled {fld} | dead {len(dead)}", flush=True)
write_ledger([assemble(nu, h, results.get(nu, "")) for nu, h in items])
json.dump(sorted(dead), open(DEADPATH, "w", encoding="utf-8"), indent=1)
blank = sum(1 for nu, h in items if not results.get(nu))
print(f"done — {len(items)-blank}/{len(items)} described | {len(dead)} dead URLs | {blank-len(dead)} transient-blank (re-run to retry)", flush=True)
