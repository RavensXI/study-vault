/* ============================================
   StudyVault — Browse Loader
   Renders subject landing pages and unit index pages from Supabase.
   Routes: /browse/{subject}        → subject landing (shows unit cards)
           /browse/{subject}/{unit}  → unit index (shows lesson cards)
   ============================================ */

(function () {
  'use strict';

  var sb = window.supabase.createClient(
    'https://baipckgywpnwapobwtsy.supabase.co',
    'sb_publishable_PYj2nvjclOsUWmZPolhRuA_1OvYhnc2'
  );

  var loadingEl = document.getElementById('browse-loading');
  var errorEl = document.getElementById('browse-error');
  var contentEl = document.getElementById('browse-content');

  // ---- Parse URL ----
  function parseUrl() {
    var path = window.location.pathname;
    var match = path.match(/^\/browse\/([^/]+)(?:\/([^/]+))?\/?$/);
    if (!match) return null;
    return {
      subjectSlug: match[1],
      unitSlug: match[2] || null
    };
  }

  // ---- One-time slug migration ----
  // Old free-tier slugs that have been renamed for consistency. For Unity
  // students (school session active), most of these still map to the bespoke
  // version of the same slug — don't redirect them. For free / anonymous
  // users, redirect to the suffixed equivalent and preserve any pref-based
  // board choice.
  //
  // History (Apr 2026): `history` → `history-edexcel` so AQA could take `history-aqa`.
  // Slug refactor (May 2026): every free-tier subject is now -{board} suffixed.
  var OLD_TO_NEW_SLUGS = {
    'history':             ['history-aqa', 'history-edexcel'],
    'english-language':    ['english-language-aqa', 'english-language-edexcel', 'english-language-ocr', 'english-language-eduqas'],
    'english-literature':  ['english-literature-aqa', 'english-literature-edexcel', 'english-literature-ocr', 'english-literature-eduqas'],
    'maths':               ['maths-edexcel', 'maths-aqa', 'maths-ocr', 'maths-eduqas'],
    'science':             ['science-aqa', 'science-edexcel', 'science-ocr'],
    'religious-education': ['religious-studies-aqa'],
    'geography':           ['geography-aqa', 'geography-edexcel-a', 'geography-edexcel-b', 'geography-ocr', 'geography-eduqas'],
    'health-social-care':  ['health-social-care-edexcel', 'health-social-care-ocr'],
    // food-technology renamed to food-preparation-and-nutrition for Unity bespoke;
    // free users got food-preparation-and-nutrition-eduqas as the only built option.
    'food-technology':     ['food-preparation-and-nutrition-eduqas']
  };

  function chooseRedirectTarget(oldSlug) {
    var candidates = OLD_TO_NEW_SLUGS[oldSlug] || [];
    if (!candidates.length) return null;
    // Prefer a target the user has already picked
    if (typeof FreeUser !== 'undefined' && FreeUser.isActive && FreeUser.isActive()) {
      for (var i = 0; i < candidates.length; i++) {
        var c = candidates[i];
        if (FreeUser.getSubject(c)) return c;
      }
      // Also check via baseSlug match (e.g. baseSlug='religious-studies' matches 'religious-studies-aqa')
      var baseGuess = candidates[0].replace(/-(aqa|edexcel|edexcel-a|edexcel-b|ocr|eduqas)$/, '');
      var byBase = FreeUser.getSubject(baseGuess);
      if (byBase && byBase.slug) return byBase.slug;
    }
    // Otherwise default to the first candidate (the AQA / Edexcel / dominant build)
    return candidates[0];
  }

  function maybeRedirectOldSlug(slug) {
    if (!OLD_TO_NEW_SLUGS[slug]) return false;
    // Unity students keep using bare slugs for their bespoke content (matches
    // Supabase row scoped by school_id). Don't redirect them.
    var isUnity = (typeof SchoolSession !== 'undefined' && SchoolSession.isActive && SchoolSession.isActive());
    if (isUnity) return false;
    var target = chooseRedirectTarget(slug);
    if (!target) return false;
    var newPath = window.location.pathname.replace(
      new RegExp('^/browse/' + slug.replace(/[-]/g, '\\-') + '(/|$)'),
      '/browse/' + target + '$1'
    );
    if (newPath !== window.location.pathname) {
      window.location.replace(newPath + (window.location.search || '') + (window.location.hash || ''));
      return true;
    }
    return false;
  }
  // Back-compat alias for any callers still using the old name
  var maybeRedirectOldHistorySlug = maybeRedirectOldSlug;

  // ---- baseSlug → board picker ----
  // Some URLs are baseSlugs (e.g. /browse/physical-education) shared across
  // multiple boards, no real Supabase row. When the lookup fails for these,
  // render a small board-picker page instead of a 404.
  // Mirrors slugMap in index.html — kept manually in sync. Each entry is the
  // baseSlug → list of {board, slug, label} pairs we have built content for.
  var BASE_SLUG_BOARDS = {
    'english-language': [
      { board: 'AQA', slug: 'english-language-aqa' },
      { board: 'Edexcel', slug: 'english-language-edexcel' },
      { board: 'OCR', slug: 'english-language-ocr' },
      { board: 'Eduqas', slug: 'english-language-eduqas' }
    ],
    'english-literature': [
      { board: 'AQA', slug: 'english-literature-aqa' },
      { board: 'Edexcel', slug: 'english-literature-edexcel' },
      { board: 'OCR', slug: 'english-literature-ocr' },
      { board: 'Eduqas', slug: 'english-literature-eduqas' }
    ],
    'maths': [
      { board: 'Edexcel', slug: 'maths-edexcel' },
      { board: 'AQA', slug: 'maths-aqa' },
      { board: 'OCR', slug: 'maths-ocr' },
      { board: 'Eduqas', slug: 'maths-eduqas' }
    ],
    'science': [
      { board: 'AQA', slug: 'science-aqa' },
      { board: 'Edexcel', slug: 'science-edexcel' },
      { board: 'OCR', slug: 'science-ocr' }
    ],
    'business': [
      { board: 'AQA', slug: 'business-aqa' },
      { board: 'Edexcel', slug: 'business-edexcel' },
      { board: 'OCR', slug: 'business-ocr' }
    ],
    'psychology': [
      { board: 'AQA', slug: 'psychology-aqa' },
      { board: 'Edexcel', slug: 'psychology-edexcel' },
      { board: 'OCR', slug: 'psychology-ocr' }
    ],
    'french': [
      { board: 'AQA', slug: 'french-aqa' },
      { board: 'Edexcel', slug: 'french-edexcel' }
    ],
    'spanish': [
      { board: 'AQA', slug: 'spanish-aqa' },
      { board: 'Edexcel', slug: 'spanish-edexcel' }
    ],
    'german': [
      { board: 'AQA', slug: 'german-aqa' },
      { board: 'Edexcel', slug: 'german-edexcel' }
    ],
    'sociology': [
      { board: 'AQA', slug: 'sociology-aqa' },
      { board: 'Eduqas', slug: 'sociology-eduqas' },
      { board: 'WJEC', slug: 'sociology-eduqas' }
    ],
    'geography': [
      { board: 'AQA', slug: 'geography-aqa' },
      { board: 'Edexcel A', slug: 'geography-edexcel-a' },
      { board: 'Edexcel B', slug: 'geography-edexcel-b' },
      { board: 'OCR', slug: 'geography-ocr' },
      { board: 'Eduqas', slug: 'geography-eduqas' }
    ],
    'history': [
      { board: 'AQA', slug: 'history-aqa' },
      { board: 'Edexcel', slug: 'history-edexcel' },
      { board: 'OCR', slug: 'history-ocr' },
      { board: 'Eduqas', slug: 'history-eduqas' }
    ],
    'physical-education': [
      { board: 'AQA', slug: 'physical-education-aqa' },
      { board: 'OCR', slug: 'physical-education-ocr' }
    ],
    'religious-studies': [
      { board: 'AQA', slug: 'religious-studies-aqa' },
      { board: 'Edexcel', slug: 'religious-studies-edexcel' },
      { board: 'Eduqas', slug: 'religious-studies-eduqas' },
      { board: 'WJEC', slug: 'religious-studies-eduqas' }
    ],
    'health-social-care': [
      { board: 'Edexcel', slug: 'health-social-care-edexcel' },
      { board: 'OCR', slug: 'health-social-care-ocr' },
      { board: 'Eduqas', slug: 'health-social-care-eduqas' },
      { board: 'WJEC', slug: 'health-social-care-eduqas' }
    ],
    'food-preparation-and-nutrition': [
      { board: 'Eduqas', slug: 'food-preparation-and-nutrition-eduqas' }
      // aqa, ocr to come
    ],
    'statistics': [
      { board: 'AQA', slug: 'statistics-aqa' }
    ],
    'enterprise-and-marketing': [
      { board: 'OCR', slug: 'cambridge-nationals-enterprise-and-marketing' }
    ],
    'sport-studies': [
      { board: 'OCR', slug: 'cambridge-nationals-sport-studies' }
    ],
    'computer-science': [
      { board: 'OCR', slug: 'computer-science' },
      { board: 'AQA', slug: 'computer-science-aqa' },
      { board: 'Edexcel', slug: 'computer-science-edexcel' },
      { board: 'Eduqas', slug: 'computer-science-eduqas' },
      { board: 'WJEC', slug: 'computer-science-eduqas' }
    ],
    'engineering': [
      { board: 'AQA', slug: 'engineering-aqa' },
      { board: 'Eduqas', slug: 'engineering-eduqas' },
      { board: 'WJEC', slug: 'engineering-eduqas' }
    ],
    'astronomy': [
      { board: 'Edexcel', slug: 'astronomy-edexcel' }
    ],
    'design-technology': [
      { board: 'AQA', slug: 'design-technology' },
      { board: 'Eduqas', slug: 'design-technology-eduqas' },
      { board: 'WJEC', slug: 'design-technology-eduqas' }
    ],
    'electronics': [
      { board: 'Eduqas', slug: 'electronics-eduqas' },
      { board: 'WJEC', slug: 'electronics-eduqas' }
    ],
    'geology': [
      { board: 'Eduqas', slug: 'geology-eduqas' },
      { board: 'WJEC', slug: 'geology-eduqas' }
    ],
    'film-studies': [
      { board: 'Eduqas', slug: 'film-studies-eduqas' },
      { board: 'WJEC', slug: 'film-studies-eduqas' }
    ],
    'hospitality-catering': [
      { board: 'Eduqas', slug: 'hospitality-catering' },
      { board: 'WJEC', slug: 'hospitality-catering' }
    ]
  };

  function renderBoardPicker(baseSlug) {
    var boards = BASE_SLUG_BOARDS[baseSlug];
    if (!boards || !boards.length) return false;

    // Pretty subject name from baseSlug
    var prettyName = baseSlug.split('-').map(function (w) {
      return w.charAt(0).toUpperCase() + w.slice(1);
    }).join(' ');

    loadingEl.style.display = 'none';

    // If only one board exists, just redirect there
    if (boards.length === 1) {
      window.location.replace('/browse/' + boards[0].slug + (window.location.search || '') + (window.location.hash || ''));
      return true;
    }

    document.title = prettyName + ' — Pick exam board · StudyVault';
    contentEl.style.display = '';

    var html = '';
    html += '<header class="subject-header" style="text-align:center; padding: 2rem 1rem 1.5rem;">';
    html += '<h1 style="font-family:\'Source Serif 4\',Georgia,serif; font-size:2rem; font-weight:700; margin:0 0 0.4rem;">' + esc(prettyName) + '</h1>';
    html += '<p style="color:#6b645c; font-size:1rem; margin:0;">Pick your exam board to get started.</p>';
    html += '</header>';
    html += '<div style="max-width:540px; margin:0 auto 2rem; padding:0 1rem; display:flex; flex-direction:column; gap:0.65rem;">';
    boards.forEach(function (b) {
      html += '<a href="/browse/' + esc(b.slug) + '" ';
      html += 'style="display:flex; justify-content:space-between; align-items:center; padding:1rem 1.25rem; background:#fff; border:1.5px solid #e8e2d8; border-radius:14px; text-decoration:none; color:#2d2a26; font-weight:600; transition:border-color 0.2s, transform 0.15s;" ';
      html += 'onmouseover="this.style.borderColor=\'#c15a3a\'; this.style.transform=\'translateY(-1px)\';" ';
      html += 'onmouseout="this.style.borderColor=\'#e8e2d8\'; this.style.transform=\'translateY(0)\';">';
      html += '<span>' + esc(b.board) + '</span>';
      html += '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
      html += '</a>';
    });
    html += '</div>';
    html += '<p style="text-align:center; color:#9a938a; font-size:0.85rem; margin:0 1rem 2rem;">Don\'t see your board? <a href="/" style="color:#c15a3a;">Request it on the homepage</a>.</p>';
    contentEl.innerHTML = html;
    return true;
  }

  // ---- Auth check ----
  async function checkAuth() {
    var result = await sb.auth.getSession();
    if (result.data.session) return true;
    var raw = localStorage.getItem('studyvault-user');
    if (raw) return true;
    return false;
  }

  // ---- Show error ----
  function showError(title, message) {
    loadingEl.style.display = 'none';
    document.getElementById('error-title').textContent = title;
    document.getElementById('error-message').textContent = message;
    errorEl.style.display = '';
  }

  // ---- Escape HTML ----
  function esc(str) {
    var div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  // ---- Render subject landing page (unit cards) ----
  async function renderSubjectLanding(subjectSlug) {
    // Redirect /browse/separate-sciences → /browse/science (units merge into science)
    if (subjectSlug === 'separate-sciences') {
      window.location.replace('/browse/science');
      return;
    }

    // Determine content source: bespoke (school-specific) or generic (school_id NULL)
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(subjectSlug));

    // School students can only access subscribed or bespoke subjects
    if (typeof SchoolSession !== 'undefined' && SchoolSession.isActive() && !hasBespoke && !SchoolSession.isSubscribed(subjectSlug)) {
      // Base-slug landing (e.g. /browse/maths) → if the school subscribes to a
      // single board variant (e.g. maths-edexcel), redirect there. If more than
      // one variant is subscribed, fall through to the standard board picker
      // (the user can still pick). If none, show the not-subscribed error.
      var variants = BASE_SLUG_BOARDS[subjectSlug];
      if (variants) {
        var subscribedVariants = variants.filter(function (v) {
          return SchoolSession.isSubscribed(v.slug) || SchoolSession.hasBespoke(v.slug);
        });
        if (subscribedVariants.length === 1) {
          window.location.replace('/browse/' + subscribedVariants[0].slug + (window.location.search || '') + (window.location.hash || ''));
          return;
        }
        if (subscribedVariants.length > 1) {
          // Multiple variants — let the standard flow render the picker.
        } else {
          showError('Subject not available', 'Your school does not currently subscribe to this subject.');
          return;
        }
      } else {
        showError('Subject not available', 'Your school does not currently subscribe to this subject.');
        return;
      }
    }

    var subjectQuery = sb
      .from('subjects')
      .select('id, slug, name, exam_board, spec_code, color, image_url, settings')
      .eq('slug', subjectSlug);

    if (hasBespoke) {
      subjectQuery = subjectQuery.eq('school_id', SchoolSession.getSchoolId());
    } else {
      subjectQuery = subjectQuery.is('school_id', null);
    }

    var subjectResult = await subjectQuery.maybeSingle();

    if (subjectResult.error || !subjectResult.data) {
      // Before showing 404 — is this a baseSlug we have multiple boards for?
      // If yes, render the board picker instead.
      if (renderBoardPicker(subjectSlug)) return;
      showError('Subject not found', 'No subject found with slug "' + subjectSlug + '"');
      return;
    }

    var subject = subjectResult.data;

    var unitsResult = await sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, image_url, lesson_count, sort_order')
      .eq('subject_id', subject.id)
      .order('sort_order');

    var units = unitsResult.data || [];

    // Merge Separate Sciences units into Science when student takes triple
    var isScienceSubject = subjectSlug === 'science' || subjectSlug.indexOf('science-') === 0;
    var hasSepSci = false;
    if (isScienceSubject) {
      try {
        var picks = JSON.parse(localStorage.getItem('studyvault-subjects') || '[]');
        hasSepSci = picks.indexOf('separate-sciences') !== -1;
      } catch(e) {}
      // Also check free user prefs
      if (!hasSepSci && typeof FreeUser !== 'undefined' && FreeUser.isActive()) {
        hasSepSci = FreeUser.getSubjectSlugs().indexOf('separate-sciences') !== -1;
      }
      if (hasSepSci) {
        // Fetch the separate-sciences subject and merge its units
        var sepQuery = sb.from('subjects').select('id').eq('slug', 'separate-sciences');
        if (hasBespoke) {
          sepQuery = sepQuery.eq('school_id', SchoolSession.getSchoolId());
        } else {
          sepQuery = sepQuery.is('school_id', null);
        }
        var sepResult = await sepQuery.maybeSingle();
        if (sepResult.data) {
          var sepUnitsResult = await sb.from('units')
            .select('id, slug, name, subtitle, body_class, accent, image_url, lesson_count, sort_order')
            .eq('subject_id', sepResult.data.id)
            .order('sort_order');
          var sepUnits = sepUnitsResult.data || [];
          // Only add units that aren't already in the combined list (by slug)
          var existingSlugs = units.map(function(u) { return u.slug; });
          sepUnits.forEach(function(su) {
            if (existingSlugs.indexOf(su.slug) === -1) {
              su.sort_order = (units.length ? units[units.length - 1].sort_order : 0) + su.sort_order + 1;
              su._isSeparateScience = true;
              units.push(su);
            }
          });
          // Also merge practice_units from sep sci settings
          if (subject.settings && sepResult.data) {
            var sepSubjResult = await sb.from('subjects').select('settings').eq('id', sepResult.data.id).single();
            if (sepSubjResult.data && sepSubjResult.data.settings && sepSubjResult.data.settings.practice_units) {
              subject.settings.practice_units = (subject.settings.practice_units || []).concat(sepSubjResult.data.settings.practice_units);
            }
          }
        }
      }
    }


    // Always live-count lessons per unit (replaces stale unit.lesson_count column).
    // Foundation users on tiered subjects get the count with tier='higher' excluded.
    var TIERED_OVERVIEW = ['maths', 'maths-edexcel', 'maths-aqa', 'maths-ocr', 'maths-eduqas', 'science', 'science-aqa', 'science-edexcel', 'science-ocr', 'science-ocr-b', 'separate-sciences', 'separate-sciences-edexcel', 'separate-sciences-ocr', 'separate-sciences-ocr-b', 'statistics', 'statistics-aqa'];
    var savedTiersOverview = {};
    try { savedTiersOverview = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch(e) {}
    // Tier picker writes under the base slug (e.g. 'separate-sciences') but
    // browse URLs use the board-specific slug (e.g. 'separate-sciences-edexcel').
    // Fall back to base slug if the fully-qualified slug isn't set.
    var overviewTier = savedTiersOverview[subjectSlug];
    if (!overviewTier) {
      var overviewBase = subjectSlug.replace(/-(?:aqa|edexcel|ocr-b|ocr|eduqas)$/, '');
      overviewTier = savedTiersOverview[overviewBase];
    }
    overviewTier = overviewTier || 'higher';
    var foundationFilter = (TIERED_OVERVIEW.indexOf(subjectSlug) !== -1 && overviewTier === 'foundation');
    var countPromises = units.map(function (u) {
      var q = sb.from('lessons').select('id', { count: 'exact', head: true })
        .eq('unit_id', u.id).eq('status', 'live');
      if (foundationFilter) q = q.neq('tier', 'higher');
      return q.then(function (res) { u._filteredCount = res.count || 0; });
    });
    await Promise.all(countPromises);

    // Free-user option filters (Eng Lit text picks, History options, Drama
    // set play, RE-AQA religions/themes, RE-Eduqas Route A/B picks,
    // RE-Edexcel Paper 1+2+(3-or-4)). Per-subject logic lives in
    // js/free-user-filters.js so this filter and the homepage card counts
    // share one allowlist source. To add a new option-route subject, add
    // its handler to FreeUserFilters — no edits needed here.
    if (typeof window.FreeUserFilters !== 'undefined') {
      var allowedFreeUserSlugs = window.FreeUserFilters.getAllowedUnitSlugs(subjectSlug);
      if (allowedFreeUserSlugs) {
        units = units.filter(function (u) {
          return allowedFreeUserSlugs.indexOf(u.slug) !== -1;
        });
      }
    }

    // Free user Film Studies: lesson-level filter (each unit has overviews
    // plus multiple selectable films; student picks one per section).
    // Universal units (film-form, foundations, developments) keep all their
    // lessons; only the set-film units have their lessons trimmed. Selectable
    // lesson slug set lives in FreeUserFilters.FILM_SELECTABLE.
    if (typeof window.FreeUserFilters !== 'undefined') {
      var pickedFilmList = window.FreeUserFilters.getPickedFilmSlugs(subjectSlug);
      if (pickedFilmList) {
        var pickedFilmSet = new Set(pickedFilmList);
        var FILM_SELECTABLE_MAP = window.FreeUserFilters.FILM_SELECTABLE;
        var filmCountPromises = units.map(function (u) {
          return sb.from('lessons').select('slug, tier').eq('unit_id', u.id).eq('status', 'live')
            .then(function (res) {
              var rows = res.data || [];
              if (foundationFilter) rows = rows.filter(function (r) { return r.tier !== 'higher'; });
              rows = rows.filter(function (r) {
                if (FILM_SELECTABLE_MAP[r.slug]) return pickedFilmSet.has(r.slug);
                return true;
              });
              u._filteredCount = rows.length;
            });
        });
        await Promise.all(filmCountPromises);
      }
    }

    // Free user Geography: lesson-level filter (papers contain optional topics
    // the student chooses between — ecosystem, two of three landscapes, one
    // resource). Compulsory lessons always show. Selectable lessons are keyed
    // 'unit_slug/lesson_slug' because geography slugs (lesson-NN) repeat
    // across papers. Keys/picks live in FreeUserFilters.GEO_SELECTABLE.
    if (typeof window.FreeUserFilters !== 'undefined') {
      var pickedGeoList = window.FreeUserFilters.getPickedGeoSlugs(subjectSlug);
      if (pickedGeoList) {
        var pickedGeoSet = new Set(pickedGeoList);
        var GEO_SELECTABLE_MAP = window.FreeUserFilters.GEO_SELECTABLE;
        var geoCountPromises = units.map(function (u) {
          return sb.from('lessons').select('slug, tier').eq('unit_id', u.id).eq('status', 'live')
            .then(function (res) {
              var rows = res.data || [];
              if (foundationFilter) rows = rows.filter(function (r) { return r.tier !== 'higher'; });
              rows = rows.filter(function (r) {
                var key = u.slug + '/' + r.slug;
                if (GEO_SELECTABLE_MAP[key]) return pickedGeoSet.has(key);
                return true;
              });
              u._filteredCount = rows.length;
            });
        });
        await Promise.all(geoCountPromises);
      }
    }

    document.title = subject.name + ' - StudyVault';
    document.getElementById('header-unit-label').textContent = subject.name;

    // Add nav links
    var nav = document.getElementById('header-nav');
    var isPracticeSubject = subject.settings && subject.settings.format === 'practice';
    var hasExamGuides = !!(subject.settings && subject.settings.has_exam_guides);
    var navHtml = '<a href="/">Home</a>';
    if (!isPracticeSubject) {
      if (hasExamGuides) {
        navHtml += '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>';
      }
      navHtml += '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';
    }
    nav.innerHTML = navHtml;

    // Apply colour theme from first unit
    if (units.length > 0) {
      if (units[0].body_class) document.body.classList.add(units[0].body_class);
      if (units[0].accent) document.documentElement.style.setProperty('--accent', units[0].accent);
    }

    // Build HTML matching static landing page structure
    var html = '';

    // Hero
    var displayName = hasSepSci ? 'Science (Triple)' : subject.name;
    html += '<section class="hero"><h1>' + esc(displayName) + '</h1>';
    if (TIERED_OVERVIEW.indexOf(subjectSlug) !== -1) {
      var tierBadgeLabel = overviewTier === 'foundation' ? 'Foundation' : 'Higher';
      html += '<p style="font-family:Inter,sans-serif;font-size:0.8rem;font-weight:600;color:var(--text-secondary);margin:0.5rem 0 0;letter-spacing:0.03em">' + tierBadgeLabel + ' tier</p>';
    }
    html += '</section>';

    // Quote ticker — between title and unit cards
    if (subject.settings && subject.settings.quote_ticker_html) {
      html += subject.settings.quote_ticker_html;
    }

    // Subject notice — soft dismissible banner used to flag in-flight
    // changes the user should know about (e.g. an upcoming spec change
    // that we haven't built coverage for yet). Renders if the subject
    // has `settings.subject_notice` populated; dismissed once per
    // browser, keyed on the notice's `dismiss_key` so a new notice on
    // the same subject re-appears.
    if (subject.settings && subject.settings.subject_notice) {
      var notice = subject.settings.subject_notice;
      if (notice && notice.html) {
        var dismissKey = 'sv-subject-notice-' + subjectSlug + '-' + (notice.dismiss_key || 'default');
        var alreadyDismissed = false;
        try { alreadyDismissed = localStorage.getItem(dismissKey) === '1'; } catch (e) {}
        if (!alreadyDismissed) {
          html += '<div class="subject-notice" id="subject-notice" style="max-width:760px; margin:1rem auto 0; padding:0.85rem 1.1rem; background:#fef3c7; border:1px solid #fcd34d; border-radius:12px; display:flex; gap:0.85rem; align-items:flex-start; font-size:0.9rem; color:#78350f; line-height:1.45;">';
          html += '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; margin-top:0.1rem;"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>';
          html += '<div style="flex:1;">' + notice.html + '</div>';
          html += '<button type="button" onclick="(function(b){try{localStorage.setItem(\'' + dismissKey + '\',\'1\');}catch(e){} var n=document.getElementById(\'subject-notice\'); if(n){n.style.display=\'none\';}})(this)" aria-label="Dismiss notice" style="background:none; border:none; cursor:pointer; color:#78350f; padding:0; line-height:1; flex-shrink:0;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>';
          html += '</div>';
        }
      }
    }

    // Unit grid — uses same .unit-card structure as static pages
    html += '<div class="unit-grid' + (units.length === 1 ? ' single-unit' : '') + '">';

    // Get image positions from subject settings
    var imgPositions = (subject.settings && subject.settings.unit_image_positions) || {};

    units.forEach(function (unit) {
      var unitLessonCount = unit._filteredCount != null ? unit._filteredCount : unit.lesson_count;
      // Skip units with no visible lessons (e.g. higher-only units for Foundation users)
      if (unitLessonCount === 0) return;
      html += '<a href="/browse/' + subjectSlug + '/' + unit.slug + '" class="unit-card" data-unit="' + esc(unit.slug) + '" data-total-lessons="' + unitLessonCount + '" style="--card-accent: ' + unit.accent + ';">';
      html += '<div class="unit-card-image">';
      if (unit.image_url) {
        var imgStyle = imgPositions[unit.slug] ? ' style="object-position: ' + imgPositions[unit.slug] + '"' : '';
        html += '<img src="' + esc(unit.image_url) + '" alt="' + esc(unit.name) + '"' + imgStyle + '>';
      }
      html += '</div>';
      html += '<div class="unit-card-body">';
      html += '<h2>' + esc(unit.name) + '</h2>';
      if (unit.subtitle) {
        html += '<p class="unit-subtitle">' + esc(unit.subtitle) + '</p>';
      }
      html += '<span class="unit-meta">0 of ' + unitLessonCount + ' lessons visited</span>';
      html += '<div class="progress-bar-track"><div class="progress-bar-fill"></div></div>';
      html += '</div></a>';
    });

    html += '</div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';

    // Apply localStorage visited counts to the freshly-rendered unit cards.
    // Phase 1 ran updateHomepageProgress at DOMContentLoaded but the cards
    // didn't exist yet (Supabase fetch is async), so the static "0 of N"
    // labels need a manual second pass here.
    if (typeof updateHomepageProgress === 'function') updateHomepageProgress();

    // Add nav icons (pencil/lightbulb) to Exam Technique / Revision Techniques links
    if (typeof initNavIcons === 'function') initNavIcons();

    // Render the exam-countdown pill now that the dynamic .hero section
    // exists. The script also auto-fires 500ms after DOMContentLoaded, but
    // that race can lose to slow Supabase fetches on first visit. Calling
    // explicitly after render guarantees the pill appears on cold loads.
    // Idempotent — a duplicate from the timer is suppressed.
    if (typeof window.initExamCountdown === 'function') window.initExamCountdown();

    // Deck-reveal on first visit to this subject — same animation as the
    // homepage personalisation moment, gives a sense of the unit cards
    // being assembled. Repeat visits skip straight to the static reveal
    // animation so they feel snappy.
    var seenKey = 'sv-browse-seen-' + subjectSlug;
    var seenBefore = false;
    try { seenBefore = !!localStorage.getItem(seenKey); } catch (e) {}
    var unitGrid = contentEl.querySelector('.unit-grid');
    if (!seenBefore && unitGrid && typeof window._svDeckReveal === 'function') {
      window._svDeckReveal(unitGrid, { shimmerClass: 'unit-card-shimmer' });
      try { localStorage.setItem(seenKey, '1'); } catch (e) {}
    } else if (typeof initRevealAnimations === 'function') {
      initRevealAnimations();
    }
  }

  // ---- Render unit index page (lesson cards) ----
  async function renderUnitIndex(subjectSlug, unitSlug) {
    var hasBespoke = (typeof SchoolSession !== 'undefined' && SchoolSession.hasBespoke(subjectSlug));

    var unitQuery = sb
      .from('units')
      .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, school_id, settings)')
      .eq('slug', unitSlug)
      .eq('subjects.slug', subjectSlug);

    if (hasBespoke) {
      unitQuery = unitQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
    } else {
      unitQuery = unitQuery.is('subjects.school_id', null);
    }

    var unitResult = await unitQuery.maybeSingle();

    // Fallback: if viewing science and unit not found, try separate-sciences
    if (!unitResult.data && (subjectSlug === 'science' || subjectSlug.indexOf('science-') === 0)) {
      var sepQuery = sb.from('units')
        .select('id, slug, name, subtitle, body_class, accent, accent_light, accent_badge, lesson_count, subject_id, subjects!inner(id, slug, name, school_id, settings)')
        .eq('slug', unitSlug)
        .eq('subjects.slug', 'separate-sciences');
      if (hasBespoke) {
        sepQuery = sepQuery.eq('subjects.school_id', SchoolSession.getSchoolId());
      } else {
        sepQuery = sepQuery.is('subjects.school_id', null);
      }
      unitResult = await sepQuery.maybeSingle();
    }

    if (!unitResult.data) {
      showError('Unit not found', 'No unit found.');
      return;
    }

    var unit = unitResult.data;
    var subject = unit.subjects;

    var lessonsResult = await sb
      .from('lessons')
      .select('id, lesson_number, slug, title, description, status, tier')
      .eq('unit_id', unit.id)
      .eq('status', 'live')
      .order('lesson_number');

    var lessons = lessonsResult.data || [];

    // Filter by tier if student has a Foundation preference for this subject.
    // Tier picker writes under base slug; fall back if board-specific slug
    // has no explicit value.
    var savedTiers = {};
    try { savedTiers = JSON.parse(localStorage.getItem('studyvault-tiers') || '{}'); } catch(e) {}
    var subjectTier = savedTiers[subjectSlug];
    if (!subjectTier) {
      var subjectBase = subjectSlug.replace(/-(?:aqa|edexcel|ocr-b|ocr|eduqas)$/, '');
      subjectTier = savedTiers[subjectBase];
    }
    subjectTier = subjectTier || 'higher';
    if (subjectTier === 'foundation') {
      lessons = lessons.filter(function(l) { return l.tier !== 'higher'; });
    }

    // Free user Film Studies: trim set-film lessons within this unit to only
    // the student's picked film (if any of the 5 picks falls in this unit).
    // Overviews, comparative-method, specialist-writing etc. keep showing.
    // Selectable lesson set lives in FreeUserFilters.FILM_SELECTABLE.
    if (typeof window.FreeUserFilters !== 'undefined') {
      var pickedFilmListUnit = window.FreeUserFilters.getPickedFilmSlugs(subjectSlug);
      if (pickedFilmListUnit) {
        var pickedFilmSetUnit = new Set(pickedFilmListUnit);
        var FILM_SELECTABLE_MAP_UNIT = window.FreeUserFilters.FILM_SELECTABLE;
        lessons = lessons.filter(function (l) {
          if (FILM_SELECTABLE_MAP_UNIT[l.slug]) return pickedFilmSetUnit.has(l.slug);
          return true;
        });
      }
    }

    // Free user Geography: trim optional-topic lessons within this paper to
    // only the student's picks (ecosystem, two landscapes, one resource).
    // Compulsory lessons keep showing. Keyed 'unit_slug/lesson_slug'.
    if (typeof window.FreeUserFilters !== 'undefined') {
      var pickedGeoListUnit = window.FreeUserFilters.getPickedGeoSlugs(subjectSlug);
      if (pickedGeoListUnit) {
        var pickedGeoSetUnit = new Set(pickedGeoListUnit);
        var GEO_SELECTABLE_MAP_UNIT = window.FreeUserFilters.GEO_SELECTABLE;
        lessons = lessons.filter(function (l) {
          var key = unit.slug + '/' + l.slug;
          if (GEO_SELECTABLE_MAP_UNIT[key]) return pickedGeoSetUnit.has(key);
          return true;
        });
      }
    }

    document.title = unit.name + ' - StudyVault';
    if (unit.body_class) document.body.classList.add(unit.body_class);
    if (unit.accent) document.documentElement.style.setProperty('--accent', unit.accent);
    if (unit.accent_light) document.documentElement.style.setProperty('--accent-light', unit.accent_light);
    if (unit.accent_badge) document.documentElement.style.setProperty('--accent-badge', unit.accent_badge);
    document.body.dataset.unit = unit.slug;
    document.getElementById('header-unit-label').textContent = unit.name;

    // Nav links
    var nav = document.getElementById('header-nav');
    var isPracticeUnit = (subject.settings && subject.settings.format === 'practice') ||
      (subject.settings && subject.settings.practice_units && subject.settings.practice_units.indexOf(unitSlug) !== -1);
    var unitHasExamGuides = !!(subject.settings && subject.settings.has_exam_guides);
    var unitNavHtml = '<a href="/">Home</a>' +
      '<a href="/browse/' + subjectSlug + '">Subject Home</a>';
    if (!isPracticeUnit) {
      if (unitHasExamGuides) {
        unitNavHtml += '<a href="/guide/' + subjectSlug + '/exam-technique">Exam Technique</a>';
      }
      unitNavHtml += '<a href="/guide/' + subjectSlug + '/revision-technique">Revision Techniques</a>';
    }
    nav.innerHTML = unitNavHtml;

    var html = '';

    // Unit page header — coloured strip with title and description
    html += '<div class="unit-page-header">';
    html += '<div class="unit-page-header-inner">';
    html += '<h1>' + esc(unit.name) + '</h1>';
    if (unit.subtitle) {
      html += '<p>' + esc(unit.subtitle) + '</p>';
    }
    // Tier indicator for tiered subjects
    var TIERED = ['maths', 'maths-edexcel', 'maths-aqa', 'maths-ocr', 'maths-eduqas', 'science', 'science-aqa', 'science-edexcel', 'science-ocr', 'science-ocr-b', 'separate-sciences', 'separate-sciences-edexcel', 'separate-sciences-ocr', 'separate-sciences-ocr-b', 'statistics', 'statistics-aqa'];
    if (TIERED.indexOf(subjectSlug) !== -1) {
      var tierLabel = subjectTier === 'foundation' ? 'Foundation' : 'Higher';
      html += '<div class="unit-tier-badge" style="margin-top:0.5rem">';
      html += '<span style="font-family:Inter,sans-serif;font-size:0.75rem;font-weight:600;color:#fff;background:rgba(0,0,0,0.25);padding:0.25rem 0.75rem;border-radius:6px;display:inline-block">';
      html += tierLabel + ' tier</span></div>';
    }
    html += '</div></div>';

    // Progress bar — use filtered count so Foundation students see correct total
    var displayCount = lessons.length;
    html += '<div class="unit-progress">';
    html += '<div class="unit-progress-label">0 of ' + displayCount + ' lessons visited</div>';
    html += '<div class="progress-bar-track"><div class="progress-bar-fill"></div></div>';
    html += '</div>';

    // Lesson grid
    html += '<div class="lesson-grid sv-stagger">';

    var isPractice = (subject.settings && subject.settings.format === 'practice') ||
      (subject.settings && subject.settings.practice_units && subject.settings.practice_units.indexOf(unitSlug) !== -1);
    var lessonPrefix = isPractice ? '/practice/' : '/lesson/';

    lessons.forEach(function (lesson, idx) {
      var url = lessonPrefix + subjectSlug + '/' + unitSlug + '/' + lesson.lesson_number;
      html += '<a href="' + url + '" class="lesson-card sv-reveal" data-lesson="' + esc(lesson.slug) + '">';
      html += '<span class="lesson-card-number">Lesson ' + (idx + 1) + '</span>';
      html += '<h3>' + esc(lesson.title) + '</h3>';
      if (lesson.description) {
        html += '<p>' + esc(lesson.description) + '</p>';
      }
      html += '</a>';
    });

    html += '</div>';

    // Back link — wrapped in container to match static page padding
    html += '<div style="max-width: var(--page-max); margin: 0 auto; padding: 0 1.5rem 3rem;">';
    html += '<a href="/browse/' + subjectSlug + '" class="back-link">&larr; Back to ' + esc(subject.name) + '</a>';
    html += '</div>';

    loadingEl.style.display = 'none';
    contentEl.innerHTML = html;
    contentEl.style.display = '';

    // Add nav icons, update visited cards, trigger reveal animations
    if (typeof initNavIcons === 'function') initNavIcons();
    if (typeof updateVisitedCards === 'function') updateVisitedCards();
    if (typeof initRevealAnimations === 'function') initRevealAnimations();
  }

  // ---- Main ----
  async function init() {
    var params = parseUrl();
    if (!params) {
      showError('Invalid URL', 'Browse URL format: /browse/{subject} or /browse/{subject}/{unit}');
      return;
    }
    if (maybeRedirectOldHistorySlug(params.subjectSlug)) return;

    try {
      if (params.unitSlug) {
        await renderUnitIndex(params.subjectSlug, params.unitSlug);
      } else {
        await renderSubjectLanding(params.subjectSlug);
      }
    } catch (err) {
      console.error('Browse loader error:', err);
      showError('Something went wrong', 'Could not load the page. Please try again.');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
