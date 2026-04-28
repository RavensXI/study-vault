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
  var ENGLIT_SLUGS = ['english-literature', 'english-literature-edexcel',
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
          .select('unit_id, tier')
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

      // Eng Lit free-tier slugs: filter to selected texts + compulsory
      var allowedUnitSlugs = null;
      if (ENGLIT_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeEngLitSelectedUnitSlugs(slug);
      } else if (HISTORY_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeHistorySelectedUnitSlugs(slug);
      }

      var unitCount = 0;
      var lessonCount = 0;
      var matchingUnitIds = {};
      units.forEach(function (u) {
        if (subjIds.indexOf(u.subject_id) === -1) return;
        if (allowedUnitSlugs && allowedUnitSlugs.indexOf(u.slug) === -1) return;
        matchingUnitIds[u.id] = true;
        unitCount++;
      });

      // Foundation users hide tier='higher' lessons (matches browse-loader behaviour)
      var savedTiers = {};
      try { savedTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch (e) {}
      var thisTier = savedTiers[slug] || 'higher';
      lessons.forEach(function (l) {
        if (!matchingUnitIds[l.unit_id]) return;
        if (thisTier === 'foundation' && l.tier === 'higher') return;
        lessonCount++;
      });

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
