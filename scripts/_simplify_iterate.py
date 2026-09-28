"""Iterate the Simplify-wording prompt for Sonnet 5.5 until it passes the live QA check every time
(Tom, 28 Sep 2026: "iterate on the prompt until those failures don't happen… 30 in a row").

Two fixed sets of 30 real lesson paragraphs, drawn once from live free-tier lessons (seeded):
  dev      — the prompt is tuned against these
  holdout  — never looked at while tuning; the final "30 in a row" is measured here
Writer: claude-sonnet-5-5. Judge: claude-sonnet-4-6 with api/_lib/simplify-prompt-qa.txt (the live QA).
Both through the Claude Code subscription (lesson text only; no pupil data).

  python scripts/_simplify_iterate.py sets                 build the two sets (once)
  python scripts/_simplify_iterate.py run dev|holdout TAG  -> scripts/_simplify_iter/TAG_<set>.json + summary
"""
import html, json, os, random, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_simplify_iter")
os.makedirs(OUT, exist_ok=True)
PROMPT = os.path.join(HERE, "..", "api", "_lib", "simplify-prompt-simple.txt")
QAFILE = os.path.join(HERE, "..", "api", "_lib", "simplify-prompt-qa.txt")
TERMS = "Keep every specialist subject term that appears unchanged. Simplify the sentence around it; never swap it for an easier word."
WRITER, JUDGE = os.environ.get("SV_WRITER", "claude-sonnet-5-5"), os.environ.get("SV_JUDGE", "claude-sonnet-4-6")


def claude(system, user, model):
    p = os.path.join(OUT, "_sys_%08x.txt" % (hash(system) & 0xffffffff))
    if not os.path.exists(p): open(p, "w", encoding="utf-8").write(system)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    for _ in range(5):   # claude.cmd briefly vanishes while Claude Code updates itself
        try:
            r = subprocess.run(["claude.cmd", "-p", "--model", model, "--output-format", "json", "--tools", "",
                                "--strict-mcp-config", "--setting-sources", "", "--system-prompt-file", p],
                               input=user, capture_output=True, text=True, encoding="utf-8", env=env, timeout=600)
            return (json.loads(r.stdout).get("result") or "").strip()
        except FileNotFoundError:
            time.sleep(20)
        except Exception:
            return ""
    return ""


def stats(t):
    def syl(w):
        w = re.sub(r"[^a-z]", "", w.lower())
        if not w: return 0
        n = len(re.findall(r"[aeiouy]+", w))
        if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")): n -= 1
        return max(1, n)
    sents = [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]
    words = re.findall(r"[A-Za-z’']+", t)
    return 0.39 * len(words) / max(1, len(sents)) + 11.8 * sum(syl(w) for w in words) / max(1, len(words)) - 15.59


def retry_user(text, previous, feedback):
    return ("Rewrite this passage:\n<passage>\n%s\n</passage>\n\nA checker rejected your previous rewrite:\n"
            "<previous>\n%s\n</previous>\nReason: %s\nWrite a new rewrite of the passage that fixes this, and follow every rule."
            % (text, previous, feedback))


def cmd_sets():
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    rows = json.loads(urllib.request.urlopen(urllib.request.Request(
        U + "/rest/v1/lessons?select=id,content_html,units!inner(subjects!inner(slug,school_id))&status=eq.live"
            "&content_html=not.is.null&units.subjects.school_id=is.null&limit=1500",
        headers={"apikey": K, "Authorization": "Bearer " + K}), timeout=300).read())
    random.seed(int(os.environ.get("SV_SEED", "2809")))
    random.shuffle(rows)
    by, seen = {}, set()
    for x in rows:
        s = x["units"]["subjects"]["slug"].split("-")[0]
        for p in re.findall(r"<p[^>]*>(.*?)</p>", x["content_html"] or "", re.S):
            t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", p))).strip()
            n = len(t.split())
            if 40 <= n <= 140 and not re.search(r"[:?]\s*$", t) and t not in seen:
                by.setdefault(s, []).append({"subject": x["units"]["subjects"]["slug"], "text": t}); seen.add(t)
    pick = []
    while len(pick) < 60:
        for s in sorted(by):
            if by[s] and len(pick) < 60: pick.append(by[s].pop(random.randrange(len(by[s]))))
    random.shuffle(pick)
    json.dump({"dev": pick[:30], "holdout": pick[30:]}, open(os.path.join(OUT, os.environ.get("SV_SETS", "sets.json")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("sets: 30 dev + 30 holdout from", len(by), "subject families")


def cmd_run(which, tag):
    items = json.load(open(os.path.join(OUT, os.environ.get("SV_SETS", "sets.json")), encoding="utf-8"))[which]
    system = open(PROMPT, encoding="utf-8").read().replace("{{TERMS}}", TERMS)
    qa = open(QAFILE, encoding="utf-8").read()

    def one(it):
        out = claude(system, "Rewrite this passage:\n<passage>\n%s\n</passage>" % it["text"], WRITER)
        v = claude(qa, "ORIGINAL:\n%s\n\nSIMPLIFIED:\n%s" % (it["text"], out), JUDGE)
        m = re.search(r"\{.*\}", v, re.S)
        try: verdict = json.loads(m.group(0)) if m else {}
        except Exception: verdict = {}
        res = {**it, "out": out, "pass": verdict.get("pass") is True, "reason": verdict.get("reason", v[:200]),
               "issues": verdict.get("issues", []), "first_pass": verdict.get("pass") is True}
        if os.environ.get("SV_REGEN") and not res["pass"]:
            # the live retry: the checker's reasons go back to the writer (api/_lib/simplify-prompts.js retryUser)
            fb = "; ".join([str(res["reason"])] + [str(i) for i in res["issues"]])
            out2 = claude(system, retry_user(it["text"], out, fb), WRITER)
            v2 = claude(qa, "ORIGINAL:\n%s\n\nSIMPLIFIED:\n%s" % (it["text"], out2), JUDGE)
            m2 = re.search(r"\{.*\}", v2, re.S)
            try: verdict2 = json.loads(m2.group(0)) if m2 else {}
            except Exception: verdict2 = {}
            res.update({"out": out2, "pass": verdict2.get("pass") is True, "reason": verdict2.get("reason", v2[:200]),
                        "issues": verdict2.get("issues", []), "retried": True, "first_out": out})
        return res

    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(one, items))
    json.dump(res, open(os.path.join(OUT, "%s_%s.json" % (tag, which)), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    gs = [stats(r["out"]) for r in res if r["out"]]
    grade = round(sum(g for g in gs) / len(gs), 1) if gs else None
    n = sum(r["pass"] for r in res)
    print("%s %s: %d/%d pass | first try %d/%d | reading grade %s" % (tag, which, n, len(res), sum(r.get("first_pass", r["pass"]) for r in res), len(res), grade))
    for r in res:
        if not r["pass"]: print("  FAIL", r["subject"], "|", str(r["reason"])[:220])


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "sets": cmd_sets()
    else: cmd_run(a[1], a[2])
