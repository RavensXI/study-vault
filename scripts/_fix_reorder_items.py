"""Repair `reorder` problems whose items are objects instead of strings.

renderReorder() does `p.items.map(function(item,i){return {text:item, origIdx:i}})` and the
checker reads `p.correct_order` as a list of indices into `p.items`. Six live problems on
english-language store items as `{text, correct_position}` objects with no correct_order, so
every item renders as "[object Object]" and the check throws.

Converted to the contract: items become the plain strings in their correct sequence, and
correct_order becomes the identity order. renderReorder shuffles a copy for display, so the
student still gets a genuine ordering task.

  python scripts/_fix_reorder_items.py --dry
  python scripts/_fix_reorder_items.py --apply
"""
import io, json, os, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "_backup_reorder_%s.json" % time.strftime("%Y-%m-%d"))

def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()

def fix(q):
    items = q.get("items")
    if not isinstance(items, list) or not items: return False
    if all(isinstance(x, str) for x in items) and isinstance(q.get("correct_order"), list): return False
    rows = []
    for i, x in enumerate(items):
        if isinstance(x, str): rows.append((i, x))
        elif isinstance(x, dict):
            pos = x.get("correct_position", x.get("position", i))
            rows.append((pos if isinstance(pos, int) else i, x.get("text", "")))
        else: return False
    if not all(t for _, t in rows): return False
    rows.sort(key=lambda r: r[0])
    q["items"] = [t for _, t in rows]
    q["correct_order"] = list(range(len(rows)))
    return True

def main():
    apply = "--apply" in sys.argv
    rows, off = [], 0
    while True:
        page = get("lessons?select=id,title,lesson_number,status,practice_data,units!inner(slug,subjects!inner(slug))"
                   "&practice_data=not.is.null&status=eq.live&order=id&limit=500&offset=%d" % off)
        rows += page
        if len(page) < 500: break
        off += 500
    backup, nq, nl = {}, 0, 0
    for r in rows:
        pd = r["practice_data"] or {}
        pb = pd.get("problem_bank")
        if not isinstance(pb, dict): continue
        before = json.dumps(pd, ensure_ascii=False)
        n = 0
        for tier, qs in pb.items():
            if not isinstance(qs, list): continue
            for q in qs:
                if isinstance(q, dict) and q.get("input_type") == "reorder" and fix(q): n += 1
        if not n: continue
        nl += 1; nq += n
        print("  %-24s %-18s L%-3s %-34s %d" % (r["units"]["subjects"]["slug"], r["units"]["slug"],
                                                r["lesson_number"], r["title"][:34], n))
        backup[r["id"]] = json.loads(before)
        if apply: patch("lessons?id=eq." + r["id"], {"practice_data": pd})
    if backup and apply:
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup, indent=1, ensure_ascii=False))
        print("backup written:", BACKUP)
    print("%d reorder problems in %d lessons%s" % (nq, nl, "" if apply else "  (dry run)"))

if __name__ == "__main__":
    main()
