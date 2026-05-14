/* StudyVault — Highlight & Annotate (prototype)
 *
 * Lets a student select text in #study-notes, choose a colour, add an optional note,
 * and revisit everything they've marked on a per-lesson modal or the cross-lesson
 * /highlights page. Storage is localStorage only; this is intentionally a prototype
 * that will be migrated server-side once student accounts ship.
 *
 * Activation: feature is gated behind ?highlights=1 in the URL (or
 * localStorage flag sv-hl-enabled=1, set automatically the first time the user
 * arrives with the query string). Once enabled, it stays enabled on this device.
 *
 * Public entry point: window.initHighlightAnnotate() — safe to call multiple times.
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
    { id: 'yellow', label: 'Yellow', bg: '#fef08a', mark: '#fef9c3' },
    { id: 'green',  label: 'Green',  bg: '#bbf7d0', mark: '#dcfce7' },
    { id: 'pink',   label: 'Pink',   bg: '#fbcfe8', mark: '#fce7f3' },
    { id: 'blue',   label: 'Blue',   bg: '#bfdbfe', mark: '#dbeafe' }
  ];
  var DEFAULT_COLOR = 'yellow';
  var CONTEXT_LEN = 30;
  var STORAGE_PREFIX = 'sv-hl:';
  var INDEX_KEY = 'sv-hl-index';

  function colorFor(id) {
    for (var i = 0; i < COLORS.length; i++) if (COLORS[i].id === id) return COLORS[i];
    return COLORS[0];
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
  function normalize(s) {
    return (s || '').replace(/\s+/g, ' ').trim();
  }

  function getContainerText() {
    var c = document.getElementById('study-notes');
    return c ? c.textContent : '';
  }

  // Build context anchor for a freshly-made selection
  function buildAnchor(range) {
    var container = document.getElementById('study-notes');
    if (!container || !container.contains(range.commonAncestorContainer)) return null;
    var fullText = container.textContent || '';
    var selected = range.toString();
    // Locate offset by walking text nodes and accumulating
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
    // Walk text nodes accumulating length until we reach the range's start node
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
    var total = 0;
    var n;
    while ((n = walker.nextNode())) {
      if (n === range.startContainer) return total + range.startOffset;
      total += n.nodeValue.length;
    }
    // Fallback: search by text content
    var snippet = range.toString();
    var idx = container.textContent.indexOf(snippet);
    return idx;
  }

  // Find a range in the live DOM matching a stored anchor
  function findRangeForAnchor(anchor) {
    var container = document.getElementById('study-notes');
    if (!container) return null;
    var normalizedFull = container.textContent;
    var needle = anchor.text;
    if (!needle) return null;
    // Find candidate occurrences and disambiguate by prefix/suffix when possible
    var candidates = [];
    var lower = normalizedFull;
    var from = 0;
    while (true) {
      var idx = lower.indexOf(needle, from);
      if (idx < 0) break;
      candidates.push(idx);
      from = idx + 1;
    }
    if (!candidates.length) {
      // Fallback: try whitespace-collapsed match
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

  // Build a Range from a character offset measured against textContent
  function rangeFromOffset(container, charOffset, length) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
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
    // Walk text nodes, tracking BOTH the raw offset and the collapsed offset, so
    // we can re-anchor when DOM whitespace has changed since the highlight was made.
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
    var raw = 0, collapsed = 0;
    var startNode = null, startNodeOffset = 0;
    var endNode = null, endNodeOffset = 0;
    var n;
    while ((n = walker.nextNode())) {
      var text = n.nodeValue;
      for (var i = 0; i < text.length; i++) {
        var ch = text[i];
        var isWs = /\s/.test(ch);
        // skip leading whitespace runs in collapsed form (approximation)
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
        raw++;
      }
      if (endNode) break;
    }
    if (!startNode || !endNode) return null;
    var range = document.createRange();
    range.setStart(startNode, startNodeOffset);
    range.setEnd(endNode, endNodeOffset);
    return range;
  }

  // ---------- mark wrapping (handles cross-element ranges) ----------
  function wrapRangeInMarks(range, hl) {
    if (!range || range.collapsed) return [];
    var marks = [];
    var startNode = range.startContainer;
    var endNode = range.endContainer;
    var startOff = range.startOffset;
    var endOff = range.endOffset;
    // Collect text nodes intersecting the range
    var nodes = [];
    var container = document.getElementById('study-notes');
    if (!container) return [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!range.intersectsNode(node)) return NodeFilter.FILTER_REJECT;
        // Don't re-wrap text already inside another sv-hl mark
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
      // Split out the highlighted segment
      var middle = node.splitText(s);
      // splitText returns the part AFTER s, so we then split at (e - s)
      if (e - s < middle.nodeValue.length) middle.splitText(e - s);
      var mark = document.createElement('mark');
      mark.className = 'sv-hl sv-hl--' + hl.color;
      mark.setAttribute('data-hl-id', hl.id);
      mark.setAttribute('data-hl-color', hl.color);
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

  // ---------- popover UI ----------
  var popoverEl = null;
  var activeHighlight = null; // when editing an existing one
  var pendingRange = null;    // when creating a new one
  var pendingAnchor = null;

  function buildPopover() {
    if (popoverEl) return popoverEl;
    popoverEl = document.createElement('div');
    popoverEl.className = 'sv-hl-popover';
    popoverEl.setAttribute('role', 'dialog');
    popoverEl.setAttribute('aria-label', 'Highlight options');
    popoverEl.innerHTML =
      '<div class="sv-hl-popover-row">' +
        COLORS.map(function (c) {
          return '<button class="sv-hl-swatch" data-color="' + c.id + '" ' +
            'style="background:' + c.bg + '" title="' + c.label + '" aria-label="' + c.label + '"></button>';
        }).join('') +
        '<span class="sv-hl-divider"></span>' +
        '<button class="sv-hl-icon-btn sv-hl-toggle-note" type="button" title="Add note">' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="13" y2="17"/></svg>' +
        '</button>' +
        '<button class="sv-hl-icon-btn sv-hl-delete" type="button" title="Delete highlight" hidden>' +
          '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-2 14a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="sv-hl-note-row" hidden>' +
        '<textarea class="sv-hl-note" rows="3" maxlength="1000" placeholder="Add a note (optional)…"></textarea>' +
        '<div class="sv-hl-note-actions">' +
          '<button class="sv-hl-btn sv-hl-cancel" type="button">Cancel</button>' +
          '<button class="sv-hl-btn sv-hl-save sv-hl-btn--primary" type="button">Save</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(popoverEl);

    // Swatch click — apply color
    popoverEl.querySelectorAll('.sv-hl-swatch').forEach(function (sw) {
      sw.addEventListener('click', function () {
        var color = sw.getAttribute('data-color');
        applyOrUpdateColor(color);
      });
    });
    // Toggle note row
    popoverEl.querySelector('.sv-hl-toggle-note').addEventListener('click', function () {
      var row = popoverEl.querySelector('.sv-hl-note-row');
      row.hidden = !row.hidden;
      if (!row.hidden) popoverEl.querySelector('.sv-hl-note').focus();
    });
    // Save note
    popoverEl.querySelector('.sv-hl-save').addEventListener('click', function () {
      var note = popoverEl.querySelector('.sv-hl-note').value;
      saveNote(note);
      hidePopover();
    });
    popoverEl.querySelector('.sv-hl-cancel').addEventListener('click', function () {
      hidePopover();
    });
    // Delete
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
    var noteRow = popoverEl.querySelector('.sv-hl-note-row');
    var noteEl = popoverEl.querySelector('.sv-hl-note');
    noteEl.value = opts.note || '';
    noteRow.hidden = !(opts.note && opts.note.length);
    popoverEl.classList.remove('sv-hl-hidden');
    // Position above the selection if there's room, else below
    popoverEl.style.visibility = 'hidden';
    popoverEl.style.display = 'block';
    var ph = popoverEl.offsetHeight;
    var pw = popoverEl.offsetWidth;
    var spaceAbove = rect.top;
    var top, left;
    if (spaceAbove > ph + 12) {
      top = window.scrollY + rect.top - ph - 8;
    } else {
      top = window.scrollY + rect.bottom + 8;
    }
    left = window.scrollX + rect.left + (rect.width / 2) - (pw / 2);
    // Clamp horizontally to viewport
    var maxLeft = window.scrollX + document.documentElement.clientWidth - pw - 12;
    var minLeft = window.scrollX + 12;
    if (left > maxLeft) left = maxLeft;
    if (left < minLeft) left = minLeft;
    popoverEl.style.top = top + 'px';
    popoverEl.style.left = left + 'px';
    popoverEl.style.visibility = 'visible';
  }

  function hidePopover() {
    if (popoverEl) {
      popoverEl.style.display = 'none';
      popoverEl.classList.add('sv-hl-hidden');
    }
    activeHighlight = null;
    pendingRange = null;
    pendingAnchor = null;
  }

  // ---------- create / update / delete flow ----------
  function applyOrUpdateColor(color) {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    if (activeHighlight) {
      // Update existing
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
      // Re-render marks with new color
      var marks = document.querySelectorAll('mark.sv-hl[data-hl-id="' + cssEscape(activeHighlight.id) + '"]');
      marks.forEach(function (m) {
        COLORS.forEach(function (c) { m.classList.remove('sv-hl--' + c.id); });
        m.classList.add('sv-hl--' + color);
        m.setAttribute('data-hl-color', color);
      });
      refreshFab();
    } else if (pendingRange && pendingAnchor) {
      // Create new
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
      if (!marks2.length) {
        console.warn('[highlights] could not wrap range');
        hidePopover();
        return;
      }
      var list2 = getHighlights(lessonId);
      list2.push(hl);
      saveHighlights(lessonId, list2);
      activeHighlight = hl;
      pendingRange = null;
      pendingAnchor = null;
      window.getSelection().removeAllRanges();
      refreshFab();
    }
  }

  function saveNote(note) {
    if (!activeHighlight) return;
    var lessonId = window._lessonId;
    var list = getHighlights(lessonId);
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === activeHighlight.id) {
        list[i].note = (note || '').trim();
        list[i].updatedAt = new Date().toISOString();
        break;
      }
    }
    saveHighlights(lessonId, list);
    // Update mark data attribute
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

  // ---------- selection handling ----------
  function onMouseUp(evt) {
    if (evt.target.closest && evt.target.closest('.sv-hl-popover')) return;
    setTimeout(function () {
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) return;
      var range = sel.getRangeAt(0);
      var container = document.getElementById('study-notes');
      if (!container || !container.contains(range.commonAncestorContainer)) return;
      var text = range.toString();
      if (!text || !text.trim()) return;
      // Refuse selections that are entirely whitespace or just inside an existing mark
      if (text.length > 600) return; // soft cap
      var anchor = buildAnchor(range);
      if (!anchor) return;
      pendingRange = range.cloneRange();
      pendingAnchor = anchor;
      activeHighlight = null;
      showPopoverAt(range.getBoundingClientRect(), { canDelete: false, note: '' });
    }, 10);
  }

  // Capture-phase click handler runs BEFORE the narration jump-to-clip listener
  // that main.js attaches to [data-narration-id] paragraphs. Two responsibilities:
  // (1) open the popover when an existing highlight is clicked
  // (2) suppress the click that follows a drag-selection so narration doesn't fire
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
      showPopoverAt(mark.getBoundingClientRect(), { canDelete: true, note: hl.note || '' });
      return;
    }
    if (justDragged) {
      var sel = window.getSelection();
      if (sel && !sel.isCollapsed && sel.toString().trim().length > 0) {
        evt.stopPropagation();
      }
      justDragged = false;
    }
  }

  // Drag-detection: only suppress narration on real selections, not bare clicks
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

  function onDocClick(evt) {
    if (!popoverEl || popoverEl.style.display === 'none') return;
    if (popoverEl.contains(evt.target)) return;
    if (evt.target.closest && evt.target.closest('mark.sv-hl')) return;
    hidePopover();
  }

  function onKeyDown(evt) {
    if (evt.key === 'Escape') hidePopover();
  }

  // ---------- rehydrate marks on load ----------
  function rehydrate() {
    var lessonId = window._lessonId;
    if (!lessonId) return;
    var list = getHighlights(lessonId);
    var rehydrated = 0;
    for (var i = 0; i < list.length; i++) {
      var hl = list[i];
      try {
        var range = findRangeForAnchor(hl);
        if (range) {
          var marks = wrapRangeInMarks(range, hl);
          if (marks.length) rehydrated++;
        }
      } catch (e) {
        console.warn('[highlights] could not rehydrate', hl.id, e);
      }
    }
    return rehydrated;
  }

  // ---------- floating action button + per-lesson modal ----------
  var fabEl = null;
  var modalEl = null;

  function refreshFab() {
    if (!fabEl) return;
    var n = getHighlights(window._lessonId).length;
    fabEl.querySelector('.sv-hl-fab-count').textContent = n;
    fabEl.style.display = (n > 0) ? 'flex' : 'flex'; // always show; "0" prompts first highlight
    fabEl.classList.toggle('sv-hl-fab--empty', n === 0);
  }

  function buildFab() {
    if (fabEl) return fabEl;
    fabEl = document.createElement('button');
    fabEl.className = 'sv-hl-fab';
    fabEl.type = 'button';
    fabEl.setAttribute('aria-label', 'My highlights');
    fabEl.innerHTML =
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>' +
      '<span class="sv-hl-fab-label">Highlights</span>' +
      '<span class="sv-hl-fab-count">0</span>';
    fabEl.addEventListener('click', openModal);
    document.body.appendChild(fabEl);
    return fabEl;
  }

  function openModal() {
    if (!modalEl) {
      modalEl = document.createElement('div');
      modalEl.className = 'sv-hl-modal';
      modalEl.innerHTML =
        '<div class="sv-hl-modal-backdrop"></div>' +
        '<div class="sv-hl-modal-panel" role="dialog" aria-modal="true" aria-label="My highlights">' +
          '<header class="sv-hl-modal-header">' +
            '<h2>My highlights</h2>' +
            '<a class="sv-hl-modal-allpages" href="/highlights.html">All lessons →</a>' +
            '<button class="sv-hl-modal-close" aria-label="Close">×</button>' +
          '</header>' +
          '<div class="sv-hl-modal-body"></div>' +
        '</div>';
      document.body.appendChild(modalEl);
      modalEl.querySelector('.sv-hl-modal-backdrop').addEventListener('click', closeModal);
      modalEl.querySelector('.sv-hl-modal-close').addEventListener('click', closeModal);
    }
    renderModalBody();
    modalEl.classList.add('sv-hl-modal--open');
  }

  function closeModal() {
    if (modalEl) modalEl.classList.remove('sv-hl-modal--open');
  }

  function renderModalBody() {
    var body = modalEl.querySelector('.sv-hl-modal-body');
    var list = getHighlights(window._lessonId);
    if (!list.length) {
      body.innerHTML =
        '<div class="sv-hl-modal-empty">' +
          '<p>No highlights on this lesson yet.</p>' +
          '<p class="sv-hl-modal-hint">Select any text in the lesson, choose a colour, and optionally write a note.</p>' +
        '</div>';
      return;
    }
    // Newest first
    list.sort(function (a, b) { return (b.createdAt || '').localeCompare(a.createdAt || ''); });
    body.innerHTML = list.map(function (h) {
      var c = colorFor(h.color);
      var noteHtml = h.note
        ? '<p class="sv-hl-modal-note">' + escapeHtml(h.note) + '</p>'
        : '';
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
      'mark.sv-hl{padding:0.05em 0;border-radius:3px;cursor:pointer;transition:filter .15s ease;color:inherit}' +
      'mark.sv-hl:hover{filter:brightness(.96)}' +
      'mark.sv-hl--yellow{background:#fef9c3}' +
      'mark.sv-hl--green{background:#dcfce7}' +
      'mark.sv-hl--pink{background:#fce7f3}' +
      'mark.sv-hl--blue{background:#dbeafe}' +
      'mark.sv-hl[data-hl-has-note]::after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:#2d2a26;vertical-align:super;margin-left:2px;opacity:.6}' +
      'mark.sv-hl--flash{animation:sv-hl-flash 1.4s ease}' +
      '@keyframes sv-hl-flash{0%,100%{box-shadow:0 0 0 0 rgba(45,42,38,0)}30%{box-shadow:0 0 0 6px rgba(45,42,38,.25)}}' +
      // Popover
      '.sv-hl-popover{position:absolute;z-index:9000;background:#fff;border:1px solid rgba(45,42,38,.12);border-radius:14px;box-shadow:0 12px 30px rgba(20,18,15,.18);padding:8px;font-family:Inter,system-ui,sans-serif;color:#2d2a26;min-width:240px}' +
      '.sv-hl-popover-row{display:flex;align-items:center;gap:6px}' +
      '.sv-hl-swatch{width:28px;height:28px;border-radius:50%;border:2px solid rgba(45,42,38,.08);cursor:pointer;padding:0;transition:transform .12s ease,border-color .12s ease}' +
      '.sv-hl-swatch:hover{transform:scale(1.08);border-color:rgba(45,42,38,.3)}' +
      '.sv-hl-divider{width:1px;height:22px;background:rgba(45,42,38,.12);margin:0 2px}' +
      '.sv-hl-icon-btn{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;background:transparent;border:none;border-radius:8px;color:#5d564b;cursor:pointer}' +
      '.sv-hl-icon-btn:hover{background:rgba(45,42,38,.06);color:#2d2a26}' +
      '.sv-hl-note-row{margin-top:8px;display:flex;flex-direction:column;gap:6px}' +
      '.sv-hl-note{width:100%;border:1px solid rgba(45,42,38,.15);border-radius:10px;padding:8px 10px;font-family:inherit;font-size:.92rem;color:inherit;resize:vertical;min-height:64px}' +
      '.sv-hl-note:focus{outline:none;border-color:#2d2a26}' +
      '.sv-hl-note-actions{display:flex;justify-content:flex-end;gap:6px}' +
      '.sv-hl-btn{padding:6px 12px;border-radius:10px;border:1px solid rgba(45,42,38,.15);background:#fff;font-family:inherit;font-size:.86rem;color:#2d2a26;cursor:pointer}' +
      '.sv-hl-btn:hover{background:#faf8f5}' +
      '.sv-hl-btn--primary{background:#2d2a26;color:#faf8f5;border-color:#2d2a26}' +
      '.sv-hl-btn--primary:hover{background:#1f1c19}' +
      // FAB
      '.sv-hl-fab{position:fixed;right:18px;bottom:18px;z-index:8000;display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;background:#2d2a26;color:#faf8f5;border:none;cursor:pointer;box-shadow:0 10px 24px rgba(20,18,15,.25);font-family:Inter,system-ui,sans-serif;font-size:.9rem;font-weight:500}' +
      '.sv-hl-fab:hover{background:#1f1c19}' +
      '.sv-hl-fab-count{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:#faf8f5;color:#2d2a26;font-size:.78rem;font-weight:600}' +
      '.sv-hl-fab--empty .sv-hl-fab-count{background:rgba(250,248,245,.22);color:#faf8f5}' +
      '@media (max-width:640px){.sv-hl-fab-label{display:none}}' +
      // Modal
      '.sv-hl-modal{position:fixed;inset:0;z-index:9500;display:none;align-items:flex-end;justify-content:center}' +
      '.sv-hl-modal--open{display:flex}' +
      '.sv-hl-modal-backdrop{position:absolute;inset:0;background:rgba(20,18,15,.32);backdrop-filter:blur(2px)}' +
      '.sv-hl-modal-panel{position:relative;background:#faf8f5;width:min(640px,100%);max-height:80vh;border-radius:16px 16px 0 0;display:flex;flex-direction:column;box-shadow:0 -20px 48px rgba(20,18,15,.18);font-family:Inter,system-ui,sans-serif;color:#2d2a26}' +
      '@media (min-width:720px){.sv-hl-modal{align-items:center}.sv-hl-modal-panel{border-radius:16px}}' +
      '.sv-hl-modal-header{display:flex;align-items:center;gap:14px;padding:18px 22px;border-bottom:1px solid rgba(45,42,38,.08)}' +
      '.sv-hl-modal-header h2{margin:0;font-size:1.1rem;font-weight:600;flex:1}' +
      '.sv-hl-modal-allpages{font-size:.85rem;color:#5d564b;text-decoration:none}' +
      '.sv-hl-modal-allpages:hover{color:#2d2a26;text-decoration:underline}' +
      '.sv-hl-modal-close{background:transparent;border:none;font-size:1.5rem;line-height:1;color:#5d564b;cursor:pointer;padding:4px 8px;border-radius:8px}' +
      '.sv-hl-modal-close:hover{background:rgba(45,42,38,.06);color:#2d2a26}' +
      '.sv-hl-modal-body{padding:14px 22px 22px;overflow-y:auto;display:flex;flex-direction:column;gap:14px}' +
      '.sv-hl-modal-empty{text-align:center;padding:32px 8px;color:#5d564b}' +
      '.sv-hl-modal-empty p{margin:0 0 6px}' +
      '.sv-hl-modal-hint{font-size:.88rem;color:#7a7367}' +
      '.sv-hl-modal-item{display:flex;flex-direction:column;gap:8px;padding:14px;background:#fff;border-radius:12px;border:1px solid rgba(45,42,38,.06)}' +
      '.sv-hl-modal-snippet{position:relative;padding:10px 12px 10px 16px;border-radius:10px;font-size:.95rem;line-height:1.5}' +
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
    if (!document.getElementById('study-notes')) return; // not on a lesson page
    if (!window._lessonId) {
      // Loader hasn't finished yet — retry a few times
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
    var container = document.getElementById('study-notes');
    container.addEventListener('mousedown', onMouseDownTracker, true);
    container.addEventListener('mousemove', onMouseMoveTracker);
    container.addEventListener('mouseup', onMouseUp);
    // Touch support: long-press handled via native selection, then trigger on selectionchange
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

  window.initHighlightAnnotate = init;

  // Also self-init on DOMContentLoaded for static pages (defensive — main.js calls us too)
  if (document.readyState !== 'loading') {
    setTimeout(init, 50);
  } else {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(init, 50); });
  }
})();
