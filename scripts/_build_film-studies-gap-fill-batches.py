"""Phase 7 GAP-FILL — emits 4 batch JSONs for the gap-fill content agents.

Outputs:
  scripts/_content_film-studies-eduqas/_batch_global-english_b1.json (5 lessons)
  scripts/_content_film-studies-eduqas/_batch_global-non-english_b1.json (5 lessons)
  scripts/_content_film-studies-eduqas/_batch_contemporary-uk_b1.json (5 lessons)
  scripts/_content_film-studies-eduqas/_batch_indie-split_b1.json (2 lessons — Hurt Locker rewrite + Hate U Give new)

Pulls the shared subject_level_teaching_brief from _batch_global-film_b1.json so
the brief is identical to the existing batches.

Idempotent. Safe to re-run.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "_content_film-studies-eduqas"

# Pull the shared brief from the existing global-film batch.
existing = json.loads((CONTENT_DIR / "_batch_global-film_b1.json").read_text(encoding="utf-8"))
SHARED_BRIEF = existing["subject_level_teaching_brief"]
SHARED_QUOTE_HTML = existing["quote_ticker_html_for_unit"]
REGISTERED_TYPES = existing["registered_question_type_names"]
ALLOWED_TYPES = existing["allowed_question_types_for_this_unit"]

# ============================================================ Per-film briefs

# Slumdog / Wadjda / Girlhood / Hurt Locker / Hate U Give brief content is reused
# from _batch_global-film_b1.json (Slumdog, Wadjda, Girlhood) and
# _batch_us-indie_b2.json (Hurt Locker, Hate U Give). Other 11 films are new.

SLUMDOG_BRIEF = {
    "title": "Slumdog Millionaire (2008)",
    "synopsis": "A young man from the Mumbai slums sits one question away from winning the Indian version of Who Wants to Be a Millionaire? while the police interrogate him over how he could possibly know the answers. Danny Boyle's frame-narrative love story.",
    "director_year_country": "Danny Boyle (co-directed by Loveleen Tandan) — 2008 — UK / India",
    "major_characters": [
        "Jamal Malik — the protagonist (Dev Patel)",
        "Latika — the woman Jamal loves (Freida Pinto)",
        "Salim — Jamal's older brother (Madhur Mittal)",
        "Prem Kumar — the quiz-show host (Anil Kapoor)",
        "the Inspector — the Mumbai police investigator (Irrfan Khan)"
    ],
    "major_themes": [
        "fate, destiny and the love story across two decades",
        "Mumbai as transforming megacity — slum to glass tower",
        "social mobility and the lottery of birth",
        "corruption and survival in the urban underclass",
        "frame narrative as the machinery of memory",
        "globalisation and the export of British and Indian cinema"
    ],
    "production_context": "British-Indian co-production made by Celador Films and Film4 Productions, distributed by Fox Searchlight Pictures. Director Danny Boyle (with co-director Loveleen Tandan crediting the Hindi-language scenes). Screenwriter Simon Beaufoy (adapting Vikas Swarup's novel Q & A). Cinematographer Anthony Dod Mantle (Dogme 95 veteran). Editor Chris Dickens. Score by A. R. Rahman. Made for around $15m, shot in Mumbai with a mixed Hindi/English production. Eight Academy Awards including Best Picture, Best Director and Best Adapted Screenplay.",
    "critical_reception": "Major critical and commercial hit. Subsequent reassessment has engaged with questions about its representation of poverty, the British-director's-eye-on-Mumbai framing, and the closing dance sequence's tonal switch.",
    "filmic_methods": [
        "frame narrative — quiz show as the present, flashbacks as the past",
        "dual timeline editing across childhood, adolescence and adulthood",
        "saturated colour palette — yellows and reds particularly in the Mumbai scenes",
        "handheld camera throughout chase and slum sequences",
        "A. R. Rahman score blending diegetic Mumbai street music and non-diegetic instrumental",
        "closing-credits Bollywood dance number as deliberate tonal coda"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening interrogation that establishes the frame",
        "the childhood toilet-pit autograph sequence",
        "the train-rooftop traversal of central India",
        "the Taj Mahal tourist-scam sequence",
        "the closing platform dance number"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

DISTRICT_9_BRIEF = {
    "title": "District 9 (2009)",
    "synopsis": "In an alternate Johannesburg, a million stranded extraterrestrial refugees live in a fenced township called District 9. A bureaucrat tasked with relocating them is exposed to alien biotechnology and begins a slow physical transformation. Neill Blomkamp's debut feature, expanded from his short Alive in Joburg.",
    "director_year_country": "Neill Blomkamp — 2009 — South Africa / New Zealand / USA",
    "major_characters": [
        "Wikus van de Merwe — the MNU bureaucrat (Sharlto Copley)",
        "Christopher Johnson — an alien father working to leave Earth",
        "Christopher's son — a child alien whose tools trigger the change",
        "Koobus Venter — the MNU mercenary commander",
        "the Nigerian gang leader Obesandjo — the township's black-market boss"
    ],
    "major_themes": [
        "apartheid as cinematic allegory in a post-apartheid setting",
        "segregation, displacement and the refugee body",
        "corporate bureaucracy and dehumanisation",
        "the alien as metaphor for the racialised Other",
        "documentary realism inside science fiction",
        "the fluid line between victim and perpetrator"
    ],
    "production_context": "Made by TriStar Pictures, WingNut Films and Block Block Productions, distributed by Sony Pictures Releasing. Director and co-writer Neill Blomkamp; co-writer Terri Tatchell. Producer Peter Jackson. Cinematographer Trent Opaloch (shooting on multiple Red One digital cameras). Editor Julian Clarke. Score by Clinton Shorter. Made for around $30m, shot largely in Johannesburg's Chiawelo and Soweto with practical and CGI effects. Four Academy Award nominations including Best Picture, Best Adapted Screenplay, Best Film Editing and Best Visual Effects.",
    "critical_reception": "Major critical and commercial success — widely praised for fusing science fiction with documentary realism and for its allegorical reading of apartheid. Subsequent debate has engaged with the depiction of the Nigerian gang and the politics of putting a white South African at the centre of the story.",
    "filmic_methods": [
        "mockumentary-into-narrative shift — opening interview-and-news-footage gradually folds into conventional third-person narration",
        "handheld camera throughout to maintain found-footage texture",
        "telephoto and surveillance-style framing during the township raids",
        "practical-and-CGI hybrid for the alien Prawns, with motion-capture references",
        "diegetic news-footage intercutting against silence and ambient sound",
        "abrupt match-cuts between TV-image footage and unmediated camera"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening mockumentary interviews establishing the alternate history",
        "the eviction-notice door-to-door sequence in District 9",
        "the boat-arrival flashback that explains the alien presence",
        "the MNU laboratory transformation sequence",
        "the climactic mech-suit confrontation with Koobus"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

BABADOOK_BRIEF = {
    "title": "The Babadook (2014)",
    "synopsis": "A widowed mother and her troubled six-year-old son find a sinister pop-up book in their home, and the figure of Mister Babadook begins to enter their lives. Jennifer Kent's debut feature, expanded from her short Monster, treats grief as a literal household creature.",
    "director_year_country": "Jennifer Kent — 2014 — Australia / Canada",
    "major_characters": [
        "Amelia Vanek — the bereaved mother (Essie Davis)",
        "Samuel Vanek — her six-year-old son (Noah Wiseman)",
        "Mister Babadook — the figure from the storybook",
        "Claire — Amelia's sister",
        "Robbie — Amelia's nursing-home colleague"
    ],
    "major_themes": [
        "bereavement and the unresolved grief of a sudden death",
        "single motherhood under social and economic pressure",
        "the family home as a site of horror",
        "the children's storybook as harbinger",
        "horror as expressive form for psychological states",
        "denial, repression and the unspoken"
    ],
    "production_context": "Made by Causeway Films and Smoking Gun Productions in association with Screen Australia, the South Australian Film Corporation and Entertainment One. Director and writer Jennifer Kent (her feature debut). Cinematographer Radek Ladczuk. Editor Simon Njoo. Score by Jed Kurzel. Production design by Alex Holmes. Made on a tight budget of around AU$2.5m with a Kickstarter top-up to fund set construction. Filmed in and around Adelaide. Acclaimed on the festival horror circuit (Sundance premiere, then international release).",
    "critical_reception": "Widely admired as a contemporary horror with literary ambition. Subsequent reception has folded the Babadook himself into broader cultural conversations about depression and grief; the figure became an unexpected meme in 2016-17.",
    "filmic_methods": [
        "claustrophobic domestic framing with locked-off shots",
        "low-key, desaturated palette — cool blues and greys",
        "sound-design shocks and abrupt silence as horror device",
        "stop-motion-style animation for the storybook reveal",
        "long takes that hold the mother in close-up to track psychological strain",
        "corridor-and-doorway compositions that stage the threshold of the home"
    ],
    "key_scenes_for_micro_analysis": [
        "the children's-book opening reveal of Mister Babadook",
        "the basement descent in the second act",
        "the bedroom doorway confrontation between mother and son",
        "the police-station sequence with the visiting officer",
        "the closing basement-feeding ritual"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

BREADWINNER_BRIEF = {
    "title": "The Breadwinner (2017)",
    "synopsis": "An eleven-year-old girl in Taliban-controlled Kabul cuts her hair and dresses as a boy after her father is arrested, taking on the role of family breadwinner. A frame-tale animation that runs a storybook her father has taught her alongside her own daily survival.",
    "director_year_country": "Nora Twomey — 2017 — Ireland / Canada / Luxembourg",
    "major_characters": [
        "Parvana — the eleven-year-old protagonist",
        "Nurullah — Parvana's father, a former teacher",
        "Fattema — Parvana's mother",
        "Soraya — Parvana's elder sister",
        "Shauzia — Parvana's friend, also disguised as a boy",
        "the storybook hero — the boy who confronts the Elephant King"
    ],
    "major_themes": [
        "girlhood and disguise under occupation",
        "storytelling as survival",
        "family separation and the absent father",
        "Afghan history compressed into a child's experience",
        "the frame-tale as structural principle",
        "animated cinema for serious subject matter"
    ],
    "production_context": "Made by Cartoon Saloon (Ireland), Aircraft Pictures (Canada) and Melusine Productions (Luxembourg), distributed internationally by Elevation Pictures and GKIDS. Executive produced by Angelina Jolie, who advised on cultural detail through her UN Goodwill Ambassador work. Director Nora Twomey. Screenplay Anita Doron, adapting Deborah Ellis's 2000 novel. Music by Mychael Danna and Jeff Danna. Animation directed at Cartoon Saloon's Kilkenny studio in the studio's house-style 2D approach. Academy Award nominee for Best Animated Feature 2018; Annie Award winner for Best Independent Animated Feature.",
    "critical_reception": "Major critical hit, particularly admired for its restraint with difficult material and for treating its young audience as capable of processing serious history.",
    "filmic_methods": [
        "2D animation alternating with stylised storybook insets",
        "warm earth-tone palette for Kabul; saturated jewel-tone palette for the storybook",
        "child-narrator voice-over threading the storybook",
        "long static frames that hold daily-life observation",
        "tracking shots through Kabul streets that index spatial geography",
        "music that shifts register between realist and mythic registers"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening market-stall storybook sequence",
        "the storybook frame-tale insets across the film",
        "the Pul-e-Charkhi prison-visit sequence",
        "the disguise-haircut transformation scene",
        "the closing reunion sequence"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

JOJO_RABBIT_BRIEF = {
    "title": "Jojo Rabbit (2019)",
    "synopsis": "A ten-year-old Hitler Youth recruit in late-war Germany discovers his mother is hiding a Jewish girl in their attic, and his imaginary friend — a buffoonish Adolf Hitler — works to keep him in line. Taika Waititi's anti-hate satire, adapted from Christine Leunens' novel Caging Skies.",
    "director_year_country": "Taika Waititi — 2019 — USA / New Zealand / Czech Republic",
    "major_characters": [
        "Johannes 'Jojo' Betzler — the ten-year-old protagonist (Roman Griffin Davis)",
        "Rosie Betzler — Jojo's mother (Scarlett Johansson)",
        "Elsa Korr — the young Jewish woman in hiding (Thomasin McKenzie)",
        "Captain Klenzendorf — the demoted Hitler Youth officer (Sam Rockwell)",
        "Adolf — Jojo's imaginary-friend Hitler (Taika Waititi)",
        "Yorki — Jojo's best friend"
    ],
    "major_themes": [
        "indoctrination and the child's-eye-view of fascism",
        "comic distance as a strategy for handling historical horror",
        "imaginary friendship and the construction of belief",
        "the home as resistance space",
        "loss, complicity and moral awakening",
        "the satirical mode and its risks"
    ],
    "production_context": "Made by Defender Films, Piki Films and TSG Entertainment, distributed by Fox Searchlight Pictures. Director and screenwriter Taika Waititi (adapting Christine Leunens). Cinematographer Mihai Malaimare Jr. Editor Tom Eagles. Score by Michael Giacchino. Production design by Ra Vincent. Filmed in Prague and the Czech countryside. Made for around $14m. Six Academy Award nominations including Best Picture, Best Supporting Actress (Johansson) and Best Adapted Screenplay (Waititi won). Audience Award at the Toronto International Film Festival.",
    "critical_reception": "Critically polarising on release — reviewers split on whether the comic-distance strategy treats fascism with sufficient gravity. Subsequent appraisal has tended to defend the film's anti-hate stance while acknowledging its tonal tightrope.",
    "filmic_methods": [
        "saturated symmetrical Wes-Anderson-influenced compositions",
        "anachronistic music — David Bowie, the Beatles in German — across diegetic and non-diegetic registers",
        "child's-eye low-angle framing sustained through Jojo's perspective",
        "abrupt tonal cuts between comic and serious registers",
        "warm autumnal palette for the home scenes; muted greys for the war scenes",
        "the imaginary-Hitler scenes staged as if real, with editing that blurs the boundary"
    ],
    "key_scenes_for_micro_analysis": [
        "the imaginary-Hitler dance opening sequence",
        "the Hitler Youth camp opening scenes",
        "the attic-discovery moment",
        "the public-square hanging sequence midway",
        "the closing 'free at last' street-dance"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

TSOTSI_BRIEF = {
    "title": "Tsotsi (2005)",
    "synopsis": "A young gang leader in a Johannesburg township shoots a woman during a carjacking and discovers her baby on the back seat. Over a few days, caring for the child forces him to confront the life he has built. Gavin Hood's adaptation of Athol Fugard's novel.",
    "director_year_country": "Gavin Hood — 2005 — South Africa / United Kingdom",
    "major_characters": [
        "Tsotsi (David) — the young gang leader (Presley Chweneyagae)",
        "Miriam — the young mother forced to nurse the baby",
        "Aap — the gentle gang member",
        "Boston — the educated gang member",
        "Butcher — the violent gang member",
        "the baby — referred to only by Tsotsi's chosen name"
    ],
    "major_themes": [
        "post-apartheid masculinity and township violence",
        "the recovered child as moral pivot",
        "memory, trauma and absent parents",
        "wealth and segregation in modern Johannesburg",
        "naming and identity — 'Tsotsi' itself meaning 'thug'",
        "the redemption narrative under realist constraint"
    ],
    "production_context": "Made by Industrial Development Corporation of South Africa, the UK Film and TV Production Company and Tsotsi Films, distributed by Miramax Films. Director and screenwriter Gavin Hood. Cinematographer Lance Gewer. Editor Megan Gill. Score by Mark Kilian and Paul Hepker, featuring South African kwaito artist Zola and the voice of Vusi Mahlasela. Filmed on location in the Soweto township and central Johannesburg. Best Foreign Language Film at the 78th Academy Awards (2006) — the first South African film to win that category.",
    "critical_reception": "Major critical hit and a breakthrough for post-apartheid South African cinema. Subsequent debate has engaged with whether the film redeems its protagonist too quickly and with the tension between melodrama and social realism.",
    "filmic_methods": [
        "Johannesburg-township naturalism with hand-held camera",
        "low-key lighting in the township scenes; brighter coverage at Miriam's apartment",
        "kwaito-music score (Zola) layered against orchestral cues",
        "long takes that hold the protagonist's face in close-up",
        "the recurring train-line and shantytown geography that anchors space",
        "child-perspective inserts during the protagonist's flashbacks"
    ],
    "key_scenes_for_micro_analysis": [
        "the township-arrival opening on the train platform",
        "the carjacking sequence and the discovery of the baby",
        "the Miriam apartment-feeding sequence",
        "the protagonist's childhood-flashback under the concrete pipes",
        "the closing house-return confrontation"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

WAVE_BRIEF = {
    "title": "The Wave / Die Welle (2008)",
    "synopsis": "During a school project week on autocracy in modern Germany, a teacher runs an experiment with his class to demonstrate how fascism could happen here. The students embrace it. Dennis Gansel's adaptation, drawing on Ron Jones's 1967 'Third Wave' classroom experiment in California.",
    "director_year_country": "Dennis Gansel — 2008 — Germany",
    "major_characters": [
        "Rainer Wenger — the school teacher running the experiment (Jurgen Vogel)",
        "Tim — the lonely student who commits hardest (Frederick Lau)",
        "Marco — the popular boy whose girlfriend resists",
        "Karo — the student who pushes back against The Wave",
        "Dennis — the playwriting student",
        "Sinan — the Turkish-German student"
    ],
    "major_themes": [
        "the recurrence-question — could fascism happen here?",
        "conformity and the dynamics of group identity",
        "school as social laboratory",
        "uniformity as political instrument — the white shirts, the salute",
        "alienation and belonging in the modern teenager",
        "the teacher as charismatic leader"
    ],
    "production_context": "Made by Rat Pack Filmproduktion, Constantin Film and Medienfonds GFP, distributed by Constantin Film (Germany) and Momentum Pictures internationally. Director and co-writer Dennis Gansel; co-writer Peter Thorwarth. Based on Ron Jones's 1967 Cubberley High School experiment in Palo Alto and Todd Strasser's 1981 novelisation. Cinematographer Torsten Breuer. Editor Ueli Christen. Score by Heiko Maile (Camouflage). Made for around 4.5 million euros over a 38-day shoot. Released into German cinemas in March 2008; over 2.3 million domestic admissions in the first ten weeks.",
    "critical_reception": "Major German box-office success and widely used as a school-curriculum text. Subsequent debate has engaged with whether the film's compressed timeline lands as warning or as melodrama.",
    "filmic_methods": [
        "controlled school-room framing with locked-off coverage early",
        "gradual handheld escalation as the experiment intensifies",
        "white-shirt costume design as visual marker of in-group membership",
        "classical-cinema cuts during early classroom scenes; faster cutting later",
        "the rising-tide motif staged through pool and water imagery",
        "diegetic-only sound throughout the school sequences"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening lesson on autocracy",
        "the white-shirt uniform-adoption sequence",
        "the school playground 'wave' chant scene",
        "the late-night graffiti tagging sequence",
        "the closing assembly-hall reveal"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

WADJDA_BRIEF = {
    "title": "Wadjda (2012)",
    "synopsis": "A ten-year-old girl in Riyadh wants a green bicycle she sees in a shop and enters her school's Quran-recitation competition to win the prize money. Haifaa Al-Mansour's debut feature — the first feature film shot entirely in Saudi Arabia, the first by a Saudi female director.",
    "director_year_country": "Haifaa Al-Mansour — 2012 — Saudi Arabia / Germany",
    "major_characters": [
        "Wadjda — the ten-year-old protagonist (Waad Mohammed)",
        "Wadjda's mother — caught between work, marriage and motherhood",
        "Wadjda's father — peripheral figure considering a second wife",
        "Abdullah — Wadjda's neighbourhood friend who has a bicycle",
        "Ms. Hussa — the school principal"
    ],
    "major_themes": [
        "girlhood under restriction in 2010s Saudi Arabia",
        "the bicycle as symbol of agency",
        "motherhood and women's economic precariousness",
        "religious culture and individual desire",
        "national cinema emerging from a country with no previous feature-film industry",
        "the small-scale narrative as political document"
    ],
    "production_context": "Made by Razor Film Produktion (Germany) and Highlook Group (UAE / Saudi Arabia). Distributed internationally by Pictures in a Frame and Sony Pictures Classics in the US. Director and screenwriter Haifaa Al-Mansour. Cinematographer Lutz Reitemeier. Score by Max Richter. Made for around 3 million euros. Filmed in Riyadh — Al-Mansour reportedly directed many street scenes from inside a van, since at the time of production women were not permitted to direct men in public spaces in Saudi Arabia. The film helped catalyse the gradual loosening of restrictions on Saudi cinema (the country ended its commercial-cinema ban in 2018).",
    "critical_reception": "Major international critical hit; selected as Saudi Arabia's first-ever submission to the Best Foreign-Language Film Academy Award category. Widely studied for the bicycle as symbol and for its production-context story of the female director.",
    "filmic_methods": [
        "naturalistic lighting and observation — hand-held within a generally locked frame",
        "child's-eye low-angle shots through Wadjda's perspective",
        "long static takes that hold scenes of restriction",
        "Max Richter score used sparingly",
        "framing of female characters often through doorways and windows — visible enclosure",
        "the bicycle introduced visually before it is named"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening classroom recitation",
        "the toy-shop bicycle reveal",
        "the rooftop sequence with Wadjda and her mother",
        "the Quran-competition prize-announcement",
        "the closing street-traversal"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

GIRLHOOD_BRIEF = {
    "title": "Girlhood / Bande de filles (2014)",
    "synopsis": "A Black teenage girl in suburban Paris falls in with a friendship group of three other young women and renegotiates her identity. Celine Sciamma's third feature, on Black femininity and friendship in the Parisian banlieues.",
    "director_year_country": "Celine Sciamma — 2014 — France",
    "major_characters": [
        "Marieme / Vic — the protagonist (Karidja Toure)",
        "Lady, Adiatou, Fily — the three friends",
        "Marieme's older brother — a controlling presence",
        "Ismael — Marieme's love interest",
        "Marieme's younger sister"
    ],
    "major_themes": [
        "Black femininity on screen in French cinema",
        "girlhood and friendship as identity formation",
        "the suburban banlieue as social space",
        "music and dance as belonging",
        "constraints — domestic, economic, gendered",
        "subverting national-cinema stereotypes"
    ],
    "production_context": "Made by Hold Up Films (France) and Lilies Films, distributed internationally by Strand Releasing. Director and screenwriter Celine Sciamma (whose work traces the development of girls and young women — Water Lilies, Tomboy, Portrait of a Lady on Fire). Cinematographer Crystel Fournier. Editor Julien Lacheray. Score by Para One (Jean-Baptiste de Laubier). Made for around 4 million euros and shot in Paris suburbs. Screened in the Directors' Fortnight at Cannes 2014 and won the Carrosse d'Or.",
    "critical_reception": "Major critical hit on the international festival circuit; debate has continued over the cultural ethics of a white French director making a Black-led film, which is a useful classroom topic at GCSE level when handled carefully.",
    "filmic_methods": [
        "Cinemascope widescreen framing of the four friends as ensemble",
        "saturated colour blocks — pink, blue — used as identity statement",
        "long static takes that hold the friends in frame together",
        "needle-drop and original score (Para One) used in extended sequences",
        "the famous Rihanna 'Diamonds' karaoke scene as a single sustained set-piece",
        "the 'mall ambush' opening with high-key field lighting"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening American-football-game tracking shot",
        "the train-station fight",
        "the hotel-room karaoke 'Diamonds' set piece",
        "the boxing-fight in the second act",
        "the closing crossing-the-road sequence"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

FAREWELL_BRIEF = {
    "title": "The Farewell (2019)",
    "synopsis": "A Chinese-American family discovers that their grandmother has terminal cancer, but, following Chinese custom, they choose not to tell her. They stage a wedding to bring everyone together for what may be a last visit. Lulu Wang's autobiographical second feature, with the on-screen tag 'Based on an actual lie'.",
    "director_year_country": "Lulu Wang — 2019 — USA / China",
    "major_characters": [
        "Billi — the New York-based protagonist (Awkwafina)",
        "Nai Nai — the grandmother (Zhao Shuzhen)",
        "Haiyan — Billi's father",
        "Lu Jian — Billi's mother",
        "Hao Hao — Billi's cousin, the groom",
        "Aiko — Hao Hao's Japanese fiancee"
    ],
    "major_themes": [
        "diasporic Chinese-American identity",
        "the cultural ethics of the withheld diagnosis",
        "family ritual as collective lie",
        "grief expressed through indirection",
        "the wedding as social-stage and emotional cover",
        "language, translation and what cannot be said"
    ],
    "production_context": "Made by Big Beach, Depth of Field, Kindred Spirit and Ray Productions, distributed by A24 (US) and Entertainment One (international). Director and screenwriter Lulu Wang, expanding her 2016 This American Life episode 'In Defense of Ignorance'. Cinematographer Anna Franquesa Solano. Editor Matthew Friedman and Michael Taylor. Score by Alex Weston. Made for around $3m and shot largely in Changchun, China. Premiered at Sundance 2019; Independent Spirit Award for Best Feature; Golden Globe Best Actress for Awkwafina.",
    "critical_reception": "Major critical and audience hit; A24 backed the release as a specialty crossover. Subsequent reception has folded the film into wider conversations about Asian-American representation and the hyphenated experience.",
    "filmic_methods": [
        "long static takes and centred frames",
        "warm interior light at Nai Nai's apartment; cooler exteriors elsewhere",
        "restrained Alex Weston score, used sparingly",
        "wide ensemble framing during family meals",
        "a single sustained slow-motion family-walk",
        "language-shift cuts between Mandarin and English dialogue"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening Billi-and-Nai-Nai phone call",
        "the airport-arrival and family-greeting sequence",
        "the wedding-banquet hall set piece",
        "the hospital scan-results sequence",
        "the closing slow-motion street-walk"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

SUBMARINE_BRIEF = {
    "title": "Submarine (2010)",
    "synopsis": "A precocious fifteen-year-old boy in Swansea narrates his attempts to lose his virginity to his classmate Jordana and to stop his mother from leaving his father. Richard Ayoade's debut feature, adapted from Joe Dunthorne's novel.",
    "director_year_country": "Richard Ayoade — 2010 — United Kingdom / United States",
    "major_characters": [
        "Oliver Tate — the fifteen-year-old protagonist (Craig Roberts)",
        "Jordana Bevan — Oliver's classmate (Yasmin Paige)",
        "Lloyd Tate — Oliver's depressed father (Noah Taylor)",
        "Jill Tate — Oliver's mother (Sally Hawkins)",
        "Graham Purvis — the New Age neighbour (Paddy Considine)"
    ],
    "major_themes": [
        "adolescent imagination and the unreliable narrator",
        "first love and the staged romantic gesture",
        "the depressed parent and household tension",
        "Welsh provincial setting as place and as joke",
        "indie aesthetic as register for self-conscious teenage interiority",
        "the literary novella tradition translated to screen"
    ],
    "production_context": "Made by Warp Films and Film4, distributed by Optimum Releasing (UK) and The Weinstein Company (US). Director and screenwriter Richard Ayoade, adapting Joe Dunthorne's 2008 novel. Cinematographer Erik Wilson. Editor Chris Dickens and Nick Fenton. Original songs and incidental music by Alex Turner (Arctic Monkeys); orchestral score by Andrew Hewitt. Made for around $1.5m and shot in and around Swansea. Premiered at the Toronto International Film Festival 2010; cult-favourite indie debut.",
    "critical_reception": "Major critical hit on the indie-circuit, particularly admired for its directorial precision and its Wes-Anderson-adjacent visual register. Subsequent reception has consolidated it as a landmark British indie debut of the early 2010s.",
    "filmic_methods": [
        "saturated 1980s-throwback colour palette — yellows, mustards, mid-blues",
        "Wes-Anderson-influenced symmetrical framing and iris transitions",
        "Alex Turner needle-drop original songs across the narrative montages",
        "voice-over from the protagonist threading the film",
        "Super-8-style inserts as memory/imagination cues",
        "mannered theatrical dialogue within naturalistic locations"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening credit-sequence beach montage",
        "the bullying-of-Zoe playground scene",
        "the candlelit-dinner sequence with Jordana",
        "the cliff-side argument with the mother",
        "the closing return-to-the-beach sequence"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

ATTACK_BLOCK_BRIEF = {
    "title": "Attack the Block (2011)",
    "synopsis": "A teenage gang on a South London council estate mug a young woman on Bonfire Night, only for the night to be interrupted by an alien invasion landing on their block. They become its unlikely defenders. Joe Cornish's debut feature.",
    "director_year_country": "Joe Cornish — 2011 — United Kingdom",
    "major_characters": [
        "Moses — the gang leader (John Boyega, in his feature-film debut)",
        "Sam — the young nurse the gang mug (Jodie Whittaker)",
        "Pest, Dennis, Jerome, Biggz — Moses's gang",
        "Hi-Hatz — the local drug dealer",
        "Brewis — the middle-class accidental ally (Luke Treadaway)",
        "Ron — the second-floor weed-dealer (Nick Frost)"
    ],
    "major_themes": [
        "the South London council block as social and geographic world",
        "moral arc — from mugger to defender",
        "youth-and-authority — police, dealers, residents",
        "genre-mixing as British urban science fiction",
        "estate solidarity and class",
        "the alien as defamiliarising lens on familiar space"
    ],
    "production_context": "Made by Big Talk Productions and Film4, distributed by Optimum Releasing (UK) and Sony Pictures Classics (US). Director and screenwriter Joe Cornish (his feature debut). Cinematographer Tom Townend. Editor Jonathan Amos. Score by Steven Price and Basement Jaxx. Made for around 8 million pounds and shot largely on the Heygate Estate in Elephant and Castle. Premiered at SXSW 2011 to strong reviews; cult success on home formats.",
    "critical_reception": "Major critical hit on the festival circuit and a launching pad for John Boyega. Subsequent reassessment has read the film through the lens of urban gentrification and the demolition of the Heygate Estate after filming.",
    "filmic_methods": [
        "neon-lit South London nights — sodium yellows, fluorescent greens",
        "hand-held council-block geography that maps stairs, lifts and corridors",
        "John Carpenter-influenced synth-and-percussion score (Steven Price / Basement Jaxx)",
        "long lens compression on aliens against block walkways",
        "diegetic-music intercutting (grime, dancehall) with the score",
        "the firework-night opening as visual establishment of the world"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening firework-night street confrontation",
        "the first alien-encounter on the bin-cupboards",
        "the corridor-stalking sequence with the larger creatures",
        "the swimming-pool flat sequence",
        "the closing block-defence finale"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

SKYFALL_BRIEF = {
    "title": "Skyfall (2012)",
    "synopsis": "James Bond's loyalty to M is tested when her past comes back to haunt them. Sam Mendes's third Bond entry — the franchise's twenty-third film, marking its fiftieth anniversary — and the first directed by an Oscar-winning auteur.",
    "director_year_country": "Sam Mendes — 2012 — United Kingdom / United States",
    "major_characters": [
        "James Bond — 007 (Daniel Craig)",
        "M — head of MI6 (Judi Dench)",
        "Raoul Silva — the antagonist, ex-MI6 (Javier Bardem)",
        "Eve Moneypenny — the field officer (Naomie Harris)",
        "Q — the new quartermaster (Ben Whishaw)",
        "Mallory — the new M (Ralph Fiennes)"
    ],
    "major_themes": [
        "the spy-hero approaching obsolescence",
        "loyalty, betrayal and the surrogate mother",
        "Britain on the world stage — the Whitehall setting",
        "the franchise reflecting on its own past",
        "spectacle as story-telling instrument",
        "auteur cinematographer applied to blockbuster form"
    ],
    "production_context": "Made by Eon Productions, MGM and Columbia Pictures, distributed by Columbia (US) and Sony Pictures (international). Director Sam Mendes. Screenplay Neal Purvis, Robert Wade and John Logan. Cinematographer Roger Deakins (the franchise's first Oscar-nominated cinematographer of the modern run). Editor Stuart Baird and Kate Baird. Score by Thomas Newman. Title song co-written and performed by Adele. Made for around $200m. Grossed over $1.1bn worldwide — the highest-grossing Bond film at the time of its release. Five Academy Award nominations including Best Cinematography, with wins for Best Sound Editing and Best Original Song.",
    "critical_reception": "Major critical and commercial success, widely cited as the strongest Daniel Craig entry. Subsequent appraisal has noted its careful balance between modern blockbuster spectacle and Bond-franchise iconography.",
    "filmic_methods": [
        "Roger Deakins's silhouette-and-skyline framing — Shanghai, Macau, Highlands",
        "high-contrast neon palettes (Shanghai-tower, Macau casino) versus desaturated Highlands",
        "long-lens telephoto for the rooftop motorbike chase",
        "Adele theme-song foreshadowing across the score",
        "static wide compositions of M's offices versus handheld during action",
        "the climactic chapel-and-house sequence using practical fire"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening Istanbul motorbike-rooftop chase",
        "the Shanghai-tower silhouette assassination sequence",
        "the Macau-casino lizard-pit confrontation",
        "the Whitehall public-inquiry attack mid-act",
        "the closing Skyfall-house chapel finale"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

BLINDED_LIGHT_BRIEF = {
    "title": "Blinded by the Light (2019)",
    "synopsis": "A British-Pakistani teenager in 1987 Luton finds his life transformed when a friend lends him two Bruce Springsteen cassettes. Gurinder Chadha's musical-realist coming-of-age film, adapted from journalist Sarfraz Manzoor's 2007 memoir.",
    "director_year_country": "Gurinder Chadha — 2019 — United Kingdom / United States",
    "major_characters": [
        "Javed Khan — the protagonist (Viveik Kalra)",
        "Malik Khan — Javed's father (Kulvinder Ghir)",
        "Roops — the school friend who introduces Springsteen (Aaron Phagura)",
        "Eliza — Javed's girlfriend (Nell Williams)",
        "Matt — Javed's childhood friend",
        "Ms. Clay — Javed's English teacher (Hayley Atwell)"
    ],
    "major_themes": [
        "second-generation British-Asian identity in Thatcher-era England",
        "music as identity-forming text",
        "father-son intergenerational conflict",
        "racism on the streets of late-1980s Luton",
        "writing as means of escape and recognition",
        "the magical-realist musical and how lyrics overlay onto life"
    ],
    "production_context": "Made by Cornerstone Films, Bend It Films, Levantine Films and Ingenious Media, distributed by Warner Bros. (UK) and New Line Cinema (US). Director Gurinder Chadha. Screenplay Sarfraz Manzoor, Gurinder Chadha and Paul Mayeda Berges, adapting Manzoor's memoir Greetings from Bury Park. Cinematographer Ben Smithard (shot on Arri Alexa Mini at 2.8K). Editor Justin Krish. Score by A. R. Rahman; the Springsteen catalogue licensed for needle drops. Filmed primarily in Luton over six weeks in 2018. Premiered at Sundance 2019; Bruce Springsteen personally approved the licensing.",
    "critical_reception": "Critical and audience hit. Subsequent reception has read the film through the British-Asian musical tradition that Chadha helped establish (Bend It Like Beckham, Bhaji on the Beach).",
    "filmic_methods": [
        "Springsteen needle-drops across the narrative montages",
        "magical-realist lyric-text overlays appearing on walls and skies",
        "warm autumnal Luton palette in the home and high-street scenes",
        "extended musical set-pieces (the rooftop 'Born to Run' sequence)",
        "split-screen and superimposition during the music-listening discoveries",
        "Asian-British family-house mise-en-scene contrasted with the high-street public space"
    ],
    "key_scenes_for_micro_analysis": [
        "the cassette-and-Walkman first-listen sequence",
        "the rooftop 'Born to Run' lyric-overlay sequence",
        "the National Front street-confrontation scene",
        "the New Jersey poetry-class trip sequence",
        "the closing father-and-son speech-and-reconciliation"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

ROCKS_BRIEF = {
    "title": "Rocks (2019)",
    "synopsis": "A Black British teenage girl in Hackney, nicknamed Rocks, comes home to find her mother gone and a note saying she will not return for some time. With her younger brother Emmanuel to look after, she tries to keep the family together and out of social services. Sarah Gavron's collaborative ensemble film with a non-professional cast.",
    "director_year_country": "Sarah Gavron — 2019 — United Kingdom",
    "major_characters": [
        "Olushola 'Rocks' Omotoso — the protagonist (Bukky Bakray)",
        "Emmanuel — Rocks's younger brother (D'angelou Osei Kissiedu)",
        "Sumaya — Rocks's best friend (Kosar Ali)",
        "Roshe — a friend in the group (Shaneigha-Monik Greyson)",
        "Khadijah, Yawa, Sabina — the wider friendship circle"
    ],
    "major_themes": [
        "single-parenthood-by-default — children left to keep family running",
        "multicultural London teenage friendship",
        "social services as ambient threat",
        "estate-and-school as the texture of the everyday",
        "loss, abandonment and the steady response",
        "social-realist aesthetic with non-professional cast"
    ],
    "production_context": "Made by Fable Pictures, Film4 and the BFI, distributed by Altitude Film Distribution. Director Sarah Gavron. Screenplay Theresa Ikoko and Claire Wilson, developed in workshops with the cast. Cinematographer Helene Louvart. Editor Maya Maffioli. Score by Emilie Levienaise-Farrouch. Crew approximately 75% women. Filmed in Hackney, Hoxton, Shoreditch and Dalston with a cast almost entirely of non-professional teenagers cast from local schools. Seven BAFTA nominations including Outstanding British Film and Best Actress (Bakray); Bukky Bakray won the BAFTA Rising Star Award.",
    "critical_reception": "Major critical hit; widely admired as a contemporary social-realist achievement that puts a multicultural London adolescence on screen with naturalism and warmth.",
    "filmic_methods": [
        "naturalistic available light and Helene Louvart's hand-held coverage",
        "real London exteriors — bus stops, school corridors, Hackney streets",
        "non-professional teenage cast with workshop-developed dialogue",
        "ensemble framings that hold the friendship group together",
        "minimal score, used sparingly",
        "documentary-adjacent textures — phone-camera inserts, raw audio"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening rooftop friendship-group sequence",
        "the school-corridor improvisation scene",
        "the supermarket-shoplifting moment",
        "the seaside daytrip set-piece",
        "the closing reunion scene"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

HURT_LOCKER_BRIEF = {
    "title": "The Hurt Locker (2008)",
    "synopsis": "An American Explosive Ordnance Disposal team in Iraq faces the daily work of disarming bombs in Baghdad. Kathryn Bigelow's Iraq-war thriller and a foundational text of the issue-led contemporary indie war film.",
    "director_year_country": "Kathryn Bigelow — 2008 — USA",
    "major_characters": [
        "Sergeant William James — the new EOD team leader (Jeremy Renner)",
        "Sergeant J. T. Sanborn — the team's second-in-command",
        "Specialist Owen Eldridge — the youngest team member",
        "Colonel John Cambridge — the unit's commander"
    ],
    "major_themes": [
        "war as work — the EOD specialist's daily labour",
        "addiction to risk — the title's metaphor",
        "the Iraq War as recent history",
        "masculinity and combat",
        "the contractor/soldier moral frame",
        "issue-led indie cinema as political intervention"
    ],
    "production_context": "Made by Voltage Pictures, Grosvenor Park Media and Film Capital Europe Funds, distributed by Summit Entertainment. Director Kathryn Bigelow (the first woman to win Best Director at the Academy Awards for this film). Screenwriter Mark Boal (a war-correspondent journalist whose embedded reporting informed the script). Cinematographer Barry Ackroyd (a Ken Loach regular). Editors Bob Murawski and Chris Innis. Made for around $15m, mostly shot on 16mm in Jordan with handheld cameras. Six Academy Awards including Best Picture, Best Director and Best Original Screenplay.",
    "critical_reception": "Major critical hit; modest theatrical performance amplified by awards. Subsequent debate has continued over its political stance — does the film critique or aestheticise the Iraq invasion? The film won Best Picture against Avatar, a fact often noted in contemporary coverage.",
    "filmic_methods": [
        "handheld 16mm cinematography across all locations",
        "long lenses for spectator-distance during bomb-disposal sequences",
        "diegetic-only ambient sound — sparse non-diegetic score",
        "extreme telephoto coverage of urban watchers",
        "rapid in-camera focus pulls during tension sequences",
        "extended real-time bomb-disposal sequences with minimal cutting"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening pre-credits bomb-disposal that introduces the team's first leader",
        "the desert-sniper duel mid-act",
        "the supermarket-aisle cereal-choice cutaway in the closing act",
        "the climactic city-square car-bomb sequence",
        "the closing return-to-Iraq tarmac shot"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

HATE_U_GIVE_BRIEF = {
    "title": "The Hate U Give (2018)",
    "synopsis": "A Black teenager from a poor neighbourhood attends an affluent suburban school and witnesses the police shooting of a childhood friend. George Tillman Jr.'s adaptation of Angie Thomas's YA novel, a foundational Black-Lives-Matter-era youth indie.",
    "director_year_country": "George Tillman Jr. — 2018 — USA",
    "major_characters": [
        "Starr Carter — the protagonist (Amandla Stenberg)",
        "Khalil — Starr's childhood friend",
        "Maverick 'Mav' Carter — Starr's father",
        "Lisa Carter — Starr's mother",
        "Chris — Starr's white boyfriend",
        "King — the local gang leader",
        "April Ofrah — the lawyer"
    ],
    "major_themes": [
        "police violence and Black Lives Matter context",
        "code-switching between two communities — Garden Heights and Williamson Prep",
        "voice and silence — when to speak, what speaking costs",
        "family as moral frame",
        "youth activism",
        "issue-led indie cinema in the late 2010s"
    ],
    "production_context": "Made by Fox 2000 Pictures, State Street Pictures and Temple Hill Entertainment, distributed by 20th Century Fox. Director George Tillman Jr. (Soul Food, Notorious). Adapted from Angie Thomas's bestselling 2017 YA novel. Cinematographer Mihai Malaimare Jr. Editors Alex Blatt and Craig Hayes. Made for around $23m and grossed over $34m. Released into a 2018 culture moment when Black Lives Matter as a movement and as a publishing-and-film category was at its broadest reach. The film is studied in the indie unit although it had wide-release distribution because its thematic material aligns with issue-led indie sensibility.",
    "critical_reception": "Major critical and audience response, particularly among student readers of Thomas's novel. NAACP Image Award winner. Subsequent reassessment focuses on the film's deliberate accessibility — its YA register meant it reached audiences that more challenging Black-cinema entries could not.",
    "filmic_methods": [
        "naturalistic mid-shot coverage of family scenes",
        "warm, saturated palette in Garden Heights; cooler greys at Williamson Prep",
        "handheld camera during the police-shooting sequence and its aftermath",
        "non-diegetic score by Dustin O'Halloran with a Black-music needle-drop overlay",
        "voice-over by Starr threading first-person reflection",
        "code-switching dramatised through framing — closer in family scenes, wider at school"
    ],
    "key_scenes_for_micro_analysis": [
        "the opening 'the talk' father-children kitchen-table scene",
        "the traffic-stop police-shooting sequence",
        "the protest-and-tear-gas mid-act sequence",
        "the kitchen confrontation with King in the third act",
        "the closing house-fire and recovery sequence"
    ],
    "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred"
}

# ============================================================ Batch metadata

GLOBAL_ENGLISH_UNIT = {
    "name": "Global English-language Films",
    "slug": "global-english-language-films",
    "subtitle": "Slumdog Millionaire, District 9, The Babadook, The Breadwinner, Jojo Rabbit — narrative analysis.",
    "accent": "#2563eb",
    "accent_light": "#eff6ff",
    "accent_badge": "#3b82f633",
    "body_class": "unit-film-studies-eduqas-6",
    "lesson_count": 5
}

GLOBAL_NON_ENGLISH_UNIT = {
    "name": "Global Non-English-Language Films",
    "slug": "global-non-english-language-films",
    "subtitle": "Tsotsi, The Wave, Wadjda, Girlhood, The Farewell — representation analysis.",
    "accent": "#0e7490",
    "accent_light": "#ecfeff",
    "accent_badge": "#06b6d433",
    "body_class": "unit-film-studies-eduqas-7",
    "lesson_count": 5
}

CONTEMPORARY_UK_UNIT = {
    "name": "Contemporary UK Films",
    "slug": "contemporary-uk-films",
    "subtitle": "Submarine, Attack the Block, Skyfall, Blinded by the Light, Rocks — aesthetic analysis.",
    "accent": "#be185d",
    "accent_light": "#fdf2f8",
    "accent_badge": "#ec489933",
    "body_class": "unit-film-studies-eduqas-8",
    "lesson_count": 5
}

US_INDEPENDENT_UNIT = {
    "name": "US Independent Film and Specialist Writing",
    "slug": "us-independent",
    "subtitle": "Five contemporary US indies and the specialist film writing that helps unlock their meaning.",
    "accent": "#b45309",
    "accent_light": "#fffbeb",
    "accent_badge": "#d97706",
    "body_class": "unit-film-studies-eduqas-3",
    "lesson_count": 7
}


def make_batch(batch_id, unit, set_films_covered, lessons, unit_focus, what_remember, common_misc):
    return {
        "batch_id": batch_id,
        "subject": {
            "name": "Film Studies",
            "slug": "film-studies-eduqas",
            "exam_board": "Eduqas",
            "target_audience": "free-tier"
        },
        "unit": unit,
        "spec_slice_path": "scripts/_content_film-studies-eduqas/_spec_set-films.txt",
        "reference_lesson_path": "scripts/_content_film-studies-eduqas/_reference_lesson.json",
        "subject_level_teaching_brief": SHARED_BRIEF,
        "unit_level_teaching_brief": {
            "set_films_covered": set_films_covered,
            "what_students_should_remember": what_remember,
            "common_misconceptions_for_unit": common_misc,
            "unit_focus": unit_focus,
        },
        "quote_ticker_html_for_unit": SHARED_QUOTE_HTML,
        "registered_question_type_names": REGISTERED_TYPES,
        "allowed_question_types_for_this_unit": ALLOWED_TYPES,
        "lessons_in_batch": lessons,
        "output_dir": "scripts/_content_film-studies-eduqas/lessons"
    }


# ============================================================ Lesson lists

NARRATIVE_QTYPES = [
    "1 mark — Identify",
    "2 marks — Define",
    "5 marks — Explain Effect",
    "10 marks — Micro-Analysis",
    "25 marks — Extended Essay"
]
REPRESENTATION_QTYPES = [
    "1 mark — Identify",
    "2 marks — Define",
    "5 marks — Explain Effect",
    "10 marks — Micro-Analysis",
    "25 marks — Extended Essay"
]
AESTHETIC_QTYPES = [
    "1 mark — Identify",
    "2 marks — Define",
    "5 marks — Explain Effect",
    "10 marks — Micro-Analysis",
    "25 marks — Extended Essay"
]
INDIE_QTYPES = [
    "1 mark — Identify",
    "2 marks — Define",
    "5 marks — Explain Effect",
    "10 marks — Micro-Analysis",
    "15 marks — Compare and Contrast",
    "25 marks — Extended Essay"
]


GLOBAL_ENGLISH_LESSONS = [
    {
        "number": 1,
        "title": "Slumdog Millionaire: Narrative and Mumbai",
        "slug": "slumdog-millionaire-narrative-and-mumbai",
        "description": "Boyle's quiz-show frame, dual timelines and Mumbai mise-en-scene as narrative engine.",
        "spec_references": ["2.2 Section A: Global English language film – focus on narrative", "Set film option: Slumdog Millionaire (2008)"],
        "section_markers": [
            "Danny Boyle", "Loveleen Tandan", "Anthony Dod Mantle", "A. R. Rahman", "frame narrative",
            "dual timeline", "non-linear time", "withholding information", "Mumbai setting",
            "saturated colour palette", "Bollywood coda", "social mobility narrative", "production context"
        ],
        "suggested_question_types": NARRATIVE_QTYPES
    },
    {
        "number": 2,
        "title": "District 9: Narrative and Segregation Allegory",
        "slug": "district-9-narrative-and-segregation-allegory",
        "description": "Blomkamp's mockumentary-into-narrative shift and the apartheid allegory inside a science fiction frame.",
        "spec_references": ["2.2 Section A: Global English language film – focus on narrative", "Set film option: District 9 (2009)"],
        "section_markers": [
            "Neill Blomkamp", "Trent Opaloch", "Clinton Shorter", "Peter Jackson",
            "mockumentary", "narrative shift", "interview frame", "found-footage texture",
            "Johannesburg setting", "apartheid allegory", "the Other", "transformation narrative",
            "Wikus van de Merwe", "Christopher Johnson", "production context"
        ],
        "suggested_question_types": NARRATIVE_QTYPES
    },
    {
        "number": 3,
        "title": "The Babadook: Narrative and Grief as Monster",
        "slug": "the-babadook-narrative-and-grief-as-monster",
        "description": "Kent's domestic horror narrative and how the monster works as a bereavement metaphor.",
        "spec_references": ["2.2 Section A: Global English language film – focus on narrative", "Set film option: The Babadook (2014)"],
        "section_markers": [
            "Jennifer Kent", "Radek Ladczuk", "Jed Kurzel", "Essie Davis", "domestic horror",
            "psychological narrative", "horror narrative", "the storybook frame",
            "single-mother protagonist", "grief metaphor", "low-key palette",
            "claustrophobic framing", "Kickstarter production", "Adelaide shoot", "production context"
        ],
        "suggested_question_types": NARRATIVE_QTYPES
    },
    {
        "number": 4,
        "title": "The Breadwinner: Narrative and Animation Under Occupation",
        "slug": "the-breadwinner-narrative-and-animation-under-occupation",
        "description": "Twomey's frame-tale animation and the storybook insets that carry the film's interior narrative.",
        "spec_references": ["2.2 Section A: Global English language film – focus on narrative", "Set film option: The Breadwinner (2017)"],
        "section_markers": [
            "Nora Twomey", "Cartoon Saloon", "Angelina Jolie", "Mychael Danna", "Jeff Danna",
            "animation narrative", "frame-tale structure", "storybook insets",
            "child-narrator voice-over", "Kabul setting", "Taliban context",
            "disguise narrative", "girlhood under occupation", "production context"
        ],
        "suggested_question_types": NARRATIVE_QTYPES
    },
    {
        "number": 5,
        "title": "Jojo Rabbit: Narrative and Comic Distance",
        "slug": "jojo-rabbit-narrative-and-comic-distance",
        "description": "Waititi's child-narrator satire and the comic-distance strategies that make the historical setting bearable.",
        "spec_references": ["2.2 Section A: Global English language film – focus on narrative", "Set film option: Jojo Rabbit (2019)"],
        "section_markers": [
            "Taika Waititi", "Mihai Malaimare Jr", "Michael Giacchino", "Caging Skies",
            "satirical narrative", "comic distance", "imaginary friend",
            "child-perspective narrative", "Wes-Anderson influence", "anachronistic music",
            "Hitler Youth setting", "moral awakening", "Best Adapted Screenplay", "production context"
        ],
        "suggested_question_types": NARRATIVE_QTYPES
    }
]

GLOBAL_NON_ENGLISH_LESSONS = [
    {
        "number": 1,
        "title": "Tsotsi: Representation and Johannesburg",
        "slug": "tsotsi-representation-and-johannesburg",
        "description": "Hood's Johannesburg slum naturalism and the representation of post-apartheid masculinity.",
        "spec_references": ["2.2 Section B: Global non-English language film – focus on representation", "Set film option: Tsotsi (2005)"],
        "section_markers": [
            "Gavin Hood", "Lance Gewer", "Mark Kilian", "Paul Hepker", "Vusi Mahlasela",
            "Athol Fugard", "Soweto setting", "post-apartheid representation",
            "township masculinity", "kwaito score", "low-key lighting",
            "redemption narrative", "Best Foreign Language Film", "production context"
        ],
        "suggested_question_types": REPRESENTATION_QTYPES
    },
    {
        "number": 2,
        "title": "The Wave: Representation and Conformity",
        "slug": "the-wave-representation-and-conformity",
        "description": "Gansel's classroom-set thriller and how representation builds a portrait of conformity.",
        "spec_references": ["2.2 Section B: Global non-English language film – focus on representation", "Set film option: The Wave / Die Welle (2008)"],
        "section_markers": [
            "Dennis Gansel", "Torsten Breuer", "Heiko Maile", "Camouflage band",
            "Ron Jones experiment", "Todd Strasser", "Third Wave",
            "representation of youth", "conformity", "uniformity", "white-shirt costume",
            "school as social laboratory", "fascism warning narrative", "production context"
        ],
        "suggested_question_types": REPRESENTATION_QTYPES
    },
    {
        "number": 3,
        "title": "Wadjda: Representation and Saudi Girlhood",
        "slug": "wadjda-representation-and-saudi-girlhood",
        "description": "Al-Mansour's Riyadh-set debut and the representation of girlhood under restriction.",
        "spec_references": ["2.2 Section B: Global non-English language film – focus on representation", "Set film option: Wadjda (2012)"],
        "section_markers": [
            "Haifaa Al-Mansour", "Lutz Reitemeier", "Max Richter", "Razor Film",
            "Riyadh setting", "representation of gender", "Saudi cinema",
            "the bicycle as symbol", "child's-eye-view", "doorway-and-window framing",
            "Quran competition", "first Saudi feature", "production context"
        ],
        "suggested_question_types": REPRESENTATION_QTYPES
    },
    {
        "number": 4,
        "title": "Girlhood: Representation and the Paris Banlieue",
        "slug": "girlhood-representation-and-paris-banlieue",
        "description": "Sciamma's Cinemascope ensemble and the representation of Black femininity in suburban Paris.",
        "spec_references": ["2.2 Section B: Global non-English language film – focus on representation", "Set film option: Girlhood / Bande de filles (2014)"],
        "section_markers": [
            "Celine Sciamma", "Crystel Fournier", "Para One", "banlieue setting",
            "representation of Black femininity", "ensemble friendship",
            "Cinemascope framing", "saturated colour blocks", "the gaze",
            "Diamonds karaoke set piece", "Cannes Directors' Fortnight", "production context"
        ],
        "suggested_question_types": REPRESENTATION_QTYPES
    },
    {
        "number": 5,
        "title": "The Farewell: Representation and Diaspora Grief",
        "slug": "the-farewell-representation-and-diaspora-grief",
        "description": "Wang's static-take family film and the representation of diasporic Chinese-American grief.",
        "spec_references": ["2.2 Section B: Global non-English language film – focus on representation", "Set film option: The Farewell (2019)"],
        "section_markers": [
            "Lulu Wang", "Anna Franquesa Solano", "Alex Weston", "A24",
            "Awkwafina", "diasporic identity", "Chinese-American representation",
            "withheld diagnosis", "the wedding-as-cover", "static long takes",
            "language-shift cuts", "Changchun shoot", "production context"
        ],
        "suggested_question_types": REPRESENTATION_QTYPES
    }
]

CONTEMPORARY_UK_LESSONS = [
    {
        "number": 1,
        "title": "Submarine: Aesthetic and Adolescent Imagination",
        "slug": "submarine-aesthetic-and-adolescent-imagination",
        "description": "Ayoade's saturated 1980s-throwback look and the indie-aesthetic register of adolescent imagination.",
        "spec_references": ["2.2 Section C: Contemporary UK film – focus on aesthetic qualities of film", "Set film option: Submarine (2010)"],
        "section_markers": [
            "Richard Ayoade", "Erik Wilson", "Alex Turner", "Andrew Hewitt",
            "Warp Films", "indie aesthetic", "Wes Anderson influence",
            "saturated palette", "voice-over narration", "Super-8 inserts",
            "Swansea setting", "iris transitions", "Joe Dunthorne novel", "production context"
        ],
        "suggested_question_types": AESTHETIC_QTYPES
    },
    {
        "number": 2,
        "title": "Attack the Block: Aesthetic and Genre Mixing",
        "slug": "attack-the-block-aesthetic-and-genre-mixing",
        "description": "Cornish's neon-lit South London nights and the genre-mixing aesthetic of urban science fiction.",
        "spec_references": ["2.2 Section C: Contemporary UK film – focus on aesthetic qualities of film", "Set film option: Attack the Block (2011)"],
        "section_markers": [
            "Joe Cornish", "Tom Townend", "Steven Price", "Basement Jaxx",
            "Heygate Estate", "John Carpenter influence", "neon palette",
            "council-block geography", "long-lens compression", "John Boyega",
            "genre-mixing aesthetic", "urban science fiction", "production context"
        ],
        "suggested_question_types": AESTHETIC_QTYPES
    },
    {
        "number": 3,
        "title": "Skyfall: Aesthetic and Bond Cinematography",
        "slug": "skyfall-aesthetic-and-bond-cinematography",
        "description": "Mendes and Roger Deakins's silhouette-and-skyline blockbuster look applied to the Bond franchise.",
        "spec_references": ["2.2 Section C: Contemporary UK film – focus on aesthetic qualities of film", "Set film option: Skyfall (2012)"],
        "section_markers": [
            "Sam Mendes", "Roger Deakins", "Thomas Newman", "Adele",
            "Daniel Craig", "blockbuster aesthetic", "silhouette framing",
            "Shanghai-tower set piece", "Macau casino sequence", "Highlands palette",
            "auteur cinematographer", "Eon Productions", "production context"
        ],
        "suggested_question_types": AESTHETIC_QTYPES
    },
    {
        "number": 4,
        "title": "Blinded by the Light: Aesthetic and Musical Realism",
        "slug": "blinded-by-the-light-aesthetic-and-musical-realism",
        "description": "Chadha's Springsteen needle-drops and the magical-realist text-overlay sequences that build a musical-realist look.",
        "spec_references": ["2.2 Section C: Contemporary UK film – focus on aesthetic qualities of film", "Set film option: Blinded by the Light (2019)"],
        "section_markers": [
            "Gurinder Chadha", "Ben Smithard", "A. R. Rahman", "Sarfraz Manzoor",
            "Bruce Springsteen", "Luton 1987 setting", "musical-realist aesthetic",
            "lyric-text overlay", "needle-drop set pieces", "warm autumnal palette",
            "British-Asian cinema", "production context"
        ],
        "suggested_question_types": AESTHETIC_QTYPES
    },
    {
        "number": 5,
        "title": "Rocks: Aesthetic and Multicultural London",
        "slug": "rocks-aesthetic-and-multicultural-london",
        "description": "Gavron's hand-held London naturalism and the social-realist aesthetic of a multicultural teenage cast.",
        "spec_references": ["2.2 Section C: Contemporary UK film – focus on aesthetic qualities of film", "Set film option: Rocks (2019)"],
        "section_markers": [
            "Sarah Gavron", "Helene Louvart", "Theresa Ikoko", "Claire Wilson",
            "Bukky Bakray", "Kosar Ali", "social-realist aesthetic",
            "non-professional cast", "Hackney setting", "Hoxton", "Dalston",
            "available-light naturalism", "ensemble framing", "BAFTA Rising Star", "production context"
        ],
        "suggested_question_types": AESTHETIC_QTYPES
    }
]

INDIE_SPLIT_LESSONS = [
    {
        "number": 5,
        "title": "The Hurt Locker: Bigelow's Iraq Thriller",
        "slug": "the-hurt-locker-and-the-hate-u-give-issue-led-indies",
        "description": "Bigelow's Iraq-war thriller as the foundational issue-led indie of the late 2000s — handheld 16mm, real-time bomb-disposal sequences, ambition as addiction.",
        "spec_references": ["2.1 US independent film option: The Hurt Locker (2008)"],
        "section_markers": [
            "Kathryn Bigelow", "Mark Boal", "Barry Ackroyd", "Iraq War",
            "EOD specialist", "handheld 16mm", "long lenses", "real-time tension",
            "Voltage Pictures", "Best Picture Academy Award", "first woman Best Director",
            "issue-led indie", "documentary realism aesthetic", "production context"
        ],
        "suggested_question_types": INDIE_QTYPES
    },
    {
        "number": 7,
        "title": "The Hate U Give: Issue-Led Indie",
        "slug": "the-hate-u-give-and-issue-led-indie",
        "description": "Tillman Jr.'s Black-Lives-Matter-era YA adaptation as the canonical late-2010s issue-led indie — code-switching, voice-over and family as moral frame.",
        "spec_references": ["2.1 US independent film option: The Hate U Give (2018)"],
        "section_markers": [
            "George Tillman Jr", "Mihai Malaimare Jr", "Dustin O'Halloran",
            "Angie Thomas novel", "Amandla Stenberg", "Black Lives Matter context",
            "code-switching", "Garden Heights", "Williamson Prep",
            "police-shooting sequence", "voice-over narration", "issue-led indie",
            "YA adaptation", "production context"
        ],
        "suggested_question_types": INDIE_QTYPES
    }
]

# ============================================================ Build batches

OUT_DIR = CONTENT_DIR

batches = [
    (
        "global-english_b1",
        GLOBAL_ENGLISH_UNIT,
        [SLUMDOG_BRIEF, DISTRICT_9_BRIEF, BABADOOK_BRIEF, BREADWINNER_BRIEF, JOJO_RABBIT_BRIEF],
        GLOBAL_ENGLISH_LESSONS,
        "Five lessons covering the five Global English-language set-film options. Each lesson takes the NARRATIVE focus area and applies it to one named film.",
        [
            "The five Global English-language set-film options are Slumdog Millionaire, District 9, The Babadook, The Breadwinner and Jojo Rabbit.",
            "Each lesson teaches narrative analysis: structure, time, perspective, frame, withholding-and-releasing, theory.",
            "Production context for each film anchors AO1 — director, country, year, principal cinematographer/composer where notable.",
            "Students choose ONE of the five options for the written paper but should know the others as comparison context."
        ],
        [
            "Students confuse narrative structure with plot summary — they retell the story rather than describing how the story is told.",
            "Students under-use the named theorists (Todorov, Bordwell) at the moment of analysis.",
            "Students over-rely on plot recall on what is fundamentally a narrative-analysis question."
        ]
    ),
    (
        "global-non-english_b1",
        GLOBAL_NON_ENGLISH_UNIT,
        [TSOTSI_BRIEF, WAVE_BRIEF, WADJDA_BRIEF, GIRLHOOD_BRIEF, FAREWELL_BRIEF],
        GLOBAL_NON_ENGLISH_LESSONS,
        "Five lessons covering the five Global Non-English-Language set-film options. Each lesson takes the REPRESENTATION focus area and applies it to one named film.",
        [
            "The five Global Non-English-Language set-film options are Tsotsi, The Wave, Wadjda, Girlhood and The Farewell.",
            "Each lesson teaches representation analysis: gender, ethnicity, age, culture, power and the gaze.",
            "Each option carries strong national-cinema specificity — South African, German, Saudi, French, Chinese-American — which is part of the analysis.",
            "Mulvey gaze theory at GCSE-appropriate framing is a useful but optional analytic lens."
        ],
        [
            "Students treat 'global non-English' as a single category rather than respecting the cultural specificity of each option.",
            "Students apply Mulvey's gaze theory schematically rather than to a specific moment of looking.",
            "Students confuse representation with plot — they describe what happens rather than how a group is constructed for the spectator."
        ]
    ),
    (
        "contemporary-uk_b1",
        CONTEMPORARY_UK_UNIT,
        [SUBMARINE_BRIEF, ATTACK_BLOCK_BRIEF, SKYFALL_BRIEF, BLINDED_LIGHT_BRIEF, ROCKS_BRIEF],
        CONTEMPORARY_UK_LESSONS,
        "Five lessons covering the five Contemporary UK set-film options. Each lesson takes the AESTHETIC focus area — distinctive 'look' and how it shapes meaning — and applies it to one named film.",
        [
            "The five Contemporary UK set-film options are Submarine, Attack the Block, Skyfall, Blinded by the Light and Rocks.",
            "Each lesson teaches aesthetic analysis: production design, colour, lighting, framing, music and how these build a distinctive look.",
            "Each option sits in a different industrial scale — micro-budget indie (Submarine), mid-budget studio indie (Attack the Block, Rocks), franchise blockbuster (Skyfall), specialty mid-budget (Blinded by the Light).",
            "The aesthetic question is also a question about TYPICALITY — what is typical or atypical of the film's style or genre."
        ],
        [
            "Students describe lighting and colour without articulating typicality of style — they say 'the lighting is dark' rather than 'this low-key palette is typical of social-realist British cinema'.",
            "Students treat the blockbuster aesthetic of Skyfall as if it requires no analysis because it is 'mainstream'.",
            "Students miss that aesthetic is institutional as well as artistic — different production scales produce different looks."
        ]
    ),
    (
        "indie-split_b1",
        US_INDEPENDENT_UNIT,
        [HURT_LOCKER_BRIEF, HATE_U_GIVE_BRIEF],
        INDIE_SPLIT_LESSONS,
        "Two lessons in the US Independent unit. Lesson 5 is the gap-fill rewrite of the existing combined Hurt Locker / Hate U Give lesson — single-film coverage of The Hurt Locker. Lesson 7 is a new single-film lesson on The Hate U Give. The existing combined slug at L5 is preserved so the row id is stable; the content_html is rewritten as Hurt-Locker-only.",
        [
            "The Hurt Locker (2008, dir. Bigelow) and The Hate U Give (2018, dir. Tillman Jr.) are studied as separate set-film options in the US independent unit.",
            "Both films are issue-led indies but from different historical moments — Iraq-War era and Black-Lives-Matter-era.",
            "Both films use voice-over and handheld camera but to different ends; this is fertile compare-and-contrast territory.",
            "AO2 is weighted higher than AO1 in the extended-writing question — analytical depth on micro-features matters more than plot recall."
        ],
        [
            "Students treat 'issue-led indie' as a stylistic label rather than an industrial-and-thematic category.",
            "Students assume Hate U Give is a Hollywood blockbuster because of its YA-novel source and wide release; the unit places it in the issue-led-indie category for its sensibility.",
            "Students compare the two films on plot rather than on specific filmic choices in named sequences."
        ]
    )
]

written = []
for batch_id, unit, films, lessons, focus, remember, misc in batches:
    payload = make_batch(batch_id, unit, films, lessons, focus, remember, misc)
    out = OUT_DIR / f"_batch_{batch_id}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    written.append(out.name)
    print(f"  wrote {out.name}  ({len(lessons)} lessons, {len(films)} film briefs)")

print(f"\n{len(written)} batch JSONs written to {OUT_DIR}")
