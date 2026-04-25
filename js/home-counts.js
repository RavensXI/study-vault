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

  // Fetch all subjects + units + (paginated) live lessons in parallel.
  async function fetchCounts() {
    var subjectsP = sb.from('subjects').select('id, slug');
    var unitsP = sb.from('units').select('id, slug, subject_id');

    async function fetchAllLessons() {
      var rows = [];
      var offset = 0;
      while (true) {
        var res = await sb.from('lessons')
          .select('unit_id')
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

    // Group subjects by slug so we can apply Eng Lit filtering per slug
    var subjectsBySlug = {};
    subjects.forEach(function (s) {
      if (!subjectsBySlug[s.slug]) subjectsBySlug[s.slug] = [];
      subjectsBySlug[s.slug].push(s);
    });

    var counts = {};
    Object.keys(subjectsBySlug).forEach(function (slug) {
      var subjList = subjectsBySlug[slug];
      var subjIds = subjList.map(function (s) { return s.id; });

      // Eng Lit free-tier slugs: filter to selected texts + compulsory
      var allowedUnitSlugs = null;
      if (ENGLIT_SLUGS.indexOf(slug) !== -1) {
        allowedUnitSlugs = getFreeEngLitSelectedUnitSlugs(slug);
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
      lessons.forEach(function (l) {
        if (matchingUnitIds[l.unit_id]) lessonCount++;
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
      if (newText) detail.textContent = newText;
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
      var obs = new MutationObserver(function () { applyToStaticCards(counts); });
      obs.observe(grid, { childList: true, subtree: true });
    }
    return counts;
  }).catch(function (e) {
    console.warn('[home-counts] fetch failed', e);
  });
})();
