"""Upload related_media for history-ocr Units 9-12 directly via Supabase service key.

Units covered:
- war-british-society-790-2010 (L1-L10)
- impact-empire-britain-1688-1730 (L1-L10)
- english-reformation-1520-1550 (L1-L10)
- personal-rule-restoration-1629-1660 (L1-L10)

Usage:
    python scripts/_insert_history_ocr_units9_12_related_media.py
    python scripts/_insert_history_ocr_units9_12_related_media.py --dry-run
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()

# Lesson ID -> related_media list
LESSON_MEDIA = {

    # ============================================================
    # UNIT 9: WAR & BRITISH SOCIETY 790-2010
    # ============================================================

    # L1: Viking raids on Anglo-Saxon England 790-1066
    "c58c5812-7ced-4c9e-9c2f-8b83bb14059f": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l01.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/gone-medieval/episodes/vikings", "title": "Gone Medieval — Vikings", "description": "Matt Lewis examines what the Vikings actually wanted when they raided England, and why Lindisfarne 793 marked a new era."},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Hundred Years War", "description": "Background on the Anglo-Saxon military tradition that the Vikings first disrupted — useful thematic context."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=p46RDqyogFc", "title": "The Vikings in Britain and Ireland: An Overview", "description": "Clear overview of Viking raiding, settlement and integration from the first raids to Cnut’s kingdom."},
            {"url": "https://www.youtube.com/watch?v=UGbdnhUkXDI", "title": "Anglo-Saxon Revenge — Vikings in Britain (Part 4)", "description": "Follows the Viking campaigns and Alfred the Great’s resistance — the military-society relationship at the heart of this thematic study."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/vikings", "title": "Vikings (2013–20)", "description": "Dramatisation of the Viking raids on Anglo-Saxon England via Ragnar Lothbrok — atmospheric if not always accurate on detail."},
            {"url": "https://www.justwatch.com/uk/tv-series/the-last-kingdom", "title": "The Last Kingdom (2015–22)", "description": "Set during Alfred the Great’s wars against the Danes — captures the experience of Viking invasion and Anglo-Saxon defence."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (Schools History Project)", "description": "Hub for the full OCR SHP specification — use it to check the thematic study sub-bullets."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B (Schools History Project) Specification", "description": "Official OCR J411 specification — download for the exact key concepts and assessment objectives."}
        ]}
    ],

    # L2: Norman conquest and feudal warfare 1066-1215
    "3f913622-3e17-4e60-8e4f-5fefac8ab5a1": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l02.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://podcasts.apple.com/us/podcast/the-battle-of-cr%C3%A9cy/id1564113746?i=1000703456065", "title": "Gone Medieval — The Battle of Crécy", "description": "History Hit on how the longbow and the lessons of Hastings shaped English warfare."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=OJoovrGWcl0", "title": "Eleanor Janega on 1066 and the Norman Conquest", "description": "Medieval historian Eleanor Janega explains the military innovation the Normans brought to England."},
            {"url": "https://www.youtube.com/watch?v=nhIP6dfr_FE", "title": "Modern History TV — The Evolution of Knightly Armour 1066–1485", "description": "Walks through how cavalry warfare and plate armour developed after the Conquest."},
            {"url": "https://www.youtube.com/watch?v=gkPJ5ncikZ0", "title": "How the Normans Ruthlessly Conquered the Anglo-Saxons", "description": "Explores the speed and brutality of the Norman pacification — how war reshaped English society from 1066."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/braveheart", "title": "Braveheart (1995)", "description": "Mel Gibson’s epic on feudal warfare and resistance — captures the cavalry tactics introduced after the Norman Conquest."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (Schools History Project)", "description": "Hub page for the full specification — navigate to War & British Society for the Norman period content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Download the J411 spec to check which aspects of Norman feudal warfare are assessed."}
        ]}
    ],

    # L3: Late medieval warfare c.1290-c.1450
    "dda04649-069d-44ad-aeff-938de3400f24": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l03.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://podcasts.apple.com/us/podcast/the-battle-of-cr%C3%A9cy/id1564113746?i=1000703456065", "title": "Gone Medieval — The Battle of Crécy", "description": "Matt Lewis on how the English longbow dismantled French cavalry at Crécy 1346 — the central technological shift of late medieval warfare."},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Hundred Years War", "description": "Overview of the long English-French conflict that drove tactical evolution from Crécy to Agincourt."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=DBxdTkddHaE", "title": "Tod’s Workshop — Arrows vs Armour: Medieval Myth Busting", "description": "Practical test of whether a 160 lb war-bow could pierce 15th-century armour — directly relevant to the longbow revolution."},
            {"url": "https://www.youtube.com/watch?v=JjbY6rZsQlg", "title": "Dan Snow Explains: The Battle of Agincourt", "description": "Ten-minute explainer on the 1415 battle — mud, the archer’s role and why the outnumbered English won."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/henry-v", "title": "Henry V (1989)", "description": "Kenneth Branagh’s gritty Shakespeare on Agincourt — the longbow volley and the archers’ stake formation shown vividly."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://royalarmouries.org/stories/our-collection/longbows-of-agincourt/", "title": "Royal Armouries — The longbows of Agincourt", "description": "The national collection’s deep-dive on the Mary Rose longbows — draw weights, range, and battlefield impact."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "Hub page for the full OCR specification — navigate to War & British Society for the medieval warfare content."}
        ]}
    ],

    # L4: Elizabeth, Spain and the new world
    "fe00a85c-69cf-44bc-81f5-962e49ccc73d": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l04.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Elizabeth I and Mary, Queen of Scots", "description": "Suzannah Lipscomb on Elizabeth’s legitimacy crisis and the threat from Catholic Europe — the background to the Armada."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=YUKD59cJoIA", "title": "GCSE History: Why did Philip II launch the Spanish Armada?", "description": "Clear exam-oriented explainer on Spanish motivations and the strategic stakes of 1588."},
            {"url": "https://www.youtube.com/watch?v=eVnYXsXgwXs", "title": "Drake and Cadiz (The EverLearner)", "description": "Covers Drake’s ‘singeing the king of Spain’s beard’ and how English naval aggression escalated to full war."},
            {"url": "https://www.youtube.com/watch?v=2CFTbeuIRes", "title": "The Spanish Armada 1588 — History GCSE", "description": "Straightforward 10-minute revision video on the Armada campaign and its impact on Elizabethan warfare."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/elizabeth", "title": "Elizabeth (1998)", "description": "Cate Blanchett’s portrayal of Elizabeth’s early reign — the political context for England’s confrontation with Spain."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "Hub for the OCR specification — useful summary notes on the Elizabethan wars and naval power."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official spec — check the exact key concepts for the Elizabethan period in War & British Society."}
        ]}
    ],

    # L5: Border warfare c.1500-c.1600
    "e1b1b5f2-517b-4301-8e5c-1bcd39f256ad": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l05.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Elizabeth I and Mary, Queen of Scots", "description": "The political context for border warfare — the Anglo-Scottish relationship and the threat from the north."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=oaS5m11eVGA", "title": "Exam Skills Live: Elizabeth’s Accession in 1558 (tutor2u)", "description": "The problems Elizabeth faced from Scotland and France on accession — the strategic backdrop for the border campaigns."},
            {"url": "https://www.youtube.com/watch?v=_tD3KvqCc8g", "title": "Early Elizabethan England 1558–1588: Threats to the Settlement", "description": "Covers the northern threat from Scotland and France that shaped border military policy in the early Tudor period."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/braveheart", "title": "Braveheart (1995)", "description": "Set in the period of Scottish-English border conflict — captures the guerrilla warfare and reiver culture that made the borders distinctive."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/the-last-kingdom", "title": "The Last Kingdom (2015–22)", "description": "Shows the origins of the Anglo-Scottish borderland in the contested kingdoms of the north — useful backdrop to Tudor border policy."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub page — navigate to War & British Society for the Tudor border warfare content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 specification for checking the exact assessment requirements for this period."}
        ]}
    ],

    # L6: Civil Wars in England, Scotland and Ireland 1642-1651
    "52b1dc4f-b65f-4e97-aced-459e91874060": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l06.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Hundred Years War", "description": "Background on the evolving British military tradition — context for the constitutional issues that the Civil Wars brought to a head."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "How the New Model Army’s professional structure changed English warfare — the key military innovation of the Civil War period."},
            {"url": "https://www.youtube.com/watch?v=FZoyt6UA3TE", "title": "Naseby: The Grim Battle That Decided The English Civil War", "description": "Step-by-step account of the 1645 battle — how cavalry, infantry and artillery combined under New Model Army command."},
            {"url": "https://www.youtube.com/watch?v=_CmIvXGCBco", "title": "Pike & Shot Warfare: The Musket and the Transformation of Battle", "description": "Explains the tactical revolution of pike-and-musket formations — the weapon system at the heart of Civil War battles."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Richard Harris as Cromwell — dramatises the New Model Army and the battles that defined the British Civil Wars."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Newark’s dedicated Civil War museum — collections, resources and interpretation of how war affected British society 1642–51."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to War & British Society for Civil War content and revision notes."}
        ]}
    ],

    # L7: Jacobite rebellions and imperial wars
    "282c10a7-f009-4845-8867-92e721e064c4": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l07.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Hanseatic League (BBC Radio 4)", "description": "Melvyn Bragg on the European trading networks that Britain’s imperial expansion would eventually displace."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=Ut5gtrezN4E", "title": "Black British History We’re Not Taught in Schools (BBC Stories)", "description": "Explainer on the long history behind Britain’s imperial expansion — the early empire’s impact on British society."},
            {"url": "https://www.youtube.com/watch?v=JfTaXRFV7EA", "title": "Black Tudors: Three Untold Stories — Gresham College", "description": "How early imperial contact with West Africa preceded the Jacobite era — useful backdrop on who served in Britain’s growing forces."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-man-who-would-be-king", "title": "The Man Who Would Be King (1975)", "description": "John Huston’s adventure on British imperial soldiers in Afghanistan — evokes the individual experience of imperial warfare."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/horrible-histories", "title": "Horrible Histories (2009–)", "description": "CBBC comedy — the Jacobite and Hanoverian episodes explain the dynastic wars behind the imperial period in accessible style."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub page — use for War & British Society revision on the 18th-century campaigns."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official OCR J411 spec — check the key concepts for the Jacobite and imperial war period."}
        ]}
    ],

    # L8: Napoleonic wars and Victorian imperial conflicts
    "5bc26dab-49bf-43c0-8926-53f91367c94d": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l08.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Hundred Years War", "description": "Background on the long Anglo-French military rivalry that culminated in the Napoleonic Wars."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=nDZGL1xsqzs", "title": "Napoleonic Wars: Battle of Waterloo 1815", "description": "The decisive battle — infantry squares, cavalry charges and the Duke of Wellington’s defensive tactics in detail."},
            {"url": "https://www.youtube.com/watch?v=hmfeEeophSg", "title": "Balaclava 1854 (Light Brigade) — History of Warfare", "description": "The Crimean War cavalry disaster that exposed the failures of Victorian aristocratic command — a key case study in reform."},
            {"url": "https://www.youtube.com/watch?v=c3y6ip22iF8", "title": "Extra History: Into the Valley of Death — The Crimean War", "description": "How the Crimean War’s press coverage transformed public attitudes to warfare and soldiers’ welfare."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/victoria-and-abdul", "title": "Victoria & Abdul (2017)", "description": "Judi Dench as Queen Victoria at the height of empire — shows the personal and political culture of Victorian imperial Britain."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "Hub page for OCR SHP — revision content on Napoleonic and Victorian warfare in the War & British Society unit."},
            {"url": "https://www.nam.ac.uk/", "title": "National Army Museum", "description": "The National Army Museum’s collection covers Waterloo, Crimea and Victorian imperial campaigns — free online resources."}
        ]}
    ],

    # L9: Two world wars and total war 1914-1945
    "f443b254-6011-4104-b7f9-9cddc79f6ac0": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l09.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Hundred Years War", "description": "Historical context on how British military culture evolved through centuries of conflict to produce the total war approach of 1914–18."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=GG0LY8OLBG8", "title": "World War One (All Parts) — Epic History", "description": "Comprehensive animated overview of WWI — technology, tactics and the transformation of British society under total war."},
            {"url": "https://www.youtube.com/watch?v=0HZLsrwDArw", "title": "GCSE History: WWI Recruitment, Conscription and Conditions", "description": "Specifically covers how the British army was raised — volunteers to conscripts — and what conditions soldiers faced."},
            {"url": "https://www.youtube.com/watch?v=E4mC4HdjJwQ", "title": "The Great Evacuation of 1939: Children Flee Britain", "description": "Total war’s impact on the home front — evacuation as a case study of how WWI lessons changed WWII civilian planning."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/1917", "title": "1917 (2019)", "description": "Sam Mendes’s real-time WWI drama — captures the technology, landscape and human cost of the Western Front total war."},
            {"url": "https://www.justwatch.com/uk/movie/testament-of-youth", "title": "Testament of Youth (2015)", "description": "Vera Brittain’s WWI memoir — the war that ended liberal optimism and made the case for total mobilisation of society."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.iwm.org.uk/", "title": "Imperial War Museum", "description": "IWM’s online collections, exhibitions and learning resources for both World Wars — authoritative and freely accessible."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to War & British Society for the twentieth-century total war content."}
        ]}
    ],

    # L10: Cold War, IRA and the wars on terror
    "3f5441a0-78c6-4108-b18f-0ce28c722d72": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/war-british-society-790-2010/podcast_l10.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — Cold War Conflicts", "description": "Overview of Britain’s Cold War military commitments and how they changed public attitudes to defence."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=pNYnhk_6YRY", "title": "The Invasion of Iraq 2003 — Complete Animated Documentary", "description": "Full animated breakdown of the 2003 invasion — technology, objectives and the British public’s response."},
            {"url": "https://www.youtube.com/watch?v=ggRom-hFnfM", "title": "Adapt and Overcome: The British Army in Iraq — IWM", "description": "Imperial War Museum film on British forces adapting counter-insurgency tactics in Basra."},
            {"url": "https://www.youtube.com/watch?v=4tm5hUhvSmM", "title": "Iraq War: Hearts and Minds — a very British tactic", "description": "Examines the distinctly British approach to winning over civilian populations — relevant to continuity and change in warfare since 1945."}
        ]},
        {"category": "Documentaries", "items": [
            {"url": "https://www.justwatch.com/uk/movie/michael-collins", "title": "Michael Collins (1996)", "description": "Neil Jordan’s film on the IRA campaign in the early 20th century — useful historical comparison for the Troubles module."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.iwm.org.uk/", "title": "Imperial War Museum", "description": "IWM collections covering Northern Ireland, Falklands, Gulf War and War on Terror — essential primary source resource."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — use the War & British Society section for post-1945 conflict revision content."}
        ]}
    ],

    # ============================================================
    # UNIT 10: IMPACT OF EMPIRE ON BRITAIN 1688-1730
    # ============================================================

    # L1: Glorious Revolution and the Hanoverian succession
    "740148c1-e8ce-4c49-8136-9b3181383c52": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l01.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Hanseatic League (BBC Radio 4)", "description": "Melvyn Bragg and historians on European commerce — the trading world that Britain’s Glorious Revolution aimed to protect."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=ldbZ1HnbRcQ", "title": "Henry VIII and the Break with Rome: Exploring England’s Reformation", "description": "Historical context — the religious settlement that the Glorious Revolution protected against Catholic restoration."},
            {"url": "https://www.youtube.com/watch?v=Ut5gtrezN4E", "title": "Black British History We’re Not Taught in Schools (BBC Stories)", "description": "How the commercial revolution of William III’s reign shaped British society and its engagement with empire."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-favourite", "title": "The Favourite (2018)", "description": "Olivia Colman as Queen Anne — set in the Hanoverian succession crisis and shows court politics in the exact period this lesson examines."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub for this specification — navigate to the Empire unit for Glorious Revolution context."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — download to check the key concepts for the Impact of Empire unit."}
        ]}
    ],

    # L2: Ireland 1688-1691 and the Jacobite threat
    "268da837-59c8-4f99-86cd-ef00246419cc": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l02.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Battle of the Boyne (BBC Radio 4)", "description": "Melvyn Bragg on the 1690 battle that confirmed William III’s Irish victory and shaped Protestant/Catholic relations for centuries."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=5uNMGzSL42U", "title": "The Great Famine — BBC 1995 (Part 1 of 2)", "description": "Background on Irish history — the religious and land tensions that the 1688-91 Williamite wars locked in place for 200 years."},
            {"url": "https://www.youtube.com/watch?v=xXyyQXAL8Po", "title": "The Famine Irish in Liverpool from Strokestown Park 1847", "description": "Traces how the Williamite land settlement drove the long chain of events leading to 19th-century Irish migration to Britain."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-wind-that-shakes-the-barley", "title": "The Wind That Shakes the Barley (2006)", "description": "Ken Loach’s Palme d’Or film on Irish resistance — the roots lie in the Williamite settlement this lesson examines."},
            {"url": "https://www.justwatch.com/uk/movie/michael-collins", "title": "Michael Collins (1996)", "description": "Liam Neeson as the independence leader — the Catholic Ireland that fought for freedom had been shaped by the 1691 defeat."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub page — navigate to the Impact of Empire unit for the Irish content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 specification — Ireland 1688-1691 assessment requirements."}
        ]}
    ],

    # L3: Scotland 1688-1715: Glencoe to Union
    "ca76a5bf-fc9d-4372-b5d6-71c4351884d6": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l03.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Act of Union 1707 (BBC Radio 4)", "description": "Melvyn Bragg and historians on why Scotland joined Great Britain in 1707 — economics, religion and the Jacobite threat."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=Gu4yOqdfStY", "title": "David Olusoga: Black British History and Belonging", "description": "Olusoga on how the 1707 Act of Union created a shared British identity that encompassed very different national histories."},
            {"url": "https://www.youtube.com/watch?v=5uNMGzSL42U", "title": "The Great Famine — BBC 1995", "description": "The Scottish clearances and Irish famine were the long-term consequences of a unification project that began at Glencoe."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/braveheart", "title": "Braveheart (1995)", "description": "Set 400 years earlier but captures the Scottish independence tradition that the Jacobites drew on — the emotional backdrop to the Union debates."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Impact of Empire unit for Scotland and Union content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — check the key concepts for Scotland in the Empire unit."}
        ]}
    ],

    # L4: Emigration from the British Isles
    "adbeeb0c-5ed6-4e80-b168-e09049753912": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l04.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The British Empire (BBC Radio 4)", "description": "How emigration shaped the empire — population movement from Scotland, Ireland and England to the Atlantic colonies."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=5uNMGzSL42U", "title": "The Great Famine — BBC 1995", "description": "The most dramatic episode of mass emigration in British history — the 1840s Irish famine saw two million leave in a decade."},
            {"url": "https://www.youtube.com/watch?v=I8Ax8RNxsmg", "title": "Irish Famine Lecture Series: Impact of Irish Refugees", "description": "How Irish emigration transformed British and American cities — useful context for long-term emigration patterns."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-wind-that-shakes-the-barley", "title": "The Wind That Shakes the Barley (2006)", "description": "Set in Ireland’s fight for independence — the population displacement and emigration the Williamite settlement began is this film’s deep background."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.ourmigrationstory.org.uk/", "title": "Our Migration Story (Runnymede Trust + Cambridge)", "description": "Award-winning teaching site on British emigration and immigration — directly useful for source-skills questions on population movement."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Empire unit for emigration content and revision notes."}
        ]}
    ],

    # L5: Bank of England, East India Company and the trade revolution
    "20153642-74c8-4e7d-809b-c0c40f2e169c": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l05.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The East India Company (BBC Radio 4)", "description": "Melvyn Bragg and historians on how the East India Company became the world’s most powerful commercial enterprise."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=UTn-ujN81Ds", "title": "Shaping the City: History of the Huguenots / Spitalfields Site", "description": "How Huguenot weavers brought commercial and banking expertise to England — directly connected to the financial revolution this lesson covers."},
            {"url": "https://www.youtube.com/watch?v=Gu4yOqdfStY", "title": "David Olusoga: Black British History and Belonging", "description": "Olusoga on how global trade transformed Britain’s racial and commercial profile — context for the East India Company’s social impact."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-lost-city-of-z", "title": "The Lost City of Z (2017)", "description": "A British explorer following the imperial trade routes of the 18th century — the ambition and danger of the commercial empire."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bankofengland.co.uk/museum/online-museum", "title": "Bank of England Museum — Online Collections", "description": "The Bank of England’s own account of its 1694 founding and early role in financing the empire and trade revolution."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — trade and empire content for this unit."}
        ]}
    ],

    # L6: Royal African Company and the slave economy
    "eda60c41-4419-4315-ba75-da24cc6d9249": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l06.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Slave Trade (BBC Radio 4)", "description": "Melvyn Bragg and leading historians on the transatlantic slave trade and its centrality to British commercial expansion 1688-1730."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=zQaF4BNY9LA", "title": "BBC4 — The Extraordinary Equiano (2005)", "description": "Documentary on Olaudah Equiano, the enslaved African who became an abolitionist — a human face on the Royal African Company’s trade."},
            {"url": "https://www.youtube.com/watch?v=4ci6MdIMKew", "title": "Olaudah Equiano: Story of a Former Slave Who Worked Against Slavery", "description": "Short explainer on Equiano’s life and legacy — links the slave trade of this period to later abolition movements."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/12-years-a-slave", "title": "12 Years a Slave (2013)", "description": "Steve McQueen’s Oscar-winning film — a direct account of chattel slavery; the system the Royal African Company built and defended."},
            {"url": "https://www.justwatch.com/uk/movie/belle", "title": "Belle (2013)", "description": "Mixed-race heiress Dido Elizabeth Belle and the Zong massacre case — shows how the slavery economy intersected with English law."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.nationalarchives.gov.uk/slavery/", "title": "National Archives — Slavery and the British Transatlantic Slave Trade", "description": "Primary source documents from the National Archives: RAC charter, ship logs, insurance claims. Free and authoritative."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Empire unit for slave economy content and source-skills practice."}
        ]}
    ],

    # L7: Consumerism, coffee houses and political activism
    "faf18d68-38d2-48e4-b99e-5f48f0aa8f26": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l07.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5aQZaxPyCitvCUBt6kIaLa", "title": "In Our Time — The Coffee House (BBC Radio 4)", "description": "Melvyn Bragg on how 17th- and 18th-century coffee houses became engines of news, finance and political debate — the direct subject of this lesson."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=Gu4yOqdfStY", "title": "David Olusoga: Black British History and Belonging", "description": "Olusoga on how the commercial revolution of the late 17th century, driven by empire, reshaped everyday British life."},
            {"url": "https://www.youtube.com/watch?v=UTn-ujN81Ds", "title": "Shaping the City: History of the Huguenots / Spitalfields Site", "description": "The transformation of London’s commercial culture in exactly the 1688-1730 period — trade goods, consumer culture and political discourse."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-favourite", "title": "The Favourite (2018)", "description": "Set in the coffeehouse political culture of early-18th-century Britain — Queen Anne’s court and the Whig/Tory factionalism that coffee houses fuelled."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.museumofthehome.org.uk/", "title": "Museum of the Home", "description": "The Museum of the Home (Hoxton) holds collections on domestic consumption and interiors from exactly the 1688-1730 period — free online resources."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — use for Empire unit revision on consumerism and social change."}
        ]}
    ],

    # L8: Spitalfields: site introduction and Huguenot weavers
    "7b8d94b0-b2aa-4dfd-a4f5-bdaf78ba03d4": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l08.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/gone-medieval/episodes/jews-medieval-england", "title": "Gone Medieval — Jews in Medieval England", "description": "Useful context on earlier waves of migrants to London’s East End before the Huguenots — helps trace Spitalfields’s layered migration history."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=UTn-ujN81Ds", "title": "Shaping the City: History of the Huguenots / Spitalfields Site", "description": "Directly covers the Huguenot weaving community, Christ Church Spitalfields and the silk trade that the lesson explores."},
            {"url": "https://www.youtube.com/watch?v=JfTaXRFV7EA", "title": "Black Tudors: Three Untold Stories — Gresham College", "description": "Puts the Huguenot settlement in the context of London’s diverse early-modern migrant communities in the East End."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "Caroline Quentin on restoring historic buildings — several episodes cover Georgian and Queen Anne townhouses of the type the Huguenots built in Spitalfields."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/christ-church-spitalfields/", "title": "English Heritage — Christ Church Spitalfields", "description": "Nicholas Hawksmoor’s 1729 church, built for the Huguenot community — English Heritage’s curatorial notes on the building’s history and symbolism."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Empire unit for Spitalfields source-skills material."}
        ]}
    ],

    # L9: Spitalfields: Irish, Jewish and Bangladeshi communities
    "d4789cef-b75b-48a6-8955-a7ad0817e81e": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l09.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/gone-medieval/episodes/jews-medieval-england", "title": "Gone Medieval — Jews in Medieval England", "description": "Background on Jewish communities in England before their 1290 expulsion — the context for the Jewish re-settlement in Spitalfields from the 1650s."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=oA1DTYGs2tc", "title": "La Bohème to Gardiners: Sights and Sounds of the Jewish East End", "description": "Film on the Jewish community of the East End — the culture, synagogues and businesses that replaced the Huguenot silk trade in Spitalfields."},
            {"url": "https://www.youtube.com/watch?v=UTn-ujN81Ds", "title": "Shaping the City: History of the Huguenots / Spitalfields Site", "description": "The full sequence of migrant communities in Spitalfields — from Huguenot church to Jewish synagogue to Bangladeshi mosque."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-wind-that-shakes-the-barley", "title": "The Wind That Shakes the Barley (2006)", "description": "The Irish independence story whose predecessors settled in Spitalfields’ Irish quarter after the 1840s famine — one of the communities this lesson examines."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.ourmigrationstory.org.uk/", "title": "Our Migration Story (Runnymede Trust + Cambridge)", "description": "Organised by migrant community and period — covers all three Spitalfields communities (Irish, Jewish, Bangladeshi) with primary sources."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Empire unit for Spitalfields site material and source skills."}
        ]}
    ],

    # L10: Source skills for Spitalfields and Empire
    "af5160c4-ceea-4341-ac75-1eac629ba6d1": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/impact-empire-britain-1688-1730/podcast_l10.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/gone-medieval/episodes/jews-medieval-england", "title": "Gone Medieval — Working with Historical Evidence", "description": "History Hit on evaluating primary sources — the same source-skills approach the OCR SHP exam requires."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=UTn-ujN81Ds", "title": "Shaping the City: History of the Huguenots / Spitalfields Site", "description": "A documentary-style treatment of the Spitalfields site that models how historians use buildings, images and documents as sources."},
            {"url": "https://www.youtube.com/watch?v=Gu4yOqdfStY", "title": "David Olusoga: Black British History and Belonging", "description": "Olusoga demonstrates how to read the silences in historical sources — a key skill for OCR SHP source questions."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "Shows historians using physical buildings as evidence — exactly the type of site-based source analysis the OCR SHP source skills section demands."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/christ-church-spitalfields/", "title": "English Heritage — Christ Church Spitalfields", "description": "Curatorial notes on the building as a historical source — use for practising source analysis questions on the site."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Download the specification to review the exact source-skills assessment objectives (AO1, AO2, AO3) for this unit."}
        ]}
    ],

    # ============================================================
    # UNIT 11: ENGLISH REFORMATION 1520-1550
    # ============================================================

    # L1: The pre-Reformation English Church c.1520
    "86b66689-7d8e-47f9-b143-a181d3106e7e": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l01.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://www.englandcast.com/thomas-wolsey-and-thomas-more/", "title": "Episode 9: A Tale of Two Thomases — Renaissance English History Podcast", "description": "Heather Teysko sets up the Wolsey/More double-act — useful background on the church before the break."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=ldbZ1HnbRcQ", "title": "Henry VIII and the Break with Rome: Exploring England’s Reformation", "description": "Clear explainer on the state of the English Church before 1520 — corruption, anticlerical feeling and the Pope’s authority."},
            {"url": "https://www.youtube.com/watch?v=gxrWKq7JyPI", "title": "The King’s Cardinal? Wolsey and Henry VIII — Glenn Richardson", "description": "Academic lecture on Wolsey’s dual role — both the church’s most powerful figure in England and the king’s minister."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/wolf-hall", "title": "Wolf Hall (2015)", "description": "BBC drama that opens with Wolsey as both Cardinal and Lord Chancellor — shows the church’s power and wealth before the Reformation began."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for pre-Reformation context and key concepts."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — download for the Reformation unit’s key concepts and assessment objectives."}
        ]}
    ],

    # L2: Lollards, Luther and English criticism of the church
    "7b9fe5e8-2441-4573-9856-8b197e812369": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l02.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://www.englandcast.com/thomas-wolsey-and-thomas-more/", "title": "Renaissance English History Podcast — Wolsey, Luther and Reform", "description": "Heather Teysko on how Luther’s ideas reached England via Cambridge scholars in the early 1520s."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=ldbZ1HnbRcQ", "title": "Henry VIII and the Break with Rome: Exploring England’s Reformation", "description": "Covers the Lollard tradition and Luther’s influence on English reformers — the intellectual roots of the English Reformation."},
            {"url": "https://www.youtube.com/watch?v=7RjKG6gwmiE", "title": "Henry VIII: Mind of a Tyrant Part 1 — David Starkey", "description": "David Starkey on the young Henry VIII — his initial hostility to Luther and the shifting religious landscape of the 1520s."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-other-boleyn-girl", "title": "The Other Boleyn Girl (2008)", "description": "The Boleyn family’s reformist connections — Anne Boleyn’s reading of Tyndale and her role in bringing Protestant ideas to court."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bl.uk/medieval-manuscripts/articles/the-wycliffe-bible", "title": "British Library — The Wycliffe Bible", "description": "The British Library on John Wycliffe’s English Bible and the Lollard movement that influenced later reformers like Tyndale."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for Lollards and Luther content."}
        ]}
    ],

    # L3: The King's Great Matter and the Reformation Parliament
    "4112bb3b-0687-4fca-855f-49b49b786008": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l03.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/5UVvpuruWMTPdBh2OwTMeV", "title": "Cardinal Wolsey: His Rise and Fall — Not Just the Tudors", "description": "Suzannah Lipscomb on Wolsey’s failure to secure the annulment — the event that triggered the King’s Great Matter and his fall."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=EOwLeamzbCA", "title": "The Tudors: Henry VIII — The King’s Great Matter and the Queen", "description": "Direct explainer on the annulment crisis — Catherine of Aragon, the Pope and why Henry couldn’t get what he wanted."},
            {"url": "https://www.youtube.com/watch?v=ZTCAFaNo6QI", "title": "GCSE History Rapid Revision: Wolsey and Henry’s Divorce", "description": "Rapid revision of the King’s Great Matter — the failed Legatine Court and its political consequences."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/wolf-hall", "title": "Wolf Hall (2015)", "description": "The BBC drama covers Cromwell’s rise as Henry’s solution to the deadlocked annulment — exactly the political shift the Reformation Parliament represents."},
            {"url": "https://www.justwatch.com/uk/tv-series/the-tudors", "title": "The Tudors (2007–10)", "description": "The early seasons dramatise the King’s Great Matter in detail — useful for visualising the court politics around the break with Rome."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for the King’s Great Matter content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — check the key concepts for the Reformation Parliament and its significance."}
        ]}
    ],

    # L4: Valor Ecclesiasticus and Visitation of the Monasteries
    "c0302a44-efcc-49b7-a7b4-aec21ba40f29": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l04.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://www.englandcast.com/thomas-wolsey-and-thomas-more/", "title": "Renaissance English History Podcast — Cromwell and the Monasteries", "description": "Heather Teysko on how Thomas Cromwell built the administrative machinery that made the Dissolution possible."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=XHN_joj0adc", "title": "Henry VIII’s real intention for the Monasteries (Episode 1/5)", "description": "Revisionist take on what the Valor Ecclesiasticus visitation was really for — wealth extraction, reform or both?"},
            {"url": "https://www.youtube.com/watch?v=qkYiCRFtkGo", "title": "Rethinking Thomas Cromwell", "description": "Academic re-evaluation of Cromwell as the architect of the visitation — his methods and motivations examined."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/wolf-hall", "title": "Wolf Hall (2015)", "description": "Hilary Mantel’s Cromwell is the administrator who runs the visitation — the series captures the bureaucratic reality of Tudor dissolution."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.nationalarchives.gov.uk/education/resources/dissolution-of-the-monasteries/", "title": "National Archives — Dissolution of the Monasteries", "description": "Primary source documents from the Valor Ecclesiasticus visitation — free and directly relevant to source-skills questions."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for the Valor Ecclesiasticus and Dissolution content."}
        ]}
    ],

    # L5: Dissolution: process, impact and resistance
    "1d202846-e8bd-4ffe-b2e6-c76ba88e4dc0": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l05.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://www.englandcast.com/thomas-wolsey-and-thomas-more/", "title": "Renaissance English History Podcast — The Pilgrimage of Grace", "description": "Heather Teysko on the northern rising against the Dissolution — the largest popular rebellion of the Tudor period."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=_H7mvlZ022o", "title": "It’s All Henry VIII: A Beginner’s Guide to the Dissolution", "description": "Accessible overview of how the Dissolution unfolded in phases from 1535 — which monasteries closed when and why."},
            {"url": "https://www.youtube.com/watch?v=3bNtri0it4I", "title": "The BRUTAL Execution of Robert Aske — The Pilgrimage of Grace", "description": "The leader of the resistance to the Dissolution — his demands, his march south, and his fate after the rebellion was suppressed."},
            {"url": "https://www.youtube.com/watch?v=5pYB1wr70Zs", "title": "The Pilgrimage of Grace — Reading the Past", "description": "Scholarly overview of the 1536 rising — religious grievances, political demands and why Henry’s response changed the nature of the Reformation."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/atonement", "title": "Atonement (2007)", "description": "Filmed at a repurposed historic country house — the kind of estate wealthy families acquired through the Dissolution. Evokes the transformation of the English landscape."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.nationalarchives.gov.uk/education/resources/dissolution-of-the-monasteries/", "title": "National Archives — Dissolution of the Monasteries", "description": "Primary source documents including the Act of Suppression and reports from visitors — free classroom resources."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — Dissolution process and impact revision content."}
        ]}
    ],

    # L6: Religious worship under Henry and Edward
    "c08dd5c4-ce62-461a-b30f-61c7d978c785": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l06.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Religious Change Under the Tudors", "description": "Suzannah Lipscomb on how the experience of worship changed for ordinary English people between 1530 and 1560."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=-GbkZ_Y1AeQ", "title": "Early Elizabethan England: The Religious Settlement", "description": "Covers the Prayer Book debate and how Elizabeth’s settlement tried to resolve the divisions created under Henry and Edward."},
            {"url": "https://www.youtube.com/watch?v=J4luTCHc-tc", "title": "GCSE History Rapid Revision: The Elizabethan Religious Settlement", "description": "The religious settlement Edward’s reign prepared the ground for — context for why Elizabeth needed to act in 1559."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/the-tudors", "title": "The Tudors (2007–10)", "description": "The later series covers the changing religious practices of Henry’s reign — the Six Articles, the English Bible, and the shifting orthodoxy."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for the Henrician and Edwardian religion content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — download for the Reformation key concepts on religious change under Henry and Edward."}
        ]}
    ],

    # L7: Parish reaction and the Prayer Book Rebellion
    "0359cbd7-48f0-4348-8c79-789f43372a10": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l07.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Popular Religion and Rebellion", "description": "How ordinary people responded to the religious changes imposed from above — the Prayer Book Rebellion as a case study."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=Guy5Ydb7OaI", "title": "Edexcel GCSE History: The Catholic Challenge to the Religious Settlement", "description": "Covers the Catholic resistance to Protestant worship changes — the same grievances that drove the 1549 rebels in Devon and Cornwall."},
            {"url": "https://www.youtube.com/watch?v=5pYB1wr70Zs", "title": "The Pilgrimage of Grace — Reading the Past", "description": "The 1536 precedent — a similar popular reaction to Tudor religious change that ended in brutal suppression."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/the-other-boleyn-girl", "title": "The Other Boleyn Girl (2008)", "description": "Shows the court politics that drove the religious changes which provoked popular anger — the gap between the court and the parishes."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for the Prayer Book Rebellion content."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — check the key concepts for popular reaction to the Edwardian Reformation."}
        ]}
    ],

    # L8: Kenilworth Castle: location and physical fabric
    "ade240b6-103e-4b31-8671-0f7100d0f715": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l08.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Tudor Castles and Palaces", "description": "Suzannah Lipscomb on how Tudor monarchs used royal buildings as instruments of power — the context for reading Kenilworth as a site."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/@EnglishHeritageFilm", "title": "English Heritage — YouTube Channel", "description": "English Heritage’s channel includes footage of Kenilworth Castle — drone shots, guided tours and the Elizabethan garden restoration."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/elizabeth", "title": "Elizabeth (1998)", "description": "Cate Blanchett’s depiction of Elizabethan court life — the same political world in which Kenilworth was Leicester’s most ambitious display of loyalty."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "Caroline Quentin on restoring historic buildings — the architectural analysis skills modelled here apply directly to OCR site-study questions."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/", "title": "English Heritage — Kenilworth Castle", "description": "The authoritative site for Kenilworth — history, floor plans, collections and educational resources for OCR source-skills questions."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the English Reformation unit for Kenilworth site-study content."}
        ]}
    ],

    # L9: Kenilworth's functions: defence, residence, administration
    "db2bd630-c89e-4505-b9bb-8809b5cb21f8": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l09.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — Tudor Patronage and Power", "description": "How Tudor magnates used their residences as political tools — a model for reading Leicester’s investments at Kenilworth."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/@EnglishHeritageFilm", "title": "English Heritage — YouTube Channel", "description": "English Heritage’s videos on Kenilworth include the defensive history of the keep and Leicester’s great hall addition — directly useful for site analysis."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/elizabeth", "title": "Elizabeth (1998)", "description": "Shows Elizabethan magnates competing for royal favour through patronage and building — the culture behind Leicester’s Kenilworth investment."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "The architectural analysis skills modelled here apply directly to OCR site-study questions on Kenilworth’s functions."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/", "title": "English Heritage — Kenilworth Castle", "description": "Full historical account, interactive map and audio tours — the definitive resource for OCR source skills on Kenilworth as a site."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — check the site-study assessment objectives for how the exam uses Kenilworth as a source."}
        ]}
    ],

    # L10: Source skills for Kenilworth and the Reformation
    "0384caf3-baa4-470c-899b-bdfb427f8fb9": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/english-reformation-1520-1550/podcast_l10.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://shows.acast.com/not-just-the-tudors/episodes/elizabethiandmary-queenofscots-rivalqueens", "title": "Not Just the Tudors — How Historians Read the Past", "description": "Suzannah Lipscomb on evaluating sources for the Elizabethan period — models the critical approach required by OCR source-skills questions."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/@EnglishHeritageFilm", "title": "English Heritage — YouTube Channel", "description": "English Heritage’s Kenilworth content models how to read the site as a historical source — essential exam preparation."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/elizabeth", "title": "Elizabeth (1998)", "description": "Shows the Elizabethan political world that Kenilworth’s architecture was designed to impress — helpful for understanding the site’s function as evidence."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "Shows how historians and architects read buildings as documents — directly applicable to OCR source-skills methodology."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/", "title": "English Heritage — Kenilworth Castle", "description": "Official site with architectural history, photos and documents — use for practising source-analysis and site-study exam questions."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Download the J411 spec to review the exact mark scheme structure for source-skills questions on site studies."}
        ]}
    ],

    # ============================================================
    # UNIT 12: PERSONAL RULE & RESTORATION 1629-1660
    # ============================================================

    # L1: Charles I's Personal Rule 1629-1640
    "b83a41e7-248d-4bb9-9dca-7ac6a9754e8c": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l01.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — Charles I and the Personal Rule", "description": "Overview of the 1629-1640 period — the constitutional, financial and religious crises Charles created by ruling without Parliament."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "Context for the military revolution — the Personal Rule’s collapse led directly to the New Model Army that defeated Charles."},
            {"url": "https://www.youtube.com/watch?v=qkYiCRFtkGo", "title": "Rethinking Thomas Cromwell", "description": "Revisionist academic history — the kind of evidence-based argument the OCR SHP source-skills section rewards."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Opens with Charles I’s Personal Rule and the constitutional grievances that would bring him to trial — Richard Harris as Cromwell."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Newark’s Civil War museum — resources on the causes of the Civil War including the Personal Rule’s constitutional crises."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Personal Rule unit for Charles I and the 1629-40 period."}
        ]}
    ],

    # L2: Slide to civil war 1640-1642
    "4bdf9afa-5d3d-41e1-87bc-97c86a089b6f": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l02.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Road to Civil War", "description": "How the Short and Long Parliaments, the Grand Remonstrance and the Five Members crisis made war inevitable by 1642."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The constitutional crisis of 1640-42 was the background to the army reform that would decide the war’s outcome."},
            {"url": "https://www.youtube.com/watch?v=_CmIvXGCBco", "title": "Pike & Shot Warfare: The Musket and the Transformation of Battle", "description": "The weapon systems both sides would use once the constitutional slide to war turned into open conflict."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "The film dramatises the constitutional breakdown — Charles’s attempts to raise money without Parliament and the slide to armed conflict."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Resources on the 1640-42 crisis — timeline, primary sources and analysis of why the constitutional conflict became a shooting war."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — the Personal Rule unit covers the 1640-42 slide to Civil War."}
        ]}
    ],

    # L3: First Civil War 1642-1646
    "9802b81b-9f91-4a3a-895f-1b9ba7f60f97": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l03.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The First Civil War 1642-1646", "description": "Key battles, turning points — Edgehill, Marston Moor, Naseby — and how the war changed British society."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=FZoyt6UA3TE", "title": "Naseby: The Grim Battle That Decided The English Civil War", "description": "Step-by-step account of the 1645 decisive battle — how the New Model Army destroyed the Royalist field army."},
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "How Cromwell’s restructured army won the war — the decisive military innovation of the First Civil War."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Dramatises the key battles of the First Civil War — Edgehill, Marston Moor and the capture of Charles I."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Primary sources, battle maps and analysis of the First Civil War — essential for both content revision and source skills."},
            {"url": "https://www.battlefieldstrust.com/resource-centre/war-of-the-roses/battlepageview.asp?pageid=878", "title": "Battlefields Trust — Battle of Naseby", "description": "The Battlefields Trust’s account of Naseby 1645 — the decisive engagement that ended the First Civil War."}
        ]}
    ],

    # L4: Levellers, Diggers and radical religion
    "e220b05d-84fb-480b-b269-e0ebc13eca5d": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l04.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — Radicals of the English Revolution", "description": "Overview of the Levellers, Diggers and Fifth Monarchists — the radical movements the Civil War unleashed."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The New Model Army was the crucible of Leveller thought — soldiers who expected political rights in return for military service."},
            {"url": "https://www.youtube.com/watch?v=qkYiCRFtkGo", "title": "Rethinking Thomas Cromwell", "description": "Models the kind of revisionist historical argument relevant to debates about Cromwell’s crushing of the Levellers at Burford."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Shows the radical energy the Civil War released and Cromwell’s eventual repression of it — the aftermath of the Burford mutiny dramatised."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Collections and resources on radical religion and political thought — the Putney Debates archive is particularly relevant."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Personal Rule unit for the radical movements content."}
        ]}
    ],

    # L5: Second Civil War, Pride's Purge and regicide
    "0a2efafc-3f21-4433-8599-5d96ee5d871c": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l05.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Trial and Execution of Charles I", "description": "The regicide of 1649 — the legal innovation, the political stakes and why only a small minority of MPs went through with it."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=FZoyt6UA3TE", "title": "Naseby: The Grim Battle That Decided The English Civil War", "description": "The Second Civil War was Charles’s gamble after Naseby — this video shows why his military options were exhausted by 1648."},
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The army that carried out Pride’s Purge and then demanded the king’s trial — the political role of the New Model Army."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "The film’s climax covers the trial and execution of Charles I — a dramatised account of one of the most shocking events in British history."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Resources on Pride’s Purge and the regicide — primary documents including the death warrant and trial records."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — the regicide and its aftermath in the Personal Rule unit."}
        ]}
    ],

    # L6: Rump Parliament and the rise of Cromwell 1649-1653
    "5a7dcace-9d8b-41a2-b846-c016993eb2c8": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l06.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Commonwealth and Cromwell’s Rise", "description": "How Cromwell went from MP to military commander to the man who dissolved the Rump Parliament in 1653."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The army Cromwell commanded was also the political force that made and unmade governments — including the Rump."},
            {"url": "https://www.youtube.com/watch?v=qkYiCRFtkGo", "title": "Rethinking Thomas Cromwell", "description": "Academic re-evaluation of a political outsider who shaped British history — the historiographical debate about Cromwell parallels this period."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Richard Harris as Cromwell — his rise from gentleman farmer to Lord Protector, including the Rump Parliament dissolution scene."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Resources on the Commonwealth period and Cromwell’s political career — essential for the rise of Cromwell content."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Personal Rule unit for Commonwealth and Cromwell content."}
        ]}
    ],

    # L7: Protectorate 1653-1658
    "ae1234a4-5146-4e8f-82d8-9cbe2f85a374": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l07.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Cromwellian Protectorate", "description": "How Cromwell governed as Lord Protector — his constitutional experiments, religious policies and military campaigns."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The army that underpinned the Protectorate — Cromwell’s military rule depended on the loyalty of the soldiers he had led to victory."},
            {"url": "https://www.youtube.com/watch?v=qkYiCRFtkGo", "title": "Rethinking Thomas Cromwell", "description": "How historians divide on Cromwell — tyrant or reformer? The debate is central to evaluating the Protectorate’s achievements."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "The film’s final act covers the Protectorate — Cromwell’s reluctance to become king and the instability of his regime."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Dedicated Protectorate resources — Cromwell as Lord Protector, the Major-Generals’ government and the failure to find a settlement."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Personal Rule unit for the Protectorate content and key concepts."}
        ]}
    ],

    # L8: Restoration 1658-1660
    "c151b298-62f4-4019-b7e3-a1532693b898": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l08.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — The Restoration of Charles II", "description": "Why the Protectorate collapsed so quickly after Cromwell’s death and how Charles II returned in triumph."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/watch?v=B9DlZs_CkDU", "title": "The New Model Army: Cromwell, Meritocracy, and Naseby", "description": "The army that had carried the Commonwealth ultimately couldn’t sustain it — understanding why it backed the Restoration."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "The film’s epilogue covers the context for the Restoration — the failure of the Good Old Cause and the return of monarchy."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/horrible-histories", "title": "Horrible Histories (2009–)", "description": "The Stuart episodes cover the Restoration with characteristic wit — Cavaliers and Roundheads explained accessibly."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.national-civil-war-centre.com/", "title": "National Civil War Centre", "description": "Resources on the Restoration settlement — what changed and what remained from the pre-war constitutional order."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — the Restoration and its constitutional significance in the Personal Rule unit."}
        ]}
    ],

    # L9: Kenilworth Castle in the Civil War
    "f2037a2d-53e2-421b-962e-6a7b83b8b5ca": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l09.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — Siege Warfare in the English Civil War", "description": "Overview of Civil War siege warfare — the context for Kenilworth’s use as a garrison and its subsequent slighting."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/@EnglishHeritageFilm", "title": "English Heritage — YouTube Channel", "description": "English Heritage’s Kenilworth coverage includes the Civil War period — slighting evidence visible in the castle’s current fabric."},
            {"url": "https://www.youtube.com/watch?v=FZoyt6UA3TE", "title": "Naseby: The Grim Battle That Decided The English Civil War", "description": "The Midlands context for Kenilworth’s Civil War garrison — the castle sat in contested territory during the 1642-46 campaigns."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "The film shows Parliamentarian armies taking castles in the Midlands — the same campaigns that saw Kenilworth garrisoned and slighted."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/", "title": "English Heritage — Kenilworth Castle", "description": "English Heritage’s account of Kenilworth in the Civil War — slighting evidence, garrison history and what survives today."},
            {"url": "https://www.bbc.co.uk/bitesize/examspecs/zxcrxnb", "title": "BBC Bitesize — OCR GCSE History (SHP)", "description": "OCR SHP hub — navigate to the Personal Rule unit for Kenilworth site-study content in the Civil War context."}
        ]}
    ],

    # L10: Source skills for Kenilworth and Personal Rule
    "e8191897-450f-4eaf-ae7b-d279b2312566": [
        {"category": "Podcasts", "items": [
            {"url": "https://pub-f7b76d81365b4b2f954567763694a24e.r2.dev/history-ocr/personal-rule-restoration-1629-1660/podcast_l10.mp3", "title": "Lesson Podcast", "description": "AI-generated audio overview of this lesson"},
            {"url": "https://open.spotify.com/episode/4KSTAv1Or2ASHKquJnLRCN", "title": "Dan Snow’s History Hit — Using Primary Sources for the Civil War", "description": "How historians use letters, newsbooks and physical evidence from the Civil War period — models the source-skills approach required by OCR."}
        ]},
        {"category": "Videos & Channels", "items": [
            {"url": "https://www.youtube.com/@EnglishHeritageFilm", "title": "English Heritage — YouTube Channel", "description": "English Heritage’s Kenilworth content models how to read the site as a source — essential for OCR site-study source questions."}
        ]},
        {"category": "Movies", "items": [
            {"url": "https://www.justwatch.com/uk/movie/cromwell", "title": "Cromwell (1970)", "description": "Dramatises the Civil War context that shaped Kenilworth’s slighting — useful for contextualising the physical evidence at the site."}
        ]},
        {"category": "TV Shows", "items": [
            {"url": "https://www.justwatch.com/uk/tv-series/restoration-home", "title": "Restoration Home (2011)", "description": "Shows how physical buildings can be read as historical documents — the analytical approach the OCR source-skills section demands."}
        ]},
        {"category": "Study Tools", "items": [
            {"url": "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/", "title": "English Heritage — Kenilworth Castle", "description": "Official site with the full history, images and documents for Kenilworth — essential for source-analysis exam questions."},
            {"url": "https://www.ocr.org.uk/qualifications/gcse/history-b-schools-history-project-j411-from-2016/", "title": "OCR — GCSE History B Specification", "description": "Official J411 spec — download to review the exact mark scheme and source-skills assessment objectives for the site-study questions."}
        ]}
    ],
}

# ---- Run ----
sb = get_client()
total = len(LESSON_MEDIA)
updated = 0
errors = []

for lesson_id, media in LESSON_MEDIA.items():
    if args.dry_run:
        total_items = sum(len(c["items"]) for c in media)
        print(f"  DRY-RUN {lesson_id}: {len(media)} categories, {total_items} items")
        updated += 1
        continue

    resp = (
        sb.table("lessons")
        .update({"related_media": media})
        .eq("id", lesson_id)
        .execute()
    )

    if resp.data:
        updated += 1
        if updated % 10 == 0:
            print(f"  Uploaded {updated}/{total}")
    else:
        errors.append(f"No rows updated for {lesson_id}")

print(f"\n=== Done: {updated}/{total} lessons updated ===")
if errors:
    print(f"\n{len(errors)} errors:")
    for e in errors:
        print(f"  {e}")
