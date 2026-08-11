/**
 * Free user session utility — manages localStorage prefs for anonymous visitors.
 * Separate from SchoolSession (sessionStorage) which is for school students.
 */
(function () {
  var KEY = 'studyvault-free-prefs';
  var WIZ_KEY = 'sv-welcome';

  /* The welcome page's picker writes WIZ_KEY; everything older reads KEY. A
     student who set up on the new front door therefore looked, to the rest of
     the site, like someone who had never chosen anything — and every guide page
     bounced them back to the start. Read the wizard as a fallback so one setup
     satisfies both.

     SUBSLUG is copied verbatim from dash-data.js (the file that owns it) because
     dash-data.js is not loaded on lesson or guide pages. If a subject slug ever
     changes there, change it here too. */
  var SUBSLUG = {
    maths: { aqa: 'maths-aqa', edexcel: 'maths-edexcel', ocr: 'maths-ocr', eduqas: 'maths-eduqas' },
    lang: { aqa: 'english-language-aqa', edexcel: 'english-language-edexcel', ocr: 'english-language-ocr', eduqas: 'english-language-eduqas' },
    lit: { aqa: 'english-literature-aqa', edexcel: 'english-literature-edexcel', ocr: 'english-literature-ocr', eduqas: 'english-literature-eduqas' },
    science: { aqa: 'science-aqa', edexcel: 'science-edexcel', ocr: 'science-ocr' },
    triple: { aqa: 'separate-sciences', edexcel: 'separate-sciences-edexcel', ocr: 'separate-sciences-ocr' },
    history: { aqa: 'history-aqa', edexcel: 'history-edexcel', ocr: 'history-ocr', eduqas: 'history-eduqas' },
    geog: { aqa: 'geography-aqa', edexcel: 'geography-edexcel-a', ocr: 'geography-ocr', eduqas: 'geography-eduqas' },
    french: { aqa: 'french-aqa', edexcel: 'french-edexcel', eduqas: 'french-eduqas' },
    spanish: { aqa: 'spanish-aqa', edexcel: 'spanish-edexcel', eduqas: 'spanish-eduqas' },
    german: { aqa: 'german-aqa', edexcel: 'german-edexcel' },
    cs: { aqa: 'computer-science-aqa', edexcel: 'computer-science-edexcel', ocr: 'computer-science', eduqas: 'computer-science-eduqas' },
    business: { aqa: 'business-aqa', edexcel: 'business-edexcel', ocr: 'business-ocr' },
    pe: { aqa: 'physical-education-aqa', edexcel: 'physical-education-edexcel', ocr: 'physical-education-ocr' },
    psych: { aqa: 'psychology-aqa' },
    rs: { aqa: 'religious-studies-aqa', edexcel: 'religious-studies-edexcel', ocr: 'religious-studies-ocr', eduqas: 'religious-studies-eduqas' },
    socio: { aqa: 'sociology-aqa', eduqas: 'sociology-eduqas' },
    econ: { aqa: 'economics-aqa' }, stats: { aqa: 'statistics-aqa' }, media: { aqa: 'media-studies-aqa' },
    film: { eduqas: 'film-studies-eduqas' }, drama: { aqa: 'drama-aqa' }, music: { aqa: 'music-aqa' },
    mtech: { ncfe: 'music-technology' },
    dt: { aqa: 'design-technology', eduqas: 'design-technology-eduqas' },
    eng: { aqa: 'engineering-aqa', eduqas: 'engineering-eduqas' },
    electronics: { eduqas: 'electronics-eduqas' }, it: { ocr: 'it-ocr' }, astro: { edexcel: 'astronomy-edexcel' },
    geology: { eduqas: 'geology-eduqas' }, classics: { ocr: 'classical-civilisation-ocr' },
    citizenship: { aqa: 'citizenship-aqa' },
    food: { aqa: 'food-preparation-and-nutrition-aqa', eduqas: 'food-preparation-and-nutrition-eduqas' },
    hosp: { eduqas: 'hospitality-catering' },
    hsc: { edexcel: 'health-social-care-edexcel', ocr: 'health-social-care-ocr', eduqas: 'health-social-care-eduqas' }
  };

  /* wizard shape {picked:['history'],boards:{history:'aqa'}} -> free-user shape */
  function fromWizard() {
    try {
      var w = JSON.parse(localStorage.getItem(WIZ_KEY) || 'null');
      if (!w || !Array.isArray(w.picked) || !w.picked.length) return null;
      var subjects = [];
      w.picked.forEach(function (short) {
        var byBoard = SUBSLUG[short];
        if (!byBoard) return;
        var board = (w.boards || {})[short];
        // no board chosen yet: fall back to the only option, or AQA
        var keys = Object.keys(byBoard);
        var slug = byBoard[board] || (keys.length === 1 ? byBoard[keys[0]] : byBoard.aqa);
        if (slug) subjects.push({ slug: slug, baseSlug: short, board: board || null });
      });
      return subjects.length ? { subjects: subjects, fromWizard: true } : null;
    } catch (e) { return null; }
  }


  // One-time slug migrations applied on every read (idempotent — re-runs are
  // no-ops once a user has been migrated). Avoids needing a separate migration
  // script — users get rewritten silently on next page load.
  //
  // History split (Apr 2026): `history` → `history-edexcel` so the AQA build
  // could take `history-aqa`.
  //
  // Free-tier slug consistency refactor (May 2026): every free-tier subject
  // now ends with -{board}. Old bare-slug entries get rewritten:
  //   english-language    → english-language-aqa
  //   english-literature  → english-literature-aqa
  //   maths               → maths-edexcel
  //   science             → science-aqa
  //   religious-education → religious-studies-aqa  (also baseSlug rename)
  //   geography           → geography-aqa
  //   health-social-care  → health-social-care-edexcel
  var SLUG_MIGRATIONS = {
    'history':             { slug: 'history-edexcel',          examBoard: 'edexcel' },
    'english-language':    { slug: 'english-language-aqa',     examBoard: 'aqa' },
    'english-literature':  { slug: 'english-literature-aqa',   examBoard: 'aqa' },
    'maths':               { slug: 'maths-edexcel',            examBoard: 'edexcel' },
    'science':             { slug: 'science-aqa',              examBoard: 'aqa' },
    'religious-education': { slug: 'religious-studies-aqa',    examBoard: 'aqa', baseSlug: 'religious-studies' },
    'geography':           { slug: 'geography-aqa',            examBoard: 'aqa' },
    'health-social-care':  { slug: 'health-social-care-edexcel', examBoard: 'edexcel' }
  };

  function migrateSlugs(prefs) {
    if (!prefs || !prefs.subjects) return prefs;
    var changed = false;
    prefs.subjects.forEach(function (s) {
      var mig = SLUG_MIGRATIONS[s.slug];
      if (mig) {
        s.slug = mig.slug;
        if (!s.examBoard && mig.examBoard) s.examBoard = mig.examBoard;
        if (mig.baseSlug && s.baseSlug && SLUG_MIGRATIONS[s.baseSlug]) {
          // baseSlug also needs renaming (e.g. religious-education → religious-studies)
          s.baseSlug = mig.baseSlug;
        }
        changed = true;
      }
    });
    if (changed) {
      try { localStorage.setItem(KEY, JSON.stringify(prefs)); } catch (e) {}
    }
    return prefs;
  }

  window.FreeUser = {
    get: function () {
      try {
        var raw = localStorage.getItem(KEY);
        if (raw) {
          var p = migrateSlugs(JSON.parse(raw));
          if (p && p.subjects && p.subjects.length) return p;
        }
        return fromWizard();     // set up on the new welcome page instead
      } catch (e) {
        return fromWizard();
      }
    },

    set: function (data) {
      data.createdAt = data.createdAt || new Date().toISOString();
      localStorage.setItem(KEY, JSON.stringify(data));
    },

    clear: function () {
      localStorage.removeItem(KEY);
    },

    isActive: function () {
      var prefs = this.get();
      return prefs !== null && prefs.subjects && prefs.subjects.length > 0;
    },

    getSubjectSlugs: function () {
      var prefs = this.get();
      if (!prefs || !prefs.subjects) return [];
      return prefs.subjects.map(function (s) { return s.slug; });
    },

    getSubject: function (slug) {
      var prefs = this.get();
      if (!prefs || !prefs.subjects) return null;
      // Match by exact slug or by baseSlug (for multi-board subjects)
      return prefs.subjects.find(function (s) { return s.slug === slug || s.baseSlug === slug; }) || null;
    }
  };
})();
