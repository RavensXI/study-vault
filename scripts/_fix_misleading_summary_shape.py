"""Repair live misleading_summary problems that cannot render.

practice.html's renderMS() reads only p.summaryParts. 20 live problems across the three
English Language subjects still carry the older `statements` shape, so renderMS throws on
undefined, the question shows no options, and the next problem's markup bleeds into the same
card (Tom saw it on english-language-edexcel/paper-1-writing/2 Q6, 21 Sep 2026).

Each statement becomes a summaryPart: text kept verbatim, `misleading` inverted into `wrong`,
`explain` carried over. A backup of every practice_data touched is written first.

  python scripts/_fix_misleading_summary_shape.py --dry     # report only
  python scripts/_fix_misleading_summary_shape.py --apply
"""
import io, json, os, sys, time, urllib.request

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, "_backup_misleading_summary_%s.json" % time.strftime("%Y-%m-%d"))

def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body):
    urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(),
        headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=120).read()

def convert(q):
    """statements[] or options[] -> summaryParts[]; returns True if it changed.

    Two older shapes exist: `statements` (Edexcel, OCR) and `options` (Eduqas). Both hold
    {text, misleading} objects; only the key differs."""
    if q.get("summaryParts"):
        return False
    src = q.get("statements") or q.get("options")
    if not src:
        return False
    parts = []
    for s in src:
        if not isinstance(s, dict):
            return False
        part = {"text": s.get("text", ""), "wrong": bool(s.get("misleading") or s.get("wrong"))}
        if s.get("explain"):
            part["explain"] = s["explain"]
        parts.append(part)
    if not parts or not any(p["text"] for p in parts):
        return False
    q["summaryParts"] = parts
    q.pop("statements", None)
    q.pop("options", None)
    if q.get("explanation") and not any(p.get("explain") for p in parts):
        parts[0]["explain"] = q.pop("explanation")   # Eduqas keeps one explanation for the set
    return True

def main():
    apply = "--apply" in sys.argv
    rows = []
    off = 0
    while True:
        page = get("lessons?select=id,title,lesson_number,practice_data,units!inner(slug,subjects!inner(slug))"
                   "&practice_data=not.is.null&status=eq.live&order=id&limit=500&offset=%d" % off)
        rows += page
        if len(page) < 500:
            break
        off += 500
    backup, fixed, lessons = {}, 0, 0
    for r in rows:
        pd = r["practice_data"] or {}
        pb = pd.get("problem_bank")
        if not isinstance(pb, dict):
            continue
        before = json.dumps(pd, ensure_ascii=False)
        n = 0
        for tier, qs in pb.items():
            if not isinstance(qs, list):
                continue
            for q in qs:
                if isinstance(q, dict) and q.get("input_type") == "misleading_summary" and convert(q):
                    n += 1
        if not n:
            continue
        lessons += 1; fixed += n
        print("  %-26s %-22s L%-3s %-38s %d problem(s)" % (
            r["units"]["subjects"]["slug"], r["units"]["slug"], r["lesson_number"], r["title"][:38], n))
        backup[r["id"]] = json.loads(before)
        if apply:
            patch("lessons?id=eq." + r["id"], {"practice_data": pd})
    if backup and apply:
        io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(backup, indent=1, ensure_ascii=False))
        print("backup written:", BACKUP)
    print("%d problems in %d lessons%s" % (fixed, lessons, "" if apply else "  (dry run, nothing written)"))

if __name__ == "__main__":
    main()
