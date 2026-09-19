"""E3/E9/E12/E15 - content QA at scale on live free-tier lessons.
  qtype    : classify each practice question's exam type from its text; compare with the badge label
  kc       : knowledge-check distractor audit (an option that is ALSO right; a correct answer that is
             debatable; a question the lesson does not teach)
  dupes    : lesson-pair overlap inside a unit; ground truth = the four RS lessons archived 18 Sep
  readable : reading-level score of lesson paragraphs vs a Flesch-Kincaid grade computed in code
Run: python exp_content_qa.py qtype|kc|dupes|readable|all"""
import io, json, os, sys, re, random, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev import ask_many, answers, save, sb_all, sb_get, Choice, Score, Noul

def strip(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
random.seed(3)

def lessons(n=None, extra=""):
    """sample ids first (light), then fetch the heavy columns for the sample in batches of 40,
    so three experiments can run at once without hammering Supabase"""
    light = sb_all("lessons?select=id,units!inner(subjects!inner(school_id))&status=eq.live&is_listening=eq.false&units.subjects.school_id=is.null" + extra)
    random.shuffle(light)
    ids = [r["id"] for r in (light[:n] if n else light)]
    rows = []
    for k in range(0, len(ids), 40):
        chunk = ",".join(ids[k:k + 40])
        for attempt in range(4):
            try:
                rows += sb_get("lessons?select=id,title,description,lesson_number,practice_questions,knowledge_checks,related_media,content_html,units!inner(slug,name,subjects!inner(slug,school_id))&id=in.(" + chunk + ")")
                break
            except Exception as e:
                import time; time.sleep(3 * (attempt + 1))
    return rows

# ---------------------------------------------------------------- qtype
QTYPES = {"multiple_choice": "pick one option from a list", "recall": "state, name, give, identify or define a fact in a word or short phrase", "describe": "describe a thing, process or feature without explaining causes",
          "explain": "explain how or why, giving reasons or mechanisms", "compare": "explain similarities or differences between two things", "calculate": "work out a number, show working, use a formula or data",
          "analyse_source_or_extract": "analyse a given source, extract, poem or text", "evaluate_judgement": "how far do you agree, evaluate, assess, discuss or justify a judgement with a conclusion",
          "narrative_account": "write an account or narrative of how events unfolded", "extended_writing": "a creative, descriptive or persuasive writing task", "plan_or_design": "plan, design or suggest a method or investigation"}
def run_qtype():
    ls = lessons(600)
    items = []
    for l in ls:
        for i, q in enumerate(l.get("practice_questions") or []):
            if not q.get("text") or not q.get("type"): continue
            items.append({"lesson_id": l["id"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"], "n": l["lesson_number"], "i": i, "text": strip(q["text"])[:1200], "badge": q["type"]})
    random.shuffle(items); items = items[:1500]
    def build(it):
        return ({"subject": it["subject"], "question": it["text"]}, {"qtype": Choice(instructions="What kind of exam question is this", criteria=QTYPES)})
    res = ask_many(items, build, tag="qtype", workers=8)
    rows = []
    for it, r, err in res:
        if not r: continue
        a = answers(r); it["jev"] = a["qtype"]["choice"]; it["conf"] = a["qtype"]["confidence"]; rows.append(it)
    # badge family from the label text
    def fam(b):
        b = b.lower()
        if "multiple" in b: return "multiple_choice"
        if re.search(r"calculat|work out|numerical|data", b): return "calculate"
        if re.search(r"agree|evaluat|assess|discuss|justify|judgement", b): return "evaluate_judgement"
        if re.search(r"narrativ|account", b): return "narrative_account"
        if re.search(r"compar|similar|differen", b): return "compare"
        if re.search(r"source|extract|analys|poem|text", b): return "analyse_source_or_extract"
        if re.search(r"creative|descriptive|persuasive|writing|speech|letter|article", b): return "extended_writing"
        if re.search(r"explain|why|how", b): return "explain"
        if re.search(r"describ", b): return "describe"
        if re.search(r"plan|design|method|suggest", b): return "plan_or_design"
        if re.search(r"state|name|give|identify|define|recall|short", b): return "recall"
        return None
    agree = n = 0; dis = collections.Counter()
    for r in rows:
        f = fam(r["badge"]); r["badge_family"] = f
        if not f: continue
        n += 1
        if f == r["jev"]: agree += 1
        else: dis[(f, r["jev"])] += 1
    mism = [r for r in rows if r.get("badge_family") and r["badge_family"] != r["jev"] and r["conf"] >= 0.85]
    summary = {"questions": len(rows), "with_badge_family": n, "agree": agree, "rate": round(agree / max(n, 1), 3), "confident_disagreements": len(mism), "top_disagreements": [{"badge": k[0], "jev": k[1], "n": v} for k, v in dis.most_common(12)]}
    print(json.dumps(summary, indent=1)); save("qtype.json", {"summary": summary, "rows": rows})

# ---------------------------------------------------------------- kc
def run_kc():
    ls = [l for l in lessons(700) if l.get("content_html") and len(l["content_html"]) > 1500]      # article lessons only; practice sets keep their teaching elsewhere
    items = []
    for l in ls:
        body = strip(l.get("content_html"))[:36000]
        for i, k in enumerate(l.get("knowledge_checks") or []):
            if k.get("type") not in (None, "mcq") or not k.get("options") or k.get("correct") is None: continue
            items.append({"lesson_id": l["id"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"], "n": l["lesson_number"], "i": i, "q": k["q"], "options": k["options"], "correct": k["correct"], "body": body})
    random.shuffle(items); items = items[:1200]
    def build(it):
        opts = {chr(65 + j): o for j, o in enumerate(it["options"])}
        qs = {"taught": Noul(instructions="The lesson text teaches what this question asks, so a student who read it could answer"),
              "answer_key_right": Noul(instructions="The option marked correct is the best answer to the question")}
        for L, o in opts.items():
            if ord(L) - 65 == it["correct"]: continue
            qs["also_right_" + L] = Noul(instructions="Option %s is also a defensible correct answer to the question, not a clear distractor" % L)
        return ({"lesson_text": it["body"], "question": it["q"], "options": opts, "marked_correct": chr(65 + it["correct"])}, qs)
    res = ask_many(items, build, tag="kc", workers=8)
    rows = []; flags = collections.Counter()
    for it, r, err in res:
        if not r: continue
        a = answers(r); row = {k: it[k] for k in ("lesson_id", "subject", "unit", "n", "i", "q", "options", "correct")}
        row["taught"] = a["taught"]["noul"]; row["key_right"] = a["answer_key_right"]["noul"]
        row["also_right"] = {k[-1]: v["noul"] for k, v in a.items() if k.startswith("also_right_")}
        if row["taught"] < 0.4: flags["not_taught"] += 1
        if row["key_right"] < 0.5: flags["key_doubtful"] += 1
        if any(v >= 0.7 for v in row["also_right"].values()): flags["second_right_option"] += 1
        rows.append(row)
    summary = {"questions": len(rows), "flags": dict(flags), "flag_rate": round(sum(flags.values()) / max(len(rows), 1), 3)}
    print(json.dumps(summary, indent=1)); save("kc_full.json", {"summary": summary, "rows": rows})

# ---------------------------------------------------------------- dupes
def run_dupes():
    rows = sb_all("lessons?select=id,title,description,lesson_number,status,content_html,units!inner(slug,name,subjects!inner(slug,school_id))&units.subjects.slug=eq.religious-studies&units.subjects.school_id=eq.a5414d1c-8841-4bc5-8573-a9756752361b&status=in.(live,archived)")
    byunit = collections.defaultdict(list)
    for r in rows: byunit[r["units"]["slug"]].append(r)
    pairs = []
    for u, ls in byunit.items():
        ls.sort(key=lambda x: x["lesson_number"])
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                pairs.append({"unit": u, "a": ls[i], "b": ls[j], "truth": ls[i]["status"] == "archived" or ls[j]["status"] == "archived"})
    def build(p):
        return ({"lesson_A": {"title": p["a"]["title"], "description": p["a"]["description"], "text": strip(p["a"]["content_html"])[:3500]},
                 "lesson_B": {"title": p["b"]["title"], "description": p["b"]["description"], "text": strip(p["b"]["content_html"])[:3500]}},
                {"overlap": Score(instructions="How much of the same content the two lessons teach", criteria=["different topics", "some shared ground, each has its own content", "largely the same content, one is redundant"])})
    res = ask_many(pairs, build, tag="dupes", workers=6)
    out = []
    for p, r, err in res:
        if not r: continue
        a = answers(r); out.append({"unit": p["unit"], "A": "%d %s" % (p["a"]["lesson_number"], p["a"]["title"]), "B": "%d %s" % (p["b"]["lesson_number"], p["b"]["title"]), "archived_pair": p["truth"], "overlap": a["overlap"]["score"], "conf": a["overlap"]["confidence"]})
    out.sort(key=lambda x: -x["overlap"])
    top = out[:12]; arch = [o for o in out if o["archived_pair"]]
    summary = {"pairs": len(out), "archived_pairs": len(arch), "archived_pairs_in_top_12": sum(1 for o in top if o["archived_pair"]), "top": top, "archived_scores": [{"A": o["A"], "B": o["B"], "overlap": o["overlap"]} for o in arch]}
    print(json.dumps(summary, indent=1, ensure_ascii=False)); save("dupes.json", {"summary": summary, "rows": out})

# ---------------------------------------------------------------- readable
def fk_grade(text):
    sents = max(1, len(re.findall(r"[.!?]+", text))); words = re.findall(r"[A-Za-z']+", text); w = max(1, len(words))
    def syl(x):
        x = x.lower(); c = len(re.findall(r"[aeiouy]+", x)); return max(1, c - (1 if x.endswith("e") and c > 1 else 0))
    s = sum(syl(x) for x in words)
    return 0.39 * (w / sents) + 11.8 * (s / w) - 15.59
def run_readable():
    ls = lessons(400)
    items = []
    for l in ls:
        paras = [strip(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", l.get("content_html") or "", re.S)]
        paras = [p for p in paras if 200 <= len(p) <= 900]
        if not paras: continue
        p = random.choice(paras)
        items.append({"lesson_id": l["id"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"], "n": l["lesson_number"], "para": p, "fk": round(fk_grade(p), 1)})
    def build(it):
        return ({"subject": it["subject"], "paragraph": it["para"]},
                {"level": Score(instructions="How hard this paragraph is for a 15-year-old GCSE student to read", criteria=["easy: short sentences, everyday words", "right for GCSE: some subject terms, explained", "hard: long sentences or dense terms a 15-year-old would stumble on", "university level"]),
                 "jargon_unexplained": Noul(instructions="A subject term is used without being explained anywhere in the paragraph")})
    res = ask_many(items, build, tag="readable", workers=8)
    rows = []
    for it, r, err in res:
        if not r: continue
        a = answers(r); it["jev_level"] = a["level"]["score"]; it["jargon"] = a["jargon_unexplained"]["noul"]; rows.append(it)
    # rank correlation between fk grade and jev level
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for k, i in enumerate(s): r[i] = k
        return r
    fk = [r["fk"] for r in rows]; jv = [r["jev_level"] for r in rows]
    rf, rj = rank(fk), rank(jv); n = len(rows)
    rho = 1 - 6 * sum((a - b) ** 2 for a, b in zip(rf, rj)) / max(n * (n * n - 1), 1)
    hard = sorted(rows, key=lambda x: -x["jev_level"])[:15]
    summary = {"paragraphs": n, "spearman_fk_vs_jev": round(rho, 3), "share_hard_or_worse": round(sum(1 for r in rows if r["jev_level"] >= 2) / max(n, 1), 3), "share_jargon": round(sum(1 for r in rows if r["jargon"] >= 0.7) / max(n, 1), 3),
               "hardest": [{"subject": h["subject"], "unit": h["unit"], "n": h["n"], "level": h["jev_level"], "fk": h["fk"], "para": h["para"][:220]} for h in hard]}
    print(json.dumps(summary, indent=1, ensure_ascii=False)); save("readable.json", {"summary": summary, "rows": rows})

# ---------------------------------------------------------------- desc + media (appended)
def run_desc():
    ls = lessons(800)
    items = [{"lesson_id": l["id"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"], "n": l["lesson_number"], "title": l["title"], "description": l["description"] or "", "body": strip(l.get("content_html"))[:5000]} for l in ls if l.get("description")]
    def build(it):
        return ({"title": it["title"], "description": it["description"], "lesson_text": it["body"]},
                {"matches": Noul(instructions="The description accurately summarises what this lesson text teaches"),
                 "promises_missing": Noul(instructions="The description mentions a topic, example or skill that the lesson text does not actually cover"),
                 "quality": Score(instructions="How well the description would help a student decide whether this is the lesson they need", criteria=["vague or generic, could describe many lessons", "names the topic but little more", "specific: names the ideas, examples or skills the lesson covers"])})
    res = ask_many(items, build, tag="desc", workers=8)
    rows = []
    for it, r, err in res:
        if not r: continue
        a = answers(r); rows.append({**{k: it[k] for k in ("lesson_id", "subject", "unit", "n", "title", "description")}, "matches": a["matches"]["noul"], "promises_missing": a["promises_missing"]["noul"], "quality": a["quality"]["score"]})
    summary = {"lessons": len(rows), "mismatch_rate": round(sum(1 for r in rows if r["matches"] < 0.5) / max(len(rows), 1), 3), "promises_missing_rate": round(sum(1 for r in rows if r["promises_missing"] >= 0.7) / max(len(rows), 1), 3),
               "vague_rate": round(sum(1 for r in rows if r["quality"] < 0.5) / max(len(rows), 1), 3), "worst": sorted(rows, key=lambda x: x["matches"])[:12]}
    print(json.dumps(summary, indent=1, ensure_ascii=False)); save("desc.json", {"summary": summary, "rows": rows})

def run_media():
    ls = lessons(600)
    items = []
    for l in ls:
        for cat in (l.get("related_media") or []) if isinstance(l.get("related_media"), list) else []:
            for m in cat.get("items") or []:
                if not m.get("title"): continue
                items.append({"lesson_id": l["id"], "subject": l["units"]["subjects"]["slug"], "unit": l["units"]["slug"], "n": l["lesson_number"], "lesson_title": l["title"], "description": l.get("description") or "", "category": cat.get("category"), "title": m["title"], "blurb": m.get("description") or "", "url": m.get("url")})
    random.shuffle(items); items = items[:1500]
    def build(it):
        return ({"lesson": {"title": it["lesson_title"], "description": it["description"], "subject": it["subject"]}, "media_item": {"category": it["category"], "title": it["title"], "description": it["blurb"], "url": it["url"]}},
                {"relevant": Noul(instructions="This media item is about the same topic as the lesson and would help a GCSE student revising it"),
                 "too_advanced": Noul(instructions="The item is pitched well above GCSE level (undergraduate lecture, academic paper, specialist documentary)"),
                 "generic": Noul(instructions="The item is a whole channel, a homepage or a general overview rather than something on this lesson's topic")})
    res = ask_many(items, build, tag="media", workers=8)
    rows = []
    for it, r, err in res:
        if not r: continue
        a = answers(r); rows.append({**it, "relevant": a["relevant"]["noul"], "advanced": a["too_advanced"]["noul"], "generic": a["generic"]["noul"]})
    summary = {"items": len(rows), "irrelevant_rate": round(sum(1 for r in rows if r["relevant"] < 0.4) / max(len(rows), 1), 3), "generic_rate": round(sum(1 for r in rows if r["generic"] >= 0.7) / max(len(rows), 1), 3), "advanced_rate": round(sum(1 for r in rows if r["advanced"] >= 0.7) / max(len(rows), 1), 3),
               "least_relevant": [{"subject": r["subject"], "unit": r["unit"], "n": r["n"], "lesson": r["lesson_title"], "item": r["title"], "p": r["relevant"]} for r in sorted(rows, key=lambda x: x["relevant"])[:15]]}
    print(json.dumps(summary, indent=1, ensure_ascii=False)); save("media.json", {"summary": summary, "rows": rows})

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (["qtype", "kc", "dupes", "readable", "desc", "media"] if which == "all" else [which]):
        globals()["run_" + name]()

