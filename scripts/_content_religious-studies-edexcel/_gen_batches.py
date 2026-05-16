"""Generate all 7 batch JSON files for RS Edexcel content agents."""
import json
import re
from pathlib import Path

plan = json.loads(Path("scripts/_plan_religious-studies-edexcel.json").read_text("utf-8"))


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[''′']", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


units_by_slug = {}
for unit in plan["article_units"]:
    used = set()
    lessons_with_slugs = []
    for L in unit["lessons"]:
        base = slugify(L["title"]) or f"lesson-{L['number']}"
        slug = base
        i = 2
        while slug in used:
            slug = f"{base}-{i}"
            i += 1
        used.add(slug)
        lessons_with_slugs.append({**L, "lesson_slug": slug})
    units_by_slug[unit["slug"]] = {"meta": unit, "lessons": lessons_with_slugs}

subject_meta = {
    "name": "Religious Studies",
    "exam_board": "Edexcel",
    "spec_code": "1RA0",
}
question_type_names = plan["question_type_names"]
teaching_brief = plan["teaching_brief"]

workspace = Path("scripts/_content_religious-studies-edexcel")

batches = [
    {
        "batch_id": "b01",
        "unit_slugs": ["paper-1-catholic-christianity"],
        "batch_teaching_note": (
            "Paper 1 Catholic Christianity = highest weighting (50%). Starred spec points "
            "1A 1.8* (eschatology) and 1A 2.2* (liturgical worship) anchor Discuss questions. "
            "Sources of Wisdom (section 3) and Forms of Expression (section 4) are Edexcel-unique "
            "— do not shortchange them. L06 is fresh content: Vatican II documents, four marks of "
            "the Church, magisterium, Catholic art/architecture/music/symbolism."
        ),
    },
    {
        "batch_id": "b02",
        "unit_slugs": ["paper-1-christianity"],
        "batch_teaching_note": (
            "Paper 1 Christianity (denomination-wide). Starred: 1B 1.6* (eschatology), "
            "1B 2.1* (worship). L03 covers problem of evil — beware Augustinian/Irenaean/Hick "
            "conflation. Sources/Forms sections are Edexcel-unique for L06 (Bible authority, "
            "denominations including Filioque, role of women, Christian art/music including "
            "CS Lewis as spec-named author). L06 is fresh content."
        ),
    },
    {
        "batch_id": "b03",
        "unit_slugs": ["paper-1-islam"],
        "batch_teaching_note": (
            "Paper 1 Islam. Starred: 1C 1.8* (akhirah), 1C 2.3* (salah/worship). "
            "Jihad framing critical — never reduce to holy war/inner struggle binary. "
            "Sources of Authority (section 3) and Muslim Identity (section 4) are "
            "Edexcel-unique for L06: Sufi figures al-Ghazali, ibn al-Arabi and "
            "Rabi'a al-Adawiyya are spec-named — get their bios right. L06 is fresh content."
        ),
    },
    {
        "batch_id": "b04",
        "unit_slugs": [
            "paper-2-buddhism",
            "paper-2-hinduism",
            "paper-2-judaism",
            "paper-2-sikhism",
        ],
        "batch_teaching_note": (
            "Paper 2 second-religion units (4 lessons each = 16 total). No Sources/Forms "
            "sections. Edexcel-specific anchor texts for Buddhism (Buddhavamsa, Milinda Panha, "
            "named Suttas). Hinduism cosmology (yugas, maya, prakriti, tri-guna) more developed "
            "than AQA. Judaism: 'the Almighty' is Edexcel's formal name for God. Sikhism: "
            "Guru Granth Sahib page numbers are the citation format. Starred comparison-marked "
            "spec points: 2D 1.5* (Buddhism cessation/afterlife), 2E 1.5* (Hindu life after death), "
            "2F 1.8* (Jewish afterlife), 2G 1.4* (Sikh mukti/afterlife)."
        ),
    },
    {
        "batch_id": "b05",
        "unit_slugs": [
            "paper-2-catholic-christianity",
            "paper-2-christianity",
            "paper-2-islam",
        ],
        "batch_teaching_note": (
            "Paper 2 Abrahamic second-religion units (4 lessons each = 12 total). These reuse "
            "Paper 1 content but compressed — no Sources/Forms sections. Frame the intro for "
            "students whose main religion is a different tradition (e.g. a student taking "
            "Islam as Paper 1 now studying Catholic Christianity as Paper 2). "
            "All content_transfer scores are HIGH — refer to _aqa_source_lessons.json. "
            "Starred spec points: 2A 1.8*, 2A 2.2*, 2B 1.6*, 2B 2.1*, 2C 1.8*, 2C 2.3*."
        ),
    },
    {
        "batch_id": "b06",
        "unit_slugs": [
            "paper-3-philosophy-ethics-catholic",
            "paper-3-philosophy-ethics-christianity",
            "paper-3-philosophy-ethics-islam",
        ],
        "batch_teaching_note": (
            "Paper 3 Philosophy & Ethics — 3 religion routes (5 lessons each = 15 total). "
            "CRITICAL fact-check zone: Aquinas's First Three Ways (motion, causation, "
            "contingency) — NOT seven, NOT Ontological, NOT kalam; kalam cosmological argument "
            "= al-Ghazali (Edexcel 3C 1.6), NOT Aquinas; soul-making theodicy = Irenaeus/Hick "
            "NOT Augustine; Augustine = free-will defence (privation of good). "
            "Paper 3A (Catholic) requires Catechism paragraph numbers and named papal documents. "
            "Paper 3B (Christianity) is denomination-wide. Paper 3C (Islam) uses Qur'an + "
            "Hadith anchors. All lessons are MEDIUM transfer — AQA Themes A + C are sources "
            "but require religion-specific rework. 3B L03 (Religious Upbringing as Argument) "
            "is fresh — no AQA source."
        ),
    },
    {
        "batch_id": "b07",
        "unit_slugs": ["paper-4-marks-gospel", "paper-4-quran"],
        "batch_teaching_note": (
            "Paper 4 Textual Studies — ALL FRESH CONTENT (no AQA source; content_transfer "
            "scores are all 'fresh'). Mark's Gospel (5 lessons): STOP at Mark 16:8. Never "
            "cite 16:9-20. All passage references in section_markers are spec-verified — "
            "preserve them exactly. Elias = Edexcel archaic spelling of Elijah. "
            "The Qur'an (5 lessons): Surah 4:157-158 on Isa must be presented respectfully "
            "as Islamic theological position. The son in Ibrahim's sacrifice story is "
            "traditionally Ismail per most Muslim scholars — note the debate as the spec does. "
            "Paper 4 students rely most heavily on these lesson notes — be explicit and "
            "passage-focused."
        ),
    },
]


def make_lesson_entry(L, lesson_slug):
    return {
        "lesson_id": "LOOKUP_BY_SLUG",
        "lesson_slug": lesson_slug,
        "number": L["number"],
        "title": L["title"],
        "description": L.get("description", ""),
        "spec_references": L.get("spec_references", []),
        "section_markers": L.get("section_markers", []),
        "content_transfer": L.get("content_transfer", {}),
    }


total_lessons = 0
for batch in batches:
    batch_id = batch["batch_id"]
    lessons_in_batch = []
    for unit_slug in batch["unit_slugs"]:
        unit_data = units_by_slug[unit_slug]
        for L_with_slug in unit_data["lessons"]:
            lessons_in_batch.append(
                make_lesson_entry(L_with_slug, L_with_slug["lesson_slug"])
            )

    batch_json = {
        "batch_id": batch_id,
        "subject_slug": "religious-studies-edexcel",
        "unit_slugs": batch["unit_slugs"],
        "subject_meta": subject_meta,
        "question_type_names": question_type_names,
        "subject_level_teaching_brief": teaching_brief,
        "batch_teaching_note": batch["batch_teaching_note"],
        "reference_lesson_path": "scripts/_content_religious-studies-edexcel/_reference_lesson.json",
        "aqa_source_lessons_path": "scripts/_content_religious-studies-edexcel/_aqa_source_lessons.json",
        "lessons_in_batch": lessons_in_batch,
    }

    out_path = workspace / f"_batch_{batch_id}.json"
    out_path.write_text(
        json.dumps(batch_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    total_lessons += len(lessons_in_batch)
    print(
        f"Written {out_path.name}: {len(lessons_in_batch)} lessons "
        f"({', '.join(batch['unit_slugs'])})"
    )

print(f"\nTotal lessons across all batches: {total_lessons}")
