/* StudyVault — Highlight Mode
 *
 * Simple text highlighter for lessons. Students enter Highlight Mode from
 * the lesson checklist; in mode, drag-select to highlight in the current
 * colour, then add an optional note. Four colours, no categorisation.
 * Highlights survive across visits via localStorage. They can be reviewed
 * on /highlights.html and printed via /knowledge-organiser.html.
 *
 * Activation: gated behind ?highlights=1 in the URL (or localStorage flag
 * sv-hl-enabled=1, set automatically the first time the user arrives with
 * the query string, or implicitly when entering Highlight Mode).
 *
 * Public entry points:
 *   window.initHighlightAnnotate() — wire up the feature on a lesson page.
 *   window.svEnterHighlightMode() — called by the lesson-checklist click.
 *   window.svExitHighlightMode()
 *   window.svIsHighlightModeActive()
 *   window.svLessonHasHighlights() — used by the checklist's auto-tick.
 */
(function () {
  'use strict';

  // ---------- feature gating ----------
  function isEnabled() {
    try {
      var url = new URL(window.location.href);
      if (url.searchParams.get('highlights') === '1') {
        try { localStorage.setItem('sv-hl-enabled', '1'); } catch (e) {}
        return true;
      }
      if (url.searchParams.get('highlights') === '0') {
        try { localStorage.removeItem('sv-hl-enabled'); } catch (e) {}
        return false;
      }
      return localStorage.getItem('sv-hl-enabled') === '1';
    } catch (e) {
      return false;
    }
  }

  // ---------- constants ----------
  var COLORS = [
    { id: 'yellow', bg: '#fef08a', mark: '#fef9c3', label: 'Yellow' },
    { id: 'green',  bg: '#86efac', mark: '#dcfce7', label: 'Green' },
    { id: 'pink',   bg: '#f9a8d4', mark: '#fce7f3', label: 'Pink' },
    { id: 'blue',   bg: '#93c5fd', mark: '#dbeafe', label: 'Blue' }
  ];
  var DEFAULT_COLOR = 'yellow';
  var CONTEXT_LEN = 30;
  var STORAGE_PREFIX = 'sv-hl:';
  var INDEX_KEY = 'sv-hl-index';
  var HL_MODE_KEY = 'sv-hl-mode';
  var LAST_COLOR_KEY = 'sv-hl-last-color';

  function colorFor(id) {
    for (var i = 0; i < COLORS.length; i++) if (COLORS[i].id === id) return COLORS[i];
    return COLORS[0];
  }

  function getLastColor() {
    try {
      var c = localStorage.getItem(LAST_COLOR_KEY);
      if (c && colorFor(c).id === c) return c;
    } catch (e) {}
    return DEFAULT_COLOR;
  }
  function setLastColor(c) {
    try { localStorage.setItem(LAST_COLOR_KEY, c); } catch (e) {}
  }

  // ---------- storage ----------
  function lessonKey(lessonId) { return STORAGE_PREFIX + lessonId; }

  function getHighlights(lessonId) {
    try {
      var raw = localStorage.getItem(lessonKey(lessonId));
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function saveHighlights(lessonId, list) {
    try {
      if (list && list.length) {
        localStorage.setItem(lessonKey(lessonId), JSON.stringify(list));
      } else {
        localStorage.removeItem(lessonKey(lessonId));
      }
      updateIndex(lessonId, list ? list.length : 0);
    } catch (e) {
      console.warn('[highlights] save failed', e);
    }
    if (typeof notifyHighlightsChanged === 'function') notifyHighlightsChanged();
  }

  function readIndex() {
    try {
      var raw = localStorage.getItem(INDEX_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function updateIndex(lessonId, count) {
    var idx = readIndex();
    var existing = -1;
    for (var i = 0; i < idx.length; i++) {
      if (idx[i].lesson_id === lessonId) { existing = i; break; }
    }
    if (count === 0) {
      if (existing >= 0) idx.splice(existing, 1);
    } else {
      var entry = {
        lesson_id: lessonId,
        lesson_title: document.getElementById('lesson-title')
          ? (document.getElementById('lesson-title').textContent || '').trim()
          : '',
        subject_name: window._subjectName || '',
        subject_slug: window._subjectSlug || '',
        unit_name: window._unitName || '',
        unit_slug: window._unitSlug || '',
        lesson_url: window.location.pathname,
        count: count,
        last_updated: new Date().toISOString()
      };
      if (existing >= 0) idx[existing] = entry;
      else idx.push(entry);
    }
    try { localStorage.setItem(INDEX_KEY, JSON.stringify(idx)); } catch (e) {}
  }

  // ---------- text normalization & anchoring ----------
  // Glossary popups (.term-popup) are children of .term elements and contain
  // the definition text. They're invisible (opacity:0) but live in the DOM,
  // so range.toString() and container.textContent both include them. Exclude
  // them everywhere or selections leak the definition into the highlight.
  var EXCLUDED_FROM_HIGHLIGHT = '.term-popup';

  function normalize(s) {
    return (s || '').replace(/\s+/g, ' ').trim();
  }

  function isExcludedTextNode(node) {
    return !!(node.parentElement && node.parentElement.closest(EXCLUDED_FROM_HIGHLIGHT));
  }

  function cleanTextContent(container) {
    if (!container) return '';
    var parts = [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) parts.push(n.nodeValue);
    return parts.join('');
  }

  function cleanRangeText(range) {
    if (!range || range.collapsed) return '';
    var container = document.getElementById('study-notes');
    if (!container) return range.toString();
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    var parts = [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!range.intersectsNode(n)) return NodeFilter.FILTER_REJECT;
        if (isExcludedTextNode(n)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) {
      var text = n.nodeValue;
      var s = (n === startNode) ? range.startOffset : 0;
      var e = (n === endNode) ? range.endOffset : text.length;
      if (e > s) parts.push(text.substring(s, e));
    }
    return parts.join('');
  }

  function buildAnchor(range) {
    var container = document.getElementById('study-notes');
    if (!container || !container.contains(range.commonAncestorContainer)) return null;
    var fullText = cleanTextContent(container);
    var selected = cleanRangeText(range);
    var offset = textOffsetOfRangeStart(container, range);
    if (offset < 0) return null;
    var prefix = fullText.substring(Math.max(0, offset - CONTEXT_LEN), offset);
    var suffix = fullText.substring(offset + selected.length, offset + selected.length + CONTEXT_LEN);
    return {
      text: normalize(selected),
      prefix: normalize(prefix),
      suffix: normalize(suffix)
    };
  }

  function textOffsetOfRangeStart(container, range) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var total = 0;
    var n;
    while ((n = walker.nextNode())) {
      if (n === range.startContainer) return total + range.startOffset;
      total += n.nodeValue.length;
    }
    var snippet = cleanRangeText(range);
    var idx = cleanTextContent(container).indexOf(snippet);
    return idx;
  }

  function findRangeForAnchor(anchor) {
    var container = document.getElementById('study-notes');
    if (!container) return null;
    var normalizedFull = cleanTextContent(container);
    var needle = anchor.text;
    if (!needle) return null;
    var candidates = [];
    var from = 0;
    while (true) {
      var idx = normalizedFull.indexOf(needle, from);
      if (idx < 0) break;
      candidates.push(idx);
      from = idx + 1;
    }
    if (!candidates.length) {
      var collapsed = normalize(normalizedFull);
      var pos = collapsed.indexOf(needle);
      if (pos < 0) return null;
      return rangeFromCollapsedOffset(container, pos, needle.length);
    }
    var best = candidates[0];
    var bestScore = -1;
    for (var i = 0; i < candidates.length; i++) {
      var o = candidates[i];
      var pre = normalize(normalizedFull.substring(Math.max(0, o - CONTEXT_LEN), o));
      var suf = normalize(normalizedFull.substring(o + needle.length, o + needle.length + CONTEXT_LEN));
      var score = 0;
      if (anchor.prefix && pre.indexOf(anchor.prefix.substr(-15)) >= 0) score += 2;
      if (anchor.suffix && suf.indexOf(anchor.suffix.substr(0, 15)) >= 0) score += 2;
      if (score > bestScore) { bestScore = score; best = o; }
    }
    return rangeFromOffset(container, best, needle.length);
  }

  function rangeFromOffset(container, charOffset, length) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var consumed = 0;
    var startNode = null, startNodeOffset = 0;
    var endNode = null, endNodeOffset = 0;
    var n;
    while ((n = walker.nextNode())) {
      var len = n.nodeValue.length;
      if (!startNode && consumed + len > charOffset) {
        startNode = n;
        startNodeOffset = charOffset - consumed;
      }
      if (consumed + len >= charOffset + length) {
        endNode = n;
        endNodeOffset = (charOffset + length) - consumed;
        break;
      }
      consumed += len;
    }
    if (!startNode || !endNode) return null;
    var range = document.createRange();
    range.setStart(startNode, startNodeOffset);
    range.setEnd(endNode, endNodeOffset);
    return range;
  }

  function rangeFromCollapsedOffset(container, collapsedOffset, length) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return isExcludedTextNode(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var collapsed = 0;
    var startNode = null, startNodeOffset = 0;
    var endNode = null, endNodeOffset = 0;
    var n;
    while ((n = walker.nextNode())) {
      var text = n.nodeValue;
      for (var i = 0; i < text.length; i++) {
        var ch = text[i];
        var isWs = /\s/.test(ch);
        var advance = isWs ? (i === 0 || /\s/.test(text[i - 1]) ? 0 : 1) : 1;
        if (!startNode && collapsed >= collapsedOffset) {
          startNode = n;
          startNodeOffset = i;
        }
        if (startNode && collapsed >= collapsedOffset + length) {
          endNode = n;
          endNodeOffset = i;
          break;
        }
        collapsed += advance;
      }
      if (endNode) break;
    }
    if (!startNode || !endNode) return null;
    var range = document.createRange();
    range.setStart(startNode, startNodeOffset);
    range.setEnd(endNode, endNodeOffset);
    return range;
  }

  // ---------- mark wrapping ----------
  function wrapRangeInMarks(range, hl) {
    if (!range || range.collapsed) return [];
    var marks = [];
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    var startOff = range.startOffset;
    var endOff = range.endOffset;
    var nodes = [];
    var container = document.getElementById('study-notes');
    if (!container) return [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!range.intersectsNode(node)) return NodeFilter.FILTER_REJECT;
        if (isExcludedTextNode(node)) return NodeFilter.FILTER_REJECT;
        var p = node.parentNode;
        while (p && p !== container) {
          if (p.classList && p.classList.contains('sv-hl')) return NodeFilter.FILTER_REJECT;
          p = p.parentNode;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) nodes.push(n);
    if (!nodes.length) return [];

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var text = node.nodeValue;
      var s = (node === startNode) ? startOff : 0;
      var e = (node === endNode) ? endOff : text.length;
      if (e <= s) continue;
      var middle = node.splitText(s);
      if (e - s < middle.nodeValue.length) middle.splitText(e - s);
      var mark = document.createElement('mark');
      var col = hl.color || DEFAULT_COLOR;
      mark.className = 'sv-hl sv-hl--' + col;
      mark.setAttribute('data-hl-id', hl.id);
      mark.setAttribute('data-hl-color', col);
      if (hl.note) mark.setAttribute('data-hl-has-note', '1');
      middle.parentNode.insertBefore(mark, middle);
      mark.appendChild(middle);
      marks.push(mark);
    }
    return marks;
  }

  function unwrapMark(mark) {
    var parent = mark.parentNode;
    while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
    parent.removeChild(mark);
    if (parent.normalize) parent.normalize();
  }

  function unwrapHighlightById(hlId) {
    var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(hlId) + '"]');
    marks.forEach(unwrapMark);
  }

  function cssEscape(s) {
    return String(s).replace(/["\\]/g, '\\$&');
  }

  // ---------- popover ----------
  // Single popover: four colour swatches at top, note textarea, save / delete.
  // Shown after a fresh selection in Highlight Mode (highlight already created
  // in last-color) or when an existing mark is clicked (in or out of mode).
  var popoverEl = null;
  var activeHighlight = null;
  var pendingRange = null;
  var pendingAnchor = null;

  function buildPopover() {
    if (popoverEl) return popoverEl;
    popoverEl = document.createElement('div');
    popoverEl.className = 'sv-hl-popover';
    popoverEl.setAttribute('role', 'dialog');
    popoverEl.setAttribute('aria-label', 'Highlight options');
    popoverEl.innerHTML =
      '<div class="sv-hl-popover-swatches">' +
        COLORS.map(function (c) {
          return '<button class="sv-hl-swatch sv-hl-swatch--' + c.id + '" type="button" data-color="' + c.id + '" aria-label="' + c.label + '" title="' + c.label + '"></button>';
        }).join('') +
      '</div>' +
      '<textarea class="sv-hl-note" rows="3" maxlength="1000" placeholder="Add a note (optional)…"></textarea>' +
      '<div class="sv-hl-note-actions">' +
        '<button class="sv-hl-icon-btn sv-hl-delete" type="button" title="Delete highlight" hidden>' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>' +
        '</button>' +
        '<button class="sv-hl-btn sv-hl-done sv-hl-btn--primary" type="button">Done</button>' +
      '</div>';
    document.body.appendChild(popoverEl);

    popoverEl.querySelectorAll('.sv-hl-swatch').forEach(function (sw) {
      sw.addEventListener('click', function () {
        var color = sw.getAttribute('data-color');
        applyOrUpdateColor(color);
        // Reflect selection state in swatches
        popoverEl.querySelectorAll('.sv-hl-swatch').forEach(function (s) {
          s.setAttribute('aria-pressed', s === sw ? 'true' : 'false');
        });
      });
    });
    popoverEl.querySelector('.sv-hl-done').addEventListener('click', commitAndHide);
    popoverEl.querySelector('.sv-hl-delete').addEventListener('click', function () {
      if (activeHighlight) deleteHighlight(activeHighlight.id);
      hidePopover();
    });
    return popoverEl;
  }

  function showPopoverAt(rect, opts) {
    buildPopover();
    var deleteBtn = popoverEl.querySelector('.sv-hl-delete');
    deleteBtn.hidden = !opts.canDelete;
    var noteEl = popoverEl.querySelector('.sv-hl-note');
    noteEl.value = opts.note || '';
    var activeColor = opts.color || '';
    popoverEl.querySelectorAll('.sv-hl-swatch').forEach(function (s) {
      s.setAttribute('aria-pressed', s.getAttribute('data-color') === activeColor ? 'true' : 'false');
    });
    popoverEl.style.visibility = 'hidden';
    popoverEl.style.display = 'block';
    var ph = popoverEl.offsetHeight;
    var pw = popoverEl.offsetWidth;
    var spaceAbove = rect.top;
    var top = (spaceAbove > ph + 12) ? window.scrollY + rect.top - ph - 8 : window.scrollY + rect.bottom + 8;
    var left = window.scrollX + rect.left + (rect.width / 2) - (pw / 2);
    var maxLeft = window.scrollX + document.documentElement.clientWidth - pw - 12;
    var minLeft = window.scrollX + 12;
    if (left > maxLeft) left = maxLeft;
    if (left < minLeft) left = minLeft;
    popoverEl.style.top = top + 'px';
    popoverEl.style.left = left + 'px';
    popoverEl.style.visibility = 'visible';
    setTimeout(function () { noteEl.focus(); }, 0);
  }

  function hidePopover() {
    if (popoverEl) popoverEl.style.display = 'none';
    activeHighlight = null;
    pendingRange = null;
    pendingAnchor = null;
  }

  // Save whatever's typed in the note textarea (if a highlight is active)
  // and close. Used by Done, click-outside, and Escape — all paths through
  // a single behaviour so students don't lose typed notes.
  function commitAndHide() {
    if (popoverEl && activeHighlight) {
      var note = popoverEl.querySelector('.sv-hl-note').value;
      saveNote(note);
    }
    hidePopover();
  }

  // ---------- create / update / delete ----------
  function applyOrUpdateColor(color) {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    if (activeHighlight) {
      var list = getHighlights(lessonId);
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === activeHighlight.id) {
          list[i].color = color;
          list[i].updatedAt = new Date().toISOString();
          activeHighlight = list[i];
          break;
        }
      }
      saveHighlights(lessonId, list);
      var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(activeHighlight.id) + '"]');
      marks.forEach(function (m) {
        COLORS.forEach(function (c) { m.classList.remove('sv-hl--' + c.id); });
        m.classList.add('sv-hl--' + color);
        m.setAttribute('data-hl-color', color);
      });
    } else if (pendingRange && pendingAnchor) {
      var hl = {
        id: 'hl-' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36),
        text: pendingAnchor.text,
        prefix: pendingAnchor.prefix,
        suffix: pendingAnchor.suffix,
        color: color,
        note: '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      var marks2 = wrapRangeInMarks(pendingRange, hl);
      if (!marks2.length) { hidePopover(); return; }
      var list2 = getHighlights(lessonId);
      list2.push(hl);
      saveHighlights(lessonId, list2);
      activeHighlight = hl;
      pendingRange = null;
      pendingAnchor = null;
      window.getSelection().removeAllRanges();
    }
    setLastColor(color);
    applyModeBodyClasses(color);
    refreshFab();
  }

  function saveNote(note) {
    if (!activeHighlight) return;
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId);
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === activeHighlight.id) {
        list[i].note = (note || '').trim();
        list[i].updatedAt = new Date().toISOString();
        activeHighlight = list[i];
        break;
      }
    }
    saveHighlights(lessonId, list);
    var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(activeHighlight.id) + '"]');
    marks.forEach(function (m) {
      if (note && note.trim()) m.setAttribute('data-hl-has-note', '1');
      else m.removeAttribute('data-hl-has-note');
    });
    refreshFab();
  }

  function deleteHighlight(hlId) {
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId).filter(function (h) { return h.id !== hlId; });
    saveHighlights(lessonId, list);
    unwrapHighlightById(hlId);
    refreshFab();
  }

  // ---------- highlight mode ----------
  // Single body class drives cursor + ::selection colour. Tracks last-used
  // colour so the highlighter "feels loaded" with whatever the student
  // picked most recently.
  function isHighlightModeActive() {
    try { return localStorage.getItem(HL_MODE_KEY) === '1'; } catch (e) { return false; }
  }

  function applyModeBodyClasses(color) {
    var b = document.body;
    b.classList.toggle('sv-hl-mode', isHighlightModeActive());
    COLORS.forEach(function (c) { b.classList.remove('sv-hl-color-' + c.id); });
    if (isHighlightModeActive()) {
      b.classList.add('sv-hl-color-' + (color || getLastColor()));
    }
  }

  function enterHighlightMode() {
    try { localStorage.setItem(HL_MODE_KEY, '1'); } catch (e) {}
    try { localStorage.setItem('sv-hl-enabled', '1'); } catch (e) {}
    if (!bootstrapped) bootstrap();
    applyModeBodyClasses(getLastColor());
    refreshFab();
  }

  function exitHighlightMode() {
    try { localStorage.removeItem(HL_MODE_KEY); } catch (e) {}
    document.body.classList.remove('sv-hl-mode');
    COLORS.forEach(function (c) { document.body.classList.remove('sv-hl-color-' + c.id); });
    refreshFab();
  }

  function lessonHasHighlights(lessonId) {
    lessonId = lessonId || window._lessonId;
    if (!lessonId) return false;
    return getHighlights(lessonId).length > 0;
  }

  // ---------- selection handling ----------
  var justDragged = false;
  var mouseDownX = 0;
  var mouseDownY = 0;
  function onMouseDownTracker(evt) {
    mouseDownX = evt.clientX;
    mouseDownY = evt.clientY;
    justDragged = false;
  }
  function onMouseMoveTracker(evt) {
    if (Math.abs(evt.clientX - mouseDownX) > 3 || Math.abs(evt.clientY - mouseDownY) > 3) {
      justDragged = true;
    }
  }

  function onMouseUp(evt) {
    if (evt.target.closest && evt.target.closest('.sv-hl-popover')) return;
    // Out of mode: don't create new highlights. Existing-mark click is
    // handled separately by onMarkClick.
    if (!isHighlightModeActive()) return;
    setTimeout(function () {
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) return;
      var range = sel.getRangeAt(0);
      var container = document.getElementById('study-notes');
      if (!container || !container.contains(range.commonAncestorContainer)) return;
      var text = range.toString();
      if (!text || !text.trim()) return;
      if (text.length > 5000) return;  // generous cap; Ctrl+A guard
      var anchor = buildAnchor(range);
      if (!anchor) return;
      pendingRange = range.cloneRange();
      pendingAnchor = anchor;
      activeHighlight = null;
      var color = getLastColor();
      var rect = range.getBoundingClientRect();
      applyOrUpdateColor(color);  // creates the highlight in last-used colour
      showPopoverAt(rect, { canDelete: true, note: '', color: color });
    }, 10);
  }

  function onMarkClick(evt) {
    var mark = evt.target.closest('mark.sv-hl');
    if (mark) {
      evt.preventDefault();
      evt.stopPropagation();
      var hlId = mark.getAttribute('data-hl-id');
      var lessonId = window._lessonId;
      var list = getHighlights(lessonId);
      var hl = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === hlId) { hl = list[i]; break; }
      }
      if (!hl) return;
      activeHighlight = hl;
      pendingRange = null;
      pendingAnchor = null;
      showPopoverAt(mark.getBoundingClientRect(), {
        canDelete: true,
        note: hl.note || '',
        color: hl.color || DEFAULT_COLOR
      });
      return;
    }
    // Suppress the click that follows a drag-select inside the article — stops
    // the narration jump-to-clip handler from firing when the student is
    // highlighting in mode.
    if (justDragged && isHighlightModeActive()) {
      var sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.toString().trim().length > 0) {
        evt.stopPropagation();
      }
      justDragged = false;
    }
  }

  function onDocClick(evt) {
    if (!popoverEl || popoverEl.style.display === 'none') return;
    if (popoverEl.contains(evt.target)) return;
    if (evt.target.closest && evt.target.closest('mark.sv-hl')) return;
    commitAndHide();
  }

  function onKeyDown(evt) {
    if (evt.key === 'Escape') commitAndHide();
  }

  // ---------- rehydrate marks on load ----------
  function rehydrate() {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    var list = getHighlights(lessonId);
    for (var i = 0; i < list.length; i++) {
      var hl = list[i];
      try {
        var range = findRangeForAnchor(hl);
        if (range) wrapRangeInMarks(range, hl);
      } catch (e) {
        console.warn('[highlights] could not rehydrate', hl.id, e);
      }
    }
  }

  // ---------- FAB (bottom-left) ----------
  // Out of mode: [Highlight mode]                    — single button, enters mode
  // In mode:    [Lesson Highlights (N)] [Exit Mode]  — two equal buttons side-by-side
  var fabStackEl = null;
  var fabEnterEl = null;
  var fabLessonEl = null;
  var fabExitEl = null;
  var modalEl = null;

  function refreshFab() {
    if (!fabStackEl) return;
    var inMode = isHighlightModeActive();
    var n = getHighlights(window._lessonId).length;
    fabStackEl.classList.toggle('sv-hl-fab-stack--in-mode', inMode);
    fabEnterEl.style.display = inMode ? 'none' : 'inline-flex';
    fabLessonEl.style.display = inMode ? 'inline-flex' : 'none';
    fabExitEl.style.display = inMode ? 'inline-flex' : 'none';
    fabLessonEl.querySelector('.sv-hl-fab-count').textContent = n;
    fabLessonEl.classList.toggle('sv-hl-fab--empty', n === 0);
  }

  function buildFab() {
    if (fabStackEl) return fabStackEl;
    fabStackEl = document.createElement('div');
    fabStackEl.className = 'sv-hl-fab-stack';

    // Out-of-mode: single "Highlight mode" toggle
    fabEnterEl = document.createElement('button');
    fabEnterEl.className = 'sv-hl-fab sv-hl-fab--enter';
    fabEnterEl.type = 'button';
    fabEnterEl.setAttribute('aria-label', 'Enter highlight mode');
    fabEnterEl.innerHTML =
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
      '<span class="sv-hl-fab-label">Highlight mode</span>';
    fabEnterEl.addEventListener('click', enterHighlightMode);
    fabStackEl.appendChild(fabEnterEl);

    // In-mode: Lesson Highlights modal opener
    fabLessonEl = document.createElement('button');
    fabLessonEl.className = 'sv-hl-fab sv-hl-fab--lesson';
    fabLessonEl.type = 'button';
    fabLessonEl.setAttribute('aria-label', 'Lesson highlights');
    fabLessonEl.style.display = 'none';
    fabLessonEl.innerHTML =
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
      '<span class="sv-hl-fab-label">Lesson Highlights</span>' +
      '<span class="sv-hl-fab-count">0</span>';
    fabLessonEl.addEventListener('click', openModal);
    fabStackEl.appendChild(fabLessonEl);

    // In-mode: Exit button
    fabExitEl = document.createElement('button');
    fabExitEl.className = 'sv-hl-fab sv-hl-fab--exit';
    fabExitEl.type = 'button';
    fabExitEl.setAttribute('aria-label', 'Exit highlight mode');
    fabExitEl.style.display = 'none';
    fabExitEl.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
      '<span class="sv-hl-fab-label">Exit Highlight Mode</span>';
    fabExitEl.addEventListener('click', exitHighlightMode);
    fabStackEl.appendChild(fabExitEl);

    document.body.appendChild(fabStackEl);
    return fabStackEl;
  }

  // ---------- per-lesson modal ----------
  function openModal() {
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.className = 'sv-hl-modal';
      modalEl.innerHTML =
        '<div class="sv-hl-modal-backdrop"></div>' +
        '<div class="sv-hl-modal-panel" role="dialog" aria-modal="true" aria-label="My highlights">' +
          '<header class="sv-hl-modal-header">' +
            '<h2>My highlights</h2>' +
            '<button class="sv-hl-modal-allpages sv-hl-modal-print" type="button">Print these notes</button>' +
            '<button class="sv-hl-modal-close" aria-label="Close">×</button>' +
          '</header>' +
          '<div class="sv-hl-modal-body"></div>' +
        '</div>';
      document.body.appendChild(modalEl);
      modalEl.querySelector('.sv-hl-modal-backdrop').addEventListener('click', closeModal);
      modalEl.querySelector('.sv-hl-modal-close').addEventListener('click', closeModal);
      modalEl.querySelector('.sv-hl-modal-print').addEventListener('click', openPrintView);
    }
    renderModalBody();
    modalEl.classList.add('sv-hl-modal--open');
  }

  // Build a sv-ko-data payload from THIS lesson's highlights and navigate
  // to the print page. Used from the lesson-highlights modal as the
  // "Print these notes" action.
  function openPrintView() {
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId);
    if (!list.length) return;
    var titleEl = document.getElementById('lesson-title');
    var lessonTitle = titleEl ? (titleEl.textContent || '').trim() : 'Lesson';
    var payload = {
      generated_at: new Date().toISOString(),
      source_url: window.location.pathname + window.location.search,
      subjects: [{
        name: window._subjectName || 'Subject',
        units: [{
          name: window._unitName || '',
          lessons: [{
            lesson_id: lessonId,
            lesson_title: lessonTitle,
            lesson_url: window.location.pathname,
            highlights: list
          }]
        }]
      }]
    };
    try {
      sessionStorage.setItem('sv-ko-data', JSON.stringify(payload));
      window.location.href = '/knowledge-organiser.html';
    } catch (e) {
      console.warn('[highlights] could not open print view', e);
    }
  }

  function closeModal() {
    if (modalEl) modalEl.classList.remove('sv-hl-modal--open');
  }

  function renderModalBody() {
    var body = modalEl.querySelector('.sv-hl-modal-body');
    var list = getHighlights(window._lessonId);
    var printBtn = modalEl.querySelector('.sv-hl-modal-print');
    if (printBtn) printBtn.disabled = list.length === 0;
    if (!list.length) {
      body.innerHTML =
        '<div class="sv-hl-modal-empty">' +
          '<p>No highlights on this lesson yet.</p>' +
          '<p class="sv-hl-modal-hint">Enter Highlight Mode from the lesson checklist, then drag-select any text.</p>' +
        '</div>';
      return;
    }
    list.sort(function (a, b) { return (b.createdAt || '').localeCompare(a.createdAt || ''); });
    body.innerHTML = list.map(function (h) {
      var c = colorFor(h.color);
      var noteHtml = h.note ? '<p class="sv-hl-modal-note">' + escapeHtml(h.note) + '</p>' : '';
      return '<article class="sv-hl-modal-item" data-hl-id="' + escapeHtml(h.id) + '">' +
          '<div class="sv-hl-modal-snippet" style="background:' + c.mark + '">' +
            '<span class="sv-hl-modal-bar" style="background:' + c.bg + '"></span>' +
            '<span class="sv-hl-modal-text">' + escapeHtml(h.text) + '</span>' +
          '</div>' +
          noteHtml +
          '<div class="sv-hl-modal-actions">' +
            '<button class="sv-hl-modal-jump" type="button">Jump to</button>' +
            '<button class="sv-hl-modal-delete" type="button">Delete</button>' +
          '</div>' +
        '</article>';
    }).join('');
    body.querySelectorAll('.sv-hl-modal-item').forEach(function (item) {
      var hlId = item.getAttribute('data-hl-id');
      item.querySelector('.sv-hl-modal-jump').addEventListener('click', function () {
        var firstMark = document.querySelector('mark.sv-hl[data-hl-id="' + cssEscape(hlId) + '"]');
        if (firstMark) {
          closeModal();
          firstMark.scrollIntoView({ behavior: 'smooth', block: 'center' });
          firstMark.classList.add('sv-hl--flash');
          setTimeout(function () { firstMark.classList.remove('sv-hl--flash'); }, 1500);
        }
      });
      item.querySelector('.sv-hl-modal-delete').addEventListener('click', function () {
        deleteHighlight(hlId);
        renderModalBody();
      });
    });
  }

  function escapeHtml(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ---------- styles ----------
  function injectStyles() {
    if (document.getElementById('sv-hl-styles')) return;
    var s = document.createElement('style');
    s.id = 'sv-hl-styles';
    s.textContent =
      // Glossary popups never get selected (browser belt-and-braces; JS layer
      // also excludes them in case the browser ignores user-select).
      '.term-popup{user-select:none;-webkit-user-select:none}' +
      // Highlight marks
      'mark.sv-hl{padding:0.05em 0;border-radius:3px;cursor:pointer;transition:filter .15s ease;color:#2d2a26}' +
      'mark.sv-hl:hover{filter:brightness(.96)}' +
      'mark.sv-hl--yellow{background:#fef9c3}' +
      'mark.sv-hl--green{background:#dcfce7}' +
      'mark.sv-hl--pink{background:#fce7f3}' +
      'mark.sv-hl--blue{background:#dbeafe}' +
      'body.dark-mode mark.sv-hl{color:#f5f1ec}' +
      'body.dark-mode mark.sv-hl--yellow{background:rgba(234,179,8,.55)}' +
      'body.dark-mode mark.sv-hl--green{background:rgba(34,197,94,.45)}' +
      'body.dark-mode mark.sv-hl--pink{background:rgba(236,72,153,.45)}' +
      'body.dark-mode mark.sv-hl--blue{background:rgba(59,130,246,.5)}' +
      'mark.sv-hl[data-hl-has-note]::after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;vertical-align:super;margin-left:2px;opacity:.5}' +
      'mark.sv-hl--flash{animation:sv-hl-flash 1.4s ease}' +
      '@keyframes sv-hl-flash{0%,100%{box-shadow:0 0 0 0 rgba(45,42,38,0)}30%{box-shadow:0 0 0 6px rgba(45,42,38,.25)}}' +
      // Highlight Mode — give #study-notes a soft drop shadow so it lifts
      // off the page. Page background, header, gutter, sidebar all stay as
      // they were — only the article you're actually highlighting pops.
      'body.sv-hl-mode #study-notes{box-shadow:0 0 0 1px rgba(45,42,38,.05), 0 16px 44px -18px rgba(45,42,38,.22);border-radius:10px;transition:box-shadow .3s ease}' +
      'body.dark-mode.sv-hl-mode #study-notes{box-shadow:0 0 0 1px rgba(245,241,236,.08), 0 16px 44px -18px rgba(0,0,0,.6)}' +
      // Highlight Mode — cursor + live selection match the last-used colour
      // (so the highlighter feels "loaded"). One pair per colour.
      'body.sv-hl-mode.sv-hl-color-yellow #study-notes,body.sv-hl-mode.sv-hl-color-yellow #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%23fef08a" stroke="%23854d0e" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%23854d0e" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-mode.sv-hl-color-green #study-notes,body.sv-hl-mode.sv-hl-color-green #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%2386efac" stroke="%23166534" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%23166534" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-mode.sv-hl-color-pink #study-notes,body.sv-hl-mode.sv-hl-color-pink #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%23f9a8d4" stroke="%239d174d" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%239d174d" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-mode.sv-hl-color-blue #study-notes,body.sv-hl-mode.sv-hl-color-blue #study-notes *{cursor:url(\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28"><path d="M5 22h14v3H5z" fill="%232d2a26"/><path d="M5 22l1-7 6-12h0a3 3 0 0 1 5 0l1 7-6 12H5z" fill="%2393c5fd" stroke="%231e40af" stroke-width="1.2"/><path d="M11 4l5 3" stroke="%231e40af" stroke-width="1.2" fill="none"/></svg>\') 2 26, text}' +
      'body.sv-hl-mode #study-notes mark.sv-hl{cursor:pointer}' +
      'body.sv-hl-mode.sv-hl-color-yellow #study-notes ::selection{background:#fef9c3;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-yellow #study-notes ::-moz-selection{background:#fef9c3;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-green #study-notes ::selection{background:#dcfce7;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-green #study-notes ::-moz-selection{background:#dcfce7;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-pink #study-notes ::selection{background:#fce7f3;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-pink #study-notes ::-moz-selection{background:#fce7f3;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-blue #study-notes ::selection{background:#dbeafe;color:#2d2a26}' +
      'body.sv-hl-mode.sv-hl-color-blue #study-notes ::-moz-selection{background:#dbeafe;color:#2d2a26}' +
      // Popover
      '.sv-hl-popover{position:absolute;z-index:9000;background:#fff;border:1px solid rgba(45,42,38,.12);border-radius:14px;box-shadow:0 12px 30px rgba(20,18,15,.18);padding:10px;font-family:Inter,system-ui,sans-serif;color:#2d2a26;min-width:240px;max-width:300px;display:none}' +
      'body.dark-mode .sv-hl-popover{background:#3a3631;color:#f5f1ec;border-color:rgba(245,241,236,.12)}' +
      '.sv-hl-popover-swatches{display:flex;justify-content:center;gap:8px;margin-bottom:8px}' +
      '.sv-hl-swatch{width:28px;height:28px;border-radius:50%;border:2px solid rgba(45,42,38,.1);cursor:pointer;padding:0;transition:transform .12s ease,border-color .12s ease}' +
      '.sv-hl-swatch:hover{transform:scale(1.1);border-color:rgba(45,42,38,.4)}' +
      '.sv-hl-swatch[aria-pressed="true"]{border-color:#2d2a26;box-shadow:0 0 0 1px #2d2a26 inset}' +
      'body.dark-mode .sv-hl-swatch{border-color:rgba(245,241,236,.18)}' +
      'body.dark-mode .sv-hl-swatch[aria-pressed="true"]{border-color:#f5f1ec;box-shadow:0 0 0 1px #f5f1ec inset}' +
      '.sv-hl-swatch--yellow{background:#fef08a}' +
      '.sv-hl-swatch--green{background:#86efac}' +
      '.sv-hl-swatch--pink{background:#f9a8d4}' +
      '.sv-hl-swatch--blue{background:#93c5fd}' +
      '.sv-hl-note{width:100%;border:1px solid rgba(45,42,38,.15);border-radius:10px;padding:8px 10px;font-family:inherit;font-size:.92rem;color:inherit;resize:vertical;min-height:64px;background:#faf8f5;box-sizing:border-box}' +
      'body.dark-mode .sv-hl-note{background:#2a2826;border-color:rgba(245,241,236,.18)}' +
      '.sv-hl-note:focus{outline:none;border-color:#2d2a26}' +
      'body.dark-mode .sv-hl-note:focus{border-color:#f5f1ec}' +
      '.sv-hl-note-actions{display:flex;align-items:center;justify-content:flex-end;gap:6px;margin-top:8px}' +
      '.sv-hl-note-actions .sv-hl-icon-btn{margin-right:auto}' +
      '.sv-hl-icon-btn{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:transparent;border:none;border-radius:8px;color:#a14242;cursor:pointer}' +
      '.sv-hl-icon-btn:hover{background:rgba(161,66,66,.1)}' +
      '.sv-hl-btn{padding:6px 12px;border-radius:10px;border:1px solid rgba(45,42,38,.15);background:#fff;font-family:inherit;font-size:.86rem;color:#2d2a26;cursor:pointer}' +
      '.sv-hl-btn:hover{background:#faf8f5}' +
      '.sv-hl-btn--primary{background:#2d2a26;color:#faf8f5;border-color:#2d2a26}' +
      '.sv-hl-btn--primary:hover{background:#1f1c19}' +
      'body.dark-mode .sv-hl-btn{background:#2a2826;color:#f5f1ec;border-color:rgba(245,241,236,.18)}' +
      'body.dark-mode .sv-hl-btn:hover{background:#3a3631}' +
      'body.dark-mode .sv-hl-btn--primary{background:#f5f1ec;color:#2d2a26;border-color:#f5f1ec}' +
      'body.dark-mode .sv-hl-btn--primary:hover{background:#fff}' +
      // FAB — bottom-left. Single "Highlight mode" button out of mode;
      // pair of equal "Lesson Highlights" + "Exit Highlight Mode" in mode.
      // On wide viewports (≥1400px) the stack centres under the gutter
      // checklist column so it feels like one visual unit with the rail.
      '.sv-hl-fab-stack{position:fixed;left:18px;bottom:18px;z-index:8000;display:flex;flex-direction:column;gap:8px;align-items:flex-start}' +
      '@media (min-width:1400px){.sv-hl-fab-stack{left:calc((100vw - var(--page-max, 1160px)) / 4);transform:translateX(-50%);align-items:center}}' +
      '.sv-hl-fab{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;background:var(--accent,#2d2a26);color:#fff;border:none;cursor:pointer;text-decoration:none;box-shadow:0 10px 24px rgba(20,18,15,.18);font-family:Inter,system-ui,sans-serif;font-size:.9rem;font-weight:500;transition:filter .15s ease,transform .15s ease}' +
      '.sv-hl-fab:hover{filter:brightness(1.1);transform:translateY(-1px)}' +
      '.sv-hl-fab--exit{background:#2d2a26;color:#fff}' +
      '.sv-hl-fab--exit:hover{filter:brightness(1.15)}' +
      '.sv-hl-fab-count{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:rgba(255,255,255,.95);color:#2d2a26;font-size:.78rem;font-weight:600}' +
      '.sv-hl-fab--empty .sv-hl-fab-count{background:rgba(255,255,255,.22);color:#fff}' +
      '@media (max-width:640px){.sv-hl-fab-label{display:none}.sv-hl-fab{padding:10px}}' +
      // Modal
      '.sv-hl-modal{position:fixed;inset:0;z-index:9500;display:none;align-items:flex-end;justify-content:center}' +
      '.sv-hl-modal--open{display:flex}' +
      '.sv-hl-modal-backdrop{position:absolute;inset:0;background:rgba(20,18,15,.32);backdrop-filter:blur(2px)}' +
      '.sv-hl-modal-panel{position:relative;background:#faf8f5;width:min(640px,100%);max-height:80vh;border-radius:16px 16px 0 0;display:flex;flex-direction:column;box-shadow:0 -20px 48px rgba(20,18,15,.18);font-family:Inter,system-ui,sans-serif;color:#2d2a26}' +
      '@media (min-width:720px){.sv-hl-modal{align-items:center}.sv-hl-modal-panel{border-radius:16px}}' +
      '.sv-hl-modal-header{display:flex;align-items:center;gap:14px;padding:18px 22px;border-bottom:1px solid rgba(45,42,38,.08)}' +
      '.sv-hl-modal-header h2{margin:0;font-size:1.1rem;font-weight:600;flex:1}' +
      '.sv-hl-modal-allpages{font-size:.85rem;color:#2d2a26;background:#fef9c3;border:1px solid #fde047;padding:5px 12px;border-radius:8px;font-family:inherit;font-weight:600;cursor:pointer}' +
      '.sv-hl-modal-allpages:hover{background:#fef08a}' +
      '.sv-hl-modal-allpages:disabled{opacity:.4;cursor:not-allowed;background:#faf8f5;border-color:rgba(45,42,38,.12);color:#7a7367}' +
      'body.dark-mode .sv-hl-modal-allpages{background:rgba(234,179,8,.35);border-color:rgba(234,179,8,.6);color:#fef9c3}' +
      'body.dark-mode .sv-hl-modal-allpages:hover{background:rgba(234,179,8,.5)}' +
      '.sv-hl-modal-close{background:transparent;border:none;font-size:1.5rem;line-height:1;color:#5d564b;cursor:pointer;padding:4px 8px;border-radius:8px}' +
      '.sv-hl-modal-close:hover{background:rgba(45,42,38,.06);color:#2d2a26}' +
      '.sv-hl-modal-body{padding:14px 22px 22px;overflow-y:auto;display:flex;flex-direction:column;gap:14px}' +
      '.sv-hl-modal-empty{text-align:center;padding:32px 8px;color:#5d564b}' +
      '.sv-hl-modal-empty p{margin:0 0 6px}' +
      '.sv-hl-modal-hint{font-size:.88rem;color:#7a7367}' +
      '.sv-hl-modal-item{display:flex;flex-direction:column;gap:8px;padding:14px;background:#fff;border-radius:12px;border:1px solid rgba(45,42,38,.06)}' +
      '.sv-hl-modal-snippet{position:relative;padding:10px 12px 10px 16px;border-radius:10px;font-size:.95rem;line-height:1.5;color:#2d2a26}' +
      '.sv-hl-modal-bar{position:absolute;left:0;top:6px;bottom:6px;width:4px;border-radius:2px}' +
      '.sv-hl-modal-note{margin:0;padding:8px 12px;background:#faf8f5;border-radius:10px;font-size:.92rem;color:#3d3a35;border-left:3px solid rgba(45,42,38,.25)}' +
      '.sv-hl-modal-actions{display:flex;gap:8px;justify-content:flex-end}' +
      '.sv-hl-modal-jump,.sv-hl-modal-delete{padding:6px 12px;border-radius:8px;border:1px solid rgba(45,42,38,.15);background:#fff;font-family:inherit;font-size:.82rem;color:#2d2a26;cursor:pointer}' +
      '.sv-hl-modal-jump:hover{background:#faf8f5}' +
      '.sv-hl-modal-delete{color:#a14242;border-color:rgba(161,66,66,.25)}' +
      '.sv-hl-modal-delete:hover{background:#fbecec}';
    document.head.appendChild(s);
  }

  // ---------- entry point ----------
  function init() {
    if (!isEnabled()) return;
    if (!document.getElementById('study-notes')) return;
    if (!window._lessonId) {
      var tries = 0;
      var retry = setInterval(function () {
        tries++;
        if (window._lessonId) {
          clearInterval(retry);
          bootstrap();
        } else if (tries > 20) {
          clearInterval(retry);
        }
      }, 200);
      return;
    }
    bootstrap();
  }

  var bootstrapped = false;
  function bootstrap() {
    if (bootstrapped) { refreshFab(); return; }
    bootstrapped = true;
    injectStyles();
    buildFab();
    refreshFab();
    rehydrate();
    // Restore highlight mode if active when the student last navigated
    if (isHighlightModeActive()) {
      applyModeBodyClasses(getLastColor());
    }
    var container = document.getElementById('study-notes');
    container.addEventListener('mousedown', onMouseDownTracker, true);
    container.addEventListener('mousemove', onMouseMoveTracker);
    container.addEventListener('mouseup', onMouseUp);
    container.addEventListener('touchend', onMouseUp);
    container.addEventListener('click', onMarkClick, true);
    document.addEventListener('mousedown', onDocClick);
    document.addEventListener('keydown', onKeyDown);
    // If URL hash points at a specific highlight, scroll & flash it
    var hash = window.location.hash || '';
    if (hash.indexOf('#hl-') === 0) {
      var targetId = hash.slice(1);
      setTimeout(function () {
        var m = document.querySelector('mark.sv-hl[data-hl-id="' + cssEscape(targetId) + '"]');
        if (m) {
          m.scrollIntoView({ behavior: 'smooth', block: 'center' });
          m.classList.add('sv-hl--flash');
          setTimeout(function () { m.classList.remove('sv-hl--flash'); }, 1500);
        }
      }, 250);
    }
  }

  function notifyHighlightsChanged() {
    try {
      document.dispatchEvent(new CustomEvent('sv-hl-changed', {
        detail: { lessonId: window._lessonId, hasHighlights: lessonHasHighlights() }
      }));
    } catch (e) {}
  }

  window.initHighlightAnnotate = init;
  window.svEnterHighlightMode = enterHighlightMode;
  window.svExitHighlightMode = exitHighlightMode;
  window.svIsHighlightModeActive = isHighlightModeActive;
  window.svLessonHasHighlights = lessonHasHighlights;

  if (document.readyState !== 'loading') {
    setTimeout(init, 50);
  } else {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(init, 50); });
  }
})();
