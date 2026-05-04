"""Build the 8 Phase-3 batch JSONs for Film Studies Eduqas / WJEC.

Reads the Phase 1 plan, slices the lessons into batches, and writes each batch
file with subject + unit metadata, the appropriate spec slice path, the
universal subject-level teaching brief (including the full film_content_rules
block), and per-unit teaching briefs (substantive for set-film units 2/3/4,
lighter for toolkit units 1/5).

Run from repo root:
  python scripts/_content_film-studies-eduqas/_build_batches.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "scripts" / "_plan_film-studies-eduqas.json"
OUT_DIR = ROOT / "scripts" / "_content_film-studies-eduqas"

REGISTERED_QUESTION_TYPE_NAMES = [
    "1 mark — Identify",
    "2 marks — Define",
    "5 marks — Explain Effect",
    "8 marks — Analyse Filmic Element",
    "10 marks — Micro-Analysis",
    "15 marks — Compare and Contrast",
    "25 marks — Extended Essay",
]

# All 7 types are valid in every unit. (Per unit, the agent prompt specifies
# which are most appropriate, but the validator allows any.)
ALLOWED_FOR_ALL_UNITS = list(REGISTERED_QUESTION_TYPE_NAMES)

QUOTE_TICKER_HTML = (
    "<blockquote>&ldquo;Cinema is a matter of what&rsquo;s in the frame and what&rsquo;s out.&rdquo; "
    "<cite>&mdash; Martin Scorsese</cite></blockquote>\n"
    "<blockquote>&ldquo;There is no terror in the bang, only in the anticipation of it.&rdquo; "
    "<cite>&mdash; Alfred Hitchcock</cite></blockquote>\n"
    "<blockquote>&ldquo;I never know what the next shot is going to be until the moment before I take it.&rdquo; "
    "<cite>&mdash; Akira Kurosawa</cite></blockquote>\n"
    "<blockquote>&ldquo;Films are made of three things: the script, the script and the script.&rdquo; "
    "<cite>&mdash; Greta Gerwig</cite></blockquote>\n"
    "<blockquote>&ldquo;The most honest form of filmmaking is to make a film for yourself.&rdquo; "
    "<cite>&mdash; Peter Jackson</cite></blockquote>\n"
    "<blockquote>&ldquo;Movies touch our hearts and awaken our vision.&rdquo; "
    "<cite>&mdash; Roger Ebert</cite></blockquote>"
)


# Per-set-film substantive briefs. Pulled from publicly verifiable production
# facts (BFI, Britannica, Wikipedia, IMDb level). NO copyrighted dialogue.
# Synopses are concept-only, no plot detail.
SET_FILM_BRIEFS: dict[str, dict] = {
    "dracula-1931": {
        "title": "Dracula (1931)",
        "synopsis": "Universal Pictures' adaptation of Bram Stoker's novel about an Eastern European vampire travelling to London. The studio horror cycle's foundation text and Bela Lugosi's defining role. A film of stillness, theatrical staging and expressionist shadow.",
        "director_year_country": "Tod Browning — 1931 — USA",
        "major_characters": [
            "Count Dracula — the vampire, a still and watchful aristocrat played by Bela Lugosi",
            "Renfield — solicitor turned servant, the human face of corruption",
            "Mina — fiancee of Harker, the figure the vampire pursues",
            "Van Helsing — Dutch professor, the rational counter-force",
            "Jonathan Harker — Mina's fiance, the audience surrogate",
            "Lucy — Mina's friend, an early victim",
        ],
        "major_themes": [
            "the foreign aristocrat as threat — anxieties about migration into 1930s America",
            "sexuality and seduction coded through the vampire",
            "rationality (Van Helsing) versus the supernatural (Dracula)",
            "boundary anxiety — the edges of empire, the female body, the home invaded",
            "death drawn out as theatrical spectacle",
            "the monster as outsider rather than as transgressive other",
        ],
        "production_context": "Made by Universal Pictures during the Great Depression as a studio gamble on horror as a saleable genre. Cinematographer Karl Freund (later director of The Mummy) brought Weimar German expressionism to Hollywood. Theatrical in pacing — adapted in part from the 1924 Hamilton Deane stage version. Shot on Universal's lot in studio sets only. Pre-Hays Code; though the film looks restrained, contemporary censors were uneasy. Audiences responded so strongly that Universal launched the studio horror cycle (Frankenstein, The Mummy, The Wolf Man).",
        "critical_reception": "Box-office success that cemented Universal's horror brand. Lugosi's performance became the template for screen vampires. Modern critics often note the film's dramatic stiffness in its second act but its first-act atmospherics remain influential.",
        "filmic_methods": [
            "expressionist low-key lighting with deep shadows in the castle sequences",
            "long static takes — the camera observes rather than participates",
            "minimal non-diegetic music for a sound-era film (an early-talkies habit)",
            "in-camera optical effects: bats, mist, eye-light close-ups on Lugosi",
            "theatrical blocking — the legacy of the stage adaptation",
            "iconography: the cape, the candelabra, the cobwebs, the staircase",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening at Castle Dracula — the carriage arrival, the staircase descent",
            "the eye-light close-up on Lugosi's first 'I am Dracula' moment",
            "Renfield's transformation aboard the schooner",
            "the London opera-house meeting with Mina",
            "Van Helsing's mirror reveal in the drawing room",
            "the Carfax Abbey climax",
        ],
        "most_relevant_film_theory": [
            "genre theory — the studio horror cycle as a producer-led genre formation",
            "iconography and visual convention as genre signal",
            "sociological / contextual reading — monster as displaced anxiety",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "lost-boys-1987": {
        "title": "The Lost Boys (1987)",
        "synopsis": "A teenage vampire film set in a fictional California beach town, in which two brothers discover the boardwalk's biker gang are vampires. The MTV-era teen horror — soundtrack-driven, glossy, ironic, aware of its own genre legacy.",
        "director_year_country": "Joel Schumacher — 1987 — USA",
        "major_characters": [
            "Michael Emerson — older brother, drawn into the gang",
            "Sam Emerson — younger brother, the audience surrogate",
            "David — leader of the vampire gang, charismatic and amoral",
            "Star — the girl on the threshold of becoming a vampire",
            "Lucy Emerson — the boys' mother, the absent-father subplot",
            "Edgar and Alan Frog — comic-book-store vampire hunters",
            "Max — the video-store owner, the head vampire",
        ],
        "major_themes": [
            "1980s consumerism and the boardwalk as commercial spectacle",
            "vampires as teen freedom fantasy — staying young forever",
            "broken family — single mother, absent father, sibling bond",
            "MTV-era cinema — image, music, surface",
            "the genre cycle — knowing reference to the older horror tradition",
            "anxiety about teenage independence",
        ],
        "production_context": "Made by Warner Bros at the height of 1980s teen-cinema dominance. Cinematographer Michael Chapman (Raging Bull) brought a saturated, music-video gloss. Score by Thomas Newman with a heavy needle-drop soundtrack including 'Cry Little Sister'. Marketed to the same MTV-watching teen audience as The Breakfast Club and The Goonies. Schumacher's earlier St. Elmo's Fire established his Brat Pack credentials. Significantly higher budget than Dracula — the difference between studio horror and 1980s blockbuster horror is itself a genre-evolution lesson.",
        "critical_reception": "Modest theatrical success; cult classic on home video and cable. Influenced subsequent teen-vampire texts (Buffy, Twilight). Often discussed in terms of how it updated horror iconography for the MTV generation.",
        "filmic_methods": [
            "saturated, neon-tinted night cinematography",
            "frequent crane shots and Steadicam tracking through the boardwalk",
            "rapid music-video-style editing during the gang sequences",
            "non-diegetic rock soundtrack used as score",
            "stylised costume — leather, mullets, earrings as gang signifier",
            "comic-book intertextuality — the Frog brothers reading horror comics on screen",
            "in-camera flying effects with wirework",
        ],
        "key_scenes_for_micro_analysis": [
            "the boardwalk-arrival sequence at the start",
            "the cliff-hang gang initiation",
            "the dinner-table 'noodles or worms' scene (no dialogue reproduction needed)",
            "the bathtub-of-blood reveal",
            "the comic-book store recruitment sequence",
            "the climactic house-fortification finale",
        ],
        "most_relevant_film_theory": [
            "genre theory — generic evolution and revision",
            "Bordwell on style — the music-video influence on continuity",
            "spectator positioning — the teen audience as target",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "singin-in-the-rain-1952": {
        "title": "Singin' in the Rain (1952)",
        "synopsis": "An MGM musical about Hollywood's transition from silent film to sound, made by the studio's Freed Unit at the height of the integrated-musical form. Self-reflexive, Technicolor, performance-driven — a film about the medium it celebrates.",
        "director_year_country": "Stanley Donen and Gene Kelly — 1952 — USA",
        "major_characters": [
            "Don Lockwood — silent-film matinee idol making the talkies transition (Gene Kelly)",
            "Kathy Selden — aspiring serious actress, the love interest (Debbie Reynolds)",
            "Cosmo Brown — Don's sidekick and pianist (Donald O'Connor)",
            "Lina Lamont — silent star with an unsuitable speaking voice (Jean Hagen)",
            "R. F. Simpson — studio head",
            "Roscoe Dexter — director within the film",
        ],
        "major_themes": [
            "the integrated musical — song and dance arising organically from narrative",
            "nostalgia for the silent era from the perspective of 1950s Hollywood",
            "the labour of performance — what it takes to make a number look effortless",
            "voice as identity — the gag of dubbing rebounds across the film",
            "old Hollywood self-mythology",
            "love story as device for reconciling competing professional ambitions",
        ],
        "production_context": "Made by MGM's Freed Unit (producer Arthur Freed), the studio's elite musical production team. Cinematographer Harold Rosson, with three-strip Technicolor at its mid-century peak. Choreography by Gene Kelly and Stanley Donen, who co-directed. Production-numbers shot on MGM's Stage 5 and Stage 27. Songs were almost all repurposed from earlier Freed catalogue rather than written new, which is itself a fact about Freed Unit production economics. Released into a market where television was beginning to bite into cinema attendance.",
        "critical_reception": "Modest success at original release; reputation grew through subsequent decades and now widely cited as the definitive American musical. Frequently appears at the top of best-musical critical polls.",
        "filmic_methods": [
            "long master shots of dance numbers — letting the dancer's whole body fill the frame",
            "saturated three-strip Technicolor palette: yellow raincoat, magenta, electric blue",
            "studio-lot rain effect for the title number",
            "non-diegetic orchestral arrangements integrated with diegetic vocal performance",
            "self-reflexive sound design — the dubbed-voice gag dramatises the medium",
            "split focus — the foreground number, the background reaction",
        ],
        "key_scenes_for_micro_analysis": [
            "the title number — Kelly dancing in the rain on a back-lot street",
            "the 'Make 'Em Laugh' solo on the studio lot",
            "the 'Good Morning' three-hander",
            "the early sound-on-set disaster sequence within the diegetic film-within-a-film",
            "the closing premiere reveal of the dubbing",
        ],
        "most_relevant_film_theory": [
            "the integrated musical as a generic mode (song / dance / narrative integrated rather than interrupted)",
            "self-reflexivity and intertextuality",
            "Bordwell on classical Hollywood style",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "grease-1978": {
        "title": "Grease (1978)",
        "synopsis": "A 1970s film musical set in late-1950s Rydell High, adapted from the 1971 stage show. The 1970s' nostalgia film par excellence — looking back at the rock-and-roll teen culture of two decades earlier through the lens of 1970s youth cinema.",
        "director_year_country": "Randal Kleiser — 1978 — USA",
        "major_characters": [
            "Danny Zuko — leader of the T-Birds (John Travolta)",
            "Sandy Olsson — Australian transfer student (Olivia Newton-John)",
            "Rizzo — leader of the Pink Ladies",
            "Kenickie — Danny's right-hand T-Bird",
            "Frenchy, Jan, Marty — Pink Ladies",
            "Sonny, Doody, Putzie — T-Birds",
        ],
        "major_themes": [
            "1970s nostalgia for the 1950s",
            "youth culture and rock-and-roll as identity",
            "gender performance — the climactic costume reversal",
            "high school as social hierarchy",
            "rebellion as posture rather than substance",
            "love story as social negotiation",
        ],
        "production_context": "Made by Paramount during the post-Star-Wars blockbuster era. Director Randal Kleiser, cinematographer Bill Butler. Choreography by Patricia Birch. Massive commercial hit — second-highest-grossing 1978 release. Soundtrack album produced by Louis St. Louis. The film's nostalgia-machine is typical of late-1970s Hollywood: American Graffiti (1973), Happy Days (1974-) and Animal House (1978) all mined the 1950s for 1970s audiences.",
        "critical_reception": "Mixed contemporary reviews; vast popular success. Modern reassessment often focuses on its gender politics (the closing transformation reads differently in different decades) and its place in the late-70s nostalgia boom.",
        "filmic_methods": [
            "Panavision widescreen framing of group ensemble numbers",
            "highly saturated colour — pinks, school-jacket reds, cars",
            "non-diegetic 1970s recording-studio sound on songs nominally diegetic",
            "fast cutting on dance numbers — closer to MTV than to the integrated-musical long take",
            "iconic costume choices: the leather jacket, the pink jacket, the satin",
            "deliberate anachronism — songs feel 1970s, settings feel 1950s",
        ],
        "key_scenes_for_micro_analysis": [
            "the beach-flashback opening 'Summer Nights' duet",
            "the 'Greased Lightnin'' garage number",
            "the dance-off at the gym",
            "Sandy's bedroom 'Hopelessly Devoted to You' solo",
            "the closing 'You're the One That I Want' transformation",
            "the carnival finale and the flying car",
        ],
        "most_relevant_film_theory": [
            "genre theory — the 1970s revival musical and the integrated form's evolution",
            "nostalgia as a 1970s mode (Jameson-influenced cultural reading at GCSE level)",
            "representation — the 1970s lens on 1950s gender",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "pillow-talk-1959": {
        "title": "Pillow Talk (1959)",
        "synopsis": "A late-1950s romantic comedy about an interior decorator and a songwriter who share a telephone party line and trade insults before falling in love. The high-water mark of the Doris Day persona and the colour-glossy Universal romantic comedy.",
        "director_year_country": "Michael Gordon — 1959 — USA",
        "major_characters": [
            "Jan Morrow — interior decorator (Doris Day)",
            "Brad Allen — songwriter and serial seducer (Rock Hudson)",
            "Jonathan Forbes — Brad's friend and Jan's persistent suitor (Tony Randall)",
            "Alma — Jan's housekeeper",
        ],
        "major_themes": [
            "1950s sexual politics — what could and could not be shown",
            "the career woman trope — Jan's professional independence",
            "performance of identity — Brad's invented Texan persona",
            "domestic space and the colour-coded apartment",
            "the telephone as a medium of intimacy and deception",
            "romantic comedy as a genre of mistaken identity",
        ],
        "production_context": "Universal-International production, photographed in CinemaScope and Eastmancolor by Arthur E. Arling. Director Michael Gordon (returning from a McCarthy-era blacklist). Costume design by Jean Louis. Released into a film culture still enforcing the Hays Code (production code era), which is why the famous 'double bed' was forbidden and the film's seductions are fully verbal. Doris Day's persona as wholesome career woman is itself a 1950s-Hollywood construction worth contextualising.",
        "critical_reception": "Major commercial hit; Best Original Screenplay Oscar in 1960. Subsequent reassessment is mixed — the gender politics that played as comic in 1959 read more uncomfortably now. It remains a touchstone of the late-classical Hollywood romantic comedy.",
        "filmic_methods": [
            "split-screen telephone conversations — the film's signature visual device",
            "saturated Eastmancolor production design — colour-coded apartments per character",
            "long static two-shots in the apartments contrasted with quick split-screen exchanges",
            "non-diegetic orchestral score with a recurring romantic theme",
            "Doris Day's vocal performance style — clean, projected, mid-Atlantic",
            "diegetic music inside Brad's songwriting flat",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening split-screen telephone duet establishing the conflict",
            "Brad's invented-Texan dinner-date masquerade",
            "the apartment-decoration revenge sequence near the end",
            "the bathtub split-screen sequence (no dialogue reproduction)",
            "the closing reconciliation",
        ],
        "most_relevant_film_theory": [
            "genre theory — the screwball-comedy heritage and its 1950s descendant",
            "representation — the 1950s career woman as constructed image",
            "Mulvey gaze theory at GCSE-appropriate framing — who looks at whom in the split-screen",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "when-harry-met-sally-1989": {
        "title": "When Harry Met Sally (1989)",
        "synopsis": "A Manhattan-set romantic comedy following a man and a woman who meet, lose touch, and meet again across twelve years, debating whether men and women can be friends. The post-feminism romantic-comedy benchmark and the verbal-sparring template for thirty years of follow-on films.",
        "director_year_country": "Rob Reiner — 1989 — USA",
        "major_characters": [
            "Harry Burns — political consultant, sceptic, neurotic (Billy Crystal)",
            "Sally Albright — journalist, organised, confident (Meg Ryan)",
            "Jess — Harry's best friend, magazine editor",
            "Marie — Sally's best friend, who falls for Jess",
        ],
        "major_themes": [
            "men and women as friends — the film's central question",
            "romantic comedy as a genre that can hold long-form character study",
            "1980s Manhattan as romantic geography",
            "verbal sparring as a courtship device (a screwball legacy)",
            "the friends-to-lovers narrative arc",
            "post-feminism and the renegotiated romantic landscape",
        ],
        "production_context": "Castle Rock Entertainment / Columbia Pictures production. Screenwriter Nora Ephron (a major figure in the late-80s/90s romantic-comedy revival). Cinematographer Barry Sonnenfeld. Score and song selections by Marc Shaiman, including a Harry Connick Jr. soundtrack album that became a hit in its own right. Editing by Robert Leighton. Released into a 1989 Hollywood that had largely abandoned the romantic comedy as a major genre — its commercial success effectively re-launched the form.",
        "critical_reception": "Critical and commercial hit. Frequently cited as one of the great Hollywood romantic comedies. Pauline Kael's review (in the New Yorker) and subsequent academic writing on the film and on Ephron's screenplay are well-known reference points; for free-tier work, refer to such writers as 'critics writing on the film' rather than reproducing copyrighted criticism.",
        "filmic_methods": [
            "character-vignette interviews with older couples cut between act blocks — a Brechtian framing device",
            "long static two-shots in restaurants and walk-and-talks in Central Park",
            "warm autumnal palette across all New York exteriors",
            "Harry Connick Jr. soundtrack as non-diegetic score",
            "minimal handheld — Sonnenfeld holds the frame still and lets the dialogue run",
            "split-screen telephone scene as a knowing reference back to Pillow Talk",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening road-trip drive from Chicago to New York",
            "the Katz's Delicatessen restaurant scene (refer descriptively, no dialogue reproduction)",
            "the post-divorce karaoke-store encounter",
            "the New Year's Eve party climax",
            "the talking-head couple interview cutaways",
        ],
        "most_relevant_film_theory": [
            "genre theory — romantic comedy and screwball heritage",
            "representation — post-feminist gender on screen",
            "Bordwell on style — character-driven dialogue as structural unit",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "rebel-without-a-cause-1955": {
        "title": "Rebel Without a Cause (1955)",
        "synopsis": "A high-school drama about a troubled teenager arriving in a new town and falling in with two other adolescents in crisis. The 1950s 'juvenile delinquent' film, James Dean's defining role, and a foundational text in the screen iconography of teenage rebellion.",
        "director_year_country": "Nicholas Ray — 1955 — USA",
        "major_characters": [
            "Jim Stark — the rebel of the title (James Dean)",
            "Judy — the girl drawn to him (Natalie Wood)",
            "John 'Plato' Crawford — the lonely third figure (Sal Mineo)",
            "Frank Stark — Jim's father, the absent authority figure",
            "Buzz — the high-school antagonist",
        ],
        "major_themes": [
            "1950s juvenile delinquency as a moral panic",
            "alienation from authority — parents, school, police",
            "fragile masculinity and the absent-father motif",
            "found family — the trio's brief shelter together",
            "rebellion as performance",
            "the planetarium and the cosmic frame for adolescent fear",
        ],
        "production_context": "Made by Warner Bros and shot in CinemaScope and WarnerColor by cinematographer Ernest Haller. James Dean was already filming Giant when it released. Director Nicholas Ray (later associated with European auteur readings of Hollywood film) developed the script with Stewart Stern from a 1944 case study. Famously the third of Dean's only three lead roles — he died in a car crash in September 1955, weeks before the film's October release. Hays Code era — visible only in what the film does NOT show.",
        "critical_reception": "Major commercial success, greatly amplified by Dean's death. Subsequently a touchstone of post-war American film studies, often discussed alongside The Wild One and Blackboard Jungle as the trilogy of 1950s teen films.",
        "filmic_methods": [
            "CinemaScope wide framing of the planetarium and cliff-edge sequences",
            "WarnerColor saturated palette — Jim's red windbreaker as iconographic signature",
            "long-take blocking around the staircase set in the Stark home",
            "non-diegetic Leonard Rosenman score using dissonance for adolescent emotion",
            "sympathetic high-key lighting on the trio in the abandoned mansion sequence",
            "blocking that pushes Plato into corners and Jim into open space",
        ],
        "key_scenes_for_micro_analysis": [
            "the police-station opening with the three protagonists separately introduced",
            "the planetarium-lecture set piece",
            "the chickie-run cliff-edge sequence",
            "the abandoned-mansion 'family' scene",
            "the closing planetarium-and-staircase climax",
        ],
        "most_relevant_film_theory": [
            "genre theory — the foundational text in the post-war teen-rebellion film cycle",
            "representation — adolescence as a constructed category in 1950s cinema",
            "auteurism — Nicholas Ray's framing as recognisable signature",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "ferris-buellers-1986": {
        "title": "Ferris Bueller's Day Off (1986)",
        "synopsis": "A Chicago-set teen comedy following a charismatic high-school senior who takes an unauthorised day off school. John Hughes's most expansive teen film and the 1980s answer to the 1950s rebel — playful rather than tortured, knowing rather than alienated.",
        "director_year_country": "John Hughes — 1986 — USA",
        "major_characters": [
            "Ferris Bueller — the protagonist, charm personified (Matthew Broderick)",
            "Cameron Frye — Ferris's anxious best friend (Alan Ruck)",
            "Sloane Peterson — Ferris's girlfriend (Mia Sara)",
            "Ed Rooney — the school principal pursuing Ferris (Jeffrey Jones)",
            "Jeanie Bueller — Ferris's resentful sister (Jennifer Grey)",
        ],
        "major_themes": [
            "1980s suburban affluence and the high-school as social system",
            "rebellion as pleasure rather than alienation",
            "the fourth wall and direct address — Ferris speaking to camera",
            "father-son anxiety routed through Cameron's plot rather than Ferris's",
            "Reagan-era teen optimism",
            "Chicago as romantic American city — the parade, the museum, the skyline",
        ],
        "production_context": "Made by Paramount Pictures for Hughes Productions. Cinematographer Tak Fujimoto (later Silence of the Lambs, Sixth Sense). Editor Paul Hirsch. Produced and directed by John Hughes during his 1984-87 peak (Sixteen Candles, The Breakfast Club, Pretty in Pink, Some Kind of Wonderful all sit in this run). The film's budget was modestly higher than the earlier Hughes teen films and the production used real Chicago locations — the Sears Tower, the Art Institute of Chicago, Wrigley Field, and a downtown parade staged for the film.",
        "critical_reception": "Major commercial success; widely considered one of the high points of 1980s teen cinema and of Hughes's career. The closing-credits Ferrari moment and the parade lip-sync are now widely referenced cultural images.",
        "filmic_methods": [
            "fourth-wall break — Ferris addresses the camera directly across the film",
            "warm Chicago summer-light cinematography",
            "long Steadicam tracking through the Bueller home and through downtown",
            "needle-drop pop soundtrack as non-diegetic score",
            "the Art Institute sequence — slow-motion close-ups paced to a non-diegetic instrumental",
            "the closing-credits scene as a coda — a habit later directors emulated",
        ],
        "key_scenes_for_micro_analysis": [
            "the fourth-wall opening monologue from Ferris's bed",
            "the museum-visit sequence with Cameron and the Seurat painting",
            "the downtown parade lip-sync set piece",
            "the Ferrari garage-attendant cutaway",
            "the closing-credits 'you're still here?' break",
        ],
        "most_relevant_film_theory": [
            "genre theory — the 1980s teen film as a Hughes-defined cycle",
            "Bordwell on style — fourth-wall address as classical narration's outer limit",
            "spectator positioning — direct address as audience flattery",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "body-snatchers-1956": {
        "title": "Invasion of the Body Snatchers (1956)",
        "synopsis": "A small-town doctor discovers that the residents of his California community are being replaced by emotionless duplicates grown from giant pods. The 1950s science-fiction film as Cold War allegory and the foundational paranoid invasion narrative.",
        "director_year_country": "Don Siegel — 1956 — USA",
        "major_characters": [
            "Dr Miles Bennell — the small-town physician (Kevin McCarthy)",
            "Becky Driscoll — Miles's old flame, returned to town (Dana Wynter)",
            "Jack Belicec — friend of Miles, an early discoverer",
            "Theodora 'Teddy' Belicec — Jack's wife",
            "Dan Kauffman — the town psychiatrist, ambiguous figure",
        ],
        "major_themes": [
            "Cold War paranoia — communism / McCarthyism allegory",
            "conformity and the loss of individuality",
            "the small town as both safe space and enemy",
            "rationality (the doctor) versus the irrational",
            "the boundary between human and inhuman",
            "the body as site of invasion",
        ],
        "production_context": "An Allied Artists production, modestly budgeted for a B-picture. Cinematographer Ellsworth Fredericks shot in monochrome SuperScope. Director Don Siegel (later Dirty Harry). Score by Carmen Dragon. Released into the height of the Red Scare and shortly after the McCarthy hearings — the political reading is built into its first reception. The film's framing device (a hospital interview where Miles tells the story to a sceptical psychiatrist) was added by Allied Artists against Siegel's wishes; the in-film narrative reads as ambiguously paranoid as a result.",
        "critical_reception": "Modest 1956 release reception; reputation grew over decades. Now widely studied as the foundational text of the 1950s science-fiction allegory cycle and as a key Cold War film. Has been remade three times (Kaufman 1978, Ferrara 1993, Hirschbiegel 2007).",
        "filmic_methods": [
            "monochrome SuperScope cinematography with deep contrast",
            "low-key lighting in the basement / pod-discovery sequences",
            "long static medium shots that hold the small-town normality intact",
            "an unsettling diegetic-versus-non-diegetic sound design — distant ambient noise that should not be there",
            "narrative framing device (the hospital interview) bracketing the flashback",
            "the pod itself as an iconographic object — the moment of its first reveal is staged as gradual rather than shock",
        ],
        "key_scenes_for_micro_analysis": [
            "the quiet small-town opening establishing normality",
            "the basement-pod discovery at the Belicec house",
            "the greenhouse pod-growing reveal",
            "the late-act 'don't fall asleep' chase through the streets",
            "the highway 'they're already here!' final monologue",
        ],
        "most_relevant_film_theory": [
            "sociological / allegorical reading — film as cultural symptom",
            "genre theory — the 1950s science-fiction-horror cycle",
            "narrative theory — the framing device and unreliable narration",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "et-1982": {
        "title": "E.T. the Extra-Terrestrial (1982)",
        "synopsis": "A suburban Californian boy befriends a stranded extraterrestrial and helps him return home. Steven Spielberg's child's-eye-view science-fiction fable and a foundational text of 1980s family cinema.",
        "director_year_country": "Steven Spielberg — 1982 — USA",
        "major_characters": [
            "Elliott — the ten-year-old protagonist (Henry Thomas)",
            "E.T. — the alien botanist",
            "Mary — Elliott's mother, a single parent",
            "Gertie — Elliott's younger sister (Drew Barrymore)",
            "Michael — Elliott's older brother",
            "Keys — the government scientist",
        ],
        "major_themes": [
            "the alien as friend, not threat — opposing the 1950s tradition",
            "1980s suburbia as cinematic space — bicycles, cul-de-sacs, kitchens",
            "the broken family — single mother, absent father",
            "childhood imagination and emotional life",
            "compassion as moral compass",
            "the spectator-as-child point of view",
        ],
        "production_context": "An Amblin Entertainment / Universal production. Cinematographer Allen Daviau (a frequent Spielberg collaborator). Production designer James D. Bissell. Score by John Williams — one of the most-recognised film scores of its era. Released summer 1982 against a strong field; the highest-grossing film at original release of any film to that date. The Amblin production aesthetic (warm light through doorways, suburban kitchens, child's-eye-view low camera) became a template that 1980s and post-2010s 'Amblin tribute' films continue to reference (Stranger Things, Super 8).",
        "critical_reception": "Massive critical and commercial hit. Frequently cited as the foundational text of the family-blockbuster mode that Spielberg shaped through the 1980s. Modern reassessment continues to engage with its representation of single motherhood and its emotional-manipulation craft.",
        "filmic_methods": [
            "low-angle child's-eye-view camera throughout suburban scenes",
            "warm key-light through kitchen doorways and forest moonlight",
            "John Williams non-diegetic score that explicitly cues emotion",
            "the bicycle-flying sequence as an iconographic image",
            "BMX iconography — the bike as freedom and friendship motif",
            "long takes in the bedroom scenes that allow child performance to unfold",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening forest pursuit (E.T.'s arrival)",
            "the closet hide-and-find first contact",
            "the Halloween bike-ride sequence",
            "the iconic flying-bicycles silhouette against the moon",
            "the closing 'I'll be right here' departure",
        ],
        "most_relevant_film_theory": [
            "genre theory — family blockbuster as Spielberg-shaped 1980s mode",
            "auteurism — the Amblin / Spielberg signature aesthetic",
            "spectator positioning — child's-eye-view as audience strategy",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "juno-2007": {
        "title": "Juno (2007)",
        "synopsis": "A whip-smart Minnesota teenager facing an unplanned pregnancy chooses to give the baby up for adoption to a suburban couple. Indie-comedy benchmark of the late 2000s and a watershed for the Fox Searchlight specialty-division era.",
        "director_year_country": "Jason Reitman — 2007 — USA",
        "major_characters": [
            "Juno MacGuff — the protagonist (Ellen Page / Elliot Page)",
            "Paulie Bleeker — the father",
            "Mac MacGuff — Juno's father (J. K. Simmons)",
            "Bren MacGuff — Juno's stepmother",
            "Mark Loring — prospective adoptive father (Jason Bateman)",
            "Vanessa Loring — prospective adoptive mother (Jennifer Garner)",
        ],
        "major_themes": [
            "tonal comedy — finding humour in serious subject matter without flippancy",
            "the indie 'voice' — stylised dialogue as character identity",
            "non-judgemental treatment of teenage pregnancy",
            "indie soundtrack as character extension",
            "domestic mise-en-scene — the suburban home as warm rather than oppressive",
            "the Fox Searchlight specialty-division business model",
        ],
        "production_context": "Made by Mr. Mudd Productions and distributed by Fox Searchlight Pictures (the specialty-division indie arm of 20th Century Fox). Screenwriter Diablo Cody (her debut feature; she won an Academy Award for Original Screenplay). Cinematographer Eric Steelberg. Soundtrack curated heavily around Kimya Dawson and the Moldy Peaches — a deliberate aesthetic choice that became part of the film's identity. Made for around $7m and grossed over $230m worldwide. Often cited as the high-water mark of the late-2000s indie-comedy moment alongside Little Miss Sunshine and (500) Days of Summer.",
        "critical_reception": "Major critical and commercial success. Four Academy Award nominations, including Best Picture. Subsequent reassessment has been mixed — Cody's stylised dialogue has been read as both a strength and a weakness depending on the critic.",
        "filmic_methods": [
            "stylised, mannered dialogue as character voice",
            "warm domestic palette inside the MacGuff home",
            "needle-drop indie-folk soundtrack as non-diegetic score",
            "long static-camera dialogue scenes — the writing carries the cinematography",
            "voice-over confidence at narrative thresholds",
            "graphic-titles cartoon sequences that interrupt diegetic action",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening hamburger-phone test sequence",
            "the convenience-store 'three of these' purchase",
            "the Loring living-room first-meeting scene",
            "Juno's track-running encounter with Paulie",
            "the closing porch duet scene",
        ],
        "most_relevant_film_theory": [
            "genre theory — indie-comedy as a late-2000s mode",
            "auteurism — Reitman's directorial signature plus Cody as screenwriter-author",
            "specialty-division economics as institutional context",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "whiplash-2014": {
        "title": "Whiplash (2014)",
        "synopsis": "An ambitious young drummer at an elite New York conservatory falls under the orbit of a brutally demanding teacher. Damien Chazelle's breakout indie thriller and a benchmark for editing rhythm and percussive sound design.",
        "director_year_country": "Damien Chazelle — 2014 — USA",
        "major_characters": [
            "Andrew Neiman — the drummer (Miles Teller)",
            "Terence Fletcher — the conducting teacher (J. K. Simmons)",
            "Nicole — Andrew's brief girlfriend",
            "Jim Neiman — Andrew's father",
        ],
        "major_themes": [
            "ambition and abuse — what greatness costs",
            "mentor-pupil power dynamics",
            "music as labour rather than transcendence",
            "individual perfectionism versus the orchestra as collective",
            "the cost of obsessive practice on the body",
            "indie thriller as a lean form",
        ],
        "production_context": "Made by Bold Films, Blumhouse Productions and Right of Way Films. Distributed by Sony Pictures Classics (a specialty division). Director Damien Chazelle (later La La Land, First Man). Cinematographer Sharone Meir. Editor Tom Cross (Academy Award winner for this film). Composers Justin Hurwitz with songs by Hank Levy. Made for around $3m and grossed over $49m. Originally a 2013 short film that Chazelle expanded to feature length after Sundance success. Three Academy Awards including Best Supporting Actor and Best Film Editing.",
        "critical_reception": "Major critical hit. Cross's editing and Simmons's performance are widely studied. Subsequent debate has focused on whether the film endorses or critiques Fletcher's teaching philosophy — the closing sequence reads either way depending on the critic.",
        "filmic_methods": [
            "rhythmic cutting tied to drum hits — editing as percussion",
            "extreme close-ups on hands, sweat, blood, cymbals",
            "warm jazz-club lighting in the rehearsal-room scenes",
            "diegetic music as the film's effective score",
            "handheld coverage during emotional dialogue, locked-off camera during performance",
            "long single-take crescendos in the final sequence",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening solo-drumming entry into the rehearsal room",
            "the chair-throwing teaching scene",
            "the car-crash mid-act sequence",
            "the public confrontation in the second-act jazz club",
            "the closing solo-drumming sequence",
        ],
        "most_relevant_film_theory": [
            "auteurism — Chazelle's directorial signature",
            "Bordwell on style — editing as the structural principle",
            "spectator positioning — the closing-sequence ambiguity",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "lady-bird-2017": {
        "title": "Lady Bird (2017)",
        "synopsis": "A senior at a Catholic high school in Sacramento navigates her last year at home. Greta Gerwig's solo directorial debut — autobiographical-feeling, vignette-structured, precise in its craft beneath the warmth.",
        "director_year_country": "Greta Gerwig — 2017 — USA",
        "major_characters": [
            "Christine 'Lady Bird' McPherson — the protagonist (Saoirse Ronan)",
            "Marion McPherson — her mother (Laurie Metcalf)",
            "Larry McPherson — her father",
            "Julie Steffans — her best friend",
            "Danny — her first boyfriend",
            "Kyle — her second boyfriend",
            "Sister Sarah Joan — the school's principal nun",
        ],
        "major_themes": [
            "mother-daughter dynamic across the year of leaving home",
            "place and belonging — Sacramento as both prison and home",
            "Catholic school as social setting",
            "early-2000s context (the post-9/11 backdrop, AIM messaging, dial-up music)",
            "memory and nostalgia",
            "ambition and class anxiety",
        ],
        "production_context": "Made by Scott Rudin Productions, Management 360 and IAC Films. Distributed by A24. Director and writer Greta Gerwig (her solo directorial debut). Cinematographer Sam Levy. Editor Nick Houy. Music by Jon Brion plus a curated late-90s/early-2000s needle-drop soundtrack. Made for around $10m and grossed over $78m. Five Academy Award nominations including Best Picture and Best Director. A24's specialty-division ascendancy in the late 2010s is its institutional context — Lady Bird became one of the studio's signature hits.",
        "critical_reception": "Major critical hit; high audience scores; widely cited example of late-2010s indie-coming-of-age cinema. Reviewers from Manohla Dargis (NYT) onwards praised Gerwig's directorial precision; for free-tier work, refer to such writers as 'critics writing on the film' rather than reproducing copyrighted criticism.",
        "filmic_methods": [
            "vignette structure — short scenes punctuated by hard cuts",
            "warm Sacramento autumnal light",
            "naturalistic dialogue (against Cody-style indie stylisation)",
            "passing-time montages set to Dave Matthews Band and other early-2000s tracks",
            "two-shots that hold mother and daughter in the frame together — a Gerwig signature",
            "ending phone-call sequence cross-cut between two locations",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening car-door dive that gives Lady Bird's first-act tone",
            "the school musical-theatre-audition sequence",
            "the prom-rejection moment and its quiet aftermath",
            "the New York arrival sequence",
            "the closing voicemail-and-walk sequence",
        ],
        "most_relevant_film_theory": [
            "auteurism — Gerwig's directorial debut style",
            "narrative theory — vignette structure versus three-act convention",
            "representation — late-2010s coming-of-age cinema and gender",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "hurt-locker-2008": {
        "title": "The Hurt Locker (2008)",
        "synopsis": "An American Explosive Ordnance Disposal team in Iraq faces the daily work of disarming bombs in Baghdad. Kathryn Bigelow's Iraq-war thriller and a foundational text of the issue-led contemporary indie war film.",
        "director_year_country": "Kathryn Bigelow — 2008 — USA",
        "major_characters": [
            "Sergeant William James — the new EOD team leader (Jeremy Renner)",
            "Sergeant J. T. Sanborn — the team's second-in-command",
            "Specialist Owen Eldridge — the youngest team member",
            "Colonel John Cambridge — the unit's commander",
        ],
        "major_themes": [
            "war as work — the EOD specialist's daily labour",
            "addiction to risk — the title's metaphor",
            "the Iraq War as recent history",
            "masculinity and combat",
            "the contractor/soldier moral frame",
            "issue-led indie cinema as political intervention",
        ],
        "production_context": "Made by Voltage Pictures, Grosvenor Park Media and Film Capital Europe Funds. Distributed by Summit Entertainment. Director Kathryn Bigelow (the first woman to win Best Director at the Academy Awards for this film). Screenwriter Mark Boal (a war-correspondent journalist whose embedded reporting informed the script). Cinematographer Barry Ackroyd (a Ken Loach regular). Editor Bob Murawski and Chris Innis. Made for around $15m, mostly shot on 16mm in Jordan with handheld cameras. Six Academy Awards including Best Picture, Best Director, Best Original Screenplay.",
        "critical_reception": "Major critical hit; modest theatrical performance amplified by awards. Subsequent debate has continued over its political stance — does the film critique or aestheticise the Iraq invasion? The film won Best Picture against Avatar, a fact often noted in contemporary coverage.",
        "filmic_methods": [
            "handheld 16mm cinematography across all locations",
            "long lenses for spectator-distance during bomb-disposal sequences",
            "diegetic-only ambient sound — sparse non-diegetic score",
            "extreme telephoto coverage of urban watchers — the question of who is observing whom",
            "rapid in-camera focus pulls during tension sequences",
            "extended real-time bomb-disposal sequences with minimal cutting",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening pre-credits bomb-disposal that introduces the team's first leader",
            "the desert-sniper duel mid-act",
            "the supermarket-aisle cereal-choice cutaway in the closing act",
            "the climactic city-square car-bomb sequence",
            "the closing return-to-Iraq tarmac shot",
        ],
        "most_relevant_film_theory": [
            "documentary realism as aesthetic strategy",
            "auteurism — Bigelow's directorial signature",
            "issue-led indie cinema as institutional category",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "hate-u-give-2018": {
        "title": "The Hate U Give (2018)",
        "synopsis": "A Black teenager from a poor neighbourhood attends an affluent suburban school and witnesses the police shooting of a childhood friend. George Tillman Jr.'s adaptation of Angie Thomas's YA novel, the foundational Black-Lives-Matter-era youth indie.",
        "director_year_country": "George Tillman Jr. — 2018 — USA",
        "major_characters": [
            "Starr Carter — the protagonist (Amandla Stenberg)",
            "Khalil — Starr's childhood friend",
            "Maverick 'Mav' Carter — Starr's father",
            "Lisa Carter — Starr's mother",
            "Chris — Starr's white boyfriend",
            "King — local gang leader",
            "April Ofrah — the lawyer",
        ],
        "major_themes": [
            "police violence and Black Lives Matter context",
            "code-switching between two communities — Garden Heights and Williamson Prep",
            "voice and silence — when to speak, what speaking costs",
            "family as moral frame",
            "youth activism",
            "issue-led indie cinema in the late 2010s",
        ],
        "production_context": "Made by Fox 2000 Pictures, State Street Pictures and Temple Hill Entertainment. Distributed by 20th Century Fox. Director George Tillman Jr. (Soul Food, Notorious). Adapted from Angie Thomas's bestselling 2017 YA novel. Cinematographer Mihai Mălaimare Jr. Editor Alex Blatt and Craig Hayes. Made for around $23m and grossed over $34m. Released into a 2018 culture moment when Black Lives Matter as a movement and as a publishing-and-film category was at its broadest reach. The film is studied in the indie unit although it had wide-release distribution because its thematic material aligns with issue-led indie sensibility.",
        "critical_reception": "Major critical and audience response, particularly among student readers of Thomas's novel. NAACP Image Award winner. Subsequent reassessment focuses on the film's deliberate accessibility — its YA register meant it reached audiences that more challenging Black-cinema entries could not.",
        "filmic_methods": [
            "naturalistic mid-shot coverage of family scenes",
            "warm, saturated palette in Garden Heights; cooler greys at Williamson Prep",
            "handheld camera during the police-shooting sequence and its aftermath",
            "non-diegetic score by Dustin O'Halloran with a Black-music needle-drop overlay",
            "voice-over by Starr threading first-person reflection",
            "code-switching dramatised through framing — closer in family scenes, wider at school",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening 'the talk' father-children kitchen-table scene",
            "the traffic-stop police-shooting sequence",
            "the protest-and-tear-gas mid-act sequence",
            "the kitchen confrontation with King in the third act",
            "the closing house-fire and recovery sequence",
        ],
        "most_relevant_film_theory": [
            "representation — race, ethnicity and youth on screen",
            "issue-led indie cinema as institutional category",
            "narrative theory — first-person voice-over and audience identification",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "slumdog-2008": {
        "title": "Slumdog Millionaire (2008)",
        "synopsis": "A young man from the Mumbai slums sits one question away from winning the Indian version of Who Wants to Be a Millionaire? while the police interrogate him over how he could possibly know the answers. Danny Boyle's frame-narrative love story.",
        "director_year_country": "Danny Boyle (co-directed by Loveleen Tandan) — 2008 — UK / India",
        "major_characters": [
            "Jamal Malik — the protagonist (Dev Patel)",
            "Latika — the woman Jamal loves",
            "Salim — Jamal's older brother",
            "Prem Kumar — the quiz-show host",
            "the Inspector — the Mumbai police investigator",
        ],
        "major_themes": [
            "fate, destiny and the love story",
            "Mumbai as transforming megacity — slum to glass tower",
            "social mobility and the lottery of birth",
            "corruption and survival",
            "frame narrative as machinery of memory",
            "globalisation and the export of British and Indian cinema",
        ],
        "production_context": "A British-Indian co-production made by Celador Films and Film4 Productions, distributed by Fox Searchlight Pictures. Director Danny Boyle (with co-director Loveleen Tandan crediting the Hindi-language scenes). Screenwriter Simon Beaufoy (adapting Vikas Swarup's novel Q & A). Cinematographer Anthony Dod Mantle (Dogme 95 veteran). Editor Chris Dickens. Score by A. R. Rahman. Made for around $15m, shot in Mumbai with a mixed Hindi/English production. Eight Academy Awards including Best Picture, Best Director, Best Adapted Screenplay.",
        "critical_reception": "Major critical and commercial hit. Subsequent reassessment has engaged with questions about its representation of poverty, the British-director's-eye-on-Mumbai framing, and the closing dance sequence's tonal switch.",
        "filmic_methods": [
            "frame narrative — quiz show as the present, flashbacks as the past",
            "dual timeline editing",
            "saturated colour palette — yellows and reds particularly in the Mumbai scenes",
            "handheld camera throughout chase and slum sequences",
            "A. R. Rahman score blending diegetic Mumbai street music and non-diegetic instrumental",
            "closing-credits Bollywood dance number as deliberate tonal coda",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening interrogation scene establishing the frame",
            "the childhood toilet-pit-to-autograph sequence",
            "the train-rooftop traversal of central India",
            "the Taj Mahal tourist-scam sequence",
            "the closing platform dance number",
        ],
        "most_relevant_film_theory": [
            "Todorov's narrative model — equilibrium, disruption, new equilibrium",
            "frame narrative as a structural principle",
            "global film and the British-Asian co-production model",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "wadjda-2012": {
        "title": "Wadjda (2012)",
        "synopsis": "A ten-year-old girl in Riyadh wants a green bicycle she sees in a shop and enters her school's Quran-recitation competition to win the prize money. Haifaa Al-Mansour's debut feature — the first feature film shot entirely in Saudi Arabia, the first by a Saudi female director.",
        "director_year_country": "Haifaa Al-Mansour — 2012 — Saudi Arabia / Germany",
        "major_characters": [
            "Wadjda — the ten-year-old protagonist (Waad Mohammed)",
            "Wadjda's mother — caught between work, marriage and motherhood",
            "Wadjda's father — peripheral figure considering a second wife",
            "Abdullah — Wadjda's neighbourhood friend who has a bicycle",
            "Ms. Hussa — the school principal",
        ],
        "major_themes": [
            "girlhood under restriction — what mobility means in 2010s Saudi Arabia",
            "the bicycle as symbol of agency",
            "motherhood and women's economic precariousness",
            "religious culture and individual desire",
            "national cinema emerging from a country with no previous feature-film industry",
            "small-scale narrative as political document",
        ],
        "production_context": "Made by Razor Film Produktion (Germany) and Highlook Group (UAE / Saudi Arabia). Distributed internationally by Pictures in a Frame and Sony Pictures Classics in the US. Director and screenwriter Haifaa Al-Mansour. Cinematographer Lutz Reitemeier. Score by Max Richter. Made for around €3m. Filmed in Riyadh — Al-Mansour reportedly directed many street scenes from inside a van, since at the time of production women were not permitted to direct men in public spaces in Saudi Arabia. The film helped catalyse the gradual loosening of restrictions on Saudi cinema (Saudi Arabia ended its commercial-cinema ban in 2018).",
        "critical_reception": "Major international critical hit; selected as Saudi Arabia's first-ever submission to the Best Foreign-Language Film Academy Award category. Widely studied for the bicycle as symbol and for its production-context story of the female director.",
        "filmic_methods": [
            "naturalistic lighting and observation — hand-held within a generally locked frame",
            "child's-eye-view low-angle shots through Wadjda's perspective",
            "long static takes that hold scenes of restriction",
            "Max Richter score used sparingly",
            "framing of female characters often through doorways and windows — visible enclosure",
            "the bicycle introduced visually before it is named",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening classroom recitation sequence",
            "the toy-shop bicycle reveal",
            "the rooftop sequence with Wadjda and her mother",
            "the Quran-competition prize-announcement sequence",
            "the closing street-traversal sequence",
        ],
        "most_relevant_film_theory": [
            "representation — gender, age, culture in non-Western cinema",
            "Mulvey gaze theory at GCSE-appropriate framing — who is permitted to look",
            "national cinema as a category and a political project",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "girlhood-2014": {
        "title": "Girlhood (2014, original title 'Bande de filles')",
        "synopsis": "A Black teenage girl in suburban Paris falls in with a friendship group of three other young women and renegotiates her identity. Celine Sciamma's third feature, on Black femininity and friendship in the Parisian banlieues.",
        "director_year_country": "Celine Sciamma — 2014 — France",
        "major_characters": [
            "Marieme / Vic — the protagonist (Karidja Toure)",
            "Lady, Adiatou, Fily — the three friends",
            "Marieme's older brother — a controlling presence",
            "Ismael — Marieme's love interest",
            "Marieme's younger sister",
        ],
        "major_themes": [
            "Black femininity on screen in French cinema",
            "girlhood and friendship as identity formation",
            "the suburban banlieue as social space",
            "music and dance as belonging",
            "constraints — domestic, economic, gendered",
            "subverting national-cinema stereotypes",
        ],
        "production_context": "Made by Hold Up Films (France) and Lilies Films. Distributed internationally by Strand Releasing. Director and screenwriter Celine Sciamma (whose work traces the development of girls and young women — Water Lilies, Tomboy, Portrait of a Lady on Fire). Cinematographer Crystel Fournier. Editor Julien Lacheray. Score by Para One (Jean-Baptiste de Laubier). Made for around €4m and shot in Paris suburbs. Won the Carrosse d'Or at Cannes Directors' Fortnight 2014.",
        "critical_reception": "Major critical hit on the international festival circuit; debate has continued over the cultural ethics of a white French director making a Black-led film, which is a useful classroom topic at GCSE level when handled carefully.",
        "filmic_methods": [
            "Cinemascope widescreen framing of the four friends as ensemble",
            "saturated colour blocks — pink, blue, the costume choices used as identity statement",
            "long static takes that hold the friends in frame together",
            "needle-drop and original score (Para One) used in extended sequences",
            "the famous Rihanna 'Diamonds' karaoke scene as a single sustained set-piece",
            "the 'mall ambush' opening sequence with high-key field lighting",
        ],
        "key_scenes_for_micro_analysis": [
            "the opening American-football-game tracking shot",
            "the train-station fight sequence",
            "the hotel-room karaoke 'Diamonds' set piece",
            "the boxing-fight in the second act",
            "the closing crossing-the-road sequence",
        ],
        "most_relevant_film_theory": [
            "representation — gender, ethnicity, age, culture",
            "Mulvey gaze theory at GCSE-appropriate framing — who looks at whom in the frame",
            "national cinema and cultural politics",
        ],
        "copyright_status": "IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "uk-film-context": {
        "title": "Contemporary UK Film — generic context",
        "synopsis": "Five contemporary UK films released since 2010 demonstrating distinct aesthetic styles: Submarine (Ayoade, 2010), Attack the Block (Cornish, 2011), Skyfall (Mendes, 2012), Rocks (Gavron, 2019) and Blinded by the Light (Chadha, 2019). The lesson teaches the AESTHETIC focus area — distinctive 'look' and how it shapes meaning.",
        "director_year_country": "various — 2010–2019 — UK",
        "major_characters": ["see individual films — the lesson teaches aesthetic style across the five options, not character per film"],
        "major_themes": [
            "indie aesthetic (Submarine — Ayoade's stylised colour and Wes-Anderson-influenced framing)",
            "genre-film aesthetic (Attack the Block — Cornish's South London science fiction look)",
            "blockbuster aesthetic (Skyfall — Mendes and cinematographer Roger Deakins's spectacle look)",
            "social-realist aesthetic (Rocks — Gavron's hand-held London naturalism)",
            "musical-drama aesthetic (Blinded by the Light — Chadha's Bruce-Springsteen-led aesthetic)",
            "the spectacle-versus-narrative balance",
            "production design as part of national-cinema identity",
        ],
        "production_context": "Each film sits in a different industrial context. Submarine — Warp Films, Film4. Attack the Block — Big Talk Productions, StudioCanal. Skyfall — MGM, Eon Productions, Columbia. Rocks — Fable Pictures, Film4. Blinded by the Light — Cornerstone Films, Bend It Films, Levantine Films. The unit covers all five at aesthetic level rather than narrative or character, with named cinematographers where notable: Roger Deakins (Skyfall), Erik Wilson (Submarine), Helene Louvart (Rocks).",
        "critical_reception": "Reception varies film-by-film. Skyfall is the largest commercial success of the five; Rocks the most critically lauded as a social-realist achievement; Submarine a cult-favourite indie debut.",
        "filmic_methods": [
            "Submarine — saturated 1980s-throwback colour palette, mannered dialogue, Alex Turner score",
            "Attack the Block — neon-lit South London nights, hand-held council-block geography, John Carpenter-influenced score",
            "Skyfall — Roger Deakins's silhouette-and-skyline blockbuster framing, Shanghai-tower set piece, Adele theme song",
            "Rocks — naturalistic light, hand-held coverage of a non-professional teenage cast, real London exteriors",
            "Blinded by the Light — Springsteen needle-drops, magical-realist text-overlay sequences, warm Luton autumnal light",
        ],
        "key_scenes_for_micro_analysis": [
            "Submarine — the credit-sequence beach montage",
            "Attack the Block — the opening firework-night street confrontation",
            "Skyfall — the Shanghai-tower silhouette assassination sequence",
            "Rocks — the school-corridor improvisation scene",
            "Blinded by the Light — the rooftop 'Born to Run' lyric-overlay sequence",
        ],
        "most_relevant_film_theory": [
            "auteurism — director-as-stylist applied across five British directors",
            "Bordwell on style — how distinct aesthetic registers shape spectator experience",
            "national cinema — UK as a spectrum of production scales",
        ],
        "copyright_status": "All five films IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "global-english-context": {
        "title": "Global English-Language Film — generic context",
        "synopsis": "Five global English-language films produced outside the US demonstrating distinct narrative approaches: Slumdog Millionaire (Boyle, UK/India, 2008), District 9 (Blomkamp, South Africa, 2009), The Babadook (Kent, Australia, 2014), The Breadwinner (Twomey, Ireland, 2017) and Jojo Rabbit (Waititi, New Zealand, 2019). The lesson teaches the NARRATIVE focus area.",
        "director_year_country": "various — 2008–2019 — global English-language outside US",
        "major_characters": ["see individual films — the lesson teaches narrative across the five options"],
        "major_themes": [
            "frame narrative (Slumdog Millionaire — quiz show as present-tense framing)",
            "mockumentary narrative (District 9 — interview-and-news-footage opening folding into conventional narration)",
            "horror narrative (The Babadook — domestic narrative inflected by horror conventions)",
            "animation narrative (The Breadwinner — animated frame-tale within a frame-tale)",
            "satirical narrative (Jojo Rabbit — first-person child's-eye-view of Nazi Germany)",
            "Todorov's equilibrium / disruption / new equilibrium",
            "non-linear time and withholding/releasing",
        ],
        "production_context": "Slumdog — Celador / Film4 / Fox Searchlight, dir Danny Boyle. District 9 — TriStar / WingNut Films, dir Neill Blomkamp. The Babadook — Causeway Films / Smoking Gun / Screen Australia, dir Jennifer Kent. The Breadwinner — Cartoon Saloon / Aircraft Pictures / Melusine Productions, dir Nora Twomey, exec produced by Angelina Jolie. Jojo Rabbit — Fox Searchlight / Czech Anglo Productions, dir Taika Waititi. The diasporic / transnational production context is itself a teaching point.",
        "critical_reception": "Slumdog Millionaire — eight Academy Awards. Jojo Rabbit — Best Adapted Screenplay Academy Award. District 9 — Best Picture nomination. The Babadook — major critical hit on the festival horror circuit. The Breadwinner — Annie Award winner and Academy Award nominee for Best Animated Feature.",
        "filmic_methods": [
            "Slumdog — frame narrative, dual timeline, saturated palette, A. R. Rahman score",
            "District 9 — mockumentary-into-narrative shift, handheld 16mm, news-footage intercutting",
            "The Babadook — claustrophobic domestic framing, low-key palette, sound-design shocks",
            "The Breadwinner — 2D animation alternating with stylised storybook insets, child-narrator voice-over",
            "Jojo Rabbit — saturated symmetrical Wes-Anderson-influenced compositions, anachronistic music, child's-eye-view",
        ],
        "key_scenes_for_micro_analysis": [
            "Slumdog — the opening interrogation",
            "District 9 — the documentary-to-narrative break-point",
            "The Babadook — the children's-book reveal",
            "The Breadwinner — the storybook frame-tale insets",
            "Jojo Rabbit — the imaginary-Hitler dance opening",
        ],
        "most_relevant_film_theory": [
            "Todorov's equilibrium / disruption / new equilibrium",
            "Bordwell on narration as the formal organisation of story information",
            "frame narrative as structural principle",
        ],
        "copyright_status": "All five films IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "global-non-english-context": {
        "title": "Global Non-English-Language Film — generic context",
        "synopsis": "Five global non-English-language films demonstrating distinct representation choices: Tsotsi (Hood, South Africa, 2005), The Wave (Gansel, Germany, 2008), Wadjda (Al-Mansour, Saudi Arabia, 2012), Girlhood (Sciamma, France, 2014), The Farewell (Wang, China/US, 2019). The lesson teaches the REPRESENTATION focus area.",
        "director_year_country": "various — 2005–2019 — non-English-language",
        "major_characters": ["see individual films — the lesson teaches representation across the five options"],
        "major_themes": [
            "South African post-apartheid identity (Tsotsi)",
            "fascism's recurrence and conformity in modern Germany (The Wave)",
            "girlhood under restriction in Saudi Arabia (Wadjda)",
            "Black femininity and the Parisian banlieue (Girlhood)",
            "diasporic Chinese-American identity and family (The Farewell)",
            "stereotype, counter-type and spectator positioning",
            "the gaze — who is permitted to look",
        ],
        "production_context": "Tsotsi — UK/SA co-production, dir Gavin Hood, Academy Award winner Best Foreign-Language Film. The Wave — German production, dir Dennis Gansel. Wadjda — Saudi/German, dir Haifaa Al-Mansour. Girlhood — French, dir Celine Sciamma. The Farewell — US/Chinese, dir Lulu Wang, distributed by A24.",
        "critical_reception": "Tsotsi — Academy Award winner. The Wave — major German box-office hit. Wadjda — international festival breakthrough. Girlhood — Cannes Directors' Fortnight prize. The Farewell — Independent Spirit Awards Best Feature.",
        "filmic_methods": [
            "Tsotsi — Johannesburg slum naturalism, low-key lighting, kwaito music score",
            "The Wave — controlled school-room framing, gradual handheld escalation, classical-film-noir cuts",
            "Wadjda — restrained child's-eye-view, framing through doorways and windows, sparing Max Richter score",
            "Girlhood — Cinemascope ensemble framing, saturated colour blocks, Para One score",
            "The Farewell — slow static takes, warm interior light, restrained score",
        ],
        "key_scenes_for_micro_analysis": [
            "Tsotsi — the township-arrival opening",
            "The Wave — the classroom 'unity' sequence",
            "Wadjda — the toy-shop bicycle reveal",
            "Girlhood — the hotel-room karaoke 'Diamonds' set piece",
            "The Farewell — the wedding-banquet hall set piece",
        ],
        "most_relevant_film_theory": [
            "Mulvey gaze theory at GCSE-appropriate framing",
            "representation — stereotype and counter-type",
            "national cinema as a category and a political project",
        ],
        "copyright_status": "All five films IN COPYRIGHT — 15-word cap, paraphrase preferred",
    },
    "specialist-writing-context": {
        "title": "Specialist Writing on Film — generic context",
        "synopsis": "Three sources of specialist writing rotate every three years on the WJEC secure website: one source on cinematography, one source on US independent film, one film review (one set per US independent film option). The lesson teaches the SKILL of applying a critical source — never the specific rotating sources themselves. Students access the actual sources via their teacher.",
        "director_year_country": "n/a",
        "major_characters": ["see set US independent film options — Juno, Whiplash, Lady Bird, The Hurt Locker, The Hate U Give"],
        "major_themes": [
            "what a film review does (evaluative judgement, specialist vocabulary)",
            "what film criticism does (interpretation and argument)",
            "what writing on cinematography does (technical analysis)",
            "applying a source — quote a fragment, name the writer, use it to support analysis of a moment",
            "auteur theory as a critical lens (Sarris, Truffaut etc. as historical reference)",
            "specialist film vocabulary in extended writing",
        ],
        "production_context": "The Eduqas/WJEC specification rotates the set sources every three years. They are confidential to enrolled centres. Generic published critical writers students may legitimately encounter as REFERENCE POINTS only — Pauline Kael (New Yorker), Roger Ebert (Chicago Sun-Times), Mark Kermode (Observer), Manohla Dargis (NYT), David Bordwell (academic). Free-tier work mentions these critics by name as orientation, never reproduces their copyrighted text.",
        "critical_reception": "The lesson teaches the application skill, not specific source content. Worked examples use clearly fictional or generic sample sentences, e.g. 'imagine a critic writes that Chazelle directs sound the way other directors direct light — you would apply this idea by...'.",
        "filmic_methods": [
            "five US independent set films are eligible for source-application practice — see individual film briefs",
            "the lesson teaches: identify the source's argument, quote a fragment, apply to a named sequence",
            "indie aesthetic terms (mumblecore, slow cinema, festival circuit, specialty division) used precisely",
        ],
        "key_scenes_for_micro_analysis": [
            "see individual set US independent films — the lesson uses worked examples drawn from those films",
        ],
        "most_relevant_film_theory": [
            "auteur theory (Sarris and Truffaut as historical reference)",
            "evaluative criticism as a mode (Kael, Ebert as historical reference)",
            "academic film writing as a register (Bordwell as historical reference)",
        ],
        "copyright_status": "The skill is teachable WITHOUT reproducing copyrighted sources. Use only generic exemplar fragments.",
    },
}


def make_subject_brief(plan: dict) -> dict:
    """Subject-level teaching brief that every batch carries verbatim."""
    return {
        "common_misconceptions": plan["teaching_brief"]["common_misconceptions"],
        "student_errors_by_question_type": plan["teaching_brief"][
            "student_errors_by_question_type"
        ],
        "topic_weighting_notes": plan["teaching_brief"]["topic_weighting_notes"],
        "current_spec_changes": plan["teaching_brief"]["current_spec_changes"],
        "pedagogical_notes": plan["teaching_brief"]["pedagogical_notes"],
        "film_content_rules": plan["teaching_brief"]["film_content_rules"],
        "studyvault_mark_scheme_rules": {
            "rubric_tiers": ["Mastering", "Secure", "Developing", "Emerging"],
            "do_not_use": [
                "Level 1 / Level 2 / Level 3 / Level 4",
                "Award N marks for ... (banned phrasing — validator hard-fail)",
                "Nothing worthy of credit",
                "Eduqas/WJEC verbatim mark scheme stems",
                "Section A / Section B / Section C labels in user-facing strings",
                "Component 1 / Component 2 / Component 3 in user-facing strings",
                "C670QS / 3670QS spec codes in user-facing strings",
            ],
            "use_instead": [
                "1 mark for X; 1 mark for Y (for short-answer questions)",
                "Up to N marks: ... (for short-answer with multiple credit points)",
                "Mastering tier (top): describes what the strongest answer shows",
                "Secure tier: describes a solid answer",
                "Developing tier: describes a partial answer",
                "Emerging tier (bottom): describes a minimal answer",
            ],
            "micro_macro_lens_required": (
                "For 8/10/15/25-mark questions, the mark scheme MUST require the candidate "
                "to link a specific MICRO choice (a named shot type, edit, lighting state or "
                "sound design choice) to a MACRO meaning (theme, narrative function, "
                "representation, genre convention or context). Pure thematic analysis is "
                "insufficient; pure technique-spotting is insufficient."
            ),
        },
        "glossary_target": (
            "Six or more glossary terms per lesson, embedded inline as <dfn class=\"term\" "
            "data-def=\"...\">. Film Studies is technical-vocabulary heavy "
            "(cinematography, mise-en-scene, editing, sound, narrative, genre, representation, theory) "
            "so this is easy to hit; aim for 6–10 per lesson. Do not pad with non-film terms."
        ),
        "flashcard_rules": (
            "Eight to fifteen flashcards per lesson. Each answer must be ONE fact, not an enumeration. "
            "Bad: 'The five micro-features are cinematography, mise-en-scene, editing, sound and narrative.' "
            "Good: split into separate cards. Film-specific card types: term ↔ definition (diegetic, jump cut, "
            "frame narrative); director ↔ year/country/film; film ↔ named sequence; theorist ↔ idea (Mulvey — "
            "what is the gaze?); genre ↔ convention; technological development ↔ year (Toy Story — what year? 1995)."
        ),
        "plain_text_fields_rule": (
            "Plain unicode characters only in description, practice_questions[].text/.type/.marks, "
            "knowledge_checks[].q, flashcard_questions[].q/.a, glossary_terms[].term/.definition. "
            "NEVER HTML entities (&rsquo;, &amp;, &ldquo;, &mdash;) — these are blocked by the validator. "
            "HTML entities are only acceptable inside content_html and other _html-suffixed fields."
        ),
    }


# Batch definitions — (batch_id, unit_index, lesson_numbers, unit_brief_dict)
# unit_index is 0-based into plan["article_units"].

def unit_brief_for(unit_slug: str, lesson_numbers: list[int]) -> dict:
    """Return the unit_level_teaching_brief for a given unit + lesson range."""
    if unit_slug == "film-form-and-language":
        return {
            "what_students_should_remember": [
                "The micro-toolkit (cinematography / mise-en-scene / editing / sound) is the spine of every set-film answer. Lessons 1-4 build this toolkit.",
                "The macro-toolkit (narrative / genre / representation / context) is layered onto micro analysis in Lessons 5-7.",
                "Every term introduced here will be re-applied in Units 2-4 to specific set films. Glossary precision matters.",
            ],
            "common_misconceptions_for_unit": [
                "Students confuse types of cut (cut, dissolve, fade, jump cut, match cut) — the unit must drill these distinctions.",
                "Students treat 'mise-en-scene' as just 'set design' and forget costume, props, lighting and performance also belong inside the term.",
                "Students mis-apply theory — they describe Todorov in the abstract instead of pointing to a moment of equilibrium / disruption / new equilibrium.",
                "Students treat 'genre' and 'narrative' as interchangeable — the unit must distinguish them.",
            ],
            "unit_focus": "Toolkit unit — universal film language, applied later to specific set films. Worked examples may draw on famous public-knowledge films at illustrative level (no plot reproduction, no quotation > 15 words).",
        }
    if unit_slug == "developments-in-film-technology":
        return {
            "what_students_should_remember": [
                "Six historical anchor points: 1895 first moving images (Lumiere), 1927 synchronised sound (Jazz Singer), 1935 three-strip Technicolor (Becky Sharp), 1948 Paramount decree, 1975 Steadicam (Garrett Brown), 1995 first computer-generated feature (Toy Story).",
                "The 2018 Eduqas/WJEC timeline extension added 1995–2018 — Toy Story, Tangerine (2015 iPhone-shot), Netflix (2007), streaming-overtakes-DVD (2017), Avengers: Infinity War (2018, IMAX-shot).",
                "This unit carries only 5 of 70 marks on Component 1 and rewards short factual recall — do not over-write extended-essay answers here.",
            ],
            "common_misconceptions_for_unit": [
                "Students confuse the dates of CinemaScope (1953) and the Paramount decree (1948).",
                "Students attribute Steadicam to a studio rather than to inventor Garrett Brown.",
                "Students forget that Toy Story (1995) was the first feature-length computer-generated animated film, not the first film with computer-generated imagery.",
                "Students treat 'IMAX' and 'IMAX-shot' as interchangeable — Avengers: Infinity War was the first major fiction feature shot entirely on IMAX cameras.",
            ],
            "unit_focus": "Short factual recall on a chronological timeline. Worked examples are technological developments anchored to year, name, country and one consequence.",
        }
    if unit_slug == "us-mainstream-comparative":
        # Unit 2 lessons:
        # L1 = Hollywood institutional (no set film)
        # L2-L6 = each pair
        # L7 = comparative method (no specific pair)
        briefs = {
            "set_films_covered": [],
            "what_students_should_remember": [
                "Each comparative pair sits in one genre — horror, musical, romantic comedy, teen film, science fiction.",
                "The comparative method is matched-moment-then-named-difference-then-contextual-reason. Two parallel single-film descriptions are not a comparison.",
                "Section A carries 50 of 70 marks on Component 1 — the unit's most rehearsed material.",
            ],
            "common_misconceptions_for_unit": [
                "Students write two parallel descriptions instead of an explicit comparative line.",
                "Students rely on plot-recall rather than named-sequence micro-analysis.",
                "Students miss the contextual reason for the difference between the two films (1930s/50s versus 1970s/80s).",
            ],
            "unit_focus": "Five comparative pairs, one per lesson 2-6; institutional and comparative-method bookends in lessons 1 and 7.",
        }
        # Add per-pair film briefs only for the pairs covered in this batch's lesson range
        pair_lookup = {
            2: ("dracula-1931", "lost-boys-1987"),
            3: ("singin-in-the-rain-1952", "grease-1978"),
            4: ("pillow-talk-1959", "when-harry-met-sally-1989"),
            5: ("rebel-without-a-cause-1955", "ferris-buellers-1986"),
            6: ("body-snatchers-1956", "et-1982"),
        }
        for n in lesson_numbers:
            for film_key in pair_lookup.get(n, ()):
                briefs["set_films_covered"].append(SET_FILM_BRIEFS[film_key])
        return briefs
    if unit_slug == "us-independent":
        briefs = {
            "set_films_covered": [],
            "what_students_should_remember": [
                "AO2 is weighted higher than AO1 in the extended-writing question on the US independent film — analytical depth on micro-features matters more than plot recall.",
                "Specialist writing on film rotates every three years and is not on this platform — the lesson teaches the SKILL of applying a critical source generically.",
                "Indie-cinema institutional context (Sundance, Miramax, A24, Fox Searchlight, Sony Pictures Classics, specialty divisions) anchors AO1.",
            ],
            "common_misconceptions_for_unit": [
                "Students summarise a critical source instead of applying it to a specific moment of the chosen film.",
                "Students treat 'indie' as a stylistic label rather than an industrial category — independent of which studio?",
                "Students miss the difference between 'studio indie' (Fox Searchlight, Focus Features, Sony Pictures Classics) and fully independent production (true Sundance early-career).",
            ],
            "unit_focus": "Five US independent set films plus a specialist-writing skill lesson. The 25-mark Extended Essay form is the unit's signature.",
        }
        film_lookup = {
            1: [],  # institutional / overview
            2: ["juno-2007"],
            3: ["whiplash-2014"],
            4: ["lady-bird-2017"],
            5: ["hurt-locker-2008", "hate-u-give-2018"],
            6: ["specialist-writing-context"],
        }
        for n in lesson_numbers:
            for film_key in film_lookup.get(n, []):
                briefs["set_films_covered"].append(SET_FILM_BRIEFS[film_key])
        return briefs
    if unit_slug == "global-film":
        briefs = {
            "set_films_covered": [],
            "what_students_should_remember": [
                "Three focus areas across the unit: NARRATIVE (global English-language), REPRESENTATION (global non-English-language), AESTHETIC (contemporary UK).",
                "Component 2 splits its 70 marks roughly evenly across the three sections — lesson allocation is balanced.",
                "Each set-film slate is a five-option pick — students study one of the five per section. Wide coverage at lesson level rather than depth on a single text.",
            ],
            "common_misconceptions_for_unit": [
                "Students confuse the focus areas — narrative becomes representation becomes aesthetic.",
                "Students retell the plot of their chosen film rather than apply the focus area to specific named sequences.",
                "Students treat global non-English-language film as a single category rather than recognising the cultural specificity of each option.",
            ],
            "unit_focus": "Five lessons covering three focus areas across the global-film slate. Worked examples draw on representative options (Slumdog for narrative, Wadjda + Girlhood for representation, the five UK options for aesthetic).",
        }
        film_lookup = {
            1: ["global-english-context"],
            2: ["slumdog-2008"],
            3: ["global-non-english-context"],
            4: ["wadjda-2012", "girlhood-2014"],
            5: ["uk-film-context"],
        }
        for n in lesson_numbers:
            for film_key in film_lookup.get(n, []):
                briefs["set_films_covered"].append(SET_FILM_BRIEFS[film_key])
        return briefs
    raise ValueError(f"Unknown unit slug: {unit_slug}")


def determine_spec_slice(unit_slug: str) -> str:
    if unit_slug in ("film-form-and-language", "developments-in-film-technology"):
        return "scripts/_content_film-studies-eduqas/_spec_universal.txt"
    return "scripts/_content_film-studies-eduqas/_spec_set-films.txt"


def make_batch(plan: dict, batch_id: str, unit_idx: int, lesson_numbers: list[int]) -> dict:
    unit = plan["article_units"][unit_idx]
    lessons = [l for l in unit["lessons"] if l["number"] in lesson_numbers]
    # Build the lessons_in_batch shape — strip section_markers, derive slug from Supabase-known list.
    # Slugs are pre-confirmed against Supabase (see _PREP_REPORT.md).
    slug_lookup = {
        "film-form-and-language": {
            1: "cinematography-shot-angle-movement-and-lighting",
            2: "mise-en-scene-setting-costume-props-make-up",
            3: "editing-cuts-continuity-pace-and-visual-effects",
            4: "sound-diegetic-non-diegetic-score-and-sound-bridges",
            5: "narrative-structure-plot-story-and-three-act-form",
            6: "genre-representation-and-spectatorship",
            7: "contexts-of-film-social-cultural-historical-political-institutional",
        },
        "us-mainstream-comparative": {
            1: "hollywood-then-and-now-studio-system-to-modern-blockbuster",
            2: "dracula-and-the-lost-boys-vampires-across-eras",
            3: "singin-in-the-rain-and-grease-the-hollywood-musical",
            4: "pillow-talk-and-when-harry-met-sally-the-romantic-comedy",
            5: "rebel-without-a-cause-and-ferris-buellers-day-off-teen-rebellion",
            6: "invasion-of-the-body-snatchers-and-et-aliens-and-anxiety",
            7: "comparing-films-genre-narrative-context-side-by-side",
        },
        "us-independent": {
            1: "what-is-american-independent-cinema",
            2: "juno-tonal-comedy-and-the-indie-voice",
            3: "whiplash-cutting-sound-and-pursuit-of-greatness",
            4: "lady-bird-coming-of-age-and-greta-gerwigs-direction",
            5: "the-hurt-locker-and-the-hate-u-give-issue-led-indies",
            6: "specialist-writing-on-film-reviews-theory-cinematography",
        },
        "global-film": {
            1: "global-english-language-film-narrative-in-focus",
            2: "analysing-narrative-slumdog-millionaire-and-frame-devices",
            3: "global-non-english-language-film-representation-in-focus",
            4: "analysing-representation-wadjda-girlhood-and-power",
            5: "contemporary-uk-film-aesthetic-style-in-focus",
        },
        "developments-in-film-technology": {
            1: "silent-cinema-to-sound-1895-1935",
            2: "widescreen-steadicam-and-the-push-for-spectacle-1948-1990s",
            3: "digital-streaming-and-citizen-cinema-1995-2018",
        },
    }
    suggested_question_types_per_lesson = {
        # Unit 1: toolkit weighting
        "film-form-and-language": {
            1: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            2: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            3: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            4: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            5: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            6: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
            7: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis"],
        },
        # Unit 2: comparative weighting
        "us-mainstream-comparative": {
            1: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "15 marks — Compare and Contrast"],
            2: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            3: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            4: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            5: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            6: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            7: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
        },
        # Unit 3: extended-essay weighting
        "us-independent": {
            1: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            2: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            3: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            4: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            5: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "15 marks — Compare and Contrast", "25 marks — Extended Essay"],
            6: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "25 marks — Extended Essay"],
        },
        # Unit 4: balanced
        "global-film": {
            1: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "25 marks — Extended Essay"],
            2: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            3: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element", "25 marks — Extended Essay"],
            4: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
            5: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "10 marks — Micro-Analysis", "25 marks — Extended Essay"],
        },
        # Unit 5: short factual weighting
        "developments-in-film-technology": {
            1: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element"],
            2: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element"],
            3: ["1 mark — Identify", "2 marks — Define", "5 marks — Explain Effect", "8 marks — Analyse Filmic Element"],
        },
    }

    out_lessons = []
    for l in lessons:
        out_lessons.append({
            "number": l["number"],
            "title": l["title"],
            "slug": slug_lookup[unit["slug"]][l["number"]],
            "description": l["description"],
            "spec_references": l["spec_references"],
            "section_markers": l["section_markers"],
            "suggested_question_types": suggested_question_types_per_lesson[unit["slug"]][l["number"]],
        })

    batch = {
        "batch_id": batch_id,
        "subject": {
            "name": "Film Studies",
            "slug": "film-studies-eduqas",
            "exam_board": "Eduqas",
            "target_audience": "free-tier",
        },
        "unit": {
            "name": unit["name"],
            "slug": unit["slug"],
            "subtitle": unit["subtitle"],
            "accent": unit["accent"],
            "accent_light": unit["accent_light"],
            "accent_badge": unit["accent_badge"],
            "body_class": unit["body_class"],
            "lesson_count": unit["lesson_count"],
        },
        "spec_slice_path": determine_spec_slice(unit["slug"]),
        "reference_lesson_path": "scripts/_content_film-studies-eduqas/_reference_lesson.json",
        "subject_level_teaching_brief": make_subject_brief(plan),
        "unit_level_teaching_brief": unit_brief_for(unit["slug"], lesson_numbers),
        "quote_ticker_html_for_unit": QUOTE_TICKER_HTML,
        "registered_question_type_names": list(REGISTERED_QUESTION_TYPE_NAMES),
        "allowed_question_types_for_this_unit": list(ALLOWED_FOR_ALL_UNITS),
        "lessons_in_batch": out_lessons,
        "output_dir": "scripts/_content_film-studies-eduqas/lessons",
    }
    return batch


# Batch plan: 8 batches, 28 lessons total
BATCH_DEFS = [
    # Unit 1 (7 lessons): 3 + 4
    ("film-form_b1", 0, [1, 2, 3]),
    ("film-form_b2", 0, [4, 5, 6, 7]),
    # Unit 2 (7 lessons): 3 + 4
    ("us-mainstream_b1", 1, [1, 2, 3]),
    ("us-mainstream_b2", 1, [4, 5, 6, 7]),
    # Unit 3 (6 lessons): 3 + 3
    ("us-indie_b1", 2, [1, 2, 3]),
    ("us-indie_b2", 2, [4, 5, 6]),
    # Unit 4 (5 lessons): 1 batch
    ("global-film_b1", 3, [1, 2, 3, 4, 5]),
    # Unit 5 (3 lessons): 1 batch
    ("developments_b1", 4, [1, 2, 3]),
]


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_lessons = 0
    written = []
    for batch_id, unit_idx, lesson_numbers in BATCH_DEFS:
        batch = make_batch(plan, batch_id, unit_idx, lesson_numbers)
        path = OUT_DIR / f"_batch_{batch_id}.json"
        path.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
        written.append(path)
        total_lessons += len(batch["lessons_in_batch"])
        print(f"WROTE {path.name} ({len(batch['lessons_in_batch'])} lessons)")
    print(f"\nTotal: {len(written)} batches, {total_lessons} lessons")


if __name__ == "__main__":
    main()
