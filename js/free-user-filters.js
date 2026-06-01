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

  function getAllowedUnitSlugs(subjectSlug) {
    var pref = freePref(subjectSlug);
    if (ENGLIT_SLUGS.indexOf(subjectSlug) !== -1) return englitFilter(pref);
    if (HISTORY_SLUGS.indexOf(subjectSlug) !== -1) return historyFilter(pref);
    if (HISTORY_OCR_SLUGS.indexOf(subjectSlug) !== -1) return historyOcrFilter(pref);
    if (DRAMA_SLUGS.indexOf(subjectSlug) !== -1) return dramaFilter(pref);
    if (CLASSICAL_CIV_SLUGS.indexOf(subjectSlug) !== -1) return classicalCivFilter(pref);
    if (RE_AQA_SLUGS.indexOf(subjectSlug) !== -1) return reAqaFilter(pref);
    if (RE_EDUQAS_SLUGS.indexOf(subjectSlug) !== -1) return reEduqasFilter(pref);
    if (RE_EDEXCEL_SLUGS.indexOf(subjectSlug) !== -1) return reEdexcelFilter(pref);
    return null;
  }

  function getPickedFilmSlugs(subjectSlug) {
    if (FILM_STUDIES_SLUGS.indexOf(subjectSlug) === -1) return null;
    return filmStudiesPickedSlugs(freePref(subjectSlug));
  }

  window.FreeUserFilters = {
    getAllowedUnitSlugs: getAllowedUnitSlugs,
    getPickedFilmSlugs: getPickedFilmSlugs,
    FILM_SELECTABLE: FILM_SELECTABLE_SET
  };
})();
