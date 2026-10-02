"""Science Key Takeaways shown twice (retro fact-check worklist; drafted 3 Oct 2026, NOT applied).

Eight science lessons end content_html with a <div class="conclusion"> Key Takeaways box that repeats
conclusion_html word for word, so the page shows the box twice and the narration reads it twice.
The fix: remove that trailing box from content_html, and drop its clips from narration_manifest
(the conclusion's own clips stay). Nothing else in the lesson changes.

  python scripts/_keytakeaways_dedup_2026-10-03.py            # draft: writes the review file, changes nothing
  python scripts/_keytakeaways_dedup_2026-10-03.py --apply    # Tom's go only: backs up, then writes the 8 rows
"""
import json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lib.supabase_client import get_client

IDS = ["925c7721-6788-4ae0-b4cb-f1f2a546a47a", "c5419502-a45f-492e-b998-11aa5b1dcf31", "73945b80-c569-41b5-8d6b-582f76927c7d",
       "0e45f87f-fb4f-45dc-80c0-7d0f0e3bed5f", "8dba8f58-2cad-4cfb-82e0-b202792fbfe3", "bf094a53-2a2e-4812-b33c-aa59fd9f7313",
       "5a3e0554-797d-4dc2-bb55-2625595b2ffb", "61a8058e-39b9-4568-9031-7f62477089d5"]
REVIEW = os.path.join(HERE, "_keytakeaways_dedup_2026-10-03_review.md")
# two forms: wrapped in <div class="conclusion"> (5 lessons), or a bare <h3> + <ul> (the three chemistry L1s)
BLOCK = re.compile(r'\s*(?:<div class="conclusion">\s*<h3[^>]*>\s*Key Takeaways\s*</h3>.*?</div>'
                   r'|<h3[^>]*>\s*Key Takeaways\s*</h3>\s*<ul>.*?</ul>)\s*$', re.S | re.I)


def plain(h):
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
            for x in re.findall(r"<li[^>]*>(.*?)</li>", h, re.S)]


def plan(sb):
    out = []
    for lid in IDS:
        r = sb.table("lessons").select("id,lesson_number,content_html,conclusion_html,narration_manifest,"
                                       "units!inner(slug,subjects!inner(slug,school_id))").eq("id", lid).execute().data[0]
        label = "%s/%s/L%02d" % (r["units"]["subjects"]["slug"], r["units"]["slug"], r["lesson_number"])
        m = BLOCK.search(r["content_html"])
        if not m:
            out.append({"id": lid, "label": label, "ok": False, "why": "no trailing Key Takeaways box found"}); continue
        block = m.group(0)
        same = plain(block) == plain(r["conclusion_html"] or "")
        drop = re.findall(r'data-narration-id="([^"]+)"', block)
        man = r["narration_manifest"] or []
        out.append({"id": lid, "label": label, "ok": same, "why": "" if same else "the two boxes differ - not touched",
                    "block": block.strip(), "points": plain(block), "drop_ids": drop,
                    "manifest_before": len(man), "manifest_after": len([e for e in man if e["id"] not in drop]),
                    "new_content": r["content_html"][:m.start()].rstrip() + "\n", "row": r})
    return out


def main():
    sb = get_client()
    P = plan(sb)
    lines = ["# Science Key Takeaways shown twice: draft fix (3 Oct 2026)", "",
             "Each lesson below ends its main content with a Key Takeaways box that repeats the conclusion box under it, "
             "word for word. The fix removes the copy in the main content and its narration clips. The conclusion box and "
             "everything else stay as they are.", "",
             "Apply with: `python scripts/_keytakeaways_dedup_2026-10-03.py --apply` (backs up the 8 rows first).", ""]
    for p in P:
        lines.append("## %s %s" % (p["label"], "" if p["ok"] else "- NOT TOUCHED: " + p["why"]))
        if p.get("points"):
            lines.append("Copy removed from the main content (identical to the conclusion: %s):" % ("yes" if p["ok"] else "NO"))
            lines += ["- " + x for x in p["points"]]
            lines.append("Narration clips dropped: %s (%d clips -> %d)" % (", ".join(p["drop_ids"]), p["manifest_before"], p["manifest_after"]))
        lines.append("")
    open(REVIEW, "w", encoding="utf-8").write("\n".join(lines))
    print("review:", REVIEW, "| ready:", sum(p["ok"] for p in P), "of", len(P))

    if "--apply" not in sys.argv:
        return
    ready = [p for p in P if p["ok"]]
    bk = os.path.join(HERE, "_backup_keytakeaways_dedup_%s.json" % time.strftime("%Y-%m-%d_%H%M"))
    json.dump([{"id": p["id"], "content_html": p["row"]["content_html"], "narration_manifest": p["row"]["narration_manifest"]}
               for p in ready], open(bk, "w", encoding="utf-8"), ensure_ascii=False)
    print("backup:", bk)
    for p in ready:
        man = [e for e in (p["row"]["narration_manifest"] or []) if e["id"] not in p["drop_ids"]]
        sb.table("lessons").update({"content_html": p["new_content"], "narration_manifest": man}).eq("id", p["id"]).execute()
        print("  fixed", p["label"])


if __name__ == "__main__":
    main()
