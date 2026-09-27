"""Write each department's opening line (the subject and the exact boards we serve for it) into
departments/<dept>.json, from the LIVE database: free-tier subjects (school_id null), status live.
The variant of each board (Edexcel A, OCR Gateway, AQA Trilogy ...) comes from the row's spec_code
looked up in specs/index.json; a board with no variant in the spec name shows the board alone.

  python boards.py            (SUPABASE_URL / SUPABASE_SERVICE_KEY in the environment; read-only)
"""
import io, json, os, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
DEPTS = {"history": ("History", r"^history-"), "geography": ("Geography", r"^geography-"), "science": ("Combined Science", r"^science-")}
ORDER = ["AQA", "Edexcel", "OCR", "Eduqas", "WJEC"]


def get(q):
    return json.loads(urllib.request.urlopen(urllib.request.Request(U + "/rest/v1/" + q, headers={"apikey": K, "Authorization": "Bearer " + K})).read())


def variant(spec_subject):
    """'Geography A' -> 'A'; 'History A (Explaining the Modern World)' -> 'A'; 'Combined Science A (Gateway Science)'
    -> 'Gateway'; 'Combined Science B (Twenty First Century Science)' -> 'Twenty First Century';
    'Combined Science: Trilogy' -> 'Trilogy'; 'History' -> ''."""
    m = re.search(r"\(([^)]*)\)", spec_subject)
    if m and spec_subject.startswith("Combined Science"):
        return re.sub(r"\s*Science$", "", m.group(1)).strip()
    m = re.search(r":\s*(\w+)$", spec_subject)
    if m: return m.group(1)
    m = re.search(r"\b([AB])\b", spec_subject.split("(")[0])
    return m.group(1) if m else ""


def main():
    index = json.load(io.open(os.path.join(REPO, "specs", "index.json"), encoding="utf-8"))
    specs = index if isinstance(index, list) else index.get("specs", list(index.values()))
    by_code = {s["spec_code"]: s for s in specs}
    rows = get("subjects?select=slug,name,exam_board,spec_code,status,school_id&school_id=is.null&status=eq.live&order=slug")
    for dept, (subject, pat) in DEPTS.items():
        mine = [r for r in rows if re.match(pat, r["slug"]) and not r["slug"].startswith("separate")]
        labels, src = [], []
        for r in mine:
            base = (r["exam_board"] or "").split()[0]
            spec = by_code.get(r["spec_code"])
            v = variant(spec["subject"]) if spec else ""
            label = (base + " " + v).strip() if v else base
            labels.append((ORDER.index(base) if base in ORDER else 9, label))
            src.append(f"{r['slug']} ({r['spec_code']}: {spec['subject'] if spec else 'spec not in index'})")
        labels = [l for _, l in sorted(set(labels))]
        p = os.path.join(HERE, "departments", dept + ".json")
        d = json.load(io.open(p, encoding="utf-8"))
        d["headline"] = {"subject": subject, "boards": labels, "source": "Live free-tier subjects: " + "; ".join(src) + " (specs/index.json for the variant)."}
        io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
        print(dept, labels)


if __name__ == "__main__":
    main()
