"""Tile answers the page marks wrong although the student built the key's exact text (26 Sep 2026).

reorder compares item POSITIONS (items[shuffIdx].origIdx === correct_order[pos]), and vocab_match
ties each label to one pair id, so when two tiles show the same text ('a' and 'a', 'en' and 'en', two
'I would like' labels) a pupil who picks the other identical tile is marked wrong. That is a page
fault, not a key fault: these findings are relabelled "renderer_fault" so they never become fix drafts,
and listed in scripts/_studentwalk_renderer_faults.md.

  python scripts/_studentwalk_renderer_faults.py <walk dir name> [...]
"""
import io, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
OUT = os.path.join(HERE, "_studentwalk_renderer_faults.md")


def get(q):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + q, headers=H), timeout=120).read())


def norm(s):
    return " ".join(str(s).split())


def main(dirs):
    rows = []
    for d in dirs:
        p = os.path.join(HERE, "_studentwalk_" + d)
        if not os.path.exists(os.path.join(p, "adjudications.json")): continue
        v = json.load(io.open(os.path.join(p, "views.json"), encoding="utf-8"))
        at = json.load(io.open(os.path.join(p, "attempts.json"), encoding="utf-8"))
        m = json.load(io.open(os.path.join(p, "marks.json"), encoding="utf-8"))
        adj = json.load(io.open(os.path.join(p, "adjudications.json"), encoding="utf-8"))
        cache, changed = {}, 0
        for k, x in m.items():
            t = v[k]["type"]
            if x.get("verdict") == "right" or t not in ("reorder", "vocab_match"): continue
            lid = v[k].get("lesson_id")
            if lid not in cache: cache[lid] = get("lessons?select=practice_data&id=eq.%s" % lid)[0]["practice_data"]
            q = cache[lid]["problem_bank"][v[k]["tier"]][v[k]["i"]]
            ans = (at.get(k) or {}).get("answer")
            fault = False
            if t == "reorder":
                key = [norm(q["items"][i]) for i in q.get("correct_order") or []]
                dup = len(set(map(norm, q["items"]))) < len(q["items"])
                fault = dup and isinstance(ans, list) and [norm(a) for a in ans] == key
            else:
                pairs = q.get("pairs") or []
                rights = [norm(pr["right"]) for pr in pairs]; lefts = [norm(pr["left"]) for pr in pairs]
                dup = len(set(rights)) < len(rights) or len(set(lefts)) < len(lefts)
                ok = {(norm(pr["left"]), norm(pr["right"])) for pr in pairs}
                fault = dup and isinstance(ans, list) and ans and all((norm(a.get("left")), norm(a.get("right"))) in ok for a in ans if isinstance(a, dict))
            if fault:
                was = (adj.get(k) or {}).get("finding")
                adj[k] = dict(adj.get(k) or {}, finding="renderer_fault", was=was,
                              why="The student built the key's exact text, but two tiles show the same text and the page compares "
                                  "tile positions, so picking the other identical tile is marked wrong. Page fault, not a key fault.")
                rows.append((d, k, t)); changed += 1
        if changed:
            io.open(os.path.join(p, "adjudications.json"), "w", encoding="utf-8").write(json.dumps(adj, ensure_ascii=False, indent=1))
    old = io.open(OUT, encoding="utf-8").read().splitlines() if os.path.exists(OUT) else []
    have = set(old)
    new = ["- %s — `%s` (%s)" % r for r in rows]
    lines = (old or ["# Practice walk: page faults on identical tiles", "",
                     "reorder compares tile positions and vocab_match ties each label to one pair, so when two tiles show the",
                     "same text a correct answer built with the other identical tile is marked wrong. Code fix, not a data fix.", ""])
    lines += [l for l in new if l not in have]
    io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("renderer faults relabelled: %d" % len(rows))


if __name__ == "__main__":
    main(sys.argv[1:])
