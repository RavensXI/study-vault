"""
Set up AQA Science lesson plans in Supabase.
Creates Combined Science (48 lessons, 6 units) and Separate Sciences (22 lessons, 3 units).
"""
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

from lib.supabase_client import get_client

COMBINED_JOB_ID = "86b8b3dd-3317-4e7e-ac7c-38aaf7a6cc58"

# Question types for AQA GCSE Science
QUESTION_TYPE_NAMES = [
    "1 mark — Recall",
    "2 marks — Describe",
    "2 marks — Calculate",
    "3 marks — Explain",
    "4 marks — Compare and Explain",
    "6 marks — Extended Response",
]

COMBINED_PLAN = {
    "subject_name": "Science",
    "subject_slug": "science",
    "exam_board": "AQA",
    "spec_code": "8464",
    "question_type_names": QUESTION_TYPE_NAMES,
    "units": [
        {
            "name": "Biology Paper 1",
            "slug": "biology-paper-1",
            "subtitle": "Cell biology, organisation, infection & response, bioenergetics",
            "lesson_count": 8,
            "lessons": [
                {
                    "number": 1,
                    "title": "Cell Structure and Microscopy",
                    "description": "Eukaryotic and prokaryotic cells, sub-cellular structures, and how microscopy reveals the hidden world.",
                    "ppt_section_markers": ["cell structure", "eukaryote", "prokaryote", "microscopy", "animal cell", "plant cell", "specialised cell", "cell differentiation", "magnification"],
                    "spec_references": ["4.1.1.1", "4.1.1.2", "4.1.1.3", "4.1.1.4", "4.1.1.5"],
                },
                {
                    "number": 2,
                    "title": "Cell Division and Transport",
                    "description": "Mitosis, the cell cycle, stem cells, and how substances move in and out of cells.",
                    "ppt_section_markers": ["mitosis", "cell division", "cell cycle", "stem cell", "diffusion", "osmosis", "active transport"],
                    "spec_references": ["4.1.2.1", "4.1.2.2", "4.1.2.3", "4.1.3.1", "4.1.3.2", "4.1.3.3"],
                },
                {
                    "number": 3,
                    "title": "Organisation and the Digestive System",
                    "description": "How cells form tissues, organs and organ systems, with a focus on the human digestive system.",
                    "ppt_section_markers": ["organisation", "digestive system", "enzyme", "bile", "protease", "lipase", "amylase", "stomach", "small intestine"],
                    "spec_references": ["4.2.1", "4.2.2.1"],
                },
                {
                    "number": 4,
                    "title": "The Heart, Blood and Circulatory Disease",
                    "description": "How the heart pumps blood, the components of blood, and the causes of coronary heart disease.",
                    "ppt_section_markers": ["heart", "blood vessel", "artery", "vein", "capillary", "red blood cell", "white blood cell", "platelet", "plasma", "coronary heart disease", "stent"],
                    "spec_references": ["4.2.2.2", "4.2.2.3", "4.2.2.4"],
                },
                {
                    "number": 5,
                    "title": "Health, Non-Communicable Diseases and Plant Tissues",
                    "description": "Risk factors for disease, the link between lifestyle and illness, cancer, and how plants are organised.",
                    "ppt_section_markers": ["health", "non-communicable", "lifestyle", "cancer", "tumour", "benign", "malignant", "risk factor", "plant tissue", "xylem", "phloem", "transpiration"],
                    "spec_references": ["4.2.2.5", "4.2.2.6", "4.2.2.7", "4.2.3.1", "4.2.3.2"],
                },
                {
                    "number": 6,
                    "title": "Communicable Diseases and Human Defences",
                    "description": "How pathogens cause disease, examples of viral, bacterial, fungal and protist infections, and how the body fights back.",
                    "ppt_section_markers": ["communicable disease", "pathogen", "virus", "bacteria", "fungal", "protist", "malaria", "HIV", "measles", "salmonella", "gonorrhoea", "rose black spot", "defence", "white blood cell", "antibody", "phagocytosis"],
                    "spec_references": ["4.3.1.1", "4.3.1.2", "4.3.1.3", "4.3.1.4", "4.3.1.5", "4.3.1.6"],
                },
                {
                    "number": 7,
                    "title": "Vaccination, Antibiotics and Drug Development",
                    "description": "How vaccines protect populations, why antibiotics only work on bacteria, and the journey from discovery to prescription.",
                    "ppt_section_markers": ["vaccination", "vaccine", "herd immunity", "antibiotic", "painkiller", "drug development", "clinical trial", "placebo", "double blind", "penicillin", "digitalis", "aspirin"],
                    "spec_references": ["4.3.1.7", "4.3.1.8", "4.3.1.9"],
                },
                {
                    "number": 8,
                    "title": "Photosynthesis and Respiration",
                    "description": "The equations, factors and uses of photosynthesis, plus aerobic and anaerobic respiration and metabolism.",
                    "ppt_section_markers": ["photosynthesis", "chlorophyll", "light intensity", "carbon dioxide concentration", "glucose", "respiration", "aerobic", "anaerobic", "fermentation", "oxygen debt", "metabolism", "response to exercise"],
                    "spec_references": ["4.4.1.1", "4.4.1.2", "4.4.1.3", "4.4.2.1", "4.4.2.2", "4.4.2.3"],
                },
            ],
        },
        {
            "name": "Biology Paper 2",
            "slug": "biology-paper-2",
            "subtitle": "Homeostasis & response, inheritance, variation & evolution, ecology",
            "lesson_count": 8,
            "lessons": [
                {
                    "number": 1,
                    "title": "Homeostasis and the Nervous System",
                    "description": "Why internal conditions must be regulated and how the nervous system detects and responds to stimuli.",
                    "ppt_section_markers": ["homeostasis", "nervous system", "neurone", "synapse", "reflex arc", "receptor", "effector", "stimulus", "response", "reaction time", "CNS"],
                    "spec_references": ["4.5.1", "4.5.2.1"],
                },
                {
                    "number": 2,
                    "title": "The Endocrine System and Blood Glucose Control",
                    "description": "How hormones coordinate body functions, with a focus on insulin, glucagon and diabetes.",
                    "ppt_section_markers": ["endocrine", "hormone", "pituitary", "insulin", "glucagon", "diabetes", "type 1 diabetes", "type 2 diabetes", "blood glucose", "pancreas", "negative feedback"],
                    "spec_references": ["4.5.3.1", "4.5.3.2", "4.5.3.7"],
                },
                {
                    "number": 3,
                    "title": "Hormones in Reproduction and Contraception",
                    "description": "The roles of FSH, LH, oestrogen and progesterone in the menstrual cycle, plus methods of contraception.",
                    "ppt_section_markers": ["reproduction", "menstrual cycle", "oestrogen", "progesterone", "FSH", "LH", "contraception", "hormonal contraception", "barrier method", "IVF", "infertility", "fertility"],
                    "spec_references": ["4.5.3.4", "4.5.3.5", "4.5.3.6"],
                },
                {
                    "number": 4,
                    "title": "Reproduction, Meiosis and DNA",
                    "description": "Sexual vs asexual reproduction, how meiosis produces gametes, and the role of DNA and the genome.",
                    "ppt_section_markers": ["sexual reproduction", "asexual reproduction", "meiosis", "gamete", "DNA", "genome", "gene", "chromosome", "allele"],
                    "spec_references": ["4.6.1.1", "4.6.1.2", "4.6.1.4"],
                },
                {
                    "number": 5,
                    "title": "Genetic Inheritance and Inherited Disorders",
                    "description": "Punnett squares, dominant and recessive alleles, inherited disorders, and how sex is determined.",
                    "ppt_section_markers": ["genetic inheritance", "Punnett square", "dominant", "recessive", "homozygous", "heterozygous", "genotype", "phenotype", "cystic fibrosis", "polydactyly", "sex determination", "XX", "XY"],
                    "spec_references": ["4.6.1.6", "4.6.1.7", "4.6.1.8"],
                },
                {
                    "number": 6,
                    "title": "Variation, Evolution and Natural Selection",
                    "description": "What causes variation, how natural selection drives evolution, and the evidence including fossils and resistant bacteria.",
                    "ppt_section_markers": ["variation", "evolution", "natural selection", "mutation", "selective breeding", "fossil", "extinction", "antibiotic resistance", "resistant bacteria", "evidence for evolution"],
                    "spec_references": ["4.6.2.1", "4.6.2.2", "4.6.2.3", "4.6.3.4", "4.6.3.5", "4.6.3.6", "4.6.3.7"],
                },
                {
                    "number": 7,
                    "title": "Genetic Engineering and Ecology",
                    "description": "How genetic engineering works, classification of organisms, and the factors that shape ecosystems.",
                    "ppt_section_markers": ["genetic engineering", "GM", "classification", "ecosystem", "community", "habitat", "population", "abiotic", "biotic", "adaptation", "competition", "interdependence"],
                    "spec_references": ["4.6.2.4", "4.6.4", "4.7.1.1", "4.7.1.2", "4.7.1.3", "4.7.1.4"],
                },
                {
                    "number": 8,
                    "title": "Ecosystems, Biodiversity and Human Impact",
                    "description": "How materials cycle through ecosystems, the threats to biodiversity, and what we can do to protect the environment.",
                    "ppt_section_markers": ["ecosystem", "carbon cycle", "water cycle", "biodiversity", "deforestation", "global warming", "greenhouse", "waste management", "land use", "maintaining biodiversity", "quadrat", "sampling"],
                    "spec_references": ["4.7.2.1", "4.7.2.2", "4.7.3.1", "4.7.3.2", "4.7.3.3", "4.7.3.4", "4.7.3.5", "4.7.3.6"],
                },
            ],
        },
        {
            "name": "Chemistry Paper 1",
            "slug": "chemistry-paper-1",
            "subtitle": "Atomic structure, bonding, quantitative chemistry, chemical changes, energy changes",
            "lesson_count": 9,
            "lessons": [
                {
                    "number": 1,
                    "title": "Atoms, Elements, Compounds and the Model of the Atom",
                    "description": "The structure of atoms, how the atomic model has developed over time, and how to read the periodic table.",
                    "ppt_section_markers": ["atom", "element", "compound", "mixture", "proton", "neutron", "electron", "atomic number", "mass number", "isotope", "model of the atom", "plum pudding", "Rutherford", "Bohr", "electronic structure"],
                    "spec_references": ["4.1.1.1", "4.1.1.2", "4.1.1.3", "4.1.1.4", "4.1.1.5", "4.1.1.6", "4.1.1.7"],
                },
                {
                    "number": 2,
                    "title": "The Periodic Table and Its Groups",
                    "description": "How elements are arranged, trends across periods and down groups, and the properties of Groups 0, 1 and 7.",
                    "ppt_section_markers": ["periodic table", "group 1", "group 7", "group 0", "alkali metal", "halogen", "noble gas", "metals and non-metals", "Mendeleev", "trend"],
                    "spec_references": ["4.1.2.1", "4.1.2.2", "4.1.2.3", "4.1.2.4", "4.1.2.5", "4.1.2.6"],
                },
                {
                    "number": 3,
                    "title": "Ionic, Covalent and Metallic Bonding",
                    "description": "How atoms bond by transferring or sharing electrons, and how metallic bonding holds metals together.",
                    "ppt_section_markers": ["ionic bond", "covalent bond", "metallic bond", "ion", "electron transfer", "electron sharing", "dot and cross", "ionic compound", "giant lattice"],
                    "spec_references": ["4.2.1.1", "4.2.1.2", "4.2.1.3", "4.2.1.4", "4.2.1.5"],
                },
                {
                    "number": 4,
                    "title": "Structure, Properties and Carbon Allotropes",
                    "description": "How bonding affects properties, states of matter, and the structures of diamond, graphite and graphene.",
                    "ppt_section_markers": ["states of matter", "ionic properties", "covalent properties", "polymer", "giant covalent", "alloy", "diamond", "graphite", "graphene", "fullerene", "conductor"],
                    "spec_references": ["4.2.2.1", "4.2.2.2", "4.2.2.3", "4.2.2.4", "4.2.2.5", "4.2.2.6", "4.2.2.7", "4.2.2.8", "4.2.3.1", "4.2.3.2", "4.2.3.3"],
                },
                {
                    "number": 5,
                    "title": "Quantitative Chemistry: Mass, Moles and Concentrations",
                    "description": "Conservation of mass, relative formula mass, mole calculations, and working with solution concentrations.",
                    "ppt_section_markers": ["conservation of mass", "relative formula mass", "Mr", "mole", "Avogadro", "concentration", "balanced equation", "limiting reactant", "reacting mass"],
                    "spec_references": ["4.3.1.1", "4.3.1.2", "4.3.1.3", "4.3.1.4", "4.3.2.1", "4.3.2.2", "4.3.2.3", "4.3.2.4", "4.3.2.5"],
                },
                {
                    "number": 6,
                    "title": "Reactivity of Metals and Metal Extraction",
                    "description": "The reactivity series, displacement reactions, how metals are extracted from ores, and oxidation and reduction.",
                    "ppt_section_markers": ["reactivity series", "displacement", "metal oxide", "extraction", "reduction", "oxidation", "carbon", "blast furnace", "ore", "thermite"],
                    "spec_references": ["4.4.1.1", "4.4.1.2", "4.4.1.3", "4.4.1.4"],
                },
                {
                    "number": 7,
                    "title": "Reactions of Acids, pH and Neutralisation",
                    "description": "How acids react with metals, bases and carbonates, the pH scale, and strong vs weak acids.",
                    "ppt_section_markers": ["acid", "alkali", "base", "neutralisation", "pH", "salt", "hydrogen", "carbonate", "metal hydroxide", "indicator", "universal indicator", "strong acid", "weak acid"],
                    "spec_references": ["4.4.2.1", "4.4.2.2", "4.4.2.3", "4.4.2.4", "4.4.2.6"],
                },
                {
                    "number": 8,
                    "title": "Electrolysis",
                    "description": "How ionic compounds are broken down by electricity, including molten and aqueous electrolysis.",
                    "ppt_section_markers": ["electrolysis", "electrode", "anode", "cathode", "electrolyte", "molten", "aqueous", "aluminium extraction", "brine", "half equation"],
                    "spec_references": ["4.4.3.1", "4.4.3.2", "4.4.3.3", "4.4.3.4", "4.4.3.5"],
                },
                {
                    "number": 9,
                    "title": "Energy Changes in Chemical Reactions",
                    "description": "Exothermic and endothermic reactions, reaction profiles, and bond energy calculations.",
                    "ppt_section_markers": ["exothermic", "endothermic", "energy change", "reaction profile", "activation energy", "bond energy", "temperature change", "hand warmer", "cold pack"],
                    "spec_references": ["4.5.1.1", "4.5.1.2", "4.5.1.3"],
                },
            ],
        },
        {
            "name": "Chemistry Paper 2",
            "slug": "chemistry-paper-2",
            "subtitle": "Rates of reaction, organic chemistry, chemical analysis, atmosphere, resources",
            "lesson_count": 7,
            "lessons": [
                {
                    "number": 1,
                    "title": "Rates of Reaction and Collision Theory",
                    "description": "How to measure and calculate reaction rates, what affects them, and how collision theory explains why.",
                    "ppt_section_markers": ["rate of reaction", "collision theory", "activation energy", "catalyst", "surface area", "concentration", "temperature", "gas syringe", "marble chips"],
                    "spec_references": ["4.6.1.1", "4.6.1.2", "4.6.1.3", "4.6.1.4"],
                },
                {
                    "number": 2,
                    "title": "Reversible Reactions and Equilibrium",
                    "description": "Reactions that go both ways, dynamic equilibrium, and how changing conditions shifts the balance.",
                    "ppt_section_markers": ["reversible reaction", "equilibrium", "dynamic equilibrium", "Le Chatelier", "ammonium chloride", "hydrated copper sulfate"],
                    "spec_references": ["4.6.2.1", "4.6.2.2", "4.6.2.3", "4.6.2.4", "4.6.2.5", "4.6.2.6", "4.6.2.7"],
                },
                {
                    "number": 3,
                    "title": "Crude Oil, Hydrocarbons and Cracking",
                    "description": "How crude oil is separated by fractional distillation, the properties of hydrocarbons, and why cracking is important.",
                    "ppt_section_markers": ["crude oil", "hydrocarbon", "alkane", "fractional distillation", "fraction", "viscosity", "flammability", "cracking", "alkene", "petrochemical"],
                    "spec_references": ["4.7.1.1", "4.7.1.2", "4.7.1.3", "4.7.1.4"],
                },
                {
                    "number": 4,
                    "title": "Chemical Analysis: Purity, Chromatography and Gas Tests",
                    "description": "How to test for pure substances, separate mixtures using chromatography, and identify common gases.",
                    "ppt_section_markers": ["pure substance", "formulation", "chromatography", "Rf value", "gas test", "hydrogen", "oxygen", "carbon dioxide", "chlorine", "limewater", "squeaky pop"],
                    "spec_references": ["4.8.1.1", "4.8.1.2", "4.8.1.3", "4.8.2.1", "4.8.2.2", "4.8.2.3", "4.8.2.4"],
                },
                {
                    "number": 5,
                    "title": "The Earth's Atmosphere and Greenhouse Effect",
                    "description": "How the atmosphere evolved, what greenhouse gases do, and the human impact on climate change.",
                    "ppt_section_markers": ["atmosphere", "greenhouse gas", "greenhouse effect", "carbon dioxide", "methane", "global warming", "climate change", "carbon footprint", "early atmosphere", "oxygen"],
                    "spec_references": ["4.9.1.1", "4.9.1.2", "4.9.1.3", "4.9.1.4", "4.9.2.1", "4.9.2.2", "4.9.2.3", "4.9.2.4"],
                },
                {
                    "number": 6,
                    "title": "Atmospheric Pollutants and Their Effects",
                    "description": "Where pollutants like carbon monoxide, sulfur dioxide and particulates come from, and the damage they cause.",
                    "ppt_section_markers": ["pollutant", "carbon monoxide", "sulfur dioxide", "nitrogen oxide", "particulate", "acid rain", "global dimming", "incomplete combustion"],
                    "spec_references": ["4.9.3.1", "4.9.3.2"],
                },
                {
                    "number": 7,
                    "title": "Using Earth's Resources and Sustainability",
                    "description": "How we use natural resources, making water safe to drink, life cycle assessments, and reducing our impact.",
                    "ppt_section_markers": ["natural resource", "sustainable", "potable water", "desalination", "waste water", "sewage", "life cycle assessment", "recycling", "reduce reuse recycle", "phytomining", "bioleaching"],
                    "spec_references": ["4.10.1.1", "4.10.1.2", "4.10.1.3", "4.10.1.4", "4.10.2.1", "4.10.2.2"],
                },
            ],
        },
        {
            "name": "Physics Paper 1",
            "slug": "physics-paper-1",
            "subtitle": "Energy, electricity, particle model of matter, atomic structure",
            "lesson_count": 8,
            "lessons": [
                {
                    "number": 1,
                    "title": "Energy Stores, Transfers and Power",
                    "description": "The different energy stores, how energy is transferred between them, and what power means.",
                    "ppt_section_markers": ["energy store", "energy transfer", "kinetic energy", "gravitational potential", "elastic potential", "thermal energy", "chemical energy", "power", "work done", "joule"],
                    "spec_references": ["4.1.1.1", "4.1.1.2", "4.1.1.3", "4.1.1.4"],
                },
                {
                    "number": 2,
                    "title": "Conservation of Energy, Efficiency and Energy Resources",
                    "description": "Why energy is always conserved, how to calculate efficiency, and the pros and cons of renewable and non-renewable resources.",
                    "ppt_section_markers": ["conservation of energy", "dissipation", "efficiency", "wasted energy", "renewable", "non-renewable", "fossil fuel", "nuclear", "solar", "wind", "hydroelectric", "geothermal", "tidal"],
                    "spec_references": ["4.1.2.1", "4.1.2.2", "4.1.3"],
                },
                {
                    "number": 3,
                    "title": "Circuits: Current, Resistance and Potential Difference",
                    "description": "What current, resistance and potential difference are, Ohm's law, and how to investigate I-V characteristics.",
                    "ppt_section_markers": ["current", "resistance", "potential difference", "voltage", "Ohm", "V=IR", "ammeter", "voltmeter", "circuit", "filament lamp", "diode", "LDR", "thermistor", "I-V"],
                    "spec_references": ["4.2.1.1", "4.2.1.2", "4.2.1.3", "4.2.1.4"],
                },
                {
                    "number": 4,
                    "title": "Series and Parallel Circuits",
                    "description": "How current and voltage behave in series and parallel circuits, and how to calculate total resistance.",
                    "ppt_section_markers": ["series circuit", "parallel circuit", "series", "parallel", "total resistance", "current in series", "voltage in parallel"],
                    "spec_references": ["4.2.2"],
                },
                {
                    "number": 5,
                    "title": "Domestic Electricity, Power and the National Grid",
                    "description": "AC vs DC, the three-pin plug, electrical safety, calculating power and energy, and how the National Grid works.",
                    "ppt_section_markers": ["AC", "DC", "alternating current", "direct current", "mains electricity", "plug", "earth wire", "live wire", "neutral", "fuse", "circuit breaker", "power", "P=IV", "E=Pt", "national grid", "transformer", "step up", "step down"],
                    "spec_references": ["4.2.3.1", "4.2.3.2", "4.2.4.1", "4.2.4.2", "4.2.4.3"],
                },
                {
                    "number": 6,
                    "title": "Density, States of Matter and Changes of State",
                    "description": "What density is and how to measure it, the particle model of states, and what happens during changes of state.",
                    "ppt_section_markers": ["density", "mass", "volume", "state of matter", "solid", "liquid", "gas", "melting", "boiling", "evaporation", "condensation", "sublimation", "particle model"],
                    "spec_references": ["4.3.1.1", "4.3.1.2"],
                },
                {
                    "number": 7,
                    "title": "Internal Energy, Specific Heat Capacity and Latent Heat",
                    "description": "How heating a substance changes its internal energy, and calculations involving SHC and specific latent heat.",
                    "ppt_section_markers": ["internal energy", "specific heat capacity", "SHC", "latent heat", "specific latent heat", "fusion", "vaporisation", "particle motion", "heating curve"],
                    "spec_references": ["4.3.2.1", "4.3.2.2", "4.3.2.3", "4.3.3.1"],
                },
                {
                    "number": 8,
                    "title": "Atomic Structure, Radioactivity and Half-Life",
                    "description": "The structure of atoms, types of nuclear radiation, radioactive decay equations, and the concept of half-life.",
                    "ppt_section_markers": ["atomic structure", "radioactive", "alpha", "beta", "gamma", "decay", "half-life", "nuclear equation", "contamination", "irradiation", "isotope", "nuclear radiation"],
                    "spec_references": ["4.4.1.1", "4.4.1.2", "4.4.1.3", "4.4.2.1", "4.4.2.2", "4.4.2.3", "4.4.2.4"],
                },
            ],
        },
        {
            "name": "Physics Paper 2",
            "slug": "physics-paper-2",
            "subtitle": "Forces, waves, magnetism & electromagnetism",
            "lesson_count": 8,
            "lessons": [
                {
                    "number": 1,
                    "title": "Forces, Gravity and Resultant Forces",
                    "description": "Scalar vs vector quantities, contact and non-contact forces, gravity, weight, and finding resultant forces.",
                    "ppt_section_markers": ["scalar", "vector", "force", "contact force", "non-contact", "gravity", "gravitational field", "weight", "mass", "resultant force", "free body diagram"],
                    "spec_references": ["4.5.1.1", "4.5.1.2", "4.5.1.3", "4.5.1.4"],
                },
                {
                    "number": 2,
                    "title": "Work Done, Elasticity and Hooke's Law",
                    "description": "How forces do work to transfer energy, elastic and inelastic deformation, and the spring constant.",
                    "ppt_section_markers": ["work done", "W=Fs", "elastic", "inelastic", "Hooke", "spring constant", "extension", "limit of proportionality", "force extension", "elastic potential energy"],
                    "spec_references": ["4.5.2", "4.5.3"],
                },
                {
                    "number": 3,
                    "title": "Speed, Velocity and Acceleration",
                    "description": "Distance vs displacement, speed vs velocity, distance-time and velocity-time graphs, and calculating acceleration.",
                    "ppt_section_markers": ["speed", "velocity", "acceleration", "distance-time", "velocity-time", "gradient", "area under graph", "displacement", "uniform acceleration", "v=s/t", "a=(v-u)/t"],
                    "spec_references": ["4.5.6.1.1", "4.5.6.1.2", "4.5.6.1.3", "4.5.6.1.4", "4.5.6.1.5"],
                },
                {
                    "number": 4,
                    "title": "Newton's Laws of Motion",
                    "description": "Newton's three laws, inertia, F=ma calculations, and action-reaction force pairs.",
                    "ppt_section_markers": ["Newton", "first law", "second law", "third law", "F=ma", "inertia", "inertial mass", "action reaction", "equilibrium", "terminal velocity"],
                    "spec_references": ["4.5.6.2.1", "4.5.6.2.2", "4.5.6.2.3"],
                },
                {
                    "number": 5,
                    "title": "Stopping Distances, Braking and Momentum",
                    "description": "Reaction time, thinking and braking distance, factors affecting stopping, and conservation of momentum.",
                    "ppt_section_markers": ["stopping distance", "thinking distance", "braking distance", "reaction time", "braking force", "momentum", "conservation of momentum", "p=mv"],
                    "spec_references": ["4.5.6.3.1", "4.5.6.3.2", "4.5.6.3.3", "4.5.6.3.4", "4.5.7.1", "4.5.7.2"],
                },
                {
                    "number": 6,
                    "title": "Waves: Properties and Behaviour",
                    "description": "Transverse and longitudinal waves, amplitude, frequency, wavelength, wave speed, and the wave equation.",
                    "ppt_section_markers": ["transverse wave", "longitudinal wave", "amplitude", "wavelength", "frequency", "wave speed", "v=f lambda", "period", "oscillation", "ripple tank"],
                    "spec_references": ["4.6.1.1", "4.6.1.2"],
                },
                {
                    "number": 7,
                    "title": "The Electromagnetic Spectrum",
                    "description": "The types of electromagnetic waves, their properties, uses, and dangers across the spectrum.",
                    "ppt_section_markers": ["electromagnetic", "EM spectrum", "radio", "microwave", "infrared", "visible light", "ultraviolet", "X-ray", "gamma ray", "ionising"],
                    "spec_references": ["4.6.2.1", "4.6.2.2", "4.6.2.3", "4.6.2.4"],
                },
                {
                    "number": 8,
                    "title": "Magnets, Electromagnetism and the Motor Effect",
                    "description": "Permanent and induced magnets, magnetic fields, electromagnets, Fleming's left-hand rule, and electric motors.",
                    "ppt_section_markers": ["magnet", "magnetic field", "north pole", "south pole", "electromagnet", "solenoid", "motor effect", "Fleming", "left-hand rule", "electric motor", "force on conductor"],
                    "spec_references": ["4.7.1.1", "4.7.1.2", "4.7.2.1", "4.7.2.2", "4.7.2.3"],
                },
            ],
        },
    ],
    "gaps": [],
}


SEPARATE_PLAN = {
    "subject_name": "Separate Sciences",
    "subject_slug": "separate-sciences",
    "exam_board": "AQA",
    "spec_code": "8461/8462/8463",
    "question_type_names": QUESTION_TYPE_NAMES,
    "units": [
        {
            "name": "Biology (Separate)",
            "slug": "biology-separate",
            "subtitle": "Additional biology content for triple science students",
            "lesson_count": 7,
            "lessons": [
                {
                    "number": 1,
                    "title": "Culturing Microorganisms and Plant Disease",
                    "description": "Aseptic technique for growing bacteria, and how to detect and identify diseases in plants.",
                    "ppt_section_markers": ["culturing microorganisms", "agar", "aseptic technique", "zone of inhibition", "plant disease", "ion deficiency", "aphid", "plant defence"],
                    "spec_references": ["4.1.1.6", "4.3.3.1", "4.3.3.2"],
                },
                {
                    "number": 2,
                    "title": "Monoclonal Antibodies",
                    "description": "How monoclonal antibodies are produced using hybridoma cells, and their uses in diagnosis and treatment.",
                    "ppt_section_markers": ["monoclonal antibody", "hybridoma", "lymphocyte", "tumour cell", "pregnancy test", "cancer treatment"],
                    "spec_references": ["4.3.2.1", "4.3.2.2"],
                },
                {
                    "number": 3,
                    "title": "The Brain, the Eye and Temperature Control",
                    "description": "The structure and function of the brain, how the eye focuses light, and thermoregulation in the body.",
                    "ppt_section_markers": ["brain", "cerebral cortex", "cerebellum", "medulla", "eye", "retina", "cornea", "iris", "lens", "ciliary muscle", "suspensory ligament", "accommodation", "thermoregulation", "vasodilation", "vasoconstriction", "body temperature"],
                    "spec_references": ["4.5.2.2", "4.5.2.3", "4.5.2.4"],
                },
                {
                    "number": 4,
                    "title": "The Kidney, Water Balance and Plant Hormones",
                    "description": "How the kidneys filter blood and regulate water, dialysis and transplants, and how auxins control plant growth.",
                    "ppt_section_markers": ["kidney", "nephron", "ADH", "osmoregulation", "dialysis", "kidney transplant", "urea", "plant hormone", "auxin", "gibberellin", "tropism", "phototropism", "gravitropism"],
                    "spec_references": ["4.5.3.3", "4.5.4.1", "4.5.4.2"],
                },
                {
                    "number": 5,
                    "title": "DNA Structure, Cloning and the History of Genetics",
                    "description": "The double helix, protein synthesis, cloning techniques, and how Darwin, Wallace and Mendel shaped genetics.",
                    "ppt_section_markers": ["DNA structure", "double helix", "nucleotide", "base pairing", "protein synthesis", "cloning", "tissue culture", "cutting", "embryo transplant", "Darwin", "Wallace", "Mendel", "speciation", "geographical isolation"],
                    "spec_references": ["4.6.1.3", "4.6.1.5", "4.6.2.5", "4.6.3.1", "4.6.3.2", "4.6.3.3"],
                },
                {
                    "number": 6,
                    "title": "Trophic Levels and Transfer of Biomass",
                    "description": "Food chains, trophic levels, pyramids of biomass, and how energy is lost between levels.",
                    "ppt_section_markers": ["trophic level", "producer", "primary consumer", "secondary consumer", "pyramid of biomass", "biomass transfer", "food chain", "food web", "energy transfer", "10% rule"],
                    "spec_references": ["4.7.4.1", "4.7.4.2", "4.7.4.3"],
                },
                {
                    "number": 7,
                    "title": "Decomposition, Food Security and Biotechnology",
                    "description": "How decomposition works, threats to food security, sustainable farming, and the role of biotechnology.",
                    "ppt_section_markers": ["decomposition", "decay", "compost", "food security", "farming", "sustainable fisheries", "biotechnology", "mycoprotein", "Quorn", "GM crops", "environmental change"],
                    "spec_references": ["4.7.2.3", "4.7.2.4", "4.7.5.1", "4.7.5.2", "4.7.5.3", "4.7.5.4"],
                },
            ],
        },
        {
            "name": "Chemistry (Separate)",
            "slug": "chemistry-separate",
            "subtitle": "Additional chemistry content for triple science students",
            "lesson_count": 7,
            "lessons": [
                {
                    "number": 1,
                    "title": "Transition Metals and Nanoparticles",
                    "description": "Properties of transition metals compared to Group 1, and how nanoparticles behave differently to bulk materials.",
                    "ppt_section_markers": ["transition metal", "Group 1", "catalyst", "coloured compound", "nanoparticle", "surface area to volume", "nanoparticle uses", "sunscreen"],
                    "spec_references": ["4.1.3.1", "4.1.3.2", "4.2.4.1", "4.2.4.2"],
                },
                {
                    "number": 2,
                    "title": "Yield, Atom Economy, Molar Concentrations and Gas Volumes",
                    "description": "Calculating percentage yield and atom economy, concentrations in mol/dm3, and the molar volume of gases.",
                    "ppt_section_markers": ["percentage yield", "atom economy", "mol/dm3", "molar concentration", "molar volume", "gas volume", "24 dm3"],
                    "spec_references": ["4.3.3.1", "4.3.3.2", "4.3.4", "4.3.5"],
                },
                {
                    "number": 3,
                    "title": "Titrations, Chemical Cells and Fuel Cells",
                    "description": "How to carry out an acid-alkali titration, how chemical cells generate electricity, and how hydrogen fuel cells work.",
                    "ppt_section_markers": ["titration", "burette", "pipette", "end point", "concordant", "indicator", "chemical cell", "battery", "fuel cell", "hydrogen fuel cell"],
                    "spec_references": ["4.4.2.5", "4.5.2.1", "4.5.2.2"],
                },
                {
                    "number": 4,
                    "title": "Alkenes, Alcohols and Carboxylic Acids",
                    "description": "The structure and reactions of alkenes, alcohols and carboxylic acids as functional group chemistry.",
                    "ppt_section_markers": ["alkene", "C=C", "double bond", "addition reaction", "bromine water", "alcohol", "methanol", "ethanol", "fermentation", "carboxylic acid", "ethanoic acid", "functional group"],
                    "spec_references": ["4.7.2.1", "4.7.2.2", "4.7.2.3", "4.7.2.4"],
                },
                {
                    "number": 5,
                    "title": "Polymers: Addition, Condensation and Natural",
                    "description": "How addition and condensation polymerisation work, amino acids, and naturally occurring polymers like DNA and starch.",
                    "ppt_section_markers": ["addition polymerisation", "condensation polymerisation", "monomer", "polymer", "amino acid", "protein", "DNA", "starch", "naturally occurring polymer"],
                    "spec_references": ["4.7.3.1", "4.7.3.2", "4.7.3.3", "4.7.3.4"],
                },
                {
                    "number": 6,
                    "title": "Chemical Tests for Ions",
                    "description": "Flame tests, testing for metal hydroxides, carbonates, halides and sulfates, and instrumental methods of analysis.",
                    "ppt_section_markers": ["flame test", "metal hydroxide", "precipitate", "carbonate", "halide", "sulfate", "instrumental method", "flame emission spectroscopy", "ion test", "sodium hydroxide"],
                    "spec_references": ["4.8.3.1", "4.8.3.2", "4.8.3.3", "4.8.3.4", "4.8.3.5", "4.8.3.6", "4.8.3.7"],
                },
                {
                    "number": 7,
                    "title": "Materials, Corrosion, Haber Process and Fertilisers",
                    "description": "Preventing corrosion, uses of alloys and composites, the Haber process for making ammonia, and NPK fertilisers.",
                    "ppt_section_markers": ["corrosion", "rust", "alloy", "ceramic", "composite", "Haber process", "ammonia", "NPK", "fertiliser", "nitrogen", "reversible"],
                    "spec_references": ["4.10.3.1", "4.10.3.2", "4.10.3.3", "4.10.4.1", "4.10.4.2"],
                },
            ],
        },
        {
            "name": "Physics (Separate)",
            "slug": "physics-separate",
            "subtitle": "Additional physics content for triple science students",
            "lesson_count": 8,
            "lessons": [
                {
                    "number": 1,
                    "title": "Static Electricity and Electric Fields",
                    "description": "How static charge builds up, the dangers and uses of static electricity, and the shape of electric fields.",
                    "ppt_section_markers": ["static electricity", "static charge", "electron transfer", "earthing", "electric field", "field lines", "Van de Graaff", "sparking"],
                    "spec_references": ["4.2.5.1", "4.2.5.2"],
                },
                {
                    "number": 2,
                    "title": "Gas Pressure and Pressure in Fluids",
                    "description": "How gas pressure relates to temperature and volume, pressure in liquids, atmospheric pressure, and upthrust.",
                    "ppt_section_markers": ["gas pressure", "pressure volume", "Boyle", "pressure in fluid", "atmospheric pressure", "upthrust", "column of liquid", "P=hpg"],
                    "spec_references": ["4.3.3.2", "4.3.3.3", "4.5.5.1", "4.5.5.2"],
                },
                {
                    "number": 3,
                    "title": "Nuclear Radiation: Uses, Fission and Fusion",
                    "description": "Background radiation sources, using radioactive isotopes in medicine and industry, and how nuclear power works.",
                    "ppt_section_markers": ["background radiation", "uses of nuclear radiation", "medical tracer", "nuclear fission", "nuclear fusion", "chain reaction", "control rod", "moderator", "nuclear reactor", "star formation"],
                    "spec_references": ["4.4.3.1", "4.4.3.2", "4.4.3.3", "4.4.4.1", "4.4.4.2"],
                },
                {
                    "number": 4,
                    "title": "Moments, Levers, Gears and Momentum Changes",
                    "description": "Calculating moments, how levers and gears multiply forces, and the relationship between force and rate of change of momentum.",
                    "ppt_section_markers": ["moment", "lever", "gear", "pivot", "turning effect", "torque", "change in momentum", "rate of change", "impulse", "F=mv/t", "crumple zone", "air bag"],
                    "spec_references": ["4.5.4", "4.5.7.3"],
                },
                {
                    "number": 5,
                    "title": "Reflection, Sound Waves and Waves for Detection",
                    "description": "The law of reflection, how sound waves travel, ultrasound applications, and using seismic waves to explore the Earth.",
                    "ppt_section_markers": ["reflection", "law of reflection", "normal", "angle of incidence", "sound wave", "ultrasound", "echo", "sonar", "seismic wave", "P-wave", "S-wave", "earthquake"],
                    "spec_references": ["4.6.1.3", "4.6.1.4", "4.6.1.5"],
                },
                {
                    "number": 6,
                    "title": "Lenses, Visible Light and Black Body Radiation",
                    "description": "How convex and concave lenses form images, colour filters, and how all objects emit and absorb infrared radiation.",
                    "ppt_section_markers": ["lens", "convex", "concave", "focal point", "magnification", "real image", "virtual image", "colour filter", "spectrum", "black body", "infrared", "emission", "absorption"],
                    "spec_references": ["4.6.2.5", "4.6.2.6", "4.6.3.1", "4.6.3.2"],
                },
                {
                    "number": 7,
                    "title": "Electromagnetic Induction and Transformers",
                    "description": "The generator effect, how alternators and dynamos work, microphones, and step-up and step-down transformers.",
                    "ppt_section_markers": ["induced potential", "generator effect", "alternator", "dynamo", "microphone", "loudspeaker", "transformer", "step up", "step down", "Vs/Vp", "turns ratio"],
                    "spec_references": ["4.7.2.4", "4.7.3.1", "4.7.3.2", "4.7.3.3", "4.7.3.4"],
                },
                {
                    "number": 8,
                    "title": "Space Physics: The Solar System and Beyond",
                    "description": "Our solar system, the life cycle of stars, orbital motion, and evidence for the Big Bang and expanding universe.",
                    "ppt_section_markers": ["solar system", "planet", "star", "main sequence", "red giant", "white dwarf", "supernova", "neutron star", "black hole", "red-shift", "Big Bang", "dark matter", "dark energy", "satellite", "orbit"],
                    "spec_references": ["4.8.1.1", "4.8.1.2", "4.8.1.3", "4.8.2"],
                },
            ],
        },
    ],
    "gaps": [],
}


def main():
    sb = get_client()

    # --- COMBINED SCIENCE ---
    print("Saving Combined Science lesson plan to Supabase...")
    sb.table("upload_jobs").update({
        "lesson_plan": COMBINED_PLAN,
    }).eq("id", COMBINED_JOB_ID).execute()
    print(f"  Saved to job {COMBINED_JOB_ID}")

    # Count lessons
    combined_total = sum(u["lesson_count"] for u in COMBINED_PLAN["units"])
    print(f"  Combined Science: {combined_total} lessons across {len(COMBINED_PLAN['units'])} units")

    # Create pipeline_steps for Combined Science
    print("  Creating pipeline_steps...")
    for unit in COMBINED_PLAN["units"]:
        for lesson in unit["lessons"]:
            step = {
                "job_id": COMBINED_JOB_ID,
                "unit_slug": unit["slug"],
                "lesson_number": lesson["number"],
                "lesson_title": lesson["title"],
                "subject_slug": "science",
                "content_done": False,
                "questions_done": False,
                "glossary_done": False,
                "diagrams_done": False,
                "hero_done": False,
                "narration_done": False,
                "media_done": False,
            }
            sb.table("pipeline_steps").upsert(
                step, on_conflict="job_id,unit_slug,lesson_number"
            ).execute()
    print(f"  Created {combined_total} pipeline steps")

    # --- SEPARATE SCIENCES ---
    # Create a new upload_jobs record for Separate Sciences
    print("\nCreating Separate Sciences upload job...")
    separate_job = {
        "filename": "Separate Sciences (from science upload)",
        "status": "pending",
        "subject_slug": "separate-sciences",
        "subject_config": {
            "subject_name": "Separate Sciences",
            "exam_board": "AQA",
            "spec_code": "8461/8462/8463",
        },
        "current_phase": "generating",
        "lesson_plan": SEPARATE_PLAN,
        "extracted_text": "",  # Source text is in the combined job
    }

    # Get school_id from the combined job
    combined_job = sb.table("upload_jobs").select("school_id").eq("id", COMBINED_JOB_ID).single().execute()
    if combined_job.data.get("school_id"):
        separate_job["school_id"] = combined_job.data["school_id"]

    result = sb.table("upload_jobs").insert(separate_job).execute()
    separate_job_id = result.data[0]["id"]
    print(f"  Created job {separate_job_id}")

    separate_total = sum(u["lesson_count"] for u in SEPARATE_PLAN["units"])
    print(f"  Separate Sciences: {separate_total} lessons across {len(SEPARATE_PLAN['units'])} units")

    # Create pipeline_steps for Separate Sciences
    print("  Creating pipeline_steps...")
    for unit in SEPARATE_PLAN["units"]:
        for lesson in unit["lessons"]:
            step = {
                "job_id": separate_job_id,
                "unit_slug": unit["slug"],
                "lesson_number": lesson["number"],
                "lesson_title": lesson["title"],
                "subject_slug": "separate-sciences",
                "content_done": False,
                "questions_done": False,
                "glossary_done": False,
                "diagrams_done": False,
                "hero_done": False,
                "narration_done": False,
                "media_done": False,
            }
            sb.table("pipeline_steps").upsert(
                step, on_conflict="job_id,unit_slug,lesson_number"
            ).execute()
    print(f"  Created {separate_total} pipeline steps")

    # --- SUMMARY ---
    print(f"\n{'=' * 60}")
    print(f"SETUP COMPLETE")
    print(f"{'=' * 60}")
    print(f"Combined Science (Trilogy 8464):  {combined_total} lessons, 6 units")
    print(f"  Job ID: {COMBINED_JOB_ID}")
    print(f"Separate Sciences (8461/62/63):  {separate_total} lessons, 3 units")
    print(f"  Job ID: {separate_job_id}")
    print(f"Total: {combined_total + separate_total} lessons")
    print(f"\nQuestion types: {', '.join(QUESTION_TYPE_NAMES)}")
    print(f"\nNext: Run CSS + activation agent, then content generation agents")


if __name__ == "__main__":
    main()
