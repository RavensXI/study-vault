# -*- coding: utf-8 -*-
"""Mark a retro-fact-check queue item as rebuilt after a unit rebuild.

Usage:
  python scripts/api_build/mark_queue_rebuilt.py <unit> "note"                 # english-literature-ocr, 15 lessons
  python scripts/api_build/mark_queue_rebuilt.py <subject> <unit> <lessons> "note"
"""
import io
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QUEUE = r"C:\Users\tshau\Documents\Study Vault\scripts\_retrofc\_queue.json"


def main(subject, unit, lessons, note):
    q = json.load(io.open(QUEUE, encoding="utf-8"))
    hits = [it for it in q["items"]
            if it.get("subject") == subject and it.get("unit") == unit]
    if len(hits) != 1:
        raise SystemExit("expected 1 queue item for %s/%s, found %d"
                         % (subject, unit, len(hits)))
    it = hits[0]
    it["status"] = "rebuilt-pending-review"
    it["lessons"] = lessons
    it["rebuilt_on"] = time.strftime("%Y-%m-%d")
    it["note"] = note
    io.open(QUEUE, "w", encoding="utf-8").write(json.dumps(q, ensure_ascii=False, indent=1))
    print("queue updated:", subject, unit, "->", it["status"])


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2:
        main("english-literature-ocr", a[0], 15, a[1])
    elif len(a) == 4:
        main(a[0], a[1], int(a[2]), a[3])
    else:
        raise SystemExit(__doc__)
