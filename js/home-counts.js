/* StudyVault — Home Card Counts
   Replaces hardcoded "X units · Y lessons" strings on the homepage with
   live counts from Supabase. Walks all .home-card[data-subject] elements
   and updates their .home-card-detail. Also exposes
   window.HomeCounts.getDetail(slug) for the free-user dynamic renderer.
*/
(function () {
  'use strict';

  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  // English Lit text-pick filtering: free users select 1 Shakespeare + 1
  // 19th-C novel + 1 Modern + 1 Poetry cluster (per board). Mirror the
  // browse-loader filter so home counts match what the student actually sees.
  var ENGLIT_SLUGS = ['english-literature', 'english-literature-aqa', 'english-literature-edexcel',
                       'english-literature-ocr', 'english-literature-eduqas'];
  var ENGLIT_COMPULSORY = ['unseen-poetry'];

  function getFreeEngLitSelectedUnitSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    if (!pref || !pref.texts || !Object.keys(pref.texts).length) return null;
    var slugs = Object.values(pref.texts);
    return slugs.concat(ENGLIT_COMPULSORY);
  }

  // History option-pick filtering: free users pick 1 from each of 4 paper
  // sections (Period · Wider World Depth · Thematic · British Depth). Mirror
  // the browse-loader filter so the home card shows 4 units / N lessons.
  var HISTORY_SLUGS = ['history-aqa', 'history-edexcel'];

  function getFreeHistorySelectedUnitSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    return Object.values(pref.options);
  }

  // Drama: free users pick 1 set play from 9 options. Universal units
  // (theatre roles, practitioners, live theatre review) always show.
  var DRAMA_SLUGS = ['drama-aqa'];
  var DRAMA_UNIVERSAL = ['theatre-roles-stagecraft', 'practitioners-styles', 'live-theatre-review'];

  function getFreeDramaSelectedUnitSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    if (!pref || !pref.options || !Object.keys(pref.options).length) return null;
    return Object.values(pref.options).concat(DRAMA_UNIVERSAL);
  }

  // Religious Studies (AQA): free users pick 2 of 7 religions (each gives
  // Beliefs + Practices) and 4 of 6 themes — visible set = 8 units. Legacy
  // users without picks fall back to the pre-gap-fill 8-unit set.
  // Both old (`religious-education`) and new (`religious-studies-aqa`) slugs
  // listed for the slug-refactor transition window.
  var RE_SLUGS = ['religious-studies-aqa', 'religious-education'];
  var RE_DEFAULT_UNITS = [
    'christianity-beliefs', 'christianity-practices',
    'islam-beliefs', 'islam-practices',
    'theme-a-relationships', 'theme-b-religion-life',
    'theme-d-peace-conflict', 'theme-e-crime-punishment'
  ];

  function getFreeRESelectedUnitSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    // Only filter for free users who actually have RE picked. Anonymous home
    // visitors (no FreeUser session) get the unfiltered 20-unit total.
    if (!pref) return null;
    if ((pref.religions && pref.religions.length) || (pref.themes && pref.themes.length)) {
      var rels = pref.religions || [];
      var thms = pref.themes || [];
      var slugs = [];
      rels.forEach(function (r) {
        slugs.push(r + '-beliefs');
        slugs.push(r + '-practices');
      });
      thms.forEach(function (t) { slugs.push(t); });
      return slugs;
    }
    // Legacy free user: RE picked but no religion/theme data — show default 8.
    return RE_DEFAULT_UNITS.slice();
  }

  // Eduqas / WJEC RS uses a flatter unit structure (no -beliefs/-practices
  // suffix) and Route B has implicit Foundational Catholic Theology units
  // not surfaced in the picker. Mirror browse-loader's filter exactly.
  var RE_EDUQAS_SLUGS = ['religious-studies-eduqas'];

  function getFreeREEduqasSelectedUnitSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    if (!pref) return null;
    if ((pref.religions && pref.religions.length) || (pref.themes && pref.themes.length)) {
      var slugs = (pref.religions || []).slice();
      (pref.themes || []).forEach(function (t) { slugs.push(t); });
      // Route B implicitly adds Foundational Catholic Theology units.
      if (pref.route === 'b' || slugs.indexOf('catholic-christianity') !== -1) {
        slugs.push('catholic-foundational-origins-and-meaning');
        slugs.push('catholic-foundational-good-and-evil');
      }
      return slugs;
    }
    return null;
  }

  // Film Studies: free users pick 1 film from each of 5 sections. Filtering
  // is at LESSON level (each unit contains multiple selectable films).
  var FILM_STUDIES_SLUGS = ['film-studies-eduqas'];
  var FILM_SELECTABLE = {
    'dracula-and-the-lost-boys-vampires-across-eras': true,
    'singin-in-the-rain-and-grease-the-hollywood-musical': true,
    'pillow-talk-and-when-harry-met-sally-the-romantic-comedy': true,
    'rebel-without-a-cause-and-ferris-buellers-day-off-teen-rebellion': true,
    'invasion-of-the-body-snatchers-and-et-aliens-and-anxiety': true,
    'juno-tonal-comedy-and-the-indie-voice': true,
    'whiplash-cutting-sound-and-pursuit-of-greatness': true,
    'lady-bird-coming-of-age-and-greta-gerwigs-direction': true,
    'the-hurt-locker-and-the-hate-u-give-issue-led-indies': true,
    'the-hate-u-give-and-issue-led-indie': true,
    'slumdog-millionaire-narrative-and-mumbai': true,
    'district-9-narrative-and-segregation-allegory': true,
    'the-babadook-narrative-and-grief-as-monster': true,
    'the-breadwinner-narrative-and-animation-under-occupation': true,
    'jojo-rabbit-narrative-and-comic-distance': true,
    'tsotsi-representation-and-johannesburg': true,
    'the-wave-representation-and-conformity': true,
    'wadjda-representation-and-saudi-girlhood': true,
    'girlhood-representation-and-paris-banlieue': true,
    'the-farewell-representation-and-diaspora-grief': true,
    'submarine-aesthetic-and-adolescent-imagination': true,
    'attack-the-block-aesthetic-and-genre-mixing': true,
    'skyfall-aesthetic-and-bond-cinematography': true,
    'blinded-by-the-light-aesthetic-and-musical-realism': true,
    'rocks-aesthetic-and-multicultural-london': true
  };

  function getFreeFilmStudiesPickedFilmSlugs(subjectSlug) {
    if (typeof FreeUser === 'undefined' || !FreeUser.isActive()) return null;
    var pref = FreeUser.getSubject(subjectSlug);
    if (!pref || !pref.films || !Object.keys(pref.films).length) return null;
    return Object.values(pref.films);
  }

  // Determine which subject rows to count for the current viewer.
  // - School student: school's bespoke + subscribed (anything the student can see)
  // - Free user / anonymous: free-tier only (school_id NULL)
  // Filter is applied at the SUBJECT level — count only lessons whose subject
  // matches the viewer's tier.
  function isVisibleSubject(subj) {
    if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive && SchoolSession.isActive()) {
      // For school students, accept their own school's bespoke OR generic (NULL).
      var sid = SchoolSession.getSchoolId && SchoolSession.getSchoolId();
      return subj.school_id == null || subj.school_id === sid;
    }
    // Free user or anonymous → free-tier only
    return subj.school_id == null;
  }

  // Fetch all subjects + units + (paginated) live lessons in parallel.
  async function fetchCounts() {
    var subjectsP = sb.from('subjects').select('id, slug, school_id');
    var unitsP = sb.from('units').select('id, slug, subject_id');

    async function fetchAllLessons() {
      var rows = [];
      var offset = 0;
      while (true) {
        var res = await sb.from('lessons')
          .select('unit_id, tier, slug')
          .eq('status', 'live')
          .range(offset, offset + 999);
        var data = res.data || [];
        rows = rows.concat(data);
        if (data.length < 1000) break;
        offset += 1000;
      }
      return rows;
    }

    var results = await Promise.all([subjectsP, unitsP, fetchAllLessons()]);
    var subjects = results[0].data || [];
    var units = results[1].data || [];
    var lessons = results[2];

    // Build maps
    var unitIdToSubjectId = {};
    var unitIdToSlug = {};
    units.forEach(function (u) {
      unitIdToSubjectId[u.id] = u.subject_id;
      unitIdToSlug[u.id] = u.slug;
    });

    // Group subjects by slug, restricted to ones visible to the current viewer.
    var subjectsBySlug = {};
    subjects.forEach(function (s) {
      if (!isVisibleSubject(s)) return;
      if (!subjectsBySlug[s.slug]) subjectsBySlug[s.slug] = [];
      subjectsBySlug[s.slug].push(s);
    });

    // School students: when a slug has BOTH a bespoke (school-specific) row
    // and a generic (school_id=null) row, only count the bespoke. Otherwise
    // the homepage shows double the units/lessons (Unity History = 8 units
    // 96 lessons instead of 4 / 60). Free users only see generic anyway,
    // so this filter only affects school-logged-in viewers.
    if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive && SchoolSession.isActive()) {
      var schoolId = SchoolSession.getSchoolId && SchoolSession.getSchoolId();
      Object.keys(subjectsBySlug).forEach(function (slug) {
        var list = subjectsBySlug[slug];
        var hasBespoke = list.some(function (s) { return s.school_id === schoolId; });
        if (hasBespoke) {
          subjectsBySlug[slug] = list.filter(function (s) { return s.school_id === schoolId; });
        }
      });
    }

    var counts = {};
    Object.keys(subjectsBySlug).forEach(function (slug) {
      var subjList = subjectsBySlug[slug];
      var subjIds = subjList.map(function (s) { return s.id; });

      // Eng Lit / History / Drama / RE free-tier slugs: filter to selected unit slugs.
      var allowedUnitSlugs = null;
      if (ENGLIT_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeEngLitSelectedUnitSlugs(slug);
      } else if (HISTORY_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeHistorySelectedUnitSlugs(slug);
      } else if (DRAMA_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeDramaSelectedUnitSlugs(slug);
      } else if (RE_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeRESelectedUnitSlugs(slug);
      } else if (RE_EDUQAS_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeREEduqasSelectedUnitSlugs(slug);
      }

      // Film Studies: lesson-level filter (each unit has overviews + multiple
      // selectable films; student picks one per section).
      var pickedFilmSlugs = null;
      if (FILM_STUDIES_SLUGS.indexOf(slug) !== -1) {
        pickedFilmSlugs = getFreeFilmStudiesPickedFilmSlugs(slug);
      }

      var unitCount = 0;
      var lessonCount = 0;
      var matchingUnitIds = {};
      units.forEach(function (u) {
        if (subjIds.indexOf(u.subject_id) === -1) return;
        if (allowedUnitSlugs && allowedUnitSlugs.indexOf(u.slug) === -1) return;
        matchingUnitIds[u.id] = true;
      });

      // Foundation users hide tier='higher' lessons (matches browse-loader behaviour)
      var savedTiers = {};
      try { savedTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch (e) {}
      var thisTier = savedTiers[slug] || 'higher';
      var unitsWithVisibleLessons = {};
      lessons.forEach(function (l) {
        if (!matchingUnitIds[l.unit_id]) return;
        if (thisTier === 'foundation' && l.tier === 'higher') return;
        // Film Studies lesson-level filter: drop selectable lessons not in picks
        if (pickedFilmSlugs && FILM_SELECTABLE[l.slug] && pickedFilmSlugs.indexOf(l.slug) === -1) return;
        lessonCount++;
        unitsWithVisibleLessons[l.unit_id] = true;
      });

      // Unit count = units that have at least one visible lesson after filters.
      // (For unit-level filters this matches matchingUnitIds, so it's a no-op.
      // For Film Studies' lesson-level filter, units with all-hidden lessons drop out.)
      Object.keys(unitsWithVisibleLessons).forEach(function () { unitCount++; });

      counts[slug] = { units: unitCount, lessons: lessonCount };
    });
    return counts;
  }

  function formatDetail(c) {
    if (!c || c.lessons === 0) return '';
    var unitWord = c.units === 1 ? 'unit' : 'units';
    var lessonWord = c.lessons === 1 ? 'lesson' : 'lessons';
    return c.units + ' ' + unitWord + ' · ' + c.lessons + ' ' + lessonWord;
  }

  function applyToStaticCards(counts) {
    var cards = document.querySelectorAll('.home-card[data-subject]');
    cards.forEach(function (card) {
      var slug = card.getAttribute('data-subject');
      var c = counts[slug];
      if (!c) return;
      var detail = card.querySelector('.home-card-detail');
      if (!detail) return;
      var newText = formatDetail(c);
      // Only assign if different — assigning the same value still triggers a
      // DOM mutation, which would re-fire the MutationObserver below and loop
      // forever (this caused the homepage freeze on 2026-04-26 after the
      // tier picker re-rendered #home-grid).
      if (newText && detail.textContent !== newText) detail.textContent = newText;
    });
  }

  window.HomeCounts = {
    counts: null,
    ready: null,
    getDetail: function (slug) {
      if (this.counts && this.counts[slug]) return formatDetail(this.counts[slug]);
      return '';
    }
  };

  window.HomeCounts.ready = fetchCounts().then(function (counts) {
    window.HomeCounts.counts = counts;
    applyToStaticCards(counts);
    // Re-apply after the free-user dynamic renderer runs (it overwrites the grid).
    // index.html main.js triggers free-user render synchronously on DOMContentLoaded.
    // We listen for any future re-render via a MutationObserver on #home-grid.
    var grid = document.getElementById('home-grid');
    if (grid) {
      var applying = false;
      var obs = new MutationObserver(function () {
        if (applying) return;            // prevent infinite re-entry
        applying = true;
        try { applyToStaticCards(counts); }
        finally {
          // Drain any mutations triggered by our own writes before re-arming
          setTimeout(function () { applying = false; }, 0);
        }
      });
      obs.observe(grid, { childList: true, subtree: true });
    }
    return counts;
  }).catch(function (e) {
    console.warn('[home-counts] fetch failed', e);
  });
})();
