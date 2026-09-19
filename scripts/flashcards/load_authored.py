"""Load the passing cards of one or more gated files into lessons.recall_cards, replacing any
earlier authored cards on those lessons (re-runnable).
  python scripts/flashcards/load_authored.py scripts/flashcards/_authored/unity__history.gated.json [...]
"""
import io, json, os, sys, urllib.request
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=60).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=60).read()
added = held = 0; lessons = 0
for src in sys.argv[1:]:
    cards = json.load(io.open(src, encoding="utf-8"))
    by = {}
    for c in cards:
        if c.get("gate") != "pass": held += 1; continue
        by.setdefault(c["lesson_id"], []).append({k: c[k] for k in ("kind", "front", "answer", "items", "tier", "src") if c.get(k) is not None})
    for lid, new in by.items():
        cur = get("lessons?select=recall_cards&id=eq." + lid)[0]["recall_cards"] or []
        keep = [c for c in cur if c.get("src") != "authored"]; fronts = {c["front"] for c in keep}
        merged = keep + [c for c in new if c["front"] not in fronts]
        patch("lessons?id=eq." + lid, {"recall_cards": merged}); added += len(merged) - len(keep); lessons += 1
    print(os.path.basename(src), "loaded")
print("authored cards loaded:", added, "| held back:", held, "| lessons:", lessons)
