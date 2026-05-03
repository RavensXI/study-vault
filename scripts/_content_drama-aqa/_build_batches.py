"""Build all 21 batch JSONs for Drama AQA Phase 3.

Reads the Phase 1 plan, assembles each batch with:
- subject + unit metadata
- spec_slice_path (universal vs set-play)
- subject_level_teaching_brief (shared, with drama_content_rules)
- unit_level_teaching_brief (set-play units carry the play-specific brief)
- registered_question_type_names + allowed_question_types_for_this_unit
- quote_ticker_html_for_unit
- lessons_in_batch (with suggested_question_types)

Run: python scripts/_content_drama-aqa/_build_batches.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN_PATH = ROOT / "scripts" / "_plan_drama-aqa.json"
OUT_DIR = ROOT / "scripts" / "_content_drama-aqa"

# ---------------------------------------------------------------------------
# Question type taxonomy
# ---------------------------------------------------------------------------
REGISTERED_QTS = [
    "1 mark — Identify",
    "2 marks — Define",
    "4 marks — Explain Effect",
    "4 marks — Short Analysis",
    "8 marks — Interpret as Performer",
    "8 marks — Interpret as Designer",
    "12 marks — Analyse Intentions",
    "20 marks — Extended Staging Response",
    "32 marks — Live Theatre Review",
]

# Set-play units use 8 types (no 32-mark Live Theatre Review)
SET_PLAY_ALLOWED = [q for q in REGISTERED_QTS if q != "32 marks — Live Theatre Review"]
# Theatre Roles & Stagecraft + Practitioners — same 8 types (no live theatre review)
STAGECRAFT_ALLOWED = SET_PLAY_ALLOWED[:]
# Live Theatre Review — full 9 types (includes the 32-mark)
LIVE_THEATRE_ALLOWED = REGISTERED_QTS[:]

# Default suggested types per lesson type
DEFAULT_SET_PLAY_SUGGESTED = [
    "1 mark — Identify",
    "2 marks — Define",
    "4 marks — Explain Effect",
    "8 marks — Interpret as Performer",
    "12 marks — Analyse Intentions",
    "20 marks — Extended Staging Response",
]

# Per-lesson override map (unit_slug -> lesson_number -> [types])
# Drives variety across the 8 lessons of each set play unit
SET_PLAY_PER_LESSON_SUGGESTED = {
    1: [  # Plot and Structure — fact-rich, asks "explain effect"
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "4 marks — Explain Effect",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    2: [  # Characters — performer-leaning
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Performer",
        "20 marks — Extended Staging Response",
    ],
    3: [  # Themes
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "4 marks — Explain Effect",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    4: [  # Context — short types + intentions
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    5: [  # Dramatic Methods — analyse intentions
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "4 marks — Explain Effect",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    6: [  # Staging and Design — designer-leaning
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Designer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    7: [  # Performance Interpretation — performer-leaning
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Performer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    8: [  # Practitioner Application — both performer + designer
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Performer",
        "8 marks — Interpret as Designer",
        "20 marks — Extended Staging Response",
    ],
}

UNIVERSAL_PER_LESSON_SUGGESTED = {
    # Unit 1 — Theatre Roles & Stagecraft (5 lessons)
    ("theatre-roles-stagecraft", 1): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "4 marks — Explain Effect",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("theatre-roles-stagecraft", 2): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Designer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("theatre-roles-stagecraft", 3): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Designer",
        "20 marks — Extended Staging Response",
    ],
    ("theatre-roles-stagecraft", 4): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Performer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("theatre-roles-stagecraft", 5): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    # Unit 2 — Practitioners & Styles (4 lessons)
    ("practitioners-styles", 1): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Performer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("practitioners-styles", 2): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Designer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("practitioners-styles", 3): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Designer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    ("practitioners-styles", 4): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Performer",
        "12 marks — Analyse Intentions",
        "20 marks — Extended Staging Response",
    ],
    # Unit 3 — Live Theatre Review (4 lessons) — uses 32-mark in 2 of 4
    ("live-theatre-review", 1): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Performer",
        "32 marks — Live Theatre Review",
    ],
    ("live-theatre-review", 2): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "8 marks — Interpret as Performer",
        "32 marks — Live Theatre Review",
    ],
    ("live-theatre-review", 3): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "8 marks — Interpret as Designer",
        "12 marks — Analyse Intentions",
        "32 marks — Live Theatre Review",
    ],
    ("live-theatre-review", 4): [
        "1 mark — Identify",
        "2 marks — Define",
        "4 marks — Explain Effect",
        "4 marks — Short Analysis",
        "12 marks — Analyse Intentions",
        "32 marks — Live Theatre Review",
    ],
}

# ---------------------------------------------------------------------------
# Quote ticker (uses Phase 1 quote_ticker_quotes)
# ---------------------------------------------------------------------------
QUOTE_TICKER_HTML = (
    '<blockquote>&ldquo;An actor&rsquo;s job is not to feel &mdash; it is to make the audience feel.&rdquo; '
    '<cite>&mdash; Constantin Stanislavski</cite></blockquote>\n'
    '<blockquote>&ldquo;Art is not a mirror held up to reality, but a hammer with which to shape it.&rdquo; '
    '<cite>&mdash; Bertolt Brecht</cite></blockquote>\n'
    '<blockquote>&ldquo;The stage is a magic circle where only the most real things happen.&rdquo; '
    '<cite>&mdash; Peter Brook</cite></blockquote>\n'
    '<blockquote>&ldquo;Theatre is the art of looking at ourselves.&rdquo; '
    '<cite>&mdash; Augusto Boal</cite></blockquote>\n'
    '<blockquote>&ldquo;Stories are how we know ourselves; theatre is how we share that knowing.&rdquo; '
    '<cite>&mdash; Tanika Gupta</cite></blockquote>\n'
    '<blockquote>&ldquo;Don&rsquo;t chase a play; let it come to you.&rdquo; '
    '<cite>&mdash; Mike Leigh</cite></blockquote>'
)

# ---------------------------------------------------------------------------
# Per-play unit-level teaching brief
# ---------------------------------------------------------------------------
# Each entry covers: synopsis, major_characters, major_themes, historical_context,
# playwright_context, dramatic_methods, key_scenes_for_staging,
# most_relevant_practitioners, copyright_status, stage_history_highlights,
# common_misconceptions
PLAY_BRIEFS = {
    "the-crucible": {
        "synopsis": "Salem, Massachusetts, 1692. A community grips itself in religious hysteria after a group of girls is found dancing in the woods. Accusations of witchcraft escalate into a kangaroo court that destroys neighbours, friends and families. John Proctor, a flawed farmer, must decide whether to confess to a lie that would save his life or refuse and protect his name. Miller wrote it in 1953 as an allegory for the McCarthy hearings.",
        "major_characters": [
            "John Proctor — Salem farmer; flawed, conscience-stricken; the play's tragic hero",
            "Abigail Williams — Reverend Parris's niece; vengeful former servant of the Proctors; leads the accusing girls",
            "Elizabeth Proctor — John's wife; reserved, principled; lies in court to protect John",
            "Reverend Parris — Salem's minister; status-anxious; fears for his reputation",
            "Reverend Hale — outside expert on witchcraft; arc from confidence to remorse",
            "Judge Danforth — deputy governor; presides over the court; refuses to admit the trials might be wrong",
            "Tituba — Parris's enslaved servant from Barbados; first to be accused",
            "Mary Warren — Proctor servant; tries to recant; fails under pressure from Abigail",
            "Giles Corey — elderly farmer; presses for justice; pressed to death off-stage",
            "Rebecca Nurse — pious midwife; falsely accused; moral counterweight to the hysteria",
        ],
        "major_themes": [
            "Mass hysteria — how rumour, fear and group-think collapse a community's reason",
            "Reputation and 'name' — what John defends in his final choice",
            "Conscience and integrity — refusing a public lie even at cost",
            "Hypocrisy and religious authority — those who claim to serve God do the most harm",
            "Power and vengeance — Abigail's accusations as a tool of personal grievance",
            "Allegory — Salem 1692 as McCarthy 1953; theatre as political indictment",
            "Patriarchy and silenced women — who is heard, who is not, in a Puritan court",
        ],
        "historical_context": "Set in Salem, Massachusetts, 1692, during the real Salem witch trials in which 19 people were hanged and one (Giles Corey) was pressed to death. Written 1953 in response to Senator Joseph McCarthy's House Un-American Activities Committee (HUAC) hearings, which sought to expose alleged communist sympathisers in American public life. Miller himself was subpoenaed by HUAC in 1956 and refused to name names. First Broadway production: Martin Beck Theatre, 22 January 1953.",
        "playwright_context": "Arthur Miller (1915–2005), American playwright, married to Marilyn Monroe 1956–1961. Plays explore individual conscience versus social pressure: All My Sons (1947), Death of a Salesman (1949), A View from the Bridge (1955). Miller's HUAC subpoena (1956) is directly tied to The Crucible's themes — he refused to name suspected communists and was convicted of contempt (later overturned).",
        "dramatic_methods": [
            "Four-act structure: rumour (Act 1) → domestic test (Act 2) → public confrontation in court (Act 3) → moral choice in jail (Act 4)",
            "Heightened pseudo-Puritan idiom (thee, thou, archaic syntax) that signals period without being authentic 17th-century speech",
            "Long stage directions and authorial expository notes (printed in some editions) that frame characters as social types",
            "Public confrontation scenes with large casts (the courtroom in Act 3)",
            "Dramatic irony — the audience knows the girls are lying long before the court does",
            "Tragic structure — Proctor as hamartia-bearing protagonist whose flaw (the affair) makes his redemption costly",
            "Subtext in domestic scenes — what John and Elizabeth don't say carries the weight",
        ],
        "key_scenes_for_staging": [
            "Act 1 opening: Parris over Betty's bed; the discovery of the dancing in the woods",
            "Act 2 'linen scene': John and Elizabeth's strained kitchen, Mary Warren returning, Hale's visit, Elizabeth's arrest",
            "Act 3 courtroom: Proctor's confession of adultery; Elizabeth's lie; Mary Warren's collapse under Abigail's stage-managed possession",
            "Act 4 jail: John's signed confession; the moment he tears the paper; the final tableau as the drum sounds and Elizabeth speaks of his goodness",
            "The off-stage pressing of Giles Corey (referred to but not seen)",
        ],
        "most_relevant_practitioners": [
            "Bertolt Brecht — gestus for Danforth (the gavel, the pointed finger), audience as jury, didactic intent suits Miller's allegorical purpose",
            "Constantin Stanislavski — psychological truth for Proctor and Elizabeth's interior conflict (given circumstances, emotion memory)",
            "Could be staged in either lens or hybrid — Stanislavskian intimacy in domestic scenes, Brechtian framing in courtroom",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "Premiere: Martin Beck Theatre, Broadway, 1953, dir. Jed Harris",
            "Old Vic 2014 dir. Yaël Farber, in-the-round; long-form sustained tension; Richard Armitage as Proctor",
            "RSC 2019 (Stratford-upon-Avon) — but never reference these as worked examples for live theatre review",
        ],
        "common_misconceptions": [
            "Students treat the play as a straight historical document rather than an allegory; they miss the McCarthy parallel and so under-explain Miller's intentions in 12-mark questions.",
            "Students reduce Abigail to a 'villain' rather than a teenager weaponising the only power available to her in a patriarchal Puritan community.",
            "Students confuse Reverend Parris and Reverend Hale and so misread the play's critique of religious authority (Parris is self-interested; Hale has an arc).",
            "Students answer the 8-mark performer question with vocal tone only ('I would say it angrily'), missing physical choices (stillness, levels, proxemics) that examiners reward.",
            "Students suggest 'dark lighting' as a designer choice without naming intensity, gobo, lantern type or angle — examiners reward concrete design vocabulary.",
        ],
    },
    "blood-brothers": {
        "synopsis": "Liverpool, 1960s to 1980s. Mrs Johnstone, a single mother of seven and pregnant with twins, agrees to give one twin to her wealthy childless employer Mrs Lyons. The twins, Mickey and Edward, grow up unaware of each other on opposite sides of the British class divide. They become friends as children, drift apart as teenagers, and the play closes on the moment the truth is revealed and a tragedy that the Narrator has foretold from the prologue.",
        "major_characters": [
            "Mickey Johnstone — working-class twin raised by Mrs Johnstone; arc from cheeky child to depressed unemployed adult",
            "Edward Lyons — middle-class twin raised by Mrs Lyons; well-spoken, Oxbridge-bound, becomes a councillor",
            "Mrs Johnstone — single mother of nine; warm, exhausted, the play's emotional centre",
            "Mrs Lyons — anxious, controlling, unable to have her own child; manipulates Mrs Johnstone using superstition",
            "Linda — Mickey's childhood friend, later wife; loved by both brothers",
            "Sammy — Mickey's older brother; petty criminal; pulls Mickey into the bank robbery",
            "Narrator — Brechtian commentator who watches and warns; never named",
        ],
        "major_themes": [
            "Class and the British class divide — the same biological children, two different futures",
            "Fate, superstition and 'shoes on the table' — Russell's framing device for the inevitable",
            "Nature versus nurture — biology or environment, what makes the man",
            "Motherhood — Mrs Johnstone's love, Mrs Lyons's anxiety; both insufficient on their own",
            "Childhood innocence and adolescent identity",
            "Unemployment and Thatcher-era deindustrialisation",
            "Friendship and brotherhood — Mickey and Edward's bond as sacred and doomed",
        ],
        "historical_context": "Liverpool 1960s through to early 1980s. Mass unemployment in Liverpool reached 20% by 1981 amid the closure of docks and manufacturing. The play is haunted by the social cost of Margaret Thatcher's 1979–1990 government, though the play takes care not to attack any individual politician. First produced 1983 (Liverpool Playhouse / national tour); West End musical version opened 1988 at the Phoenix Theatre and ran for 24 years to 2012.",
        "playwright_context": "Willy Russell (born 1947, Whiston, Merseyside) — former hairdresser turned working-class British playwright. Other major works: Educating Rita (1980), Shirley Valentine (1986), Our Day Out (1977). Russell writes plays about working-class life with naturalistic dialect and direct address; Blood Brothers is his most performed work.",
        "dramatic_methods": [
            "Two-act musical play with through-composed songs and recurring motifs",
            "Circular framing — opens and closes on the same tableau (Mickey and Edward dead) so the audience knows the ending from the start",
            "The Narrator as Brechtian commentator — direct address, breaking the fourth wall, recurring chorus warning of the devil",
            "Recurring Marilyn Monroe motif — Mrs Johnstone's youth, then her husband leaving, then Mickey's prescription drugs",
            "'Shoes on the table' superstition — Mrs Lyons's manipulation device; recurs as foreshadowing",
            "Liverpudlian dialect for the Johnstones contrasted with RP for the Lyons family",
            "Songs that comment rather than advance plot — 'Marilyn Monroe', 'Bright New Day', 'Tell Me It's Not True'",
            "Time leaps — children at seven, adolescents at fourteen, adults at twenty-five — typically signalled by costume change and physicality, not by set",
        ],
        "key_scenes_for_staging": [
            "Prologue tableau — the bodies of Mickey and Edward; Narrator's opening",
            "The deal scene — Mrs Lyons persuading Mrs Johnstone to give up one twin, exploiting superstition",
            "The 'I'm seven' scene — children meeting for the first time, Mickey and Edward's friendship pact, the blood-brother oath",
            "The teenage scenes — Mickey, Linda and Edward at the funfair / on the bus; the shifting romantic dynamics",
            "Mickey's depression and prescription-drug arc — the bedroom scene with Linda",
            "The factory closure / Mickey's job loss — the moment unemployment lands",
            "The final scene — Mickey storming the council chamber where Edward is speaking; the Narrator's intervention; the closing tableau",
        ],
        "most_relevant_practitioners": [
            "Bertolt Brecht — the Narrator IS a Brechtian device; the songs interrupt action; the audience is reminded throughout that this is a story about a class system",
            "Constantin Stanislavski — for actors playing Mickey, Edward, Mrs Johnstone (especially across the age leaps); given circumstances and emotion memory help the age work",
            "Russell himself called Blood Brothers a Brechtian musical — students should know that framing",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "Premiere: Liverpool Playhouse 1983, dir. Chris Bond",
            "Phoenix Theatre West End run 1988–2012 (24 years; longest-running British musical at time of close)",
            "Frequent revival on UK regional tours",
        ],
        "common_misconceptions": [
            "Students miss that the Narrator is Brechtian — they treat him as a neutral storyteller rather than a moral commentator who breaks the fourth wall.",
            "Students focus on the songs as decoration rather than as Brechtian alienation devices that interrupt and comment on the action.",
            "Students confuse Blood Brothers with a straight West End musical and forget Russell's social-realist intent (the class-divide critique).",
            "Students give 'sad lighting' as a design answer without naming a wash, intensity, lantern type or directional angle.",
            "Students attempt to 'play seven' through voice alone — examiners reward physical choices (skipping, awkward limb co-ordination, lower centre of gravity) too.",
        ],
    },
    "noughts-and-crosses": {
        "synopsis": "An alternate Britain in which Crosses (Black) form the ruling class and noughts (white) are second-class citizens. Sephy Hadley, daughter of an influential Cross politician, and Callum McGregor, the son of the family's former nought servant, have grown up as childhood friends. Their teenage relationship becomes politically dangerous as Callum's family are drawn into the Liberation Militia and Sephy's family hardens against the noughts. The play tracks their attempt to be together against a state that will not allow it, ending in tragedy.",
        "major_characters": [
            "Sephy Hadley — Cross teenager; daughter of a Home Secretary-equivalent; idealistic at first, hardened by experience",
            "Callum McGregor — nought teenager; bright, denied entry to a 'good' school, drawn into the Liberation Militia",
            "Jasmine Hadley — Sephy's mother; outwardly upper-middle-class, alcoholic in private",
            "Kamal Hadley — Sephy's father; senior Cross politician; cold, ambitious",
            "Meggie McGregor — Callum's mother; once Jasmine's nanny; principled, exhausted",
            "Ryan McGregor — Callum's father; nought activist; arrested",
            "Jude McGregor — Callum's brother; radicalised by his sister's death; becomes Liberation Militia",
            "Lynette McGregor — Callum's sister; mentally ill after a racist attack; dies",
            "Officials of the state — interrogators, prison officers — often multi-roled",
        ],
        "major_themes": [
            "Race, racial hierarchy and the question 'what if it had been reversed'",
            "Power, privilege and white invisibility (here flipped to nought invisibility)",
            "Resistance, terrorism and the moral cost of political violence",
            "Love across enforced lines and the personal cost of state racism",
            "Family loyalty versus political loyalty",
            "Education as gatekeeping — who is admitted, who is not",
            "The state's monopoly on legitimate violence — public execution as theatre of power",
        ],
        "historical_context": "Blackman's novel (2001) and Cooke's stage adaptation (RSC 2007) deliberately invert Britain's racial history. The text engages with the post-Stephen Lawrence Inquiry (Macpherson Report 1999) era of British racial politics and with US civil-rights and anti-apartheid history reimagined. The play premiered at the RSC's Civic Hall, Stratford, in 2007 (later toured by Pilot Theatre).",
        "playwright_context": "Malorie Blackman OBE (born 1962) — British author, Children's Laureate 2013–2015. Wrote the original novel (2001) and three sequels. Dominic Cooke (born 1966) — British director; was Artistic Director of the Royal Court 2007–2013; his RSC stage adaptation premiered 2007 with Pilot Theatre. Cooke's adaptation compresses the novel to roughly two acts and centres the dual-narrator device.",
        "dramatic_methods": [
            "Two-act structure with epilogue",
            "Dual narration — Sephy and Callum address the audience in alternating monologues that interlock with the dramatic action",
            "Direct address — the audience is positioned as witnesses",
            "News bulletins and broadcast voiceovers as world-building",
            "Letters as a device (Callum's final letter)",
            "Vocabulary of segregation — 'Cross', 'nought', 'dagger' (slur for nought) — coined by Blackman",
            "Episodic time-jumps marked by lighting and sound transitions",
            "Stage directions specify projection and soundscape rather than naturalistic sets",
        ],
        "key_scenes_for_staging": [
            "Opening on the beach — Sephy and Callum as children, before the politics intrude",
            "The first day at the Cross school — Callum's arrival, the protest outside, the violence",
            "The interrogation scene — Callum questioned; tension between captor and captive",
            "The hideout / Liberation Militia scenes — Callum's induction; moral compromise",
            "The hostage scene — Sephy and Callum together, the relationship's brief hope",
            "The execution scene — the play's climactic public moment (referred to but staged choices vary)",
            "The final letter / Sephy's final monologue — closing tableau",
        ],
        "most_relevant_practitioners": [
            "Bertolt Brecht — political theatre, audience as witness, didactic intent; gestus for Cross officials' authority",
            "Constantin Stanislavski — for the intimate two-handers between Sephy and Callum, given circumstances make their love specific",
            "Companies like Pilot Theatre have used multi-roling and minimal staging — physical-theatre traditions also relevant",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "RSC premiere 2007, Civic Hall Stratford-upon-Avon, dir. Dominic Cooke",
            "Pilot Theatre revival tours 2019 and 2022 — but never reference these as worked examples for live theatre review",
        ],
        "common_misconceptions": [
            "Students treat the racial reversal as a simple swap rather than a thought experiment that asks them to interrogate their own assumptions about whiteness and privilege.",
            "Students sympathise with Callum's terrorism without weighing the moral compromise the play carefully stages.",
            "Students miss Cooke's structural compression — they retell the novel rather than the stage adaptation's 90-minute arc.",
            "Students suggest 'Black and white costumes' as a design answer without explaining what colour, fabric, fit and uniform signify in THIS world's hierarchy.",
            "Students confuse the dual-narrator monologues with internal soliloquy — they miss the direct-address Brechtian dimension.",
        ],
    },
    "around-the-world-80-days": {
        "synopsis": "Phileas Fogg, a precise Victorian gentleman, wagers £20,000 at the Reform Club that he can travel around the world in 80 days. With his French valet Jean Passepartout he sets out from London, pursued by Inspector Fix (who believes Fogg is a bank robber). Across India, Hong Kong, Yokohama, San Francisco and the Atlantic crossing they encounter elephants, typhoons, train robberies and a young Indian widow named Aouda whom they rescue. Eason's stage adaptation distils Verne's 1872 novel into a high-energy ensemble piece for eight actors playing dozens of roles.",
        "major_characters": [
            "Phileas Fogg — eccentric Reform Club gentleman; precise, unflappable; the play's still centre",
            "Jean Passepartout — Fogg's French valet; energetic, comic, the audience's emotional way in",
            "Inspector Fix — Scotland Yard detective convinced Fogg is a bank robber",
            "Aouda — young Indian widow rescued from sati; becomes part of Fogg's company",
            "Reform Club gentlemen — the wager-makers in London, framing the adventure",
            "Multi-roled minor parts — train guards, ship's captains, customs officials, brigands, Native American attackers, Yokohama acrobats, an elephant — typically rotated between the small ensemble",
        ],
        "major_themes": [
            "Time, schedule and Victorian punctuality — the wager itself as a meditation on industrial time",
            "British Empire and the colonial gaze — what Verne sees, what the modern stage chooses to question",
            "Adventure, comedy and the exotic — Victorian thirst for the world reimagined for a modern audience",
            "Friendship and ensemble — Fogg, Passepartout, Aouda, Fix as a found family by the end",
            "The mechanics of travel — steam, rail, the Suez Canal, transcontinental track",
            "Comedy and stoicism — the play laughs with Fogg's eccentricity rather than at the cultures he passes through",
        ],
        "historical_context": "Verne's novel was published 1872, shortly after the opening of the Suez Canal (1869) and the completion of the US transcontinental railroad (1869) — both made circumnavigation in 80 days theoretically possible for the first time. Eason's stage adaptation premiered at the New Vic Theatre, Newcastle-under-Lyme in 2013 (in-the-round). Modern productions navigate the novel's colonial assumptions by foregrounding the ensemble's awareness of the cultures they pass through.",
        "playwright_context": "Jules Verne (1828–1905) — French novelist, founder of speculative adventure fiction. Laura Eason — American playwright (Sex with Strangers; House of Cards writers' room). Her 80 Days adaptation was commissioned by the New Vic and premiered in 2013, dir. Theresa Heskins; designed for a small ensemble (typically 8 actors) with extensive multi-roling and physical-theatre staging.",
        "dramatic_methods": [
            "Episodic structure — short scenes in different locations, narrated transitions",
            "Eight-actor ensemble multi-roling — each actor plays many minor parts",
            "Direct address narration — actors step out to set the scene or comment on Fogg's progress",
            "Mime and physical theatre — bodies become trains, ships and elephants",
            "Object transformation — chairs become railway carriages; rope becomes the rigging of a ship",
            "Comic timing — Fogg's stillness against Passepartout's energy",
            "Soundscape-driven scene-setting — train whistles, ship bells, foreign-language fragments",
            "Fast costume changes — base layer plus accessories, like Frantic Assembly / Complicite practice",
        ],
        "key_scenes_for_staging": [
            "The Reform Club opening — establishing Fogg's precision and the terms of the wager",
            "The Suez Canal customs inspection — Fix's first attempt to detain Fogg",
            "The elephant journey through India — typically staged through ensemble physical theatre",
            "The rescue of Aouda from sati — the play's first real moral stakes",
            "The Hong Kong opium-house scene — Passepartout's misadventure",
            "The crossing of the snowy plains — train under attack by Native American warriors",
            "The Atlantic crossing — burning the deck for fuel",
            "The London ending — apparent failure, then the international-date-line reveal, then the wedding",
        ],
        "most_relevant_practitioners": [
            "Frantic Assembly — ensemble physical theatre, lifts, bodies-as-objects vocabulary",
            "Complicite — object transformation, storytelling theatre, narrator-led ensemble",
            "Bertolt Brecht — narrator function, episodic structure, songs (some productions interpolate music-hall numbers)",
            "Music-hall and circus traditions — comic precision, audience awareness",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred (Eason adaptation is the prescribed text; Verne novel is public domain but the spec prescribes Eason)",
        "stage_history_highlights": [
            "New Vic Newcastle-under-Lyme premiere 2013, dir. Theresa Heskins, in-the-round",
            "Multiple regional revivals 2014–2024",
        ],
        "common_misconceptions": [
            "Students treat the play as a costume drama rather than recognising the ensemble-physical-theatre form Eason is writing for.",
            "Students under-write the role of Aouda and miss her arc from rescued widow to active company member.",
            "Students suggest a literal naturalistic set (a train carriage, an elephant) rather than understanding that the play's pleasure is in transformation by the ensemble.",
            "Students confuse Fogg with a comedic character — examiners reward students who understand his stillness as the comic engine that lets Passepartout's energy land.",
            "Students miss that modern productions actively address Verne's colonial blind spots through performer choice and design — they treat the play as innocent of empire.",
        ],
    },
    "things-i-know-to-be-true": {
        "synopsis": "Adelaide, Australia, contemporary. Bob and Fran Price are settled into late middle age in their suburban garden when each of their four adult children arrives across the four seasons of a year with a revelation. Pip is leaving her family for a new life. Mark is undergoing gender transition and will return as Mia. Ben has been embezzling at work and will be arrested. Rosie returns home heartbroken from Europe. The play closes on a sudden, devastating shock that re-orders everything we have been told. Co-developed with Frantic Assembly, it interweaves naturalistic family scenes with stylised movement sequences.",
        "major_characters": [
            "Bob Price — retired father; tends the rose garden; quietly principled; emotionally guarded",
            "Fran Price — mother; nurse; direct-spoken, tougher than Bob",
            "Pip — eldest child; mother of two; leaving her marriage and her city",
            "Mark — second child; transitioning to Mia; the family's most contested journey",
            "Ben — youngest son; corporate financier; the embezzler",
            "Rosie — youngest daughter; returns from Berlin heartbroken; the play's narrator-figure",
        ],
        "major_themes": [
            "Family — what binds it, what reveals its limits",
            "Conditional and unconditional parental love",
            "Gender identity and transition (Mark / Mia's arc)",
            "Money, theft and corporate ethics (Ben's arc)",
            "Infidelity and a long marriage (Bob's late-revealed arc)",
            "Ageing parents and the children's moment of seeing them as fallible",
            "Memory, the garden, and the things we know to be true (and the things we don't)",
            "Australian suburbia as a setting that does and doesn't shape character",
        ],
        "historical_context": "Contemporary Adelaide. The play premiered May 2016 at the State Theatre Company South Australia in Adelaide and transferred the same year to a UK Frantic Assembly co-production at the Lyric Hammersmith and on tour. Bovell wrote it specifically with Frantic Assembly's Scott Graham as co-developer, integrating physical-theatre movement sequences with naturalistic dialogue. The play sits within Australian theatre's tradition of suburban-realist drama (David Williamson, Patricia Cornelius) but takes its movement language from British devised practice.",
        "playwright_context": "Andrew Bovell (born 1962, Australia) — playwright and screenwriter. Major plays: When the Rain Stops Falling (2008), Speaking in Tongues (1996, adapted into the film Lantana). Bovell often writes about families, secrets and the long shadow of the past. He worked closely with Scott Graham of Frantic Assembly on Things I Know to Be True; Graham contributed movement direction.",
        "dramatic_methods": [
            "Four-part structure — spring, summer, autumn, winter — each season foregrounding one child's revelation",
            "Naturalistic dialogue interlaced with direct-address monologue",
            "Frantic Assembly movement sequences — chair duets, lifts, round-by-through-under contact work — that abstract emotional moments rather than play them naturalistically",
            "Stage directions specify movement sequences with care",
            "Garden imagery — Bob's rose bush as a recurring motif and physical anchor",
            "Memory time — characters can speak from a future or past viewpoint, especially Rosie",
            "The kitchen and the garden as twin centres of action",
            "A late-play revelation about Bob that re-orders earlier scenes — Bovell uses dramatic irony in retrospect",
        ],
        "key_scenes_for_staging": [
            "Spring opening — the family at home, Rosie's return from Berlin",
            "Pip's departure scene — the kitchen confrontation with Fran",
            "Mark's reveal scene — coming out as Mia to his parents",
            "Ben's confession scene — money, dread, a son seeking his father's response",
            "The rose-garden scenes — Bob alone with the plants, sometimes joined by one child",
            "The chair-duet movement sequences (Frantic Assembly hallmark) — typically embedded between dialogue scenes",
            "The autumn / winter shock — the play's ending tableau (kept here without spoilers; staging choices around the moment of revelation are exam-rich)",
        ],
        "most_relevant_practitioners": [
            "Andrew Bovell co-wrote with Frantic Assembly — they ARE a primary practitioner reference",
            "Scott Graham (Frantic Assembly Artistic Director) co-directed the original — round-by-through-under, lifts, chair duets",
            "Constantin Stanislavski — for the naturalistic dialogue scenes; given circumstances make the family specific",
            "Hybrid style: Stanislavskian acting interrupted by Frantic Assembly movement is the play's distinctive form",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "World premiere: State Theatre Company South Australia, May 2016",
            "UK premiere: Lyric Hammersmith / Frantic Assembly co-production 2016, dir. Geordie Brookman and Scott Graham",
            "UK tour 2016–2017",
        ],
        "common_misconceptions": [
            "Students treat the play as a piece of straight kitchen-sink naturalism and miss the Frantic Assembly movement sequences as integral, not decorative.",
            "Students mishandle Mark / Mia's storyline — examiners reward sensitive, specific performer choices that respect the character's identity at each point in the arc.",
            "Students under-interpret the rose garden — they treat it as set dressing rather than a recurring symbol of Bob's emotional life.",
            "Students answer 'movement' designer questions with vague gestures rather than naming Frantic Assembly's vocabulary (chair duets, lifts, contact-improvised sequences).",
            "Students retell the four reveals as plot rather than analysing why Bovell stages them across the seasons (cumulative weight, structural symmetry).",
        ],
    },
    "romeo-and-juliet": {
        "synopsis": "Verona. Two warring noble households, Capulet and Montague, are at the centre of a feud the city's Prince has tried in vain to suppress. Romeo Montague, lovesick for Rosaline, attends a Capulet feast in disguise and falls instantly for Juliet Capulet. They marry secretly the next day. Within hours, Romeo's friend Mercutio is killed by Juliet's cousin Tybalt, Romeo kills Tybalt in revenge, and is banished. Juliet, forced to marry Paris, takes a sleeping potion to feign death. Misinformation reaches Romeo. He kills Paris, drinks poison and dies beside her tomb. Juliet wakes, sees Romeo dead, stabs herself. The Prince and the families confront the cost of the feud.",
        "major_characters": [
            "Romeo — young Montague; intense, impulsive, language-rich",
            "Juliet — young Capulet; thirteen in the text; quick-witted, decisive in love",
            "Tybalt — Juliet's cousin; hot-tempered Capulet; killed by Romeo",
            "Mercutio — Romeo's friend; mercurial, sharp-tongued; killed by Tybalt; non-aligned",
            "Benvolio — Romeo's cousin; peace-keeper",
            "Nurse — Juliet's nurse; comic earthiness, then betrayal of confidence in Act 3",
            "Friar Lawrence — Franciscan friar; arranges the marriage and the potion plan",
            "Lord and Lady Capulet — Juliet's parents; the patriarch hardens against her in Act 3",
            "Lord and Lady Montague — Romeo's parents; less prominent",
            "Paris — Juliet's intended husband; killed by Romeo at the tomb",
            "Prince Escalus — Verona's authority; the play's frame",
        ],
        "major_themes": [
            "Romantic love (Romeo and Juliet's swift courtship) versus familial / sexual love (the Nurse, Mercutio's bawdy, Capulet's idea of marriage)",
            "Fate and free will — 'star-crossed lovers'; the play's prologue tells the audience the ending",
            "Honour, the feud and inherited rage — youth pulled into ancestral violence",
            "Youth versus age — the Nurse, the Friar, the parents, the Prince, all giving advice the lovers cannot hear",
            "Patriarchy — Capulet's threats against Juliet in Act 3; Lady Capulet's withdrawal",
            "Haste — the play's compressed timeline as a thematic point",
            "Light and dark — recurring imagery (Juliet as the sun, the night that hides them, the day that exiles Romeo)",
        ],
        "historical_context": "Written c. 1594–1596. First printed Q1 1597, Q2 1599. Source: Arthur Brooke's narrative poem 'The Tragicall Historie of Romeus and Juliet' (1562), itself derived from Italian novellas. Set in Verona, Italy, in an unspecified Renaissance period. Performed first at Elizabethan playhouses (the Theatre, the Curtain, later the Globe from 1599), played by all-male companies including boy actors as Juliet, in shared light (mid-afternoon performances under open sky).",
        "playwright_context": "William Shakespeare (1564–1616) — actor and playwright with the Lord Chamberlain's Men (later the King's Men). Wrote across genres: comedies (A Midsummer Night's Dream, Twelfth Night), histories (Henry V, Richard III), tragedies (Hamlet, King Lear, Macbeth), late romances (The Tempest). Romeo and Juliet (c.1595) is an early tragedy; he had explored similar territory in Two Gentlemen of Verona but Romeo and Juliet is the first to fuse comic and tragic structures with the verse-driven inwardness of his later tragedies.",
        "dramatic_methods": [
            "Five-act structure (Aristotelian) compressed into roughly five days of in-world time",
            "Iambic pentameter blank verse for noble characters; prose for the Nurse, Peter and the servants",
            "Rhyming couplets to close scenes and signal heightened formality",
            "A shared sonnet on the lovers' first meeting (the 'pilgrim' exchange) — fourteen lines split between Romeo and Juliet",
            "Soliloquies — Juliet's 'gallop apace' speech; Romeo's tomb soliloquy",
            "Asides and stagecraft of the open-air playhouse (no curtain, no scenery, props minimal)",
            "Imagery of light and dark sustained across the play",
            "Antithesis as a verbal habit — Romeo's 'O brawling love, O loving hate'",
            "Public scenes (the brawl, the feast, the duel) versus private scenes (the balcony, the bedroom)",
        ],
        "key_scenes_for_staging": [
            "The opening brawl in Verona's square — the prologue chorus, then street violence",
            "The Capulet feast — Romeo and Juliet's first meeting, the shared sonnet",
            "The balcony scene (Act 2 Scene 2) — the play's most-quoted moment",
            "The marriage in Friar Lawrence's cell",
            "Mercutio's death and Romeo's revenge on Tybalt (Act 3 Scene 1)",
            "Capulet's threat to Juliet (Act 3 Scene 5) — 'hang, beg, starve, die in the streets'",
            "Juliet's potion soliloquy (Act 4 Scene 3) — alone, deciding, drinking",
            "The tomb (Act 5 Scene 3) — Paris's death, Romeo's poison, Juliet's dagger, the Prince's reckoning",
        ],
        "most_relevant_practitioners": [
            "Constantin Stanislavski — for psychological realism in the soliloquies and the lovers' scenes",
            "Heightened-style verse-speaking traditions (RSC, Cicely Berry, Patsy Rodenburg) — verse as both meaning and physical impulse",
            "Bertolt Brecht — for the framing of public violence, the chorus's foreknowledge, the feud as social commentary",
            "Physical theatre approaches (Frantic Assembly Romeo and Juliet, 2008) — for the duels and the lovers' physicality",
            "Globe Theatre 'shared light' tradition — direct audience contact, no fourth wall",
        ],
        "copyright_status": "public domain (Shakespeare died 1616) — quote freely but keep quotes short and purposeful (a half-line, a famous phrase)",
        "stage_history_highlights": [
            "First Quarto 1597; first performances at the Theatre and the Curtain",
            "Notable modern productions: Baz Luhrmann's 1996 film (often referenced in classrooms); RSC stagings; Shakespeare's Globe productions",
            "Frantic Assembly's Romeo and Juliet (2008) — physical-theatre focus on the lovers' bodies",
        ],
        "common_misconceptions": [
            "Students treat the play as a love story alone and under-discuss the feud, the Prince and the patriarchal violence — examiners reward students who hold all three frames at once.",
            "Students forget the play opens with a chorus telling the audience the ending — they miss the dramatic irony Shakespeare builds in.",
            "Students give 'romantic lighting' as a designer answer for the balcony scene without naming colour temperature, intensity, gobo or angle.",
            "Students play Juliet as older than thirteen — the text's age matters and modern productions make staging choices around it.",
            "Students miss that the Nurse's prose drops into verse only when Juliet's death is feared in Act 4 — verse choice IS character.",
        ],
    },
    "a-taste-of-honey": {
        "synopsis": "Salford, Lancashire, late 1950s. Jo, a 17-year-old girl with literary ambitions, lives with her unreliable mother Helen in a damp flat above a shop. When Helen leaves to marry her boyfriend Peter, Jo has a brief winter affair with a Black sailor on shore leave; he sails on, and Jo is pregnant. Geof, a young queer art student, moves in to look after her. The play's second act tracks the makeshift family Jo and Geof build — and Helen's eventual return, breaking it apart. The play is a series of arrivals and departures with live jazz musicians on stage.",
        "major_characters": [
            "Jo — 17; sharp-tongued, frightened, hopeful; poet of the wallpaper",
            "Helen — Jo's mother; semi-alcoholic, restless; charming and absent",
            "Peter — Helen's boyfriend, then husband; older, wealthier, sexually predatory and physically violent",
            "Geof — Jo's queer art-student friend; gentle; the play's moral centre",
            "Boy / Jimmie — Black sailor on shore leave; Jo's brief love; never named on first appearance",
        ],
        "major_themes": [
            "Working-class life in 1950s northern England",
            "Single motherhood and the cycle Jo seems doomed to repeat",
            "Race, class, and an interracial affair in 1950s Britain",
            "Queer friendship and queer family at the edge of legality (homosexuality was a crime in 1958)",
            "Female desire — Jo and Helen as two generations of women who wanted to be more than mothers",
            "Performance and mask — Helen's chosen identity as 'good time girl', Jo's caustic wit",
            "Childhood ending and adulthood arriving",
        ],
        "historical_context": "Salford, late 1950s. Britain post-rationing, pre-Wolfenden Report (which recommended decriminalising homosexuality in 1957 but legislation followed only in 1967). Joan Littlewood's Theatre Workshop premiered the play at Theatre Royal Stratford East on 27 May 1958, with Avis Bunnage as Helen. Delaney was 19. The Lord Chamberlain's office still exercised pre-performance censorship (until 1968) — A Taste of Honey was edited but not banned. The kitchen-sink drama movement (Look Back in Anger, 1956; A Taste of Honey, 1958; Saturday Night and Sunday Morning, 1958) reframed British theatre around working-class voices.",
        "playwright_context": "Shelagh Delaney (1938–2011) — born in Salford; left school at 17; wrote A Taste of Honey at 18 partly as a corrective to plays where working-class women were patronised. Delaney sent the script to Joan Littlewood at Theatre Workshop. Littlewood's company workshopped and shaped the production — including the device of the live jazz musicians (a Theatre Workshop touch, not in Delaney's original script).",
        "dramatic_methods": [
            "Two-act structure across one year — winter to summer, then back",
            "Direct address — characters break the fourth wall to speak to the audience",
            "Live jazz musicians on stage — Theatre Workshop's signature element; comment on action between scenes",
            "Single setting — the damp flat — with the world (Peter's car, the fairground, the canal) implied off-stage",
            "Salford dialect — Delaney's ear for 1950s northern speech",
            "Tonal swings — comic banter into pathos and back",
            "Stage directions sparse; reliance on actor and director invention (Theatre Workshop's devised practice)",
            "Naturalistic content with Brechtian presentational moments — the hybrid that defines the play",
        ],
        "key_scenes_for_staging": [
            "The opening — Helen and Jo arriving at the new flat with their luggage and complaints",
            "Helen and Peter's courtship scene — Peter's manipulation, Helen's wavering",
            "Jo and the Boy on the bridge / by the canal — winter, the brief affair",
            "Jo alone with the dolls / the kettle — the moment she realises she's pregnant",
            "Geof's arrival — the fairground meeting; the move-in",
            "Jo and Geof making a home — the play's tenderest stretch",
            "Helen's return — the fight; Geof's exit; the closing on Jo and Helen alone",
        ],
        "most_relevant_practitioners": [
            "Joan Littlewood and Theatre Workshop — devised methods, improvisation, direct address, live music, ensemble; the original production WAS Theatre Workshop and a fair amount of the staging is Littlewood's invention as much as Delaney's",
            "Bertolt Brecht — the live jazz musicians, the direct address, the breaking of fourth wall — Theatre Workshop drew explicitly on Brecht",
            "Constantin Stanislavski — for the naturalistic emotional truth of Jo and Geof's friendship scenes",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "Premiere: Theatre Royal Stratford East, 27 May 1958, dir. Joan Littlewood",
            "1961 film adaptation dir. Tony Richardson, with Rita Tushingham as Jo",
            "National Theatre revival 2014 dir. Bijan Sheibani — but never reference these as worked examples for live theatre review",
        ],
        "common_misconceptions": [
            "Students treat the play as straight kitchen-sink naturalism and miss its presentational devices (direct address, jazz musicians) — examiners reward students who recognise the hybrid form.",
            "Students moralise about Helen — examiners reward students who play her sympathetically, as a woman shaped by limited choices.",
            "Students miss that homosexuality was illegal in 1958, so under-explain Geof's vulnerability and what he risks by moving in with Jo.",
            "Students suggest 'sad jazz' as a sound-design answer without specifying instrument, tempo, recorded vs live, or the use of underscore versus diegetic music.",
            "Students confuse Salford and Manchester — Salford is its own city and the play's specifically Salford voice matters.",
        ],
    },
    "the-great-wave": {
        "synopsis": "1979, the Sea of Japan coast. Two teenage sisters, Hanako and Reiko, argue on the beach in a thunderstorm; Hanako disappears, presumed drowned. The play tracks two parallel timelines for the next 24 years: Reiko and her mother in Japan refusing to accept Hanako is dead; and Hanako herself, alive in North Korea, having been abducted by DPRK agents. She is forced into a new identity, taught Korean, and made to teach the Japanese language to North Korean spies. The play closes in 2003, after the Pyongyang Declaration, with the family's confirmation that Hanako has been alive — and the cost of those decades.",
        "major_characters": [
            "Hanako — 17 at her abduction; the play's anchoring figure across two decades",
            "Reiko — Hanako's older sister; spends her adult life believing her, then advocating for her",
            "Etsuko — the mother; ages across the play; her grief shapes the family",
            "Tetsuo — Reiko's husband; introduced in adulthood",
            "Kum-Chol — North Korean officer who oversees Hanako's captivity; complicit in the regime, recognisably human",
            "Jung Sun — Hanako's North Korean 'student'; later partner; born of state coercion",
            "Officials — Japanese diplomats, North Korean handlers — sometimes multi-roled",
        ],
        "major_themes": [
            "State authoritarianism and its private cost",
            "Abduction as state policy (the documented DPRK abductions of Japanese citizens, 1977–1983)",
            "Identity erasure — language, name, history",
            "Ambiguous loss — grief without certainty over decades",
            "Family endurance and the activism it produces",
            "Diplomatic silence and the gap between official narrative and individual life",
            "Complicity, moral compromise, and the question of whether captor and captive can become anything other than that",
        ],
        "historical_context": "Between 1977 and 1983, North Korean agents abducted at least 17 Japanese citizens (Japanese government count) from coastal Japan to use as language teachers and identity sources for DPRK spies. The most famous case is Megumi Yokota, abducted aged 13 in 1977. In 2002 the Pyongyang Declaration acknowledged the abductions and five abductees were returned to Japan. Several others, including Megumi Yokota, were declared dead by North Korea but families continue to dispute this. Turnly's play premiered at the Tricycle Theatre, Kilburn in 2018 and transferred to the National Theatre's Dorfman in 2018, dir. Indhu Rubasingham.",
        "playwright_context": "Francis Turnly — Northern Irish playwright; Japanese-Irish heritage (his grandfather was Japanese). Lived in Japan; speaks Japanese. The Great Wave is his best-known work and grew out of years of research with abductee families. Turnly's other plays include Charge (2016).",
        "dramatic_methods": [
            "Two-act structure with extended timeline (1979–2003)",
            "Cross-cutting between parallel storylines in Japan and North Korea — scenes alternate",
            "Stage directions specify the sea — its sound, its threat — as a recurring presence",
            "Code-switching between English (standing in for Japanese) and stylised Korean",
            "Time leaps signalled by lighting and sound, costume change, and aged physicality",
            "Documentary realism — the play's research roots show in interrogation scenes and diplomatic exchanges",
            "Stillness as a dramatic choice — the abducted Hanako contained physically across years",
            "Soundscape carrying emotional weight — waves, propaganda music, silence",
        ],
        "key_scenes_for_staging": [
            "1979 beach storm — the abduction itself; Reiko and Hanako's last argument",
            "The first interrogation — Hanako confronted with her new identity",
            "The teaching scenes — Hanako teaching Japanese to North Korean students; the slow building of relationship with Jung Sun",
            "Reiko's grief scenes — the family in Japan refusing closure",
            "The diplomatic scenes — Japanese officials, North Korean officials, the press conference",
            "The 2002 Pyongyang declaration scene — official news reaches the family",
            "The closing reunion / non-reunion — Turnly's choices about what is and is not seen",
        ],
        "most_relevant_practitioners": [
            "Documentary theatre tradition (Verbatim Theatre, Tricycle Theatre house style under Nicolas Kent and Indhu Rubasingham)",
            "Bertolt Brecht — the audience as witness to a state crime, the political-theatre frame",
            "Constantin Stanislavski — for Hanako's interior life over 20+ years; given circumstances are crucial in the captivity scenes",
            "Companies like Out of Joint, Hampstead Theatre, Tricycle/Kiln have led the British political-theatre tradition Turnly works within",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "Tricycle / Kiln Theatre premiere 2018",
            "National Theatre Dorfman transfer 2018, dir. Indhu Rubasingham",
        ],
        "common_misconceptions": [
            "Students treat the play as fiction loosely inspired by real events rather than as documentary-rooted political theatre about the named DPRK abductions — examiners reward awareness of the Megumi Yokota / Pyongyang Declaration context.",
            "Students play Hanako 'sad' across two decades rather than tracking the specific physical and vocal choices that show ageing, accommodation, internal resistance.",
            "Students suggest 'cold blue lighting' for North Korea without specifying intensity, gobo (e.g. window-frame), lantern type or angle.",
            "Students under-explain the 'wave' of the title — they treat it as set-dressing rather than as the controlling metaphor for forces that move people.",
            "Students collapse the parallel storylines together rather than analysing the discipline of cross-cutting Turnly imposes on the audience.",
        ],
    },
    "the-empress": {
        "synopsis": "1887, Tilbury Docks. Rani, a young Indian ayah (children's nanny) is paid off by the British family she travelled with and finds herself stranded in London with no return passage. She discovers the Ayahs' Home in Hackney and the Lascar sailor community in the East End. In a parallel storyline, Abdul Karim arrives at Windsor Castle to serve Queen Victoria at her Golden Jubilee; he becomes her Indian secretary (munshi), teaching her Hindustani and rising in her household to the fury of the British court. The play interweaves Rani's grass-roots story of survival with Abdul's rise at court, both grounded in real Victorian Indian-British history. They meet near the play's end at a moment of solidarity.",
        "major_characters": [
            "Rani — Indian ayah; abandoned in London; the play's invented protagonist whose story parallels documented ayahs' experiences",
            "Abdul Karim — historical figure; Queen Victoria's Indian secretary 1887–1901",
            "Queen Victoria — historical figure; Empress of India from 1876; protector of Abdul",
            "Hari Mohan Lal — Indian-born MP-figure (echo of real Dadabhai Naoroji, Liberal MP for Finsbury Central 1892–1895)",
            "Lascar sailor (Mr Das) — East End Lascar community member who helps Rani",
            "Sally — English friend / fellow servant",
            "Mrs Wormwood — English mistress who pays Rani off",
            "Lord Salisbury / Bertie Prince of Wales / English court figures — multi-roled or fixed depending on production",
        ],
        "major_themes": [
            "British Empire seen from inside Britain — Indian subjects of the Crown in Britain itself",
            "Race and racial hierarchy in late-Victorian Britain",
            "Domestic service — ayahs and Lascars as the Empire's hidden labour force",
            "Solidarity between Indian women, Indian sailors and early Indian MPs — communities forming in the diaspora",
            "Queen Victoria's late-life fascination with India and Abdul Karim",
            "Memory and loss of homeland; language as identity (Hindustani, Bengali, English)",
            "The contrast between official Imperial narrative and lived experience",
        ],
        "historical_context": "Late Victorian Britain. 1887 was the Golden Jubilee of Queen Victoria's reign; 1897 the Diamond Jubilee. Britain ruled India directly from 1858 (after the East India Company) and Victoria was declared Empress of India in 1876. Real history Gupta draws on: the Ayahs' Home in Hackney (a hostel for stranded Indian nannies, opened c. 1900 by Christian missionaries; Gupta has shifted the date earlier for dramatic compression); Lascar sailors in the East End (long-established Indian and Yemeni seafaring communities); Abdul Karim's real service to Victoria 1887–1901 (he was sidelined and his papers burned by the royal household after her death); Dadabhai Naoroji's real election as the first Indian MP in 1892. The play premiered at the RSC's Swan Theatre, Stratford-upon-Avon, in 2013, dir. Emma Rice.",
        "playwright_context": "Tanika Gupta MBE (born 1965) — British playwright of Bengali heritage; specialises in restoring South Asian voices to British history. Plays include The Waiting Room (2000, NT), Lions and Tigers (2017), Hobson's Choice adaptations. The Empress was commissioned by the RSC and is part of a body of work that re-reads canonical British history through diasporic and feminist lenses.",
        "dramatic_methods": [
            "Two-act structure with parallel storylines (Rani's, Abdul's) intercutting",
            "Bilingual exchanges — English, Bengali, Hindustani — code-switching as social and political signal",
            "Letters as a device — Abdul's letters home; the family Rani writes to",
            "Direct address — characters speaking out to the audience, especially Rani",
            "Hindi songs and Indian music underscore",
            "Naturalistic dialogue with poetic interludes",
            "Stage directions that contrast a Lascar lodging house with Windsor Castle interiors — fluid scene transitions across the play's social geography",
            "Multi-roling minor English court figures",
            "Period detail in costume and props as both research and political signal",
        ],
        "key_scenes_for_staging": [
            "Tilbury Docks opening — Rani arriving with the English family, being paid off",
            "The Ayahs' Home scenes — found community in Hackney",
            "Windsor Castle / Abdul's first meeting with Victoria — court formality and personal warmth",
            "The Lascar lodgings — Rani's encounter with Mr Das and the Indian seafaring community",
            "The court conspiracy against Abdul — Lord Salisbury, Bertie, the household",
            "The Hari Mohan Lal political scenes — early Indian MP at Westminster",
            "The convergence near the end — Rani and Abdul or Rani and Hari meeting; the play's solidarity moment",
            "The closing tableau — what survives, what is lost",
        ],
        "most_relevant_practitioners": [
            "Bertolt Brecht — the play's avowed project of making hidden histories visible to a contemporary audience is Brechtian",
            "Documentary / verbatim theatre tradition — the historical research is foregrounded",
            "Constantin Stanislavski — for Rani's interior life and Abdul's specificity as a person",
            "Emma Rice's house style for the original RSC production used ensemble multi-roling and music underscore — touches of Kneehigh practice",
        ],
        "copyright_status": "in copyright — 15-word cap, paraphrase preferred",
        "stage_history_highlights": [
            "RSC Swan Theatre premiere 2013, dir. Emma Rice",
            "Lyric Hammersmith / RSC revival 2023, dir. Pooja Ghai",
        ],
        "common_misconceptions": [
            "Students treat the play as straight history and miss Gupta's compressions (the Ayahs' Home opened slightly later than 1887; Hari is loosely modelled on Dadabhai Naoroji rather than identical) — examiners reward awareness that this is dramatic history.",
            "Students focus only on Abdul or only on Rani; examiners reward students who can hold both storylines in tension and analyse the structural choice to interweave them.",
            "Students suggest 'Indian costumes' as a designer answer without naming sari fabric, weave, embroidery, contrasting British wool tailoring, and the political signal each carries.",
            "Students under-discuss the bilingual code-switching; they treat language choice as decoration rather than as a tool of power.",
            "Students mishandle Queen Victoria — examiners reward students who can show her warmth to Abdul without sentimentalising the Empire.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Subject-level teaching brief (shared across all batches; built once)
# ---------------------------------------------------------------------------
def build_subject_brief(plan: dict) -> dict:
    tb = plan["teaching_brief"]
    return {
        "common_misconceptions": tb["common_misconceptions"],
        "student_errors_by_question_type": tb["student_errors_by_question_type"],
        "topic_weighting_notes": tb["topic_weighting_notes"],
        "current_spec_changes": tb["current_spec_changes"],
        "pedagogical_notes": tb["pedagogical_notes"],
        "drama_content_rules": tb["drama_content_rules"],
        "studyvault_mark_scheme_rules": {
            "rubric_tiers": ["Mastering", "Secure", "Developing", "Emerging"],
            "do_not_use": [
                "Level 1 / Level 2 / Level 3 / Level 4 (AQA's tier names)",
                "Award N marks for ... (banned phrasing — validator hard-fail)",
                "Nothing worthy of credit",
                "AQA's verbatim mark scheme stems",
                "Section A / Section B / Section C labels in user-facing strings",
                "Component 1 / Component 2 / Component 3 in user-facing strings",
            ],
            "use_instead": [
                "1 mark for X; 1 mark for Y (for short-answer questions)",
                "Up to N marks: ... (for short-answer where multiple credit-worthy points are possible)",
                "Mastering tier (top): describes what the strongest answer shows",
                "Secure tier: describes what a solid answer shows",
                "Developing tier: describes a partial answer",
                "Emerging tier (bottom): describes a minimal answer",
            ],
            "performer_designer_lens_required": (
                "For 8 marks — Interpret as Performer questions, the mark scheme MUST require both a vocal AND a "
                "physical choice anchored to a named moment. For 8 marks — Interpret as Designer questions, the mark "
                "scheme MUST require concrete, named design elements (lantern type, gobo, fabric, colour, "
                "instrument, soundscape texture) — not generic descriptors like 'dark mood' or 'period costume'."
            ),
        },
        "glossary_target": (
            "Six or more glossary terms per lesson, embedded inline as <dfn class=\"term\" data-def=\"...\">. "
            "Drama is stagecraft- and practitioner-terminology heavy — proxemics, gestus, gobo, soundscape, "
            "blocking, multi-roling, naturalism, fourth wall, tableau — easy to hit; aim for 6–10 per lesson."
        ),
        "flashcard_rules": (
            "Eight to fifteen flashcards per lesson. Each answer must be ONE fact, not an enumeration. Bad: "
            "'The four key practitioners are Stanislavski, Brecht, Artaud and Frantic Assembly.' Good: split into "
            "four separate cards. Drama-specific card types: term ↔ definition (gestus, gobo, fourth wall), "
            "practitioner ↔ technique, play ↔ playwright/year/context, character ↔ defining trait, play ↔ themes."
        ),
        "plain_text_fields_rule": (
            "Plain unicode characters only in description, practice_questions[].text/.type/.marks, "
            "knowledge_checks[].q, flashcard_questions[].q/.a, glossary_terms[].term/.definition. NEVER HTML "
            "entities (&rsquo;, &amp;, &ldquo;, &mdash;) — these are blocked by the validator. HTML entities are "
            "only acceptable inside content_html and other _html-suffixed fields."
        ),
    }


# ---------------------------------------------------------------------------
# Build batches
# ---------------------------------------------------------------------------
def slugify_lesson(title: str) -> str:
    """Match the activation script's slugify."""
    import re
    s = title.lower().strip()
    s = re.sub(r"[‘’′']", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


def make_subject_block() -> dict:
    return {
        "name": "Drama",
        "slug": "drama-aqa",
        "exam_board": "AQA",
        "target_audience": "free-tier",
    }


def make_unit_block(unit: dict) -> dict:
    return {
        "name": unit["name"],
        "slug": unit["slug"],
        "subtitle": unit["subtitle"],
        "accent": unit["accent"],
        "accent_light": unit["accent_light"],
        "accent_badge": unit["accent_badge"],
        "body_class": unit["body_class"],
        "lesson_count": unit["lesson_count"],
    }


def lesson_to_batch_entry(unit_slug: str, lesson: dict) -> dict:
    """Convert a plan-lesson entry into a batch-lesson entry."""
    n = lesson["number"]
    if unit_slug in PLAY_BRIEFS:
        suggested = SET_PLAY_PER_LESSON_SUGGESTED[n]
    else:
        suggested = UNIVERSAL_PER_LESSON_SUGGESTED[(unit_slug, n)]
    slug = slugify_lesson(lesson["title"])
    return {
        "number": n,
        "title": lesson["title"],
        "slug": slug,
        "description": lesson["description"],
        "spec_references": lesson["spec_references"],
        "section_markers": lesson.get("section_markers", []),
        "suggested_question_types": suggested,
    }


def write_batch(
    batch_id: str,
    unit: dict,
    lessons: list[dict],
    spec_slice: str,
    subject_brief: dict,
    unit_brief: dict,
    allowed_qts: list[str],
) -> Path:
    batch = {
        "batch_id": batch_id,
        "subject": make_subject_block(),
        "unit": make_unit_block(unit),
        "spec_slice_path": spec_slice,
        "reference_lesson_path": "scripts/_content_drama-aqa/_reference_lesson.json",
        "subject_level_teaching_brief": subject_brief,
        "unit_level_teaching_brief": unit_brief,
        "quote_ticker_html_for_unit": QUOTE_TICKER_HTML,
        "registered_question_type_names": REGISTERED_QTS,
        "allowed_question_types_for_this_unit": allowed_qts,
        "lessons_in_batch": [
            lesson_to_batch_entry(unit["slug"], L) for L in lessons
        ],
        "output_dir": "scripts/_content_drama-aqa/lessons",
    }
    out_path = OUT_DIR / f"_batch_{batch_id}.json"
    out_path.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def main():
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    subject_brief = build_subject_brief(plan)
    units = plan["article_units"]

    written = []
    total_lessons = 0

    # Build batch_id mapping per unit
    # Universal units: single batch each
    # Set-play units: 2 batches (b1 = L1-4, b2 = L5-8)
    UNIT_BATCH_PLAN = {
        # universal — 1 batch each
        "theatre-roles-stagecraft": [("universal_b1", list(range(1, 6)))],
        "practitioners-styles": [("universal_b2", list(range(1, 5)))],
        "live-theatre-review": [("universal_b3", list(range(1, 5)))],
        # set plays — 2 batches each
        "the-crucible": [("crucible_b1", [1, 2, 3, 4]), ("crucible_b2", [5, 6, 7, 8])],
        "blood-brothers": [("blood-brothers_b1", [1, 2, 3, 4]), ("blood-brothers_b2", [5, 6, 7, 8])],
        "noughts-and-crosses": [("noughts-and-crosses_b1", [1, 2, 3, 4]), ("noughts-and-crosses_b2", [5, 6, 7, 8])],
        "around-the-world-80-days": [("around-the-world_b1", [1, 2, 3, 4]), ("around-the-world_b2", [5, 6, 7, 8])],
        "things-i-know-to-be-true": [("things-i-know_b1", [1, 2, 3, 4]), ("things-i-know_b2", [5, 6, 7, 8])],
        "romeo-and-juliet": [("romeo-and-juliet_b1", [1, 2, 3, 4]), ("romeo-and-juliet_b2", [5, 6, 7, 8])],
        "a-taste-of-honey": [("taste-of-honey_b1", [1, 2, 3, 4]), ("taste-of-honey_b2", [5, 6, 7, 8])],
        "the-great-wave": [("great-wave_b1", [1, 2, 3, 4]), ("great-wave_b2", [5, 6, 7, 8])],
        "the-empress": [("empress_b1", [1, 2, 3, 4]), ("empress_b2", [5, 6, 7, 8])],
    }

    for unit in units:
        slug = unit["slug"]
        plan_for_unit = UNIT_BATCH_PLAN.get(slug)
        if plan_for_unit is None:
            raise SystemExit(f"No batch plan for unit {slug}")

        # Pick spec slice + allowed QTs + unit brief
        if slug in PLAY_BRIEFS:
            spec_slice = "scripts/_content_drama-aqa/_spec_set-play.txt"
            unit_brief = PLAY_BRIEFS[slug]
            allowed = SET_PLAY_ALLOWED
        elif slug == "live-theatre-review":
            spec_slice = "scripts/_content_drama-aqa/_spec_universal.txt"
            unit_brief = {
                "fictional_production_examples_only": (
                    "Every worked example in this unit must reference a CLEARLY FICTIONAL production. "
                    "Acceptable phrasings: 'imagine you saw a production of An Inspector Calls at a fictional "
                    "regional theatre in 2024 where the director chose…', 'in a hypothetical staging of A Midsummer "
                    "Night's Dream set in a 1990s Tokyo nightclub…'. Never reference a real named production. "
                    "Every student writes about THEIR own production and StudyVault cannot assume what they have seen."
                ),
                "what_students_should_remember": [
                    "Performance must be at least 50 minutes excluding breaks, with at least two actors, dialogue, and a range of production values (lighting, sound, set and costume).",
                    "Students may not write about their set play in the live-theatre question — the production seen must contrast with their set play.",
                    "Live theatre includes plays, physical theatre, theatre in education and musical theatre — at amateur or professional level (not peer).",
                ],
                "what_a_strong_answer_does": [
                    "Names a specific moment in the production; specifies the performer's vocal AND physical choices for that moment; explains the effect on the audience.",
                    "Specifies design elements concretely: lantern type, intensity, gobo, colour wash; sound cue type and texture; set element with material; costume colour, fit and fabric. Links each to the production's directorial concept.",
                    "Reaches a substantiated evaluative judgement: did this choice succeed in communicating meaning, and why?",
                    "Uses What/How/Why scaffold: What was the choice? How was it executed (technical detail)? Why did it work (effect on audience and meaning)?",
                ],
                "common_misconceptions_for_unit": [
                    "Students retell what happened in the production scene by scene rather than analysing how meaning was communicated.",
                    "Students name design elements ('the lighting was dark', 'there was sad music') without naming the technical specifics that examiners reward.",
                    "Students describe the actors' emotions ('he was angry') without translating that into vocal and physical choices the audience could see.",
                    "Students fail to evaluate — they describe choices without judging whether the choice succeeded.",
                ],
            }
            allowed = LIVE_THEATRE_ALLOWED
        else:
            spec_slice = "scripts/_content_drama-aqa/_spec_universal.txt"
            unit_brief = {
                "what_students_should_remember": [
                    "Theatre roles, design fundamentals, performer skills, and the rehearsal process are foundational — they will be drawn on in every other unit and in every set-play extended response.",
                    "The 4-mark multiple-choice section on theatre roles is short but uses precise terminology — every term in this unit must be used precisely.",
                ] if slug == "theatre-roles-stagecraft" else [
                    "Each practitioner has a defined set of techniques and a guiding philosophy — students must apply the techniques to a specific moment of their set play, not just describe the practitioner's biography.",
                    "Stanislavski / Brecht / Artaud / Frantic Assembly are the canonical four; students should know each well enough to recommend the most useful for any given set-play moment.",
                ],
                "common_misconceptions_for_unit": [
                    "Students confuse stage configurations (proscenium, thrust, in-the-round, traverse, end-on, promenade) — they should be able to define and contrast them in detail.",
                    "Students treat 'performer skills' as just acting and forget the spec's split between vocal (accent, volume, pitch, timing, pace, intonation, phrasing, emotional range, delivery) and physical (build, age, height, movement, posture, gesture, facial expression).",
                ] if slug == "theatre-roles-stagecraft" else [
                    "Students describe a practitioner's biography without applying their techniques to a specific moment of the set play.",
                    "Students confuse Stanislavski's emotion memory with Brecht's gestus — these are very different ideas about what an actor should give the audience.",
                ],
            }
            allowed = STAGECRAFT_ALLOWED

        # Iterate batches for this unit
        for batch_id, lesson_numbers in plan_for_unit:
            lessons_in_batch = [L for L in unit["lessons"] if L["number"] in lesson_numbers]
            assert len(lessons_in_batch) == len(lesson_numbers), \
                f"Batch {batch_id}: expected {len(lesson_numbers)} lessons, got {len(lessons_in_batch)}"
            path = write_batch(
                batch_id=batch_id,
                unit=unit,
                lessons=lessons_in_batch,
                spec_slice=spec_slice,
                subject_brief=subject_brief,
                unit_brief=unit_brief,
                allowed_qts=allowed,
            )
            written.append(path)
            total_lessons += len(lessons_in_batch)

    print(f"Wrote {len(written)} batches, total {total_lessons} lessons")
    for p in written:
        print(f"  {p.relative_to(ROOT)}")
    if total_lessons != 85:
        raise SystemExit(f"Expected 85 lessons, wrote {total_lessons}")


if __name__ == "__main__":
    main()
