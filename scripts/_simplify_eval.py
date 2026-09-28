"""Simplify-wording prompt evaluation (28 Sep 2026).

Tom: the Simplify wording button "often just truncates the text into shorter sentences, but it's
pretty much a word-for-word rewrite", and twice it replied to the paragraph ("I understand. When
rewriting, I will...") instead of rewriting it. This compares the LIVE prompt with a proposed one on
real cached paragraphs, through the Claude Code subscription (claude -p, no tools, our system prompt).

Measures per output: reading grade (Flesch-Kincaid), average sentence length, how much of the
original wording is kept (share of the original's 3-word runs that survive), and meta-replies.
Then the proposed QA check judges the proposed outputs.

  python scripts/_simplify_eval.py       -> scripts/_simplify_eval.json + .md
"""
import json, os, random, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_simplify_eval")
os.makedirs(OUT, exist_ok=True)
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]

OLD = """You rewrite GCSE revision text into plainer English for students with a lower reading age or who are learning English as an additional language.

Rules you must never break:
1. Keep any specialist subject term that appears unchanged — simplify the sentence around it, never swap it for an easier word.
2. Never change any number, date, name, place, or quotation. Never change a fact.
3. Never add a new point and never remove a point. Same information, simpler wording. If the text is an introduction, a rhetorical question, or ends with a colon pointing to a list or section, rewrite ONLY the words you are given — do not answer the question and do not fill in or list the items it introduces. That content is in other paragraphs you cannot see.
4. Use shorter sentences and everyday words. Break long sentences into two if it helps. Keep roughly the same overall length.
5. Keep a neutral, factual tone. Do not address the student ("you"), do not add encouragement, do not add commentary.
6. Output ONLY the rewritten text as plain prose. No markdown, no headings, no preamble, no notes, no quotation marks around it."""

NEW = open(os.path.join(HERE, "..", "api", "_lib", "simplify-prompt-simple.txt"), encoding="utf-8").read().replace("{{TERMS}}", "Keep every specialist subject term that appears unchanged. Simplify the sentence around it; never swap it for an easier word.")
QA = open(os.path.join(HERE, "..", "api", "_lib", "simplify-prompt-qa.txt"), encoding="utf-8").read()
META = re.compile(r"^\s*(i understand|i will|i'll|i can|sure|certainly|of course|here is|here's|okay|ok[,.]|when rewriting|as requested|understood)", re.I)


def claude(system, user, model):
    p = os.path.join(OUT, "_sys_%d.txt" % (hash(system) & 0xffffff))
    if not os.path.exists(p): open(p, "w", encoding="utf-8").write(system)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    r = subprocess.run(["claude.cmd", "-p", "--model", model, "--output-format", "json", "--tools", "", "--strict-mcp-config",
                        "--setting-sources", "", "--system-prompt-file", p], input=user, capture_output=True, text=True,
                       encoding="utf-8", env=env, timeout=600)
    try: return (json.loads(r.stdout).get("result") or "").strip()
    except Exception: return ""


def syllables(w):
    w = w.lower(); w = re.sub(r"[^a-z]", "", w)
    if not w: return 0
    v = re.findall(r"[aeiouy]+", w); n = len(v)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")): n -= 1
    return max(1, n)


def stats(t):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s]
    words = re.findall(r"[A-Za-z’']+", t)
    if not words: return {}
    fk = 0.39 * len(words) / max(1, len(sents)) + 11.8 * sum(syllables(w) for w in words) / len(words) - 15.59
    return {"grade": round(fk, 1), "words_per_sentence": round(len(words) / max(1, len(sents)), 1), "words": len(words)}


def kept(orig, new):
    def tri(t):
        w = re.findall(r"[a-z’']+", (t or "").lower())
        return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}
    a = tri(orig)
    return round(len(a & tri(new)) / max(1, len(a)), 2)


def main():
    rows = json.loads(urllib.request.urlopen(urllib.request.Request(
        U + "/rest/v1/simplify_cache?select=original_hash,subject_slug,original_text,simplified_text&target_level=eq.simple&qa_status=eq.pass&limit=1000",
        headers={"apikey": K, "Authorization": "Bearer " + K})).read())
    rows = [r for r in rows if len(r["original_text"].split()) >= 45]
    random.seed(28)
    by = {}
    for r in rows: by.setdefault(r["subject_slug"], []).append(r)
    sample = []
    for s in sorted(by):
        sample += random.sample(by[s], min(2, len(by[s])))
    sample = sample[:26]
    # the two paragraphs that produced meta-replies
    for t in ["This is a genuinely two-part skill: you must connect a specific feature of the cover (a cover line, an image choice, a styling decision) to a specific aspect of context, rather than stating a general historical fact and a general cover description side by side without linking them.",
              "For AO3, always link context to Shelley’s purpose. Instead of “Galvanism was popular in the early 19th century,” write “Shelley uses Victor’s galvanic experiments to warn against the Enlightenment belief that science can overcome all limits, reflecting contemporary anxieties about rapid scientific progress.” Context should always explain WHY Shelley makes the choices she does."]:
        sample.append({"subject_slug": "meta-case", "original_text": t, "simplified_text": ""})

    def run(r):
        o = r["original_text"]
        res = {"subject": r["subject_slug"], "original": o, "live_cached": r["simplified_text"],
               "old_haiku": claude(OLD, o, "haiku"),
               "new_haiku": claude(NEW, "Rewrite this passage:\n<passage>\n%s\n</passage>" % o, "haiku"),
               "new_sonnet": claude(NEW, "Rewrite this passage:\n<passage>\n%s\n</passage>" % o, "sonnet")}
        for k in ("new_haiku", "new_sonnet"):
            v = claude(QA, "ORIGINAL:\n%s\n\nSIMPLIFIED:\n%s" % (o, res[k]), "sonnet")
            m = re.search(r"\{.*\}", v, re.S)
            try: res[k + "_qa"] = json.loads(m.group(0)) if m else {"pass": None}
            except Exception: res[k + "_qa"] = {"pass": None, "raw": v[:200]}
        return res

    with ThreadPoolExecutor(4) as ex:
        results = list(ex.map(run, sample))
    for r in results:
        for k in ("original", "old_haiku", "new_haiku", "new_sonnet"):
            r[k + "_stats"] = stats(r[k])
            if k != "original": r[k + "_kept"] = kept(r["original"], r[k]); r[k + "_meta"] = bool(META.match(r[k] or ""))
    json.dump(results, open(os.path.join(HERE, os.environ.get("SV_EVAL_TAG","") + "_simplify_eval.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def avg(key, sub):
        v = [r[key].get(sub) for r in results if r.get(key)]
        return round(sum(v) / len(v), 1) if v else None
    lines = ["# Simplify wording: live prompt vs proposed (28 Sep 2026)", "",
             "| | Reading grade (FK) | Words per sentence | Original 3-word runs kept | Meta-replies | QA pass |", "|---|---|---|---|---|---|",
             "| Original paragraph | %s | %s | 100%% | | |" % (avg("original_stats", "grade"), avg("original_stats", "words_per_sentence"))]
    for k, label in (("old_haiku", "Live prompt (Haiku)"), ("new_haiku", "Proposed prompt (Haiku)"), ("new_sonnet", "Proposed prompt (Sonnet)")):
        keptv = [r[k + "_kept"] for r in results]
        qa = [r.get(k + "_qa", {}).get("pass") for r in results if k + "_qa" in r]
        lines.append("| %s | %s | %s | %d%% | %d | %s |" % (label, avg(k + "_stats", "grade"), avg(k + "_stats", "words_per_sentence"),
                     round(100 * sum(keptv) / len(keptv)), sum(r[k + "_meta"] for r in results),
                     ("%d/%d" % (sum(1 for q in qa if q), len(qa))) if qa else "-"))
    lines += ["", "## Side by side", ""]
    for r in results:
        lines += ["### %s" % r["subject"], "", "**Original:** " + r["original"], "", "**Live prompt:** " + r["old_haiku"], "",
                  "**Proposed (Haiku):** " + r["new_haiku"], "", "**Proposed (Sonnet):** " + r["new_sonnet"],
                  "", "QA Haiku: %s — QA Sonnet: %s" % (r.get("new_haiku_qa", {}).get("reason"), r.get("new_sonnet_qa", {}).get("reason")), ""]
    open(os.path.join(HERE, os.environ.get("SV_EVAL_TAG","") + "_simplify_eval.md"), "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines[:8]))


if __name__ == "__main__":
    main()
