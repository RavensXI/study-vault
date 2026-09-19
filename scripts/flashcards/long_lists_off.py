"""Mechanical pass: switch off every active list card that asks for more items than a GCSE
student would ever be asked (more than LIST_MAX) or more than the card itself holds.
No judge; re-runnable.  python scripts/flashcards/long_lists_off.py [--dry]
"""
import io, json, os, re, sys, urllib.request
LIST_MAX = 6
NUM = {"three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json"}
def get(path): return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, headers=H), timeout=180).read())
def patch(path, body): urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + path, data=json.dumps(body).encode(), headers=dict(H, Prefer="return=minimal"), method="PATCH"), timeout=60).read()
def list_count(front):
    m = re.search(r"\b(three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\b", (front or "").lower())
    return 0 if not m else (NUM.get(m.group(1)) or int(m.group(1)))
dry = "--dry" in sys.argv
rows, off = [], 0
while True:
    page = get("lessons?select=id,recall_cards&recall_cards=not.is.null&order=id&limit=1000&offset=%d" % off); rows += page
    if len(page) < 1000: break
    off += 1000
n = 0; shown = 0
for l in rows:
    rc = l["recall_cards"] or []; changed = False
    for c in rc:
        if not c or c.get("off") or c.get("kind") != "list": continue
        items = c.get("items") or []
        if len(items) > LIST_MAX or list_count(c.get("front")) > max(len(items), LIST_MAX):
            c["off"] = True; c["why"] = "too long a list"; changed = True; n += 1
            if shown < 8: print("  OFF", c["front"][:100]); shown += 1
    if changed and not dry: patch("lessons?id=eq." + l["id"], {"recall_cards": rc})
print("long list cards switched off:", n, "(dry)" if dry else "")
