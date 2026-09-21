"""Put traffic-light categories in the order their colours mean.

practice.html's renderTL() colours the legend by the ORDER a category first appears in
statements[], against a fixed palette: green, amber, red. Nothing keys the colour to the
category's meaning, so a question whose first statement happens to be the false one puts the
GREEN dot on "false" and the amber one on "true" (Tom found it on the 1EN2 Paper 1 Reading
lesson 1, 21 Sep 2026: the key read green/red/amber against green/amber/red dots).

This reorders statements[] so the affirmative category comes first, any hedged category
second and the negative one last. Statement order is not otherwise meaningful — renderTL
shuffles a copy for display — so only the legend changes. Colour-word category names
("green", "amber", "red") are also renamed to what they mean, since the renderer will not
honour them and a legend reading "Red" beside an amber dot is worse than no colour at all.

  python scripts/_fix_traffic_light_order.py --dry
  python scripts/_fix_traffic_light_order.py --apply [--include-pending]
"""
import io, json, os, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "_backup_traffic_light_%s.json" % time.strftime("%Y-%m-%d"))

NEG = ("not ", "no ", "false", "unsupported", "stretch", "misleading", "wrong", "inaccurate", "incorrect")
MID = ("part", "some", "arguable", "maybe", "depends", "partially")
COLOUR = {"green": "true", "amber": "partly true", "red": "false", "yellow": "partly true"}

def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()

def rank(cat):
    c = str(cat).lower()
    if any(w in c for w in NEG): return 2
    if any(w in c for w in MID): return 1
    return 0

def fix(q):
    """Returns True if the problem changed."""
    sts = q.get("statements")
    if not isinstance(sts, list) or len(sts) < 2: return False
    before = json.dumps(sts, ensure_ascii=False)
    for s in sts:
        if isinstance(s, dict):
            lo = str(s.get("correct", "")).lower()
            if lo in COLOUR: s["correct"] = COLOUR[lo]
    cats = []
    for s in sts:
        c = s.get("correct") if isinstance(s, dict) else None
        if isinstance(c, str) and c not in cats: cats.append(c)
    # only touch two- or three-way judgements; a 4+ category sort has no colour meaning
    if not (2 <= len(cats) <= 3):
        return json.dumps(sts, ensure_ascii=False) != before
    ranks = [rank(c) for c in cats]
    if len(set(ranks)) < 2:
        return json.dumps(sts, ensure_ascii=False) != before      # nothing to order by
    q["statements"] = sorted(sts, key=lambda s: (rank(s.get("correct")), str(s.get("correct"))))
    return json.dumps(q["statements"], ensure_ascii=False) != before

def main():
    apply = "--apply" in sys.argv
    pending = "--include-pending" in sys.argv
    only = sys.argv[sys.argv.index("--subject") + 1] if "--subject" in sys.argv else None
    rows, off = [], 0
    while True:
        page = get("lessons?select=id,title,lesson_number,status,practice_data,units!inner(slug,subjects!inner(slug))"
                   "&practice_data=not.is.null&order=id&limit=500&offset=%d" % off)
        rows += page
        if len(page) < 500: break
        off += 500
    backup, nq, nl = {}, 0, 0
    for r in rows:
        if only and r["units"]["subjects"]["slug"] != only: continue
        if r["status"] != "live" and not (pending or only): continue
        pd = r["practice_data"] or {}
        pb = pd.get("problem_bank")
        if not isinstance(pb, dict): continue
        before = json.dumps(pd, ensure_ascii=False)
        n = 0
        for tier, qs in pb.items():
            if not isinstance(qs, list): continue
            for q in qs:
                if isinstance(q, dict) and q.get("input_type") == "traffic_light" and fix(q): n += 1
        if not n: continue
        nl += 1; nq += n
        print("  %-28s %-22s L%-3s %-34s %d" % (r["units"]["subjects"]["slug"], r["units"]["slug"],
                                                r["lesson_number"], r["title"][:34], n))
        backup[r["id"]] = json.loads(before)
        if apply: patch("lessons?id=eq." + r["id"], {"practice_data": pd})
    if backup and apply:
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup, indent=1, ensure_ascii=False))
        print("backup written:", BACKUP)
    print("%d traffic-light problems in %d lessons%s" % (nq, nl, "" if apply else "  (dry run)"))

if __name__ == "__main__":
    main()
