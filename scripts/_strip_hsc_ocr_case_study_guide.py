"""One-off: drop the 10-mark Case Study Response exam-technique guide from
HSC OCR (it doesn't apply — OCR R032 has no 10-mark question type).

Steps:
1. Hard-delete /guide/health-social-care-ocr/exam-technique/case-study
2. Strip the corresponding card from /exam-technique/index
3. Strip <li> sidebar entries pointing at it
4. Strip the 'Next →' nav link from the evaluate guide (it was the previous step)
5. Body-prose pass: replace '8 and 10 mark' with OCR-correct '6 and 8 mark
   extended response'

Kept here as a reference for future cross-board guide imports where the
source board has a question type the target board doesn't.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()
sid = sb.table("subjects").select("id").eq("slug", "health-social-care-ocr").is_("school_id", "null").execute().data[0]["id"]

# 1. Hard-delete
cs = sb.table("guide_pages").select("id, title").eq("subject_id", sid).eq("guide_type", "exam-technique").eq("slug", "case-study").execute().data
if cs:
    sb.table("guide_pages").delete().eq("id", cs[0]["id"]).execute()
    print(f"Deleted: {cs[0]['title']}")
else:
    print("Already deleted.")

# 2. Strip from exam-technique/index
idx_row = sb.table("guide_pages").select("id, content_html").eq("subject_id", sid).eq("guide_type", "exam-technique").eq("slug", "index").execute().data
if idx_row:
    h = idx_row[0]["content_html"]
    new = re.sub(r'\s*<a\s+class="guide-question-card"\s+href="[^"]*case-study"[^>]*>.*?</a>', "", h, flags=re.DOTALL)
    if new != h:
        sb.table("guide_pages").update({"content_html": new}).eq("id", idx_row[0]["id"]).execute()
        print("Stripped card from exam-technique/index")

# 3. Strip <li> sidebar entries + 4. Strip 'Next →' nav link in all guides
guides = sb.table("guide_pages").select("id, guide_type, slug, content_html").eq("subject_id", sid).execute().data
for g in guides:
    h = g["content_html"]
    new = re.sub(r'\s*<li>\s*<a[^>]*href="[^"]*/exam-technique/case-study"[^>]*>.*?</a>\s*</li>', "", h, flags=re.DOTALL)
    new = re.sub(r'\s*<a\s+class="guide-nav-link guide-nav-next"\s+href="[^"]*/exam-technique/case-study"[^>]*>.*?</a>', "", new, flags=re.DOTALL)
    new = re.sub(r'href="(/guide/[^"]*)/exam-technique/case-study"', r'href="\1/exam-technique/evaluate"', new)
    if new != h:
        sb.table("guide_pages").update({"content_html": new}).eq("id", g["id"]).execute()
        print(f"Cleaned: {g['guide_type']}/{g['slug']}")

# 5. Body prose: 8 and 10 mark → 6 and 8 mark extended response
ppp = sb.table("guide_pages").select("id, content_html").eq("subject_id", sid).eq("guide_type", "revision-technique").eq("slug", "past-paper-practice").execute().data
if ppp:
    h = ppp[0]["content_html"]
    new = h.replace("8 and 10 mark questions", "6 and 8 mark extended response questions")
    if new != h:
        sb.table("guide_pages").update({"content_html": new}).eq("id", ppp[0]["id"]).execute()
        print("Fixed past-paper-practice prose '8 and 10 mark'")
