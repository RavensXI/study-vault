# Fact-check — religious-studies-b-edexcel

Checked 6 lessons. HIGH=4 MED=5 LOW=3

- **low** `area1-catholic-christianity-L06` [knowledge_checks]: The distractor 'death' is semantically identical to the keyed answer 'end' ('sacred from beginning to natural death' is standard phrasing of the same teaching), so the item has two defensible correct answers and a studen → Replace the ambiguous distractor: "The Catechism of the Catholic Church (2276–2279) teaches that human life is sacred from beginning to natural _____." Options:
- **high** `area1-christianity-L03` [content_html]: Expecting ',' delimiter: line 1 column 1367 (char 1366) → 
- **high** `area1-christianity-L04` [content_html]: Expecting ',' delimiter: line 1 column 2643 (char 2642) → 
- **medium** `area2-islam-L01` [content_html]: The hadith reference for the Six Beliefs of Sunni Islam (the Hadith of Jibril in Sahih Muslim, Book of Faith) is cited as Kitab al-Iman 1:1 in the board's Islam Beliefs content and in the endorsed textbooks, not 1:4. A w → based on a hadith known as <strong>Kitab al-Iman 1:1</strong>
- **medium** `area2-islam-L01` [content_html]: Same mis-citation repeated in the Key Fact box: the hadith source for the Six Beliefs is Kitab al-Iman 1:1 (Sahih Muslim, Book of Faith), not 1:4. → They come from Kitab al-Iman 1:1 and are the foundation of Sunni religious identity.
- **medium** `area2-islam-L01` [knowledge_checks]: The correct answer given is a mis-citation; the hadith reference is Kitab al-Iman 1:1. Students would memorise an incorrect source reference. → The Sunni Six Beliefs come from a hadith known as _____. — Kitab al-Iman 1:1
- **medium** `area2-islam-L01` [flashcard_questions]: Mis-citation of the hadith reference; the Six Beliefs come from Kitab al-Iman 1:1 (Sahih Muslim, Book of Faith). → What source gives the Sunni Six Beliefs? — Kitab al-Iman 1:1, a hadith of the Prophet.
- **medium** `area2-islam-L01` [conclusion_html]: Same mis-citation in the takeaways; the source is Kitab al-Iman 1:1. → Sunni Islam holds the Six Beliefs (Allah, Angels, Books, Prophets, Day of Judgement, al-Qadr) from Kitab al-Iman 1:1
- **low** `area2-islam-L01` [content_html]: Imprecise: 'Sevener' strictly describes those who hold Isma'il ibn Ja'far to be the seventh and final Imam; Isma'ilis more broadly (e.g. the Nizari Isma'ilis, led today by the Aga Khan) continue a living line of Imams, s → <strong>Sevener</strong> Shi'a Muslims recognise a different line of succession, ending with the seventh Imam; they are associated with the wider Isma'ili tradi
- **low** `area2-islam-L01` [exam_tip_html]: Student-facing text should not refer students to the board's specification document (site language policy: lessons say 'the exam board', 'your exam', 'this paper'); the point can be made without it. → both are named in the content you are examined on, so they are safe, accurate citations
- **high** `area2-islam-L04` [content_html]: Expecting ',' delimiter: line 1 column 3498 (char 3497) → 
- **high** `area2-judaism-L05` [content_html]: Expecting ',' delimiter: line 1 column 1394 (char 1393) → 

## Re-check of the six partially checked lessons (17 Sep 2026)

The first round's replies for six lessons were cut short. They were re-run at a 32k budget with `factcheck_only`.
Two parsed cleanly; four came back one closing bracket short and were recovered from the batch without re-spending
(the driver's `parse_json_reply` now closes such a reply itself). Findings across the six: 4 high (all parse artefacts,
discarded), 8 medium, 10 low. Applied and re-narrated:

- `area2-islam-L01`: the hadith source for the Six Beliefs mis-cited as Kitab al-Iman 1:4 in five places, now 1:1 throughout.
- `area2-islam-L04`: Surah 3:17 and 3:18 were run together; the praise of the patient and truthful (3:17) is now kept apart from the witness of Allah (3:18).
- `area1-christianity-L04`: a practice question cited the wrong Article of Religion for the two sacraments; now Article XXV.
- `area2-judaism-L05`: list-style flashcards split into single-answer cards.
- `area1-christianity-L03` and `area1-catholic-christianity-L06`: low findings only, nothing applied.

All 22 lessons have now had a complete fact-check. Backups of the rows as they were before each write-back are in the session scratchpad.
