/* StudyVault — Free-User Option Filters
   Single source of truth for "given a free user's picker prefs for a subject,
   which unit slugs should they see?" Used by:
     - js/browse-loader.js   (filter the unit cards on /browse/{subject})
     - js/home-counts.js     (count units/lessons on the homepage card)

   When adding a new option-route subject to the wizard, add a handler here.
   Both the browse page and the homepage card will pick up the new filter
   automatically — no duplicate filter code to keep in sync across files.

   Exports (on window.FreeUserFilters):
     - getAllowedUnitSlugs(subjectSlug)
         Returns an array of unit slugs to show, or null if no filter applies
         (subject not option-based, or user hasn't made picks). Callers should
         treat null as "show everything."
     - getPickedFilmSlugs(subjectSlug)
         Film Studies only — returns the Set of picked film lesson slugs, or
         null if no picks. Used for lesson-level (not unit-level) filtering.
     - FILM_SELECTABLE
         Set of film lesson slugs that are selectable in the Film Studies
         picker. Lessons NOT in this set always show (overviews, comparative
         method, generic film form, etc.); lessons IN this set show only when
         the user picked them.
*/
(function () {
  'use strict';

  function freePref(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    return FreeUser.getSubject(subjectSlug) || null;
  }

  // English Literature — student picks 1 Shakespeare + 1 19th-C novel +
  // 1 Modern + 1 Poetry cluster per board. 'unseen-poetry' is universally
  // compulsory across boards (no picker).
  var ENGLIT_SLUGS = [
    'english-literature', 'english-literature-aqa', 'english-literature-edexcel',
    'english-literature-ocr', 'english-literature-eduqas'
  ];
  var ENGLIT_COMPULSORY = ['unseen-poetry'];

  function englitFilter(pref) {
    if (!pref || !pref.texts || !Object.keys(pref.texts).length) return null;
    return Object.values(pref.texts).concat(ENGLIT_COMPULSORY);
  }

  // History — 4 picked options (one per paper/component section). AQA picks
  // 4 of 16, Edexcel picks 4 of 4 (auto), Eduqas picks 4 of 16 (one per
  // C100QS component). OCR has a compulsory period study so it uses its own
  // filter below.
  var HISTORY_SLUGS = ['history-aqa', 'history-edexcel', 'history-eduqas'];

  function historyFilter(pref) {
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    return Object.values(pref.options);
  }

  // History OCR (J410) — student picks one each from Non-British Depth,
  // Thematic Study and British Depth (3 units), PLUS the compulsory period
  // study (International Relations 1918-1975) that every OCR student takes.
  var HISTORY_OCR_SLUGS = ['history-ocr'];
  var HISTORY_OCR_COMPULSORY = ['international-relations-1918-1975'];

  function historyOcrFilter(pref) {
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    return Object.values(pref.options).concat(HISTORY_OCR_COMPULSORY);
  }

  // Drama AQA — pick 1 set play from 9. Universal units always show.
  var DRAMA_SLUGS = ['drama-aqa'];
  var DRAMA_UNIVERSAL = ['theatre-roles-stagecraft', 'practitioners-styles', 'live-theatre-review'];

  function dramaFilter(pref) {
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    return Object.values(pref.options).concat(DRAMA_UNIVERSAL);
  }

  // RE AQA — 2 of 7 religions (each gives Beliefs + Practices) + 4 of 6 themes
  // = 8 visible units. Legacy users (pref exists but no picks yet, from before
  // the picker) fall back to the original 8-unit set so they don't suddenly
  // see all 20 unfiltered.
  var RE_AQA_SLUGS = ['religious-studies-aqa', 'religious-education'];
  var RE_AQA_LEGACY_DEFAULT = [
    'christianity-beliefs', 'christianity-practices',
    'islam-beliefs', 'islam-practices',
    'theme-a-relationships', 'theme-b-religion-life',
    'theme-d-peace-conflict', 'theme-e-crime-punishment'
  ];

  function reAqaFilter(pref) {
    if (!pref) return null;
    if ((pref.religions && pref.religions.length) || (pref.themes && pref.themes.length)) {
      // AQA Short Course (8061) — Beliefs only, no Practices. Same Supabase row
      // as Spec A; wizard saves course_type='short' to drive this filter.
      var includesPractices = pref.course_type !== 'short';
      var slugs = [];
      (pref.religions || []).forEach(function (r) {
        slugs.push(r + '-beliefs');
        if (includesPractices) slugs.push(r + '-practices');
      });
      (pref.themes || []).forEach(function (t) { slugs.push(t); });
      return slugs;
    }
    return RE_AQA_LEGACY_DEFAULT.slice();
  }

  // RE OCR (J625) — pick 2 of 5 religions (each gives Beliefs & Teachings +
  // Practices) + all 4 Group-2 themes (mandatory, pre-selected by the wizard).
  // Religion unit slugs use the -beliefs-and-teachings / -practices suffix;
  // theme slugs are stored in full.
  var RE_OCR_SLUGS = ['religious-studies-ocr'];

  function reOcrFilter(pref) {
    if (!pref) return null;
    if ((pref.religions && pref.religions.length) || (pref.themes && pref.themes.length)) {
      var slugs = [];
      (pref.religions || []).forEach(function (r) {
        slugs.push(r + '-beliefs-and-teachings');
        slugs.push(r + '-practices');
      });
      (pref.themes || []).forEach(function (t) { slugs.push(t); });
      return slugs;
    }
    return null;
  }

  // RE Eduqas / WJEC — flatter unit structure (no -beliefs/-practices suffix).
  // Route B implicitly includes two Foundational Catholic Theology units not
  // surfaced in the picker.
  var RE_EDUQAS_SLUGS = ['religious-studies-eduqas'];
  var RE_EDUQAS_ROUTE_B_IMPLICIT = [
    'catholic-foundational-origins-and-meaning',
    'catholic-foundational-good-and-evil'
  ];

  function reEduqasFilter(pref) {
    if (!pref) return null;
    if (!((pref.religions && pref.religions.length) || (pref.themes && pref.themes.length))) {
      return null;
    }
    var slugs = (pref.religions || []).slice();
    (pref.themes || []).forEach(function (t) { slugs.push(t); });
    if (pref.route === 'b' || slugs.indexOf('catholic-christianity') !== -1) {
      RE_EDUQAS_ROUTE_B_IMPLICIT.forEach(function (s) { slugs.push(s); });
    }
    return slugs;
  }

  // RE Edexcel (1RA0) — Paper 1 + Paper 2 + (Paper 3 OR Paper 4).
  // Paper 3 religion auto-derives from Paper 1. Paper 4 text is user-picked
  // and independent of Paper 1.
  var RE_EDEXCEL_SLUGS = ['religious-studies-edexcel'];
  var RE_EDEXCEL_PAPER3_MAP = {
    'paper-1-catholic-christianity': 'paper-3-philosophy-ethics-catholic',
    'paper-1-christianity': 'paper-3-philosophy-ethics-christianity',
    'paper-1-islam': 'paper-3-philosophy-ethics-islam'
  };

  function reEdexcelFilter(pref) {
    if (!pref || !(pref.paper1 || pref.paper2)) return null;
    var slugs = [];
    if (pref.paper1) slugs.push(pref.paper1);
    if (pref.paper2) slugs.push(pref.paper2);
    // Paper 3 OR Paper 4. Fall back to Paper 3 if examChoice is missing
    // (older saved prefs from before the either/or picker shipped).
    if (pref.examChoice === 'paper4' && pref.paper4) {
      slugs.push(pref.paper4);
    } else if (pref.paper1) {
      var p3 = RE_EDEXCEL_PAPER3_MAP[pref.paper1];
      if (p3) slugs.push(p3);
    }
    return slugs;
  }

  // Film Studies — lesson-level filter, NOT unit-level. Every unit stays
  // visible; lessons whose slug is in FILM_SELECTABLE but not picked are
  // dropped. Returned to callers via getPickedFilmSlugs.
  var FILM_STUDIES_SLUGS = ['film-studies-eduqas'];
  var FILM_SELECTABLE_LIST = [
    'dracula-and-the-lost-boys-vampires-across-eras',
    'singin-in-the-rain-and-grease-the-hollywood-musical',
    'pillow-talk-and-when-harry-met-sally-the-romantic-comedy',
    'rebel-without-a-cause-and-ferris-buellers-day-off-teen-rebellion',
    'invasion-of-the-body-snatchers-and-et-aliens-and-anxiety',
    'juno-tonal-comedy-and-the-indie-voice',
    'whiplash-cutting-sound-and-pursuit-of-greatness',
    'lady-bird-coming-of-age-and-greta-gerwigs-direction',
    'the-hurt-locker-and-the-hate-u-give-issue-led-indies',
    'the-hate-u-give-and-issue-led-indie',
    'slumdog-millionaire-narrative-and-mumbai',
    'district-9-narrative-and-segregation-allegory',
    'the-babadook-narrative-and-grief-as-monster',
    'the-breadwinner-narrative-and-animation-under-occupation',
    'jojo-rabbit-narrative-and-comic-distance',
    'tsotsi-representation-and-johannesburg',
    'the-wave-representation-and-conformity',
    'wadjda-representation-and-saudi-girlhood',
    'girlhood-representation-and-paris-banlieue',
    'the-farewell-representation-and-diaspora-grief',
    'submarine-aesthetic-and-adolescent-imagination',
    'attack-the-block-aesthetic-and-genre-mixing',
    'skyfall-aesthetic-and-bond-cinematography',
    'blinded-by-the-light-aesthetic-and-musical-realism',
    'rocks-aesthetic-and-multicultural-london'
  ];
  var FILM_SELECTABLE_SET = {};
  FILM_SELECTABLE_LIST.forEach(function (s) { FILM_SELECTABLE_SET[s] = true; });

  function filmStudiesPickedSlugs(pref) {
    if (!pref || !pref.films || !Object.keys(pref.films).length) return null;
    return Object.values(pref.films);
  }

  // Geography — lesson-level filter, NOT unit-level. The units are whole exam
  // papers (all compulsory); the optionality lives WITHIN them. Keyed
  // 'unit_slug/lesson_slug' (AQA lesson slugs are 'lesson-NN' and repeat across
  // papers; Edexcel A uses descriptive slugs). A lesson in GEO_SELECTABLE shows
  // only if the student picked its option; lessons NOT in the set (compulsory
  // topics) always show. Per-board option->lesson maps below; add a board by
  // adding its subject slug here + a wizard config in index.html (geographyOptions).
  //   AQA 8035: Paper 1 = 1 ecosystem (Hot Deserts/Cold Env) + 2 of 3 landscapes
  //             (Coasts/Rivers/Glacial); Paper 2 = 1 resource (Energy/Food/Water).
  //   Edexcel A 1GA0: Paper 1 = 2 of 3 landscapes (Coastal/River/Glaciated);
  //                   Paper 2 = 1 resource (Energy/Water).
  //   Eduqas A C111QS: two "choose one of two" options, both in shared units —
  //     Hazards (Tectonic Theme 3 OR Coastal Theme 4) in `tectonic-coastal-hazards`;
  //     Issues (Social Development Theme 7 OR Environmental Challenges Theme 8) in
  //     `social-environmental-challenges`. Lesson-level keying handles the
  //     co-mingled units directly — no structural re-split needed.
  var GEO_SLUGS = ['geography-aqa', 'geography-edexcel-a', 'geography-eduqas'];
  var GEO_OPTION_LESSONS = {
    'geography-aqa': {
      'hot-deserts':       ['paper-1/lesson-12', 'paper-1/lesson-13'],
      'cold-environments': ['paper-1/lesson-21', 'paper-1/lesson-22'],
      'coasts':            ['paper-1/lesson-14', 'paper-1/lesson-15', 'paper-1/lesson-16'],
      'rivers':            ['paper-1/lesson-17', 'paper-1/lesson-18', 'paper-1/lesson-19', 'paper-1/lesson-20'],
      'glacial':           ['paper-1/lesson-23', 'paper-1/lesson-24', 'paper-1/lesson-25'],
      'energy':            ['paper-2/lesson-19', 'paper-2/lesson-20'],
      'food':              ['paper-2/lesson-21', 'paper-2/lesson-22'],
      'water':             ['paper-2/lesson-23', 'paper-2/lesson-24']
    },
    'geography-edexcel-a': {
      'coastal':   ['paper-1-physical-environment/coastal-processes-and-landforms', 'paper-1-physical-environment/coastal-management-and-a-distinctive-uk-coastline'],
      'river':     ['paper-1-physical-environment/river-processes-profiles-and-landforms', 'paper-1-physical-environment/river-management-and-a-distinctive-uk-river'],
      'glaciated': ['paper-1-physical-environment/glaciated-upland-landscapes-and-management', 'paper-1-physical-environment/glaciated-uplands-land-use-tourism-and-management'],
      'energy':    ['paper-2-human-environment/energy-resource-management'],
      'water':     ['paper-2-human-environment/water-resource-management']
    },
    'geography-eduqas': {
      'tectonic-hazards':         ['tectonic-coastal-hazards/tectonic-processes-volcanic-landforms', 'tectonic-coastal-hazards/vulnerability-tectonic-risk'],
      'coastal-hazards':          ['tectonic-coastal-hazards/vulnerable-coastlines', 'tectonic-coastal-hazards/managing-coastlines'],
      'social-development':       ['social-environmental-challenges/measuring-social-development', 'social-environmental-challenges/social-challenges-africa-south-asia'],
      'environmental-challenges': ['social-environmental-challenges/consumerism-and-environment', 'social-environmental-challenges/restoring-and-managing-habitats']
    }
  };
  var GEO_SELECTABLE = {};
  Object.keys(GEO_OPTION_LESSONS).forEach(function (subj) {
    Object.keys(GEO_OPTION_LESSONS[subj]).forEach(function (opt) {
      GEO_OPTION_LESSONS[subj][opt].forEach(function (k) { GEO_SELECTABLE[k] = true; });
    });
  });

  function geographyPickedKeys(pref, subjectSlug) {
    var map = GEO_OPTION_LESSONS[subjectSlug];
    if (!map || !pref || !pref.options || !Object.keys(pref.options).length) return null;
    var picked = [];
    Object.keys(pref.options).forEach(function (group) {
      var v = pref.options[group];
      if (Array.isArray(v)) { v.forEach(function (s) { if (s) picked.push(s); }); }
      else if (v) { picked.push(v); }
    });
    if (!picked.length) return null;
    var keys = [];
    picked.forEach(function (opt) {
      (map[opt] || []).forEach(function (k) { keys.push(k); });
    });
    return keys.length ? keys : null;
  }

  // Classical Civilisation OCR — student picks 1 thematic study (of 2) + 1
  // literature/culture option (of 3). Each option maps to 2 Supabase units, so
  // pref.options stores the OPTION slug per group and we expand to unit slugs.
  var CLASSICAL_CIV_SLUGS = ['classical-civilisation-ocr'];
  var CLASSICAL_CIV_OPTION_UNITS = {
    'myth-and-religion': ['greek-and-roman-mythology', 'greek-and-roman-religion'],
    'women-in-the-ancient-world': ['women-of-legend-and-the-home', 'women-religion-and-power'],
    'the-homeric-world': ['the-mycenaean-world', 'homers-odyssey'],
    'roman-city-life': ['the-roman-city-and-home', 'roman-leisure-and-society'],
    'war-and-warfare': ['greek-warfare-and-the-persian-wars', 'the-roman-army-and-the-values-of-war']
  };

  function classicalCivFilter(pref) {
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    var slugs = [];
    Object.keys(pref.options).forEach(function (group) {
      var optSlug = pref.options[group];
      (CLASSICAL_CIV_OPTION_UNITS[optSlug] || []).forEach(function (u) { slugs.push(u); });
    });
    return slugs.length ? slugs : null;
  }

  // D&T Eduqas (C600QS) — unit-level filter. Students study the core PLUS one
  // in-depth material specialism (1 of 6). The chosen in-depth unit shows; the
  // other five hide; the core units always show. Each in-depth option's slug
  // IS its unit slug, so the filter returns core + the picked unit directly.
  var DT_EDUQAS_SLUGS = ['design-technology-eduqas'];
  var DT_EDUQAS_CORE_UNITS = [
    'design-technology-our-world',
    'materials-and-properties',
    'designing-and-making-principles'
  ];

  function dtEduqasFilter(pref) {
    if (!pref || !pref.options) return null;
    var picked = Object.keys(pref.options).map(function (k) { return pref.options[k]; }).filter(Boolean);
    if (!picked.length) return null;
    return DT_EDUQAS_CORE_UNITS.concat(picked);
  }

  function getAllowedUnitSlugs(subjectSlug) {
    var pref = freePref(subjectSlug);
    if (ENGLIT_SLUGS.indexOf(subjectSlug) !== -1) return englitFilter(pref);
    if (DT_EDUQAS_SLUGS.indexOf(subjectSlug) !== -1) return dtEduqasFilter(pref);
    if (HISTORY_SLUGS.indexOf(subjectSlug) !== -1) return historyFilter(pref);
    if (HISTORY_OCR_SLUGS.indexOf(subjectSlug) !== -1) return historyOcrFilter(pref);
    if (DRAMA_SLUGS.indexOf(subjectSlug) !== -1) return dramaFilter(pref);
    if (CLASSICAL_CIV_SLUGS.indexOf(subjectSlug) !== -1) return classicalCivFilter(pref);
    if (RE_AQA_SLUGS.indexOf(subjectSlug) !== -1) return reAqaFilter(pref);
    if (RE_OCR_SLUGS.indexOf(subjectSlug) !== -1) return reOcrFilter(pref);
    if (RE_EDUQAS_SLUGS.indexOf(subjectSlug) !== -1) return reEduqasFilter(pref);
    if (RE_EDEXCEL_SLUGS.indexOf(subjectSlug) !== -1) return reEdexcelFilter(pref);
    return null;
  }

  function getPickedFilmSlugs(subjectSlug) {
    if (FILM_STUDIES_SLUGS.indexOf(subjectSlug) === -1) return null;
    return filmStudiesPickedSlugs(freePref(subjectSlug));
  }

  // Geography lesson-level picks — returns 'unit_slug/lesson_slug' keys to
  // KEEP (compulsory lessons, not in GEO_SELECTABLE, always show). Null when
  // the subject isn't option-filtered or the user hasn't picked.
  function getPickedGeoSlugs(subjectSlug) {
    if (GEO_SLUGS.indexOf(subjectSlug) === -1) return null;
    return geographyPickedKeys(freePref(subjectSlug), subjectSlug);
  }

  window.FreeUserFilters = {
    getAllowedUnitSlugs: getAllowedUnitSlugs,
    getPickedFilmSlugs: getPickedFilmSlugs,
    FILM_SELECTABLE: FILM_SELECTABLE_SET,
    getPickedGeoSlugs: getPickedGeoSlugs,
    GEO_SELECTABLE: GEO_SELECTABLE
  };
})();
