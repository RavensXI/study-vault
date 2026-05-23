"""Re-verify the audit's 'broken' URLs with a realistic browser User-Agent.

The main audit uses a bot UA + HEAD, which Britannica / HistoryExtra / Spartacus /
BBC bot-block (returning 403/404 even for real pages). This re-checks each flagged
URL with a browser UA via GET (following redirects) and writes a FILTERED audit
report containing only URLs that are genuinely dead (404/410/451/cert errors) — safe
to feed to _strip_broken_related_media_urls.py.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

AUDIT = Path("scripts/_fact_check/history-eduqas_url_audit.json")
OUT = Path("scripts/_fact_check/history-eduqas_url_audit_confirmed_dead.json")

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}
TIMEOUT = 15
DEAD_CODES = {404, 410, 451}


def recheck(url):
    try:
        r = requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=HEADERS, stream=True)
        code = r.status_code
        r.close()
        return (url, code)
    except Exception as e:
        return (url, f"err:{str(e)[:50]}")


def main():
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    broken = data.get("broken", [])
    urls = []
    seen = set()
    for b in broken:
        u = b.get("url")
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    print(f"Re-checking {len(urls)} flagged URLs with a browser UA...\n")

    results = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(recheck, u): u for u in urls}
        for f in as_completed(futs):
            u, code = f.result()
            results[u] = code

    alive = []
    dead = []
    ambiguous = []
    for u, code in results.items():
        if isinstance(code, int) and code < 400:
            alive.append((u, code))
        elif isinstance(code, int) and code in DEAD_CODES:
            dead.append((u, code))
        else:
            ambiguous.append((u, code))

    print(f"ALIVE (false positives, KEEP): {len(alive)}")
    print(f"CONFIRMED DEAD (404/410/451, STRIP): {len(dead)}")
    print(f"AMBIGUOUS (403/429/timeout/err — keep, likely bot-block): {len(ambiguous)}")
    print()
    print("=== CONFIRMED DEAD ===")
    for u, c in sorted(dead):
        print(f"  [{c}] {u}")
    print()
    print("=== AMBIGUOUS (kept) ===")
    from collections import Counter
    amb_dom = Counter()
    for u, c in ambiguous:
        from urllib.parse import urlparse
        amb_dom[urlparse(u).netloc.replace("www.", "")] += 1
    for h, n in amb_dom.most_common():
        print(f"  {h}: {n}")

    # Write filtered report: only confirmed-dead entries, same schema as audit.
    dead_set = {u for u, _ in dead}
    filtered = dict(data)
    filtered["broken"] = [b for b in broken if b.get("url") in dead_set]
    filtered["broken_count"] = len(filtered["broken"])
    OUT.write_text(json.dumps(filtered, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nFiltered confirmed-dead report -> {OUT}  ({len(filtered['broken'])} entries)")


if __name__ == "__main__":
    main()
