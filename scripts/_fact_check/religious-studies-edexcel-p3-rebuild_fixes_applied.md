# Fixes applied — religious-studies-edexcel-p3-rebuild

All 11 HIGH/MEDIUM findings were applied to the lesson JSON and re-validated
(3 PASS / 0 FAIL), then written to Supabase. Verified present in the final rows:

- [medium] `paper-3-philosophy-ethics-christianity-L04` content_html — This made the Methodist Church the largest Christian denomination in Britain to permit same-sex marriage, following earlier decisions by Quakers, the United Reformed Chur
- [medium] `paper-3-philosophy-ethics-christianity-L04` exam_tip_html — the specification requires you to reference one source of wisdom or authority in support of your explanation, so name the source and show how it supports the point you ar
- [medium] `paper-3-philosophy-ethics-christianity-L04` content_html — the priest crowns the bride and groom as king and queen of a new Christian household, the crowns also symbolising the glory and self-sacrifice of married love
- [medium] `paper-3-philosophy-ethics-christianity-L05` content_html — the Orthodox Church, applying the principle of oikonomia (pastoral flexibility), permits a second, and in some cases a third, marriage, celebrated with a distinct peniten
- [medium] `paper-3-philosophy-ethics-christianity-L05` flashcard_questions — Q: 'What is oikonomia in Orthodox Christianity?' A: 'The principle of pastoral flexibility that allows a penitential second or third marriage after a marriage has broken 
- [medium] `paper-3-philosophy-ethics-christianity-L05` exam_tip_html — the specification requires you to reference one source of wisdom or authority in a 5-mark 'Explain two' answer, so an answer without one cannot gain full credit
- [high] `paper-3-philosophy-ethics-islam-L05` content_html — Non-religious Humanists generally see family planning as a matter of personal autonomy and responsible parenthood, judging each case by its likely consequences for the fa
- [high] `paper-3-philosophy-ethics-islam-L05` glossary_terms — situation ethics — A Christian ethical theory developed by Joseph Fletcher in the 1960s, which rejects fixed rules and judges the right action by whichever choice is the 
- [medium] `paper-3-philosophy-ethics-islam-L05` exam_tip_html — On the 12-mark evaluation, include a non-religious viewpoint as well as divergent Muslim views (Sunni and Shi'a, or traditionalist and reformist): the Evaluate command wo
- [medium] `paper-3-philosophy-ethics-islam-L05` flashcard_questions — Split into separate cards: (1) Q: 'In what language does Shi'a law require a talaq to be pronounced?' A: 'Arabic.' (2) Q: 'Who must be present when a talaq is pronounced 
- [medium] `paper-3-philosophy-ethics-islam-L05` content_html — only once the wife's 'iddah is complete is she free to remarry, and the divorce becomes final

One manual repair followed the apply stage: the corrected situation-ethics
sentence in the Islam lesson lost its inline `<dfn class="term">` wrapper,
leaving 7 glossary_terms against 6 `<dfn>` elements. The wrapper was restored
by hand (no API call) and the lesson re-validated clean.
