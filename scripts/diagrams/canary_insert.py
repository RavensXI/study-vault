"""Diagram canary: upload accepted images to R2 and insert <figure class="diagram"> into lessons.

Usage: python scripts/diagrams/canary_insert.py <canary_dir> --gate gate.json [--dry-run]
gate.json: {"L2": {"verdict": "accept"|"reject", "note": "..."}, ...} from the vision gate.
For each accepted lesson: upload out/L{n}.jpg to studyvault-images at
diagrams/{subject}/{unit}/L{n}.jpg, then insert the figure after the section that follows
the brief's anchor_heading (i.e. immediately before the next <h2>, or at the end if none).
A backup of every touched content_html goes to <canary_dir>/_insert_backup.json (the
*_backup.json shape used by scripts/_retrofc/_renarrate_from_backup.py) and the content
validator runs on each patched row; a row with a NEW violation is not written.
No narrated text changes (the figcaption carries no data-narration-id).
"""
import argparse, json, os, sys, subprocess, tempfile, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from lib.r2 import get_r2_client, upload_file_to_r2, IMAGES_BUCKET  # noqa: E402


def validator(row):
    fd, p = tempfile.mkstemp(suffix=".json"); os.close(fd)
    json.dump(row, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "_validate_content_json.py"), p],
                       capture_output=True, text=True, encoding="utf-8")
    os.remove(p)
    return sorted(set(l.strip() for l in (r.stdout + r.stderr).splitlines()
                      if l.strip() and not l.startswith(("[OK]", "Usage", "==")) and p not in l))


def insert_figure(html, anchor_heading, figure):
    i = html.find(anchor_heading)
    if i < 0:
        return None
    nxt = html.find("<h2", i + len(anchor_heading))
    pos = nxt if nxt > 0 else len(html.rstrip())
    return html[:pos].rstrip() + "\n\n" + figure + "\n\n" + html[pos:].lstrip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canary_dir"); ap.add_argument("--gate", required=True); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); D = a.canary_dir
    data = json.load(open(os.path.join(D, "lessons.json"), encoding="utf-8"))
    briefs = {b["lesson_number"]: b for b in json.load(open(os.path.join(D, "briefs.json"), encoding="utf-8"))}
    results = json.load(open(os.path.join(D, "results.json"), encoding="utf-8"))
    gate = json.load(open(a.gate, encoding="utf-8"))
    U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
    H = {"apikey": K, "Authorization": "Bearer " + K, "Content-Type": "application/json", "Prefer": "return=minimal"}
    subj = data["unit"].get("subject_slug") or os.path.basename(os.path.dirname(D.rstrip("/\\")))  # canary dir name = unit label
    unit_slug = data["unit"]["slug"]
    r2 = None if a.dry_run else get_r2_client()
    backup = {"lessons": []}; log = []
    for l in data["lessons"]:
        n = l["lesson_number"]; key = f"L{n}"; b = briefs.get(n); g = gate.get(key, {})
        if not b or b["visual_form"] == "none" or g.get("verdict") != "accept" or not results.get(key, {}).get("ok"):
            continue
        # fresh row (the fact-check loop may have changed it since lessons.json was fetched)
        row = json.load(urllib.request.urlopen(urllib.request.Request(
            f"{U}/rest/v1/lessons?id=eq.{l['id']}&select=id,title,description,content_html,exam_tip_html,conclusion_html,practice_questions,knowledge_checks,flashcard_questions,glossary_terms",
            headers=H)))[0]
        if 'class="diagram"' in (row["content_html"] or ""):
            log.append(f"{key}: already has a diagram, skipped"); continue
        r2_key = f"diagrams/{subj}/{unit_slug}/{key}.jpg"
        url = f"https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/{r2_key}"
        alt = b["alt"].replace('"', "&quot;"); cap = b["caption"]
        figure = (f'<figure class="diagram">\n  <img src="{url}" alt="{alt}" loading="lazy">\n'
                  f'  <figcaption>{cap}</figcaption>\n</figure>')
        new = insert_figure(row["content_html"], b["anchor_heading"], figure)
        if new is None:
            log.append(f"{key}: anchor heading not found, skipped"); continue
        pre = validator(row); post_row = dict(row); post_row["content_html"] = new; post = validator(post_row)
        new_viol = [v for v in post if v not in pre]
        if new_viol:
            log.append(f"{key}: NEW validator violation, skipped: {new_viol[:2]}"); continue
        if a.dry_run:
            log.append(f"{key}: would upload {r2_key} and insert after '{b['anchor_heading'][:40]}'"); continue
        upload_file_to_r2(r2, IMAGES_BUCKET, results[key]["jpg"], r2_key, content_type="image/jpeg")
        backup["lessons"].append({"id": row["id"], "lesson_number": n, "before": {"content_html": row["content_html"]}})
        urllib.request.urlopen(urllib.request.Request(f"{U}/rest/v1/lessons?id=eq.{row['id']}",
                               data=json.dumps({"content_html": new}).encode(), headers=H, method="PATCH"))
        log.append(f"{key}: inserted {url}")
    if backup["lessons"]:
        json.dump(backup, open(os.path.join(D, "_insert_backup.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("\n".join(log) or "nothing to insert")


if __name__ == "__main__":
    main()
