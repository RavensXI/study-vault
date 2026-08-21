/* ============================================
   Lesson widget embed — inline strip + modal.

   A widget is 400-600px tall; dropping that into the middle of the prose
   costs a screenful of scrolling and breaks the reading. So the lesson
   carries a compact strip (~110px) saying what the interactive is and
   what you will do, and the widget itself opens in a modal — which on a
   phone is a genuine upgrade, since full screen is more room, not less.

   The widget file is fetched only when the student opens it, so a lesson
   nobody interacts with pays nothing.
   ============================================ */
(function () {
  'use strict';

  var MAP = {
    "astronomy-edexcel/telescopic-astronomy/11": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Radio Telescopes"
    },
    "astronomy-edexcel/telescopic-astronomy/14": {
      file: "redshift-stretching-mechanism",
      label: "Predict the spectral shift",
      line: "Give a galaxy's speed and direction, then say where its hydrogen lines land in the light that reaches Earth.",
      after: "The Redshift Formula"
    },
    "business-aqa/finance/2": {
      file: "profit-vs-cash-not-interchangeable",
      label: "Predict profit, then cash",
      line: "One month of a small business — work out what it earned, and what is actually in the bank.",
      after: "Reading a Cash-Flow Forecast"
    },
    "business-edexcel/investigating-small-business/8": {
      file: "profit-vs-cash-not-interchangeable",
      label: "Predict profit, then cash",
      line: "One month of a small business — work out what it earned, and what is actually in the bank.",
      after: "Reading a Cash-Flow Forecast"
    },
    "cambridge-nationals-engineering-programmable-systems/principles-of-electronic-and-programmable-systems/2": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Ohm's Law: V = I × R"
    },
    "classical-civilisation-ocr/greek-warfare-and-the-persian-wars/5": {
      file: "trireme-coordinated-maneuvering",
      label: "Give the order at Salamis",
      line: "Read the water ahead — the gap, the flank, the sea room — and decide where a trireme's ram can actually strike.",
      after: "The Battle and Artemisia"
    },
    "computer-science-aqa/algorithms/3": {
      file: "binary-search-requires-sorted-data",
      label: "Trace the binary search",
      line: "Predict what the search checks, and whether it finds the target at all — on lists that are not always sorted.",
      after: "Choosing the Right Algorithm"
    },
    "computer-science-aqa/computer-systems/2": {
      file: "fetch-decode-simultaneous",
      label: "Predict what each stage changes",
      line: "Given a CPU part-way through a short program, predict what one named register holds once fetch, decode or execute has finished.",
      after: "CPU Performance Factors"
    },
    "computer-science-aqa/data-representation/3": {
      file: "sampling-repeated-measurement",
      label: "Predict what gets stored",
      line: "See an ADC measure a sound wave at fixed instants, then work out how much of the wave survives — and how big the file becomes.",
      after: "Quality Versus File Size"
    },
    "computer-science-edexcel/computational-thinking/4": {
      file: "binary-search-requires-sorted-data",
      label: "Trace the binary search",
      line: "Predict what the search checks, and whether it finds the target at all — on lists that are not always sorted.",
      after: "Choosing the Right Algorithm"
    },
    "computer-science-edexcel/data/3": {
      file: "sampling-repeated-measurement",
      label: "Predict what gets stored",
      line: "See an ADC measure a sound wave at fixed instants, then work out how much of the wave survives — and how big the file becomes.",
      after: "Limitations of Binary Representation"
    },
    "computer-science-eduqas/algorithms-programming-software/3": {
      file: "binary-search-requires-sorted-data",
      label: "Trace the binary search",
      line: "Predict what the search checks, and whether it finds the target at all — on lists that are not always sorted.",
      after: "Comparing Linear and Binary Search"
    },
    "computer-science-eduqas/data-representation-storage/5": {
      file: "sampling-repeated-measurement",
      label: "Predict what gets stored",
      line: "See an ADC measure a sound wave at fixed instants, then work out how much of the wave survives — and how big the file becomes.",
      after: "Bit Depth (Sample Resolution)"
    },
    "computer-science-eduqas/hardware-and-systems/1": {
      file: "fetch-decode-simultaneous",
      label: "Predict what each stage changes",
      line: "Given a CPU part-way through a short program, predict what one named register holds once fetch, decode or execute has finished.",
      after: "Cache Memory"
    },
    "computer-science-eduqas/hardware-and-systems/2": {
      file: "fetch-decode-simultaneous",
      label: "Predict what each stage changes",
      line: "Given a CPU part-way through a short program, predict what one named register holds once fetch, decode or execute has finished.",
      after: "CPU Performance Factor 3 — Cache Size"
    },
    "computer-science/computational-thinking/3": {
      file: "binary-search-requires-sorted-data",
      label: "Trace the binary search",
      line: "Predict what the search checks, and whether it finds the target at all — on lists that are not always sorted.",
      after: "Comparing the two searches"
    },
    "computer-science/computer-systems/1": {
      file: "fetch-decode-simultaneous",
      label: "Predict what each stage changes",
      line: "Given a CPU part-way through a short program, predict what one named register holds once fetch, decode or execute has finished.",
      after: "The fetch-execute cycle"
    },
    "computer-science/computer-systems/7": {
      file: "sampling-repeated-measurement",
      label: "Predict what gets stored",
      line: "See an ADC measure a sound wave at fixed instants, then work out how much of the wave survives — and how big the file becomes.",
      after: "Quality versus File Size"
    },
    "drama-aqa/the-great-wave/5": {
      file: "cross-cutting-structural-device",
      label: "Cut between the two scenes",
      line: "Two scenes, one cut — predict what an audience experiences when a director intercuts them instead of playing one and then the other.",
      after: "The Wave as Structural Metaphor"
    },
    "economics-aqa/how-prices-are-determined/1": {
      file: "demand-curve-movement-vs-shift",
      label: "Predict movement or shift",
      line: "One chocolate bar, one demand curve — decide whether each event slides the point along the curve or moves the whole curve.",
      after: "Shifts in the Demand Curve"
    },
    "economics-aqa/how-prices-are-determined/3": {
      file: "demand-curve-movement-vs-shift",
      label: "Predict movement or shift",
      line: "One chocolate bar, one demand curve — decide whether each event slides the point along the curve or moves the whole curve.",
      after: "The Price Mechanism: Three Functions"
    },
    "electronics-eduqas/discovering-electronics/2": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Test Equipment"
    },
    "engineering-aqa/engineering-systems/4": {
      file: "transformer-voltage-current-tradeoff",
      label: "Predict the secondary side",
      line: "Choose the voltage and the current a transformer delivers, then check your pair against the supply it was given.",
      after: "Input Control Devices: Switches"
    },
    "film-studies-eduqas/film-form-and-language/5": {
      file: "plot-vs-story",
      label: "Work out the cut",
      line: "Three short stories, each re-arranged into a film — decide what the audience meets first, which events never reach the screen, and what that order creates.",
      after: "Three-Act Structure"
    },
    "geography-aqa/paper-1/14": {
      file: "longshore-drift-zigzag",
      label: "Predict the pebble's path",
      line: "Choose how one pebble moves over eight waves, then watch the swash and backwash play it out.",
      after: "Deposition"
    },
    "geography-aqa/paper-1/16": {
      file: "holderness-hard-defences",
      label: "Test a coastal defence",
      line: "Predict what a proposed scheme does to a stretch further along the coast, then watch the sediment budget settle it.",
      after: "Conflicts on the Coast"
    },
    "geography-aqa/paper-1/8": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Effects on People and the Environment"
    },
    "geography-edexcel-a/paper-1-physical-environment/2": {
      file: "longshore-drift-zigzag",
      label: "Predict the pebble's path",
      line: "Choose how one pebble moves over eight waves, then watch the swash and backwash play it out.",
      after: "Erosional Landforms: Headlands, Bays, Cliffs & Stacks"
    },
    "geography-edexcel-a/paper-1-physical-environment/3": {
      file: "holderness-hard-defences",
      label: "Test a coastal defence",
      line: "Predict what a proposed scheme does to a stretch further along the coast, then watch the sediment budget settle it.",
      after: "Soft Engineering: Working With the Sea"
    },
    "geography-edexcel-b/uk-geographical-issues/2": {
      file: "longshore-drift-zigzag",
      label: "Predict the pebble's path",
      line: "Choose how one pebble moves over eight waves, then watch the swash and backwash play it out.",
      after: "Transport and Deposition"
    },
    "geography-edexcel-b/uk-geographical-issues/3": {
      file: "holderness-hard-defences",
      label: "Test a coastal defence",
      line: "Predict what a proposed scheme does to a stretch further along the coast, then watch the sediment budget settle it.",
      after: "Sustainable Approaches: Doing Nothing and Strategic Realignment"
    },
    "geography-eduqas/landscapes-physical-processes/3": {
      file: "longshore-drift-zigzag",
      label: "Predict the pebble's path",
      line: "Choose how one pebble moves over eight waves, then watch the swash and backwash play it out.",
      after: "Beaches, Spits and Bars"
    },
    "geography-eduqas/landscapes-physical-processes/4": {
      file: "holderness-hard-defences",
      label: "Test a coastal defence",
      line: "Predict what a proposed scheme does to a stretch further along the coast, then watch the sediment budget settle it.",
      after: "Rivers Feel Human Pressure Too"
    },
    "geography-ocr/living-in-the-uk-today/3": {
      file: "longshore-drift-zigzag",
      label: "Predict the pebble's path",
      line: "Choose how one pebble moves over eight waves, then watch the swash and backwash play it out.",
      after: "UK Case Study: The Holderness Coast"
    },
    "geology-eduqas/geological-time-and-life/3": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "What Radiometric Dating Actually Dates"
    },
    "geology-eduqas/hazards-resources-and-investigative-geology/5": {
      file: "porosity-vs-permeability",
      label: "Test a rock with water",
      line: "Read the grains, predict the porosity and the permeability, then watch whether the water soaks in and stops or streams straight through.",
      after: "Domestic Waste and Landfill Sites"
    },
    "geology-eduqas/rocks-and-minerals/5": {
      file: "porosity-vs-permeability",
      label: "Test a rock with water",
      line: "Read the grains, predict the porosity and the permeability, then watch whether the water soaks in and stops or streams straight through.",
      after: "Sorting: Reading Energy Consistency"
    },
    "history-aqa/elizabethan-england/13": {
      file: "armada-chain-of-consequence",
      label: "Put the disaster in order",
      line: "Five links, shuffled. Commit to the chain, then see what forced what.",
      after: "The Long Way Home"
    },
    "history-aqa/germany-democracy-dictatorship/7": {
      file: "nazi-rise-contingent-not-inevitable",
      label: "Predict the election results",
      line: "Five real results between 1928 and 1933 — commit to a prediction, then see what the votes actually did.",
      after: "Bruning and the Politics of Austerity"
    },
    "history-aqa/germany-democracy-dictatorship/8": {
      file: "nazi-rise-contingent-not-inevitable",
      label: "Predict the election results",
      line: "Five real results between 1928 and 1933 — commit to a prediction, then see what the votes actually did.",
      after: "The Appointment, 30 January 1933"
    },
    "history-edexcel/weimar-nazi-germany/6": {
      file: "nazi-rise-contingent-not-inevitable",
      label: "Predict the election results",
      line: "Five real results between 1928 and 1933 — commit to a prediction, then see what the votes actually did.",
      after: "The Appeal of Hitler and the Nazi Party"
    },
    "music-aqa/aos1-western-classical/2": {
      file: "sonata-form-key-relationships",
      label: "Follow the key journey",
      line: "Predict where the second subject goes in the exposition — and which key it comes back in.",
      after: "Sonata form"
    },
    "physical-education-aqa/human-body-and-movement/4": {
      file: "heart-simultaneous-double-circulation",
      label: "Track one blood cell",
      line: "See both sides of the heart squeeze on the same beat, and find out why blood passes through it twice on every lap of the body.",
      after: "The Cardiac Cycle: How the Heart Beats"
    },
    "physical-education-ocr/physical-factors-affecting-performance/6": {
      file: "heart-simultaneous-double-circulation",
      label: "Track one blood cell",
      line: "See both sides of the heart squeeze on the same beat, and find out why blood passes through it twice on every lap of the body.",
      after: "The Heart: Structure and Function"
    },
    "psychology-aqa/brain-neuropsychology/2": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "Neurotransmitters and Behaviour"
    },
    "psychology-aqa/development/2": {
      file: "piaget-qualitative-stages",
      label: "Predict the child's answer",
      line: "A classic Piagetian task and a named stage — predict how that child answers, then hear them say it.",
      after: "Evaluating Piaget’s Theory"
    },
    "psychology-aqa/development/3": {
      file: "piaget-qualitative-stages",
      label: "Predict the child's answer",
      line: "A classic Piagetian task and a named stage — predict how that child answers, then hear them say it.",
      after: "Implications for Education"
    },
    "psychology-edexcel/brain-neuropsychology/3": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "Neurotransmitters and Behaviour"
    },
    "psychology-edexcel/development/2": {
      file: "piaget-qualitative-stages",
      label: "Predict the child's answer",
      line: "A classic Piagetian task and a named stage — predict how that child answers, then hear them say it.",
      after: "Piaget and Inhelder’s Three Mountains Task (1956)"
    },
    "psychology-ocr/development/2": {
      file: "piaget-qualitative-stages",
      label: "Predict the child's answer",
      line: "A classic Piagetian task and a named stage — predict how that child answers, then hear them say it.",
      after: "The Core Study: Piaget (1952) and the Conservation of Number"
    },
    "religious-studies-aqa/buddhism-beliefs/1": {
      file: "dependent-origination-web-not-chain",
      label: "Remove one condition",
      line: "See what ceases when a single condition is taken out of the web, and what carries on regardless.",
      after: "Dukkha — Unsatisfactoriness and Suffering"
    },
    "religious-studies-aqa/buddhism-beliefs/2": {
      file: "dependent-origination-web-not-chain",
      label: "Remove one condition",
      line: "See what ceases when a single condition is taken out of the web, and what carries on regardless.",
      after: "The Five Aggregates in Everyday Life"
    },
    "religious-studies-aqa/catholic-christianity-beliefs/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Scriptural Origins of the Trinity"
    },
    "religious-studies-aqa/christianity-beliefs/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "The Oneness of God and the Trinity"
    },
    "religious-studies-edexcel/paper-1-catholic-christianity/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Creation and Genesis"
    },
    "religious-studies-edexcel/paper-2-buddhism/3": {
      file: "dependent-origination-web-not-chain",
      label: "Remove one condition",
      line: "See what ceases when a single condition is taken out of the web, and what carries on regardless.",
      after: "Arahant and Bodhisattva Ideals"
    },
    "religious-studies-edexcel/paper-2-catholic-christianity/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Creation: The World as God’s Gift"
    },
    "religious-studies-edexcel/paper-2-christianity/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Creation: God and the Universe"
    },
    "religious-studies-eduqas/christianity/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Why the Trinity Matters in Practice"
    },
    "religious-studies-ocr/buddhism-beliefs-and-teachings/1": {
      file: "dependent-origination-web-not-chain",
      label: "Remove one condition",
      line: "See what ceases when a single condition is taken out of the web, and what carries on regardless.",
      after: "The Three Marks of Existence"
    },
    "religious-studies-ocr/buddhism-beliefs-and-teachings/4": {
      file: "dependent-origination-web-not-chain",
      label: "Remove one condition",
      line: "See what ceases when a single condition is taken out of the web, and what carries on regardless.",
      after: "Arahant and Bodhisattva"
    },
    "religious-studies-ocr/christianity-beliefs-and-teachings/1": {
      file: "trinity-three-persons",
      label: "Sort the Trinity claims",
      line: "Decide whether each claim keeps the doctrine of the Trinity, or slips into three gods or three masks.",
      after: "Unitarians and Rejection of the Trinity"
    },
    "science-aqa/biology-paper-1/4": {
      file: "heart-simultaneous-double-circulation",
      label: "Track one blood cell",
      line: "See both sides of the heart squeeze on the same beat, and find out why blood passes through it twice on every lap of the body.",
      after: "Blood Vessels"
    },
    "science-aqa/biology-paper-1/8": {
      file: "photosynthesis-limiting-factor-plateau",
      label: "Lift the plateau",
      line: "The graph has levelled off — work out which single change raises the rate, and which does nothing at all.",
      after: "Aerobic Respiration"
    },
    "science-aqa/biology-paper-2/1": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "Reflex Actions"
    },
    "science-aqa/biology-paper-2/12": {
      file: "biomass-transfer-respiration",
      label: "Account for every kilojoule",
      line: "Split an animal's food intake between new biomass, respiration, egestion and excretion, and find out which loss is really the big one.",
      after: "Implications for Food Production"
    },
    "science-aqa/biology-paper-2/3": {
      file: "menstrual-cycle-hormone-feedback",
      label: "Walk the hormone cycle",
      line: "Step through one 28-day cycle on the four hormone curves, then work out what causes what.",
      after: "Contraception"
    },
    "science-aqa/biology-paper-2/5": {
      file: "heterozygous-carrier-no-symptoms",
      label: "Predict health from genotype",
      line: "One working allele is enough — see why a carrier has no symptoms at all, yet can still pass the faulty allele on.",
      after: "Punnett Squares and Genetic Diagrams"
    },
    "science-aqa/chemistry-paper-1/10": {
      file: "nanoparticle-surface-area-threshold",
      label: "Cut the cube smaller",
      line: "Predict what happens to the total surface area as a block is cut into ever-smaller cubes, and why the same substance behaves differently at 10 nm.",
      after: "Uses of Nanoparticles"
    },
    "science-aqa/chemistry-paper-1/2": {
      file: "periodic-table-group-reactivity-trends",
      label: "Predict the reactivity trend",
      line: "Two elements and one prediction — work out why reactivity climbs down Group 1 but falls down Group 7.",
      after: "Group 7 — Halogens"
    },
    "science-aqa/chemistry-paper-1/8": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Electrolysis of Molten Compounds"
    },
    "science-aqa/chemistry-paper-1/9": {
      file: "bond-energy-not-sequential",
      label: "Balance the bond energies",
      line: "Work out which way the energy goes at each side, then let the two totals decide whether the reaction is exothermic or endothermic.",
      after: "Practical Applications"
    },
    "science-aqa/chemistry-paper-2/2": {
      file: "equilibrium-not-static",
      label: "Predict the next ten seconds",
      line: "A sealed flask of A ⇌ B — commit to what the amounts and the two rates do next, then watch the particles.",
      after: "Dynamic Equilibrium"
    },
    "science-aqa/chemistry-paper-2/5": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "The Greenhouse Effect"
    },
    "science-aqa/chemistry-paper-2/9": {
      file: "polymer-double-bond-electron-rearrangement",
      label: "Open the double bond",
      line: "Predict the repeat unit, then watch the C=C open and its electrons become the links along the chain.",
      after: "Condensation Polymers"
    },
    "science-aqa/physics-paper-1/1": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Work Done and Power"
    },
    "science-aqa/physics-paper-1/2": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Efficiency"
    },
    "science-aqa/physics-paper-1/3": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Electrical Power"
    },
    "science-aqa/physics-paper-1/4": [{
      file: "series-voltage-split",
      label: "Predict the voltmeter",
      line: "Two resistors, one loop. Say where the volts go before you find out.",
      after: "Parallel Circuits"
    }, {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Parallel Circuits"
    }],
    "science-aqa/physics-paper-1/6": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Density Changes During State Changes"
    },
    "science-aqa/physics-paper-1/7": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Particle Model Explanation"
    },
    "science-aqa/physics-paper-1/8": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Uses and Hazards of Radiation"
    },
    "science-aqa/physics-paper-1/9": {
      file: "field-lines-as-maps-not-paths",
      label: "Read the field map",
      line: "Predict which way a charge is pushed at a point between the lines, and where the field is strongest.",
      after: "Uses and Dangers of Static Electricity"
    },
    "science-aqa/physics-paper-2/1": {
      file: "resultant-force-vector-subtraction",
      label: "Find the resultant force",
      line: "Predict what two opposing forces add up to — and what it does to the object's motion.",
      after: "Resultant Forces"
    },
    "science-aqa/physics-paper-2/12": {
      file: "transformer-voltage-current-tradeoff",
      label: "Predict the secondary side",
      line: "Choose the voltage and the current a transformer delivers, then check your pair against the supply it was given.",
      after: "The National Grid"
    },
    "science-aqa/physics-paper-2/4": {
      file: "newtons-third-law-different-objects",
      label: "Name the partner force",
      line: "Given one force in a scenario, work out its third law partner: what type it is, which object it acts on, and which way it points.",
      after: "Terminal Velocity"
    },
    "science-edexcel/biology-paper-1/5": {
      file: "heterozygous-carrier-no-symptoms",
      label: "Predict health from genotype",
      line: "One working allele is enough — see why a carrier has no symptoms at all, yet can still pass the faulty allele on.",
      after: "Monohybrid Crosses and Punnett Squares"
    },
    "science-edexcel/biology-paper-2/1": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "The Reflex Arc"
    },
    "science-edexcel/biology-paper-2/3": {
      file: "menstrual-cycle-hormone-feedback",
      label: "Walk the hormone cycle",
      line: "Step through one 28-day cycle on the four hormone curves, then work out what causes what.",
      after: "Contraception"
    },
    "science-edexcel/biology-paper-2/4": {
      file: "punnett-square-meaning",
      label: "Test the 3:1 ratio",
      line: "Fill in the missing cell, give the chance, then see what four real offspring actually do.",
      after: "Monohybrid Inheritance"
    },
    "science-edexcel/biology-paper-2/5": {
      file: "natural-selection-not-directed",
      label: "Predict what the population does",
      line: "Commit to one of four accounts of what happens over the generations, and find out whether selection had any variation to act on.",
      after: "Evolution — Change Over Time"
    },
    "science-edexcel/biology-paper-2/8": {
      file: "biomass-transfer-respiration",
      label: "Account for every kilojoule",
      line: "Split an animal's food intake between new biomass, respiration, egestion and excretion, and find out which loss is really the big one.",
      after: "Material Cycles — Why Recycling Matters"
    },
    "science-edexcel/chemistry-paper-1/8": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Electrolysis of Specific Substances"
    },
    "science-edexcel/chemistry-paper-2/1": {
      file: "collision-theory-energy-distribution",
      label: "Predict the effect on collisions",
      line: "Warm it, dilute it or add a catalyst, then predict both the number of collisions and the share of them with enough energy to react.",
      after: "Catalysts"
    },
    "science-edexcel/chemistry-paper-2/2": {
      file: "equilibrium-not-static",
      label: "Predict the next ten seconds",
      line: "A sealed flask of A ⇌ B — commit to what the amounts and the two rates do next, then watch the particles.",
      after: "The Haber Process"
    },
    "science-edexcel/chemistry-paper-2/3": {
      file: "fractional-distillation-boiling-point",
      label: "Send it up the column",
      line: "Predict the height where a hydrocarbon condenses, from its boiling point and the column temperatures.",
      after: "How Fractions Differ"
    },
    "science-edexcel/chemistry-paper-2/5": {
      file: "polymer-double-bond-electron-rearrangement",
      label: "Open the double bond",
      line: "Predict the repeat unit, then watch the C=C open and its electrons become the links along the chain.",
      after: "Alkenes — The Monomers for Addition Polymers"
    },
    "science-edexcel/chemistry-paper-2/7": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Climate Change"
    },
    "science-edexcel/physics-paper-1/1": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Drawing Energy Transfer Diagrams"
    },
    "science-edexcel/physics-paper-1/2": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Energy Resources"
    },
    "science-edexcel/physics-paper-1/4": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Parallel Circuits"
    },
    "science-edexcel/physics-paper-1/6": {
      file: "field-lines-as-maps-not-paths",
      label: "Read the field map",
      line: "Predict which way a charge is pushed at a point between the lines, and where the field is strongest.",
      after: "Ions and Electron Transfer"
    },
    "science-edexcel/physics-paper-1/8": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Specific Heat Capacity"
    },
    "science-edexcel/physics-paper-2/1": {
      file: "newtons-third-law-different-objects",
      label: "Name the partner force",
      line: "Given one force in a scenario, work out its third law partner: what type it is, which object it acts on, and which way it points.",
      after: "Circular Motion"
    },
    "science-ocr-b/biology-paper-1/5": {
      file: "antibodies-dont-kill",
      label: "Predict what happens next",
      line: "Commit a prediction for each scene — bound antibodies, an antigen that does not fit, an antibiotic against a virus — then see what really happens.",
      after: "How Vaccination Works"
    },
    "science-ocr-b/biology-paper-1/7": {
      file: "photosynthesis-limiting-factor-plateau",
      label: "Lift the plateau",
      line: "The graph has levelled off — work out which single change raises the rate, and which does nothing at all.",
      after: "Resources That Producers Need: Minerals and Water"
    },
    "science-ocr-b/biology-paper-1/8": {
      file: "biomass-transfer-respiration",
      label: "Account for every kilojoule",
      line: "Split an animal's food intake between new biomass, respiration, egestion and excretion, and find out which loss is really the big one.",
      after: "Predator–Prey Cycles and Population Change"
    },
    "science-ocr-b/biology-paper-2/2": {
      file: "organelle-3d-spatial-architecture",
      label: "See where organelles actually sit",
      line: "Predict where a specialised cell concentrates an organelle, then watch the textbook diagram redraw itself as the crowded thing it really is.",
      after: "Prokaryotic Cell Structure"
    },
    "science-ocr-b/biology-paper-2/4": {
      file: "sa-v-ratio-real-limit",
      label: "Test which block copes",
      line: "Two blocks of living tissue side by side — commit to which can supply every cell through its own surface, then watch the surface and volume counted.",
      after: "Moving Substances Across Cell Membranes"
    },
    "science-ocr-b/biology-paper-2/5": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "The Endocrine System"
    },
    "science-ocr-b/biology-paper-2/6": {
      file: "negative-feedback-continuous-cycle",
      label: "Predict what happens next",
      line: "Join a control system mid-story and predict which response is acting, what the level does, and what happens once it crosses the set point.",
      after: "Controlling Blood Glucose"
    },
    "science-ocr-b/biology-paper-2/7": {
      file: "menstrual-cycle-hormone-feedback",
      label: "Walk the hormone cycle",
      line: "Step through one 28-day cycle on the four hormone curves, then work out what causes what.",
      after: "When Organs and Control Systems Fail"
    },
    "science-ocr-b/biology-paper-2/8": {
      file: "natural-selection-not-directed",
      label: "Predict what the population does",
      line: "Commit to one of four accounts of what happens over the generations, and find out whether selection had any variation to act on.",
      after: "Classification and Phylogenetic Trees"
    },
    "science-ocr-b/chemistry-paper-1/3": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Key Greenhouse Gases and Their Sources"
    },
    "science-ocr-b/chemistry-paper-1/5": {
      file: "atom-mostly-empty-space",
      label: "Fire the alpha beam",
      line: "Predict what a beam of alpha particles does to gold foil, then run it and see which picture of the atom survives.",
      after: "Models as Tools: Strengths and Limitations"
    },
    "science-ocr-b/chemistry-paper-2/2": {
      file: "reactivity-series-electron-transfer",
      label: "Predict the displacement",
      line: "Decide whether one metal will displace another from its solution, and which metal ends up as the ions.",
      after: "Reactions with Water and Dilute Acid"
    },
    "science-ocr-b/chemistry-paper-2/3": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Extracting Aluminium by Electrolysis"
    },
    "science-ocr-b/chemistry-paper-2/7": {
      file: "nanoparticle-surface-area-threshold",
      label: "Cut the cube smaller",
      line: "Predict what happens to the total surface area as a block is cut into ever-smaller cubes, and why the same substance behaves differently at 10 nm.",
      after: "Properties That Change at the Nanoscale"
    },
    "science-ocr-b/physics-paper-1/2": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "The Electromagnetic Spectrum and Climate"
    },
    "science-ocr-b/physics-paper-1/5": {
      file: "transformer-voltage-current-tradeoff",
      label: "Predict the secondary side",
      line: "Choose the voltage and the current a transformer delivers, then check your pair against the supply it was given.",
      after: "Why Transmit at High Voltage?"
    },
    "science-ocr-b/physics-paper-1/6": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Series and Parallel Circuits"
    },
    "science-ocr-b/physics-paper-2/4": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Work Done"
    },
    "science-ocr-b/physics-paper-2/5": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Half-Life"
    },
    "science-ocr-b/physics-paper-2/7": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Changes of State and Specific Latent Heat"
    },
    "science-ocr/biology-paper-1/1": {
      file: "organelle-3d-spatial-architecture",
      label: "See where organelles actually sit",
      line: "Predict where a specialised cell concentrates an organelle, then watch the textbook diagram redraw itself as the crowded thing it really is.",
      after: "Microscopy"
    },
    "science-ocr/biology-paper-1/4": {
      file: "photosynthesis-limiting-factor-plateau",
      label: "Lift the plateau",
      line: "The graph has levelled off — work out which single change raises the rate, and which does nothing at all.",
      after: "Factors Affecting the Rate of Photosynthesis"
    },
    "science-ocr/biology-paper-1/5": {
      file: "sa-v-ratio-real-limit",
      label: "Test which block copes",
      line: "Two blocks of living tissue side by side — commit to which can supply every cell through its own surface, then watch the surface and volume counted.",
      after: "The Challenges of Size"
    },
    "science-ocr/biology-paper-1/6": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "Synapses"
    },
    "science-ocr/biology-paper-1/8": {
      file: "negative-feedback-continuous-cycle",
      label: "Predict what happens next",
      line: "Join a control system mid-story and predict which response is acting, what the level does, and what happens once it crosses the set point.",
      after: "Blood Glucose Control"
    },
    "science-ocr/biology-paper-2/1": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Biotic and Abiotic Factors"
    },
    "science-ocr/biology-paper-2/3": {
      file: "heterozygous-carrier-no-symptoms",
      label: "Predict health from genotype",
      line: "One working allele is enough — see why a carrier has no symptoms at all, yet can still pass the faulty allele on.",
      after: "Alleles and Inheritance"
    },
    "science-ocr/biology-paper-2/4": {
      file: "natural-selection-not-directed",
      label: "Predict what the population does",
      line: "Commit to one of four accounts of what happens over the generations, and find out whether selection had any variation to act on.",
      after: "Selective Breeding"
    },
    "science-ocr/biology-paper-2/7": {
      file: "antibodies-dont-kill",
      label: "Predict what happens next",
      line: "Commit a prediction for each scene — bound antibodies, an antigen that does not fit, an antibiotic against a virus — then see what really happens.",
      after: "The Body’s Defence Systems"
    },
    "science-ocr/chemistry-paper-1/2": {
      file: "atom-mostly-empty-space",
      label: "Fire the alpha beam",
      line: "Predict what a beam of alpha particles does to gold foil, then run it and see which picture of the atom survives.",
      after: "Electronic Configuration"
    },
    "science-ocr/chemistry-paper-1/7": {
      file: "bond-energy-not-sequential",
      label: "Balance the bond energies",
      line: "Work out which way the energy goes at each side, then let the two totals decide whether the reaction is exothermic or endothermic.",
      after: "Bond Energy Calculations (Higher)"
    },
    "science-ocr/chemistry-paper-2/1": {
      file: "reactivity-series-electron-transfer",
      label: "Predict the displacement",
      line: "Decide whether one metal will displace another from its solution, and which metal ends up as the ions.",
      after: "Extracting Metals"
    },
    "science-ocr/chemistry-paper-2/5": {
      file: "equilibrium-not-static",
      label: "Predict the next ten seconds",
      line: "A sealed flask of A ⇌ B — commit to what the amounts and the two rates do next, then watch the particles.",
      after: "Le Chatelier’s Principle (Higher)"
    },
    "science-ocr/chemistry-paper-2/7": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Climate Change"
    },
    "science-ocr/physics-paper-1/2": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Specific Heat Capacity"
    },
    "science-ocr/physics-paper-1/6": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Resistance and Ohm’s Law"
    },
    "science-ocr/physics-paper-2/2": {
      file: "em-spectrum-continuous",
      label: "Slide across the spectrum",
      line: "Seven names, one continuous slide of wavelength — and one speed that never changes.",
      after: "Absorption, Transmission and Reflection"
    },
    "separate-sciences-edexcel/biology-paper-1/1": {
      file: "organelle-3d-spatial-architecture",
      label: "See where organelles actually sit",
      line: "Predict where a specialised cell concentrates an organelle, then watch the textbook diagram redraw itself as the crowded thing it really is.",
      after: "Animal and Plant Cell Organelles"
    },
    "separate-sciences-edexcel/biology-paper-1/4": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "The Eye (Triple Only)"
    },
    "separate-sciences-edexcel/biology-paper-1/5": {
      file: "punnett-square-meaning",
      label: "Test the 3:1 ratio",
      line: "Fill in the missing cell, give the chance, then see what four real offspring actually do.",
      after: "Codominance and ABO Blood Groups (Triple Only)"
    },
    "separate-sciences-edexcel/biology-paper-1/6": {
      file: "natural-selection-not-directed",
      label: "Predict what the population does",
      line: "Commit to one of four accounts of what happens over the generations, and find out whether selection had any variation to act on.",
      after: "Evidence for Evolution"
    },
    "separate-sciences-edexcel/biology-paper-1/7": {
      file: "antibodies-dont-kill",
      label: "Predict what happens next",
      line: "Commit a prediction for each scene — bound antibodies, an antigen that does not fit, an antibiotic against a virus — then see what really happens.",
      after: "Vaccination and Herd Immunity"
    },
    "separate-sciences-edexcel/biology-paper-2/4": {
      file: "negative-feedback-continuous-cycle",
      label: "Predict what happens next",
      line: "Join a control system mid-story and predict which response is acting, what the level does, and what happens once it crosses the set point.",
      after: "The Menstrual Cycle"
    },
    "separate-sciences-edexcel/biology-paper-2/7": {
      file: "sa-v-ratio-real-limit",
      label: "Test which block copes",
      line: "Two blocks of living tissue side by side — commit to which can supply every cell through its own surface, then watch the surface and volume counted.",
      after: "Alveoli and Gas Exchange"
    },
    "separate-sciences-edexcel/biology-paper-2/8": {
      file: "biomass-transfer-respiration",
      label: "Account for every kilojoule",
      line: "Split an animal's food intake between new biomass, respiration, egestion and excretion, and find out which loss is really the big one.",
      after: "Biodiversity and Food Security"
    },
    "separate-sciences-edexcel/chemistry-paper-1/1": {
      file: "atom-mostly-empty-space",
      label: "Fire the alpha beam",
      line: "Predict what a beam of alpha particles does to gold foil, then run it and see which picture of the atom survives.",
      after: "The Development of the Atomic Model"
    },
    "separate-sciences-edexcel/chemistry-paper-1/2": {
      file: "periodic-table-group-reactivity-trends",
      label: "Predict the reactivity trend",
      line: "Two elements and one prediction — work out why reactivity climbs down Group 1 but falls down Group 7.",
      after: "Group 7 — The Halogens"
    },
    "separate-sciences-edexcel/chemistry-paper-1/6": {
      file: "reactivity-series-electron-transfer",
      label: "Predict the displacement",
      line: "Decide whether one metal will displace another from its solution, and which metal ends up as the ions.",
      after: "Extracting Metals from Their Ores"
    },
    "separate-sciences-edexcel/chemistry-paper-1/8": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Electrolysis of Molten Ionic Compounds"
    },
    "separate-sciences-edexcel/chemistry-paper-2/1": {
      file: "collision-theory-energy-distribution",
      label: "Predict the effect on collisions",
      line: "Warm it, dilute it or add a catalyst, then predict both the number of collisions and the share of them with enough energy to react.",
      after: "Core Practical — Measuring Rates of Reaction"
    },
    "separate-sciences-edexcel/chemistry-paper-2/3": {
      file: "fractional-distillation-boiling-point",
      label: "Send it up the column",
      line: "Predict the height where a hydrocarbon condenses, from its boiling point and the column temperatures.",
      after: "Alkanes"
    },
    "separate-sciences-edexcel/chemistry-paper-2/5": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Human Impact and Climate Change"
    },
    "separate-sciences-edexcel/chemistry-paper-2/6": {
      file: "polymer-double-bond-electron-rearrangement",
      label: "Open the double bond",
      line: "Predict the repeat unit, then watch the C=C open and its electrons become the links along the chain.",
      after: "Condensation Polymerisation"
    },
    "separate-sciences-edexcel/chemistry-paper-2/7": {
      file: "nanoparticle-surface-area-threshold",
      label: "Cut the cube smaller",
      line: "Predict what happens to the total surface area as a block is cut into ever-smaller cubes, and why the same substance behaves differently at 10 nm.",
      after: "Applications of Nanoparticles"
    },
    "separate-sciences-edexcel/physics-paper-1/2": {
      file: "resultant-force-vector-subtraction",
      label: "Find the resultant force",
      line: "Predict what two opposing forces add up to — and what it does to the object's motion.",
      after: "Newton’s Second Law and F = ma"
    },
    "separate-sciences-edexcel/physics-paper-1/7": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Background Radiation"
    },
    "separate-sciences-edexcel/physics-paper-2/4": {
      file: "transformer-voltage-current-tradeoff",
      label: "Predict the secondary side",
      line: "Choose the voltage and the current a transformer delivers, then check your pair against the supply it was given.",
      after: "The National Grid and Transformers"
    },
    "separate-sciences-edexcel/physics-paper-2/7": {
      file: "transformer-voltage-current-tradeoff",
      label: "Predict the secondary side",
      line: "Choose the voltage and the current a transformer delivers, then check your pair against the supply it was given.",
      after: "Power and Efficiency in Transformers"
    },
    "separate-sciences-ocr-b/biology-human-body/4": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "Reflex Actions"
    },
    "separate-sciences-ocr-b/biology-life-on-earth-ecosystems/1": {
      file: "photosynthesis-limiting-factor-plateau",
      label: "Lift the plateau",
      line: "The graph has levelled off — work out which single change raises the rate, and which does nothing at all.",
      after: "Transpiration and Water Loss"
    },
    "separate-sciences-ocr-b/biology-life-on-earth-ecosystems/4": {
      file: "natural-selection-not-directed",
      label: "Predict what the population does",
      line: "Commit to one of four accounts of what happens over the generations, and find out whether selection had any variation to act on.",
      after: "Evidence for Evolution"
    },
    "separate-sciences-ocr-b/biology-you-and-your-genes/2": {
      file: "punnett-square-meaning",
      label: "Test the 3:1 ratio",
      line: "Fill in the missing cell, give the chance, then see what four real offspring actually do.",
      after: "Sex Determination"
    },
    "separate-sciences-ocr-b/chemistry-analysis-useful-products/3": {
      file: "collision-theory-energy-distribution",
      label: "Predict the effect on collisions",
      line: "Warm it, dilute it or add a catalyst, then predict both the number of collisions and the share of them with enough energy to react.",
      after: "Yield and Atom Economy"
    },
    "separate-sciences-ocr-b/chemistry-atoms-patterns-bonding/2": {
      file: "periodic-table-group-reactivity-trends",
      label: "Predict the reactivity trend",
      line: "Two elements and one prediction — work out why reactivity climbs down Group 1 but falls down Group 7.",
      after: "Group 7 — The Halogens"
    },
    "separate-sciences-ocr-b/chemistry-earth-air-water/3": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "The Evidence for Climate Change"
    },
    "separate-sciences-ocr-b/chemistry-materials-reactions/1": {
      file: "reactivity-series-electron-transfer",
      label: "Predict the displacement",
      line: "Decide whether one metal will displace another from its solution, and which metal ends up as the ions.",
      after: "Extracting Metals from Their Ores"
    },
    "separate-sciences-ocr-b/chemistry-materials-reactions/3": {
      file: "fractional-distillation-boiling-point",
      label: "Send it up the column",
      line: "Predict the height where a hydrocarbon condenses, from its boiling point and the column temperatures.",
      after: "Alkanes"
    },
    "separate-sciences-ocr-b/chemistry-materials-reactions/5": {
      file: "nanoparticle-surface-area-threshold",
      label: "Cut the cube smaller",
      line: "Predict what happens to the total surface area as a block is cut into ever-smaller cubes, and why the same substance behaves differently at 10 nm.",
      after: "Properties and Uses of Nanoparticles"
    },
    "separate-sciences-ocr-b/physics-energy-electricity/2": {
      file: "field-lines-as-maps-not-paths",
      label: "Read the field map",
      line: "Predict which way a charge is pushed at a point between the lines, and where the field is strongest.",
      after: "Uses and Hazards of Static Electricity"
    },
    "separate-sciences-ocr-b/physics-energy-electricity/3": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "I-V Graphs and Non-Ohmic Components"
    },
    "separate-sciences-ocr-b/physics-forces-motion-radioactivity/1": {
      file: "newtons-third-law-different-objects",
      label: "Name the partner force",
      line: "Given one force in a scenario, work out its third law partner: what type it is, which object it acts on, and which way it points.",
      after: "Weight and the Gravitational Field"
    },
    "separate-sciences-ocr-b/physics-forces-motion-radioactivity/4": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Contamination and Irradiation"
    },
    "separate-sciences-ocr-b/physics-particle-models-universe/1": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Density and Changes of State"
    },
    "separate-sciences-ocr-b/physics-radiation-waves/2": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Climate Models and the Role of Evidence"
    },
    "separate-sciences-ocr/biology-paper-1/1": {
      file: "organelle-3d-spatial-architecture",
      label: "See where organelles actually sit",
      line: "Predict where a specialised cell concentrates an organelle, then watch the textbook diagram redraw itself as the crowded thing it really is.",
      after: "Microscopy — Seeing Cells"
    },
    "separate-sciences-ocr/biology-paper-1/4": {
      file: "photosynthesis-limiting-factor-plateau",
      label: "Lift the plateau",
      line: "The graph has levelled off — work out which single change raises the rate, and which does nothing at all.",
      after: "Limiting Factors"
    },
    "separate-sciences-ocr/biology-paper-1/5": {
      file: "sa-v-ratio-real-limit",
      label: "Test which block copes",
      line: "Two blocks of living tissue side by side — commit to which can supply every cell through its own surface, then watch the surface and volume counted.",
      after: "Specialised Exchange Surfaces"
    },
    "separate-sciences-ocr/biology-paper-1/7": {
      file: "synapse-electrical-to-chemical",
      label: "Find where the signal stops",
      line: "A signal reaches a synapse — predict the last thing that still happens, then watch the gap play it out.",
      after: "The Brain"
    },
    "separate-sciences-ocr/biology-paper-1/8": {
      file: "menstrual-cycle-hormone-feedback",
      label: "Walk the hormone cycle",
      line: "Step through one 28-day cycle on the four hormone curves, then work out what causes what.",
      after: "Plant Hormones"
    },
    "separate-sciences-ocr/biology-paper-2/1": {
      file: "negative-feedback-continuous-cycle",
      label: "Predict what happens next",
      line: "Join a control system mid-story and predict which response is acting, what the level does, and what happens once it crosses the set point.",
      after: "Blood Glucose Control"
    },
    "separate-sciences-ocr/biology-paper-2/3": {
      file: "biomass-transfer-respiration",
      label: "Account for every kilojoule",
      line: "Split an animal's food intake between new biomass, respiration, egestion and excretion, and find out which loss is really the big one.",
      after: "Adaptations and Biodiversity"
    },
    "separate-sciences-ocr/biology-paper-2/5": {
      file: "heterozygous-carrier-no-symptoms",
      label: "Predict health from genotype",
      line: "One working allele is enough — see why a carrier has no symptoms at all, yet can still pass the faulty allele on.",
      after: "Inherited Disorders"
    },
    "separate-sciences-ocr/biology-paper-2/9": {
      file: "antibodies-dont-kill",
      label: "Predict what happens next",
      line: "Commit a prediction for each scene — bound antibodies, an antigen that does not fit, an antibiotic against a virus — then see what really happens.",
      after: "Vaccination and Antibiotics"
    },
    "separate-sciences-ocr/chemistry-paper-1/1": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Heating and Cooling Curves"
    },
    "separate-sciences-ocr/chemistry-paper-1/2": {
      file: "atom-mostly-empty-space",
      label: "Fire the alpha beam",
      line: "Predict what a beam of alpha particles does to gold foil, then run it and see which picture of the atom survives.",
      after: "Electronic Configuration"
    },
    "separate-sciences-ocr/chemistry-paper-1/8": {
      file: "bond-energy-not-sequential",
      label: "Balance the bond energies",
      line: "Work out which way the energy goes at each side, then let the two totals decide whether the reaction is exothermic or endothermic.",
      after: "Bond Energy Calculations (Higher Tier)"
    },
    "separate-sciences-ocr/chemistry-paper-2/2": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Electrolysis of Aqueous Solutions"
    },
    "separate-sciences-ocr/chemistry-paper-2/4": {
      file: "collision-theory-energy-distribution",
      label: "Predict the effect on collisions",
      line: "Warm it, dilute it or add a catalyst, then predict both the number of collisions and the share of them with enough energy to react.",
      after: "Catalysts"
    },
    "separate-sciences-ocr/chemistry-paper-2/5": {
      file: "equilibrium-not-static",
      label: "Predict the next ten seconds",
      line: "A sealed flask of A ⇌ B — commit to what the amounts and the two rates do next, then watch the particles.",
      after: "Le Chatelier’s Principle (Higher Tier)"
    },
    "separate-sciences-ocr/chemistry-paper-2/7": {
      file: "fractional-distillation-boiling-point",
      label: "Send it up the column",
      line: "Predict the height where a hydrocarbon condenses, from its boiling point and the column temperatures.",
      after: "Alkanes"
    },
    "separate-sciences-ocr/chemistry-paper-2/8": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "Climate Change"
    },
    "separate-sciences-ocr/physics-paper-1/2": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Specific Heat Capacity"
    },
    "separate-sciences-ocr/physics-paper-1/4": {
      file: "resultant-force-vector-subtraction",
      label: "Find the resultant force",
      line: "Predict what two opposing forces add up to — and what it does to the object's motion.",
      after: "Weight, Mass and Gravitational Field Strength"
    },
    "separate-sciences-ocr/physics-paper-1/6": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Resistance and Ohm’s Law"
    },
    "separate-sciences-ocr/physics-paper-1/7": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "AC and DC"
    },
    "separate-sciences-ocr/physics-paper-2/2": {
      file: "em-spectrum-continuous",
      label: "Slide across the spectrum",
      line: "Seven names, one continuous slide of wavelength — and one speed that never changes.",
      after: "The Electromagnetic Spectrum"
    },
    "separate-sciences-ocr/physics-paper-2/4": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Contamination and Irradiation"
    },
    "separate-sciences-ocr/physics-paper-2/9": {
      file: "redshift-stretching-mechanism",
      label: "Predict the spectral shift",
      line: "Give a galaxy's speed and direction, then say where its hydrogen lines land in the light that reaches Earth.",
      after: "Red-Shift and the Expanding Universe"
    },
    "separate-sciences/biology-paper-1/4": {
      file: "heart-simultaneous-double-circulation",
      label: "Track one blood cell",
      line: "See both sides of the heart squeeze on the same beat, and find out why blood passes through it twice on every lap of the body.",
      after: "Blood Vessels"
    },
    "separate-sciences/biology-paper-2/3": {
      file: "menstrual-cycle-hormone-feedback",
      label: "Walk the hormone cycle",
      line: "Step through one 28-day cycle on the four hormone curves, then work out what causes what.",
      after: "Contraception"
    },
    "separate-sciences/biology-paper-2/5": {
      file: "punnett-square-meaning",
      label: "Test the 3:1 ratio",
      line: "Fill in the missing cell, give the chance, then see what four real offspring actually do.",
      after: "Sex Determination"
    },
    "separate-sciences/chemistry-paper-1/1": {
      file: "atom-mostly-empty-space",
      label: "Fire the alpha beam",
      line: "Predict what a beam of alpha particles does to gold foil, then run it and see which picture of the atom survives.",
      after: "How the Atomic Model Developed"
    },
    "separate-sciences/chemistry-paper-1/2": {
      file: "periodic-table-group-reactivity-trends",
      label: "Predict the reactivity trend",
      line: "Two elements and one prediction — work out why reactivity climbs down Group 1 but falls down Group 7.",
      after: "Group 7 — Halogens"
    },
    "separate-sciences/chemistry-paper-1/6": {
      file: "reactivity-series-electron-transfer",
      label: "Predict the displacement",
      line: "Decide whether one metal will displace another from its solution, and which metal ends up as the ions.",
      after: "Extraction of Metals"
    },
    "separate-sciences/chemistry-paper-1/8": {
      file: "ion-migration-electrolysis",
      label: "Predict where the ions go",
      line: "Choose which rod each ion travels to and what forms there, then check it against the cell.",
      after: "Electrolysis of Molten Compounds"
    },
    "separate-sciences/chemistry-paper-1/9": {
      file: "bond-energy-not-sequential",
      label: "Balance the bond energies",
      line: "Work out which way the energy goes at each side, then let the two totals decide whether the reaction is exothermic or endothermic.",
      after: "Practical Applications"
    },
    "separate-sciences/chemistry-paper-2/2": {
      file: "equilibrium-not-static",
      label: "Predict the next ten seconds",
      line: "A sealed flask of A ⇌ B — commit to what the amounts and the two rates do next, then watch the particles.",
      after: "Dynamic Equilibrium"
    },
    "separate-sciences/chemistry-paper-2/5": {
      file: "greenhouse-effect-reemission-not-blanket",
      label: "Follow the infrared out",
      line: "Step through what happens to twelve packets of infrared — and watch what more CO₂ changes.",
      after: "The Greenhouse Effect"
    },
    "separate-sciences/physics-paper-1/1": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Work Done and Power"
    },
    "separate-sciences/physics-paper-1/2": {
      file: "conservation-of-energy-dispersal",
      label: "Account for every joule",
      line: "A kettle, a hoist and a braking bike hand you their energy budget — place every joule where it really ends up, then check the books.",
      after: "Efficiency"
    },
    "separate-sciences/physics-paper-1/3": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Resistance and Ohm's Law"
    },
    "separate-sciences/physics-paper-1/4": {
      file: "current-not-used-up",
      label: "Predict all three ammeters",
      line: "Three ammeters, one loop — commit to what each one reads before the circuit tells you.",
      after: "Parallel Circuits"
    },
    "separate-sciences/physics-paper-1/7": {
      file: "state-change-energy-plateau",
      label: "Predict the next two minutes",
      line: "A heater is on and the substance sits at a known temperature — say what the thermometer does next, and where the energy is actually going.",
      after: "Particle Model Explanation"
    },
    "separate-sciences/physics-paper-1/8": {
      file: "half-life-exponential-decay",
      label: "Predict what is left",
      line: "Say how many undecayed nuclei survive several half-lives, then watch the whole decay reveal itself.",
      after: "Uses and Hazards of Radiation"
    },
    "separate-sciences/physics-paper-2/1": {
      file: "resultant-force-vector-subtraction",
      label: "Find the resultant force",
      line: "Predict what two opposing forces add up to — and what it does to the object's motion.",
      after: "Resultant Forces"
    },
    "separate-sciences/physics-paper-2/4": {
      file: "newtons-third-law-different-objects",
      label: "Name the partner force",
      line: "Given one force in a scenario, work out its third law partner: what type it is, which object it acts on, and which way it points.",
      after: "Terminal Velocity"
    },
    "separate-sciences/physics-paper-2/7": {
      file: "em-spectrum-continuous",
      label: "Slide across the spectrum",
      line: "Seven names, one continuous slide of wavelength — and one speed that never changes.",
      after: "Uses and Dangers"
    },
    "sociology-aqa/crime-deviance/3": {
      file: "labelling-theory-identity",
      label: "Predict what the label does",
      line: "Two people, one act, one label — find out whether the label changes anything.",
      after: "Primary and Secondary Deviance"
    },
    "sociology-aqa/education/5": {
      file: "labelling-theory-identity",
      label: "Predict what the label does",
      line: "Two people, one act, one label — find out whether the label changes anything.",
      after: "Labelling Theory and the Self-Fulfilling Prophecy"
    }
  };

  var BASE = '/scripts/widget_pipeline/builds/';

  var CSS = [
    '.sv-embed-strip{display:flex;align-items:center;gap:1rem;margin:2rem 0;padding:.95rem 1.1rem;',
    'background:#fff;border:1px solid #e8e3db;border-radius:14px;box-shadow:0 1px 2px rgba(45,42,38,.04)}',
    '.sv-embed-strip .sv-es-txt{flex:1 1 auto;min-width:0}',
    '.sv-embed-strip .sv-es-kick{font-size:.66rem;font-weight:700;letter-spacing:.11em;',
    'text-transform:uppercase;color:var(--accent,#8a6a4f);margin-bottom:.15rem}',
    '.sv-embed-strip .sv-es-title{font-family:"Source Serif 4",Georgia,serif;font-size:1.02rem;',
    'font-weight:600;color:#2d2a26;line-height:1.25}',
    '.sv-embed-strip .sv-es-line{font-size:.84rem;color:#5b564e;margin-top:.15rem;line-height:1.4}',
    '.sv-embed-strip .sv-es-go{flex:0 0 auto;font:inherit;font-size:.85rem;font-weight:600;',
    'padding:.55rem 1.1rem;border-radius:10px;background:#2d2a26;color:#fff;border:1px solid #2d2a26;cursor:pointer}',
    '.sv-embed-strip .sv-es-go:hover{background:#413d37}',
    '@media (max-width:560px){.sv-embed-strip{flex-direction:column;align-items:stretch;gap:.7rem}',
    '.sv-embed-strip .sv-es-go{width:100%}}',
    '.sv-modal{position:fixed;inset:0;z-index:9000;display:flex;align-items:center;justify-content:center;',
    'padding:1.5rem;background:rgba(45,42,38,.55)}',
    '.sv-modal-inner{background:#fff;border-radius:16px;max-width:940px;width:100%;max-height:92vh;',
    'overflow:auto;padding:1.1rem;position:relative}',
    '.sv-modal-close{position:absolute;top:.6rem;right:.7rem;z-index:2;width:34px;height:34px;',
    'border-radius:9px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;font-size:1.1rem;line-height:1}',
    '@media (max-width:560px){.sv-modal{padding:0}.sv-modal-inner{max-height:100vh;height:100%;border-radius:0}}'
  ].join('');

  function css() {
    if (document.getElementById('sv-embed-css')) return;
    var s = document.createElement('style');
    s.id = 'sv-embed-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function accentOf(node) {
    var v = getComputedStyle(node).getPropertyValue('--accent').trim();
    return v || '#8a6a4f';
  }

  function openModal(cfg, strip) {
    var overlay = document.createElement('div');
    overlay.className = 'sv-modal';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', cfg.label);
    var inner = document.createElement('div');
    inner.className = 'sv-modal-inner';
    var close = document.createElement('button');
    close.className = 'sv-modal-close';
    close.setAttribute('aria-label', 'Close');
    close.innerHTML = '&times;';
    var mount = document.createElement('div');
    inner.appendChild(close);
    inner.appendChild(mount);
    overlay.appendChild(inner);
    document.body.appendChild(overlay);

    var lastFocus = document.activeElement;
    document.body.style.overflow = 'hidden';

    function shut() {
      overlay.remove();
      document.body.style.overflow = '';
      document.removeEventListener('keydown', onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function onKey(e) {
      if (e.key === 'Escape') { shut(); return; }
      if (e.key !== 'Tab') return;
      var f = inner.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    }
    close.addEventListener('click', shut);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) shut(); });
    document.addEventListener('keydown', onKey);
    close.focus();

    mount.textContent = 'Loading...';
    fetch(BASE + cfg.file + '.js')
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function (src) {
        var tag = document.createElement('script');
        tag.textContent = src;
        document.head.appendChild(tag);
        if (!window.SVWidget || !window.SVWidget.mount) throw new Error('widget did not register');
        var W = window.SVWidget;
        window.SVWidget = null;
        mount.textContent = '';
        var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
        W.mount(mount, { accent: accentOf(strip), reducedMotion: !!reduced });
      })
      .catch(function (e) {
        mount.textContent = 'This interactive could not load (' + e.message + ').';
      });
  }

  function placeStrip(cfg) {
    /* some lessons structure with h3s and have no h2s at all */
    var heads = document.querySelectorAll(
      '#lesson-content h2, .lesson-content h2, article h2, ' +
      '#lesson-content h3, .lesson-content h3, article h3');
    var target = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].textContent.trim().indexOf(cfg.after) === 0) { target = heads[i]; break; }
    }
    if (!target) return;
    css();
    var strip = document.createElement('div');
    strip.className = 'sv-embed-strip';
    strip.innerHTML =
      '<div class="sv-es-txt"><div class="sv-es-kick">Interactive</div>' +
      '<div class="sv-es-title"></div><div class="sv-es-line"></div></div>';
    strip.querySelector('.sv-es-title').textContent = cfg.label;
    strip.querySelector('.sv-es-line').textContent = cfg.line;
    var go = document.createElement('button');
    go.className = 'sv-es-go';
    go.type = 'button';
    go.textContent = 'Try it';
    go.addEventListener('click', function () { openModal(cfg, strip); });
    strip.appendChild(go);
    /* never trap the strip inside a tier-gated block - a widget for a
       core idea must be visible to Foundation students too */
    var gate = target.closest && target.closest('.higher-only, .foundation-only');
    var anchor = gate || target;
    anchor.parentNode.insertBefore(strip, anchor);
  }

  function inject() {
    var m = location.pathname.match(/\/lesson\/([^/]+)\/([^/]+)\/(\d+)/);
    var cfg = m && MAP[m[1] + '/' + m[2] + '/' + m[3]];
    if (!cfg || document.querySelector('.sv-embed-strip')) return;
    /* a lesson can carry more than one interactive (different sections) */
    var list = Array.isArray(cfg) ? cfg : [cfg];
    for (var wi = 0; wi < list.length; wi++) placeStrip(list[wi]);
  }

  /* Hook the loader's post-render callback.

     CAREFUL: js/lesson-widgets.js wraps the same function, and each file
     re-arms on DOMContentLoaded. If each guards only on its OWN marker,
     they wrap each other's wrapper forever and the first real call blows
     the stack - taking every lesson feature down with it, not just this
     strip. So: we skip only on OUR marker (so we still wrap lesson-widgets'
     wrapper and actually run), and we stamp __svw on the wrapper we install
     so lesson-widgets' own re-arm sees itself and stops. */
  function arm() {
    var f = window.initLessonFeatures;
    if (typeof f !== 'function') return;
    if (f.__svEmbed) return;               // we are already in the chain
    var wrapped = function () {
      var r = f.apply(this, arguments);
      try { inject(); } catch (e) {}
      return r;
    };
    wrapped.__svEmbed = true;
    wrapped.__svw = true;                  // stop lesson-widgets re-wrapping us
    window.initLessonFeatures = wrapped;
  }
  arm();
  document.addEventListener('DOMContentLoaded', arm);
})();
