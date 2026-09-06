# -*- coding: utf-8 -*-
"""Mark a retro-fact-check queue item as rebuilt after an OCR cluster rebuild.

Usage: python scripts/api_build/mark_queue_rebuilt.py poetry-conflict "note text"
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QUEUE = r"C:\Users\tshau\Documents\Study Vault\scripts\_retrofc\_queue.json"


def main(unit, note):
    q = json.load(io.open(QUEUE, encoding="utf-8"))
    hits = [it for it in q["items"]
            if it.get("subject") == "english-literature-ocr" and it.get("unit") == unit]
    if len(hits) != 1:
        raise SystemExit("expected 1 queue item for %s, found %d" % (unit, len(hits)))
    it = hits[0]
    it["status"] = "rebuilt-pending-review"
    it["lessons"] = 15
    it["rebuilt_on"] = "2026-09-06"
    it["note"] = note
    io.open(QUEUE, "w", encoding="utf-8").write(json.dumps(q, ensure_ascii=False, indent=1))
    print("queue updated:", unit, "->", it["status"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
