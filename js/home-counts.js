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

  // Fetch all subjects + units + (paginated) live lessons in parallel.
  async function fetchCounts() {
    var subjectsP = sb.from('subjects').select('id, slug');
    var unitsP = sb.from('units').select('id, subject_id');

    // Lessons: paginate through live + non-higher-tier rows
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
    var unitsBySubject = {};
    units.forEach(function (u) {
      unitIdToSubjectId[u.id] = u.subject_id;
      if (!unitsBySubject[u.subject_id]) unitsBySubject[u.subject_id] = 0;
      unitsBySubject[u.subject_id]++;
    });
    var lessonsBySubject = {};
    lessons.forEach(function (l) {
      var sid = unitIdToSubjectId[l.unit_id];
      if (!sid) return;
      if (!lessonsBySubject[sid]) lessonsBySubject[sid] = 0;
      lessonsBySubject[sid]++;
    });

    // Build slug → {units, lessons}
    // Multiple subjects may share a slug (Unity + free-tier). Sum across them
    // so slugs like 'business' (Unity) + 'business-aqa/...' (free) work intuitively.
    var counts = {};
    subjects.forEach(function (s) {
      if (!counts[s.slug]) counts[s.slug] = { units: 0, lessons: 0 };
      counts[s.slug].units += unitsBySubject[s.id] || 0;
      counts[s.slug].lessons += lessonsBySubject[s.id] || 0;
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
