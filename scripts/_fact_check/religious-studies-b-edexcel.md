# Fact-check — Religious Studies B (Edexcel 1RB0)

Build of 16 September 2026. Subject `religious-studies-b-edexcel`, 22 article
lessons in 4 units, all inserted at `pending_review`.

## How the check was run

- Model: Opus (`claude-opus-5`), one call per lesson, through the Batch API.
- **Web search OFF** (`factcheck_search_max: 0`). For this qualification the
  specification is the authority, and each lesson's own quoted content points
  are the authority for its scope. The web is a competing authority that
  invents specification detail, so it is not consulted.
- **`assessment_rules_doc` required.** The runner refuses to fact-check without
  it (`scripts/api_build/run_rs_b_edexcel.py`, `stage_factcheck`). The document
  is `scripts/api_build/_rs_b_assessment_rules_1RB0.txt`: the specification's own
  assessment chapters quoted verbatim — the two-papers shape, the
  different-religion rule, four questions each in parts (a) to (d), 1h45 and 102
  marks per paper, SPaG at a minimum of 5%, the Appendix 3 command-word tariffs,
  the assessment objectives, and an explicit list of what the specification does
  NOT state and therefore must not be claimed. Without it the checker judges exam
  claims against nothing and calls true exam facts fabricated, which is exactly
  what happened on Media Eduqas on 15 September.
- Extra instruction for this subject: scripture and source references are checked
  hard (a cited passage must say what the lesson claims), teachings must belong to
  the tradition named, and a religion the specification asks to be shown as
  divided must not be flattened into one voice.

## Counts

| Severity | Findings |
|---|---|
| HIGH | 5 |
| MEDIUM | 40 |
| LOW | 28 |
| **Total** | **73** across 22 lessons |

HIGH and MEDIUM findings were applied to the lesson JSON by a second Batch pass
(`applyfixes`), re-validated, then inserted. LOW findings were recorded and left:
they are imprecision that does not cost a mark, and each rewrite risks the
narration IDs.

Lessons corrected: 18 of 22 (area1-catholic-christianity-L02, area1-catholic-christianity-L03, area1-catholic-christianity-L04, area1-catholic-christianity-L05, area1-catholic-christianity-L06, area1-christianity-L01, area1-christianity-L04, area1-christianity-L05, area1-christianity-L06, area2-islam-L01, area2-islam-L02, area2-islam-L03, area2-islam-L04, area2-judaism-L01, area2-judaism-L02, area2-judaism-L03, area2-judaism-L04, area2-judaism-L05).

## A caveat on completeness

The checker's reply is a JSON array of findings. On the first pass 12 of the 22
replies ended part-way through that array, and the driver's strict parser threw
the whole reply away and recorded a single fake HIGH finding reading
"(parse failure)" — which both overstated the result and lost every real
finding in it. Those 12 lessons were re-checked at double the output budget, and
every reply is now read with a recovering parser that keeps each COMPLETE
finding object and discards only a trailing partial one.

Six replies still ended mid-array, so the check on these lessons is PARTIAL —
the findings it emitted were kept and applied, but it may not have reached the
end of the lesson:

- `area1-catholic-christianity-L06` (1 findings kept)
- `area1-christianity-L03` (3 findings kept)
- `area1-christianity-L04` (4 findings kept)
- `area2-islam-L01` (5 findings kept)
- `area2-islam-L04` (5 findings kept)
- `area2-judaism-L05` (4 findings kept)

None of the six produced a HIGH finding in what it did emit.


## Findings by lesson

### `area1-catholic-christianity-L01` — 1 finding

- **LOW** (`content_html`)
  - claim: The Council of Nicaea condemned Arianism, the belief that the Son was a lesser being created by the Father rather than eternally divine. It also rejected the opposite error, later called Modalism, which taught that Father, Son and Holy Spirit are just three names for one person appearing in differen
  - problem: Nicaea (325 CE) explicitly anathematised Arianism; it did not condemn Modalism/Sabellianism. Sabellianism had already been condemned at Rome c.262 CE and was explicitly anathematised in Canon 1 of the First Council of Constantinople (381 CE). Attributing the rejection of Modalism to Nicaea is historically inaccurate, though the doctrinal contrast drawn is sound.
  - correction applied: The Council of Nicaea condemned Arianism, the belief that the Son was a lesser being created by the Father rather than eternally divine. The Church also rejected the opposite error, Modalism (or Sabellianism), which taught that Father, Son and Holy Spirit are just three names for one person appearin

### `area1-catholic-christianity-L02` — 3 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: &ldquo;the Bible says Jesus saves&rdquo; earns nothing, but &ldquo;in Acts 4:12, Peter says salvation is found in no other name&rdquo; earns the extra mark
  - problem: This invents an internal mark allocation for the 5-mark 'Explain two' question. The specification states only that the 5-mark use of 'Explain' requires students to 'reference one source of wisdom or authority in support of their explanation'; it does not publish which mark is awarded for the source, nor does it state that a general reference to the Bible scores zero. Claims about what does or does
  - correction applied: On a five-mark &ldquo;Explain two&hellip;&rdquo; question you must reference a source of wisdom and authority in support of your explanation, so name it precisely &mdash; for example &ldquo;in Acts 4:12, Peter says salvation is found in no other name&rdquo; rather than a vague &ldquo;the Bible says 
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "Why does belief in life after death matter to Catholics today?", "a": "It gives hope, shapes funeral rites, and motivates prayer for the dead."}
  - problem: The answer is a list of three separate items ('X, Y and Z'), which breaches the flashcard rule that each card should test one point; these belong on separate cards.
  - correction applied: {"q": "How does belief in life after death shape Catholic funeral practice?", "a": "The funeral rite proclaims eternal life in Christ, offering hope to mourners rather than only marking a death."}
- **LOW** (`flashcard_questions`)
  - claim: {"q": "What does 'Paschal Mystery' refer to?", "a": "The saving events of Jesus's death and resurrection."}
  - problem: Inconsistent with the lesson's own glossary and knowledge-check, which define the Paschal Mystery as Jesus's suffering, death, resurrection and ascension. Omitting the ascension could cost precision in a recall answer.
  - correction applied: {"q": "What does 'Paschal Mystery' refer to?", "a": "The saving events of Jesus's suffering, death, resurrection and ascension, through which humanity is redeemed."}

### `area1-catholic-christianity-L03` — 7 findings

- **MEDIUM** (`content_html`)
  - claim: One named example is the <dfn class="term" data-def="An international Catholic movement founded in France in 1947 that supports families through small group meetings, prayer and mutual support.">Family Group Movement</dfn>, founded in France in 1947, where small groups of families meet regularly for
  - problem: The founding details are wrong. The Family Group Movement usually cited in Catholic parish life is the Passionist Family Group Movement, begun by Fr Peter McGrath CP at Terrey Hills, Sydney, Australia, in 1973 (Passionist Family Group Movement official history); it is not a French movement of 1947. The 1947 French date appears to confuse it with Équipes Notre-Dame (Teams of Our Lady), and the 1940
  - correction applied: One named example is the <dfn class="term" data-def="An international Catholic movement, begun in Australia in 1973, that supports families through small group meetings, prayer and mutual support.">Family Group Movement</dfn> (the Passionist Family Group Movement, begun in Sydney, Australia, in 1973
- **MEDIUM** (`glossary_terms`)
  - claim: Family Group Movement — An international Catholic movement founded in France in 1947 that supports families through small group meetings, prayer and mutual support.
  - problem: Same factual error as in the content: the Passionist Family Group Movement was founded in Australia (Terrey Hills, Sydney) in 1973 by Fr Peter McGrath CP, not in France in 1947.
  - correction applied: Family Group Movement — An international Catholic movement (the Passionist Family Group Movement), begun in Australia in 1973, that supports families through small group meetings, prayer and mutual support.
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "What is the Family Group Movement?", "a": "A Catholic movement, founded in France in 1947, of small family groups meeting for prayer and support."}
  - problem: The founding country and year are wrong: the Passionist Family Group Movement was founded in Australia in 1973, not France in 1947.
  - correction applied: {"q": "What is the Family Group Movement?", "a": "A Catholic movement, begun in Australia in 1973, of small family groups meeting for prayer and mutual support."}
- **MEDIUM** (`knowledge_checks`)
  - claim: Small Catholic family groups that meet for prayer and support, founded in France in 1947
  - problem: Same error: the Family Group Movement (Passionist Family Group Movement) was founded in Australia in 1973, not France in 1947.
  - correction applied: Small Catholic family groups that meet for prayer and support, begun in Australia in 1973
- **MEDIUM** (`glossary_terms`)
  - claim: gender prejudice — Unfair treatment of a person on the grounds of their gender.
  - problem: This defines discrimination, not prejudice. In standard GCSE Religious Studies terminology prejudice is an unfair pre-judgement or attitude held about a person or group, while discrimination is the resulting action or unfair treatment. Using the wrong definition risks losing specialist-terminology credit.
  - correction applied: gender prejudice — Unfairly pre-judging or holding a negative attitude towards someone because of their gender (acting on it is gender discrimination).
- **MEDIUM** (`exam_tip_html`)
  - claim: Do not write one long descriptive paragraph &mdash; examiners reward a weighed argument.
  - problem: Unevidenced claim about examiner behaviour. The stated assessment rules say only that 'Evaluate' questions reward a 'sustained line of reasoning which is coherent, relevant, substantiated and logically structured'; they say nothing about what examiners reward or penalise in paragraph terms.
  - correction applied: Do not write one long descriptive paragraph &mdash; the 12-mark question credits a sustained, logically structured line of reasoning that weighs different points of view.
- **LOW** (`content_html`)
  - claim: Catechism paragraph 2207 describes the family as the &ldquo;original cell of social life&rdquo; in which men and women are equal in dignity, each with an essential role.
  - problem: The quotation from CCC 2207 is accurate, but that paragraph does not state the equality in dignity of men and women; it deals with the family as the original cell of social life. Equal personal dignity is taught at CCC 2334 ('In creating man and woman, God gives man and woman an equal personal dignity') and CCC 369.
  - correction applied: Catechism paragraph 2207 describes the family as the &ldquo;original cell of social life&rdquo;, and Catechism 2334 teaches that God gives man and woman &ldquo;an equal personal dignity&rdquo;, each with an essential role.

### `area1-catholic-christianity-L04` — 5 findings

- **HIGH** (`content_html`)
  - claim: The Second Vatican Council document Lumen Gentium, paragraph 7, describes the Eucharist as the &lsquo;source and summit of the Christian life&rsquo;
  - problem: Wrong paragraph reference. Lumen Gentium 7 is about the Church as the Mystical Body of Christ. The 'source and summit' (Latin: 'fons et culmen'/'fount and apex of the whole Christian life') statement is Lumen Gentium 11, which is the paragraph quoted in CCC 1324 and cited in the specification content for the Mass. Giving students the wrong paragraph number risks an inaccurate source reference in a
  - correction applied: The Second Vatican Council document Lumen Gentium, paragraph 11, describes the Eucharist as the &lsquo;source and summit of the Christian life&rsquo;
- **HIGH** (`exam_tip_html`)
  - claim: &ldquo;Lumen Gentium, paragraph 7&rdquo;, &ldquo;Matthew 6:5&ndash;14&rdquo; or &ldquo;Matthew 25:31&ndash;46&rdquo; are all safe choices for this lesson
  - problem: 'Source and summit of the Christian life' comes from Lumen Gentium 11, not paragraph 7 (LG 7 concerns the Church as the Body of Christ). Recommending paragraph 7 as a 'safe choice' would hand students an inaccurate source reference.
  - correction applied: &ldquo;Lumen Gentium, paragraph 11&rdquo;, &ldquo;Matthew 6:5&ndash;14&rdquo; or &ldquo;Matthew 25:31&ndash;46&rdquo; are all safe choices for this lesson
- **HIGH** (`conclusion_html`)
  - claim: the Mass is called the &lsquo;source and summit of the Christian life&rsquo; (Lumen Gentium 7)
  - problem: Incorrect citation: the phrase is from Lumen Gentium 11 (quoted in CCC 1324), not Lumen Gentium 7.
  - correction applied: the Mass is called the &lsquo;source and summit of the Christian life&rsquo; (Lumen Gentium 11)
- **HIGH** (`practice_questions`)
  - claim: The Eucharist is described as the 'source and summit of the Christian life' (Lumen Gentium, paragraph 7), meaning all Catholic life flows from and returns to it
  - problem: The model answer gives the wrong paragraph: the quotation is Lumen Gentium 11, not paragraph 7. A model answer for a 'refer to a source of wisdom and authority' question must cite the source accurately.
  - correction applied: The Eucharist is described as the 'source and summit of the Christian life' (Lumen Gentium, paragraph 11), meaning all Catholic life flows from and returns to it
- **LOW** (`knowledge_checks`)
  - claim: The Lord's Prayer is found in Matthew 6:5–_____.
  - problem: The Lord's Prayer itself is Matthew 6:9–13; Matthew 6:5–14 is the wider passage of Jesus's teaching on prayer (warning against praying for show, the prayer, and the saying on forgiveness). As worded, the card implies the prayer spans 6:5–14.
  - correction applied: Jesus's teaching on prayer, including the Lord's Prayer, is found in Matthew 6:5–_____. (answer: 14)

### `area1-catholic-christianity-L05` — 3 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: A common mistake is writing only one side of the argument or forgetting the conclusion.
  - problem: This is an unevidenced assertion about how candidates typically perform. The stated assessment rules say only that 'Evaluate' questions require different points of view, logical chains of reasoning and a justified conclusion; they make no claim about common candidate errors.
  - correction applied: For the 12-mark 'Discuss a Statement' question the mark scheme rewards different points of view, logical chains of reasoning and a justified conclusion, so make sure your answer includes both sides and ends with a clear judgement.
- **LOW** (`content_html`)
  - claim: Because Lemaître was both a Catholic priest and a scientist, the Church points to his work as proof that science and faith can support each other rather than conflict.
  - problem: Overstatement: Lemaître's work is used as an illustration that faith and science need not conflict, not as 'proof'. Lemaître himself resisted using the theory as religious proof (he objected when Pius XII linked it to creation in 1951).
  - correction applied: Because Lemaître was both a Catholic priest and a scientist, Catholics often point to his work as an example of how science and faith can support each other rather than conflict.
- **LOW** (`flashcard_questions`)
  - claim: {"q": "What is meant by 'survival of the fittest'?", "a": "The idea that only the best-adapted species survive over time."}
  - problem: Survival of the fittest describes individual organisms best adapted to their environment surviving and reproducing, passing on their characteristics; describing it as species-level survival is imprecise.
  - correction applied: {"q": "What is meant by 'survival of the fittest'?", "a": "The idea that the organisms best adapted to their environment are most likely to survive and pass on their characteristics."}

### `area1-catholic-christianity-L06` — 1 finding

- **MEDIUM** (`?`)
  - claim: Catholics can use a similar weighing of outcomes when judging particular cases of animal use, while always insisting that unnecessary cruelty remains wrong regardless of the benefit produced.
  - problem: This misleadingly presents Catholic moral reasoning as a form of utilitarian/consequentialist weighing. Catholic teaching explicitly rejects consequentialism: the Catechism (1789) states that 'One may never do evil so that good may result from it', and CCC 2417's 'reasonable limits' is natural-law proportionality, not greatest-good calculation. Students who write that Catholics use utilitarian rea
  - correction applied: Catholic teaching does not use utilitarian calculation: the Church holds that an act which is wrong in itself can never be justified by its good consequences. Catholics do, however, weigh whether a particular use of animals stays within 'reasonable limits' (Catechism 2417), insisting that unnecessar

### `area1-christianity-L01` — 4 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: Without a named source you cannot gain the extra mark that question carries.
  - problem: This states a within-question mark allocation (that the fifth mark is specifically awarded for the named source). The specification only says the 5-mark 'Explain' requires students to 'reference one source of wisdom or authority in support of their explanation'; it publishes no per-mark breakdown, so this is an invented mark split.
  - correction applied: If you leave out a named source, you lose marks, because this version of the question requires you to reference one source of wisdom or authority in support of your explanation.
- **LOW** (`content_html`)
  - claim: Forty days later, Luke 24:50&ndash;53 records the ascension, when Jesus returns to the Father in heaven.
  - problem: Luke 24:50–53 records the ascension but gives no time interval; the 'forty days' detail comes from Acts 1:3. Attributing the figure to Luke 24 misdescribes the passage.
  - correction applied: Luke 24:50&ndash;53 records the ascension, when Jesus returns to the Father in heaven; Acts 1:3 tells Christians this happened forty days after the resurrection.
- **LOW** (`content_html`)
  - claim: Close this and list the six events of Jesus's last days in order, then explain what the crucifixion and the resurrection each show about who Jesus is.
  - problem: The Key Fact in the same box lists seven events (Last Supper, betrayal, arrest, trial, crucifixion, resurrection, ascension), so the instruction to list 'six' contradicts the material students are revising from.
  - correction applied: Close this and list the seven events of Jesus's last days in order, then explain what the crucifixion and the resurrection each show about who Jesus is.
- **LOW** (`content_html`)
  - claim: set prayers such as grace before meals address all three persons directly
  - problem: The well-known Trinitarian prayer called 'the Grace' (based on 2 Corinthians 13:14) is a blessing used in worship, usually at the end of a service, not a mealtime grace; the two are conflated here.
  - correction applied: set prayers such as the Grace (based on 2 Corinthians 13:14), often used to close worship, address all three persons directly

### `area1-christianity-L02` — 1 finding

- **LOW** (`exam_tip_html`)
  - claim: For the 12-mark Discuss question, plan both sides before you write: give at least two developed points supporting the statement and two challenging it, each backed by named Christian teaching, before reaching a justified conclusion.
  - problem: The specification's instruction for 'Evaluate' questions requires reasoned arguments in support, reasoned arguments offering a different point of view, and a justified conclusion; it does not set a minimum number of points or paragraphs. Stating 'at least two ... and two' presents an unstated quantity requirement as if it were an exam rule.
  - correction applied: For the 12-mark Discuss question, plan both sides before you write: develop reasoned arguments supporting the statement and reasoned arguments offering a different point of view, each backed by named Christian teaching, before reaching a justified conclusion.

### `area1-christianity-L03` — 3 findings

- **LOW** (`content_html`)
  - claim: Christian teaching on sexual relationships draws on 1 Corinthians 6:7&ndash;20, where Paul instructs believers to flee sexual immorality
  - problem: The verse range is slightly off: 1 Corinthians 6:7-8 concerns lawsuits between believers, not sexual morality. The passage on sexual immorality and the body as a temple of the Holy Spirit runs from verse 9 (commonly cited as 1 Corinthians 6:9-20 in Christianity Marriage and the Family material).
  - correction applied: Christian teaching on sexual relationships draws on 1 Corinthians 6:9&ndash;20, where Paul instructs believers to flee sexual immorality
- **LOW** (`flashcard_questions`)
  - claim: {"q": "Which passage teaches that the believer's body is a temple of the Holy Spirit?", "a": "1 Corinthians 6:7-20."}
  - problem: Same verse-range imprecision as in the content: the relevant passage is 1 Corinthians 6:9-20 (6:7-8 deals with lawsuits between believers).
  - correction applied: {"q": "Which passage teaches that the believer's body is a temple of the Holy Spirit?", "a": "1 Corinthians 6:9-20."}
- **LOW** (`conclusion_html`)
  - claim: but Galatians 3:23&ndash;29 is used by all to oppose gender prejudice
  - problem: Overstated: the lesson itself notes that Christians disagree about the practical roles of men and women, and it cannot be verified that every Christian or denomination appeals to this passage. 'By all' is an unsupportable generalisation.
  - correction applied: but Galatians 3:23&ndash;29 is widely used by Christians to argue against gender prejudice

### `area1-christianity-L04` — 4 findings

- **MEDIUM** (`content_html`)
  - claim: The <strong>Thirty-Nine Articles (XXV&ndash;XXXVI)</strong>, the Church of England&rsquo;s statement of doctrine, teach that only two sacraments were &lsquo;ordained of Christ our Lord in the Gospel&rsquo;
  - problem: Both quoted phrases ('ordained of Christ our Lord in the Gospel' and 'not to be counted for Sacraments of the Gospel') come from Article XXV alone ('Of the Sacraments'). The cited range XXV–XXXVI is wrong: Articles XXXII–XXXVI concern the marriage of priests, excommunication, traditions of the Church, the Homilies and the consecration of bishops, not the number of sacraments. A misattributed sourc
  - correction applied: The <strong>Thirty-Nine Articles (Article XXV)</strong>, part of the Church of England&rsquo;s statement of doctrine, teach that only two sacraments were &lsquo;ordained of Christ our Lord in the Gospel&rsquo;
- **MEDIUM** (`exam_tip_html`)
  - claim: A vague reference to &lsquo;the Bible says&rsquo; will not earn that final mark.
  - problem: This is an unevidenced claim about how a mark is awarded. The stated assessment rules say only that the 5-mark 'Explain' requires students to 'reference one source of wisdom or authority in support of their explanation'; they say nothing about marks being withheld for vagueness.
  - correction applied: This type of question requires you to reference one source of wisdom or authority in support of your explanation, so name and attribute the source rather than writing only &lsquo;the Bible says&rsquo;.
- **LOW** (`exam_tip_html`)
  - claim: &lsquo;liturgical&rsquo;, &lsquo;Eucharist&rsquo;, &lsquo;pilgrimage&rsquo; and &lsquo;ecumenism&rsquo; all carry specialist-terminology marks
  - problem: The assessment rules state only that spelling, punctuation, grammar and use of specialist terminology contribute a minimum of 5% of the marks for the paper; no marks are attached to particular words, and the distribution of those marks is not published.
  - correction applied: Spell key terms accurately &mdash; &lsquo;liturgical&rsquo;, &lsquo;Eucharist&rsquo;, &lsquo;pilgrimage&rsquo; and &lsquo;ecumenism&rsquo; &mdash; because accurate spelling, punctuation, grammar and use of specialist terminology are assessed on this paper.
- **LOW** (`content_html`)
  - claim: The <dfn class="term" ...>Eucharist</dfn> is the one sacrament shared by virtually all Christians, but its meaning is disputed.
  - problem: Misleading and inconsistent with the lesson's own earlier statement that baptism is 'practised in some form across almost every denomination'. Baptism and the Eucharist are the two rites accepted across virtually all denominations (both are omitted only by groups such as the Quakers and the Salvation Army).
  - correction applied: The <dfn class="term" ...>Eucharist</dfn>, like baptism, is accepted by virtually all Christian denominations, but its meaning is disputed.

### `area1-christianity-L05` — 5 findings

- **MEDIUM** (`content_html`)
  - claim: The Diocese of Manchester held a special synod, referred to as Special Agenda IV, at which motions were passed stating that scientific explanations such as evolution are compatible with Christian belief
  - problem: "Special Agenda IV" is not a special synod held by a diocese: in Church of England procedure it is the category of business on the General Synod's agenda under which Diocesan Synod Motions are debated. A diocese does not hold a synod called 'Special Agenda IV', and no such Manchester 'special synod' on evolution is verifiable. The Church of England's published position on evolution is set out in o
  - correction applied: The Church of England has officially stated that evolution and Christian belief are compatible. In 2008 the Church published a statement by its Director of Mission and Public Affairs, 'Good religion needs good science', which accepted Darwin's theory and encouraged Christians not to see science as a
- **MEDIUM** (`flashcard_questions`)
  - claim: Which Church of England diocese passed synod motions on evolution and faith?" / "The Diocese of Manchester.
  - problem: This card rests on the unverifiable 'Special Agenda IV' claim above (Special Agenda IV is the General Synod's heading for Diocesan Synod Motions, not a diocesan synod on evolution). Students would be memorising an inaccurate institutional fact.
  - correction applied: Q: How has the Church of England officially responded to Darwin's theory of evolution? A: It has accepted evolution as compatible with faith, stating in 2008 that 'good religion needs good science'.
- **MEDIUM** (`content_html`)
  - claim: This is reinforced by Humanae Vitae, Pope Paul VI's 1968 teaching, which taught that human life is sacred from the moment of conception and condemned abortion as a grave offence against that sanctity.
  - problem: Humanae Vitae (1968) is an encyclical on the regulation of birth (contraception); it does rule out 'directly willed and procured abortion' (para. 14) but it is not the Church's teaching document on the sanctity of life from conception. The standard sources for that are Donum Vitae (1987) and Evangelium Vitae (John Paul II, 1995). Presenting Humanae Vitae as the main pro-life source is misleading.
  - correction applied: This is reinforced by Catholic teaching: Humanae Vitae (Pope Paul VI, 1968) rules out directly procured abortion, and Evangelium Vitae (Pope John Paul II, 1995) teaches that human life is sacred and inviolable from conception, calling abortion a grave moral disorder.
- **MEDIUM** (`content_html`)
  - claim: Most Catholic and many other Christians hold a pro-life position: life is sacred from conception, so abortion is seriously wrong except perhaps to save the mother's life.
  - problem: Official Catholic teaching does not allow direct abortion even to save the mother's life; only indirect loss of the foetus during treatment of the mother (the principle of double effect) is permitted. The exception as written misstates the Catholic position in a way that could cost marks.
  - correction applied: Most Catholic and many other Christians hold a pro-life position: life is sacred from conception, so directly intended abortion is always seriously wrong, though Catholic teaching accepts that a foetus may be lost indirectly as a side effect of medical treatment needed to save the mother's life. Som
- **LOW** (`content_html`)
  - claim: Georges Lemaître was a Catholic priest and physicist who, in 1927, proposed the theory that the universe began expanding from a single point
  - problem: Lemaître's 1927 paper proposed an expanding universe; the idea that it began from a single dense point (his 'primeval atom' hypothesis) was published in 1931. The date is attached to the wrong part of the theory.
  - correction applied: Georges Lemaître was a Catholic priest and physicist who proposed an expanding universe in 1927 and, in 1931, the idea that it began from a single dense 'primeval atom' — the theory that later became known as the Big Bang.

### `area1-christianity-L06` — 2 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: Do not write one-sided description &mdash; examiners reward weighing arguments against each other.
  - problem: Unevidenced claim about examiner behaviour. The stated assessment rules describe only what the 'Evaluate' command word requires (considering different points of view, logical chains of reasoning, a justified conclusion); they say nothing about what examiners 'reward'.
  - correction applied: Do not write one-sided description &mdash; a 12-mark answer needs different points of view, logical chains of reasoning and a justified conclusion.
- **MEDIUM** (`content_html`)
  - claim: Differing Christian views on animal testing, food production and environmental damage show that Christianity does not speak with one voice on these issues &mdash; students must show this divergence to gain full marks.
  - problem: Unevidenced claim about marking. The assessment rules state only that AO1 includes 'similarities and differences within and/or between religions and beliefs'; no requirement that divergence must be shown 'to gain full marks' is published.
  - correction applied: Differing Christian views on animal testing, food production and environmental damage show that Christianity does not speak with one voice on these issues &mdash; showing this divergence strengthens your answers, because knowledge of differences within a religion is part of what is assessed.

### `area2-islam-L01` — 5 findings

- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "What are the Six Beliefs of Sunni Islam?", "a": "Allah, Angels, Books, Prophets, Day of Judgement, al-Qadr."}
  - problem: Breach of flashcard rules: the answer is a bare list of items ('X, Y and Z'), which must be split into separate cards rather than recalled as a single string.
  - correction applied: {"q": "In the Sunni Six Beliefs, what does al-Qadr mean?", "a": "Belief in divine decree — that Allah has knowledge of, and ultimate control over, everything that happens."}
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "What are the Five Roots of Usul ad-Din?", "a": "Tawhid, 'Adl, Nubuwwah, Imamah, Mi'ad."}
  - problem: Breach of flashcard rules: the answer is a bare list of items, which belongs in separate single-focus cards.
  - correction applied: {"q": "What does Mi'ad mean in the Shi'a Five Roots of Usul ad-Din?", "a": "Belief in the Day of Judgement and the resurrection of the dead, when Allah will judge every person."}
- **MEDIUM** (`exam_tip_html`)
  - claim: A common mistake is muddling the Six Beliefs (Sunni) with the Five Roots (Shi'a)
  - problem: Unevidenced assertion about candidate behaviour/common errors. The stated assessment rules say nothing about typical candidate mistakes, so this is an invented claim about exam performance.
  - correction applied: Be careful to keep the Six Beliefs (Sunni) and the Five Roots (Shi'a) separate — they are different lists from different traditions, so never present them as identical.
- **LOW** (`exam_tip_html`)
  - claim: both are named in the specification, so they are safe, accurate citations
  - problem: Student-facing text should refer to 'your course content' / 'your exam' rather than to the board's specification document (site language policy on board/spec references).
  - correction applied: both are part of the course content you are examined on, so they are safe, accurate citations
- **LOW** (`content_html`)
  - claim: based on a hadith known as <strong>Kitab al-iman 1:4</strong>
  - problem: Kitab al-Iman ('The Book of Faith') is a chapter of a hadith collection, not itself a single hadith; 1:4 is a reference within that collection. Minor imprecision in how the source is described.
  - correction applied: based on a hadith found in <strong>Kitab al-iman 1:4</strong> (the 'Book of Faith' section of the hadith collections)

### `area2-islam-L02` — 4 findings

- **MEDIUM** (`content_html`)
  - claim: Three angels are named in the Qur&rsquo;an as especially significant:
  - problem: Jibril and Mika'il are named in the Qur'an (Surah 2:97-98), but Izra'il is not. Surah 32:11 refers only to 'the angel of death' (malak al-mawt); the name Izra'il comes from later Islamic tradition, not the Qur'an. Stating that all three are Qur'anically named is inaccurate.
  - correction applied: Three angels are especially significant in Muslim teaching &mdash; two are named in the Qur&rsquo;an and one is named in Islamic tradition:
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "What is Izra'il's role in Islam?", "a": "The angel of death, named in Surah 32:11."}
  - problem: Surah 32:11 does not name Izra'il; it speaks of 'the angel of death who has been entrusted with you'. The name Izra'il derives from Islamic tradition rather than the Qur'an, so the card teaches a false attribution.
  - correction applied: {"q": "What is Izra'il's role in Islam?", "a": "The angel of death, who takes the soul at death; Surah 32:11 refers to 'the angel of death' entrusted with each person."}
- **MEDIUM** (`exam_tip_html`)
  - claim: Naming the reference exactly, not just &ldquo;a hadith says&hellip;&rdquo;, is required to gain that mark.
  - problem: The assessment rules state only that the 5-mark Explain question requires students to 'reference one source of wisdom or authority in support of their explanation'. Nothing in the specification requires an exact chapter-and-verse or hadith citation, or says a mark is withheld without one. This is an invented marking requirement.
  - correction applied: One part of each question requires you to refer to a source of wisdom and authority, so support your explanation with a relevant teaching &mdash; for al-Qadr you could use Sahih al-Bukhari 78:685; for Akhirah, Surah 17:49&ndash;72.
- **LOW** (`knowledge_checks`)
  - claim: Which angel does Surah 32:11 describe as being entrusted to take a person's soul at death?
  - problem: Surah 32:11 does not name the angel; it refers to 'the angel of death who has been entrusted with you'. The identification as Izra'il comes from Islamic tradition, so the question's premise is imprecise.
  - correction applied: In Islamic tradition, which angel is identified as the angel of death who takes the soul (see Surah 32:11)?

### `area2-islam-L03` — 3 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: For “Discuss a Statement” questions, plan one paragraph giving Muslim arguments that agree with the statement, one giving a divergent Muslim or non-religious view that disagrees, and a short final paragraph giving your own justified conclusion
  - problem: The stated assessment rules explicitly forbid telling students a number of paragraphs (or lines/words) an answer must reach: the specification says nothing about answer length or paragraph structure, only that the 12-mark 'Evaluate'/'Discuss a Statement' response must consider different points of view and reach a justified conclusion supported by reasoning. Prescribing a three-paragraph structure 
  - correction applied: For “Discuss a Statement” questions, build your answer around developed Muslim arguments that support the statement, developed arguments (Muslim or non-religious) that support a different point of view, and a justified conclusion that weighs them — do not just describe both sides without judging bet
- **LOW** (`content_html`)
  - claim: The Muslim Chaplains Association supports the religious and pastoral needs of Muslim prisoners, helping them reflect on their actions and return to their faith.
  - problem: The Muslim Chaplains Association is a professional body for Muslim chaplains working across prisons, hospitals, universities and the armed forces; it supports and trains the chaplains who then meet prisoners' needs, rather than being a prisoner-support organisation itself. Minor imprecision in an organisation description.
  - correction applied: The Muslim Chaplains Association supports and represents Muslim chaplains, including those working in prisons, so that Muslim prisoners' religious and pastoral needs are met and offenders are helped to reflect on their actions and return to their faith.
- **LOW** (`content_html`)
  - claim: The Mosaic Community Trust works with young people, particularly in areas at risk of gang activity, offering mentoring and enterprise projects that give them a positive alternative to crime.
  - problem: The mentoring and enterprise programmes for young Muslims described here belong to 'Mosaic', the mentoring initiative founded in 2007 and later run as part of The Prince's Trust. 'Mosaic Community Trust' is a separate Westminster-based community charity focused on health, wellbeing and community support. The name and the activities are conflated.
  - correction applied: Mosaic, a mentoring initiative for young Muslims, works with young people in areas at risk of gang activity, offering mentoring and enterprise projects that give them a positive alternative to crime.

### `area2-islam-L04` — 5 findings

- **MEDIUM** (`content_html`)
  - claim: Its nature, role, significance and purpose is to require Sunni Muslims whose savings exceed the nisab threshold to give 2.5% to those in need. ... Zakah is important for Sunni Muslims because it purifies wealth and reduces inequality in the ummah.
  - problem: Zakah is presented as a Sunni-only obligation, which contradicts the lesson's own (correct) earlier statement that Zakah is one of the four acts shared between the Five Pillars and the Ten Obligatory Acts. Shi'a Muslims are also obliged to pay Zakah (in addition to Khums); the difference is in how it is calculated and distributed, not whether it applies.
  - correction applied: Its nature, role, significance and purpose is to require Muslims whose savings exceed the nisab threshold to give 2.5% to those in need. Surah 9:58–60 names eight categories entitled to receive it, including the poor and travellers in need. Zakah is important for Muslims because it purifies wealth a
- **MEDIUM** (`glossary_terms`)
  - claim: Zakah: Obligatory almsgiving in Sunni Islam — giving 2.5% of annual savings above the nisab threshold to those in need.
  - problem: Zakah is not exclusive to Sunni Islam; it is also one of the Ten Obligatory Acts of Shi'a Islam, as the lesson itself states in the 'Divergence' box. Defining it as Sunni-only is factually misleading and contradicts the content.
  - correction applied: Zakah: Obligatory almsgiving in Islam — giving 2.5% of annual savings above the nisab threshold to those in need; one of the Five Pillars and also one of the Ten Obligatory Acts.
- **LOW** (`content_html`)
  - claim: Surah 15:98–99 links glorifying Allah in prayer with certainty of faith.
  - problem: Surah 15:98–99 instructs the Prophet to glorify and prostrate to his Lord 'until what is certain comes to you' — 'al-yaqin' is standardly understood by commentators as death, not 'certainty of faith'. The gloss misreads the verse.
  - correction applied: Surah 15:98–99 commands believers to glorify Allah and prostrate in worship until death comes to them — that is, prayer is a lifelong duty.
- **LOW** (`content_html`)
  - claim: Surah 3:17–21 describes believers who bear witness patiently and truthfully to Allah as among the most praiseworthy.
  - problem: In this passage it is Allah Himself (with the angels and those of knowledge) who bears witness that there is no god but He (Surah 3:18); verse 17 praises believers for patience, truthfulness, devout worship, charity and seeking forgiveness, not for 'bearing witness'. The gloss reverses who bears witness.
  - correction applied: Surah 3:17–21 praises believers who are patient, truthful and devout in worship, and states that Allah Himself, with the angels and those of knowledge, bears witness that there is no god but He — the truth the Shahadah declares.
- **LOW** (`flashcard_questions`)
  - claim: What animal did Allah provide to Ibrahim as a substitute in the Id-ul-Adha story? — A ram, according to Surah 37:77-111.
  - problem: Surah 37:107 says Ibrahim's son was ransomed with 'a great sacrifice'; the identification of the substitute as a ram comes from later tradition and hadith rather than the Qur'anic text itself.
  - correction applied: What did Allah provide as a substitute for Ibrahim's son in the Id-ul-Adha story? — A 'great sacrifice' (Surah 37:107), understood in Muslim tradition as a ram.

### `area2-islam-L05` — 1 finding

- **LOW** (`practice_questions`)
  - claim: Outline three teachings the Qur'an gives about peace and how Muslims should treat others. Indicative content: • Surah 25:63 — servants of the Most Merciful reply to hostility with words of peace • Islam shares its root with 'salam' (peace) • Muslims greet one another with 'peace be upon you'
  - problem: The question asks specifically for teachings the Qur'an gives, but two of the four indicative points are not Qur'anic teachings — the shared Arabic root of 'Islam' and 'salam' is a linguistic point, and the greeting 'as-salamu alaykum' is a customary practice, not a Qur'anic instruction. A student following this indicative content could offer non-scriptural material for a question demanding Qur'an
  - correction applied: Indicative content: • Surah 25:63 — servants of the Most Merciful reply to hostility with words of peace • Surah 41:34 (within 41:31–38) — repel evil with something better so enmity becomes friendship • Surah 8:61 — if an enemy inclines to peace, Muslims should incline to peace also • Surah 2:192–19

### `area2-judaism-L01` — 3 findings

- **MEDIUM** (`content_html`)
  - claim: The Almighty promises Abraham that he will become the father of a great nation, that his descendants will be as numerous as the stars, and that the land of Canaan will belong to them forever.
  - problem: The image of descendants "as numerous as the stars" is not in Genesis 17; it belongs to Genesis 15:5 ("Look up at the sky and count the stars... So shall your offspring be") and Genesis 22:17. Genesis 17:2-6 promises that the Almighty will "greatly increase your numbers" and make Abraham "the father of many nations", with Canaan as an "everlasting possession" (Gen 17:8). Attributing the stars simi
  - correction applied: The Almighty promises Abraham that he will be the father of many nations, that his descendants will be greatly increased in number, and that the land of Canaan will belong to them forever as an everlasting possession.
- **MEDIUM** (`exam_tip_html`)
  - claim: the extra mark is only given for a source that is clearly identifiable, so give the book and, where you can, the chapter and verse
  - problem: This states a mark-scheme allocation that the specification does not publish. The specification says only that for the 5-mark use of 'Explain', "students will be required to reference one source of wisdom or authority in support of their explanation"; it does not state that a specific mark is awarded solely for an identifiable source, nor that chapter and verse are needed.
  - correction applied: This question requires you to reference one source of wisdom and authority in support of your explanation, so name a source such as Jeremiah 23:5-8 or 2 Chronicles 7:1-3 and show how it supports the point you are making.
- **MEDIUM** (`exam_tip_html`)
  - claim: A common mistake is describing the Jewish Messiah as divine
  - problem: Unevidenced claim about candidate performance/common errors; no published board document is cited for this. The underlying point about Jewish belief is correct, but the framing as a frequently made mistake is not evidenced.
  - correction applied: Be precise about Jewish belief here: the Messiah is a human king from David's line, not a divine figure.

### `area2-judaism-L02` — 3 findings

- **HIGH** (`content_html`)
  - claim: The specification asks students to compare Jewish beliefs about the afterlife with Christian beliefs.
  - problem: Fabricated exam requirement. The stated assessment rules list the four content sections for Area of Study 2 Judaism (Beliefs; Crime and Punishment; Living the Religious Life; Peace and Conflict) and nowhere require a comparison of Jewish afterlife beliefs with Christian beliefs. The only contrast requirement stated anywhere is inside the 'Describe' command word ('contrast with that of another'), w
  - correction applied: Contrasting Jewish beliefs about the afterlife with those of another religion can sharpen your understanding. Christianity, for example, teaches resurrection through Jesus, who said, &ldquo;I am the resurrection and the life. The one who believes in me will live, even though they die&rdquo; (John 11
- **MEDIUM** (`exam_tip_html`)
  - claim: a vague phrase like &ldquo;the Torah says&rdquo; will not earn the source mark
  - problem: Unevidenced claim about marking behaviour. The stated assessment rules only say that the 5-mark 'Explain' requires students to 'reference one source of wisdom or authority in support of their explanation'; nothing in them says an unnamed or paraphrased reference is refused credit.
  - correction applied: name your source as precisely as you can &mdash; Exodus 20, Talmud Yoma 83&ndash;84, the Mishneh Torah (Sefer Madda) or Ecclesiastes 12 &mdash; because the question asks you to reference one source of wisdom and authority in support of your explanation
- **MEDIUM** (`exam_tip_html`)
  - claim: A common mistake is assuming Judaism has no belief in life after death
  - problem: Unevidenced assertion about what candidates commonly get wrong; no board document in the stated assessment rules supports a claim about frequency of candidate error.
  - correction applied: Do not assume Judaism has no belief in life after death; Orthodox Judaism has a detailed belief in bodily resurrection, so show this divergence clearly.

### `area2-judaism-L03` — 2 findings

- **MEDIUM** (`exam_tip_html`)
  - claim: examiners cannot credit an unnamed source
  - problem: Unevidenced claim about examiner behaviour. The specification only states that for the 5-mark 'Explain' question 'students will be required to reference one source of wisdom or authority in support of their explanation' — it says nothing about what examiners can or cannot credit.
  - correction applied: When a question asks you to Explain Two teachings and reference a source of wisdom, name the exact text (for example Deuteronomy 19:19&ndash;21 or Isaiah 55:6&ndash;8) rather than just describing a teaching in general terms, because this question requires you to reference one source of wisdom and au
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "What did some rabbis call a court in Mishnah Makkot 1:10 that executed people often?", "a": "A 'bloodthirsty' court."}
  - problem: This inverts the point of Mishnah Makkot 1:10, which says a Sanhedrin that carries out an execution even once in seven years (Rabbi Elazar ben Azariah: once in seventy years) is called 'bloodthirsty'/'destructive'. The teaching is about extreme rarity, not frequency — and it contradicts the lesson's own content and MCQ ('A court that executes even rarely can be seen as bloodthirsty').
  - correction applied: {"q": "What did some rabbis in Mishnah Makkot 1:10 call a court that carried out an execution even once in seven years?", "a": "A 'bloodthirsty' court, showing Jewish caution about ever using the death penalty."}

### `area2-judaism-L04` — 4 findings

- **MEDIUM** (`glossary_terms`)
  - claim: "avelut", "definition": "The extended thirty-day period of mourning following shiva."
  - problem: In the standard Jewish mourning sequence the thirty-day period after burial is sheloshim (shloshim); avelut is the wider mourning period, extending to twelve months for a parent. Defining avelut as 'the thirty-day period' conflates it with sheloshim and could cost a mark if a student is asked about the stages of mourning.
  - correction applied: "avelut", "definition": "The wider mourning period after shiva — the thirty days of sheloshim and, for a parent, the full twelve months before normal life resumes."
- **MEDIUM** (`content_html`)
  - claim: Full communal prayer requires a <dfn class="term" data-def="A quorum of ten adult Jews required for full communal prayer.">minyan</dfn>, a quorum of ten adults.
  - problem: Imprecise on a point the lesson itself stresses (Orthodox/Reform divergence): in Orthodox Judaism a minyan is ten Jewish males aged 13 or over; Reform and Liberal synagogues count women equally. 'Ten adults' hides the divergence students are expected to show.
  - correction applied: Full communal prayer requires a <dfn class="term" data-def="A quorum of ten adults required for communal prayer: ten males aged 13 or over in Orthodox Judaism; Reform and Liberal Judaism count men and women.">minyan</dfn> — ten adult males in Orthodox Judaism, while Reform and Liberal synagogues cou
- **LOW** (`content_html`)
  - claim: The <dfn class="term" data-def="The Standing Prayer of nineteen blessings, recited at every Jewish service facing Jerusalem.">Amidah</dfn> is recited standing, in silence, facing Jerusalem, at every Jewish service. It contains nineteen blessings
  - problem: Nineteen blessings is the weekday Amidah; the Shabbat and festival Amidah has seven blessings. Also, in Orthodox services the silent Amidah is followed by a repetition aloud by the prayer leader.
  - correction applied: The Amidah is recited standing, facing Jerusalem, at every Jewish service. The weekday Amidah contains nineteen blessings (the Shabbat and festival version has seven), covering praise of the Almighty, requests for personal and community needs, and thanksgiving. It is said silently and, in Orthodox s
- **LOW** (`flashcard_questions`)
  - claim: {"q": "What does Yom Kippur commemorate?", "a": "The Day of Atonement; the holiest day, marked by fasting and repentance."}
  - problem: Yom Kippur does not commemorate a past event; it is the day on which atonement is sought. The answer effectively re-names the festival rather than answering the question as posed.
  - correction applied: {"q": "What happens on Yom Kippur and why?", "a": "Jews fast for a full day and repent, seeking atonement and forgiveness from the Almighty on the holiest day of the year."}

### `area2-judaism-L05` — 4 findings

- **MEDIUM** (`content_html`)
  - claim: Many Jews respond that the Torah&rsquo;s own vision, shown in Isaiah, is one of peace and justice
  - problem: Isaiah is part of the Nevi'im (Prophets) in the Tenakh, not the Torah (the five books of Moses). Attributing an Isaiah passage to 'the Torah' risks students writing that Isaiah is a Torah text, which is inaccurate about Jewish sources of authority.
  - correction applied: Many Jews respond that the vision of the Jewish scriptures themselves, shown in the prophet Isaiah, is one of peace and justice
- **MEDIUM** (`exam_tip_html`)
  - claim: Spelling, punctuation, grammar and correct use of specialist terms such as Milchemet reshut and Milchemet mitzvah carry marks throughout the paper.
  - problem: The specification states only that SPaG and use of specialist terminology 'will contribute a minimum of 5% of marks towards the overall weighting for this paper'; it does not state how those marks are distributed, so saying they 'carry marks throughout the paper' asserts a distribution the board does not publish.
  - correction applied: Spelling, punctuation, grammar and correct use of specialist terms such as Milchemet reshut and Milchemet mitzvah are assessed on this paper and contribute at least 5% of its marks.
- **MEDIUM** (`flashcard_questions`)
  - claim: {"q": "Who does Psalm 10:12–18 call on the Almighty to defend?", "a": "The weak, the orphan and the oppressed."}
  - problem: Flashcard rule breach: the answer is a list of three items ('X, Y and Z'), which should be split across separate cards rather than combined on one.
  - correction applied: {"q": "In Psalm 10:12–18, which group without parents does the psalmist ask the Almighty to defend?", "a": "The orphan (the fatherless)."} — with separate cards for 'the weak' and 'the oppressed'.
- **LOW** (`content_html`)
  - claim: Close this and recall, in order, the three things Pirkei Avot 1:18 says the world depends on.
  - problem: Pirkei Avot 1:18 (Rabban Shimon ben Gamliel) lists the three things as justice (din), truth (emet) and peace (shalom) in that order; the lesson consistently gives 'truth, justice and peace', so asking students to recall the list 'in order' would train the wrong order.
  - correction applied: Close this and recall the three things Pirkei Avot 1:18 says the world depends on: justice, truth and peace.

## What is NOT covered by this check

- It reads the lesson JSON, not the rendered page. Rendering, narration,
  knowledge checks and flashcards opening, related-media links and phone layout
  were checked separately in a real browser.
- It does not verify the wording of a scripture quotation against a printed
  edition; it verifies that the passage cited teaches what the lesson says it
  teaches, and flags a quotation it cannot place.
- Area of Study 3 and the five religions not built are out of scope by design.

