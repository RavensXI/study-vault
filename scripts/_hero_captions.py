"""Standardise hero captions: `{factual description} ({source-appropriate credit})`.
- DESCRIPTION: a Gemini vision pass reads the hero image WITH the lesson title +
  a short content snippet (so it doesn't mislabel abstract images), returns one
  short factual line.
- CREDIT: assembled deterministically from the image's source + licence
  (Wikimedia from the audit; Unsplash/R2 generic; PD named; generated = original).
Writes a tracking LEDGER (CSV, spreadsheet-friendly) so we can run this in batches
across months and always know what's done. Does NOT write to Supabase — that's a
separate, explicit step once captions are approved.

Pilot scope: SAM's History (history-ocr, 4 units). Generalises by swapping the
context file + source maps.
"""
import os, io, csv, json, re, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image

try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

def clean_artist(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    if re.match(r"(?i)unknown\s*author", s):   # Commons "Unknown author / not provided" variants
        return "Unknown author"
    n = len(s)
    if n and n % 2 == 0 and s[:n // 2].strip() == s[n // 2:].strip():  # Commons doubles the name (link text + plain)
        return s[:n // 2].strip()
    return s

def clean_desc(d):
    d = re.sub(r"^(a|an)\s+(close-?up\s+|aerial\s+|detailed\s+)?(watercolou?r|digital|pen[- ]and[- ]ink|ink|line)?\s*"
               r"(illustration|drawing|painting|sketch|image|artwork|photo(graph)?)\s+(of|showing|depicting|featuring)\s+",
               "", d, flags=re.I).strip()
    return d[:1].upper() + d[1:] if d else d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTX = json.load(open(os.path.join(ROOT, "scratch_history_caption_ctx.json"), encoding="utf-8"))
MANIFEST = json.load(open(os.path.join(ROOT, "design-lab", "_lw_manifest.json"), encoding="utf-8"))
GENERATED = set(json.load(open(os.path.join(ROOT, "design-lab", "_lw_generated.json"), encoding="utf-8")))
AUDIT = {a["url"].split("?")[0]: a for a in json.load(open(os.path.join(ROOT, "design-lab", "_wikimedia_attribution_audit.json"), encoding="utf-8"))}
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
UNIT_NAMES = {"international-relations-1918-1975": "International Relations 1918–1975",
              "germany-people-state-1925-1955": "Germany 1925–1955",
              "migration-to-britain-1000-2010": "Migration to Britain c.1000–c.2010",
              "usa-people-state-1919-1948": "The USA 1919–1948"}

def norm(u): return (u or "").split("?")[0].strip()

def source_type(url):
    n = norm(url)
    if n in GENERATED: return "generated"
    if "wikimedia.org" in n or "wikipedia.org" in n: return "wikimedia"
    if "unsplash.com" in n: return "unsplash"
    if "r2.dev" in n: return "r2"
    if not n or n.startswith("/") or not n.startswith("http"): return "relative"
    return "other"

# LINE-AND-WASH form (these heroes are the redrawn/generated versions).
# For un-redrawn live photos, swap "Illustration after a photo" -> "Photo".
def make_credit(url, lw=True):
    st = source_type(url)
    lead = "Illustration after a photo" if lw else "Photo"
    if st == "generated":
        return "StudyVault illustration", "", "generated", ""
    if st == "wikimedia":
        a = AUDIT.get(norm(url), {})
        artist = clean_artist(a.get("artist")) or "unknown artist"
        lic = a.get("license") or ""; risk = a.get("risk") or ""
        if risk == "FREE":
            return f"{lead} by {artist} · public domain · Wikimedia Commons", lic, risk, artist
        return f"{lead} by {artist} · {lic} · Wikimedia Commons", lic, risk, artist
    # unsplash / r2 / relative-non-generated
    return f"{lead} via Unsplash", "", "", ""

DESC_PROMPT = (
    "This is the hero image for a GCSE History lesson titled \"{title}\".\n"
    "{ctx}"
    "Say what the picture SHOWS in ONE short, factual sentence (max ~14 words), for a 15–16 year old student — "
    "name the concrete subject, especially if it is abstract or might be unfamiliar. "
    "Describe the SUBJECT ONLY: do NOT mention the art style, or that it is an illustration, drawing, watercolour, "
    "painting or photo. Describe only what is visible; do not infer beyond the image. "
    "No lead-in and no quotation marks. Reply with only the sentence.")

def describe(local_png, title, desc):
    img = Image.open(local_png).convert("RGB")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    part = {"inline_data": {"mime_type": "image/png", "data": buf.getvalue()}}
    ctx = (f"The lesson is about: {desc}\n" if desc else "")
    prompt = DESC_PROMPT.format(title=title, ctx=ctx)
    for _ in range(5):
        try:
            r = client.models.generate_content(model=MODEL, contents=[prompt, part])
            t = (getattr(r, "text", "") or "").strip().strip('"').split("\n")[0].strip()
            if t:
                return clean_desc(re.sub(r"\s*\.\s*$", "", t))   # drop trailing full stop, caption style
        except Exception:
            time.sleep(4)
    return ""

# build work list
work = []
for unit, lessons in CTX.items():
    for L in lessons:
        lw = MANIFEST.get(norm(L["hero"]))
        local = os.path.join(ROOT, lw.lstrip("/")) if lw else None
        work.append({"subject": "history-ocr", "unit": unit, "unitName": UNIT_NAMES.get(unit, unit),
                     "n": L["n"], "id": L["id"], "title": L["title"], "desc": L["desc"],
                     "hero": L["hero"], "local": local})

# resume: reuse descriptions already in the ledger (so monthly batches only fill gaps)
LEDGER = os.path.join(ROOT, "design-lab", "_hero_caption_ledger.csv")
prior = {}
if os.path.exists(LEDGER):
    with open(LEDGER, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            dsc = (row.get("description") or "").strip()
            if dsc and not dsc.startswith("(needs"):
                prior[row.get("lesson_id")] = dsc

def run(w):
    cred, lic, risk, artist = make_credit(w["hero"])
    d = prior.get(str(w["id"]))
    if not d:
        d = describe(w["local"], w["title"], w["desc"]) if w["local"] and os.path.exists(w["local"]) else ""
    caption = f"{d} ({cred})" if d else f"(needs description) ({cred})"
    w.update({"source_type": source_type(w["hero"]), "license": lic, "risk": risk, "artist": artist,
              "description": d, "credit": cred, "caption_final": caption,
              "art_status": "generated (original)" if source_type(w["hero"]) == "generated" else "line-and-wash"})
    return w

print(f"captioning {len(work)} History heroes…", flush=True)
done = []
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = [ex.submit(run, w) for w in work]
    for f in as_completed(futs):
        done.append(f.result())
done.sort(key=lambda x: (x["unit"], x["n"]))

# write ledger
cols = ["subject", "unit", "lesson_number", "lesson_id", "title", "hero_url", "source_type",
        "license", "license_risk", "artist", "art_status", "description", "credit",
        "caption_final", "written_to_db"]
out = os.path.join(ROOT, "design-lab", "_hero_caption_ledger.csv")
with open(out, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh); w.writerow(cols)
    for r in done:
        w.writerow([r["subject"], r["unit"], r["n"], r["id"], r["title"], norm(r["hero"]),
                    r["source_type"], r["license"], r["risk"], r["artist"], r["art_status"],
                    r["description"], r["credit"], r["caption_final"], "N"])
print("wrote", out)

# readable preview
print("\n================ CAPTION PREVIEW ================")
cur = None
for r in done:
    if r["unit"] != cur: cur = r["unit"]; print("\n### " + r["unitName"])
    print(f"  L{r['n']:>2} [{r['source_type']:9}] {r['caption_final']}")
