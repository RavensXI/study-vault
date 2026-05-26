/**
 * Lesson Tutor — a standalone, lesson-grounded Socratic chat.
 *
 * Adds an "Ask the Tutor" card to the lesson sidebar. Opening it shows a
 * FLOATING, DRAGGABLE chat window that does NOT block the page — students can
 * scroll and read the lesson behind it while they type. Drag it by the header.
 *
 * The tutor coaches Socratically (guiding questions + progressive hints) via
 * /api/tutor, grounded in the lesson content read from the page.
 *
 * Self-contained: injects its own styles, no dependencies. Safe to remove by
 * deleting this file + its <script> tag.
 */
(function () {
  'use strict';

  var conversation = [];   // [{role:'user'|'assistant', content}]
  var greeted = false;
  var sending = false;
  var lastPos = null;      // remember dragged position across opens {left, top}
  var els = {};

  // Daily message cap (per-device, per-day localStorage — mirrors the AI-mark
  // limit). Soft by design; the server's per-IP rate limit is the real ceiling.
  var TUTOR_DAILY_LIMIT = 25;
  function todayKey() { return 'sv_tutor_turns_' + new Date().toISOString().slice(0, 10); }
  function usedToday() { try { return parseInt(localStorage.getItem(todayKey()) || '0', 10) || 0; } catch (e) { return 0; } }
  function incToday() { try { localStorage.setItem(todayKey(), String(usedToday() + 1)); } catch (e) {} }
  function remainingToday() { return Math.max(0, TUTOR_DAILY_LIMIT - usedToday()); }
  function updateCount() {
    var left = remainingToday();
    if (els.count) els.count.textContent = left + '/' + TUTOR_DAILY_LIMIT + ' messages left today';
    var none = left <= 0;
    if (els.input) {
      els.input.disabled = none;
      els.input.placeholder = none ? 'Daily limit reached — resets at midnight' : 'Ask about this lesson...';
    }
    if (els.send) els.send.disabled = none || sending;
  }

  function lessonContext() {
    var titleEl = document.getElementById('lesson-title');
    var notesEl = document.getElementById('study-notes');
    var examTip = document.getElementById('exam-tip');
    var conclusion = document.getElementById('conclusion');
    var title = titleEl ? titleEl.textContent.trim() : (document.title || 'this lesson');
    var parts = [];
    if (notesEl) parts.push(notesEl.innerText);
    if (examTip && examTip.style.display !== 'none') parts.push('Exam tip: ' + examTip.innerText);
    if (conclusion && conclusion.style.display !== 'none') parts.push(conclusion.innerText);
    return { title: title, text: parts.join('\n\n').replace(/\n{3,}/g, '\n\n').trim().slice(0, 9000) };
  }

  function injectStyles() {
    if (document.getElementById('lesson-tutor-styles')) return;
    var s = document.createElement('style');
    s.id = 'lesson-tutor-styles';
    s.textContent = [
      // Launcher card (sidebar)
      '.tutor-launch{display:flex;align-items:center;gap:0.6rem;width:100%;padding:0.85rem 1rem;border:1px solid var(--border-light,#e8e4df);border-radius:14px;background:var(--accent-light,#f0ece7);color:var(--accent,#2d2a26);font-family:Inter,system-ui,sans-serif;font-size:0.92rem;font-weight:600;cursor:pointer;text-align:left;transition:filter .15s ease,transform .15s ease}',
      '.tutor-launch:hover{filter:brightness(0.97);transform:translateY(-1px)}',
      '.tutor-launch svg{width:20px;height:20px;flex-shrink:0}',
      '.tutor-launch-sub{display:block;font-weight:400;font-size:0.72rem;color:var(--text-muted,#8a8178);margin-top:1px}',
      // Floating, draggable, NON-blocking panel — no backdrop, page stays interactive.
      '.tutor-panel{position:fixed;right:24px;bottom:24px;left:auto;top:auto;z-index:9500;display:none;flex-direction:column;width:min(380px,calc(100vw - 24px));height:min(70vh,560px);background:var(--bg-page,#faf8f5);border:1px solid var(--border-light,#e3ddd5);border-radius:16px;box-shadow:0 12px 48px rgba(20,18,15,0.28);overflow:hidden}',
      '.tutor-panel.open{display:flex;animation:tutorPop .22s cubic-bezier(0.16,1,0.3,1)}',
      '@keyframes tutorPop{from{transform:translateY(12px) scale(0.98);opacity:0.4}to{transform:translateY(0) scale(1);opacity:1}}',
      'body.dark-mode .tutor-panel{background:#1c1b19;border-color:#3a3733}',
      // Header doubles as the drag handle
      '.tutor-head{display:flex;align-items:center;gap:0.6rem;padding:0.7rem 0.9rem;border-bottom:1px solid var(--border-light,#e8e4df);background:#fff;cursor:move;user-select:none;touch-action:none}',
      'body.dark-mode .tutor-head{background:#262420}',
      '.tutor-grip{display:flex;flex-direction:column;gap:3px;flex-shrink:0;opacity:0.4}',
      '.tutor-grip i{display:block;width:14px;height:2px;border-radius:2px;background:currentColor}',
      '.tutor-head-icon{width:32px;height:32px;border-radius:50%;background:var(--accent,#2d2a26);color:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0}',
      '.tutor-head-icon svg{width:17px;height:17px}',
      '.tutor-head-title{font-family:Inter,system-ui,sans-serif;font-weight:700;font-size:0.92rem;color:var(--text-primary,#2d2a26);line-height:1.2}',
      '.tutor-head-title small{display:block;font-weight:400;font-size:0.7rem;color:var(--text-muted,#8a8178)}',
      '.tutor-close{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--text-muted,#8a8178);padding:0.3rem;border-radius:8px;line-height:0}',
      '.tutor-close:hover{background:var(--border-light,#e8e4df)}',
      '.tutor-close svg{width:20px;height:20px}',
      '.tutor-log{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:0.7rem}',
      '.tutor-msg{max-width:88%;padding:0.6rem 0.85rem;border-radius:14px;font-size:0.88rem;line-height:1.5;white-space:pre-wrap;word-wrap:break-word}',
      '.tutor-msg.user{align-self:flex-end;background:var(--accent,#2d2a26);color:#fff;border-bottom-right-radius:4px}',
      '.tutor-msg.bot{align-self:flex-start;background:#fff;color:var(--text-primary,#2d2a26);border:1px solid var(--border-light,#e8e4df);border-bottom-left-radius:4px}',
      'body.dark-mode .tutor-msg.bot{background:#262420;color:#f5f1ec;border-color:#3a3733}',
      '.tutor-msg.bot p{margin:0 0 0.5em}.tutor-msg.bot p:last-child{margin-bottom:0}',
      '.tutor-msg.bot strong{font-weight:700}',
      '.tutor-msg.bot ul{margin:0.3em 0 0.5em;padding-left:1.15em}.tutor-msg.bot li{margin:0.15em 0}',
      '.tutor-msg.bot code{background:rgba(0,0,0,0.06);padding:0.05em 0.3em;border-radius:5px;font-size:0.9em}',
      'body.dark-mode .tutor-msg.bot code{background:rgba(255,255,255,0.1)}',
      '.tutor-typing{align-self:flex-start;display:flex;gap:4px;padding:0.65rem 0.9rem;background:#fff;border:1px solid var(--border-light,#e8e4df);border-radius:14px}',
      'body.dark-mode .tutor-typing{background:#262420;border-color:#3a3733}',
      '.tutor-typing span{width:7px;height:7px;border-radius:50%;background:var(--text-muted,#8a8178);animation:tutorBlink 1.2s infinite ease-in-out}',
      '.tutor-typing span:nth-child(2){animation-delay:0.2s}.tutor-typing span:nth-child(3){animation-delay:0.4s}',
      '@keyframes tutorBlink{0%,80%,100%{opacity:0.3}40%{opacity:1}}',
      '.tutor-input-row{display:flex;gap:0.5rem;padding:0.7rem 0.8rem;border-top:1px solid var(--border-light,#e8e4df);background:#fff}',
      'body.dark-mode .tutor-input-row{background:#1c1b19}',
      '.tutor-input{flex:1;resize:none;border:1px solid var(--border-light,#ddd);border-radius:12px;padding:0.55rem 0.75rem;font-family:inherit;font-size:0.88rem;line-height:1.4;max-height:110px;background:var(--bg-page,#faf8f5);color:var(--text-primary,#2d2a26)}',
      '.tutor-input:focus{outline:none;border-color:var(--accent,#2d2a26)}',
      '.tutor-send{flex-shrink:0;width:40px;border:none;border-radius:12px;background:var(--accent,#2d2a26);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center}',
      '.tutor-send:disabled{opacity:0.45;cursor:default}',
      '.tutor-send svg{width:19px;height:19px}',
      '.tutor-note{font-size:0.66rem;color:var(--text-muted,#8a8178);text-align:center;padding:0 0.9rem 0.55rem;background:#fff}',
      'body.dark-mode .tutor-note{background:#1c1b19}',
    ].join('\n');
    document.head.appendChild(s);
  }

  function buildPanel() {
    if (els.panel) return;
    var panel = document.createElement('div');
    panel.className = 'tutor-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Lesson tutor chat');
    panel.innerHTML =
      '<div class="tutor-head" id="tutor-head" title="Drag to move">' +
        '<span class="tutor-grip" aria-hidden="true"><i></i><i></i></span>' +
        '<span class="tutor-head-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>' +
        '<span class="tutor-head-title">Ask the Tutor<small>Drag me &middot; the lesson stays clickable</small></span>' +
        '<button class="tutor-close" aria-label="Close tutor"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>' +
      '</div>' +
      '<div class="tutor-log" id="tutor-log"></div>' +
      '<div class="tutor-input-row">' +
        '<textarea class="tutor-input" id="tutor-input" rows="1" placeholder="Ask about this lesson..."></textarea>' +
        '<button class="tutor-send" id="tutor-send" aria-label="Send"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>' +
      '</div>' +
      '<div class="tutor-note">Your tutor nudges you toward answers rather than giving them away. It can make mistakes — check against the lesson.</div>';
    document.body.appendChild(panel);

    els.panel = panel;
    els.log = panel.querySelector('#tutor-log');
    els.input = panel.querySelector('#tutor-input');
    els.send = panel.querySelector('#tutor-send');
    els.count = panel.querySelector('.tutor-head-title small');

    panel.querySelector('.tutor-close').addEventListener('click', closeTutor);
    els.send.addEventListener('click', onSend);
    els.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); onSend(); }
    });
    els.input.addEventListener('input', function () {
      els.input.style.height = 'auto';
      els.input.style.height = Math.min(els.input.scrollHeight, 110) + 'px';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && els.panel.classList.contains('open')) closeTutor();
    });

    makeDraggable(panel, panel.querySelector('#tutor-head'));
  }

  // Drag the panel by its header. Switches positioning to left/top on first
  // grab, clamps to the viewport, and remembers the position across opens.
  function makeDraggable(panel, handle) {
    var dragging = false, sx = 0, sy = 0, startLeft = 0, startTop = 0;
    function point(e) { return e.touches && e.touches[0] ? e.touches[0] : e; }
    function down(e) {
      if (e.target.closest('.tutor-close')) return;
      var pt = point(e);
      var rect = panel.getBoundingClientRect();
      panel.style.left = rect.left + 'px';
      panel.style.top = rect.top + 'px';
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
      startLeft = rect.left; startTop = rect.top;
      sx = pt.clientX; sy = pt.clientY;
      dragging = true;
      document.addEventListener('mousemove', move);
      document.addEventListener('mouseup', up);
      document.addEventListener('touchmove', move, { passive: false });
      document.addEventListener('touchend', up);
      if (e.cancelable) e.preventDefault();
    }
    function move(e) {
      if (!dragging) return;
      var pt = point(e);
      var w = panel.offsetWidth, h = panel.offsetHeight;
      var nl = Math.max(8, Math.min(startLeft + (pt.clientX - sx), window.innerWidth - w - 8));
      var nt = Math.max(8, Math.min(startTop + (pt.clientY - sy), window.innerHeight - h - 8));
      panel.style.left = nl + 'px';
      panel.style.top = nt + 'px';
      if (e.cancelable) e.preventDefault();
    }
    function up() {
      if (!dragging) return;
      dragging = false;
      document.removeEventListener('mousemove', move);
      document.removeEventListener('mouseup', up);
      document.removeEventListener('touchmove', move);
      document.removeEventListener('touchend', up);
      lastPos = { left: panel.style.left, top: panel.style.top };
    }
    handle.addEventListener('mousedown', down);
    handle.addEventListener('touchstart', down, { passive: false });
  }

  // Minimal, XSS-safe markdown for the tutor's replies. Escape first, then only
  // emit a fixed set of tags (strong/em/code/p/ul/li/br) — the model likes to
  // bold key terms and use the odd short list, so we render that rather than
  // fight it in the prompt.
  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function renderMarkdown(src) {
    var t = escapeHtml(src);
    t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
    t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    t = t.replace(/(^|[^*])\*(?!\s)([^*\n]+?)\*/g, '$1<em>$2</em>');
    var lines = t.split('\n');
    var html = '';
    var para = [];
    function flush() { if (para.length) { html += '<p>' + para.join('<br>') + '</p>'; para = []; } }
    for (var i = 0; i < lines.length; i++) {
      if (/^\s*[-*]\s+/.test(lines[i])) {
        flush();
        var items = '';
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          items += '<li>' + lines[i].replace(/^\s*[-*]\s+/, '') + '</li>';
          i++;
        }
        i--;
        html += '<ul>' + items + '</ul>';
      } else if (lines[i].trim() === '') {
        flush();
      } else {
        para.push(lines[i]);
      }
    }
    flush();
    return html;
  }

  function addBubble(role, text) {
    var div = document.createElement('div');
    div.className = 'tutor-msg ' + (role === 'user' ? 'user' : 'bot');
    if (role === 'user') div.textContent = text;
    else div.innerHTML = renderMarkdown(text);
    els.log.appendChild(div);
    els.log.scrollTop = els.log.scrollHeight;
    return div;
  }

  function showTyping() {
    var t = document.createElement('div');
    t.className = 'tutor-typing';
    t.id = 'tutor-typing';
    t.innerHTML = '<span></span><span></span><span></span>';
    els.log.appendChild(t);
    els.log.scrollTop = els.log.scrollHeight;
  }
  function hideTyping() {
    var t = document.getElementById('tutor-typing');
    if (t) t.remove();
  }

  function openTutor() {
    buildPanel();
    els.panel.classList.add('open');
    // Restore the last dragged position if the student moved it before.
    if (lastPos) {
      els.panel.style.left = lastPos.left;
      els.panel.style.top = lastPos.top;
      els.panel.style.right = 'auto';
      els.panel.style.bottom = 'auto';
    }
    if (!greeted) {
      greeted = true;
      var ctx = lessonContext();
      addBubble('bot', 'Hi! I’m your tutor for “' + ctx.title + '”. Ask me anything about it — I’ll help you work it out rather than just hand over the answer. What’s on your mind?');
    }
    updateCount();
    setTimeout(function () { if (els.input && !els.input.disabled) els.input.focus(); }, 100);
  }

  function closeTutor() {
    if (els.panel) els.panel.classList.remove('open');
  }

  async function onSend() {
    if (sending) return;
    var text = (els.input.value || '').trim();
    if (!text) return;
    if (remainingToday() <= 0) {
      addBubble('bot', 'That’s all your tutor messages for today — they reset at midnight. You can still read the lesson and use everything else. See you tomorrow!');
      updateCount();
      return;
    }
    els.input.value = '';
    els.input.style.height = 'auto';
    addBubble('user', text);
    conversation.push({ role: 'user', content: text });

    sending = true;
    els.send.disabled = true;
    showTyping();

    var ctx = lessonContext();
    try {
      var resp = await fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lessonTitle: ctx.title, lessonText: ctx.text, messages: conversation }),
      });
      hideTyping();
      var data = await resp.json().catch(function () { return {}; });
      if (!resp.ok) {
        addBubble('bot', data.error || 'Sorry, I had trouble responding. Try again in a moment.');
      } else {
        var reply = (data.reply || '').trim() || 'Sorry, I didn’t catch that — could you rephrase?';
        addBubble('bot', reply);
        conversation.push({ role: 'assistant', content: reply });
        incToday();   // count a turn only when the tutor actually answered
      }
    } catch (err) {
      hideTyping();
      addBubble('bot', 'I couldn’t reach the tutor just now. Check your connection and try again.');
    } finally {
      sending = false;
      updateCount();
      if (els.input && !els.input.disabled) els.input.focus();
    }
  }

  function insertLauncher() {
    var sidebar = document.querySelector('.lesson-sidebar');
    if (!sidebar || document.querySelector('.tutor-launch')) return false;

    var section = document.createElement('div');
    section.className = 'sidebar-section sidebar-tutor';
    section.innerHTML =
      '<button class="tutor-launch" type="button">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' +
        '<span>Ask the Tutor<span class="tutor-launch-sub">Stuck? Get a Socratic hint</span></span>' +
      '</button>';
    section.querySelector('.tutor-launch').addEventListener('click', openTutor);

    var kc = sidebar.querySelector('.sidebar-knowledge-check');
    if (kc && kc.nextSibling) sidebar.insertBefore(section, kc.nextSibling);
    else if (kc) sidebar.appendChild(section);
    else sidebar.insertBefore(section, sidebar.firstChild);
    return true;
  }

  function init() {
    injectStyles();
    var tries = 0;
    var timer = setInterval(function () {
      tries++;
      var notes = document.getElementById('study-notes');
      var ready = notes && notes.textContent.trim().length > 0;
      if (ready && insertLauncher()) { clearInterval(timer); }
      else if (tries > 40) { clearInterval(timer); }
    }, 500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
