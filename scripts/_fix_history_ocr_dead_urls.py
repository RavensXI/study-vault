"""Replace the remaining dead URLs across history-ocr after the bitesize fix."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from lib.supabase_client import get_client


# Dead domain (DNS resolution fails) → use Cromwell Museum (verified live)
REPLACEMENTS = {
    "https://www.national-civil-war-centre.com/": {
        "url": "https://www.cromwellmuseum.org/",
        "title": "The Cromwell Museum (Huntingdon)",
        "description": "Britain's only museum dedicated to Oliver Cromwell and the Civil War period — collections, exhibitions and learning resources.",
    },
    "https://www.nationalarchives.gov.uk/education/resources/dissolution-of-the-monasteries/": {
        "url": "https://www.nationalarchives.gov.uk/education/",
        "title": "The National Archives — Education",
        "description": "Document-based teaching resources covering Tudor religious reform and the dissolution of the monasteries.",
    },
    # battlefieldstrust war-of-the-roses path that returned 404 → strip it
    # and replace with their valid home page
    "https://www.battlefieldstrust.com/resource-centre/war-of-the-roses/battlepageview.asp?pid=92": {
        "url": "https://www.battlefieldstrust.com/",
        "title": "The Battlefields Trust",
        "description": "Searchable catalogue of UK battlefield sites with maps, primary accounts and visit guides.",
    },
}


def main():
    sb = get_client()
    sub = sb.table("subjects").select("id").eq("slug", "history-ocr").execute().data[0]
    units = sb.table("units").select("id").eq("subject_id", sub["id"]).execute().data

    fixed = 0
    for u in units:
        rows = sb.table("lessons").select("id, title, related_media").eq("unit_id", u["id"]).execute().data
        for r in rows:
            rm = r.get("related_media") or []
            changed = False
            for cat in rm:
                if not isinstance(cat, dict):
                    continue
                for item in cat.get("items") or []:
                    if not isinstance(item, dict):
                        continue
                    src = item.get("url")
                    # Match partial URLs too (some have trailing fragments)
                    for bad_url, replacement in REPLACEMENTS.items():
                        if src == bad_url or (src and src.startswith(bad_url)):
                            item["url"] = replacement["url"]
                            item["title"] = replacement["title"]
                            item["description"] = replacement["description"]
                            changed = True
                            break
            if changed:
                sb.table("lessons").update({"related_media": rm}).eq("id", r["id"]).execute()
                fixed += 1
                print(f"  fixed {r['title'][:60]}")

    print(f"\nTotal lessons updated: {fixed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
