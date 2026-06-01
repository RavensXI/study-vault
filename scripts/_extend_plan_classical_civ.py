"""Append the 6 units for the 3 missing OCR J199 options to the Classical Civ plan."""
import json
from pathlib import Path

P = Path("scripts/_plan_classical-civilisation-ocr.json")
p = json.loads(P.read_text(encoding="utf-8"))


def U(slug, name, subtitle, bc_n, accent, al, sort, lessons):
    return {
        "name": name, "slug": slug, "subtitle": subtitle,
        "body_class": f"unit-classical-civilisation-ocr-{bc_n}",
        "accent": accent, "accent_light": al, "accent_badge": accent + "33",
        "lesson_count": len(lessons), "sort_order": sort, "lessons": lessons,
    }


def L(n, title, desc, sr, markers):
    return {"number": n, "title": title, "description": desc, "spec_references": [sr], "section_markers": markers}


new = []

# ---- Women in the Ancient World (J199/12) ----
new.append(U("women-of-legend-and-the-home", "Women of Legend & the Home",
    "Mythological women from Pandora to Medea, the rituals of marriage and coming of age, and the lives of Athenian, Spartan and Roman women in the home.",
    5, "#be123c", "#ffe4e6", 5, [
    L(1, "Women of Legend", "Powerful and dangerous women of Greek and Roman myth - Pandora, Helen, Clytemnestra, Medea and the Sabine Women.",
      "Women in the Ancient World: Women of Legend",
      ["women of legend", "Pandora the first woman", "Helen of Troy", "Clytemnestra", "Medea", "Penelope as the faithful wife", "the Sabine Women and Tarpeia", "how myth portrays women as both ideal and dangerous"]),
    L(2, "Marriage & Coming of Age", "How young women came of age and married - Athenian wedding rituals and the very different Spartan system.",
      "Women in the Ancient World: Young Women",
      ["young women coming of age", "typical Athenian wedding rituals and arrangements", "the dowry", "the role of the kyrios in arranging marriage", "the Spartan system of education and marriage", "age of marriage Athens versus Sparta", "comparison of Athenian and Spartan upbringing"]),
    L(3, "The Athenian Woman & the Home", "The life of a respectable Athenian woman - the kyria, ideals of wifely virtue, seclusion and domestic slaves.",
      "Women in the Ancient World: Women in the Home",
      ["the kyria the woman of the house", "Athenian ideas of wifely virtue", "the seclusion of women the gynaikon womens quarters", "managing the household and weaving", "Athenian domestic slaves", "the ideal of the respectable invisible woman"]),
    L(4, "The Spartan Woman", "Why Spartan women were so different - their education, physical training, property and the role of wife and mother.",
      "Women in the Ancient World: Women in the Home",
      ["the experience of a Spartan wife and mother", "Spartan female education and physical training", "Spartan women and property", "producing strong children for the state", "freedoms of Spartan women compared with Athenian women", "Spartan attitudes to motherhood"]),
    L(5, "Roman Women & the Home", "The Roman matron, her role in the household and family, and the ideals of female virtue such as Lucretia.",
      "Women in the Ancient World: Women in the Home",
      ["the Roman matron materfamilias", "the role of women in the Roman household", "Roman ideals of female virtue and chastity", "Lucretia as the model of virtue", "women and the family in Rome", "comparison of Roman with Greek women"]),
]))

new.append(U("women-religion-and-power", "Women, Religion & Power",
    "Women as priestesses and in festivals, their exclusion from politics and informal influence, powerful queens and empresses, and the warrior women of myth and history.",
    6, "#9f1239", "#ffe4e6", 6, [
    L(1, "Women & Religion", "The major religious roles open to women - priestesses, the Pythia at Delphi, the Vestal Virgins and women-only festivals.",
      "Women in the Ancient World: Women and religion",
      ["women and religion", "priestesses and prophetesses including the Pythia", "the Vestal Virgins at Rome", "womens roles in festivals", "the Thesmophoria festival for women", "religion as a public role open to women"]),
    L(2, "Women, Power & Exclusion", "Women's exclusion from formal politics and the informal power they could still exercise.",
      "Women in the Ancient World: Women and power",
      ["women and power", "the Athenian Assembly and the exclusion of women from politics", "women as citizens but not voters", "informal influence within the household and family", "how women could exercise power behind the scenes"]),
    L(3, "Powerful Women of Rome", "Roman women who wielded real power - imperial women such as Livia and Agrippina, and Cleopatra of Egypt.",
      "Women in the Ancient World: Women and power",
      ["powerful women of Rome", "Livia wife of Augustus", "Agrippina mother of Nero", "imperial women and influence at court", "Cleopatra queen of Egypt", "how sources portray powerful women as dangerous"]),
    L(4, "Warrior Women", "Women who fought - the Amazons of myth and art, and the historical warrior queen Boudica.",
      "Women in the Ancient World: Warrior Women",
      ["warrior women", "the Amazons in Greek myth and art", "Amazonomachy in sculpture", "Penthesilea", "Boudica the British warrior queen", "women to be reckoned with", "how warrior women challenge normal gender roles"]),
    L(5, "Notable Women & the Sources", "Other remarkable women and the problem of how male-authored sources portray women's lives.",
      "Women in the Ancient World: sources",
      ["notable women of the ancient world", "Cornelia mother of the Gracchi", "Lucretia and Roman virtue", "the problem of male-authored sources for womens lives", "literary versus visual sources for women", "how to use evidence about women critically"]),
]))

# ---- Roman City Life (J199/22) ----
new.append(U("the-roman-city-and-home", "The Roman City & Home",
    "How a Roman city was planned and built, the forum and public buildings, the town house and the apartment block, and Pompeii and Herculaneum as our evidence.",
    7, "#92400e", "#fef3c7", 7, [
    L(1, "Town Planning & the City", "How Roman cities were laid out - the grid plan, streets and amenities - using Rome, Ostia, Pompeii and Herculaneum.",
      "Roman City Life: town planning",
      ["Roman town planning", "the grid plan of streets", "Rome Ostia Pompeii and Herculaneum as examples", "streets pavements and amenities", "water supply and aqueducts", "the forum at the centre of the city"]),
    L(2, "The Forum & Public Buildings", "The heart of the Roman city - the forum, the basilica, temples and the buildings of civic life.",
      "Roman City Life: public buildings",
      ["the forum as the civic centre", "the basilica for law and business", "temples in the city", "public buildings and civic life", "markets and shops", "the public face of the Roman city"]),
    L(3, "The Roman Domus", "The Roman town house - the atrium, the peristyle garden and the rooms - and what it shows about family and status.",
      "Roman City Life: housing",
      ["Roman housing the domus", "the atrium and impluvium", "the peristyle garden", "the rooms tablinum triclinium cubiculum", "wall paintings and mosaics", "the domus as a display of status"]),
    L(4, "Apartment Living: the Insula", "How ordinary Romans lived - the insula apartment block, using the Insula of Diana at Ostia, and urban living conditions.",
      "Roman City Life: housing",
      ["apartment living the insula", "the Insula of Diana at Ostia", "living conditions for ordinary Romans", "shops on the ground floor", "fire and collapse risks", "contrast between the domus and the insula"]),
    L(5, "Pompeii & Herculaneum as Evidence", "How the eruption of Vesuvius preserved two Roman towns and what they reveal about daily life.",
      "Roman City Life: evidence",
      ["Pompeii and Herculaneum as evidence", "the eruption of Vesuvius AD 79", "preservation of buildings and objects", "what the towns reveal about daily life", "graffiti and inscriptions", "the value and limits of the evidence"]),
]))

new.append(U("roman-leisure-and-society", "Roman Leisure & Society",
    "How Romans spent their leisure - the baths, the amphitheatre and gladiators, the theatre and chariot racing - and the slaves, freedmen and religion of the city.",
    8, "#c2410c", "#fff7ed", 8, [
    L(1, "The Roman Baths", "The role of the public baths in Roman life - the bathing routine, the rooms, and the baths as a social centre.",
      "Roman City Life: leisure and entertainment",
      ["the Roman baths", "the Forum or Central Baths at Pompeii", "the bathing routine apodyterium tepidarium caldarium frigidarium", "the hypocaust heating system", "the baths as a social centre", "exercise and the palaestra"]),
    L(2, "The Amphitheatre & Gladiators", "The games of the arena - the amphitheatre, the types of gladiator, and Roman attitudes to the spectacle.",
      "Roman City Life: leisure and entertainment",
      ["the amphitheatre", "gladiatorial games", "types of gladiator murmillo retiarius thraex", "the organisation of the games", "wild beast hunts venationes", "Roman attitudes to violence and spectacle"]),
    L(3, "Theatre & Chariot Racing", "Other Roman entertainments - the theatre and its drama, and the thrill of chariot racing at the Circus Maximus.",
      "Roman City Life: leisure and entertainment",
      ["the Roman theatre", "Roman drama comedy and pantomime", "the structure of the theatre", "chariot racing", "the Circus Maximus", "the racing factions and their supporters"]),
    L(4, "Slaves & Freedmen", "The slaves who underpinned Roman city life, the relationship of slaves and masters, and the freedmen who won their liberty.",
      "Roman City Life: slaves and freedmen",
      ["slaves and freedmen", "slaves and masters in the Roman city", "the work and treatment of slaves", "manumission the freeing of slaves", "the status of freedmen", "the role of freedmen in commerce"]),
    L(5, "Religion in the Roman City", "Religion in everyday city life - household gods, temples and the festivals that filled the Roman calendar.",
      "Roman City Life: religion",
      ["religion in the Roman city", "household gods the Lares and Penates", "the household shrine the lararium", "temples in the city", "public festivals and the religious calendar", "religion woven into daily life"]),
]))

# ---- War and Warfare (J199/23) ----
new.append(U("greek-warfare-and-the-persian-wars", "Greek Warfare & the Persian Wars",
    "How the Greeks fought - the hoplite and the phalanx, Spartan military society, and the great Persian War battles of Marathon, Thermopylae and Salamis.",
    9, "#1e40af", "#dbeafe", 9, [
    L(1, "The Hoplite & the Phalanx", "The Greek citizen-soldier - the hoplite's equipment and the phalanx formation that made him so effective.",
      "War and Warfare: Greek warfare",
      ["the hoplite citizen-soldier", "hoplite equipment the hoplon shield spear helmet greaves", "the phalanx formation", "fighting in close order", "the importance of holding the line", "the cost of equipment and the hoplite class"]),
    L(2, "Sparta & the Idealisation of War", "The most militarised society in Greece - the Spartan agoge, the warrior ideal and the idealisation of war.",
      "War and Warfare: Spartan society",
      ["the idealisation of war and warfare in Spartan society", "the agoge Spartan military education", "the warrior ideal", "with your shield or on it", "the krypteia", "Spartan discipline and courage"]),
    L(3, "The Battle of Marathon", "The Athenian victory over Persia in 490 BC and why it became so celebrated.",
      "War and Warfare: famous battles",
      ["the battle of Marathon 490 BC", "the Persian invasion of Greece", "the Athenian hoplites against the Persians", "the tactics of Miltiades", "the run to Athens", "why Marathon was celebrated"]),
    L(4, "Thermopylae & the 300", "Leonidas and the Spartans at the pass of Thermopylae in 480 BC - the famous last stand.",
      "War and Warfare: famous battles",
      ["the battle of Thermopylae 480 BC", "Leonidas and the three hundred Spartans", "the pass of Thermopylae", "the betrayal by Ephialtes", "the last stand", "Thermopylae as a symbol of courage and sacrifice"]),
    L(5, "Salamis & Naval Warfare", "The sea battle that saved Greece - the trireme, the battle of Salamis, and naval warfare.",
      "War and Warfare: naval warfare",
      ["the battle of Salamis 480 BC", "naval warfare and the trireme", "the design and crew of a trireme", "ramming tactics", "Themistocles and the Athenian fleet", "the Lenormant Trireme relief", "the importance of sea power"]),
]))

new.append(U("the-roman-army-and-the-values-of-war", "The Roman Army & the Values of War",
    "The Roman war machine - the legion and the legionary, arms, armour and the marching camp, Roman campaigns, and the ideals of heroism and leadership in war.",
    10, "#991b1b", "#fee2e2", 10, [
    L(1, "The Roman Legion", "The organisation of the Roman army - the legion, its subdivisions and the discipline that made it formidable.",
      "War and Warfare: the Roman army",
      ["the Roman army", "the organisation of the legion", "centuries cohorts and the centurion", "the legionary citizen-soldier", "training and discipline", "the strength of the Roman military system"]),
    L(2, "Arms, Armour & the Camp", "The legionary's equipment and the famous Roman marching camp and fortifications.",
      "War and Warfare: material culture",
      ["Roman arms and armour", "the gladius pilum and scutum", "segmented armour lorica segmentata", "the marching camp", "fortifications and the rampart", "engineering and siege equipment"]),
    L(3, "Roman Warfare & Expansion", "How Rome fought and won an empire - campaigns, famous battles and siege warfare.",
      "War and Warfare: famous battles",
      ["Roman warfare and expansion", "famous Roman campaigns and battles", "siege warfare and the testudo", "the conquest of new territory", "the role of the army in expansion", "Roman tactics and adaptability"]),
    L(4, "Heroism & Leadership in War", "The ideals of courage, leadership and glory in Greek and Roman war, and famous commanders.",
      "War and Warfare: values",
      ["heroism and leadership in war", "Greek and Roman ideals of courage", "famous military leaders", "the values of bravery duty and glory", "leadership and the general", "how war was glorified and commemorated"]),
    L(5, "The Material Culture of War", "How war was depicted and remembered - armour, monuments, reliefs and the commemoration of victory.",
      "War and Warfare: material culture",
      ["the material culture of war", "armour and weapons as evidence", "war memorials and monuments", "reliefs depicting battle the Lenormant relief", "the commemoration of victory", "how art presents and idealises war"]),
]))

p["article_units"].extend(new)
p["gaps"][0] = ("This build covers ALL FIVE options of OCR J199 so students select their thematic study "
                "(Myth and Religion OR Women in the Ancient World) and their literature/culture option "
                "(The Homeric World, Roman City Life OR War and Warfare) via the homepage picker. Each option = 2 units.")

P.write_text(json.dumps(p, indent=2, ensure_ascii=False), encoding="utf-8")
print("plan now has", len(p["article_units"]), "units,", sum(u["lesson_count"] for u in p["article_units"]), "lessons")
for u in p["article_units"]:
    print(" ", u["sort_order"], u["name"], u["lesson_count"])
