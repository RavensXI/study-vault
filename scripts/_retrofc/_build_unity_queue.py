"""Queue every article unit of a school's bespoke subjects for the retro fact-check.

The free-tier programme never covered school content: three bare slugs it listed
resolved to free-tier rows. Items here carry `school_id` and `school_tag`, which
_unit.py uses to fetch the school's row and to name the unit dir, plus `board`,
`spec` (from specs/index.json by board + spec_code) and `family` (which brief).

  python scripts/_retrofc/_build_unity_queue.py --school unity [--confirm]
"""
import io, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
QUEUE = os.path.join(HERE, "_queue.json"); INDEX = os.path.join(ROOT, "specs", "index.json")
SCHOOLS = {"unity": "a5414d1c-8841-4bc5-8573-a9756752361b"}
FAMILY = {"english-literature": "english-literature", "science": "science", "separate-sciences": "science", "history": "history"}
# the practice-first units carry no article to check
def get(path):
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    req = urllib.request.Request(U + "/rest/v1/" + path, headers={"apikey": K, "Authorization": "Bearer " + K})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())

def spec_for(board, code, index):
    codes = [c.strip() for c in (code or "").replace("/", " ").split()]
    paths = []
    for c in codes:
        hit = next((e for e in index if e["board"].lower() == (board or "").lower() and e["spec_code"] == c), None)
        if hit: paths.append("specs/" + hit["path"])
    return paths

def main():
    a = sys.argv[1:]
    tag = a[a.index("--school") + 1] if "--school" in a else "unity"
    sid = SCHOOLS[tag]; confirm = "--confirm" in a
    index = json.load(io.open(INDEX, encoding="utf-8"))
    q = json.load(io.open(QUEUE, encoding="utf-8"))
    have = {(i["subject"], i["unit"], i.get("school_id")) for i in q["items"]}
    added = []
    for s in get(f"subjects?school_id=eq.{sid}&select=id,slug,name,exam_board,spec_code,settings"):
        st = s.get("settings") or {}; practice = set(st.get("practice_units") or [])
        specs = spec_for(s.get("exam_board"), s.get("spec_code"), index)
        fam = FAMILY.get(s["slug"], "generic")
        qual = "separate" if s["slug"] == "separate-sciences" else ("combined" if s["slug"] == "science" else None)
        for u in get(f"units?subject_id=eq.{s['id']}&select=id,slug,name&order=sort_order"):
            if u["slug"] in practice: continue
            n = len(get(f"lessons?unit_id=eq.{u['id']}&select=id"))
            if not n or (s["slug"], u["slug"], sid) in have: continue
            item = {"subject": s["slug"], "unit": u["slug"], "lessons": n, "status": "queued", "family": fam,
                    "spec": specs[0] if specs else None, "specs": specs, "qualification": qual,
                    "board": (s.get("exam_board") or "").split()[0].lower(), "school_id": sid, "school_tag": tag, "school_name": s["name"]}
            added.append(item)
            print(f"{s['slug']:32s} {u['slug']:40s} {n:3d}  {fam:18s} {item['spec'] or 'NO SPEC'}")
    print(f"\n{len(added)} units, {sum(i['lessons'] for i in added)} lessons; no spec: {sum(1 for i in added if not i['spec'])}")
    if confirm:
        q["items"] += added
        io.open(QUEUE, "w", encoding="utf-8").write(json.dumps(q, indent=1, ensure_ascii=False))
        print("saved")
    else:
        print("dry run: add --confirm to save")

if __name__ == "__main__":
    main()
