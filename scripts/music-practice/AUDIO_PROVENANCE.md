# Music AQA — Hosted Audio Provenance Ledger

Every real recording hosted on R2 for music-aqa, with licence evidence.
Rule (hard-won 6 Aug 2026): verify the RECORDING's licence, not just the
composition's; verify audio CONTENT matches the catalogue claim (one sourced
item was nearly shipped on metadata alone); CC BY-SA is excluded; synthesised
audio is never used for timbre-identification questions.

## AoS3 blues — LIVE in aos-listening L2 + AoS3 article (added 7 Aug 2026)

| R2 file (music-aqa/aos-listening/) | Recording | Licence basis | Evidence |
|---|---|---|---|
| aos3_rainey_seeseerider.mp3 | Ma Rainey, "See See Rider Blues", rec. 16 Oct 1924, Paramount 12252 (Louis Armstrong, cornet) | Item CC0; recording US PD (MMA, 1 Jan 2025) + UK PD (pre-1963 term expiry); composition Rainey d. 1939 | https://archive.org/details/JV-1265-1924-QmQei6ftSXLGJymA5Chd5NjBE8z1scKdPuTUnWckrr8T3Z.mp3 |
| aos3_smith_dixieflyer.mp3 | Bessie Smith, "Dixie Flyer Blues", rec. 15 May 1925, Columbia 14079-D | Item CC0; recording US PD (1 Jan 2026) + UK PD; composition Smith d. 1937 | https://archive.org/details/JV-1628-1925-QmThndipy3imoNMcPgWiipTCkNBTqmaKCmmRWtKAupjQ7j.mp3 |
| aos3_blythe_chicagostomp.mp3 | Jimmy Blythe, "Chicago Stomp", rec. Apr 1924, Paramount 12207 | Item CC0; recording US PD (1 Jan 2025) + UK PD; composition Blythe d. 1931 | https://archive.org/details/JV-980-1924-QmX3HouVVhfWkmi8HJKYncqYAFMaR2jXhmMEpAia8fNCvQ.mp3 |

Content authenticity verified 7 Aug 2026 by lyric-transcription probe
(See See Rider letter verse; Dixie Flyer train lyrics; Blythe instrumental).
Excerpts ~22s, loudnorm I=-17, fades.

## Family drill (Listening Skills L2) — LIVE roster, 7 Aug 2026

All machine-ear corroborated (>=2/3 blind votes). Woodwind: fam_flute_mozart
(Mozart K.313, Musopen PD-author), fam_clarinet_joergensmann (VRT-ticketed PD
release, 2008), fam_oboe_albinoni (Musopen CC0, Paul Arden-Taylor). Strings:
fam_violin_bach (CC0 2014), real_cello_bach (CC0 2024), fam_strings_afband
(USAF, 17 USC 105). Brass: fam_bugle_taps (USMC), fam_brass_heralds (US Army
Herald Trumpets), fam_trumpet_taps_af (USAF) — all 17 USC 105. Percussion:
fam_mallets_fleet (US Pacific Fleet Band xylophone+marimba, 17 USC 105),
exF08 constructed timpani (RULE REFINEMENT: synth allowed for timbre-ID only
when machine-corroborated — exF08 passed 3/3; no licence-clean real timpani
exists (best candidate was CC BY-SA)).

PIPELINE RULES (paid for in blood, 7 Aug): (1) ffmpeg INPUT-seek (-ss before
-i) when combining seek with fades — output-side seek applied fades on source
timestamps and silently produced silence for any window past ~21s; this also
hit 2 of 3 shipped blues clips (refixed). (2) Never upload a clip without
measuring its OUTPUT RMS (> -35dB). (3) Gemini hallucinates confident answers
on silent audio — a FLAG can mean broken clip, not wrong content; describe-
probe before concluding. (4) Trust no sourced window claim: scan RMS first.

## Acoustic-era instrument discs — PARKED (unfit for family drilling)

Eleven clips at music-aqa/listening-skills/real_*.mp3 (Henneberg flute 1916,
McNeice clarinet 1911, Mazziotta flute 1901, Heifetz violin 1917, CC0 Bach
cello 2024, Apituley viola CC BY 3.0, Pryor trombone 1904, Kryl cornet 1918,
Buono cornet 1922, Francisco xylophone 1908, Mills xylophone 1906). Licence
evidence in the 7 Aug sourcing report (session transcript). VERDICT: the
acoustic-era discs are too band-limited for fair family identification —
machine-ear cannot corroborate them and students should not be graded on
100-year-old narrowband timbre. Keep for possible context/history use. The
family drill needs MODERN clean licence-free recordings (US military band
recordings = federal PD are the recommended source). Until then L2 runs on
the balanced synthesised bank and MUST NOT be approved live.

## AoS2-4 verified excerpt bank (aos2_*, aos3_*, aos4_* at music-aqa/aos-listening/)

Flow-generated (ear-verified by Tom + gates) and PD orchestral excerpts
(Gershwin/Prokofiev/Respighi — see reference_aos4_licence_clean_audio memory).

## Constructed clips (listening-skills demos + drills, exT/exF/ex0 series)

FluidSynth + FluidR3_GM renders of our own notation — no third-party rights.
Valid for pitch-domain facts only (tonality, cadence, metre), never timbre ID.

## AoS1 works recordings — PROVENANCE SOLVED by duration matching (7 Aug)

All 8 identified to the millisecond. lesson-01 Beethoven = US Marine Band 2019
(17 USC 105). mozart-40 = Musopen Symphony 2012 (PD-author). lesson-03 Rondo:
WAS ibiblio CC BY-SA 2.0 — REPLACED with Krumpoeck/Merkur Orchester 1999 under
its CC BY 2.5 multi-licence option; credit in drill passage; character/window
re-verified. lesson-04 Haydn = Koussevitzky/BSO 1929, PD-EU-audio (US-PD
2030 — accepted posture, review before any US-market push). lesson-05 Zadok =
St Matthew's Concert Choir 2013 CC BY 3.0 — attribution now displayed in the
drill. lesson-06 Chopin = Musopen Frank Levy (PD). lesson-07/07b Kinderszenen
= Musopen set (PD, VRT ticket). lesson-08 Verdi: REPLACED 7 Aug with Fricsay/RIAS 1954 (DG), IMSLP tag
'Public Domain - Non-PD US' — UK/EU PD, same posture as the Haydn (both are
the accepted UK-exposure items to revisit before any US-market push).
Content probe confirmed the Dies irae; credit displayed in the drill.

## (superseded note)

Real recordings, multi-MB, ID3 stripped at re-encode; provenance records
absent (predate this regime). Compositions PD; the RECORDINGS' licences are
unverified. OPEN ITEM: Tom to decide accept vs re-source (Musopen).
