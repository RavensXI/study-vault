/**
 * Lesson Tutor — a standalone, lesson-grounded Socratic chat.
 *
 * Adds an "Ask the Tutor" card to the lesson sidebar. Opening it shows a chat
 * modal where the student can ask anything about THIS lesson. The tutor coaches
 * Socratically (guiding questions + progressive hints) via /api/tutor, grounded
 * in the lesson content read from the page.
 *
 * Self-contained: injects its own styles, no dependencies. Safe to remove by
 * deleting this file + its <script> tag.
 */
(function () {
  'use strict';

  var conversation = [];   // [{role:'user'|'assistant', content}]
  var greeted = false;
  var sending = false;
  var els = {};

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
      '.tutor-launch{display:flex;align-items:center;gap:0.6rem;width:100%;padding:0.85rem 1rem;border:1px solid var(--border-light,#e8e4df);border-radius:14px;background:var(--accent-light,#f0ece7);color:var(--accent,#2d2a26);font-family:Inter,system-ui,sans-serif;font-size:0.92rem;font-weight:600;cursor:pointer;text-align:left;transition:filter .15s ease,transform .15s ease}',
      '.tutor-launch:hover{filter:brightness(0.97);transform:translateY(-1px)}',
      '.tutor-launch svg{width:20px;height:20px;flex-shrink:0}',
      '.tutor-launch-sub{display:block;font-weight:400;font-size:0.72rem;color:var(--text-muted,#8a8178);margin-top:1px}',
      // overlay + panel
      '.tutor-overlay{position:fixed;inset:0;z-index:9500;display:none;align-items:flex-end;justify-content:center;background:rgba(45,42,38,0.34);backdrop-filter:blur(2px)}',
      '.tutor-overlay.open{display:flex}',
      '.tutor-panel{display:flex;flex-direction:column;width:100%;max-width:560px;height:min(78vh,680px);background:var(--bg-page,#faf8f5);border-radius:18px 18px 0 0;box-shadow:0 -8px 40px rgba(20,18,15,0.22);overflow:hidden;animation:tutorUp .28s cubic-bezier(0.16,1,0.3,1)}',
      '@keyframes tutorUp{from{transform:translateY(24px);opacity:0.4}to{transform:translateY(0);opacity:1}}',
      '@media(min-width:600px){.tutor-overlay{align-items:center}.tutor-panel{border-radius:18px}}',
      '.tutor-head{display:flex;align-items:center;gap:0.6rem;padding:0.85rem 1.1rem;border-bottom:1px solid var(--border-light,#e8e4df);background:#fff}',
      'body.dark-mode .tutor-head{background:#1c1b19}',
      '.tutor-head-icon{width:34px;height:34px;border-radius:50%;background:var(--accent,#2d2a26);color:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0}',
      '.tutor-head-icon svg{width:18px;height:18px}',
      '.tutor-head-title{font-family:Inter,system-ui,sans-serif;font-weight:700;font-size:0.95rem;color:var(--text-primary,#2d2a26);line-height:1.2}',
      '.tutor-head-title small{display:block;font-weight:400;font-size:0.72rem;color:var(--text-muted,#8a8178)}',
      '.tutor-close{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--text-muted,#8a8178);padding:0.3rem;border-radius:8px;line-height:0}',
      '.tutor-close:hover{background:var(--border-light,#e8e4df)}',
      '.tutor-close svg{width:22px;height:22px}',
      '.tutor-log{flex:1;overflow-y:auto;padding:1.1rem;display:flex;flex-direction:column;gap:0.8rem}',
      '.tutor-msg{max-width:85%;padding:0.65rem 0.9rem;border-radius:14px;font-size:0.9rem;line-height:1.5;white-space:pre-wrap;word-wrap:break-word}',
      '.tutor-msg.user{align-self:flex-end;background:var(--accent,#2d2a26);color:#fff;border-bottom-right-radius:4px}',
      '.tutor-msg.bot{align-self:flex-start;background:#fff;color:var(--text-primary,#2d2a26);border:1px solid var(--border-light,#e8e4df);border-bottom-left-radius:4px}',
      'body.dark-mode .tutor-msg.bot{background:#262420;color:#f5f1ec;border-color:#3a3733}',
      '.tutor-typing{align-self:flex-start;display:flex;gap:4px;padding:0.7rem 0.95rem;background:#fff;border:1px solid var(--border-light,#e8e4df);border-radius:14px}',
      'body.dark-mode .tutor-typing{background:#262420;border-color:#3a3733}',
      '.tutor-typing span{width:7px;height:7px;border-radius:50%;background:var(--text-muted,#8a8178);animation:tutorBlink 1.2s infinite ease-in-out}',
      '.tutor-typing span:nth-child(2){animation-delay:0.2s}.tutor-typing span:nth-child(3){animation-delay:0.4s}',
      '@keyframes tutorBlink{0%,80%,100%{opacity:0.3}40%{opacity:1}}',
      '.tutor-input-row{display:flex;gap:0.5rem;padding:0.75rem 0.9rem;border-top:1px solid var(--border-light,#e8e4df);background:#fff}',
      'body.dark-mode .tutor-input-row{background:#1c1b19}',
      '.tutor-input{flex:1;resize:none;border:1px solid var(--border-light,#ddd);border-radius:12px;padding:0.6rem 0.8rem;font-family:inherit;font-size:0.9rem;line-height:1.4;max-height:120px;background:var(--bg-page,#faf8f5);color:var(--text-primary,#2d2a26)}',
      '.tutor-input:focus{outline:none;border-color:var(--accent,#2d2a26)}',
      '.tutor-send{flex-shrink:0;width:42px;border:none;border-radius:12px;background:var(--accent,#2d2a26);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center}',
      '.tutor-send:disabled{opacity:0.45;cursor:default}',
      '.tutor-send svg{width:20px;height:20px}',
      '.tutor-note{font-size:0.68rem;color:var(--text-muted,#8a8178);text-align:center;padding:0 1rem 0.6rem;background:#fff}',
      'body.dark-mode .tutor-note{background:#1c1b19}',
    ].join('\n');
    document.head.appendChild(s);
  }

  function buildPanel() {
    if (els.overlay) return;
    var overlay = document.createElement('div');
    overlay.className = 'tutor-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Lesson tutor chat');
    overlay.innerHTML =
      '<div class="tutor-panel">' +
        '<div class="tutor-head">' +
          '<span class="tutor-head-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>' +
          '<span class="tutor-head-title">Ask the Tutor<small>Here to help you work it out</small></span>' +
          '<button class="tutor-close" aria-label="Close tutor"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>' +
        '</div>' +
        '<div class="tutor-log" id="tutor-log"></div>' +
        '<div class="tutor-input-row">' +
          '<textarea class="tutor-input" id="tutor-input" rows="1" placeholder="Ask about this lesson..."></textarea>' +
          '<button class="tutor-send" id="tutor-send" aria-label="Send"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>' +
        '</div>' +
        '<div class="tutor-note">Your tutor nudges you toward answers rather than giving them away. It can make mistakes — check against the lesson.</div>' +
      '</div>';
    document.body.appendChild(overlay);

    els.overlay = overlay;
    els.log = overlay.querySelector('#tutor-log');
    els.input = overlay.querySelector('#tutor-input');
    els.send = overlay.querySelector('#tutor-send');

    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeTutor(); });
    overlay.querySelector('.tutor-close').addEventListener('click', closeTutor);
    els.send.addEventListener('click', onSend);
    els.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); onSend(); }
    });
    els.input.addEventListener('input', function () {
      els.input.style.height = 'auto';
      els.input.style.height = Math.min(els.input.scrollHeight, 120) + 'px';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && els.overlay.classList.contains('open')) closeTutor();
    });
  }

  function addBubble(role, text) {
    var div = document.createElement('div');
    div.className = 'tutor-msg ' + (role === 'user' ? 'user' : 'bot');
    div.textContent = text;
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
    els.overlay.classList.add('open');
    if (!greeted) {
      greeted = true;
      var ctx = lessonContext();
      addBubble('bot', 'Hi! I’m your tutor for “' + ctx.title + '”. Ask me anything about it — I’ll help you work it out rather than just hand over the answer. What’s on your mind?');
    }
    setTimeout(function () { els.input && els.input.focus(); }, 100);
  }

  function closeTutor() {
    if (els.overlay) els.overlay.classList.remove('open');
  }

  async function onSend() {
    if (sending) return;
    var text = (els.input.value || '').trim();
    if (!text) return;
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
      }
    } catch (err) {
      hideTyping();
      addBubble('bot', 'I couldn’t reach the tutor just now. Check your connection and try again.');
    } finally {
      sending = false;
      els.send.disabled = false;
      els.input.focus();
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

    // Place just after the Quick Quiz card if present, else at the top.
    var kc = sidebar.querySelector('.sidebar-knowledge-check');
    if (kc && kc.nextSibling) sidebar.insertBefore(section, kc.nextSibling);
    else if (kc) sidebar.appendChild(section);
    else sidebar.insertBefore(section, sidebar.firstChild);
    return true;
  }

  // The sidebar is populated asynchronously by lesson-loader. Poll briefly for
  // it (and the lesson content) before injecting the launcher.
  function init() {
    injectStyles();
    var tries = 0;
    var timer = setInterval(function () {
      tries++;
      var notes = document.getElementById('study-notes');
      var ready = notes && notes.textContent.trim().length > 0;
      if (ready && insertLauncher()) { clearInterval(timer); }
      else if (tries > 40) { clearInterval(timer); } // ~20s give-up
    }, 500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
