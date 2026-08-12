# -*- coding: utf-8 -*-
"""Site-wide audit of practice-tier question counts.

practice.html::evaluateTier passes a tier on a streak of 4 correct, OR on
>=75% once every question has been attempted. That makes the count decisive:

    0 questions  -> attempted >= total immediately, and total > 0 is false,
                    so the tier returns 'fail'. Unpassable.
    1-3          -> a streak of 4 is impossible, and 75% of 1, 2 or 3 rounds
                    up to every single one. Perfect or fail, no margin.
    4+           -> 3/4, 4/5, 5/6 all clear 75%, so one mistake is survivable.

Anything under 4 is therefore a design fault, not a style preference.

    python scripts/_audit_practice_tiers.py           summary
    python scripts/_audit_practice_tiers.py --full    every affected lesson
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

TIERS = ("bronze", "silver", "gold")


def main():
    full = "--full" in sys.argv
    sb = get_client()

    subs = sb.table("subjects").select("id,name,slug,school_id,settings,status").execute().data
    rows, no_bank = [], []
    subjects_seen = 0

    for s in subs:
        practice_units = ((s.get("settings") or {}).get("practice_units")) or []
        if not practice_units:
            continue
        units = sb.table("units").select("id,slug,name").eq("subject_id", s["id"]).execute().data
        units = [u for u in units if u["slug"] in practice_units]
        if not units:
            continue
        subjects_seen += 1
        tag = s["slug"] + ("" if not s["school_id"] else " [school]")
        for u in units:
            for l in sb.table("lessons").select("lesson_number,title,status,practice_data") \
                    .eq("unit_id", u["id"]).order("lesson_number").execute().data:
                bank = (l.get("practice_data") or {}).get("problem_bank")
                if not isinstance(bank, dict):
                    no_bank.append((tag, u["slug"], l["lesson_number"], type(bank).__name__))
                    continue
                counts = {t: len(bank.get(t) or []) for t in TIERS}
                rows.append((tag, u["slug"], l["lesson_number"], l["status"], counts))

    print("practice subjects audited: %d | lessons: %d" % (subjects_seen, len(rows)))
    if no_bank:
        print("lessons with no dict problem_bank: %d (skipped)" % len(no_bank))
    print()

    dead = [r for r in rows if any(r[4][t] == 0 for t in TIERS)]
    tight = [r for r in rows if all(r[4][t] > 0 for t in TIERS)
             and any(r[4][t] < 4 for t in TIERS)]
    fine = len(rows) - len(dead) - len(tight)

    print("UNPASSABLE  — at least one tier has 0 questions : %4d lessons" % len(dead))
    print("NO MARGIN   — every tier populated, but one has 1-3")
    print("              (75%% of 1, 2 or 3 means 100%%)      : %4d lessons" % len(tight))
    print("HEALTHY     — every tier has 4 or more            : %4d lessons" % fine)
    print()

    # which tier is worst, and by subject
    by_sub = {}
    for tag, us, n, st, c in dead + tight:
        by_sub.setdefault(tag, [0, 0])
        by_sub[tag][0] += 1
    for tag, us, n, st, c in rows:
        by_sub.setdefault(tag, [0, 0])
        by_sub[tag][1] += 1
    print("worst-affected subjects (affected / total lessons):")
    for tag, (bad, tot) in sorted(by_sub.items(), key=lambda kv: -kv[1][0])[:18]:
        if bad:
            print("   %-42s %3d / %-3d" % (tag, bad, tot))
    print()
    per_tier = {t: sum(1 for r in rows if r[4][t] < 4) for t in TIERS}
    print("lessons with fewer than 4 questions, by tier:", per_tier)

    if full:
        print()
        print("=== every affected lesson ===")
        for tag, us, n, st, c in sorted(dead + tight):
            flag = "DEAD " if any(c[t] == 0 for t in TIERS) else "tight"
            print("  %s %-30s %-28s L%-3d %-14s b=%d s=%d g=%d"
                  % (flag, tag[:30], us[:28], n, st, c["bronze"], c["silver"], c["gold"]))


if __name__ == "__main__":
    main()
