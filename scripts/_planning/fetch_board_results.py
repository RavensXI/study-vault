"""Download and parse the four boards' own GCSE results statistics for the
June 2025 and June 2026 series, and write per-specification entry counts to
scripts/_planning/board_entries.json.

June 2025 is the series the DfE 2024/25 KS4 dataset counts, so the 2025 numbers
are the ones the report's shares must be built from. June 2026 is carried as a
second column showing the direction of travel.

Source documents are cached outside the repo (they are large binaries).
Read-only with respect to the repo and the database.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(tempfile.gettempdir(), "studyvault_board_results")
UA = {"User-Agent": "Mozilla/5.0 (StudyVault-research)"}

SOURCES = {
    # ---- June 2025 (the series behind DfE 2024/25) --------------------------
    ("AQA", 2025): {
        "file": "aqa_2025.xlsx", "kind": "aqa",
        "title": "AQA - GCSE Results statistics June 2025 (provisional)",
        "url": "https://www.aqa.org.uk/files/308c1e70-dc8d-4263-8719-d0f10f869a7f/"
               "d1c20b6fb8a0b39dd217019c50a02bd1cae10f99.xlsx",
        "page": "https://www.aqa.org.uk/exams-administration/results-days/results-statistics",
    },
    ("Edexcel", 2025): {
        "file": "pearson_2025.pdf", "kind": "pearson", "gzip": True,
        "title": "Pearson - Grade Statistics (Provisional), June 2025 GCSE (9-1) "
                 "Specifications, UK Only (withdrawn from pearson.com; served from "
                 "the Internet Archive snapshot of 31 Jan 2026)",
        "url": "https://web.archive.org/web/20260131173541id_/"
               "https://qualifications.pearson.com/content/dam/pdf/Support/"
               "Grade-statistics/GCSE/grade-statistics-june-2025-provisional-gcse-9-1-"
               "specifications.pdf",
        "page": "https://qualifications.pearson.com/en/support/support-topics/"
                "results-certification/grade-statistics.html",
    },
    ("OCR", 2025): {
        "file": "ocr_2025.pdf", "kind": "ocr",
        "title": "OCR - GCSE, Cambridge Nationals and Entry Level provisional "
                 "results statistics, June 2025",
        "url": "https://www.ocr.org.uk/Images/739518-gcse-cambridge-nationals-and-"
               "entry-level-provisional-results-statistics-june-2025.pdf",
        "page": "https://www.ocr.org.uk/administration/results-and-post-results/results/",
    },
    ("Eduqas", 2025): {
        "file": "eduqas_2025.pdf", "kind": "eduqas",
        "title": "WJEC Eduqas - Provisional GCSE Results June 2025",
        "url": "https://www.eduqas.co.uk/media/a33nq5bz/eduqas-gcse-provisional-results-2025.pdf",
        "page": "https://www.eduqas.co.uk/home/results-and-grade-boundaries/",
    },
    # ---- June 2026 (direction of travel) -----------------------------------
    ("AQA", 2026): {
        "file": "aqa_2026.xlsx", "kind": "aqa",
        "title": "AQA - GCSE Results statistics June 2026 (provisional)",
        "url": "https://www.aqa.org.uk/files/O4uKDQoYRUXkVFZ2MUl0F7/"
               "ed0a9ba76dcc3378655f3765543b96275f9fdc7e.xlsx",
        "page": "https://www.aqa.org.uk/exams-administration/results-days/results-statistics",
    },
    ("Edexcel", 2026): {
        "file": "pearson_2026.pdf", "kind": "pearson",
        "title": "Pearson - Grade Statistics (Provisional), June 2026 GCSE (9-1) "
                 "Specifications, UK Only",
        "url": "https://qualifications.pearson.com/content/dam/pdf/Support/"
               "Grade-statistics/GCSE/grade-statistics-june-2026-provisional-gcse-9-1-"
               "specifications.pdf",
        "page": "https://qualifications.pearson.com/en/support/support-topics/"
                "results-certification/grade-statistics.html",
    },
    ("OCR", 2026): {
        "file": "ocr_2026.pdf", "kind": "ocr",
        "title": "OCR - GCSE, Cambridge Nationals and Entry Level provisional "
                 "results statistics, June 2026",
        "url": "https://ocr.org.uk/Images/760870-gcse-cambridge-nationals-and-entry-"
               "level-provisional-results-statistics-june-2026.pdf",
        "page": "https://www.ocr.org.uk/administration/results-and-post-results/results/",
    },
    ("Eduqas", 2026): {
        "file": "eduqas_2026.pdf", "kind": "eduqas",
        "title": "WJEC Eduqas - Provisional GCSE Results June 2026",
        "url": "https://www.eduqas.co.uk/media/5mvobewy/gcse-eduqas-provisional-results-june-2026.pdf",
        "page": "https://www.eduqas.co.uk/home/results-and-grade-boundaries/",
    },
}


def fetch(meta, seed_dir=None):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, meta["file"])
    if os.path.exists(path) and os.path.getsize(path) > 20000:
        return path
    if seed_dir:
        seed = os.path.join(seed_dir, meta["file"])
        if os.path.exists(seed):
            open(path, "wb").write(open(seed, "rb").read())
            return path
    req = urllib.request.Request(meta["url"], headers=UA)
    raw = urllib.request.urlopen(req, timeout=180).read()
    if raw[:2] == b"\x1f\x8b":                      # archive.org serves gzip
        import gzip
        raw = gzip.decompress(raw)
    if raw[:5].lower() == b"<!doc":
        raise RuntimeError(f"{meta['file']}: got HTML, not the document")
    open(path, "wb").write(raw)
    return path


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def parse_aqa(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {}
    for sn in wb.sheetnames:
        for row in wb[sn].iter_rows(values_only=True):
            if not row or len(row) < 3:
                continue
            code, title, entry = row[0], row[1], row[2]
            if not code or not title or entry in (None, ""):
                continue
            code, title = str(code).strip(), str(title).strip()
            if not re.fullmatch(r"\d{4}", code):
                continue
            try:
                n = int(str(entry).replace(",", "").strip())
            except ValueError:
                continue
            # AQA splits English/Maths by candidate age; keep only the Total row.
            if re.search(r"\((?:15 and under|16|17 and over)\)$", title):
                continue
            title = re.sub(r"\s+Total$", "", title)
            out[(code, title.upper())] = {"entries": n, "sheet": sn}
    return out


def parse_pearson(path):
    """Pearson has used two layouts. 2026: one line per spec,
    'Subject 1ST0 Subject Name STATISTICS Total Sat 31836'. 2025: a block per
    spec, 'Subject . . . . : 1AA0  ARABIC' followed by a 'Sat 9 8 ...' header
    and a row of counts whose FIRST number is the entry ('Sat'). Both files are
    HOME candidates only."""
    text = pdf_text(path)
    out = {}
    for m in re.finditer(
            r"Subject\s+([0-9A-Z]{4})\s+Subject Name\s+(.+?)\s+Total Sat\s+([\d,]+)",
            text):
        out[(m.group(1), m.group(2).strip().upper())] = {
            "entries": int(m.group(3).replace(",", "")), "sheet": "GCSE"}
    if out:
        return out
    blocks = re.split(r"Subject\s*[\.\s]*:\s*", text)[1:]
    for b in blocks:
        head = re.match(r"([0-9A-Z]{4})\s+([^\n]+)", b)
        if not head:
            continue
        # Grade header is "Sat 9 8 ... 1 U" for single awards and
        # "Sat 9-9 9-8 ... 1-1 U" for the double award.
        row = re.search(r"Sat\s+(?:[\d\-]+\s+){5,}U\s*\n\s*([\d,]+)", b)
        if not row:
            continue
        out[(head.group(1), head.group(2).strip().upper())] = {
            "entries": int(row.group(1).replace(",", "")), "sheet": "GCSE"}
    return out


def parse_ocr(path):
    out = {}
    # "Title (QN: 603/0664/6) J198 140 355 ... 1553"  -> last integer is the total
    for line in pdf_text(path).splitlines():
        m = re.match(r"^(.*?)\s*\(QN:[^)]*\)\s+([A-Z]\d{3})\s+((?:[\d,]+\s+){5,}[\d,]+)\s*$",
                     line.strip())
        if not m:
            continue
        nums = [int(x.replace(",", "")) for x in m.group(3).split()]
        out[(m.group(2), m.group(1).strip().upper())] = {
            "entries": nums[-1], "sheet": "GCSE"}
    return out


def parse_eduqas(path):
    """The Eduqas PDF holds four tables: full course, full course by gender,
    SHORT course, and short course by gender. Only the full-course table counts
    - the DfE query excludes short courses - so section tracking is essential.
    Row shape: ' Subject  Centres Candidates  9 8 7 ...'."""
    out, live = {}, False
    for line in pdf_text(path).splitlines():
        head = re.search(r"WJEC Eduqas (?:Provisional|Final) GCSE(.*?)Results(.*)$",
                         line, re.I)
        if head:
            live = ("short course" not in head.group(1).lower()
                    and "gender" not in head.group(2).lower())
            continue
        if not live:
            continue
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9&:,'\-\(\) /\.]+?)\s+([\d,]{1,7})\s+"
                     r"([\d,]{1,9})\s+(\d+\.\d.*)$", line)
        if not m:
            continue
        name = m.group(1).strip().upper()
        if name.startswith(("SUBJECT", "PUBLISHED", "COPYRIGHT", "TOTAL")):
            continue
        out[(None, name)] = {"entries": int(m.group(3).replace(",", "")),
                             "centres": int(m.group(2).replace(",", "")),
                             "sheet": "GCSE"}
    return out


PARSERS = {"aqa": parse_aqa, "pearson": parse_pearson,
           "ocr": parse_ocr, "eduqas": parse_eduqas}


def main():
    seed = sys.argv[1] if len(sys.argv) > 1 else None
    result = {"sources": {}, "entries": {}}
    for (board, year), meta in SOURCES.items():
        try:
            path = fetch(meta, seed)
            rows = PARSERS[meta["kind"]](path)
        except Exception as exc:                     # noqa: BLE001
            print(f"  !! {board} {year}: {exc}")
            result["sources"][f"{board}|{year}"] = {"title": meta["title"],
                                                    "url": meta["url"],
                                                    "page": meta["page"],
                                                    "error": str(exc)}
            continue
        result["sources"][f"{board}|{year}"] = {"title": meta["title"],
                                                "url": meta["url"],
                                                "page": meta["page"],
                                                "specs": len(rows)}
        result["entries"][f"{board}|{year}"] = [
            {"spec_code": k[0], "title": k[1], **v} for k, v in sorted(
                rows.items(), key=lambda kv: kv[0][1])]
        print(f"  {board} {year}: {len(rows)} specifications")

    out = os.path.join(HERE, "board_entries.json")
    json.dump(result, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
