# -*- coding: utf-8 -*-
"""Hero image pipeline v2 — vision-gated selection with grounded captions.

Born of the psychology-ocr / psychology-edexcel hero failure (July 2026):
keyword-scored index reuse assigned other subjects' heroes to psychology
lessons, captions described the hoped-for image rather than the actual one,
and nothing deduplicated. Rules this module enforces:

  1. No image is assigned unseen — a vision model judges topical fit.
  2. The caption is written from what the image ACTUALLY shows, plus credit.
  3. One image, one lesson — uniqueness enforced via the shared `used` set.
  4. The stored hero_image_url always lives under the subject's own R2
     folder. No cross-subject URLs, no hotlinks, no site-local paths.
  5. Cross-subject index reuse is banned. Reuse only from an explicit
     same-family pool (e.g. psychology-aqa -> psychology-ocr), still
     vision-gated and re-uploaded under the new subject's own key.

Usage:
    from lib.hero_pipeline import HeroFinder
    finder = HeroFinder()                      # shares one `used` set
    result = finder.find(
        subject_slug="psychology-ocr", subject_name="Psychology",
        unit_slug="memory", unit_name="Memory", lesson_number=1,
        title="Information Processing, Forgetting and the Brain",
        description="...", reuse_pool=[{"url": ..., "title": ..., "caption": ...}])
    # result: {url, caption, alt_base, source, credit} or None
"""
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.unsplash import search_unsplash, trigger_unsplash_download
from lib.pexels import search_pexels
from lib.pixabay import search_pixabay
from lib.wikimedia import search_wikimedia, resize_and_compress, MIN_FILE_SIZE
from lib.r2 import get_r2_client, IMAGES_BUCKET

R2_PUBLIC = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev"
VISION_MODEL = "claude-haiku-4-5-20251001"
MAX_VISION_CHECKS_PER_LESSON = 8

_QUERY_PROMPT = """You suggest stock-photo search queries for the hero image of a GCSE revision lesson (students aged 15-16).

LESSON: {title}
ABOUT: {description}
SUBJECT: {subject_name}

Give 3 short search queries (2-4 words each) likely to find a strong, literal, photographic header image for this topic on a stock-photo site. Prefer concrete visible things over abstractions (for "obedience" suggest "military uniform authority", not "social influence"). Avoid names of specific studies or psychologists — stock sites have no photos of them.

Reply with ONLY a JSON array of 3 strings."""

_VISION_PROMPT = """You are choosing the hero (header) image for a GCSE revision lesson (students aged 15-16).

LESSON: {title}
ABOUT: {description}
SUBJECT: {subject_name}

Look at the image. Reply in EXACTLY this format:

GRADE: A or B or C
SHOWS: one factual sentence (max 18 words) describing what the image actually shows, suitable as its caption. Describe only what is visible — no speculation, no study names unless legibly shown.

Grading:
A = clearly illustrates this lesson's topic; a teacher would nod.
B = acceptable but generic — related mood or setting, not specific to the topic.
C = wrong: unrelated subject matter, text-heavy screenshot, software UI, watermark, logo, meme, or misleading for this topic.
"""


_US_UK = [
    ("colored", "coloured"), ("colorful", "colourful"), ("color", "colour"),
    ("gray", "grey"), ("center", "centre"), ("theater", "theatre"),
    ("artifacts", "artefacts"), ("artifact", "artefact"), ("armor", "armour"),
    ("harbor", "harbour"), ("labeled", "labelled"), ("jewelry", "jewellery"),
    ("plow", "plough"), ("traveling", "travelling"), ("meter", "metre"),
]


def briticise(text):
    """Vision models write American English; captions are British English."""
    for us, uk in _US_UK:
        text = re.sub(rf"\b{us}\b", uk, text)
        text = re.sub(rf"\b{us.capitalize()}\b", uk.capitalize(), text)
    return text


def _grade(text):
    m = re.search(r"GRADE:\s*([ABC])", text)
    return m.group(1) if m else "C"


def _shows(text):
    m = re.search(r"SHOWS:\s*(.+)", text)
    return m.group(1).strip() if m else ""


class HeroFinder:
    def __init__(self, anthropic_client=None, r2_client=None, log=print):
        import anthropic
        self.client = anthropic_client or anthropic.Anthropic()
        self.r2 = r2_client or get_r2_client()
        self.log = log
        # Source identities already assigned (source URLs / photo ids), shared
        # across every lesson this finder touches — the dedupe backbone.
        self.used = set()
        self.vision_calls = 0
        self._src_errors = {}

    def _stock_sources(self):
        """Stock-photo sources in preference order, skipping any that is
        unconfigured or has erred 3+ times in a row (dead quota)."""
        out = [("unsplash", search_unsplash, "Photo")]
        if os.environ.get("PEXELS_API_KEY"):
            out.append(("pexels", search_pexels, "Photo"))
        if os.environ.get("PIXABAY_API_KEY"):
            out.append(("pixabay", search_pixabay, "Image"))
        return [(n, f, c) for n, f, c in out if self._src_errors.get(n, 0) < 3]

    # ---------------------------------------------------------------- model calls

    def suggest_queries(self, title, description, subject_name):
        msg = self.client.messages.create(
            model=VISION_MODEL, max_tokens=200,
            messages=[{"role": "user", "content": _QUERY_PROMPT.format(
                title=title, description=(description or "")[:400],
                subject_name=subject_name)}])
        text = msg.content[0].text.strip()
        m = re.search(r"\[.*\]", text, re.S)
        try:
            queries = json.loads(m.group(0)) if m else []
        except (json.JSONDecodeError, AttributeError):
            queries = []
        return [q for q in queries if isinstance(q, str) and q.strip()][:3] or [title]

    def vision_check(self, jpeg_bytes, title, description, subject_name):
        """Returns (grade 'A'|'B'|'C', shows_sentence)."""
        import base64
        self.vision_calls += 1
        msg = self.client.messages.create(
            model=VISION_MODEL, max_tokens=200,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                             "data": base64.b64encode(jpeg_bytes).decode()}},
                {"type": "text", "text": _VISION_PROMPT.format(
                    title=title, description=(description or "")[:400],
                    subject_name=subject_name)}]}])
        text = msg.content[0].text
        return _grade(text), _shows(text)

    # ---------------------------------------------------------------- plumbing

    def _fetch_jpeg(self, url):
        """Download + resize/compress. Returns jpeg bytes or None."""
        tmp_src = tmp_dst = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".img") as f:
                tmp_src = f.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                tmp_dst = f.name
            # Wikimedia's robot policy 429s generic UAs — be identifiable
            ua = ("StudyVaultHeroBot/1.0 (https://www.studyvault.co.uk; "
                  "studyvault.info@gmail.com)")
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < MIN_FILE_SIZE:
                return None
            with open(tmp_src, "wb") as f:
                f.write(data)
            resize_and_compress(tmp_src, tmp_dst, max_width=1200, quality=82)
            with open(tmp_dst, "rb") as f:
                return f.read()
        except Exception as e:
            self.log(f"      [fetch fail] {url[:80]}: {e}")
            return None
        finally:
            for p in (tmp_src, tmp_dst):
                if p:
                    try:
                        os.unlink(p)
                    except OSError:
                        pass

    def _upload(self, jpeg_bytes, subject_slug, unit_slug, lesson_number):
        r2_key = f"{subject_slug}/{unit_slug}/lesson-{lesson_number:02d}-hero.jpg"
        self.r2.put_object(Bucket=IMAGES_BUCKET, Key=r2_key, Body=jpeg_bytes,
                           ContentType="image/jpeg")
        return f"{R2_PUBLIC}/{r2_key}"

    # ---------------------------------------------------------------- candidates

    def _reuse_candidates(self, reuse_pool, title, description):
        """Lexically shortlist same-family pool entries worth a vision check."""
        words = set(re.findall(r"[a-z]{4,}", f"{title} {description or ''}".lower()))
        scored = []
        for entry in reuse_pool or []:
            if entry["url"] in self.used:
                continue
            ewords = set(re.findall(r"[a-z]{4,}", (entry.get("title") or "").lower()))
            overlap = len(words & ewords)
            if overlap >= 2:
                scored.append((overlap, entry))
        scored.sort(key=lambda t: -t[0])
        return [e for _, e in scored[:3]]

    @staticmethod
    def _extract_credit(caption):
        m = re.search(r"\(([^()]*(?:Unsplash|Wikimedia|Photo)[^()]*)\)\s*$", caption or "")
        return m.group(1) if m else ""

    # ---------------------------------------------------------------- main entry

    @staticmethod
    def _trust_description(title, description):
        """A description that shares almost nothing with its own title is
        stale or mis-assigned (see science-edexcel, July 2026). Searching on
        it sends the finder hunting for the wrong subject entirely, so drop
        it and let the title lead."""
        if not description:
            return ""
        tw = set(re.findall(r"[a-z]{4,}", (title or "").lower()))
        dw = set(re.findall(r"[a-z]{4,}", description.lower()))
        if not tw or not dw:
            return description
        return "" if not (tw & dw) else description

    def find(self, subject_slug, subject_name, unit_slug, unit_name,
             lesson_number, title, description, reuse_pool=None):
        """Find, vision-gate, and upload one hero. Returns
        {url, caption, source, credit, shows} or None."""
        description = self._trust_description(title, description)
        checks_left = MAX_VISION_CHECKS_PER_LESSON
        seconds = []  # every B-grade seen; the most topical one wins if no A
        cur_query = ""  # the search phrase that surfaced the candidate

        def consider(jpeg, credit, source, source_id):
            nonlocal checks_left
            if jpeg is None or checks_left <= 0:
                return None
            checks_left -= 1
            grade, shows = self.vision_check(jpeg, title, description, subject_name)
            self.log(f"      [vision {grade}] {source}: {shows[:80]}")
            if grade == "A":
                return (jpeg, shows, credit, source, source_id)
            if grade == "B":
                seconds.append((jpeg, shows, credit, source, source_id, cur_query))
            return None

        def stems(text):
            # 5-char prefixes so system/systems and hormone/hormonal match
            return {w[:5] for w in re.findall(r"[a-z]{4,}", (text or "").lower())}

        def best_second():
            """Rank B-grades by topical overlap with the lesson (and with the
            query that found them) — stops a generic stock photo of a person
            beating an anatomical diagram just by being seen first."""
            if not seconds:
                return None
            want = stems(f"{title} {description or ''} {subject_name}")
            return max(seconds, key=lambda c: len(want & stems(
                f"{c[1]} {c[5] if len(c) > 5 else ''}")))

        winner = None

        # 1. Same-family reuse pool (explicit, never the cross-subject index)
        for entry in self._reuse_candidates(reuse_pool, title, description):
            self.log(f"      trying reuse: {entry['url'][:70]}")
            winner = consider(self._fetch_jpeg(entry["url"]),
                              self._extract_credit(entry.get("caption")),
                              "reuse", entry["url"])
            if winner:
                break

        # 2. Stock search — model-suggested queries across every available
        # source (Unsplash / Pexels / Pixabay), skipping used photos. A source
        # that keeps erroring (exhausted quota) is dropped for this run.
        if not winner:
            for query in self.suggest_queries(title, description, subject_name):
                if checks_left <= 0:
                    break
                cur_query = query
                for src_name, search_fn, credit_word in self._stock_sources():
                    if checks_left <= 0 or winner:
                        break
                    self.log(f"      {src_name}: '{query}'")
                    try:
                        results = search_fn(query, per_page=6)
                        self._src_errors[src_name] = 0
                    except Exception as e:
                        self._src_errors[src_name] = self._src_errors.get(src_name, 0) + 1
                        self.log(f"      {src_name} error ({self._src_errors[src_name]}): {e}")
                        continue
                    for photo in results[:2]:
                        pid = photo["url"].split("?")[0]
                        if pid in self.used:
                            continue
                        credit = f"{credit_word}: {photo['photographer']} / {src_name.capitalize()}" \
                            if photo.get("photographer") else src_name.capitalize()
                        winner = consider(self._fetch_jpeg(photo["url"]), credit,
                                          src_name, pid)
                        if winner:
                            if src_name == "unsplash":
                                try:
                                    trigger_unsplash_download(photo.get("_download_location", ""))
                                except Exception:
                                    pass
                            break
                        if checks_left <= 0:
                            break
                if winner:
                    break
                time.sleep(0.5)

        # 3. Wikimedia last resort
        if not winner and checks_left > 0:
            for query in self.suggest_queries(title, description, subject_name)[:2]:
                if checks_left <= 0:
                    break
                cur_query = query
                self.log(f"      Wikimedia: '{query}'")
                try:
                    results = search_wikimedia(query, limit=10)
                except Exception as e:
                    self.log(f"      Wikimedia error: {e}")
                    continue
                for cand in results[:3]:
                    curl = cand.get("url") or cand.get("original_url", "")
                    if not curl or curl in self.used:
                        continue
                    winner = consider(self._fetch_jpeg(curl), "Wikimedia Commons",
                                      "wikimedia", curl)
                    if winner:
                        break
                    if checks_left <= 0:
                        break
                if winner:
                    break
                time.sleep(2)

        if not winner:
            winner = best_second()  # settle for the most topical B
        if not winner:
            return None

        jpeg, shows, credit, source, source_id = winner[:5]
        self.used.add(source_id)
        url = self._upload(jpeg, subject_slug, unit_slug, lesson_number)
        self.used.add(url)
        shows = briticise(shows)
        caption = f"{shows.rstrip('.')} ({credit})" if credit else shows.rstrip(".") + "."
        return {"url": url, "caption": caption, "source": source,
                "credit": credit, "shows": shows}
