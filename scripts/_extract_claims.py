"""Extract fact-checkable claims from RS Edexcel lesson plan."""
import json
import re
import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return " ".join(self.text)


data = json.loads(
    open("scripts/_fact_check/religious-studies-edexcel_plan.json", encoding="utf-8").read()
)

# Quoted strings — curly quotes and straight double quotes
quote_re = re.compile(
    r"[“‘]([^”’“‘]{10,250})[”’]"
    r'|"([^"]{10,250})"'
)
# Scripture references with chapter:verse
scripture_re = re.compile(
    r"\b(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth"
    r"|(?:1|2)\s+Samuel|(?:1|2)\s+Kings|(?:1|2)\s+Chronicles"
    r"|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Songs?"
    r"|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel"
    r"|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi"
    r"|Matthew|Mark|Luke|John|Acts|Romans|(?:1|2)\s+Corinthians|Galatians"
    r"|Ephesians|Philippians|Colossians|(?:1|2)\s+Thessalonians"
    r"|(?:1|2)\s+Timothy|Titus|Philemon|Hebrews|James"
    r"|(?:1|2)\s+Peter|(?:1|2|3)\s+John|Jude|Revelation"
    r"|Surah|Al-Fatiha|Al-Baqarah|Al-Imran|An-Nisa|Al-Maidah|Al-Anam|Al-Araf"
    r"|At-Tawbah|Yunus|Hud|Yusuf|Ibrahim|An-Nahl|Al-Isra|Al-Kahf|Maryam"
    r"|Al-Anbiya|Al-Hajj|Al-Muminun|An-Nur|Al-Ahzab|Al-Hujurat|Qaf"
    r"|Ar-Rahman|Al-Waqiah|Al-Ikhlas|Al-Falaq|An-Nas"
    r")\s+\d+[:\-]\d+",
    re.IGNORECASE,
)
# CCC / Catechism references
ccc_re = re.compile(
    r"CCC\s*\d{3,4}|Catechism.*?paragraph\s*\d{3,4}|paragraph\s*\d{3,4}\b",
    re.IGNORECASE,
)
# Scholar attribution patterns — look for names followed by attribution language
scholars = [
    "Aquinas", "Augustine", "Irenaeus", "Anselm", "al-Ghazali", "Al-Ghazali",
    "Paley", "John Hick", "Hick", "Hume", "Aristotle", "Plato", "Kant",
    "Bonhoeffer", "Romero", "Mother Teresa", "Nagarjuna", "Sankara",
    "Maimonides", "Rambam", "Swinburne", "Mackie", "Dawkins",
]
scholar_re = re.compile(
    r"\b(" + "|".join(re.escape(s) for s in scholars) + r")\b[^.;]{0,120}[.;]",
    re.IGNORECASE,
)

all_claims = []

for lesson in data:
    extractor = TextExtractor()
    extractor.feed(lesson["content_html"])
    text = extractor.get_text()

    lid = f'L{lesson["lesson_number"]} [{lesson["unit_slug"]}] {lesson["lesson_title"]}'

    for m in quote_re.finditer(text):
        q = (m.group(1) or m.group(2) or "").strip()
        if len(q) > 15:
            all_claims.append({"lesson": lid, "type": "quote", "claim": q[:200]})

    for m in scripture_re.finditer(text):
        ctx = text[max(0, m.start() - 50) : min(len(text), m.end() + 80)].strip()
        all_claims.append({"lesson": lid, "type": "scripture", "claim": ctx[:200]})

    for m in ccc_re.finditer(text):
        ctx = text[max(0, m.start() - 40) : min(len(text), m.end() + 80)].strip()
        all_claims.append({"lesson": lid, "type": "catechism", "claim": ctx[:200]})

    for m in scholar_re.finditer(text):
        ctx = text[max(0, m.start() - 20) : min(len(text), m.end() + 20)].strip()
        all_claims.append({"lesson": lid, "type": "scholar", "claim": ctx[:200]})

print(f"Total claims: {len(all_claims)}")
print(f"  Quotes:     {sum(1 for c in all_claims if c['type']=='quote')}")
print(f"  Scripture:  {sum(1 for c in all_claims if c['type']=='scripture')}")
print(f"  Catechism:  {sum(1 for c in all_claims if c['type']=='catechism')}")
print(f"  Scholar:    {sum(1 for c in all_claims if c['type']=='scholar')}")
print()

for c in all_claims:
    print(f"[{c['type'].upper()}] {c['lesson']}")
    print(f"  >> {c['claim']}")
    print()
